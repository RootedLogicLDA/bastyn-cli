import click

from ..compose import run
from ..state import State


@click.command()
def status():
    """Show service health."""
    state = State.load()
    run(state, "ps")
