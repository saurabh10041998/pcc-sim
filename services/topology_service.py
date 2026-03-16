from core.topology import Topology
from network.bridge import create_bridge, delete_bridge
from state.manager import StateManager


class TopologyService:
    def __init__(self):
        self.state = StateManager()

    def create_topology(self, name: str, bridge: str, subnet: str) -> Topology:
        if self.state.topology_exists():
            raise RuntimeError("Topology already exists")

        network_gateway = subnet.split("/")[0][:-1] + "1"

        create_bridge(bridge, network_gateway)
        topology = Topology(name=name, bridge=bridge, subnet=subnet)
        self.state.save_topology(topology)
        return topology

    def delete_topology(self):
        topology = self.state.load_topology()

        if not topology:
            raise RuntimeError("No topology exists to delete")

        from services.node_service import NodeService

        node_service = NodeService()

        for node in topology.list_nodes():
            node_service.delete_node(node.name)

        delete_bridge(topology.bridge)
        self.state.clear_topology()

    def get_topology(self):
        topology = self.state.load_topology()

        if topology is None:
            raise RuntimeError("No topology exists")

        return topology

    def list_nodes(self):
        topology = self.ensure_topology()
        return topology.list_nodes()

    def ensure_topology(self) -> Topology:
        topology = self.state.load_topology()

        if topology is None:
            raise RuntimeError("No topology exists")

        return topology

    def register_node(self, node):
        topology = self.ensure_topology()
        topology.add_node(node)
        self.state.save_topology(topology)

    def unregister_node(self, node_name):
        topology = self.ensure_topology()
        topology.remove_node(node_name)
        self.state.save_topology(topology)
