from dataclasses import dataclass, field
from typing import Dict, Optional

from core.node import PCCNode


@dataclass
class Topology:
    name: str
    bridge: str
    subnet: str

    nodes: Dict[str, PCCNode] = field(default_factory=dict)

    def add_node(self, node: PCCNode) -> None:
        if node.name in self.nodes:
            raise ValueError(
                f"Node with name {node.name} already exists in topology {self.name}"
            )

        self.nodes[node.name] = node

    def remove_node(self, node_name: str) -> None:
        if node_name not in self.nodes:
            raise ValueError(
                f"Node with name {node_name} does not exist in topology {self.name}"
            )

        del self.nodes[node_name]

    def get_node(self, node_name: str) -> Optional[PCCNode]:
        return self.nodes.get(node_name)

    def list_nodes(self) -> Dict[str, PCCNode]:
        return list(self.nodes.values())

    def has_node(self, node_name: str) -> bool:
        return node_name in self.nodes
