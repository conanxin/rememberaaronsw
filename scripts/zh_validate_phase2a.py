#!/usr/bin/env python3
"""
Phase 2A validation script.
Uses only Python stdlib.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INV_PATH = REPO_ROOT / "zh" / "data" / "translation_inventory.json"
SAMPLE_TARGET_DIR = REPO_ROOT / "zh" / "memories" / "_posts"
NEWPOST_PATH = REPO_ROOT / "zh" / "newpost.html"

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def check_inventory():
    errors = []
    try:
        inv = json.loads(INV_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"inventory parse error: {e}")
        return errors

    samples = [e for e in inv if e.get("status") == "sample_translated"]
    if len(samples) != 3:
        errors.append(f"sample_translated count = {len(samples)}, expected 3")

    for e in samples:
        tgt = Path(e["target_path"])
        if not tgt.exists():
            errors.append(f"missing target file: {tgt}")
            continue
        text = tgt.read_text(encoding="utf-8")
        fm_match = FM_RE.match(text)
        if not fm_match:
            errors.append(f"missing front matter: {tgt}")
            continue
        fm_raw = fm_match.group(1)
        checks = {
            "layout: default_zh": "layout: default_zh" in fm_raw,
            "lang: zh-CN": "lang: zh-CN" in fm_raw,
            "original_path:": "original_path:" in fm_raw,
            "original_title:": "original_title:" in fm_raw,
            "translation_status: sample": "translation_status: sample" in fm_raw,
        }
        for k, v in checks.items():
            if not v:
                errors.append(f"{tgt} missing '{k}'")

        if not str(tgt).startswith(str(REPO_ROOT / "zh")):
            errors.append(f"target outside zh/: {tgt}")

    return errors


def check_original_content():
    errors = []
    result = subprocess.run(
        ["git", "diff", "--name-only"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    changed = result.stdout.strip().splitlines()
    bad = [p for p in changed if p.startswith("memories/_posts/") or p.startswith("statements/_posts/")]
    if bad:
        errors.append(f"original content modified: {bad}")
    return errors


def check_newpost():
    errors = []
    if not NEWPOST_PATH.exists():
        errors.append("zh/newpost.html missing")
        return errors
    text = NEWPOST_PATH.read_text(encoding="utf-8").lower()
    if "password" in text:
        errors.append("zh/newpost.html contains 'password'")
    if "github password" in text:
        errors.append("zh/newpost.html contains 'github password'")
    return errors


def main():
    all_errors = []
    all_errors.extend(check_inventory())
    all_errors.extend(check_original_content())
    all_errors.extend(check_newpost())

    if all_errors:
        print("FAIL")
        for e in all_errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("PASS")
        print("  - inventory: 3 sample_translated entries found")
        print("  - target files: all exist with required front matter")
        print("  - original content: untouched")
        print("  - newpost.html: no password references")
        sys.exit(0)


if __name__ == "__main__":
    main()
