import argparse

from cli.topology import register_topology_parser
from cli.node import register_node_parser
from cli.replay import register_replay_parser


def build_parser():
    parser = argparse.ArgumentParser(prog="pcc", description="PCC Simulator CLI")
    subparsers = parser.add_subparsers(dest="command")

    register_topology_parser(subparsers)
    register_node_parser(subparsers)
    register_replay_parser(subparsers)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
