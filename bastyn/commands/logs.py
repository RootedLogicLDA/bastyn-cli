import click

from ..compose import run
from ..state import State


@click.command()
@click.argument("service", required=False)
@click.option("-f", "--follow", is_flag=True, default=True, help="Follow log output")
@click.option("--tail", default="200", show_default=True)
def logs(service, follow, tail):
    """Tail service logs."""
    state = State.load()
    args = ["logs", "--tail", tail]
    if follow:
        args.append("-f")
    if service:
        args.append(service)
    run(state, *args, check=False)
