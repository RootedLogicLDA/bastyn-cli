import re
import secrets
from dataclasses import dataclass, field
from pathlib import Path

CHANGE_ME = "<CHANGE ME>"


@dataclass
class Field:
    key: str
    value: str
    comment: str

    @property
    def needs_input(self) -> bool:
        return CHANGE_ME in self.value

    @property
    def auto_gen(self) -> str | None:
        """Detect '`python3 -c \"...secrets.token_hex(N)...\"`' hints in comment block."""
        m = re.search(r"secrets\.token_hex\((\d+)\)", self.comment)
        if not m:
            return None
        n = int(m.group(1))
        if "'sk-'" in self.comment or '"sk-"' in self.comment:
            return "sk-" + secrets.token_hex(n)
        return secrets.token_hex(n)


@dataclass
class Parsed:
    lines: list = field(default_factory=list)  # list of ("raw", str) | ("field", Field)


def parse(path: Path) -> Parsed:
    result = Parsed()
    comment_block: list[str] = []
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if stripped.startswith("#") or not stripped:
            comment_block.append(line)
            result.lines.append(("raw", line))
            continue
        if "=" in line:
            key, _, value = line.partition("=")
            result.lines.append(
                ("field", Field(key=key.strip(), value=value, comment="\n".join(comment_block)))
            )
            comment_block = []
        else:
            result.lines.append(("raw", line))
            comment_block = []
    return result


def render(parsed: Parsed, answers: dict[str, str], extra: list[str] | None = None) -> str:
    out = []
    for kind, item in parsed.lines:
        if kind == "raw":
            out.append(item)
        else:
            value = answers.get(item.key, item.value)
            out.append(f"{item.key}={value}")
    if extra:
        out.append("")
        out.extend(extra)
    return "\n".join(out) + "\n"
