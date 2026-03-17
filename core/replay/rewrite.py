from scapy.all import IP, TCP, UDP


class PacketRewriter:
    def __init__(self, rules: Dict[str, str]):
        self.rules = rules

    def apply(self, packet):
        if IP in packet:
            if "src_ip" in self.rules:
                packet[IP].src = self.rules["src_ip"]

            if "dst_ip" in self.rules:
                packet[IP].dst = self.rules["dst_ip"]

        if TCP in packet:
            if "src_port" in self.rules:
                packet[TCP].sport = int(self.rules["src_port"])

            if "dst_port" in self.rules:
                packet[TCP].dport = int(self.rules["dst_port"])

        if UDP in packet:
            if "src_port" in self.rules:
                packet[UDP].sport = int(self.rules["src_port"])

            if "dst_port" in self.rules:
                packet[UDP].dport = int(self.rules["dst_port"])

        self._fix_checksums(packet)
        return packet

    def _fix_checksums(self, packet):
        if IP in packet:
            del packet[IP].chksum

        if TCP in packet:
            del packet[TCP].chksum

        if UDP in packet:
            del packet[UDP].chksum
