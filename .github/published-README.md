# The published snapshot of bridge-common-conventions

This branch is written by CI. Do not edit it: change `main`, and a snapshot
that passes its checks replaces this one.

| File | Holds |
|---|---|
| `pack.json` | The whole pack as one JSON document: definitions, settings, contexts, functions, levels, alerts and migrations, and every rule, test and notes file as its source text, keyed by path |
| `index.html` | A page that lists what the pack defines and what each convention has behind it, drawn from the two files below. Served by GitHub Pages |
| `manifest.json` | The commit of `main` it was built from, the rules number, the format numbers, the engine it was checked with, and each source file's hash and the date it last changed |

A snapshot is published only when the definitions pass their check, every
rule file loads, and every `.test` case passes. The contract a reader can
rely on is `docs/CONTRACT.md` on `main`.

To tell whether this snapshot is current, compare `source_commit` in the
manifest with the head of `main` (`scripts/staleness.py` there does it).
