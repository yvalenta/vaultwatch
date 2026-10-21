# HANDOFF — demo vault

Cold-start door. What exists, what works, what is pending. No figures here:
every figure lives at its assertion site under `state/`.

## What exists

A toy service, `world/server.py`, that sells one thing over HTTP and reports
how much traffic it saw. The vault below describes it.

- [state/price.md](state/price.md) — what the endpoint charges (assertion)
- [state/traffic.md](state/traffic.md) — how busy it is (snapshot)
- [laws/never-write-what-it-will-print.md](laws/never-write-what-it-will-print.md)
- [history/2026-first-lie.md](history/2026-first-lie.md)

Notes on disk: state=2 laws=1 history=1

## What can be done now

| Direction | Status |
|---|---|
| Keep the vault green before and after every session | rule #1 |
| Add a row to `audit/world.py` for any new claim in `state/` | open |

## Pending

Nothing.
