import subprocess

USER = "elspeth"


def create_session_on_server(host, email):
    return _exec_in_container(
        host, ["/venv/bin/python", "/src/manage.py", "create_session", email]  # (1)
    )


def _exec_in_container(host, commands):
    if "localhost" in host:  # (2)
        return _exec_in_container_locally(commands)
    else:
        return _exec_in_container_on_server(host, commands)


def _exec_in_container_locally(commands):
    print(f"Running {commands} on inside local docker container")
    return _run_commands(["docker", "exec", _get_container_id()] + commands)  # (3)


def _exec_in_container_on_server(host, commands):
    print(f"Running {commands!r} on {host} inside docker container")
    return _run_commands(
        ["ssh", f"{USER}@{host}", "docker", "exec", "superlists"] + commands  # (4)
    )


def _get_container_id():
    return subprocess.check_output(  # (5)
        ["docker", "ps", "-q", "--filter", "ancestor=superlists"]  # (3)
    ).strip()


def _run_commands(commands):
    process = subprocess.run(  # (5)
        commands,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    result = process.stdout.decode()
    if process.returncode != 0:
        raise Exception(result)
    print(f"Result: {result!r}")
    return result.strip()
