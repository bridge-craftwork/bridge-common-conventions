# Project plan

How this repo gets from empty to being the one place bridge-craftwork's tools
read conventions from. Written 2026-11-13 from a design review of
`convention-card` and `rusty-bidding-bot` (Rick Wilson with Claude).

Status: **Phase 0 done (contract accepted 2026-11-13). Phases 1 to 3 are
drafted and await Rick's review: the inventory (PR #59), the "before"
capture (#60), and the content moved, restructured and converted to rule
language 2 (#61). On the 22 public cards the engine bids from this pack
with no difference over 122,430 auctions. On 25 hand-made cards (Rick's own,
captured outside this repo, 2026-11-14) 5,772 of 139,125 auctions change, all
where the card fills in a convention's treatments without ticking it and the
upgrade now plays it (Stayman on 24 cards, Texas and support doubles on
one each). `convention-card`'s JavaScript library reads its vocabulary from
the pack's snapshot (`scripts/build_snapshot.py`) and reads every card into
what it means in schema 3, by the same rules as the crate (18 shared cases;
identical output on those 47 cards). Its exported card files are schema 3.
Inside, it still works in schema 2's paths. The other exports are
byte-identical for the 22 public cards; on the 25 hand-made ones the only
changes are boxes for conventions the upgrade now plays (3NT raise on ten
cards; Drury, Texas and support doubles on one each). Not yet: the editor's
save to its host, the card embedded in a PDF and the hand-off link still
carry the working form, and the editor's catalogue and the format maps still
name things by path.**

Rulings on the upgrade (Rick, 2026-11-14): a convention shown only in a note
is played, since some cards have no box for it; where two conventions want
one function, the one the card ticks or names wins over the one inferred
from a note. For Phase 5: the Bridgodex "4NT: more" line is filed under
Blackwood whatever it says (on Rick's cards it describes keycard's 0314 in
the minors), and with Stayman unset v0.15.3 plays it over 2NT but not 1NT.
Also for Phase 5: the PDF maps, the editor's catalogue and the BBO and
Bridgodex maps ask for some fields by an older spelling
(`other_conventions.gerber.play` for `slam.gerber.play`) and read the card
literally, so a card holding the current spelling prints no Gerber box. It
affects 19 of the 22 public cards today (Gerber, "Majors Limit+", the
Lebensohl response). Making path reads follow a field's spellings fixes it;
it was measured and held back as a correction.
Work is tracked as
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

## Decisions settled in Phase 0

Rick Wilson, 2026-11-13. Each is recorded in full on its issue; the format
that follows from them is [CONTRACT.md](CONTRACT.md), tested on three real
conventions in [WORKED-EXAMPLES.md](WORKED-EXAMPLES.md).

| Question | Decision | Issue |
|---|---|---|
| The context list | Fourteen contexts, below. A convention lists one or more; the first is its main one | #2 |
| The card's new shape | `conventions`, keyed by ID, each entry holding `play` (true when left out) and treatment values; and `settings`. Schema version 3 | #3 |
| What gets its own entry | The same calls in a different auction are one convention with a treatment per place. Otherwise what can be played without the other gets an ID, and what only modifies it is a treatment. The 83 switches become 76 conventions, with 7 new IDs | #3 |
| How a rule file names what it reads | `convention <id>` identifies and switches. Three address shapes: an ID, `<id>:<treatment>`, a dotted setting. Rule language 2 | #4 |
| Directory layout | Below. Rule files sit beside their definition when they carry the header, otherwise under `rules/` | #5 |
| The tie-breaker between candidate calls | Module name, in place of file path | #5 |
| Conventions that cannot be played together | Each `implements` a function (`defence_to_1nt`, `ace_ask`, `opening`), listed in `functions.toml`. No convention names another; the editor and the engine find conflicts from the functions. A card entry narrows with `for` | #3 |
| Whether Reverse Drury is a style of Drury | Yes, and the same for all nine treatments that name another convention. Each keeps its ID and points at its parent | #6 |

### What the measurements corrected

Re-measured on `convention-card` v0.44.0 and `rusty-bidding-bot` v0.15.3.

- The field counts hold: 648 fields, 83 `play` switches, 95 treatments, 72
  lone yes/no fields, 9 treatments naming another convention.
- **The 83 switches name only 70 IDs.** Fifteen switches share six IDs and
  three have none.
- **The "27 convention modules with no card switch" are switched.** Sixteen
  read their own `play` through a `param`, four are chosen by the
  defence-to-1NT setting, and seven read lone yes/no fields or another
  group's treatments. None needs classifying as part of the system.
- **Only 43 of the 107 modules are one convention's rules.** The rest are
  several conventions in one file, on by a variant alone, on two ways,
  system or judgement.
- **File order changes bids.** Over 3,319 test cases and 10,000 deals, a
  flat alphabetical order changed no test and 1 auction; a reversed order
  changed 10 tests and 24 auctions.

### Contexts

| Key | Display name | Rusty folder today | Card section today |
|---|---|---|---|
| `notrump_openings` | Notrump openings | `notrump` | notrump |
| `major_openings` | Major openings | `majors` | major_openings |
| `minor_openings` | Minor openings | part of `base` | minor_openings |
| `preemptive_openings` | Two-level and preemptive openings | `openings` | two_level, preempts |
| `responses_rebids` | Responses and rebids | part of `base` | other_conventions |
| `slam` | Slam bidding | `slam` | slam |
| `overcalls` | Our overcalls | part of `competitive` | overcalls, nt_overcalls, direct_cuebids |
| `doubles` | Our doubles | part of `competitive` | doubles |
| `after_interference` | After they interfere | parts of `competitive` and `notrump` | vs_to_double, parts of notrump and competitive |
| `vs_notrump` | Defence to their notrump | part of `competitive` | part of competitive |
| `vs_openings` | Defence to their other openings | part of `competitive`, one in `openings` | vs_preempts, part of competitive |
| `leads` | Leads | none | leads |
| `signals` | Signals | none | carding |
| `general` | General approach | system modules | general |

### Layout

```
bridge-pack.toml                   the pack's name and three format numbers
conventions/<category>/<name>/     the directory path is the ID
    convention.toml                definition: name, contexts, treatments,
                                   summary, level, names, deals, references
    <module>.bid  .test  .notes.md rules, when the file carries the
                                   `convention` header
    <name>.dlr                     dealer script, where inline
    examples.pbn                   curated hands with expert auctions
rules/<folder>/                    every other rule file: several conventions
                                   in one module, system, judgement
settings/<section>.toml            card settings: common names
contexts.toml  functions.toml  levels.toml  alerts.toml
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
- Worked examples (`docs/WORKED-EXAMPLES.md`): Texas transfers, Bergen
  raises and DONT written in the new format, with what they showed.

**Done when** Rick accepts the contract. Accepted 2026-11-13.

### Phase 1: the inventory

One reviewed table: every current card field, and what it becomes.

- A script that generates the table from `convention-card`'s
  `spec/fields.toml`: the 83 `play` switches become 76 conventions, their 95
  treatments become treatments, everything else stays a setting for now.
- Each convention's context filled in. The card's `competitive` section
  (21 switches) needs placing by hand.
- Each rule module's place: beside a definition, or under `rules/` and why.
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
- `rusty-bidding-bot`: rule language 2. The `convention` header on the 43
  modules switched by their own convention; the three address shapes on
  every `card` and `param` line; the module name as the tie-breaker.
- Functions for the choices cards already make: `defence_to_1nt` (the two
  `vs_1nt_*.system` settings become entries, with today's precedence kept
  by the migration), `ace_ask` (Blackwood, Roman Keycard) and Michaels over
  preempts (Leaping, Non-leaping). Conflicts are reported, never acted on.

**Done when** every phase 2 comparison shows no difference at all, in two
steps: today's rules under the new tie-breaker against today's rules under
the old one, giving a short list reviewed once; then the restructured
content against that, with no difference.

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

Status (2026-11-14): the workflow is `.github/workflows/publish.yml`. On a
pull request it checks the definitions, has the engine check every rule file
and run every `.test` case, and builds the snapshot; on a push to `main` it
then pushes `pack.json` and `manifest.json` to `published`. A daily run
checks that the snapshot is not behind (`scripts/staleness.py`). Until an
engine release reads rule language 2, the engine is built from a pinned
commit (`.github/engine.env`) and cached. The rule tests name the engine's
stock cards (`card 21GF-DEFAULT`), which come from the engine's repository.
Left for the cut-over: showing and logging the rules number in Bridge
Classroom and Rusty (#28), and the template repository (#30).

### Phase 5: core corrections

Each produces a small, expected difference against phase 2.

- The nine treatments that name a different convention from their group:
  Reverse Bergen, Reverse Drury, two-way Drury, Modified Jacoby 2NT,
  Puppet Stayman (two), super-accepts (two), the Parrish relay.
- Bergen's notes moved under Bergen; Texas given its own ID.
- "Treatments mean nothing while their convention is off", enforced in
  one place in the library and the crate. Today Bergen, Drury and fourth
  suit forcing are switched on by a treatment alone.
- ~~The `opening` function: Weak Twos, Multi, Mini-Roman, Flannery and the
  other two-level openings claim their bids, and the three `meaning`
  settings with `plays` give way to entries.~~ Done 2026-11-14, with two new
  IDs (Strong two-bids, Intermediate two-bids). Left out: Multi taking 2♥
  and 2♠ from the weak twos, which the rules still decide themselves.
- Reverse Flannery is responder's jump to 2♥ or 2♠ over one of a minor, not
  an opening (Rick, 2026-11-14): its definition is corrected and it fills
  `jump_to_major_over_minor`, as do Weak jump shifts and the new Strong jump
  shifts. The eight jump-shift boxes are treatments of those two conventions
  (#68, done 2026-11-14), each convention filling the function only while
  its two-level treatment is on. Still to do: Reverse Flannery's card fields
  sit in the two-level openings section, and it has a `two_d` treatment with
  no rule (#69).
- Found with #68: eight hand-made cards tick "weak jump shifts, not in
  competition" (the Bridgodex and BBO box) and bid none, because the rules
  read only the two-level box, which those formats do not set (#74).
- ~~Kickback and Minorwood claim `ace_ask.minor`.~~ Changed (Rick,
  2026-11-14): they fill a function of their own, `low_keycard_ask`, beside
  keycard's 4NT.
- The bbsa map sets a convention's switch where a BBA file has lines only
  for its treatments (fourth suit forcing: on when either line is on).
- Rule modules that gain the `convention` header move beside their
  definition.
- The editor draws a convention's row and its treatments from the
  definition, replacing the hand-written list in `conventionCatalog.js`.
  Row captions move into the definitions.

Found on the way and tracked as issues: the default for jump shifts after
an overcall (#67), the jump-shift boxes becoming entries (#68), Reverse
Flannery's leftovers (#69), Multi and the majors (#70), tools reading fields
by an older spelling (#71), the Bridgodex 4NT line (#72), and Stayman unset
over 2NT against 1NT (#73).

**Done when** every difference from phase 2 is on a reviewed list.

### Phase 6: place the 72

With the new arrangement visible, each lone yes/no field becomes a
convention, a treatment of an existing one, or stays a setting.

- The two "2NT raise over a takeout double" box groups, which stay settings
  until here: a function for 2NT over their takeout double (major, minor)
  that Jordan implements; the limit boxes become a Jordan entry; the point
  ranges stay settings (Rick, 2026-11-13).

**Done when** the inventory has no unplaced rows and the differences are
reviewed, as in phase 5.

### Phase 7: cut over

- New tags in `convention-card` and `rusty-bidding-bot`.
- Pin bumps in Bridge Classroom and Better BBO Convention Card.
- Cards converted from BBA files are converted again from their source,
  not migrated. Hand-made cards are few and take the schema 2 to 3
  migration: a convention with its switch unset becomes an entry when a
  treatment is on or filled in, and no entry otherwise.
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
