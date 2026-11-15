#!/usr/bin/env python3
"""Check a pack against docs/CONTRACT.md.

    python3 scripts/check.py [PACK_DIR]

Exit status 0 when the pack is sound. Run it before every commit that
touches content; CI will run it too.
"""
import pathlib
import re
import sys
import tomllib

KINDS = {"bool", "int", "enum", "text"}
RESERVED = {"play", "text", "from", "for"}
NAME = re.compile(r"[a-z0-9_]+\Z")


def as_list(v):
    return [] if v is None or v is False else (v if isinstance(v, list) else [v])


class Pack:
    def __init__(self, root):
        self.root = root
        self.problems = []
        self.manifest = self.load("bridge-pack.toml")
        self.contexts = self.load("contexts.toml")
        self.functions = self.load("functions.toml")
        self.defs = {}
        for f in sorted((root / "conventions").glob("*/*/convention.toml")):
            d = self.load(f.relative_to(root))
            want = "/".join(f.relative_to(root / "conventions").parts[:2])
            if d.get("id") != want:
                self.bad(f, f"id is {d.get('id')!r}, but the path says {want!r}")
            self.defs[want] = d
        self.settings = {}
        for f in sorted((root / "settings").glob("*.toml")):
            for k, v in self.load(f.relative_to(root)).items():
                self.settings[f"{f.stem}.{k}"] = v

    def load(self, rel):
        try:
            return tomllib.loads((self.root / rel).read_text())
        except (OSError, tomllib.TOMLDecodeError) as err:
            self.problems.append(f"{rel}: {err}")
            return {}

    def bad(self, where, what):
        where = where.relative_to(self.root) if isinstance(where, pathlib.Path) else where
        self.problems.append(f"{where}: {what}")

    def function_ok(self, name):
        fn, _, part = name.partition(".")
        f = self.functions.get(fn)
        return bool(f) and (not part or part in f.get("parts", []))

    def resolves(self, address, inside=None):
        """Whether an address names something this pack defines."""
        if inside and NAME.match(address):
            return address in self.defs[inside].get("treatments", {})
        if ":" in address:
            cid, t = address.split(":", 1)
            return t in self.defs.get(cid, {}).get("treatments", {})
        if "/" in address:
            return address in self.defs
        return address in self.settings or self.function_ok(address)

    def check(self):
        m = self.manifest
        for k in ("name", "pack_format_version"):
            if k not in m:
                self.bad("bridge-pack.toml", f"{k} is required")
        if self.defs and "card_schema_version" not in m:
            self.bad("bridge-pack.toml", "card_schema_version is required with definitions")

        for cid, d in self.defs.items():
            where = f"conventions/{cid}/convention.toml"
            if not d.get("name"):
                self.bad(where, "name is required")
            if "play" in d:
                self.bad(where, "a definition has no `play` key")
            if "level" in d and not 1 <= d["level"] <= 10:
                self.bad(where, f"level {d['level']} is not 1 to 10")
            for c in d.get("contexts", []):
                if c not in self.contexts:
                    self.bad(where, f"unknown context {c!r}")
            for f in d.get("implements", []):
                if not self.function_ok(f):
                    self.bad(where, f"unknown function {f!r}")
            # Not an agreement: a bridge skill, or a set of lessons. Both are
            # due to leave the pack for the skills taxonomy (docs/PLAN.md).
            # `judgement`: how a bidder decides (hand evaluation, the Law),
            # which no card records.
            if d.get("kind", "convention") not in ("convention", "skill", "judgement", "lesson"):
                self.bad(where, f"kind is {d['kind']!r}: convention (the default), skill, judgement or lesson")
            if d.get("kind") in ("skill", "judgement", "lesson") and (d.get("treatments") or d.get("implements")):
                self.bad(where, "a skill, judgement or lesson has no treatments and fills no function")
            # A definition that is a style of another names the treatments
            # that are it, and has no card entry of its own.
            for t in d.get("style_of", []):
                pid, _, name = t.partition(":")
                if name not in self.defs.get(pid, {}).get("treatments", {}):
                    self.bad(where, f"style_of names {t!r}, which is not a treatment")
                if d.get("contexts") or d.get("implements"):
                    self.bad(where, "a style of another convention has no context or function of its own")
            for i in d.get("taught_under", []):
                if i not in self.defs:
                    self.bad(where, f"taught_under names {i!r}, which is not defined")
            for t, a in d.get("treatments", {}).items():
                tw = f"{where} [{t}]"
                if not NAME.match(t):
                    self.bad(tw, "a treatment's name is lower-case letters, digits and underscores")
                if t in RESERVED:
                    self.bad(tw, "reserved name")
                self.attrs(tw, a, inside=cid)
                # A treatment may say what its convention fills while it is on.
                if "implements" in a and a.get("kind") != "bool":
                    self.bad(tw, "only a yes/no treatment can say what it implements")
                for f in a.get("implements", []):
                    if not self.function_ok(f):
                        self.bad(tw, f"unknown function {f!r}")
                # A retired name stays so cards still load; nothing uses it.
                if "retired" in a and "implements" in a:
                    self.bad(tw, "a retired treatment fills no function")
        for name, a in self.settings.items():
            self.attrs(f"settings {name}", a)
            for i in a.get("plays", {}).values():
                if i not in self.defs:
                    self.bad(f"settings {name}", f"plays {i!r}, which is not defined")

        claimed = {}
        for cid, d in self.defs.items():
            every = list(d.get("implements", []))
            for t in d.get("treatments", {}).values():
                every += t.get("implements", [])
            for f in every:
                claimed.setdefault(f.split(".")[0], set()).add(cid)
        for fname, fn in self.functions.items():
            if not fn.get("name"):
                self.bad("functions.toml", f"{fname}: name is required")
            for o, cid in fn.get("option", {}).items():
                if cid not in self.defs:
                    self.bad("functions.toml", f"{fname}: option {o} names {cid!r}, which is not defined")
                elif cid not in claimed.get(fname, ()):
                    self.bad("functions.toml", f"{fname}: {cid} does not say it implements it")
            if not claimed.get(fname):
                self.bad("functions.toml", f"{fname}: no convention implements it")

        alerts = self.load("alerts.toml")
        for i, a in enumerate(alerts.get("alert", [])):
            for f in a.get("fields", []):
                if not self.resolves(f):
                    self.bad("alerts.toml", f"alert {i + 1} names {f!r}, which is not defined")
                cid, _, t = f.partition(":")
                if "retired" in self.defs.get(cid, {}).get("treatments", {}).get(t, {}):
                    self.bad("alerts.toml", f"alert {i + 1} names {f!r}, which is retired")

        for f in sorted((self.root / "migrations").glob("*.toml")):
            mig = self.load(f.relative_to(self.root))
            if mig.get("to") != "3.0":
                continue
            targets = list(mig.get("convention", {}).values()) + list(mig.get("treatment", {}).values())
            for sf in mig.get("stood_for", []):
                ids = {a.partition(":")[0] for a in [sf["treatment"], *sf["means"]]}
                if len(ids) != 1 or not all(self.resolves(a) and ":" in a for a in [sf["treatment"], *sf["means"]]):
                    self.bad(str(f.name), f"stood_for {sf['treatment']!r}: treatments of one convention")
            targets += [t for t in mig.get("alias", {}).values()]
            for p in mig.get("place", []):
                targets += [f"{p['convention']}:{t}" for t in p["switches"].values()]
            for fn in mig.get("function", []):
                targets += list(fn["options"].values()) + [fn["function"]]
            for t in targets:
                if not self.resolves(t):
                    self.bad(f, f"{t!r} is not defined")

        modules = {}
        for f in sorted(self.root.rglob("*.bid")):
            m = re.search(r"(?m)^module\s+(\S+)", f.read_text())
            if not m:
                self.bad(f, "no module line")
            elif m.group(1) in modules:
                self.bad(f, f"module {m.group(1)} is also in {modules[m.group(1)]}")
            else:
                modules[m.group(1)] = f.relative_to(self.root)
        return modules

    def attrs(self, where, a, inside=None):
        if a.get("kind") not in KINDS:
            self.bad(where, f"kind is {a.get('kind')!r}")
        if a.get("kind") == "enum" and not a.get("options"):
            self.bad(where, "an enum needs options")
        if "default" in a and a.get("kind") == "enum" and a["default"] not in a["options"]:
            self.bad(where, f"default {a['default']!r} is not an option")
        if "level" in a and not 1 <= a["level"] <= 10:
            self.bad(where, f"level {a['level']} is not 1 to 10")
        if "context" in a and a["context"] not in self.contexts:
            self.bad(where, f"unknown context {a['context']!r}")
        for i in as_list(a.get("skill")) + as_list(a.get("taught_under")):
            if i not in self.defs:
                self.bad(where, f"names {i!r}, which is not defined")
        for k in ("explains", "requires"):
            if k in a and not self.resolves(a[k], inside):
                self.bad(where, f"{k} {a[k]!r} is not defined")
        for cid, target in a.get("implies", {}).items():
            if cid not in self.defs:
                self.bad(where, f"implies names {cid!r}, which is not defined")
            if not self.resolves(target, inside):
                self.bad(where, f"implies {target!r} is not defined")


def main():
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent)
    pack = Pack(root)
    modules = pack.check()
    treatments = sum(len(d.get("treatments", {})) for d in pack.defs.values())
    print(f"{len(pack.defs)} definitions with {treatments} treatments, {len(pack.settings)} settings, "
          f"{len(pack.functions)} functions, {len(modules)} rule modules.")
    for p in pack.problems:
        print("  " + p)
    print("Sound." if not pack.problems else f"{len(pack.problems)} problems.")
    sys.exit(1 if pack.problems else 0)


if __name__ == "__main__":
    main()
