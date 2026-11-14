# bridge-common-conventions

Common bridge conventions for the bridge-craftwork tools: what each convention
is called, where it applies, the treatments it has, and (where we have them)
bidding rules for [rusty-bidding-bot](https://github.com/bridge-craftwork/rusty-bidding-bot),
a dealer script, and references.

The definitions are independent of any convention card. The card tools in
[convention-card](https://github.com/bridge-craftwork/convention-card) map each
card format's boxes onto the names defined here.

This is the set bridge-craftwork maintains, not a registry of every
convention. Anyone can publish their own conventions in a repo of the same
shape, without asking.

**Status: being set up.** Nothing reads this repo yet. See
[docs/PLAN.md](docs/PLAN.md).

## Reading it

Tools do not read `main`. Each push to `main` that passes its checks is
published to the [`published`](../../tree/published) branch as two files:
`pack.json`, the whole pack as one JSON document, and `manifest.json`, which
says what it was built from. [docs/CONTRACT.md](docs/CONTRACT.md) is what a
reader can rely on.

## Seeing what is defined

The published branch also carries a page that lists every convention and
treatment, with what each has behind it (bidding rules, tests, notes,
sources, a function it fills) and a switch to highlight what changed
lately. Its source is [site/index.html](site/index.html); it reads
`pack.json` and `manifest.json` from beside it. To see it for a checkout:

    python3 scripts/build_snapshot.py --out /tmp/snapshot
    cp site/index.html /tmp/snapshot/
    python3 -m http.server --bind 127.0.0.1 --directory /tmp/snapshot

## Changing it

Open a pull request. The [Publish workflow](.github/workflows/publish.yml)
checks the definitions, has the engine check every rule file and run every
`.test` case, and builds the snapshot; a problem is reported with its file
and line. To run the same locally:

    python3 scripts/check.py
    rbb bid check . --rules .
    git ls-files '*.test' | xargs rbb bid test --rules . --cards PATH/TO/rusty-bidding-bot/cards/bbsa
    python3 scripts/build_snapshot.py --out /tmp/snapshot

## Licence

MIT OR Apache-2.0, at your option (`LICENSE-MIT`, `LICENSE-APACHE`).
