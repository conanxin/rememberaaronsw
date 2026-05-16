#!/usr/bin/env python3
"""Mark 3 sample entries as sample_translated in the inventory."""
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INV_PATH = REPO_ROOT / "zh" / "data" / "translation_inventory.json"

SAMPLE_FILES = {
    "memories/_posts/2013-01-12-he-was-so-fiercely-brilliant.md",
    "memories/_posts/2013-01-12-cory-doctorow-aaron.md",
    "memories/_posts/2013-01-12-freedom-to-connect.md",
}

inv = json.loads(INV_PATH.read_text(encoding="utf-8"))
changed = 0
for e in inv:
    if e["source_path"] in SAMPLE_FILES:
        e["status"] = "sample_translated"
        e["sample"] = True
        e["notes"] = "Phase 2A sample translation"
        changed += 1

INV_PATH.write_text(json.dumps(inv, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Marked {changed} entries as sample_translated.")
