import json
import platform
import socket
from dataclasses import asdict, dataclass
from pathlib import Path

import click

from . import __version__

STATE_DIR = Path.home() / ".bastyn"
STATE_FILE = STATE_DIR / "state.json"
LICENSE_FILE = STATE_DIR / "license"


@dataclass
class State:
    install_path: str = ""
    api_url: str = "https://activate.bastyn.ai"
    customer: str = ""
    customer_slug: str = ""

    @classmethod
    def load(cls) -> "State":
        if STATE_FILE.exists():
            return cls(**json.loads(STATE_FILE.read_text()))
        return cls()

    def save(self) -> None:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(asdict(self), indent=2))

    def set_license_token(self, token: str) -> None:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        LICENSE_FILE.write_text(token)
        LICENSE_FILE.chmod(0o600)

    def get_license_token(self) -> str | None:
        return LICENSE_FILE.read_text().strip() if LICENSE_FILE.exists() else None

    def client_info(self) -> dict:
        return {
            "os": platform.system(),
            "os_version": platform.release(),
            "arch": platform.machine(),
            "hostname": socket.gethostname(),
            "cli_version": __version__,
        }

    def require_installed(self) -> None:
        if not self.install_path or not Path(self.install_path).exists():
            raise click.ClickException("Not initialized. Run `bastyn init` first.")
