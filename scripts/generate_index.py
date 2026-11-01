#!/usr/bin/env python3
"""
generate_index.py — Scans docs/ and drafts/ for Markdown files with YAML
frontmatter, then regenerates the README.md writeup index tables between
sentinel comments with a streamlined, minimal layout.

Usage:
    python3 scripts/generate_index.py
"""

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
README_PATH = REPO_ROOT / "README.md"
SCAN_DIRS = ["docs", "drafts"]

START_SENTINEL = "<!-- WRITEUP_TABLE_START -->"
END_SENTINEL = "<!-- WRITEUP_TABLE_END -->"


# ---------------------------------------------------------------------------
# Frontmatter parser (stdlib only — no PyYAML dependency)
# ---------------------------------------------------------------------------
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict:
    """Minimal YAML-like frontmatter parser for flat scalar fields."""
    match = FM_RE.match(text)
    if not match:
        return {}
    block = match.group(1)
    meta: dict = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if value.startswith("[") and value.endswith("]"):
            value = [
                v.strip().strip('"').strip("'")
                for v in value[1:-1].split(",")
                if v.strip()
            ]
        meta[key] = value
    return meta


# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------

def scan_markdown_files() -> list[dict]:
    """Walk SCAN_DIRS and collect metadata from .md files with frontmatter."""
    entries = []
    for scan_dir in SCAN_DIRS:
        base = REPO_ROOT / scan_dir
        if not base.exists():
            continue
        for md_path in sorted(base.rglob("*.md")):
            if md_path.name == ".gitkeep":
                continue
            try:
                text = md_path.read_text(encoding="utf-8")
            except Exception:
                continue
            meta = parse_frontmatter(text)
            if not meta or "title" not in meta:
                continue
            # Skip navigation index pages that lack a status field
            if md_path.name == "index.md" and "status" not in meta:
                continue
            rel_path = md_path.relative_to(REPO_ROOT)
            meta["_path"] = str(rel_path)
            meta["_section"] = str(rel_path).split("/")[0]  # docs or drafts
            entries.append(meta)
    return entries


# ---------------------------------------------------------------------------
# Streamlined Table Generators (Clean, minimal, no upfront metadata clutter)
# ---------------------------------------------------------------------------

def build_published_table(entries: list[dict]) -> str:
    rows = [
        e
        for e in entries
        if e.get("status", "").lower() == "published" and e["_section"] == "docs"
    ]
    if not rows:
        return "*No published writeups yet.*\n"
    lines = [
        "| Research / Writeup | Category | Published |",
        "| :--- | :--- | :--- |",
    ]
    for r in sorted(rows, key=lambda x: x.get("date_published", ""), reverse=True):
        title_link = f"[{r.get('title', 'Untitled')}]({r['_path']})"
        category = f"`{r.get('category')}`" if r.get("category") else "—"
        date = r.get("date_published", "—")
        lines.append(f"| {title_link} | {category} | {date} |")
    return "\n".join(lines) + "\n"


def build_wip_table(entries: list[dict]) -> str:
    rows = [
        e
        for e in entries
        if e.get("status", "").lower() == "wip"
    ]
    seen_paths: set[str] = set()
    unique = []
    for r in rows:
        if r["_path"] not in seen_paths:
            seen_paths.add(r["_path"])
            unique.append(r)
    if not unique:
        return "*No drafts or WIP items yet.*\n"
    lines = [
        "| In-Progress Note / Draft | Category | Status |",
        "| :--- | :--- | :--- |",
    ]
    for r in sorted(unique, key=lambda x: x.get("date_created", ""), reverse=True):
        title_link = f"[{r.get('title', 'Untitled')}]({r['_path']})"
        category = f"`{r.get('category')}`" if r.get("category") else "—"
        status = r.get("status", "WIP")
        lines.append(f"| {title_link} | {category} | {status} |")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# README updater
# ---------------------------------------------------------------------------

def update_readme(published_table: str, wip_table: str) -> None:
    if not README_PATH.exists():
        print(f"ERROR: {README_PATH} not found.", file=sys.stderr)
        sys.exit(1)

    content = README_PATH.read_text(encoding="utf-8")

    start_idx = content.find(START_SENTINEL)
    end_idx = content.find(END_SENTINEL)

    if start_idx == -1 or end_idx == -1:
        print(f"ERROR: Sentinel comments not found in {README_PATH}.", file=sys.stderr)
        sys.exit(1)

    replacement = (
        f"{START_SENTINEL}\n\n"
        f"### 📝 Published Writeups & Research\n\n"
        f"{published_table}\n"
        f"### 🔬 In-Progress Drafts & Experiments (WIP)\n\n"
        f"{wip_table}\n"
        f"{END_SENTINEL}"
    )

    new_content = (
        content[:start_idx] + replacement + content[end_idx + len(END_SENTINEL) :]
    )
    README_PATH.write_text(new_content, encoding="utf-8")

    pub_count = len(
        [
            e
            for e in scan_markdown_files()
            if e.get("status", "").lower() == "published"
        ]
    )
    print(f"✅ README.md updated — {pub_count} published entry(ies) indexed.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    entries = scan_markdown_files()
    published_table = build_published_table(entries)
    wip_table = build_wip_table(entries)
    update_readme(published_table, wip_table)


if __name__ == "__main__":
    main()
