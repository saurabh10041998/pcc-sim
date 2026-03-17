from core.node import PCCNode
from services.topology_service import TopologyService

from network.namespace import create_namespace, delete_namespace
from network.veth import create_veth_pair, attach_to_bridge
from utils.shell import exec_in_namespace


class NodeService:
    def __init__(self):
        self.topology_service = TopologyService()

    def add_node(self, name: str, ip: str, namespace: str, iface: str):
        topology = self.topology_service.ensure_topology()

        if topology.has_node(name):
            raise ValueError(f"Node with name {name} already exists")

        create_namespace(namespace)

        veth_host = f"veth-{name}"
        veth_peer = iface
        gateway_ip = topology.subnet.split("/")[0][:-1] + "1"

        create_veth_pair(veth_host, veth_peer, namespace)
        attach_to_bridge(veth_host, topology.bridge)

        exec_in_namespace(namespace, f"ip addr add {ip}/24 dev {veth_peer}")
        exec_in_namespace(namespace, f"ip link set {veth_peer} up")
        exec_in_namespace(namespace, f"ip link set lo up")
        exec_in_namespace(namespace, f"ip route add default via {gateway_ip}")

        node = PCCNode(name=name, namespace=namespace, ip=ip, iface=iface)
        self.topology_service.register_node(node)
        return node

    def delete_node(self, name: str):
        topology = self.topology_service.ensure_topology()
        node = topology.get_node(name)

        if not node:
            raise ValueError(f"Node '{name}' not found")

        delete_namespace(node.namespace)

        self.topology_service.unregister_node(node.name)

    def list_nodes(self):
        topology = self.topology_service.ensure_topology()
        return topology.list_nodes()

    def get_node(self, name: str):
        topology = self.topology_service.ensure_topology()
        node = topology.get_node(name)

        if not node:
            raise ValueError(f"Node '{name}' not found")

        return node

    def shell_node(self, name: str):
        node = self.get_node(name)
        exec_in_namespace(node.namespace, "su - toor")
