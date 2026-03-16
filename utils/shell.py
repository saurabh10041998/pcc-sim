def exec_in_namespace(namespace: str, command: str):
    import subprocess

    subprocess.run(
        ["ip", "netns", "exec", namespace, "bash", "-c", command], check=True
    )
