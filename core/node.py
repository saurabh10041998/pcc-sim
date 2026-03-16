from dataclasses import dataclass


@dataclass
class PCCNode:
    name: str
    namespace: str
    ip: str
    iface: str = "eth1"
