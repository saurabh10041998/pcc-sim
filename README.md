### project structure
```bash
pcc-sim
│
├── main.py                 # entrypoint
│
├── cli/                    # CLI command definitions
│   ├── __init__.py
│   ├── main.py             # Typer root app
│   ├── topology.py         # topology commands
│   ├── node.py             # node commands
│   └── replay.py           # replay commands
│
├── services/               # orchestration layer (recommended)
│   ├── __init__.py
│   ├── topology_service.py
│   ├── node_service.py
│   └── replay_service.py
│
├── core/                   # domain objects
│   ├── __init__.py
│   ├── topology.py         # Topology class
│   ├── node.py             # PCCNode abstraction
│   └── runtime.py          # runtime lifecycle manager
│
├── state/                  # persistent lab state
│   ├── __init__.py
│   ├── store.py            # load/save state
│   ├── manager.py          # modify state safely
│   └── models.py           # dataclasses / pydantic models
│
├── network/                # networking infrastructure
│   ├── __init__.py
│   ├── namespace.py
│   ├── veth.py
│   ├── bridge.py
│   └── ipam.py             # IP allocation
│
├── replay/                 # packet replay
│   ├── __init__.py
│   ├── engine.py           # PCAP replay
│   ├── scheduler.py        # replay timing
│   └── rewrite.py          # packet rewriting
│
├── protocol/               # protocol implementation
│   └── pcep/
│       ├── __init__.py
│       ├── parser.py
│       ├── messages.py
│       ├── session.py
│       └── automata.py
│
├── config/
│   ├── defaults.py
│   └── topology_loader.py
│
├── utils/
│   ├── __init__.py
│   ├── shell.py
│   ├── logging.py
│   └── errors.py
│
└── tests/
    ├── test_topology.py
    ├── test_node.py
    └── test_replay.py

```