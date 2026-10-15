# demo-vault: watch an audited vault catch a lie

A tiny, runnable vault. Python 3 standard library and bash, no network, nothing
to install. It exists so you can see the method fail on purpose before you
trust it on your own project.

```
demo-vault/
├── HANDOFF.md         cold-start door; also the index every note must be linked from
├── state/             what is true today; one assertion site per figure
├── laws/ history/     method notes, closed arcs
├── world/             the "operated system": a toy HTTP endpoint (server.py)
│                      and the file it serves (served.json)
├── audit/
│   ├── coherence.py   does the doc contradict itself? no network, ~1 second
│   └── world.py       does the doc describe reality? starts the endpoint and
│                      makes real HTTP calls to it (localhost)
└── demo.sh            runs both, and breaks things on a copy
```

## Run it

```bash
./demo.sh               # both audits on the vault as it is: green
./demo.sh --drift       # the world moves, the docs stay put   -> world audit RED
./demo.sh --contradict  # the doc copies a figure by hand      -> coherence audit RED
./demo.sh --orphan      # a note nobody links to               -> coherence audit RED
./demo.sh --proof       # all of the above, with the exit codes checked
```

`--drift` is the one to watch. Nobody touched a document, every note still
agrees with every other note, and the coherence audit stays green. Only the
world audit sees that the endpoint now answers differently from what
`state/price.md` says: it prints the claim next to the answer, and the build is
red until the doc is fixed. The diff is the finding.

Every mutation is applied to a throwaway copy. The vault is never edited, and
`--proof` fingerprints the whole tree before and after to show it.

## What the proof does and does not prove

`--proof` checks that each red fires where it should. It does not check that
the auditors are *good*, only that these three failures are caught. To see the
proof itself fail, loosen an auditor on a copy (make the figure pattern in
`coherence.py` unable to match, or make `world.py` skip the comparison) and run
`--proof` there: the matching row says `WRONG` and the exit code is 1. A guard
whose silence you have never seen fail is a guard you cannot trust, because
silence prints exactly like green.

## What it leaves out on purpose

The real catalog (`skills/vaultwatch/references/auditor-checks.md`) has more:
identity constants as literals in code, table hygiene, strikethrough
discipline, anchors that cannot be silenced, the retired-values register, the
mutation sweep. This demo keeps three coherence checks and one assertion so the
mechanism fits on one screen. To build the full thing for your own project, use
the skill: `skills/vaultwatch`.

## Make it yours

Change the price in `state/price.md` without changing `world/served.json` and
run `./demo.sh`: red, with the doc and the world side by side. Then fix the
doc, not the auditor.
