---
name: vaultwatch
description: >
  Set up and operate an AUDITED knowledge vault: a plain-markdown second brain
  whose claims are verified by two instruments — a no-network coherence audit
  (the vault against itself) and a world audit (the vault against the running
  reality it describes: HTTP endpoints, served files, git remotes, on-chain
  state). Use this whenever the user wants a knowledge base, second brain,
  vault, wiki, HANDOFF, project memory, or documentation system for a repo
  that OPERATES something — servers, deployments, published content, prices,
  wallets, APIs — and also whenever they complain that docs drift, lie, go
  stale, or that "the README is always wrong". Covers bootstrapping a new
  vault, retrofitting auditors onto an existing docs/ folder, and the
  session-close ritual (fix what the session made false, re-run the audits,
  commit). If the knowledge is pure reading notes with no world that can
  contradict them, a plain wiki is enough and this skill is overkill.
---

# vaultwatch — the wiki that gets audited against reality

A second brain for **operated systems**. The difference from a normal wiki:
the vault is not something you read — it is something you **run**. Two scripts
decide whether it can be trusted before every working session, and they exist
because AI-maintained wikis compound lies exactly as well as they compound
knowledge: two pages can agree perfectly about a world that already changed.

This method comes from a real repo that accumulated 37 false claims across six
review rounds — all with tests green — including a rotated credential that a
forgotten file kept publicly serving while three auditors passed. Every rule
below was paid for before it was written.

## Step 0 — Decide the mode

- **Bootstrap**: no docs exist yet → create the full structure (Step 1), then
  the auditors (Steps 2–3).
- **Retrofit**: a docs/ folder already exists → do NOT reorganize it in one
  heroic pass. Create `state/` and move the *live figures* there one at a time
  (each move is a chance to re-measure them), add the auditors, and let the
  rest migrate when it's touched. A big-bang migration writes new lies.

Ask which the user wants only if the repo doesn't make it obvious.

## Step 1 — The structure

```
docs/
├── HANDOFF.md    the cold-start door
├── state/        what is true TODAY
├── laws/         method notes, each born from a paid error
└── history/      what happened, so it stops repeating
```

**`state/` — assertion sites.** Every living figure (a price, a key id, an
endpoint status, a deployed sha relation) appears in **exactly one file**.
Prose anywhere may quote figures freely, but *changing* a figure happens only
at its assertion site — that is the line the auditor reads. If a figure
expires faster than anyone re-reads it (balances, market counts), it does
**not** get written at all: the auditor measures and prints it at runtime.

**`laws/` — earned, not speculative.** A law may only be written after an
error was actually paid. Seed the folder with nothing; the first incident
funds the first law. (The universal ones tend to arrive fast: *never write
the number a run WILL print — run it, then write what it printed*; *what you
serve matters more than what you wrote*; *every hand-copied constant is one
more place to desynchronize*.)

**`history/` — where closed arcs go.** When a piece of work closes, its whole
narrative block moves here and **one line** stays in HANDOFF.md. A HANDOFF
that accumulates closed blocks is how a 2,600-line file that produced its own
lies happens.

**`HANDOFF.md` — the cold-start door.** What exists, what works, what is
broken, what decisions are pending. No figures — link to `state/` instead.
Two formatting rules that sound cosmetic and are not: a correction blockquote
that is not struck through **reads as present tense** (when superseded,
strike it with `~~…~~` and say what superseded it); and blockquotes go after
a table, never between its rows.

Every new note must be reachable from the vault index (`README.md` or
HANDOFF) — the coherence audit fails on orphans, because an unlinked note is
where stale claims go to hide.

## Step 2 — The coherence audit (no network)

Write `audit_coherence` in the repo's main language, zero dependencies, exit 1
on any finding, naming file and line. It answers: **does the vault contradict
itself?** It must sweep the **entire tree from the repo root** — not a list of
paths. (The original incident: two forgotten worktree copies served a
compromised credential precisely because the sweep was anchored to known
paths.)

Minimum checks — the full catalog with implementation notes is in
[references/auditor-checks.md](references/auditor-checks.md):

1. Figures appearing outside their assertion site.
2. Notes not linked from the index (orphans).
3. Counts written in docs vs counts on disk (tests, files, entries).
4. Identity constants (addresses, ids, keys) appearing as literals in code
   instead of being read from their assertion site.
5. Tables split by a blockquote between rows.

Wire it so it runs **before every session and in CI on every push**. It needs
no network, so there is no excuse for it not to.

## Step 3 — The world audit (network)

Write `audit_world`: for every claim in `state/`, derive a measurement and
compare. It answers: **does the vault describe reality?** Budget ~10 seconds.

| Claim in state/ | Measurement |
|---|---|
| "endpoint X returns 402" | make the HTTP call |
| "the served key/page is K" | fetch and byte-compare |
| "repo is pushed" | `git ls-remote` vs local HEAD |
| "wallet W holds asset A" | on-chain read |
| "deploy serves sha of main" | fetch health, compare to `git rev-parse` |

Two row types, and the distinction keeps the tool alive:

- **ASSERTION** — doc said X, world answered Y → **red build** on mismatch.
  Red even though nobody touched the doc. *Especially* then.
- **SNAPSHOT** — volatile values are printed but never fail. An auditor that
  cries hourly about market noise trains everyone to ignore it, and then it
  stops working for the failures that matter.

Print the doc's claim next to the world's answer; the diff is the finding.
And write the humility banner into the tool's own output: **an exit 0 proves
that the things these scripts know how to watch are still in place — and
nothing more.** When a lie slips past, the fix is a new auditor row, not a
resolution to be more careful.

## Step 4 — The ritual (Rule #1)

Before working: **run both audits, then read.** The audits say whether the
vault can be trusted this session.

After working: **list what the session changed in the world** (deploys,
published content, config, purchases) → **fix every vault claim those changes
made false, at its assertion site** → **re-run both audits with the fixes in
place** → **commit vault and code together.** No commit — didn't happen: the
next session starts blind.

Never end a session red. And never write what a run *will* say — run it,
then write what it said.

## Multi-project shape

One vault per project, living next to the code it describes — only there can
an auditor compare it to its own reality. Across projects keep a single thin
index: one line and one entry point per project, **pointers, never copies**.
A centralized mega-vault is where drift hides best; it has been tried, and it
is the 2,600-line file with extra steps.
