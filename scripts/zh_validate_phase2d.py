#!/usr/bin/env python3
"""Phase 2D validation script — check 10-sample batch integrity."""

import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INV_PATH = os.path.join(REPO, "zh/data/translation_inventory.json")

BATCH_7_TARGETS = [
    "zh/memories/_posts/2013-01-12-aaron-and-taren.md",
    "zh/memories/_posts/2013-01-12-inspiring-heroism-aaron-swartz.md",
    "zh/memories/_posts/2013-01-13-apple-store.md",
    "zh/memories/_posts/2013-01-13-alyssa-rosenberg.md",
    "zh/memories/_posts/2013-01-13-a-huge-loss.md",
    "zh/memories/_posts/2013-01-13-aaron-was-an-inspiration.md",
    "zh/memories/_posts/2013-01-13-anirvan-chatterjee.md",
]

REQUIRED_FM_KEYS = [
    "layout",
    "lang",
    "original_path",
    "original_title",
    "translation_status",
]

def parse_front_matter(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    fm_text = parts[1].strip()
    body = parts[2].strip()
    fm = {}
    for line in fm_text.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm, body

def main():
    errors = []

    # 1. Inventory parseable
    try:
        with open(INV_PATH, "r", encoding="utf-8") as f:
            inventory = json.load(f)
    except Exception as e:
        print(f"FAIL: cannot parse inventory: {e}")
        return 1

    # 2. Total count
    if len(inventory) != 366:
        errors.append(f"inventory total {len(inventory)} != 366")

    # 3. sample_translated count
    sample_count = sum(1 for x in inventory if x.get("status") == "sample_translated")
    if sample_count != 3:
        errors.append(f"sample_translated {sample_count} != 3")

    # 4. translated count
    translated_count = sum(1 for x in inventory if x.get("status") == "translated")
    if translated_count < 7:
        errors.append(f"translated {translated_count} < 7")

    # 5. Batch 7 target files exist and have required front matter
    for rel in BATCH_7_TARGETS:
        path = os.path.join(REPO, rel)
        if not os.path.isfile(path):
            errors.append(f"missing target file: {rel}")
            continue
        fm, _ = parse_front_matter(path)
        for key in REQUIRED_FM_KEYS:
            if key not in fm:
                errors.append(f"{rel}: missing front matter key '{key}'")
        if fm.get("layout") != "default_zh":
            errors.append(f"{rel}: layout != default_zh")
        if fm.get("lang") != "zh-CN":
            errors.append(f"{rel}: lang != zh-CN")
        if fm.get("translation_status") != "translated":
            errors.append(f"{rel}: translation_status != translated")

    # 6. All target paths under zh/
    for item in inventory:
        tgt = item.get("target_path", "")
        if tgt and not tgt.startswith(os.path.join(REPO, "zh")):
            errors.append(f"target_path not under zh/: {tgt}")

    # 7. Original content untouched
    result = subprocess.run(
        ["git", "diff", "--name-only"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    modified = result.stdout.strip().split("\n") if result.stdout.strip() else []
    orig_modified = [m for m in modified if m.startswith("memories/_posts/") or m.startswith("statements/_posts/")]
    if orig_modified:
        errors.append(f"original content modified: {orig_modified}")

    # 8. newpost.html security
    newpost_path = os.path.join(REPO, "zh/newpost.html")
    with open(newpost_path, "r", encoding="utf-8") as f:
        newpost_content = f.read().lower()
    for keyword in ("password", "github password"):
        if keyword in newpost_content:
            errors.append(f"newpost.html contains: {keyword}")

    if errors:
        print("FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    else:
        print("PASS")
        print(f"  - inventory: {len(inventory)} entries")
        print(f"  - sample_translated: {sample_count}")
        print(f"  - translated: {translated_count}")
        print(f"  - batch_7 target files: all exist with required front matter")
        print(f"  - original content: untouched")
        print(f"  - newpost.html: no password references")
        return 0

if __name__ == "__main__":
    sys.exit(main())
