import click

from ..compose import run
from ..state import State


@click.command()
@click.argument("service", required=False)
def restart(service):
    """Restart all services, or one specific service."""
    state = State.load()
    args = ["restart"]
    if service:
        args.append(service)
    run(state, *args)
    click.secho("✓ Restarted", fg="green")
