from typing import Dict
from scapy.all import *

from core.node import PCCNode
from core.replay.rewrite import PacketRewriter
from utils.shell import exec_in_namespace

# acks
ACK = 0x10
# client closing the connection
RSTACK = 0x14


def get_tcp_payload_length(p):
    if str(p[TCP].flags) == "SA":
        return 1
    ip_total_len = p.getlayer(IP).len
    ip_header_len = p.getlayer(IP).ihl * 32 // 8
    tcp_header_len = p.getlayer(TCP).dataofs * 32 // 8
    return ip_total_len - ip_header_len - tcp_header_len


class ReplayEngine:
    def __init__(self, pcap: str, rewrite_rules: Dict[str, str]):
        self.pcap = pcap
        self.attached_node = None
        self.rewriter = PacketRewriter(rewrite_rules)
        self.recv_seq_num = 0
        self.recv_payload_len = 0

    def attach_node(self, node: PCCNode):
        self.attached_node = node

    def start(self):
        if not self.attached_node:
            raise RuntimeError("No node attached to replay engine")

        # apply the iptables rule inside nodes namespace
        src_ip = self.attached_node.ip
        dst_ip = self.rewriter.rules.get("dst_ip", src_ip)
        dport = int(self.rewriter.rules.get("dst_port"))

        exec_in_namespace(
            self.attached_node.namespace,
            f"iptables -A OUTPUT -p tcp --tcp-flags RST RST -s {src_ip} -d {dst_ip} --dport {dport} -j DROP",
        )

        valid_packets = []

        for packet in self._read_pcap():
            if IP in packet and TCP in packet and packet[TCP].dport == dport:
                modified_packet = self.rewriter.apply(packet)
                if (modified_packet[TCP].flags & ACK) or (
                    modified_packet[TCP].flags & RSTACK
                ):
                    if self.recv_seq_num >= 0 and self.recv_payload_len >= 0:
                        modified_packet[TCP].ack = (
                            self.recv_seq_num + self.recv_payload_len
                        )

                valid_packets.append(modified_packet)
            else:
                if valid_packets:
                    self.send_packets(valid_packets)
                valid_packets = []
        else:
            if valid_packets:
                self.send_packets(valid_packets)

    def stop(self):
        if not self.attached_node:
            return

        src_ip = self.attached_node.ip
        dst_ip = self.rewriter.rules.get("dst_ip", src_ip)
        dport = int(self.rewriter.rules.get("dst_port"))

        exec_in_namespace(
            self.attached_node.namespace,
            f"iptables -D OUTPUT -p tcp --tcp-flags RST RST -s {src_ip} -d {dst_ip} --dport {dport} -j DROP",
        )

    def _read_pcap(self):
        try:
            packets = rdpcap(self.pcap)
            return packets
        except Exception as e:
            raise RuntimeError(f"Failed to read PCAP file: {e}")

    def send_packets(self, packets):
        rcv, _ = sr(packets, multi=True, timeout=5)
        self.recv_seq_num = -1
        self.recv_payload_len = -1
        if rcv:
            for idx in range(len(rcv)):
                received_packet = cast(Packet, rcv[idx][1])
                received_packet.show()
                if "TCP" in received_packet:
                    if received_packet[TCP].seq >= 0:
                        self.recv_seq_num = received_packet[TCP].seq
                        self.recv_payload_len = get_tcp_payload_length(received_packet)
