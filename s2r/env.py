"""Load ~/.runai/runai.env into os.environ before any config is read.

File format — a subset of dotenv:
  KEY=value          bare value
  KEY="value"        double-quoted (quotes stripped)
  KEY='value'        single-quoted (quotes stripped)
  # comment          ignored
  (blank line)       ignored

Existing env vars are NOT overwritten (shell environment wins).
"""

import os
from pathlib import Path

ENV_FILE = Path.home() / ".runai" / "runai.env"


def load_env_file(path: Path = ENV_FILE) -> dict:
    """Parse *path* and inject missing keys into os.environ.

    Returns a dict of the key/value pairs found in the file (whether or not
    they were injected — useful for display in the wizard).
    """
    found: dict = {}
    if not path.is_file():
        return found
    with path.open(encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            # Strip matching surrounding quotes
            val = val.strip()
            if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
                val = val[1:-1]
            if key:
                found[key] = val
                if key not in os.environ:
                    os.environ[key] = val
    return found


def _quote(val: str) -> str:
    """Wrap *val* in double quotes if it contains whitespace, '#', or quotes."""
    if val == "" or any(c in val for c in (" ", "\t", "#", '"', "'")):
        escaped = val.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return val


def write_env_file(values: dict, path: Path = ENV_FILE) -> None:
    """Write *values* to *path*, preserving unrelated existing lines."""
    path.parent.mkdir(parents=True, exist_ok=True)

    # Read existing lines so we can update in-place and keep unknowns
    existing_lines: list = []
    if path.is_file():
        with path.open(encoding="utf-8") as fh:
            existing_lines = fh.readlines()

    # Build a map of key → line-index for keys already present
    key_to_idx: dict = {}
    for i, line in enumerate(existing_lines):
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            k = stripped.split("=", 1)[0].strip()
            key_to_idx[k] = i

    # Update or append each value, quoting if needed to survive a future read
    for key, val in values.items():
        entry = f"{key}={_quote(val)}\n"
        if key in key_to_idx:
            existing_lines[key_to_idx[key]] = entry
        else:
            existing_lines.append(entry)

    with path.open("w", encoding="utf-8") as fh:
        fh.writelines(existing_lines)
