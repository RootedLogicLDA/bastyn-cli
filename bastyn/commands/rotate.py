import subprocess

import click

from ..api import rotate as api_rotate
from ..state import State


@click.command("rotate-key")
def rotate():
    """Rotate the registry service account key."""
    state = State.load()
    token = state.get_license_token()
    if not token:
        raise click.ClickException("No saved license. Run: bastyn init")

    try:
        resp = api_rotate(state, token)
    except Exception as e:
        raise click.ClickException(f"Rotation failed: {e}")

    registry_url = f"https://{resp['registry_url']}"
    r = subprocess.run(
        ["docker", "login", "-u", "_json_key", "--password-stdin", registry_url],
        input=resp["registry_key_json"].encode(),
        capture_output=True,
    )
    if r.returncode != 0:
        raise click.ClickException(f"docker login failed: {r.stderr.decode().strip()}")
    click.secho(f"✓ Rotated registry key for {resp['customer']}", fg="green")
