from typing import List, Dict
from services.replay_service import ReplayService


replay_service = ReplayService()


def parse_rewrite_rules(rules: List[str]) -> Dict[str, str]:
    rewrite_dict = {}
    for rule in rules:
        if "=" not in rule:
            raise ValueError(f"Invalid rewrite rule format: '{rule}'")
        key, value = rule.split("=", 1)
        rewrite_dict[key] = value
    return rewrite_dict


def register_replay_parser(subparsers):
    replay_parser = subparsers.add_parser(
        "replay", help="Replay recorded pcap file for PCCNode"
    )
    replay_subparsers = replay_parser.add_subparsers(dest="replay_command")
    start_parser = replay_subparsers.add_parser("start", help="Start pcap replay")
    start_parser.add_argument("--node", required=True)
    start_parser.add_argument("--pcap", required=True)
    start_parser.add_argument(
        "--rewrite", action="append", help="rewrite rule format key=value"
    )
    start_parser.set_defaults(func=replay_pcap)


def replay_pcap(args):
    rewrite_rules = parse_rewrite_rules(args.rewrite) if args.rewrite else {}
    replay_service.start(node=args.node, pcap=args.pcap, rewrite_rules=rewrite_rules)
