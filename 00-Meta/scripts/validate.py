#!/usr/bin/env python3
"""Validate the vault: wikilinks, frontmatter, orphans, per-folder counts.

Run from the vault root:

    python 00-Meta/scripts/validate.py

Exits 0 when clean, 1 when anything is reported.
"""

from __future__ import annotations

import os
import re
import sys
from collections import defaultdict

# Files that live in the vault but are not notes.
EXCLUDE = {"claude-code-prompt-web-apis.md"}

# Notes that are entry points and so are never "linked from" anywhere.
ORPHAN_EXEMPT = {"Home"}

WIKILINK = re.compile(r"\[\[([^\]|#]+?)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)

# Fenced blocks first (3+ backticks or tildes), then inline spans.
FENCE = re.compile(r"(?m)^(?P<f>```+|~~~+)[^\n]*\n.*?^(?P=f)[ \t]*$", re.S)
INLINE = re.compile(r"(?<!`)(`+)(?!`).*?(?<!`)\1(?!`)", re.S)


def strip_code(text: str) -> str:
    """Remove fenced blocks and inline code spans.

    Without this, the frontmatter schema documented in Vault Structure.md and
    every ```dataview query would produce phantom wikilinks.
    """
    text = FENCE.sub("", text)
    return INLINE.sub("", text)


def collect(root: str) -> list[str]:
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for name in filenames:
            if name.endswith(".md") and name not in EXCLUDE:
                out.append(os.path.relpath(os.path.join(dirpath, name), root))
    return sorted(out)


def main() -> int:
    root = os.getcwd()
    paths = collect(root)
    stem = {os.path.splitext(os.path.basename(p))[0]: p for p in paths}

    broken: list[tuple[str, str]] = []
    no_frontmatter: list[str] = []
    unquoted: list[tuple[str, str]] = []
    linked: set[str] = set()
    per_folder: dict[str, int] = defaultdict(int)

    for path in paths:
        folder = os.path.dirname(path).replace(os.sep, "/") or "(root)"
        per_folder[folder] += 1

        text = open(os.path.join(root, path), encoding="utf-8").read()
        name = os.path.splitext(os.path.basename(path))[0]

        fm = FRONTMATTER.match(text)
        if not fm:
            no_frontmatter.append(path)
            body = text
        else:
            body = text[fm.end():]
            for line in fm.group(1).split("\n"):
                if "[[" in line and not re.search(r'"\[\[[^\]]+\]\]"', line):
                    unquoted.append((path, line.strip()))
            # Frontmatter links count as real links.
            for target in WIKILINK.findall(fm.group(1)):
                target = target.strip()
                if target in stem:
                    if stem[target] != path:
                        linked.add(target)
                else:
                    broken.append((path, target))

        for target in WIKILINK.findall(strip_code(body)):
            target = target.strip()
            if target in stem:
                if stem[target] != path:
                    linked.add(target)
            else:
                broken.append((path, target))

    print(f"Vault: {len(paths)} notes\n")

    print("Notes per folder")
    for folder in sorted(per_folder):
        print(f"  {folder:<20} {per_folder[folder]:>3}")

    problems = 0

    print("\nBroken wikilinks")
    if broken:
        problems += len(broken)
        for path, target in sorted(set(broken)):
            print(f"  {path} -> [[{target}]]")
    else:
        print("  none")

    print("\nMissing frontmatter")
    if no_frontmatter:
        problems += len(no_frontmatter)
        for path in no_frontmatter:
            print(f"  {path}")
    else:
        print("  none")

    print("\nUnquoted wikilinks in YAML")
    if unquoted:
        problems += len(unquoted)
        for path, line in unquoted:
            print(f"  {path}: {line}")
    else:
        print("  none")

    orphans = [
        p for p in paths
        if os.path.splitext(os.path.basename(p))[0] not in linked
        and os.path.splitext(os.path.basename(p))[0] not in ORPHAN_EXEMPT
    ]
    print("\nOrphans (not linked from any other note)")
    if orphans:
        problems += len(orphans)
        for path in orphans:
            print(f"  {path}")
    else:
        print("  none")

    print(f"\n{'FAIL: ' + str(problems) + ' problem(s)' if problems else 'CLEAN'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
