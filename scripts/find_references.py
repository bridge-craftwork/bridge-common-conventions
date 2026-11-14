#!/usr/bin/env python3
"""Find the sources our rule files and notes mention that no definition cites.

A rule file's header and its notes often name where a treatment came from
(a Bridge Bum page, an article), with or without the link. The definition is
where a source is cited (`see`), so that the page and the tools show it.
This lists, for every link in a `.bid` or `.notes.md` file:

- the definitions the file belongs to: the one it sits beside, or the ones
  its module header names with `convention` or `skill`;
- whether one of them already cites the link.

    python3 scripts/find_references.py            # the report
    python3 scripts/find_references.py --json     # the same, as data
    python3 scripts/find_references.py --apply    # add the clear cases

A link no definition cites is clear to add when it is plain which
convention it is about:

- the file sits beside a definition; or
- the file is a convention's own module (`kind convention`) naming exactly
  one convention (lesson topics under partnership_bidding/ do not count); or
- the link's last part is the name of a definition
  (`.../wiki/Puppet_Stayman`), whatever file it is in.

`--apply` adds those, writing the entry from what the text and the link
say: the site from its domain, the title from the quoted words beside the
link, else from the link's last part. It never fetches a page and never
invents a date. Another tool's own documentation (GIB's system notes) is
not a source for a convention and is left out. What is left is printed for
a person to place.

Only links already in this repository are considered. Standard library only.
"""
import json
import pathlib
import re
import subprocess
import sys
import tomllib
import urllib.parse

HERE = pathlib.Path(__file__).resolve().parent.parent
URL = re.compile(r"https?://[^\s)>\]\"'`]+")
OURS = ("github.com/bridge-craftwork", "bridge-craftwork.com", "bridge-craftwork.github.io")
SITES = {
    "bridgebum.com": {"site": "Bridge Bum"},
    "en.wikipedia.org": {"site": "Wikipedia"},
    "larryco.com": {"by": "Larry Cohen", "site": "Larry Cohen"},
    "advinbridge.com": {"by": "Robert S. Todd", "site": "Adventures in Bridge"},
    "bridgebase.com": {"site": "Bridge Base Online"},
    "duralbridge.com": {"site": "Dural Bridge"},
    "bridgewinners.com": {"site": "Bridge Winners"},
    "acbl.org": {"site": "ACBL"},
    "acblunit390.org": {"site": "ACBL Unit 390"},
    "bridgebase.com/forums": {"site": "BBO Forums"},
}
# Placed by hand (2026-11-14): links in a shared file whose convention the
# text makes plain, and what our own notes say of a link that names nothing.
PLACED = {
    "https://www.acblunit390.org/Simon/modcapp.htm": "competitive_bidding/modified_cappelletti",
    "https://www.bridgebum.com/lebensohl_over_weak_two.php": "competitive_bidding/lebensohl",
    "https://www.bridgebum.com/defense_to_multi_2d_b.php": "bidding_conventions/multi_2d",
    "https://www.bridgebum.com/unusual_2nt.php": "competitive_bidding/unusual_notrump",
}
DETAILS = {
    "https://static1.squarespace.com/static/5127d3d2e4b0b304f0b6db24/t/5c8e551f104c7b066eb43ac8/1552831776048/3+%28269%29+The+Impossilbe+Spade+Bid+.pdf":
        {"title": "The Impossible ♠ Bid", "by": "Robert S. Todd", "site": "Adventures in Bridge"},
}
# Not cited: our notes say these were found by a search and not read in full.
NOT_READ = (
    "https://members.bridgeclublive.com/MembersArticles/TwoOverOneGameForceforBCL_v2.pdf",
    "https://www.larryco.com/uploaded/product/03569baa-88a2-4cbb-b338-e047536f3368.pdf",
)
# Lesson topics a module is taught under: not the convention a source is about.
NOT_A_CONVENTION = ("partnership_bidding/", "basic_bidding/", "declarer_play/", "defense/", "practice_deals/")
# Another tool's documentation: cited as a tool where its behaviour is
# followed, not as a source for a convention.
TOOL_DOCS = ("netbridge.dk/gib",)


