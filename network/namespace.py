import subprocess


def create_namespace(namespace_name):
    result = subprocess.run(["ip", "netns", "list"], capture_output=True, text=True)
    existing_namespaces = result.stdout.splitlines()

    if namespace_name in existing_namespaces:
        print(f"Namespace '{namespace_name}' already exists")
        return

    subprocess.run(["ip", "netns", "add", namespace_name], check=True)
    print(f"Namespace '{namespace_name}' created")


def delete_namespace(namespace_name):
    result = subprocess.run(["ip", "netns", "list"], capture_output=True, text=True)
    existing_namespaces = result.stdout.splitlines()

    if namespace_name not in existing_namespaces:
        print(f"Namespace '{namespace_name}' does not exist")
        return

    subprocess.run(["ip", "netns", "delete", namespace_name], check=True)
    print(f"Namespace '{namespace_name}' deleted")
