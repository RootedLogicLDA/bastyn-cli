import click

from . import __version__
from .commands import down, init, logs, restart, rotate, status, up, upgrade


@click.group()
@click.version_option(__version__)
def cli():
    """BASTYN on-premises deployment CLI."""


cli.add_command(init.init)
cli.add_command(up.up)
cli.add_command(down.down)
cli.add_command(restart.restart)
cli.add_command(logs.logs)
cli.add_command(status.status)
cli.add_command(upgrade.upgrade)
cli.add_command(rotate.rotate)


if __name__ == "__main__":
    cli()
