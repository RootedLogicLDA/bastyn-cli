import click

from ..compose import run
from ..state import State


@click.command()
@click.option("--pull/--no-pull", default=True, help="Pull latest images before starting")
def up(pull):
    """Start all services (docker compose up -d)."""
    state = State.load()
    if pull:
        click.echo("Pulling latest images...")
        run(state, "pull")
    run(state, "up", "-d")
    click.secho("✓ BASTYN is running. Open http://localhost", fg="green")
