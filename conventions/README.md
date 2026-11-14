# Conventions

One directory per ID: `<category>/<name>/`, and the path is the ID.
`bidding_conventions/stayman/` is `bidding_conventions/stayman`.

| In a convention's directory | |
|---|---|
| `convention.toml` | The definition: what it is called, where it applies, its treatments, where to read more |
| `<module>.bid`, `.test`, `.notes.md` | Its bidding rules, their tests and the notes behind them, when the rules are for this convention alone |

The format is [the contract](../docs/CONTRACT.md), section 4. A definition
names no card: it says which contexts it applies in, and each card model
decides where that prints.

`categories.toml` gives each category (an ID's first segment) its display
name.

A skill that never appears on a card (declarer play, basic bidding) has a
definition too, with no `contexts`: lessons and practice deals are tagged
with the same IDs.

Rules that serve more than one convention, or the system as a whole, are in
[`rules/`](../rules/).
