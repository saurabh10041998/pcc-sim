from services.topology_service import TopologyService

service = TopologyService()


def register_topology_parser(subparsers):
    topology_parser = subparsers.add_parser("topology", help="toplogy management")

    topology_subparsers = topology_parser.add_subparsers(dest="topology_command")

    create_parser = topology_subparsers.add_parser("create", help="Create a topology")
    create_parser.add_argument("--name", required=True, help="Name of the topology")
    create_parser.add_argument("--bridge", default="br-pcep")
    create_parser.add_argument("--subnet", default="10.66.3.0/24")

    create_parser.set_defaults(func=create_topology)

    delete_parser = topology_subparsers.add_parser("delete", help="Delete a topology")
    delete_parser.set_defaults(func=delete_topology)

    show_parser = topology_subparsers.add_parser("show", help="Show topology details")
    show_parser.set_defaults(func=show_topology)


def create_topology(args):
    service.create_topology(name=args.name, bridge=args.bridge, subnet=args.subnet)

    print(f"Topology '{args.name}' created")


def delete_topology(args):
    service.delete_topology()
    print(f"Topology deleted")


def show_topology(args):
    topology = service.get_topology()

    print(f"Topology Name: {topology.name}")
    print(f"Bridge: {topology.bridge}")
    print(f"Subnet: {topology.subnet}")
    print("Nodes:")
    for node in topology.list_nodes():
        print(f"  - {node.name} ({node.ip})")
