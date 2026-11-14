# Project plan

How this repo gets from empty to being the one place bridge-craftwork's tools
read conventions from. Written 2026-11-13 from a design review of
`convention-card` and `rusty-bidding-bot` (Rick Wilson with Claude).

Status: **Phase 0 not started.** Work is tracked as
[milestones](https://github.com/bridge-craftwork/bridge-common-conventions/milestones)
(one per phase) and issues; the lists below are the outline. Update the status
line as phases complete.

## Why this repo exists

Today a convention is defined in two places, and both are code releases:

- `convention-card` holds the names: 177 conventions and 648 card fields in
  `spec/`.
- `rusty-bidding-bot` holds the bidding rules: 107 `.bid` modules in
  `conventions/`, compiled into its binary.

Rusty compiles the field list in at a tag, so adding or renaming a convention
means a tag in `convention-card` and a pin bump in every consumer. In its
first six weeks `convention-card` cut 63 tags, most of them for content. The
route meant for other people's conventions (namespaced IDs carried in a
card's `other_agreements`, `convention-card` ADR-0001) is built only as a
data type: the editor, Rusty, Practice-Bidding-Scenarios and lesson-studio do
not honour it. So the only working way to add a convention is to add it to
our repos, which makes us the authority on every convention. We don't want
that role.

The fix is to separate **content** from **code**:

- **Content** (this repo, and anyone else's repo in the same shape) is read at
  run time and is never pinned.
- **Code** (the card tools, the bidding engine) is pinned by tag, and its tags
  move only when behaviour changes.
- **Formats** carry the version numbers: code declares which card format,
  pack format and rule language it reads.

## What lives where

| Here: names and rules | `convention-card`: card tools and card models | `rusty-bidding-bot`: the engine |
|---|---|---|
| Convention definitions: ID, name, context, treatments, summary, level, names people write | Editor, PDF and import/export code, the `bridge-card` crate | The rule language, engine, CLI and WASM build |
| Card settings: common names for agreements that are not conventions (ranges, lengths, carding, leads) | Card models: PDF templates, fonts, layouts | dealer3, built in, to run dealer scripts |
| Contexts, level bands, alert rules per regulator | Maps from each card model's boxes onto the common names (ACBL Classic and New, BBO, Bridgodex, `.bbsa`) | |
| Bidding rules (`.bid`, `.test`, `.notes.md`): systems, judgement and conventions | Where each card model prints a context's write-ins | |
| Dealer scripts, references, generated example deals | | |
| Migrations for any rename | | |

Someone else's repo holds any subset of the left column, in the same layout.

## Decisions already made

Rick Wilson, 2026-11-13, unless noted.

1. **Definitions are card-independent.** A definition has an ID, a name, a
   context hint, its treatments, and optionally rules, tests, a dealer script
   and references. It names no card path and no card model. `.play` is how one
   card file stores "we play this"; it is not part of a convention.
2. **IDs stay as they are**: the skill paths (`bidding_conventions/stayman`),
   which began as Baker Bridge's teaching categories and are not card
   sections.
3. **A card has two parts**: the conventions it plays, by ID, each with its
   treatment values; and settings, the agreements that are not conventions.
4. **System and judgement rules live here too, for now**, beside the
   conventions that depend on them, even though judgement is Rusty-flavoured.
   Precision and Acol are expected soon and go in this repo.
5. **Names are additive-only.** Nothing is renamed or removed without a
   migration shipped in this repo. A full refresh of the names is allowed
   later, while nothing outside bridge-craftwork depends on them.
6. **CI publishes a built snapshot to a separate branch.** It checks the
   rules, bundles everything into one file, and writes a manifest (per-file
   hash and last-changed date, the source commit, a rules number). Readers use
   only that branch. Nothing is committed back to `main`, and rules are
   published as source text, never compiled.
7. **Versions are tracked separately** for the engine, the rules, the
   vocabulary and the card, and every logged result carries all of them, so a
   change in daily Brill Challenge results can be traced to a rule file or to
   the engine.
8. **A definition may carry a dealer script**, inline or by URL, for testing,
   demonstration and practice. dealer3 is built into `rbb`, which validates the
   script with the rules. Targeted deals are the iteration step for A/B work;
   the full corpus run stays as the required final step, because targeted
   deals cannot show a module firing where it shouldn't.
9. **Example deals with auctions are generated at publish**, labelled with
   the bidder that produced them (Rusty, BBA, Brill). They are examples, not
   definitions: another bidder may bid them differently.
10. **References are a structured list per convention**: each with a role
    (basis or about), a kind (published or personal), and the date it was
    used. Entries are never deleted; a dead link gets a `gone` date. Sources
    are cited, never copied.
11. **A definition may carry curated example hands**: chosen deals, usually
    the troublesome ones for the convention, each with an auction a named
    expert gives for it. Brill's definitions are the first source. They are a
    reference for people and a targeted test set for bidders, and they are
    kept apart from generated examples: a curated auction is someone's
    stated answer, a generated one is only what a bidder did. A bidder that
    differs from a curated auction is reported, not failed, since judgement
    differs. They are added only with their author's agreement, and record
    who gave the auction and when.
12. **One cut-over.** Every consumer stays on its current tags until the new
    arrangement is complete, then moves once. No period with two styles.
13. **Licence: MIT OR Apache-2.0**, matching both source repos.

## Decisions still open

Phase 0 closes these. Each has a proposal from the review.

| Question | Proposal |
|---|---|
| The context list | Fourteen contexts, below |
| The card's new shape | `conventions` (by ID, with treatment values) and `settings`; schema version 3 |
| How a rule file names what it reads | A `convention <id>` header in place of `card <path>.play`; a treatment by its name; a setting or another convention's treatment named explicitly |
| Directory layout here | Below |
| Whether Reverse Drury is a style of Drury | Yes, as for Bergen; needs `convention-card` decision 16 amended |
| What the 27 convention modules with no card switch are | Classify each as a convention needing a switch, or part of the system |

### Proposed contexts

From cross-checking Rusty's rule folders against the card's sections.

| Context | Rusty folder today | Card section today |
|---|---|---|
| Notrump openings | `notrump` | notrump |
| Major openings | `majors` | major_openings |
| Minor openings | part of `base` | minor_openings |
| Two-level and preemptive openings | `openings` | two_level, preempts |
| Opener's and responder's rebids | part of `base` | other_conventions |
| Slam bidding | `slam` | slam |
| Our overcalls | part of `competitive` | overcalls, nt_overcalls, direct_cuebids |
| Our doubles | part of `competitive` | doubles |
| After they interfere | parts of `competitive` and `notrump` | vs_to_double, parts of notrump and competitive |
| Defence to their notrump | part of `competitive` | part of competitive |
| Defence to their other openings | part of `competitive`, one in `openings` | vs_preempts, part of competitive |
| Leads | none | leads |
| Signals | none | carding |
| General approach | system modules | general |

A convention may list more than one context.

### Proposed layout

```
conventions/<category>/<name>/     the directory path is the ID
    convention.toml                definition: name, context, treatments,
                                   summary, level, names, deals, references
    <name>.bid  .test  .notes.md   rules, where we have them
    <name>.dlr                     dealer script, where inline
    examples.pbn                   curated hands with expert auctions
systems/<system>/                  a system's base rules and judgement
settings/                          card settings: common names
contexts.toml  levels.toml  alerts.toml
migrations/                        every rename, permanent
docs/                              this plan, the contract
```

## Phases

Each phase lists what it delivers and how we know it is done; each is a
milestone, and each item an issue. Phases 3, 5 and
6 are the cut-over's three steps: they are developed on branches and released
together in phase 7.

### Phase 0: the contract

Settle the open decisions and write them down before any content moves.

- `docs/CONTRACT.md`: the definition format, the pack and manifest
  format, the card's shape, what the rule language reads, the additive-only
  promise, format version numbers.
- An ADR in `convention-card` (ADR-0003) recording the split and amending
  ADR-0001's Amendment 1 and decision 16.
- The context list, final.

**Done when** Rick accepts the contract.

### Phase 1: the inventory

One reviewed table: every current card field, and what it becomes.

- A script that generates the table from `convention-card`'s
  `spec/fields.toml`: the 83 `play` switches become conventions, their 95
  treatments become treatments, everything else stays a setting for now.
- Each convention's context filled in. The card's `competitive` section
  (21 switches) and the 27 always-on modules need placing by hand.
- The 72 yes/no fields that name a convention but have no group are
  listed and left as settings. They are placed in phase 6.

**Done when** Rick has reviewed the table. It drives the content move and the
card migration, so nothing downstream is written by hand twice.

### Phase 2: capture "before"

Record current behaviour, from the current tags, before anything changes.

- A card corpus: the 11 cards saved in Bridge Classroom, the 18
  Practice-Bidding-Scenarios cards, Rick's Bridgodex and BBO cards.
- For each card, every export from `convention-card` v0.44.0: both ACBL
  PDFs' field values, `.bbsa`, BBO, Bridgodex, card JSON.
- For each card over a fixed deal set, Rusty's auctions, explanations and
  alerts, and the list of settings it reads and ignores.
- For each card, the rows and values the editor shows.

**Done when** the captures are stored and a script can regenerate and compare
them. Cards saved in Bridge Classroom are its users' data: they and anything
captured from them stay out of public repos. The PBS cards and their captures
can be committed.

### Phase 3: move the core, with no behaviour change

- Convention files moved from `convention-card` `spec/conventions/` and
  rule files from `rusty-bidding-bot` `conventions/`, with their history
  (`git filter-repo`).
- Restructured into the layout above from the inventory.
- Settings, level bands, alert rules and the existing 1-to-2 migration
  moved.
- `convention-card`: reads content through one loader that takes a URL or
  a file; reads and writes the new card shape; migrates schema 2 cards.
- `rusty-bidding-bot`: the `convention` header; treatments read by name;
  the 52 switched modules converted.

**Done when** every phase 2 comparison shows no difference at all.

### Phase 4: the publish pipeline

- A CI workflow that validates the rules and scripts (Rusty's WASM build
  under Node, so no Rust toolchain is needed), runs the `.test` files,
  bundles, writes the manifest and pushes to the `published` branch.
- The rules number, derived from history, shown beside the engine version
  in Bridge Classroom and written to Rusty's logs.
- A staleness check: published source commit against the head of `main`.
- The workflow and layout as a template repo for other people's
  conventions.

**Done when** a push to `main` produces a consistent snapshot, and a failing
rule file blocks it with a file and line.

### Phase 5: core corrections

Each produces a small, expected difference against phase 2.

- The nine treatments that name a different convention from their group:
  Reverse Bergen, Reverse Drury, two-way Drury, Modified Jacoby 2NT,
  Puppet Stayman (two), super-accepts (two), the Parrish relay.
- Bergen's notes moved under Bergen; Texas given its own ID.
- "Treatments mean nothing while their convention is off", enforced in
  one place in the library and the crate.
- The editor draws a convention's row and its treatments from the
  definition, replacing the hand-written list in `conventionCatalog.js`.
  Row captions move into the definitions.

**Done when** every difference from phase 2 is on a reviewed list.

### Phase 6: place the 72

With the new arrangement visible, each lone yes/no field becomes a
convention, a treatment of an existing one, or stays a setting.

**Done when** the inventory has no unplaced rows and the differences are
reviewed, as in phase 5.

### Phase 7: cut over

- New tags in `convention-card` and `rusty-bidding-bot`.
- Pin bumps in Bridge Classroom and Better BBO Convention Card.
- Bridge Classroom fetches the published snapshot and hands it to the
  editor and to Rusty.
- Practice-Bidding-Scenarios and lesson-studio validate IDs against the
  published snapshot (today PBS checks against nothing, and lesson-studio
  against a stopgap copy).
- `spec/conventions/` and the field list removed from `convention-card`;
  `conventions/` removed from `rusty-bidding-bot`.
- Docs corrected: `convention-card`'s CLAUDE.md pins, Rusty's DESIGN.md
  links to `conventions/card/`.

**Done when** no other repo holds a copy of the names or the rules.

### Phase 8: deals and references

Additive, so it follows the cut-over.

- dealer3's parser and run crates built into `rbb`; scripts validated by
  the same check as rules.
- `deals` entries on definitions, starting from the PBS scripts (over 300,
  214 of 343 scenarios already tagged with a convention). The definition
  is the source for "this is the convention's own scenario"; CI checks
  PBS's tags agree.
- Example deals generated at publish, each stamped with script, seed,
  rules, engine, card and bidder; the convention's own calls marked; only
  deals where the convention fired are kept, and the rate is reported.
- Curated example hands (decision 11): the format, with each hand's
  source, author and date; a report of where each bidder's auction
  differs from the curated one. Brill's hands first, with Thorvald
  Aagaard's agreement: he plans to drop them from his own scripts, so
  this would become their home.
- `references` migrated from the definitions' `see` lists and the Sources
  sections of the `.notes.md` files. A link check that reports and never
  blocks.

## Needed for other people's repos, not for the cut-over

The cut-over uses one pack, so these do not block it. They do block loading a
second pack beside ours.

- **Layering.** Rules supplied to Rusty's WASM replace the built-in set today;
  they need to be laid over a base.
- **The conflict check.** The rule language documents one, and `replaces`, but
  neither is implemented: overlapping modules are settled by priority and file
  order, silently.
- **System switches.** The 21 system modules are always on. Each system's
  modules must switch on from the card's system setting before Precision or
  Acol is added.
- **Limits for untrusted rule text**: expression depth and run time.
- **The editor** adding a convention from a loaded pack, and a file upload for
  people without a GitHub repo.

## Later

- Dealer scripts that take parameters from the card (a 12 to 14 notrump).
- Reading other people's cards for the Brill Challenge: a partner's or
  opponent's card against yours, and what their alerts mean.
- Storing a range end as one value ("14+"), which removes 56 marker fields.
- A refresh of the common names, under decision 5.

## Risks

- **A rename breaks everyone at once.** With no pins, a bad change reaches
  every user on the next load. The additive-only rule, the CI gate and the
  separate published branch are the protection; the manifest's source commit
  is the way back.
- **The no-difference test hides intended changes** if restructuring and
  corrections are mixed. Keep phases 3 and 5 separate even on one branch.
- **Examples read as definitions.** Generated auctions show what one bidder
  does. Always label the bidder; `.test` files hold what a person has
  asserted.
- **CI silently off.** A stale snapshot looks healthy. The staleness check is
  part of phase 4, not an extra.
