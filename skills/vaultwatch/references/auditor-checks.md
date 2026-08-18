# Auditor check catalog

Implementation notes for the two instruments. Write them in the repo's main
language, zero dependencies beyond the standard library. Each check below
lists what it catches and the failure that motivated it.

## Coherence audit (no network)

### 1. Figures outside their assertion site

Anchor each living figure with a recognizable phrase pattern at its assertion
site (e.g. `tests: 74 passing`), then grep the rest of the tree for competing
statements of the same fact. A figure stated twice is two figures the moment
one changes.

Pitfall: make anchors one-per-line with a label. A date or count living
loose in a paragraph's flow will eventually be matched by the wrong sentence
— an anchor once latched onto a *different* phrase containing the same
keyword and the check went green against the wrong line.

### 2. Orphan notes

Every `.md` under the vault must be reachable from the index. An unlinked
note still renders, still gets read by grep-happy agents, and never gets
re-reviewed — it is where stale claims go to hide.

### 3. Doc counts vs disk counts

Wherever a doc states "N tests", "N files", "N entries": count the real thing
and compare. This is the single highest-yield check for AI-maintained vaults
— the model writes the number it *expects* a run to print. Three separate
incidents in the source repo were exactly this reflex.

### 4. Constants as literals

Identity constants (wallet addresses, key ids, service ids) live in one
assertion site and are **read** from there by scripts — two small readers,
one per language, cost less than one desync. The check: grep the codebase for
any literal matching the constants' shapes (0x-addresses, key-id hex, etc.)
outside the assertion site and the files explicitly allowed to embed them.

Sweep the ENTIRE tree from the repo root, including worktrees and anything
gitignored that could be served. Two forgotten worktree copies once kept a
compromised credential publicly deployable while every audit passed —
because the sweep was anchored to a path list instead of the root.

### 5. Table hygiene

A blockquote between two table rows splits the table in rendering while
looking fine in the editor. Detect `>` lines between `|` rows.

### 6. Strikethrough discipline (optional but cheap)

A correction blockquote that is not struck through reads as present tense
forever. If your vault uses dated correction blocks, check that superseded
ones carry `~~` and a pointer to what superseded them.

## World audit (network)

### Deriving measurements

For each claim in `state/`, write the measurement next to the claim pattern:

| Claim shape | Measurement | Red condition |
|---|---|---|
| endpoint status ("returns 402/200/404") | HTTP call, follow no redirects | code differs |
| served content ("the page/key is X") | fetch, byte-compare against source of truth | bytes differ |
| "pushed" / "deployed from main" | `git ls-remote origin` vs local HEAD; served sha vs `git rev-parse` | mismatch |
| on-chain facts (ownership, balances-as-structure) | RPC read | value differs |
| third-party listings ("our entry exists") | API query, paginated fully | entry absent |

### Assertion vs snapshot

Mark volatile rows (market counts, balances, anything a third party moves) as
SNAPSHOT: print, never fail. The moment an auditor produces routine red, it
trains its operators to ignore red. Reserve failure for claims whose change
means *the documentation is now lying*.

### Comparison pitfalls (each one a paid false negative)

- **Case and prefix normalization**: EVM addresses compare in lowercase
  (EIP-55 checksums make the same address print two ways); hashes compare
  with `0x` stripped and lowercased.
- **Hash function mismatch**: EVM anchors use keccak-256, not sha-256.
- **Serialization**: byte-compare only against bytes you control end-to-end;
  a proxy that pretty-prints JSON breaks naive equality. Compare
  canonicalized forms when the transport may re-serialize.
- **Retry only on connection failure**, never on an unexpected status — a
  500 that flips to 200 on retry is a finding, not a flake.

### The humility banner

Print at the end of every run, verbatim or adapted:

> exit 0 means the things these scripts know how to watch are still in
> place — and nothing more.

When a lie gets past the audits, the response is mechanical: add the row
that would have caught it, cite the incident in the row's comment, move on.
The auditor grows by autopsy, not by ambition.
