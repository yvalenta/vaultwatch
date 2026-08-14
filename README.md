# My AI Knowledge Base Lied To Me 37 Times. Every Test Was Green.

Everyone is building AI second brains right now.

Raw files in. AI-maintained wiki out. @karpathy's method — and it works.

I run one. I love it.

Then mine lied to me 37 times across six review rounds, and every single check was green while it happened.

The worst one wasn't a stale number.

A crypto wallet of ours got compromised. We rotated it. Updated the docs. Ran the audits. Green.

Meanwhile a forgotten file kept **publicly serving the old wallet** — for days.

Three auditors passed. The world had moved. The wiki hadn't noticed.

That failure built the system I actually use now.

## The Blind Spot In The Wiki Method

Karpathy's model treats documents as source code:

```
RAW FILES
   ↓
AI COMPILES A WIKI
   ↓
INDEX + LINKS + SOURCES
   ↓
FUTURE QUESTIONS USE THE WIKI
```

For reading knowledge — papers, transcripts, notes — this is exactly right.

A note about a book cannot betray you. There is no world outside it that can silently make it false.

But the moment your knowledge base describes **operated systems** — servers, prices, published contracts, wallets, deployed APIs — every page has a world outside it.

And that world changes while nobody is looking.

Contradiction detection between notes doesn't save you.

Two notes can agree perfectly about a world that no longer exists.

| | Karpathy's wiki | Audited vault |
|---|---|---|
| Source of truth | raw files | **the running world** |
| Contradiction check | note vs note | note vs **reality** |
| Failure it catches | duplicate / conflicting pages | a page that stayed "correct" while the world moved |
| When it runs | on ingest | **before every session + CI** |
| Green means | pages are consistent | what the scripts watch is still in place — *and nothing more* |

## The Fix: A Wiki That Gets Audited Against Reality

```
WIKI CLAIM: "endpoint X charges $2"
   ↓
AUDITOR SCRIPT (runs before every session)
   ↓
ACTUAL HTTP CALL TO ENDPOINT X
   ↓
MATCH?  → green, keep working
DRIFT?  → RED BUILD, fix the doc first
```

The vault is not something you read.

It is something you **run**.

Two instruments, and the second one is the difference:

**1. Coherence audit (no network, ~1 second).**
Does the document contradict itself?
Sweeps the entire tree: hand-copied constants, orphan notes, counts that don't match the disk, broken tables. Fails the build.

**2. World audit (network, ~10 seconds).**
Does the document describe reality?
Every claim in `state/` gets re-measured: HTTP calls to what's actually served, on-chain reads, `git ls-remote` against real remotes.

If the doc says an endpoint charges and the endpoint stopped charging — red. Even though nobody touched the doc.

**Especially** because nobody touched the doc.

## The Structure

```
vault/
│
├── state/       what is true TODAY — one file per fact,
│                every figure has exactly ONE assertion site
│
├── laws/        atomic method notes — each one born
│                from an error we actually paid for
│
├── history/     what happened, so we stop repeating it
│
└── HANDOFF.md   the cold-start door: what exists, what works,
                 what's broken, what's pending. Ruthlessly pruned.
```

Our first HANDOFF grew to 2,600 lines. 48% of it was correction blocks nobody re-read.

That file is where the lies incubated.

The first pruning cut half the lines without losing a word. Closed arcs move to `history/`, one line stays behind.

## The Laws That Pay Rent

Each of these cost us something before it became a rule:

**Never write the number a command WILL print. Write the one it printed.**
The auditor caught me three times writing test counts before running the tests.

**If a fact expires faster than it gets re-read, don't write it — measure it at runtime.**
Before writing any number, ask how long it lives.

**What you serve matters more than what you wrote.**
The dangerous drift isn't in your notes. It's in what a third party receives from your systems while your notes say otherwise.

**Every hand-copied constant is one more place to desynchronize.**
Scripts read constants from the assertion site. A repeated literal fails the build.

**An `exit 0` proves nothing is right.**
It proves the things the scripts know how to check are still in place. Ours stayed green through six rounds of lies. Every caught lie becomes a new auditor row — not a resolution to do better.

## The Ritual (Rule #1)

Before working: **run the auditors, then read.**

After working: **fix what your session made false. Re-run the auditors with the fixes in place. Commit.**

