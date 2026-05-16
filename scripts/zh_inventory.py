#!/usr/bin/env python3
"""
Generate translation inventory for rememberaaronsw Chinese localization.
Uses only Python stdlib — no PyYAML dependency.
"""

import json
import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIRS = {
    "memories": REPO_ROOT / "memories" / "_posts",
    "statements": REPO_ROOT / "statements" / "_posts",
}
OUTPUT_JSON = REPO_ROOT / "zh" / "data" / "translation_inventory.json"

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_front_matter(text: str) -> dict:
    m = FM_RE.match(text)
    if not m:
        return {}
    raw = m.group(1)
    result = {}
    for line in raw.splitlines():
        line = line.rstrip()
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        result[key] = val
    return result


def scan_posts(bucket_name: str, source_dir: Path) -> list:
    entries = []
    for fpath in sorted(source_dir.iterdir()):
        if not fpath.is_file():
            continue
        text = fpath.read_text(encoding="utf-8")
        fm = parse_front_matter(text)
        rel_path = str(fpath.relative_to(REPO_ROOT))
        target_path = str(REPO_ROOT / "zh" / rel_path)
        entry = {
            "source_path": rel_path,
            "target_path": target_path,
            "source_bucket": bucket_name,
            "date": fm.get("date", ""),
            "type": fm.get("type", ""),
            "title": fm.get("title", ""),
            "author": fm.get("author", ""),
            "link": fm.get("link", ""),
            "layout": fm.get("layout", ""),
            "status": "pending",
            "notes": "",
        }
        if not fm:
            entry["notes"] = "missing_front_matter"
        elif not entry["type"]:
            entry["notes"] = "missing_type"
        if fpath.suffix not in (".md", ""):
            entry["notes"] = (entry["notes"] + " " if entry["notes"] else "") + f"nonstandard_suffix={fpath.suffix}"
        elif fpath.suffix == "":
            entry["notes"] = (entry["notes"] + " " if entry["notes"] else "") + "no_file_extension"
        entries.append(entry)
    return entries


def main():
    all_entries = []
    for bucket, src_dir in SOURCE_DIRS.items():
        all_entries.extend(scan_posts(bucket, src_dir))

    # Mark abnormal types
    known_types = {"post", "quote", "image"}
    for e in all_entries:
        if e["type"] and e["type"] not in known_types:
            e["notes"] = e.get("notes", "") + " abnormal_type=" + e["type"]

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(all_entries, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    stats = {
        "memories": sum(1 for e in all_entries if e["source_bucket"] == "memories"),
        "statements": sum(1 for e in all_entries if e["source_bucket"] == "statements"),
        "type_distribution": {},
        "abnormal": sum(1 for e in all_entries if "abnormal_type" in e.get("notes", "")),
        "missing_fm": sum(1 for e in all_entries if "missing_front_matter" in e.get("notes", "")),
        "missing_type": sum(1 for e in all_entries if "missing_type" in e.get("notes", "")),
        "total": len(all_entries),
    }
    for e in all_entries:
        t = e.get("type") or "(none)"
        stats["type_distribution"][t] = stats["type_distribution"].get(t, 0) + 1

    print(json.dumps(stats, indent=2, ensure_ascii=False))
    print(f"\nOutput: {OUTPUT_JSON}")
    print(f"Size: {OUTPUT_JSON.stat().st_size} bytes")


if __name__ == "__main__":
    main()
