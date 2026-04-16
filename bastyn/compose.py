import subprocess
import sys

import click

from .state import State


def run(state: State, *args: str, check: bool = True) -> int:
    state.require_installed()
    try:
        r = subprocess.run(["docker", "compose", *args], cwd=state.install_path)
    except FileNotFoundError:
        raise click.ClickException("`docker` not found. Install Docker Desktop or Docker Engine.")
    if check and r.returncode != 0:
        sys.exit(r.returncode)
    return r.returncode
