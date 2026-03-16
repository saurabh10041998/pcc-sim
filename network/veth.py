import subprocess


def create_veth_pair(veth_host, veth_ns, namespace):
    subprocess.run(
        ["ip", "link", "add", veth_host, "type", "veth", "peer", "name", veth_ns],
        check=True,
    )
    subprocess.run(["ip", "link", "set", veth_ns, "netns", namespace], check=True)


def attach_to_bridge(veth_host, bridge_name):
    subprocess.run(["ip", "link", "set", veth_host, "master", bridge_name], check=True)
    subprocess.run(["ip", "link", "set", veth_host, "up"], check=True)