def squash(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


def clean(url):
    return url.rstrip(".,;:").rstrip("/")


def same(url):
    """A link whatever its scheme and with or without www."""
    return re.sub(r"^https?://(www\.)?", "", clean(url))


def site_of(url):
    host = urllib.parse.urlparse(url).netloc.removeprefix("www.")
    for domain, known in sorted(SITES.items(), key=lambda kv: -len(kv[0])):
        if same(url).startswith(domain) or host.endswith("." + domain.split("/")[0]) and "/" not in domain:
            return dict(known)
    return {"site": host}


def title_of(url, line):
    """The quoted words before the link, else the link's last part. `line`
    is the text up to and including the link's line."""
    before = " ".join(line.rsplit(url, 1)[0].split())
    # Quotes pair up from the start of the passage; the last pair is the title.
    quoted = [q for q in re.findall(r'"([^"]*)"', before) if 3 <= len(q) <= 80]
    quoted = quoted or re.findall(r"\[([^\]]{3,80})\]\(\s*$", before)
    if quoted:
        return quoted[-1].strip(), "the text"
    last = urllib.parse.unquote(urllib.parse.urlparse(url).path.rstrip("/").rsplit("/", 1)[-1])
    last = re.sub(r"\.(php|html?|pdf|ing\.htm)$", "", last).replace("_", " ").replace("-", " ").strip()
    return (last[:1].upper() + last[1:] if last else url), "the link"


def main():
    defs, where = {}, {}
    for f in sorted((HERE / "conventions").glob("*/*/convention.toml")):
        d = tomllib.loads(f.read_text())
        defs[d["id"]], where[d["id"]] = d, f
    cited = {i: {same(s["url"]) for s in d.get("see", []) if s.get("url")} for i, d in defs.items()}

    files = subprocess.check_output(["git", "-C", str(HERE), "ls-files", "*.bid", "*.notes.md"], text=True).split()
    # A definition by the squashed form of its ID's last part and its names.
    by_name = {}
    # Conventions a card can hold first, so a name two definitions share
    # finds the convention, not the lesson topic.
    for i, d in sorted(defs.items(), key=lambda kv: (not kv[1].get("contexts"), kv[0])):
        if i.startswith(NOT_A_CONVENTION):
            continue
        for n in [i.split("/")[1], d.get("name", ""), *d.get("names", [])]:
            by_name.setdefault(squash(n), i)
    owners, beside, own_module = {}, {}, set()
    for name in files:
        f = HERE / name
        bid = f if name.endswith(".bid") else f.with_name(f.name.replace(".notes.md", ".bid"))
        ids = []
        parts = pathlib.PurePath(name).parts
        if parts[0] == "conventions" and f"{parts[1]}/{parts[2]}" in defs:
            ids.append(f"{parts[1]}/{parts[2]}")
            beside[name] = f"{parts[1]}/{parts[2]}"
        if bid.exists():
            head = bid.read_text().split("\nafter ")[0].split("\nwhen ")[0]
            if re.search(r"^\s+kind\s+convention\b", head, re.M):
                own_module.add(name)
            for kind, i in re.findall(r"^\s+(convention|skill)\s+([a-z_]+/[a-z0-9_]+)", head, re.M):
                if i in defs and i not in ids and not i.startswith(NOT_A_CONVENTION):
                    ids.append(i)
        owners[name] = ids

    found = []
    for name in files:
        lines = (HERE / name).read_text().split("\n")
        for n, text in enumerate(lines):
            for raw in URL.findall(text):
                url = clean(raw)
                if any(o in url for o in OURS) or any(t in url for t in TOOL_DOCS) or url in NOT_READ:
                    continue
                ids = owners[name]
                title, title_from = title_of(raw, "\n".join(lines[max(0, n - 2):n + 1]))
                last = urllib.parse.unquote(urllib.parse.urlparse(url).path.rstrip("/").rsplit("/", 1)[-1])
                last = re.sub(r"\.(php|html?)$", "", last)
                named = by_name.get(squash(last)) or by_name.get(squash(re.sub(r"_(convention|cuebid)$", "", last)))
                about = (PLACED.get(url) or beside.get(name) or named
                         or (ids[0] if name in own_module and len(ids) == 1 else None))
                entry = {"title": title, **site_of(url), **DETAILS.get(url, {})}
                found.append({"file": name, "url": url, "definitions": ids, "about": about,
                              "cited_by": sorted(i for i in defs if same(url) in cited[i]),
                              "entry": {**entry, "url": url}, "title_from": title_from})
    # One row per link: the first place that says which convention it is about.
    rows = {}
    for r in found:
        if r["url"] not in rows or (r["about"] and not rows[r["url"]]["about"]):
            rows[r["url"]] = r
    rows = list(rows.values())
    missing = [r for r in rows if not r["cited_by"]]
    clear = [r for r in missing if r["about"]]
    unclear = [r for r in missing if not r["about"]]

    if "--json" in sys.argv:
        print(json.dumps({"clear": clear, "unclear": unclear}, indent=1, ensure_ascii=False))
        return
    if "--apply" in sys.argv:
        added = {}
        for r in clear:
            i = r["about"]
            if same(r["url"]) not in cited[i]:
                added.setdefault(i, []).append(r["entry"])
                cited[i].add(same(r["url"]))
        for i, entries in added.items():
            f = where[i]
            text = f.read_text()
            lines = "".join("  { " + ", ".join(f"{k} = {json.dumps(v, ensure_ascii=False)}" for k, v in e.items()) + " },\n"
                            for e in entries)
            if re.search(r"^see = \[\n", text, re.M):
                text = re.sub(r"(^see = \[\n(?:  .*\n)*?)(^\]\n)", lambda m: m.group(1) + lines + m.group(2), text, count=1, flags=re.M)
            else:
                # After the summary, before the first treatment.
                at = text.find("\n[treatments.")
                block = "see = [\n" + lines + "]\n"
                text = (text.rstrip("\n") + "\n" + block) if at < 0 else text[:at].rstrip("\n") + "\n" + block + text[at:]
            f.write_text(text)
        print(f"added {sum(len(v) for v in added.values())} sources to {len(added)} definitions")
    print(f"{len(rows)} links in {len(files)} rule and notes files; {len(rows) - len(missing)} already cited by "
          f"a definition; {len(clear)} clear to add; {len(unclear)} for a person to place.")
    for title, group in (("Clear", clear), ("To place", unclear)):
        if "--apply" in sys.argv and title == "Clear":
            continue
        print(f"\n{title}:")
        for r in group:
            to = r["about"] or "? (" + (", ".join(i.split("/")[1] for i in r["definitions"]) or "no convention") + ")"
            print(f"  {r['entry']['title']}  [{r['entry']['site']}]  ->  {to}\n      {r['url']}\n      in {r['file']}")


if __name__ == "__main__":
    main()