No commit — didn't happen. The next session starts blind.

This is not a habit we recommend. It is the repo's rule #1, and the AI sessions execute it as part of the work.

## Prompt 1: Create The Structure

```
Task: set up an audited knowledge vault.

Create:
/state       — one file per living fact. Each figure appears in
               EXACTLY one file (its "assertion site").
/laws        — atomic method notes. A law may only be written
               after an error was actually paid.
/history     — closed arcs, moved here whole; one line stays
               in HANDOFF.md
HANDOFF.md   — cold-start entry: what exists, works, is broken,
               is pending. No figures — link to /state instead.

Rules:
- prose may quote old numbers freely; changing a figure
  happens ONLY at its assertion site
- a correction block that isn't struck through reads as present
  tense; when superseded, strike it and say what superseded it
- every new note must be linked from the index, or the audit fails
- if a fact expires faster than it gets re-read, it does not get
  written: it gets measured by the auditor at runtime
```

## Prompt 2: The Coherence Audit

```
Task: write a script that fails loudly when my vault
contradicts itself. No network access.

Check the ENTIRE tree (not a list of paths — that is how two
forgotten copies once served a compromised credential):

- any figure appearing outside its assertion site
- notes not linked from the index (orphans)
- counts in docs vs counts on disk (tests, files, entries)
- identity constants appearing as literals in code
- tables split by blockquotes between rows

Exit 1 on any hit, naming file and line.
This runs before every session and in CI on every push.
```

## Prompt 3: The World Audit

```
Task: write a script that re-measures my vault against reality.
Network allowed. ~10 seconds budget.

For every claim in /state, derive a measurement:
- "endpoint X returns 402"     → make the HTTP call
- "the served key is K"        → fetch and compare bytes
- "repo is pushed"             → git ls-remote vs local HEAD
- "wallet W holds the NFT"     → on-chain read

Two row types:
- ASSERTION: doc said X, world said Y → RED on mismatch
- SNAPSHOT: volatile values (market counts, balances) are
  REPORTED but never fail the build — an auditor that cries
  hourly trains everyone to ignore it

Print what the doc claims next to what the world answered.
The diff IS the finding.
```

## Prompt 4: The Session Close

```
Task: close this working session by Rule #1.

1. List everything this session changed in the world
   (deploys, published content, config, purchases).
2. For each change, find the vault claims it made false.
   Fix them at their assertion sites.
3. Re-run the coherence audit AND the world audit
   WITH the fixes in place.
4. If green: commit vault + code together, message says
   what changed in the world and what the audit measured.
5. If red: fix and repeat. Do not end the session red.

Never write what a run WILL say. Run it, then write what it said.
```

## The Part Nobody Tells You

The wiki method's contradiction handling is good. Keep it.

But route contradictions by **who can settle them**:

A contradiction between two notes → flag it, like Karpathy says.

A contradiction between a note and the world → that is not a discussion. The world wins. The note was a lie with good intentions.

Our auditor caught a "spec is not published yet" claim that had been false for a full day — the spec was live on GitHub the whole time. The doc was asking us to do something already done.

That's the failure mode no note-vs-note check can see.

## Install It As A Claude Code Skill

This repo ships the whole method as a ready-to-use skill — the four prompts above, turned into an instrument Claude applies to your repo:

```bash
git clone https://github.com/yvalenta/audited-vault
mkdir -p ~/.claude/skills
cp -r audited-vault/skills/audited-vault ~/.claude/skills/
```

Then, in any repo: *"set up an audited vault here."* Claude builds the structure, writes both auditors fitted to what your project actually serves, and runs them in front of you.

## The Result

One brain per project, living next to the code it describes — because only there can an auditor compare it to its own reality.

A thin shared index across projects: one line and one entry point each. Pointers, never copies.

And the brains **run**: each active project has a persistent AI session that cold-starts by reading its vault and gets woken by its channel when something happens.

The vault stops being documentation *about* the system.

It becomes the system's working memory — with instruments whose only job is to contradict it.

Knowledge compounds.

Lies compound too.

The difference is who audits.

---

*Built in public. The 37 lies, the six green rounds, and the wallet incident are documented in the vault's own `history/` — that's the point.*

*This method description is public domain. Steal it, run it, and let your auditors contradict you.*
