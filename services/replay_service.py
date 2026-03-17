import os
from typing import Dict

from core.replay.engine import ReplayEngine
from state.manager import StateManager
from utils.shell import exec_in_namespace


class ReplayService:
    def __init__(self):
        self.state_manager = StateManager()

    def start(self, node: str, pcap: str, rewrite_rules: Dict[str, str]):
        if not os.path.isfile(pcap):
            raise ValueError(f"PCAP file '{pcap}' does not exist")

        topology = self.state_manager.load_topology()
        pcc_node = topology.get_node(node)
        if not pcc_node:
            raise ValueError(f"Node '{node}' not found in topology")

        engine = ReplayEngine(pcap=pcap, rewrite_rules=rewrite_rules)

        engine.attach_node(pcc_node)
        try:
            engine.start()
        except Exception as e:
            raise RuntimeError(f"Failed to start replay engine: {e}")
        finally:
            engine.stop()
