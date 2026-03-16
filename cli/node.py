from services.node_service import NodeService

service = NodeService()


def register_node_parser(subparsers):
    node_parser = subparsers.add_parser("node", help="PCC node management")

    node_subparsers = node_parser.add_subparsers(dest="node_command")
    add_parser = node_subparsers.add_parser("add", help="Add a node to the topology")

    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--ip", required=True)
    add_parser.add_argument("--namespace", required=True)
    add_parser.add_argument("--iface", default="eth1")
    add_parser.set_defaults(func=add_node)

    delete_parser = node_subparsers.add_parser(
        "delete", help="Delete PCC node from topology"
    )
    delete_parser.add_argument("name")
    delete_parser.set_defaults(func=delete_node)

    list_parser = node_subparsers.add_parser("list", help="List nodes")
    list_parser.set_defaults(func=list_nodes)

    shell_parser = node_subparsers.add_parser("shell", help="Enter namespace shell")
    shell_parser.add_argument("name")
    shell_parser.set_defaults(func=shell_node)


def add_node(args):
    service.add_node(
        name=args.name, ip=args.ip, namespace=args.namespace, iface=args.iface
    )
    print(f"Node '{args.name}' added to topology")


def delete_node(args):
    service.delete_node(name=args.name)
    print(f"Node '{args.name}' deleted from topology")


def list_nodes(args):
    nodes = service.list_nodes()
    if not nodes:
        print("No nodes in topology")
        return

    print("Nodes in topology:")
    for node in nodes:
        print(f"  - {node.name}\t({node.namespace})\t({node.ip})")


def shell_node(args):
    service.shell_node(name=args.name)
