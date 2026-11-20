# The contract between a convention pack and its readers

**Status: accepted by Rick Wilson, 2026-11-13 (Phase 0).** Nothing reads
this repo yet and no content has moved. The decisions behind it are issues
#2 to #6; [WORKED-EXAMPLES.md](WORKED-EXAMPLES.md) tests it on three real
conventions, and the points it raised are listed at
[the end](#settled-with-acceptance).

A **pack** is a repo, or a directory, of bridge content in the shape below:
convention definitions, card settings and bidding rules. This repo is one
pack. Anyone else's repo in the same shape is another.

A **reader** is any program that loads a pack: the card tools
(`convention-card`), the bidding engine (`rusty-bidding-bot`), a lesson tool
that checks its tags, a site that shows a convention's summary.

The first half of this document is what a reader may rely on. The second is
what a good pack does. It is modelled on `rusty-bidding-bot`'s
`docs/CONTRACT.md`, which stays the contract for the rule language itself.

## Words used here

| Word | Meaning |
|---|---|
| Convention | A named agreement a partnership chooses to play: Stayman, DONT |
| Treatment | A detail of one convention that partnerships vary: Texas over 2NT, the Bergen style |
| Setting | An agreement that is not a convention: a notrump range, a lead, a carding method |
| Definition | The file that describes one convention or skill |
| ID | A definition's permanent name |
| Context | The part of the bidding or play a convention belongs to |
| Card | One partnership's agreements: the conventions it plays and its settings |
| Card model | One layout of a card: a printed form, a site's form, a file format |

## Part 1: what a reader is promised

### 1. Three version numbers

Content is never pinned and has no release numbers. The three **formats**
have numbers, and a reader states which it reads.

| Number | Covers | Now |
|---|---|---|
| `pack_format_version` | The layout of a pack and the format of its definition, setting, context, level, alert and migration files | 1 |
| `card_schema_version` | The shape of a card, and so what treatments and settings a card can hold | 3 |
| `rule_language_version` | The grammar and meaning of `.bid` files | 2 |

- **A number changes only when an existing reader would misread the new
  form.** Adding an optional key, a definition, a treatment, an enum option
  or a setting changes no number.
- **A reader refuses a pack that asks for a number it does not read**, and
  says which number, which value it found and which values it reads.
- **A reader ignores a key it does not know** and, where it writes the file
  back, keeps it.
- **A reader of one version does not read another.** There is no period in
  which a tool accepts two card shapes or two rule languages. Old cards are
  brought forward by a [migration](#11-migrations), once, when read.

### 2. The layout of a pack

```
bridge-pack.toml                       the pack's name and the three numbers
conventions/
    categories.toml                    display names for the categories
    <category>/<name>/                 one directory per ID; the path is the ID
        convention.toml                the definition
        <module>.bid  .test  .notes.md its rules, when the file carries the
                                       `convention` header
        <name>.dlr                     a dealer script, where it is kept here
        examples.pbn                   curated example hands
skills/<category>/<name>/skill.toml    a skill or a judgement entry; the
                                       path is the ID
rules/<folder>/                        every other rule file
settings/<section>.toml                card settings
contexts.toml  functions.toml  levels.toml  alerts.toml
announced-names.toml                   what an opponent's announced name sets on their card
deals.toml                             where dealer scripts kept elsewhere are found
migrations/<from>-to-<to>.toml         every rename, permanent
```

`bridge-pack.toml`:

```toml
name = "bridge-common-conventions"
description = "bridge-craftwork's conventions, card settings and bidding rules"
pack_format_version = 1
card_schema_version = 3
rule_language_version = 2
```

- `name` and `pack_format_version` are required. `card_schema_version` is
  required when the pack has definitions with treatments, or settings.
  `rule_language_version` is required when it has `.bid` files.
- A pack may hold any subset: definitions only, one convention with its
  rules, settings only.
- A reader finds every `.bid` file anywhere in the pack. Where a rule file
  sits says nothing about what it is; its header does.

### 3. IDs

- **A standard ID is `<category>/<name>`**: lower-case letters, digits and
  underscores on both sides of one slash (`bidding_conventions/stayman`).
  These are the skill paths lessons already use.
- **A namespaced ID starts with a domain its author controls**
  (`github.com/alice/bridge-ideas/relay-stayman`). An ID whose first segment
  contains a dot is namespaced; no standard ID does.
- **The ID is the directory path** under `conventions/`, and the `id` key in
  the definition repeats it. A mismatch is an error.
- **An ID is permanent.** It is never renamed, reused for something else, or
  removed. A definition that is superseded stays, with a migration that says
  what replaced it. One kind of thing has left: a set of lessons or deals
  ("Stayman & Transfers (Partnership)", "100 Notrump Deals") is its
  collection's, not a convention or a skill, and the 20 that were defined
  here are recorded in `migrations/lesson-sets.toml` with where each went
  and what it covers. Their IDs are never given to anything else.
- A convention and a skill share one namespace, in two lists.
  `conventions/` holds agreements between partners, conventional or
  natural. `skills/` holds techniques and areas of competence
  (`declarer_play/holdup_plays`, `defense/opening_leads`) and judgement
  (`basic_bidding/hand_evaluation`). An ID is defined in one list only. A
  rule module's `skill` line, a setting's `skill` and `taught_under` name
  an ID from either. A skill has no treatments and fills no function.

### 4. The definition

`convention.toml`. Only `id` and `name` are required.

| Key | Meaning |
|---|---|
| `id` | The ID; must match the path |
| `name` | Display name |
| `label`, `desc` | The caption and one-line description a card editor shows, where they differ from `name` and `summary`. Carried from the card's switch; Phase 5 folds them in |
| `contexts` | One or more context keys: where it applies. The first is the main one. Left out only where no context fits (card play), or for a style of another convention, which applies where its parent does |
| `level` | 1 to 10: the lowest level at which it is taught. Bands are derived from `levels.toml`, never stored |
| `names` | The ways people write it, for finding it in free text |
| `confirm`, `confirm_names` | Names that are ordinary words or could mean another convention; a match on one is offered to a person, not applied |
| `summary` | What it is, in a few lines of the pack author's own words, sized for a chat line; suits as ♣♦♥♠ |
| `taught_under` | Other IDs whose lessons and scenarios also teach this one |
| `implements` | The [functions](#functions) it fills: `["defence_to_1nt"]`, or one part, `["ace_ask.minor"]`. Two conventions a card plays for the same function, or the same part of it, are in conflict |
| `source` | Where the ID came from: `taxonomy`, `lessons` or `proposed` |
| `[treatments.<name>]` | One table per treatment, below |
| `[variant]` | For an ID that is a version of another convention, below |
| `[[deals]]` | Dealer scripts for this convention, below |
| `[[examples]]` | Curated example hands, below |
| `[[references]]` | Citations, below |

**A definition names no card.** It has no card path, no card model, no print
position and no `play` key. Which box a convention fills on a printed form
is each card model's business.

#### Treatments

A treatment's name is lower-case letters, digits and underscores, and unique
within its convention. `play`, `text`, `from` and `for` are reserved and are
never treatment names.

| Key | Meaning |
|---|---|
| `kind` | `bool`, `int`, `enum` or `text` |
| `label` | Display name |
| `desc` | One-line description |
| `options` | The values of an `enum` |
| `min`, `max` | The bounds of an `int` |
| `default` | The value a reader assumes when a card is silent |
| `level` | 1 to 10, when it is harder to learn than the convention |
| `context` | A context key, for a treatment that says where the convention is played (Lebensohl after doubling a weak two) when that differs from the convention's main context |
| `value_aliases` | Other spellings of an enum option, as another tool writes them |
| `requires` | Another treatment of the same convention that this one depends on |
| `choice` | A group name: yes/no treatments sharing it are alternatives, at most one on |
| `bid`, `note`, `explains`, `implies`, `many`, `heading`, `about`, `plays` | As in `convention-card`'s field list today, unchanged. `explains`, `requires` and `implies` name another treatment of the same convention by its bare name, anything else by its address |
| `taught_under` | IDs the treatment is also taught under, besides its convention |
| `skill` | Carried from card schema 2 until Phase 5: an ID when the treatment names a different convention from its group (the variants), `false` when the field named no convention at all (a note, a range) |

- **A treatment means nothing while its convention is not played.** A reader
  ignores its value; a card keeps it, so switching the convention back on
  restores it.
- **A silent treatment of a played convention takes the definition's
  `default`**, and only then a reader's own. A treatment that says where
  the convention is played has `default = true` for its main place, so a
  bare entry plays it there.
- **The same calls in a different auction are one convention with a yes/no
  treatment for each place.** What can be played without another convention
  has its own ID; what only modifies another is a treatment of it.

#### Variants

An ID that is a version of another convention (Reverse Drury, Puppet Stayman
over 2NT, a super-accept) keeps its own definition, for teaching and for
finding it in text. On a card it is a treatment of its parent.

```toml
[variant]
of = "bidding_conventions/bergen_raises"
sets = { reverse = true }
```

A reader asked whether a card plays a variant answers: the parent is played
and its treatments hold the values in `sets`. A variant has no treatments of
its own, and may leave out `level`: the treatment's level is the one tools
read.

#### Deals

```toml
[[deals]]
name = "Texas transfer"
file = "texas.dlr"              # in this directory, or
url = "https://..."             # kept by its author
```

A dealer script generates deals where the convention matters, for testing,
demonstration and practice. Exactly one of `file` and `url`. A reader never
needs a script to load, check or bid a card.

A script kept elsewhere may be tagged there with this convention's ID or
with any ID in its `taught_under`. `deals.toml`, at the pack's root, says
where such collections are: each `[[source]]` names a collection, its
`manifest` (a JSON file listing its scripts), and the keys in it that hold
the scripts, the IDs each practises and each script's path. A tool that
wants the scripts for a convention reads the sources; nothing copies their
lists into this pack.

A script kept here is checked with the rule files (`rbb deal check`, from
the engine release after v0.16.2) and published with them as source text.

#### Curated examples

Chosen hands, usually the troublesome ones, each with the auction a named
person gives for it.

```toml
[[examples]]
file = "examples.pbn"
by = "A. Expert"
agreed = 2026-11-13            # the date the author agreed to their use here
```

- A curated auction is someone's stated answer. A bidder that differs from
  it is reported, never failed.
- They are kept apart from generated examples, which are only what one
  bidder did.
- **The format inside `examples.pbn` is not settled** and is not part of
  pack format 1. It is added in a later phase, as an addition.

#### References

```toml
[[references]]
role = "basis"                 # basis: our treatment follows it. about: further reading
kind = "published"             # published, or personal: a ruling, a letter, a conversation
title = "DONT"
by = "..."                     # optional
site = "Bridge Bum"            # optional
url = "https://..."            # optional
medium = "book"                # optional
chapter = 18                   # optional
used = 2026-10-05              # the date it was consulted; left out when unknown
gone = 2027-01-01              # set when the link died; the entry stays
```

- `role` is `about` when left out.
- An entry is never deleted. A dead link gets a `gone` date.
- `used` is never invented. A reference carried over from an older list
  with no date has none.
- Another tool's behaviour is cited as a tool, by name and date.

### 5. Settings

`settings/<section>.toml` holds the agreements that are not conventions. A
setting's name is `<section>.<key>`, dotted, with no slash
(`notrump.one_nt.range_min`); the file is named for the first segment.

A setting has the attributes of a treatment, plus:

| Key | Meaning |
|---|---|
| `plays` | For an `enum`: `{ option = ID }`. The card plays that convention while the setting holds that option. Kept only for the four settings that carry it today (three two-level openings and the 2/1 rebid style) until Phase 5 gives the openings a function |
| `skill` | The ID the setting is taught under |
| `aliases` | Older spellings that still load |

Section names are names, not card positions. A card model maps each setting
to wherever it prints it, or nowhere.

### 6. Contexts, functions, levels and alerts

`contexts.toml` lists the contexts in display order. Each has a key, which
never changes, and a display name, which may.

| Key | Display name |
|---|---|
| `notrump_openings` | Notrump openings |
| `major_openings` | Major openings |
| `minor_openings` | Minor openings |
| `preemptive_openings` | Two-level and preemptive openings |
| `responses_rebids` | Responses and rebids |
| `slam` | Slam bidding |
| `overcalls` | Our overcalls |
| `doubles` | Our doubles |
| `after_interference` | After they interfere |
| `vs_notrump` | Defence to their notrump |
| `vs_openings` | Defence to their other openings |
| `leads` | Leads |
| `signals` | Signals |
| `general` | General approach |

A card model prints a convention's write-in text where it puts the
convention's first context. The other contexts are for grouping and
filtering.

#### Functions

A function is a job in the system that one convention at a time can do: the
defence to their 1NT, asking for aces, what a 2♦ opening means. Conventions
do not name each other. Each says which function it fills, with
`implements`, and a reader finds a conflict by comparing those.

`functions.toml` lists them. A function may have parts, for a job that can
be shared out:

```toml
[defence_to_1nt]
name = "Defence to their 1NT opening"
parts = ["strong", "weak"]

[ace_ask]
name = "Asking for aces or keycards"
parts = ["major", "minor"]

[opening]
name = "Meaning of a two-level opening bid"
parts = ["2c", "2d", "2h", "2s"]

[low_keycard_ask]
name = "The keycard ask below 4NT"
parts = ["clubs", "diamonds", "hearts"]
```

- A definition that implements `defence_to_1nt` fills every part. One that
  implements `ace_ask.minor` fills that part only.
- **A treatment may say what its convention fills** (`implements` on a
  yes/no treatment). The convention then fills it only while that treatment
  is on: Weak jump shifts fill the jump to a major over a minor through
  their `two_level` treatment, so a card that plays them only at the three
  level, or only in competition, does not compete for it.
- A card entry may narrow what its convention fills with `for` (section 8).
- **A conflict** is two conventions the card plays filling the same part.
  Readers report it: the editor when the card is edited, the engine when it
  loads. A card in conflict still loads and prints.
- **A function is about one bid or one job, not a whole method.** Keycard's
  4NT (`ace_ask`) and the cheaper ask that Minorwood or Kickback makes
  (`low_keycard_ask`) are separate functions, so a card plays Minorwood
  beside keycard with no conflict, and Minorwood beside Kickback with one.
- **A function is listed only where conventions compete one by one.** What
  a system fixes as a whole (a Precision 1♣ against a 2/1 1♣) is part of
  choosing the system and gets no function or part.
- A function's name is never also a setting's section name.
- `[<function>.option]` and `[<function>.was.<part>]` record a card schema 2
  setting whose value chose the convention: the option words, the setting's
  label and the spellings other tools write. Card tools need them to read
  and write older formats; nothing else does.
- Adding a convention to a function touches that convention's definition
  and nothing else.

`levels.toml` names the bands of the 1 to 10 scale. `alerts.toml` says which
calls need an alert or an announcement, by regulator. Both keep
`convention-card`'s present format, with a convention or treatment named by
its [address](#7-addresses) where a card field is named today.

`announced-names.toml` maps the convention names an opponent announces
("Cappelletti", "DONT", "Multi") to the card fields that play them, each an
address or `address=value`, with the call and auction it applies to where
one name means different things in different places. An engine that reads
the opponents' announcements switches those fields on in their card; the
file's header gives the entry format and how names are matched. It is
optional data: the snapshot carries it under `announced_names`, and a reader
that does not know the key ignores it.

### 7. Addresses

One string names anything a card can hold. Rule files and card models' maps
use the same three shapes, told apart by form.

| Shape | Names | Example |
|---|---|---|
| An ID | Whether the card plays that convention | `bidding_conventions/drury` |
| `<id>:<treatment>` | That convention's treatment | `bidding_conventions/jacoby_transfers:over_2nt` |
| A dotted path with no slash | A setting | `notrump.one_nt.range_min` |
| The same shape, naming a function or one part | The ID of the convention the card plays for it | `defence_to_1nt.strong` |

Inside a rule file that carries a `convention` header, a bare name with no
dot, slash or colon is a treatment of that convention (`two_under`).

### 8. The card

Card schema 3.

```json
{
  "schema_version": "3.0",
  "conventions": {
    "bidding_conventions/smolen": {},
    "bidding_conventions/texas": { "two_under": true },
    "bidding_conventions/gerber": { "play": false },
    "github.com/alice/bridge-ideas/relay-stayman": { "text": "2♦ = no major, relay" }
  },
  "settings": {
    "notrump": { "one_nt": { "range_min": 15, "range_max": 17 } }
  }
}
```

**`conventions`** is keyed by ID. An entry holds:

| Key | Meaning |
|---|---|
| `play` | `true` or left out: the partnership plays it. `false`: it has agreed not to |
| `text` | What a person wrote about it, printed in the write-in lines of its main context |
| `from` | Where an entry added by a tool came from |
| `for` | The functions or parts this card plays it for, when fewer than the definition's `implements`: `["defence_to_1nt.strong"]` |
| any other key | A treatment's value, by the treatment's name |

- **A card written by hand can list its conventions and nothing else.**
  `{}` plays the convention with every treatment at its default.
- **No entry means not discussed.** A reader uses its own default, which for
  most conventions is "not played".
- **A migrated card gets no special value.** Where a schema 2 card recorded
  a convention's treatments without setting its switch, the migration writes
  an entry (played) when a treatment is on or filled in, and no entry
  otherwise. Cards converted from another format are converted again from
  their source, not migrated.
- **A card plays a convention** when its entry says so. (Until Phase 5, also
  when one of the four settings with `plays` holds that option.)
- **Two entries filling the same part of a function are a conflict**
  (section 6). `for` is how a card plays DONT against a strong notrump and
  Cappelletti against a weak one.
- An entry for an ID the reader does not know, and a key in an entry that is
  not a treatment it knows, are kept and written back.

**`settings`** is the nested form of the setting names, as cards hold them
today.

**A card never depends on a pack being reachable.** A pack adds names,
summaries, defaults and links. A card loads, prints and is compared without
one, and an ID with no definition still prints its `text`.

Metadata, shared-card members and other parts of a saved card are outside
this contract; they belong to the card tools.

### 9. What the rule language reads

Rule language 2 is rule language 1 with these changes. Everything else,
and the engine's own promises, are in `rusty-bidding-bot`'s
`docs/CONTRACT.md` and `docs/LANGUAGE.md`.

```
module texas-transfers "Texas Transfers"
  kind        convention
  convention  bidding_conventions/texas
  needs       notrump-base
  skill       bidding_conventions/jacoby_transfers
  param  tu  = two_under default false
  param  o23 = bidding_conventions/jacoby_transfers:over_2c_3nt default true
```

- **`convention <id>`** says the file is the rules for that definition, and
  the module is on when the card's entry plays the convention. At most one
  per module. It replaces `card <path>.play`.
  Written `convention <id> default true`, the module is also on for a card
  that is silent on the convention, and off only when the card says it does
  not play it: the bidder's own choice for a silent card (Stayman and
  Jacoby transfers), as a parameter's default is.
- **`card <address>`** stays, for a module switched by a treatment or a
  setting. Several must all hold.
- **`param <name> = <address> [default v]`** reads any address. A bare ID
  reads the card's entry only: a module that is also switched by a setting
  reads that setting too. A function address reads the ID of the convention
  the card plays for it, and the default when none or more than one does.
  A condition compares it with an ID written without spaces
  (`def is competitive_bidding/dont`), or with `none`
  (`def is none`: nothing fills it). The ID must be a convention that
  implements the function.
  The `default` is the bidder's own choice for a silent card and stays in
  the rule file.
- **A module that is more than one convention has no `convention` header**
  and spells out every read.
- **Checks.** A convention, treatment or enum option the pack does not
  define refuses the load, with file and line, as an unknown card path does
  today.
- **Ties between candidate calls are broken by module name**, in place of
  file path. Module names are unique across everything loaded, so the order
  is repeatable and does not depend on where a file sits.

### 10. The published snapshot

Readers do not read `main`. On every push to `main`, CI checks the pack,
builds one file and pushes it to the `published` branch. Nothing is
committed back to `main`.

| File on `published` | Holds |
|---|---|
| `pack.json` | Everything in the pack as one JSON document: the pack file, every definition (`conventions`), every skill and judgement entry (`skills`), the settings, contexts, levels, alerts and migrations, and every rule, test and notes file as its source text, keyed by path |
| `manifest.json` | For each source file its hash and the date it last changed; the commit of `main` it was built from; the three format numbers; the rules number |

- **Rules are published as source text**, never compiled.
- **The snapshot is all or nothing.** A rule file that fails its check, a
  failing `.test` case, or a definition that breaks this contract blocks the
  whole publish. The previous snapshot stays.
- **The rules number** identifies the rules a result was produced with. It
  only increases. It is the count of commits on `main`'s first-parent
  history that changed a source file of the pack, leaving out notes
  (`.notes.md`) and tests (`.test`), which cannot change a bid. A commit to
  the docs, the scripts, a notes file or a test does not move it, and two
  snapshots with the same number bid the same. Descriptive text inside a
  definition (a summary, a reference) does move it: the file also holds
  defaults and treatments, and a count cannot tell them apart.
- **The manifest also names the engine** the rules were checked and tested
  with (`checked_with`). Nothing in either file depends on when the build
  ran: the same commit gives the same bytes.
- **A reader can tell a stale snapshot**: the manifest's source commit is
  compared with the head of `main`.

### 11. Migrations

`migrations/<from>-to-<to>.toml`, one per card schema step. `1-to-2.toml` is
`convention-card`'s, unchanged. `2-to-3.toml` moves a card into
`conventions` and `settings`; its own header describes its tables:
`[convention]` (a switch becomes an entry), `[treatment]`, `[[place]]`
(several switches become one entry with a treatment per place),
`[[function]]` (a setting's value becomes an entry) and `[alias]`.

- `lesson-sets.toml` is not a card schema step: its `[left]` table lists the
  IDs of the lesson sets that are no longer defined, each with its `name`,
  the collection it went `to`, its `lesson` there and what it `covers`. A
  reader that meets one of those IDs (in a tag, a note, a card's list of
  other agreements) finds there what it stood for.
- A reader given a card older than the schema it reads applies the
  migrations in order, once, and writes the card back in the current schema.
- **A migration is never deleted or edited once published.** It is how cards,
  files and PDFs already in people's hands keep loading.

### 12. The additive-only promise

Once published, these are never renamed, removed, or given a different
meaning without a migration in the same push:

- an ID;
- a treatment's name, its `kind`, an enum option;
- a setting's name, its `kind`, an enum option;
- a context key;
- a treatment's or setting's `default`, since changing it changes what a
  silent card means.

These may change freely: display names and labels, summaries, descriptions,
levels, `names`, references, the display order of contexts.

One full refresh of the names is allowed, while nothing outside
bridge-craftwork depends on them. It would be one migration and one new card
schema number.

### 13. Results carry their versions

A logged bidding result records the engine version, the rule language, the
rules number, the pack's source commit and the card schema, so a change in
results can be traced to a rule file or to the engine.

A generated example deal carries the same, plus the dealer script, its seed,
the card and the name of the bidder that produced the auction.

## Part 2: what a good pack does

- **Cite sources, never copy them.** A summary is the author's own words. A
  reference is a citation: no quoted text, no borrowed level numbers, no
  borrowed example hands.
- **Name no card.** No card path, card model or print position in a
  definition, a setting or a context.
- **Hold no one's cards.** A card saved by a user of any tool is that user's
  data. It is never committed to a pack, nor is anything captured from it.
- **Add curated hands only with their author's agreement**, and record who
  gave each auction and when.
- **Name the bidder on every generated example.** It shows what one bidder
  does. What a person has asserted goes in a `.test` file.
- **Give every definition a context, a level and a summary** wherever a
  context fits. A context says where the convention applies; whether a
  card has a place for it is each card model's business, not the pack's.
- **Mark generic names.** A name that is an ordinary word, or that could
  mean another convention, goes in `confirm_names`.
- **Make one rule file one convention where the bridge allows it**, with the
  `convention` header, beside its definition. Put system, judgement and
  several-convention modules under `rules/`.
- **Do not lean on the tie-breaker.** Where two rules can offer the same
  call in the same position, say which wins with a priority and a comment.
- **Keep the engine's habits for rule files**: a `.test` beside every
  module, a `.notes.md` with a Sources section, explanations a player would
  say at the table (`rusty-bidding-bot` `docs/CONTRACT.md`, Part 2).
- **Add; do not rename.** When a name is wrong, add the right one and ship
  the migration with it.
- **Keep a restructure and a correction apart.** A change that moves content
  shows no behaviour difference; a change that corrects it lists every
  difference.

## Settled with acceptance

Raised by [WORKED-EXAMPLES.md](WORKED-EXAMPLES.md) and accepted as written
here. D6, D9 and D14 were ruled on separately and are in the sections above.

| | Question | The contract says |
|---|---|---|
| D3 | A convention's own scenario may be tagged with the ID it is taught under | Accepted by the check (section 4, Deals) |
| D4 | References carried over have no date and no role | `used` left out, `role` defaults to `about` (section 4, References) |
| D7 | A variant's level is stated twice | The treatment's level is read (section 4, Variants) |

Not settled here:

- the format inside `examples.pbn` (Phase 8);
- ~~how the rules number is derived (Phase 4)~~: section 10;
- where a v2 card's `other_agreements` entry keeps its `section` until every
  card model prints by context (Phase 3 design);
- how a second pack is laid over this one (after the cut-over).

## Changed since acceptance

Additions made while restructuring the content (Phase 3), for Rick's review.
None changes a decision.

| Section | Addition | Why |
|---|---|---|
| 4 | `label` and `desc` on a definition | 36 switches carry a caption that differs from the definition's name, and 9 a description. Tools show them today |
| 4 | `skill`, `taught_under`, `plays`, `heading`, `about` on a treatment | Each is an attribute a card field has today. Without them the move would lose information (`scripts/roundtrip.py`) |
| 4 | A played convention's silent treatment takes the definition's `default` first | It is what lets a bare `"lebensohl": {}` play Lebensohl over interference to 1NT. Every default in the field list agrees with the rules' own, so nothing changes |
| 6 | `[<function>.option]` and `[<function>.was.<part>]` in `functions.toml` | The two defence-to-1NT settings had labels, option words and other tools' spellings that the card formats still need |
| 11 | The tables of `2-to-3.toml` | The 1-to-2 format has no way to say "this switch becomes an entry" |
| 11 | `new_ids`, `order` and `[was]` in `2-to-3.toml` | A reader that still shows schema 2 paths (the card tools, until cards are stored in schema 3) rebuilds schema 2's field list from the pack. These are the three things about that list the pack held nowhere else: which IDs schema 2 lacked, the order of its fields, and five choice groups and one `requires` that schema 3 expresses another way |
| 6 | `opening` covers the two-level openings: Weak Twos, the new Strong two-bids and Intermediate two-bids, Flannery, Multi, Mini-Roman and the rest claim their bids. The three `two_level.two_<suit>.meaning` settings become entries (`weak`, `intermediate`, `strong`); `conventional` names none and stays the setting. The 2♣ setting is unchanged: Strong 2♣ and Benjamin only say they fill the part (Rick, 2026-11-14) | The plan's Phase 5 item. A meaning and a ticked convention for the same bid both stand as a conflict the card shows, and a rule reads a conflict as its own default, so bidding does not change |
| 6 | `low_keycard_ask` (clubs, diamonds, hearts): Minorwood fills the minors, Kickback all three (Redwood is Kickback with `for` the minors). They do not join `ace_ask`, which stays the 4NT ask (Rick, 2026-11-14) | As Rick plays it: 1430 at 4NT in the majors, Minorwood in the minors when available, and 4NT with 0314 answers when it is not. The conventions claim bids in a keycard context; they do not replace keycard |
| 6 | `jump_to_major_over_minor` (2h, 2s): Reverse Flannery, Weak jump shifts and the new Strong jump shifts fill it. Reverse Flannery's definition said it was an opening; it is responder's jump over 1♣ or 1♦, as its rules have it (Rick, 2026-11-14) | The definition and the rules disagreed |
| 4, 6 | `implements` on a yes/no treatment: the convention fills the function only while the treatment is on | The jump-shift conventions are played at the two level, the three level, in competition or not. Only the two-level, uncontested style competes for 1m–2M, and Reverse Flannery's two treatments each claim one jump |
| 5, 11 | The eight jump-shift boxes are treatments: `two_level`, `three_level` and `invitational` of Strong jump shifts; `two_level`, `three_level`, `not_in_comp`, `in_comp` and `notes` of Weak jump shifts. Invitational is a treatment of the strong one (Rick, 2026-11-14) | So the jump-shift styles reach the function as entries. The level boxes migrate as places: one that says no survives as an entry that is not played, because a silent card takes a rule's default (strong) and a card that says no must not |
| 6 | `defers` on a function: the words of its schema 2 setting that named no convention and left the choice to the card's entries (`other`, `conventional`). A setting that is filled in and names no convention reads as `none` where nothing fills the part | Without it a card that says its 2♦ is conventional, with no convention ticked, would fall to the bidder's default of a weak two |
| 8 | `for` is written only when it narrows what the convention can fill (Weak Twos for all of 2♦, 2♥ and 2♠ has none) | Weak Twos cannot fill 2♣, so listing its three bids said nothing |
| 4 | `style_of` on a definition: the treatments of another convention that are it (Reverse Drury is `drury:reverse`). Such a definition has no context and no function of its own | Seven names are a style of their parent, not a convention a card holds: Reverse Bergen, Reverse Drury, Two-way Drury, the two super-accepts and the Parrish relay (Rick, 2026-11-14). The name still resolves, for a note or a lesson |
| 6 | Puppet Stayman is a convention of its own, with places `over_1nt` and `over_2nt`; `major_ask_over_notrump` (1nt, 2nt) is filled by Stayman, and over 2NT by Puppet. Modified Jacoby 2NT is a convention of its own; `two_nt_response_to_major` is filled by it or by Jacoby 2NT (Rick, 2026-11-14) | Each replaces what its parent does with that bid, and is named and taught as a convention |
| 11 | `also_plays` on a `[[place]]` and `[[yields]]` in `2-to-3.toml`. A card that showed Puppet Stayman was read as playing Stayman; where both are played the general convention's entry is written `for` the parts the specific one leaves (`for = []` when it leaves none) | Otherwise nearly every card with Puppet over 2NT would show a conflict with its own Stayman, and one with Modified Jacoby a conflict with Jacoby. The rules already let the specific one win |
| 11 | A place the card is silent on is written as off only where its definition has a default | Writing every place invented an answer the card had not given (a card with Puppet over 2NT gained "Puppet over 1NT: no") |
| 8 | A treatment reads as unset while the card says it does not play its convention (`play = false`). The value is kept. A place is exempt: it is the switch itself | The plan's Phase 5 rule, "treatments mean nothing while their convention is off", enforced in one place (the crate's `effective`). Silent on the convention, a set treatment still reads, since the upgrade then takes the card to play it |
| 4 | `independent = true` on a treatment: it reads whatever the convention's switch says, as a place does | Enforcing the rule above showed five treatments that are a separate line in BBA and are on while the convention's own line is off (New Minor Forcing after a 2NT rebid; the over-2NT forms of Texas, minor-suit Stayman and minor transfers). They are places in all but name, and become proper places later |
| 4, 12 | `retired = "<date>"` on a treatment: the name stays and a card that holds it still loads and keeps it, but no tool shows it, no rule reads it and no alert names it | Reverse Flannery's `two_d` was left from when the convention was described as a 2♦ opening; it has nothing to do with one (Rick, 2026-11-14, #69). Retiring keeps the additive-only promise without a migration that throws a card's value away |
| 11 | `[[stood_for]]` in the 2-to-3 migration: a yes/no treatment that, on, turns on the treatments in `means` the card left unset | Reverse Flannery's 2♦ box was the only one an editor offered, so a card that ticked it plays both jumps over one of a minor (Rick, 2026-11-14, #69) |
| 6 | `checkback_after_1nt_rebid`: New Minor Forcing (its `after_1nt_rebid` place), two-way NMF, Checkback, Roudi and XYZ fill it | They are alternatives for responder's 2♣/2♦ after a 1NT rebid. The five `independent` treatments became places (#91), so none is left; the key stays readable |
| 3, 4 | A context is where a definition applies, not a sign that a card holds it. 62 definitions that had none now have one (lesson topics such as Major Suit Openings, conventions no card has a box for such as Muiderberg). Left without: card play, practice-deal sets, and styles of another convention | The pack names no card, so "not on a card" was not its to say (Rick, 2026-11-14). A card may list any ID, as before |
| 4 | `kind` on a definition: `skill` (a bridge skill that is not an agreement: declarer play, overcalls), `judgement` (how a bidder decides: hand evaluation, the Law of Total Tricks) or `lesson` (a set of lessons or deals). Left out for a convention | The skill naming scheme is wider than the convention one, and these 48 came in with the lesson taxonomy. They are marked until they leave the pack at the cut-over (Rick, 2026-11-14) |
| 4 | `kind = "natural"` on a definition: an agreement that is not a convention (opening bids, overcalls, rebids, the takeout double). Twelve definitions marked `skill` or `lesson` are `natural`; Slam Bidding is a `skill`, not a `lesson`. That leaves 12 natural, 14 skills, 2 judgement and 20 lesson sets | The definitions list holds agreements between partners, conventional or natural: natural bidding has rule files and differs by system as conventions do (a 1♥ opening is 12 to 21 in 2/1, 11 to 15 in Precision). A skill is a technique or an area of competence: finessing, choosing a lead, slam bidding. Where something is both, as leads and signals are, the skill is the definition and the agreement is the card's settings, which name it (Rick, 2026-11-16) |
| 4 | `brief` on a definition, and on a treatment that is a place: one line for a row in a list of conventions ("2♦ → 2♥, 2♥ → 2♠" for Jacoby transfers) | The card editor's hand-written catalogue held a caption for each row. The row is now drawn from the definition (the plan's Phase 5 item), so the caption lives with it |
| 5 | The card's 4NT notes line (`slam.blackwood.notes`) is a setting; it was a treatment of Blackwood | It is the free line beside the 4NT boxes and is about whatever ace ask the card plays. As a Blackwood treatment, a card holding only that line was taken to play Blackwood (#72) |
| 9 | `convention <id> default true` | With Stayman unset the 1NT rules took it as off and the 2NT rules as on (#73). A silent card now plays Stayman and Jacoby transfers in both places |
| 10 | The rules number is a count of first-parent commits on `main` that changed a source file other than a notes or test file (Rick, 2026-11-14); the manifest gains `rules_number` and `checked_with`, and each file's entry is `{ sha256, changed }` | Settled in Phase 4, as the section promised. A count is readable beside an engine version and cannot go backwards while `main` is not rewritten |
| 6, 10 | `announced-names.toml`, carried in `pack.json` as `announced_names`: announced convention names to card fields (#133) | In the Brill robot events the opponents' methods reach us as their announcements, mostly a convention's name. Seeded from the definitions' names and Brill's convention files; optional, so an older engine loads a snapshot that has it (2026-11-19) |
| 10 | `pack.json` has the keys `schema`, `pack`, `categories`, `conventions`, `settings`, `contexts`, `functions`, `levels`, `alerts`, `migrations` and `files` | The section said "one JSON document" without naming its parts. `scripts/build_snapshot.py` builds it; the manifest's rules number and per-file dates wait for Phase 4 |
| 2, 3, 10 | `skills/<category>/<name>/skill.toml`, and a `skills` key in `pack.json`: the 14 skills and 4 judgement entries, with the keys a definition has. Their IDs are unchanged; they are no longer under `conventions` | Bridge skills are generic, so they are this repo's, but they are not agreements, so they are their own list (Rick, 2026-11-16). A reader that looks an ID up reads both keys; one written before the split finds the 18 missing from `conventions`. The engine at v0.16.0 bids the same from either shape (measured) |
| 3, 4, 11 | A set of lessons is not defined here. The 20 marked `kind = "lesson"` are removed and recorded in `migrations/lesson-sets.toml`; `lesson` is no longer a kind. A rule module names the convention, natural method or skill it bids, never a lesson set; `taught_under` and a treatment's `skill` no longer name one | A lesson set is a collection's: the collection says what its lessons cover, in its own manifest, with IDs from here (Baker-Bridge does; Practice-Bidding-Scenarios tags its scenarios the same way). Michaels & Unusual 2NT's summary, references and names went to the Michaels and Unusual Notrump definitions (Rick, 2026-11-16) |
| 2, 4, 10 | `deals.toml`: the collections that keep dealer scripts tagged with this pack's IDs (Practice-Bidding-Scenarios is the one source). The snapshot carries it under `deals`, and a `.dlr` file kept in a definition's folder among its `files`. The checker holds a definition's `[[deals]]` entries to the form section 4 gives | Scripts exist already, 214 of them tagged with a convention, and whether keeping scripts per convention is worth it has not been tried. So the pack points at what is there, allows a script of its own, and writes none (Rick, 2026-11-16) |
| 8, 11 | A setting that named a convention keeps the card's own wording: as `text` on the entry it becomes ("Hamilton" on Cappelletti's), or, where it names no convention (`natural`, a name no option covers) or a second part is worded differently, as the setting at its old path | The card tools print that wording. Without it a card that says "Strong - Suction" would print the bare option word after the upgrade |
| 8, 11 | An unset switch whose treatments are all off or empty leaves no entry, so those values are not carried | A treatment cannot exist in schema 3 without its entry, and an entry would say the card plays, or does not play, a convention it was silent on. The rules treat silent and off differently |
| 8, 11 | On upgrade, a convention shown only by a note or by filled-in treatments is played, unless the card ticks or names another convention for the same function; then the ticked one wins and the note is kept (Rick, 2026-11-14) | Some cards have no box for a convention, so a note is the only way to show it; but a 4NT note filed under Blackwood must not displace a ticked keycard |

