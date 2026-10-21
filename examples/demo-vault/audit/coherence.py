"""Coherence audit: does the vault contradict itself? No network, ~1 second.

    python3 -I coherence.py [VAULT_DIR]

Sweeps the ENTIRE tree under VAULT_DIR, not a list of paths. Exit 1 on any
hit, naming file and line. Three checks of the catalog, kept small on purpose:

  1. a figure outside its assertion site
  2. an orphan note (not linked from HANDOFF.md)
  3. a count in the doc that does not match the disk
"""
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

# A "figure" here is an amount of money. It may live in state/ (assertion
# site) and in history/ (prose may quote old numbers freely). Anywhere else
# it is a second copy that will desynchronize.
FIGURE = re.compile(r"\d+\.\d{2} USD")
FIGURE_OK = ("state", "history")
NOTE_DIRS = ("state", "laws", "history")

hits = []
files = [p for p in sorted(root.rglob("*")) if p.is_file() and ".git" not in p.parts]
texts = {}
for p in files:
    try:
        texts[p] = p.read_text()
    except UnicodeDecodeError:
        pass  # binary: nothing to read


def rel(p):
    return p.relative_to(root).as_posix()


# 1. figures outside their assertion site
for p, text in texts.items():
    if p.relative_to(root).parts[0] in FIGURE_OK:
        continue
    for n, line in enumerate(text.splitlines(), 1):
        if FIGURE.search(line):
            hits.append(f"{rel(p)}:{n}: figure outside its assertion site: {line.strip()!r}")

# 2. orphan notes: every note under state/ laws/ history/ is linked from HANDOFF.md
handoff = root / "HANDOFF.md"
if not handoff.exists():
    hits.append("HANDOFF.md:1: the cold-start door is missing")
    handoff_text = ""
else:
    handoff_text = handoff.read_text()
notes = [p for p in files if p.suffix == ".md" and p.relative_to(root).parts[0] in NOTE_DIRS]
for p in notes:
    if rel(p) not in handoff_text:
        hits.append(f"{rel(p)}:1: orphan note, not linked from HANDOFF.md")

# 3. doc counts vs disk counts
m = re.search(r"^Notes on disk: (.+)$", handoff_text, re.M)
if not m:
    hits.append("HANDOFF.md:1: no 'Notes on disk:' line to check against the disk")
else:
    line_no = handoff_text[: m.start()].count("\n") + 1
    claimed = dict(re.findall(r"(\w+)=(\d+)", m.group(1)))
    for d in NOTE_DIRS:
        actual = sum(1 for p in notes if p.relative_to(root).parts[0] == d)
        if claimed.get(d) != str(actual):
            hits.append(f"HANDOFF.md:{line_no}: doc says {d}={claimed.get(d)}, disk has {actual}")

print(f"coherence audit: 3 checks, {len(files)} files swept, {len(notes)} notes")
for h in hits:
    print("RED  " + h)
if hits:
    print(f"coherence audit: RED, {len(hits)} hit(s)")
    sys.exit(1)
print("coherence audit: green")
