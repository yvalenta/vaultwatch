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

### 7. Anchors that cannot be silenced

A check that greps for a claim pattern has a blind spot: **delete the
sentence and the check goes quiet** — and quiet prints exactly like green.
For claims that must keep existing (a coverage figure, a served-artifact
relation), give the check a `requires_site` mode: if the anchor phrase no
longer matches anywhere, that is itself a red — "the claim disappeared", not
"nothing to check". We added this after watching the legitimate fix for a
stale claim be deleting it, which would have killed the check in silence.

### 8. The accidental second assertion site

The dual failure: a *new* note innocently writes a phrase that matches an
existing anchor ("31 pytest tests" in a status update), and from that moment
the vault has two assertion sites to keep synchronized forever. Cheap
mitigation, worth its cost: before writing a figure into any note, check it
against the anchor patterns; cite the assertion site instead of repeating the
number. If your vault renders in Obsidian, a `[[state/...]]` wikilink is the
natural citation form.

### 9. Mutation sweep: data-shaped text nobody reads (advisory)

The negative proof (below), run in bulk and before any incident. On a
throwaway copy of the committed tree (`git archive` into a temp dir — never
the working repo), take every token in `state/` with a recognizable data
shape (address, hash, CID, URL, host:port, amount, integer+unit), change one
character, run the no-network gate, and record whether it stayed green.
**Green after mutation means no instrument reads that sentence.** It is
deterministic, it needs no model, and it does not guess who the readers
are: it measures them.

Why mutation and not a cross-reference: nobody owns the list of what the
auditors read, and deriving it statically lies in both directions. In the
pilot, matching literals against the auditor's source reported 141 readers
that did not exist (dates that also appear in code comments). And two
model readers in a row — a classifier and a skeptic, each with grep in hand —
declared a row unread that the mutation had already turned red: a test
compares it against a generated page.

What one pilot measured (a live private vault, 8 state files): 548
data-shaped tokens; the no-network auditor reads 11. After discounting what
the network auditor's patterns cover, 265 tokens on 207 lines had no reader,
dates excluded; mutated against the full gate (49 checks, 1,340 tests),
262 left it green. Triage of those 207 lines, by one classifier per file
plus a skeptic mandated to knock down every "live" verdict: 91 history, 69
measured some other way (the instrument checks the fact from its own
literal — the sentence can still drift from it), 14 noise, 7 snapshots, and
26 live claims nobody watches — 25 with their negative proof, since the
sweep had already shown a reader for one. Thirteen of the 25 are facts owned
by another repo (a sibling app's local address, a timer's cadence). **The
other twelve were ours and within reach**, and they include a price we set
on our own listing, the default spending ceiling of a script whose payments
are final, the threshold of a cloud budget alert, and the cadence of the
very watcher that guards another line of the vault.

Rules of use:

- **Advisory. It never turns the gate red**, and it prints with the
  humility banner. Its output is a list of candidates, and most of them
  must NOT be anchored: history is closed, snapshots are printed, not
  asserted. About one token in twenty survived triage. This check does not
  repeal "the auditor grows by autopsy" — it shows where the next autopsy
  would be, and you add rows only for the ones that would hurt.
- **The triage is judgment, so do it adversarially.** The skeptic moved 7
  of 33 "live" verdicts down (5 to history, 2 to measured-otherwise), and
  the sweep itself overruled both on one more.
- What to do with a survivor: if the fact is yours and in reach, anchor it
  with the check that fits (#3 for a count, #4 for a constant — read it from
  the code instead of restating it). If another repo owns the fact, cite it
  instead of repeating it (#8) and let the owner anchor it. If neither, date
  it so it reads as a snapshot.
- Skip dates. In a state file a date is almost always history; 263 of the
  548 tokens were dates and the no-network auditor read exactly one.

What it does NOT cover: red after mutation proves somebody reads the
*sentence*, not that anybody measures the *fact* — the one row the sweep
overruled is read by a copy-consistency test, while the fact itself (a
timer in another repo) stays unmeasured. It cannot see claims with no data
shape ("X binds to loopback"). And it costs one full gate run per token:
265 runs took about ten minutes on six parallel copies — a quarterly
exercise, not a gate step.

## Runner discipline

**Discover, don't enumerate.** The runner finds its suites and checks by
glob, so a new suite enters the gate the day it is written, with no list to
update. Every enumerated list of instruments we kept aged the day the next
instrument was born. Corollary: the rows the runner prints ARE the living
list — a skill or doc that names individual commands will rot; teach readers
to read the printed rows instead.

**Measure the exit code without a pipe.** `ruby x.rb | tail` returns the exit
code of `tail`. If you are going to cite an exit code, run the command bare.

## The negative proof

The check catalog above defends against the world drifting. This defends
against the *fixer*: after correcting a claim, **break it by hand, confirm
the instrument goes red, restore it.** If breaking the claim leaves the run
green, the correction did not fix anything — it moved the text out of the
anchor's reach, which is the one editing failure no reviewer can see in a
diff. One negative proof per corrected claim, every time. It is the only
defense against a green nobody earned.

## Perimeter guards: forbid the act, not the name

A no-network gate that stubs helpers by name (`http_get`, `fetch`, `rpc`…)
is a guard per name — and a new code path that calls the transport directly
walks past every stub at once. Close it one level down, where there is no
name to guess: forbid **opening a socket** in no-network suites (in Ruby,
raise from the socket layer via a preloaded file; in Rails, WebMock's
`disable_net_connect!` is the same idea). Ours exists because logic coverage
grew from 23 tests to 700+ while the perimeter didn't move.

Write down what the guard does NOT cover — a suite that shells out to `curl`
opens its socket in another process, past the gate. A named gap beats a
pretended completeness; that sentence in the guard's own header is part of
the guard.

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
