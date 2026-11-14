# Settings

The agreements a card holds that are not conventions, one file per
section. A setting's name is `<section>.<key>`
(`notrump.one_nt.range_min`). See [the contract](../docs/CONTRACT.md),
section 5.

The notes below came with the field list from `convention-card`
(`spec/fields.toml`, v0.44.0) and describe the attributes as they were
there. Where they speak of conventions as groups with a `play` switch,
the contract's definitions and treatments have replaced that.

```
Convention card field registry.

Every setting a card can hold is declared here, once. A card is a set of
`path = value` pairs; the path is `<section>.<key>` as written below
(for example `notrump.one_nt.range_min`).

Field attributes:
  kind     bool | int | enum | text
  label    display name
  options  enum values (kind = "enum")
  min/max  bounds (kind = "int")
  many     (kind = "int") the value may also be a list of them: the cards
           a partnership leads from a holding, when it leads either (the A
           or the K from AKx, [1, 2])
  default  value the engine assumes when a card leaves the field unset
  aliases  older paths that load into this field (Bridge-Classroom's seed
           card and editor catalog disagree in places; both still load).
           A renamed field takes no alias: cards move to its new path by
           schema version (spec/migrations/, ADR-0002)
  desc     one-line description
  note     true for free text written for people (a card's write-in lines:
           notes, descriptions) inside a bidding section; `rbb card
           coverage` counts it with carding, leads and notes
  value_aliases  other spellings of an enum option, as another tool writes
           them ({ "Hamilton" = "cappelletti" }); an enum value also matches
           ignoring case, spaces and hyphens ("Multi-Landy" is multi_landy)
  skill    the convention the field belongs to, by its ADR-0001 ID
           ("bidding_conventions/stayman"), or a list: the first is the
           convention, the rest are skills it is also taught under. The IDs
           are the files in conventions/ (one per ID)
  level    1-10, how hard the agreement is to learn. A convention's base
           fields carry its level (its file in conventions/); an extension, such as
           Texas under Jacoby transfers or transfers after a double, carries
           its own higher level (docs/DESIGN.md, "Difficulty levels")
  choice   a choice group: yes/no fields with the same choice are
           alternatives, at most one on (standard or upside-down count).
           Only for true alternatives: a card that sets two of them is
           reported as a conflict, so boxes partnerships combine (negative
           and penalty doubles at different levels, DOPI and DEPO) are not
           grouped
  explains (text fields) the field whose agreement this text spells out:
           the 2♣ of a defence to 1NT is explained by the defence chosen.
           Once that field is set the text says nothing a tool must read,
           unless it differs from the convention (DESIGN.md, "Text on the
           card")
  plays    (enum fields) { option = convention ID }: the card plays that
           convention when the field holds that option (2♥ meaning "weak"
           plays Weak Twos), as a yes/no field does when it is on
  bid      (text fields) true: the value is a bid, the highest the
           agreement applies through (negative doubles through 4♥: a
           double of 4♠ or higher is not negative). "4♥", "4h", "4H" and
           "4 ♥" all read as 4♥, "3nt" as 3NT; anything else is kept as
           the card wrote it and stays text for a person
  implies  (text fields) { convention ID = yes/no field }: this text
           naming that convention means that box, not just the convention
           ("Puppet" as the 1NT 3♣ response is Puppet Stayman over 1NT,
           not over 2NT). Import sets it; the editor's suggestions use it
  requires a field this one depends on: on, it turns that field on, and that
           field off turns this one off (the Parrish relay follows a 2♥ bust)
  about    ([notes] fields) the sections the notes are about: the PDF's
           notes page prints them under `heading`, with those sections'
           write-ins (`note`), their other_agreements, and any of their
           values too long to read on the card
  heading  ([notes] fields) the heading they print under on the notes page

A convention is a group with a `play` switch (ADR-0002):
`<section>.<convention>.play` turns it on, and every other field of the
group is one of its treatments, meaning nothing while `play` is off. Other
groups (an opening, carding, leads, the king ask) describe agreements and
switch no convention.

Conventions with no field here go in the card's other_agreements list,
[{ id?, section?, text }], by their ID (ADR-0001 D5).

Adding a convention: add its file to conventions/ and its fields here.
```
