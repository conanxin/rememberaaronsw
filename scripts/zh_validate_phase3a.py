#!/usr/bin/env python3
import json
import re
import subprocess
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
INV = ROOT / "zh/data/translation_inventory.json"

BATCH_SOURCE_PATHS = [
    "statements/_posts/2013-01-11-donate.md",
    "statements/_posts/2013-01-11-funeral.md",
    "statements/_posts/2013-01-12-family.md",
    "memories/_posts/2013-01-12-jacob-applebaum-aaron.md",
    "memories/_posts/2013-01-13-james-fallows.md",
    "memories/_posts/2013-01-13-john-gruber.md",
    "memories/_posts/2013-01-13-john-swartz.md",
    "memories/_posts/2013-01-13-henry-farrell.md",
    "memories/_posts/2013-01-13-hero-of-the-open-world.md",
    "memories/_posts/2013-01-13-prosecutor-as-bully.md",
    "memories/_posts/2013-01-13-remembering-aaron-swartz.md",
    "memories/_posts/2013-01-13-rip-aaron-swartz.md",
    "memories/_posts/2013-01-13-the-truth.md",
    "memories/_posts/2013-01-13-tech-bloggers-pay-tribute.md",
    "memories/_posts/2013-01-13-books-in-browsers.md",
    "memories/_posts/2013-01-13-internet-freedom-activist.md",
    "memories/_posts/2013-01-13-rss-kevin-burton.md",
    "memories/_posts/2013-01-13-standards.md",
    "memories/_posts/2013-01-13-sapere-aude.md",
    "memories/_posts/2013-01-13-a-poem-for-aaron.md",
]

REQUIRED_KEYS = [
    "layout: default_zh",
    "lang: zh-CN",
    "original_path:",
    "original_title:",
    "translation_status: translated",
]

def fail(msg):
    print("FAIL")
    print("  -", msg)
    raise SystemExit(1)

if not INV.exists():
    fail("inventory missing")

try:
    data = json.loads(INV.read_text(encoding="utf-8"))
except Exception as e:
    fail(f"inventory parse error: {e}")

if len(data) != 366:
    fail(f"inventory total expected 366, got {len(data)}")

status = Counter(x.get("status") for x in data)
if status.get("sample_translated", 0) != 3:
    fail(f"sample_translated expected 3, got {status.get('sample_translated', 0)}")

if status.get("translated", 0) < 27:
    fail(f"translated expected >=27, got {status.get('translated', 0)}")

pending = status.get("pending", 0)
if pending != 336:
    print(f"WARN - pending expected 336, got {pending}")

batch_entries = [x for x in data if x.get("notes") == "phase3a_20_batch"]
if len(batch_entries) != 20:
    fail(f"phase3a_20_batch entries expected 20, got {len(batch_entries)}")

batch_paths = {x.get("source_path") for x in batch_entries}
if set(BATCH_SOURCE_PATHS) != batch_paths:
    missing = set(BATCH_SOURCE_PATHS) - batch_paths
    extra = batch_paths - set(BATCH_SOURCE_PATHS)
    fail(f"batch source mismatch. missing={sorted(missing)} extra={sorted(extra)}")

# Validate target files and front matter
statement_count = 0
for item in batch_entries:
    source_path = item["source_path"]
    bucket = item["source_bucket"]
    target = ROOT / "zh" / bucket / "_posts" / Path(source_path).name

    if not str(target).startswith(str(ROOT / "zh")):
        fail(f"target not under zh/: {target}")

    if not target.exists():
        fail(f"target file missing: {target}")

    txt = target.read_text(encoding="utf-8", errors="replace")
    for k in REQUIRED_KEYS:
        if k not in txt:
            fail(f"required key missing in {target}: {k}")

    if bucket == "statements":
        statement_count += 1

if statement_count != 3:
    fail(f"phase3a statements count expected 3, got {statement_count}")

# Ensure original source dirs untouched in git diff
r = subprocess.run(
    ["git", "diff", "--name-only"],
    cwd=ROOT,
    capture_output=True,
    text=True,
    check=False,
)
changed = [x.strip() for x in r.stdout.splitlines() if x.strip()]
for p in changed:
    if p.startswith("memories/_posts/") or p.startswith("statements/_posts/"):
        fail(f"original source modified: {p}")

# newpost security check
newpost = ROOT / "zh/newpost.html"
if newpost.exists():
    t = newpost.read_text(encoding="utf-8", errors="replace")
    if re.search(r"password|GitHub password|github password", t, flags=re.I):
        fail("password reference found in zh/newpost.html")

print("PASS")
print("  - inventory: 366 entries")
print("  - status:", dict(status))
print("  - phase3a_20_batch: 20 entries")
print("  - statements in batch: 3")
print("  - target files/front matter: all pass")
print("  - original content: untouched")
print("  - newpost.html: no password references")
