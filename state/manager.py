import json
from pathlib import Path

from core.topology import Topology
from core.node import PCCNode


STATE_DIR = Path.home() / ".pcc-sim"
STATE_FILE = STATE_DIR / "state.json"


class StateManager:
    def __init__(self):
        STATE_DIR.mkdir(exist_ok=True)

    def _load_raw(self):
        if not STATE_FILE.exists():
            return None

        with open(STATE_FILE, "r") as f:
            return json.load(f)

    def _save_raw(self, data):
        with open(STATE_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def topology_exists(self) -> bool:
        data = self._load_raw()
        return data is not None and "topology" in data

    def save_topology(self, topology: Topology):
        data = {
            "topology": {
                "name": topology.name,
                "bridge": topology.bridge,
                "subnet": topology.subnet,
                "nodes": [
                    {
                        "name": node.name,
                        "namespace": node.namespace,
                        "ip": node.ip,
                        "iface": node.iface,
                    }
                    for node in topology.list_nodes()
                ],
            }
        }
        self._save_raw(data)

    def load_topology(self) -> Topology:
        data = self._load_raw()
        if not data or "topology" not in data:
            return None

        topo_data = data["topology"]
        topology = Topology(
            name=topo_data["name"],
            bridge=topo_data["bridge"],
            subnet=topo_data["subnet"],
        )

        for node_data in topo_data.get("nodes", []):
            node = PCCNode(
                name=node_data["name"],
                namespace=node_data["namespace"],
                ip=node_data["ip"],
                iface=node_data.get("iface", "eth1"),
            )
            topology.add_node(node)

        return topology

    def clear_topology(self):
        if STATE_FILE.exists():
            STATE_FILE.unlink()
