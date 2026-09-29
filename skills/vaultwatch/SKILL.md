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
more place to desynchronize*.) The generalizable laws our vaults earned
later — to recognize when they bite, not to copy unearned — are in
[references/laws-paid.md](references/laws-paid.md).

**`history/` — where closed arcs go.** When a piece of work closes, its whole
narrative block moves here and **one line** stays in HANDOFF.md. A HANDOFF
that accumulates closed blocks is how a 2,600-line file that produced its own
lies happens.

**`HANDOFF.md` — the cold-start door.** What exists, what works, what is
broken, what decisions are pending — and a short **"what can be done now"
table: the vault's future layer, and the only place direction lives.** It
exists because a red finding usually has an obvious fix, and the obvious fix
is often wrong for where the project is going; whoever fixes must know the
direction *before* measuring. No figures — link to `state/` instead.
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
   instead of being read from their assertion site — and retired ones
   (a rotated wallet) cited in the present tense, or served at all.
5. Tables split by a blockquote between rows.

Wire it so it runs **before every session and in CI on every push**. It needs
no network, so there is no excuse for it not to.

Two mechanics that keep the instrument honest as it grows (details in the
catalog): the runner **discovers** its checks and suites by glob — an
enumerated list ages the day the next suite is born, and the rows the runner
prints are the living list; and the anchors that latch onto claims should be
able to **fail when the claim disappears**, because otherwise deleting a
sentence silences the check, and silence looks identical to green.

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

**Read the door first, then measure.** Open HANDOFF.md — what exists, what is
broken, and the "what can be done now" table — *before* running anything.
Note the contradictions you spot while reading; do not fix them yet. The
order matters twice over: the obvious fix for a red is often wrong for where
the project is going, and correcting before measuring is exactly how several
of our 37 lies were produced. Then run both audits.

**Classify a red by class, not by row** — each class has a different owner:

| The red says | Class | Who acts |
|---|---|---|
| the vault contradicts itself or the disk | coherence | this session fixes the doc |
| the vault drifted from the world | world audit | this session — unless the world actually broke |
| code broke | test suite | report and stop; that is a work session |
| an artifact no longer derives from its source | derivation check | say it loudly — that blocks a deploy |
| an external invariant fell | probe | almost never documentation |

**A red that does not reproduce is investigated, not corrected.** Re-run the
failed instrument once before touching any file — a network flake prints the
same red as a real drift. And retry only on connection failure: a 500 that
flips to 200 on retry is a finding, not a flake.

**Fix at assertion sites**, then **prove every fix with a negative proof**:
break the corrected claim by hand, confirm the instrument goes red, restore
it. The real failure mode of "edit docs until the auditor is quiet" is not
writing badly — it is moving the text out of the anchor's reach, and the
resulting silence looks identical to green. A correction without its negative
proof is just one more unmeasured assertion.

**Cap: three rounds.** A red that survives three correction rounds is no
longer the documentation — it is the world, or the instrument. Stop and say
so; the fourth insistence is how a red becomes a false green.

**Then close**: list what the session changed in the world (deploys,
published content, config, purchases) → fix every vault claim those changes
made false → re-run both audits with the fixes in place → commit. What gets
committed depends on how the tree was found:

| The tree was | Do |
|---|---|
| clean | commit your changes |
| dirty and **green** | commit only yours; list what was pending, untouched |
| dirty and **red** | **do not commit** — list it and stop |

No commit — didn't happen: the next session starts blind. Never end a
session red. And never write what a run *will* say — run it, then write what
it said.

## Touching an instrument — loosening vs changing the unit

Sooner or later a guard itself becomes the problem, and the distinction that
decides what is allowed is **loosening vs changing the unit**.

**Loosening is forbidden, always**: deleting an assertion so a check goes
quiet, widening a regex until it matches anything, lowering a threshold,
removing a row. All of it turns red into silence, and silence looks identical
to green.

**Changing the unit or the map is legitimate** when the question the
instrument asked has stopped making sense — under three tests, all three:

1. **Does the demand rise, or at least hold?** If it drops, no.
2. **Is there a negative proof?** Without it you don't know whether you fixed
   the check or moved the claim out of its reach.
3. **Is the hole that remains written down?** A named hole beats a covered one.

Even then: **not alone.** Show the red, name the proposed change, argue why
the demand rises, and ask. An agent that can declare "the bar goes up" can
rationalize almost any edit to an auditor — deciding that is exactly the
judgment this rule exists not to delegate.

## Step 5 — Ship the cold-start skill

The ritual only survives if a cold session runs it without being told. Package
it as a **repo-local skill** (e.g. `/contexto`, or whatever fits the repo):
read in order, measure, classify, fix, prove, commit, and answer with an
**earned "ok"** — a short table whose figures come from this session's runs,
never from memory or from the doc. The full template, including the No-list
(what a context session never does: run anything that writes to the world,
fix code, delete worktrees, touch an instrument without asking, invent a
figure), is in [references/contexto-skill.md](references/contexto-skill.md).

## Multi-project shape

One vault per project, living next to the code it describes — only there can
an auditor compare it to its own reality. Across projects keep a single thin
index: one line and one entry point per project, **pointers, never copies**.
A centralized mega-vault is where drift hides best; it has been tried, and it
is the 2,600-line file with extra steps.
