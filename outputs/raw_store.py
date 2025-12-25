import json
from pathlib import Path

def save_raw(out_dir, name, payload):
    raw_dir = Path(out_dir) / "raw"
    raw_dir.mkdir(exist_ok=True)
    path = raw_dir / name
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
