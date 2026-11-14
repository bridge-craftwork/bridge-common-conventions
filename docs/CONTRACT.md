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
rules/<folder>/                        every other rule file
settings/<section>.toml                card settings
contexts.toml  functions.toml  levels.toml  alerts.toml
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
  what replaced it.
- A convention and a skill share one namespace. A skill that never appears
  on a card (`declarer_play/holdup`) has a definition with no context and no
  treatments.

### 4. The definition

`convention.toml`. Only `id` and `name` are required.

| Key | Meaning |
|---|---|
| `id` | The ID; must match the path |
| `name` | Display name |
| `label`, `desc` | The caption and one-line description a card editor shows, where they differ from `name` and `summary`. Carried from the card's switch; Phase 5 folds them in |
| `contexts` | One or more context keys. The first is the main one. Left out for a skill that never appears on a card |
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
with any ID in its `taught_under`.

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
name = "Meaning of an opening bid"
parts = ["2c", "2d", "2h", "2s"]
```

- A definition that implements `defence_to_1nt` fills every part. One that
  implements `ace_ask.minor` fills that part only.
- A card entry may narrow what its convention fills with `for` (section 8).
- **A conflict** is two conventions the card plays filling the same part.
  Readers report it: the editor when the card is edited, the engine when it
  loads. A card in conflict still loads and prints.
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
- **`card <address>`** stays, for a module switched by a treatment or a
  setting. Several must all hold.
- **`param <name> = <address> [default v]`** reads any address. A bare ID
  reads the card's entry only: a module that is also switched by a setting
  reads that setting too. A function address reads the ID of the convention
  the card plays for it, and the default when none or more than one does.
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
| `pack.json` | Everything in the pack as one JSON document: the pack file, every definition, the settings, contexts, levels, alerts and migrations, and every rule, test and notes file as its source text, keyed by path |
| `manifest.json` | For each source file its hash and the date it last changed; the commit of `main` it was built from; the three format numbers; the rules number |

- **Rules are published as source text**, never compiled.
- **The snapshot is all or nothing.** A rule file that fails its check, a
  failing `.test` case, or a definition that breaks this contract blocks the
  whole publish. The previous snapshot stays.
- **The rules number** identifies the rules a result was produced with. It
  only increases. How it is derived from history is settled in Phase 4.
- **A reader can tell a stale snapshot**: the manifest's source commit is
  compared with the head of `main`.

### 11. Migrations

`migrations/<from>-to-<to>.toml`, one per card schema step. `1-to-2.toml` is
`convention-card`'s, unchanged. `2-to-3.toml` moves a card into
`conventions` and `settings`; its own header describes its tables:
`[convention]` (a switch becomes an entry), `[treatment]`, `[[place]]`
(several switches become one entry with a treatment per place),
`[[function]]` (a setting's value becomes an entry) and `[alias]`.

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
- **Give every definition a context, a level and a summary** when it can
  appear on a card.
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
- how the rules number is derived (Phase 4);
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
| 10 | `pack.json` has the keys `schema`, `pack`, `categories`, `conventions`, `settings`, `contexts`, `functions`, `levels`, `alerts`, `migrations` and `files` | The section said "one JSON document" without naming its parts. `scripts/build_snapshot.py` builds it; the manifest's rules number and per-file dates wait for Phase 4 |
| 8, 11 | On upgrade, a convention shown only by a note or by filled-in treatments is played, unless the card ticks or names another convention for the same function; then the ticked one wins and the note is kept (Rick, 2026-11-14) | Some cards have no box for a convention, so a note is the only way to show it; but a 4NT note filed under Blackwood must not displace a ticked keycard |

