# The inventory

Phase 1 of [the plan](../docs/PLAN.md): every card field, convention and rule
module as it is today, and what each becomes under
[the contract](../docs/CONTRACT.md). It drives the content move and the
schema 2 to 3 card migration, so neither is written by hand.

| File | Rows | What it is |
|---|---|---|
| [decisions.toml](decisions.toml) | | The hand decisions: new IDs, places, contexts, functions. The only file edited by hand |
| [fields.csv](fields.csv) | 648 | Every card field and what it becomes |
| [conventions.csv](conventions.csv) | 184 | Every ID, with its contexts, treatments, function and rule modules |
| [modules.csv](modules.csv) | 107 | Every rule module, what switches it, and where it will sit |
| [SUMMARY.md](SUMMARY.md) | | Counts, and anything the script could not place |

Regenerate with `python3 scripts/inventory.py`. It reads `convention-card`
and `rusty-bidding-bot` at the tags named in `decisions.toml`, through git,
from sibling checkouts.

## What to review

These are choices a script cannot make. Each is one line in
`decisions.toml`.

1. **The names of the place treatments.** Lebensohl:
   `over_1nt_interference`, `after_weak_two_double`. Rubensohl:
   `over_1nt_interference`, `after_double`. Unusual notrump: `at_1nt` to
   `at_4nt`. A bare entry plays the main place only (Lebensohl over 1NT
   interference, the Unusual 2NT).
2. **The contexts**, above all the 21 switches of the card's `competitive`
   section and the conventions listed under two.
3. **The 102 IDs with no switch today** have no context yet. Most are
   skills that never appear on a card, where the contract leaves the context
   out; the rest get one when their definitions are restructured.
4. **The `later` column of `modules.csv`**: what Phase 5 or 6 could do with
   each convention module that gets no `convention` header in Phase 3.
