# Project plan

How this repo gets from empty to being the one place bridge-craftwork's tools
read conventions from. Written 2026-11-13 from a design review of
`convention-card` and `rusty-bidding-bot` (Rick Wilson with Claude).

Status: **Phases 0 to 6 are done and merged (2026-11-14). The pack is
published from `main` to the `published` branch (rules number 19) and the
overview page is live. Phase 5's corrections and Phase 6's placements are
each recorded below with what they measured on the 22 public cards (122,430
auctions) and on 25 hand-made cards captured outside this repo (139,125).
Next is Phase 7, the cut-over: `convention-card` (draft PRs #120 and #121)
and `rusty-bidding-bot` (draft PR #90) read the pack on branches and stay
unmerged until everything moves at once. Still open from Phase 5: the
editor's remaining rows (#34), weak jump shift ranges (#86), four sources
not found (#47).**

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

- ~~The nine treatments that name a different convention from their group:
  Reverse Bergen, Reverse Drury, two-way Drury, Modified Jacoby 2NT,
  Puppet Stayman (two), super-accepts (two), the Parrish relay.~~ Done
  2026-11-14 (Rick's rulings): Puppet Stayman and Modified Jacoby 2NT are
  conventions of their own, each filling a function its parent also fills;
  the other seven are styles of their parent (`style_of`).
- Bergen's notes moved under Bergen; Texas given its own ID.
- ~~"Treatments mean nothing while their convention is off", enforced in
  one place in the library and the crate. Today Bergen, Drury and fourth
  suit forcing are switched on by a treatment alone.~~ Done 2026-11-14 in
  the crate's `effective`: where the card says it does not play a
  convention, its treatments read as unset. Found on the way: in BBA the
  Drury and Reverse Drury lines (and Bergen's) are alternatives, and 13
  stock cards play the reverse form with the plain line off, so the `.bbsa`
  map now reads either line as playing the convention. Five treatments that
  are separate lines in BBA are marked `independent`. Not done: the
  JavaScript library still shows what the card holds, gated or not.
- ~~With Stayman unset, played over 2NT but not 1NT (#73).~~ A silent card
  plays Stayman and Jacoby transfers in both (`convention <id> default
  true`). 614 of 139,125 auctions change on the nine hand-made cards that
  are silent on them.
- Closed without a change: Multi taking 2♥ and 2♠ from the weak twos (#70).
  A card that says its 2♥ is weak and ticks Multi says two things, and the
  card should keep both; the rules decide, as they do now.
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
  its two-level treatment is on. Its `two_d` treatment, left from the
  opening, is retired and its three alert rules for a 2♦ opening are gone
  (#69, done 2026-11-14). A card that ticked the old 2♦ box plays both
  jumps on upgrade, and a jump Reverse Flannery takes is no longer also bid
  as a strong jump shift (48 boards on one stock card, 100 on one hand-made
  card). Still to do: its card fields sit in the two-level
  openings section of schema 2, which the editor's layout decides (#34).
- ~~Found with #68: eight hand-made cards tick "weak jump shifts, not in
  competition" (the Bridgodex and BBO box) and bid none, because the rules
  read only the two-level box, which those formats do not set (#74).~~ The
  rules read either box. Measured: 1,152 of 139,125 auctions change on those
  eight cards (the strong jump shift gives way to a one-level response; a
  weak hand with a six-card suit now jumps). Found with it and fixed: the
  weak jump shift's follow-up rules also fired after a two-level response
  that was not a jump (1♦–2♣–2NT); 95 auctions change on the five public
  cards that play weak jump shifts.
- ~~Kickback and Minorwood claim `ace_ask.minor`.~~ Changed (Rick,
  2026-11-14): they fill a function of their own, `low_keycard_ask`, beside
  keycard's 4NT.
- ~~The bbsa map sets a convention's switch where a BBA file has lines only
  for its treatments (fourth suit forcing: on when either line is on).~~
  Done 2026-11-14 in `convention-card`, where the map lives: fourth suit
  forcing and Kickback. A convention with a line of its own (Drury beside
  Reverse Drury) is not derived.
- Rule modules that gain the `convention` header move beside their
  definition.
- The editor draws a convention's row and its treatments from the
  definition, replacing the hand-written list in `conventionCatalog.js`.
  Row captions move into the definitions. **Partly done 2026-11-14:** 46 of
  the 69 rows (a convention, or a place one is played) are drawn from the
  definition, whose `brief` holds the caption; the result is word for word
  the list as it was. Still written out by hand: the 23 rows that are a
  treatment shown as its own row, a setting, or one value of a choice, and
  the list of structured fields under each section (#34 stays open).

Found on the way and tracked as issues: the default for jump shifts after
an overcall (#67), the jump-shift boxes becoming entries (#68), Reverse
Flannery's leftovers (#69), Multi and the majors (#70), tools reading fields
by an older spelling (#71), the Bridgodex 4NT line (#72), and Stayman unset
over 2NT against 1NT (#73).

Done 2026-11-14, from the tracked list: tools read a field under any of its
spellings (#71, in `convention-card`; the Gerber box, "Majors Limit+" and
the Lebensohl response now print on the public cards that play them), and
the card's 4NT notes line is a setting, not a treatment of Blackwood (#72),
so it switches nothing on.

**Done when** every difference from phase 2 is on a reviewed list.

### Phase 6: place the 72

With the new arrangement visible, each lone yes/no field becomes a
convention, a treatment of an existing one, or stays a setting.

Placed 2026-11-14 (Rick's rulings the same day). Four had already gone to the
jump-shift conventions in Phase 5; of the other 68:

- **27 are a convention of their own, or its treatments** (13 conventions):
  XYZ; Two-way NMF (with `by_passed_hand`); Transfer Walsh; Transfers after
  a double; Mixed raise; Maximal doubles; DEPO; DOPI/ROPI (one convention,
  a place for each); Smith echo (`vs_nt`, `vs_suits`, `reverse`, of which
  Reverse Smith echo is a style); Trump suit preference; Lavinthal and
  Odd-even discards (`vs_nt`, `vs_suits`); Upside-down signals (attitude
  and count, against notrump and suits, and the first discard).
- **12 join a convention a card already held:** four places Michaels is
  played; the four single-raise strength boxes of Inverted minors, any of
  which means the card plays them; the specific-kings answer of Roman
  Keycard. Three boxes were the same agreement as a convention's own box and are now a
  second spelling of it: the 4♣/4♦ transfer (Namyats), the support cuebid
  (the cue-bid raise) and the jump 2NT for the two lowest unbid (Unusual
  2NT).
- **29 stay settings:** standard signals and which signal comes first (11),
  opening-lead agreements (10), BBA's four suit-preference situations
  ("Lavinthal on ace", "to void", "from void", "on trump"), reverses
  forcing, the double of a preempt being for takeout, and the forcing and
  semi-forcing 1NT response. Those two are settings of the 2/1 system
  (Rick), but as treatments of it a card that ticked "forcing 1NT" and was
  silent on 2/1 would be read as playing 2/1 (505 auctions on one hand-made
  card), so they stay settings until a treatment can belong to a convention
  without implying it. Signals and leads
  are a choice among methods spread over boxes; one choice setting each
  belongs with the refresh of the names (Later).

Measured on the 22 public cards (122,430 auctions) and 25 hand-made ones
(139,125): no auction changes on the public cards. On seven hand-made cards
844 change, all because they tick a single-raise strength box and so now
play Inverted minors (1♣ – 2♣ where they bid 3♣ or 2NT). The Michaels box
alone still means Michaels over every opening; a card that also says where
plays it only there. On printed cards and exports, a box that is now a
second spelling shows wherever its twin does (the "jump to 2NT, two lowest"
box on 18 public cards, the 4♣/4♦ transfer box on 7).

- ~~The two "2NT raise over a takeout double" box groups.~~ Done
  2026-11-14: `two_nt_over_takeout_double` (major, minor) is filled by
  Jordan 2NT in the place the card plays it. Jordan's own box and the
  majors' "limit or better" box are its `over_major` place; the minors'
  "limit or better" box is `over_minor`. The "limit" and "weak" boxes, the
  bare "2NT raise" boxes and the point ranges name no convention and stay
  settings (Rick, 2026-11-13, for the ranges). No rule reads Jordan over a
  minor yet.

- ~~Five treatments that stand on their own (`independent`) become
  places.~~ Done 2026-11-14 (#91): New Minor Forcing is played after a 1NT
  rebid and after a 2NT rebid; Texas, minor-suit Stayman and minor-suit
  transfers over 1NT and over 2NT (minor-suit transfers also in BBA's
  "2♠ to clubs" line). Each convention's old switch is its first place. A
  new function, `checkback_after_1nt_rebid`, is filled by New Minor Forcing
  (in that place), two-way NMF, Checkback, Roudi and XYZ; New Minor Forcing
  gives way to XYZ and to two-way NMF, as the rules already read it. No
  treatment is `independent` any more. The Texas rules read the two places:
  over 2NT if either box says so (most cards have one Texas box), over 1NT
  only if that box does. Measured: two cards say "Texas over 2NT" without
  the 1NT box, and now bid that (20 auctions on the stock SAYC card, which
  had no Texas; 59 on one hand-made card, which had it over 1NT too).

**Done when** the inventory has no unplaced rows and the differences are
reviewed, as in phase 5.

### Phase 7: cut over

#### Where each repo stands (2026-11-15)

| Repo | On `main` today | Ready on a branch | Still to do before the cut-over |
|---|---|---|---|
| This one | Phases 0 to 6, published (rules number 21) | | Nothing blocks. `engine.env` names an engine commit; it names the release tag once there is one |
| `convention-card` | v0.44.0: its own `spec/conventions/` and field list | Draft #120 (the crate reads a pack and schema 3 cards), #121 (the JavaScript library reads the bundled snapshot; every card it writes is schema 3: exported files, the editor's saves to its host, the card in a PDF, the hand-off link; the crate reads `pack.json`) and #123 (`spec/conventions/`, the field list, levels, alerts, migrations and their generated JSON removed; the crate's standard vocabulary is the bundled pack; schema 2's field list kept only as a frozen test fixture; its README, CLAUDE.md and design notes say where the content now lives) | The format maps and the rest of the editor catalogue keep schema 2's paths: the library reads both |
| `rusty-bidding-bot` | v0.15.3: its own `conventions/`, compiled in | Draft #90 (rule language 2, a pack read from its source tree), #91 (a pack read from `pack.json`, by `--rules` and by the WASM API's `pack`) and #92 (a copy of the snapshot compiled in and used by default, `conventions/` and `docs/SKILLS.md` removed, tests reading the copy, the rule checker page checking against the pack, pinned to the card tools without their field list; its docs describe the pack; `--rules-at` reads a pack as it was at a commit, with that commit's names, for before and after comparisons) | `rbb bid check`, `rbb bid test` and `--rules-at` need a folder, so a pack checkout. The examples in its LANGUAGE.md are still written with schema 2's names |
| Bridge Classroom | Pins the card tools by tag (v0.43.2) and the engine's WASM by release and hash (v0.15.2). Its server stores a card as it is given and reads only the partners' names in it; it has its own skills taxonomy | | Bump both pins (#38). Fetch the snapshot when it runs and hand it to Rusty (#39). Show the rules number (#28). Compare coverage through the library, which reads an address or a path. The service that renders its print links is upgraded first |
| Better BBO Convention Card | Pins the card tools by tag | | Bump the pin (#38) |
| Practice-Bidding-Scenarios, lesson-studio | Check IDs against nothing, or a stopgap copy | | Validate against the snapshot (#40) |

#### Decisions the cut-over needs

1. **How the engine carries its rules once `conventions/` is gone.**
   Settled in outline (Rick, 2026-11-15): rules evolve without a new
   build of the engine or of its hosts. A host fetches the published
   snapshot when it runs and hands it to the engine (the WASM API's
   `pack`, `--rules pack.json`). The engine also keeps a copy of
   `pack.json`, compiled in: the fallback when the snapshot cannot be
   fetched or is in a rule language the engine does not read, the default
   for `rbb` with no `--rules`, and the fixture for its own tests. A
   script refreshes that copy at each engine release, not at each rule
   change.
2. **Where the engine's own tests get rules.** Its Rust tests use the real
   rule files as fixtures. Agreed (Rick, 2026-11-15): they read the compiled-in snapshot;
   the rule tests (`.test`) run only here, in this repo's CI, as they do
   now.
3. **Whether the card library must load a pack at run time for the
   cut-over** (#22 in full). Agreed (Rick, 2026-11-15): no. Cut over on the bundled
   snapshot, which is one loader and works offline; a host-supplied pack is
   an addition afterwards (#52 needs it).
4. **Which rules a host follows, and the number it shows.** The newest
   published (Rick, 2026-11-15), so a rule change needs no new build and
   the solo practice table bids as Rusty does today. The host reads
   `manifest.json` (the rules number, the rule language, the snapshot's
   hash), then `pack.json`, checks the hash, and hands the snapshot to the
   engine when the engine reads that rule language; otherwise, or when the
   fetch fails, the engine bids with its compiled-in rules. It shows the
   rules number it is bidding with and logs it with every result. A bad
   publish reaches users at once: the fallback covers a failed fetch, not
   bad rules. The card library's bundled names may be older than the
   fetched rules. That is safe because names are additive-only: an older
   library does not show a newer setting, and the rules read it at its
   default.
5. **When the skills and lesson sets leave** (below). Agreed (Rick, 2026-11-15): in the
   same cut-over, since the editor's lesson links move with them; if that
   proves large, straight after, with the pack unchanged meanwhile.
   Sized on 2026-11-15, it is large (the list is under "Skills and lessons
   leave the pack" below), so it follows the cut-over.

6. **Where measurements are kept.** A rule change is judged by
   comparisons: the same cards and deals bid before and after, and our
   auctions against another bidder's. Today the conclusions are in each
   module's `.notes.md` (here) and in pull request text; the runs
   themselves are kept nowhere. Settled in outline (Rick, 2026-11-15):
   the measurement belongs to the change, not to CI. Whoever makes the
   change runs it and commits the record with it; publish runs nothing
   extra. How much is run is graded by the change:

   | The change | What is measured |
   |---|---|
   | Text only: a name, a brief, notes, references | Nothing |
   | One convention's rules | Its `.test` lines, and targeted deals bid before and after on cards that play it |
   | Rules many auctions pass through (system, judgement, base), a migration, or a default | Every public card bid before and after |
   | A convention another bidder also plays, when the question is which is right | The same deals bid by that bidder (BBA, from the Practice-Bidding-Scenarios corpora or run from the command line) |

   Recommended form: a `measurements/` folder here, one small file per
   change: the bidder and its version, what was compared (rules before
   and after, the cards, the deal set by name and hash), the auctions
   changed per card, and the score against each reference bidder before
   and after. Every record names its bidder, so another engine's runs sit
   beside Rusty's. The full auction lists stay out of git. Only public
   cards are named. CI checks a record's form, nothing more.

Not built, and not needed for the cut-over:

- **A snapshot per rule language.** There is one published snapshot. After
  a language change an older engine refuses it and falls back to its
  compiled-in rules; publishing the last snapshot of each language would
  let it keep following.
- **A user's own rules beside ours** (#48). It arrives the way the fetched
  snapshot does; how a second pack is laid over this one is in the
  contract's open list.

#### Order

Nothing below is done until the step before it is checked.

**Tags come from the branches; the merges to `main` come last** (Rick,
2026-11-15). Merging the card tools to `main` deploys the standalone
editor, whose "Save to Bridge Classroom" link and exported files would
then carry schema 3 cards. The library Bridge Classroom runs today takes
such a card without an error and finds nothing in it (measured: Stayman
on the 2/1 sample card reads as unset), so a user would save a blank
card. So the editor starts writing schema 3 only after Bridge Classroom
reads it.

1. **Freeze the pack** at a rules number. Capture the 22 public cards and
   the hand-made cards with the branch tools: this is the reference.
   *Done 2026-11-15: rules number 21, snapshot hash `74a583d2…`; the
   bundled copies in both branches equal it; 122,430 boards on the public
   cards and 139,125 on the hand-made ones, bidding, exports and coverage
   unchanged from the last capture.*
2. **`convention-card`:** tag on the tip of the branch stack (#120, #121,
   #123), not merged. *Done 2026-11-15: v0.45.0, tests and CI green; it
   differs from the captured commit only in docs and the version.*
3. **`rusty-bidding-bot`:** pin `bridge-card` to that tag; tag (v0.16.0)
   on the tip of its stack (#90, #91, #92), not merged. The tag builds
   the release binary and the WASM. Check: the compiled-in rules bid
   every captured card as the reference does.
   *Done 2026-11-15: v0.16.0; 122,430 and 139,125 boards bid as the
   reference, exports and coverage unchanged. The release holds the Linux
   and Windows binaries and the WASM. The two macOS binaries were not
   built: Apple refused to notarize them until a developer agreement is
   accepted. Nothing in the cut-over uses them.*
4. **This repo:** `engine.env` names the engine's release tag, so publish
   downloads the binary instead of building it.
   *Done 2026-11-15.*
5. **The service that renders print links** from the card data Bridge
   Classroom stores: bump the card tools pin and deploy, before any
   stored card is in schema 3. It reads both shapes afterwards.
6. **Bridge Classroom:** bump the card tools and the WASM pin; fetch the
   published snapshot when it runs and hand it to Rusty; show the rules
   number beside the engine version. Stored cards upgrade on load, by the
   migration. Check on a staging build before the live one.
7. **Merge the card tools and the engine to `main`.** The standalone
   editor and the engine's site deploy from there.
8. **Better BBO Convention Card:** bump the card tools pin.
9. **Practice-Bidding-Scenarios and lesson-studio** validate their IDs
   against the snapshot.
10. **Docs** (#42), and close #22, #23, #24, #37 to #42.

**Going back.** Every pin can return to its old tag. What cannot go back
is a card saved in schema 3: the old library does not read it. So step 6's
live build is the point of no return for stored cards; take a copy of them
first. Step 7 is the same for card files: once the standalone editor
exports schema 3, those files are in people's hands.


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
- **Skills and lessons leave the pack** (Rick, 2026-11-14). The skill
  naming scheme is wider than the convention one: every convention is a
  skill, but declarer play, hand evaluation and the like are skills that
  are not conventions, and a set of lessons or deals is neither. They came
  in with `convention-card`'s `spec/conventions/`, which held the whole
  lesson taxonomy. Until the move, a definition says which it is
  (`kind = "skill"` on 22, `kind = "judgement"` on 2, `kind = "lesson"` on
  24; the other 139 are conventions).
  - The skills taxonomy goes to Bridge Classroom for now. Later it is to
    come back here as a separate bridge-skills entity, with a conventions
    part that refers to this list. It holds skills such as declarer play,
    and no lesson or deal sets ("100 Miscellaneous Deals").
  - Lesson sets go with the lessons. Each lesson repo maps its lessons
    onto conventions and skills; the pack names no lesson.
  - The links turn round: `taught_under` and a setting's lesson `skill`
    (43 of them) come out of the pack, and the taxonomy says which
    conventions a skill or lesson covers. The editor takes a row's lesson
    and level from there.
  - Removing published IDs needs a migration that says where each went.
  - **Judgement is a third branch** of bridge-skills, beside natural
    methods and conventions: hand evaluation, fit and level decisions,
    total tricks, penalty doubles, slam decisions. It is how a bidder
    decides, and no card records it. The engine's rule language already
    says so: a module is `convention`, `defence`, `system` (the natural
    system) or `judgement`, and the last two are "every robot's own".
  - **The judgement rules stay in this repo**, since the engine reads one
    pack and they lean on the conventions around them, but they are
    labelled as one bidder's judgement and not a standard, as generated
    examples name their bidder. Six modules today (`rules/base/fit.bid`,
    `rules/competitive/total-tricks.bid` and `penalty-doubles.bid`,
    `rules/slam/slam-entry.bid`, `slam-catch.bid` and `over-3nt.bid`).
    Three of them name a lesson set as their skill; when the lesson links
    turn round they name a judgement skill instead.
  - **What the move touches** (measured 2026-11-15, rules number 21).
    It is more than deleting 48 files:
    - 126 lines elsewhere in the pack name a leaving ID: 43 `skill` lines
      in rule modules, 41 settings and treatments (36 of them as the first
      skill, which is where the card tools take a row's lesson and its
      tile in the card report), two functions, three `taught_under`
      lists and one `implies`.
    - Eight leaving definitions hold more than a name and a level: a
      summary, references, and for six of them 23 names the card tools
      recognise in a card's free text (Takeout Doubles, Reverse Bids,
      Michaels & Unusual 2NT, Defensive Signals, Opening Leads, Defending
      against 1NT). That content moves with them; none of it is dropped.
    - Bridge Classroom's taxonomy is a list of 50 IDs and nothing else. 34
      of the 48 are in it; 14 are not. It has to grow to hold what a
      definition holds, and which conventions, settings and rule modules
      each skill or lesson covers.
    - The card tools need a way to be given that taxonomy by their host,
      so that tiles, lesson links, levels and recognised names stay as
      they are. The engine's check of a module's `skill` lines, and
      lesson-studio's check of lesson tags, read both lists.
    - The contract's "an ID is never removed" is reworded: the 48 keep
      their IDs and meaning, in another list.
  - **Order, after the cut-over:** the card tools and Bridge Classroom
    take the taxonomy first; the pack drops the 48 afterwards. Hosts
    follow the newest rules, so the other order would show tiles for
    skills the fetched rules no longer name. Nothing new is to depend on
    the 48 being here in the meantime.

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
- Syntax colouring for `.bid` files: a grammar for VS Code, and the same
  grammar colouring a rule file on the overview page, in a viewer there
  rather than GitHub's raw text (Rick, 2026-11-14; #92).

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
