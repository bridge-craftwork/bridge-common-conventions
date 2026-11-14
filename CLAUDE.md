# Claude Code Notes — bridge-common-conventions

## What this repo is

Content, not code: card-independent convention definitions, common names for
card settings, and the `.bid` rule files for rusty-bidding-bot. The card tools
(`convention-card`) and the engine (`rusty-bidding-bot`) read it at run time.

**Read [docs/PLAN.md](docs/PLAN.md) first.** It holds the decisions made, the
ones still open, and the phases. Update its status line and checklists as work
lands.

## Ground rules

- **Definitions name no card.** No card paths, no `.play`, no card model. A
  convention says which context it applies in; each card model decides where
  that prints.
- **Names are additive-only.** Never rename or remove a name without a
  migration in `migrations/`, and never delete a migration.
- **Nothing is committed back to `main` by CI.** The built snapshot goes to
  the `published` branch.
- **Rules are published as source text**, never compiled.
- **Cite sources, never copy them.** References are citations with the date
  used; entries are not deleted when a link dies.
- **Generated examples name their bidder.** They show what one bidder does;
  `.test` files hold what a person has asserted.

## Git

- SSH, not HTTPS. Remote: `git@github.com:bridge-craftwork/bridge-common-conventions.git`
- Org repo, no forks: branch, PR, merge to `main`.
- When moving files in from another repo, keep their history
  (`git filter-repo`).

## Sibling checkouts

In `/Volumes/Express2T/Development/GitHub/`:
- `convention-card` — card tools and card models; the names' current home.
- `rusty-bidding-bot` — the engine; the rule files' current home.
- `dealer3` — generates deals from dealer scripts.
- `Practice-Bidding-Scenarios` — over 300 dealer scripts, tagged by convention.
- `Bridge-Classroom` is at `/Users/rick/Development/GitHub/Bridge-Classroom`.
