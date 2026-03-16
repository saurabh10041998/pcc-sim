import subprocess


def create_bridge(bridge_name, gateway_ip):
    result = subprocess.run(["ip", "link", "show", bridge_name], capture_output=True)
    if result.returncode == 0:
        print(f"Bridge '{bridge_name}' already exists")
        return

    subprocess.run(["ip", "link", "add", bridge_name, "type", "bridge"], check=True)
    subprocess.run(["ip", "addr", "add", gateway_ip, "dev", bridge_name], check=True)
    subprocess.run(["ip", "link", "set", bridge_name, "up"], check=True)

    print(f"Bridge '{bridge_name}' created and set up with IP {gateway_ip}")


def delete_bridge(bridge_name):
    result = subprocess.run(["ip", "link", "show", bridge_name], capture_output=True)
    if result.returncode != 0:
        print(f"Bridge '{bridge_name}' does not exist")
        return

    subprocess.run(["ip", "link", "set", bridge_name, "down"], check=True)
    subprocess.run(["ip", "link", "delete", bridge_name, "type", "bridge"], check=True)

    print(f"Bridge '{bridge_name}' deleted")
