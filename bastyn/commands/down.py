import click

from ..compose import run
from ..state import State


@click.command()
@click.option("--volumes", is_flag=True, help="Also remove volumes (destructive)")
def down(volumes):
    """Stop all services."""
    state = State.load()
    args = ["down"]
    if volumes:
        click.confirm(
            "This will DELETE all data including the database. Continue?",
            abort=True,
        )
        args.append("-v")
    run(state, *args)
    click.secho("✓ Stopped", fg="green")
