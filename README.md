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

### Examples
Create the topology
```bash
pcc topology create --name test --bridge br-test --subnet '10.66.3.0/24'
```

Create a node
```bash
pcc node add --name pcc1 --namespace pcc1 --ip 10.66.3.154
```

Replay for a node
```bash
pcc node shell pcc1   # switch to pcc1 namespace
pcc replay start --node pcc1 --pcap sample.pcap --rewrite 'dst_ip=10.190.201.192' --rewrite 'src_port=9002' --rewrite 'dst_port=4189' 
```

List node
```bash
pcc node list
```

Show topology
```bash
pcc topology show
```

Delete the node
```bash
pcc node delete pcc1
```

Delete topology
```bash
pcc topology delete
```