import base64
import io
import subprocess
import sys
import tarfile
from pathlib import Path

import click

from ..api import activate as api_activate
from ..envparse import parse, render
from ..state import State


@click.command()
@click.option(
    "--install-dir",
    default="./bastyn",
    show_default=True,
    help="Where to place deployment files",
)
@click.option("--license", "license_opt", default=None, help="License token (skips prompt)")
def init(install_dir, license_opt):
    """Activate, download files, authenticate to the registry, and configure .env."""
    state = State.load()
    install_path = Path(install_dir).resolve()
    install_path.mkdir(parents=True, exist_ok=True)

    click.secho("BASTYN on-premises installer", bold=True)
    click.echo()

    token = license_opt or click.prompt("License token", hide_input=True).strip()

    try:
        resp = api_activate(state, token)
    except Exception as e:
        raise click.ClickException(f"Activation failed: {e}")

    click.secho(f"✓ Activated for {resp['customer']}", fg="green")

    state.customer = resp["customer"]
    state.customer_slug = resp["customer_slug"]
    state.install_path = str(install_path)
    state.set_license_token(token)

    tar_bytes = base64.b64decode(resp["bundle_b64"])
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as tar:
        tar.extractall(install_path)
    click.secho(f"✓ Deployment files written to {install_path}", fg="green")

    registry_url = f"https://{resp['registry_url']}"
    click.echo("Authenticating to image registry...")
    try:
        r = subprocess.run(
            ["docker", "login", "-u", "_json_key", "--password-stdin", registry_url],
            input=resp["registry_key_json"].encode(),
            capture_output=True,
        )
    except FileNotFoundError:
        raise click.ClickException("`docker` not found. Install Docker Desktop or Docker Engine.")
    if r.returncode != 0:
        raise click.ClickException(f"docker login failed: {r.stderr.decode().strip()}")
    click.secho(f"✓ Authenticated to {resp['registry_url']}", fg="green")

    click.echo()
    click.secho("Configure your deployment", bold=True)
    click.echo("Press enter to accept auto-generated values where offered.")
    click.echo()

    env_example = install_path / ".env.example"
    env_out = install_path / ".env"
    parsed = parse(env_example)

    answers: dict[str, str] = {}
    for kind, item in parsed.lines:
        if kind != "field" or not item.needs_input:
            continue
        auto = item.auto_gen
        if auto and click.confirm(f"  Auto-generate {item.key}?", default=True):
            answers[item.key] = auto
            continue
        is_secret = any(w in item.key for w in ("PASSWORD", "KEY", "SECRET", "TOKEN"))
        answers[item.key] = click.prompt(f"  {item.key}", hide_input=is_secret)

    click.echo()
    provider = click.prompt(
        "LLM provider",
        type=click.Choice(["openai", "azure"], case_sensitive=False),
        default="openai",
    ).lower()
    extra: list[str] = ["# --- LLM provider (set by bastyn init) ---"]
    if provider == "openai":
        key = click.prompt("  OpenAI API key", hide_input=True)
        extra.append(f"OPENAI_DIRECT_API_KEY={key}")
    else:
        base = click.prompt("  Azure API base URL")
        key = click.prompt("  Azure API key", hide_input=True)
        extra.append(f"AZURE_API_BASE={base}")
        extra.append(f"AZURE_API_KEY={key}")
        click.secho(
            "  Note: edit litellm_config.yaml to activate Option B. See README.",
            fg="yellow",
        )

    default_email = click.prompt(
        "  FIRST_SUPERUSER (admin email)", default="admin@example.com"
    )
    extra.append(f"FIRST_SUPERUSER={default_email}")

    env_out.write_text(render(parsed, answers, extra=extra))
    env_out.chmod(0o600)
    click.secho(f"✓ Wrote {env_out}", fg="green")

    state.save()

    click.echo()
    click.secho("✓ Installation complete", fg="green", bold=True)
    click.echo()
    click.echo("Next steps:")
    click.echo("  bastyn up       # pull images and start services")
    click.echo("  bastyn status   # show service health")
    click.echo("  bastyn logs     # tail logs")
