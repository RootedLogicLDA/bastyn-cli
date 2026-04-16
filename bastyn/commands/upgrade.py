import click

from ..compose import run
from ..state import State


@click.command()
def upgrade():
    """Pull new image versions and restart services."""
    state = State.load()
    click.echo("Pulling new images...")
    run(state, "pull")
    click.echo("Recreating services...")
    run(state, "up", "-d")
    click.secho("✓ Upgraded", fg="green")
