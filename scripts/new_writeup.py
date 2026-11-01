#!/usr/bin/env python3
"""
new_writeup.py — Interactive scaffolding tool for creating new writeups,
lab research bundles, and scratchpad hubs.

Usage:
    python3 scripts/new_writeup.py
"""

import datetime
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = REPO_ROOT / "templates"
DOCS_DIR = REPO_ROOT / "docs"
DRAFTS_DIR = REPO_ROOT / "drafts"


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")


def prompt_choice(prompt_text: str, options: list[str]) -> str:
    print(f"\n{prompt_text}")
    for idx, opt in enumerate(options, 1):
        print(f"  [{idx}] {opt}")
    while True:
        try:
            choice = input(f"Select option (1-{len(options)}): ").strip()
            num = int(choice)
            if 1 <= num <= len(options):
                return options[num - 1]
        except (ValueError, EOFError, KeyboardInterrupt):
            pass
        print(f"Invalid selection. Enter a number between 1 and {len(options)}.")


def prompt_string(prompt_text: str, default: str = "") -> str:
    display_prompt = f"{prompt_text} [{default}]: " if default else f"{prompt_text}: "
    val = input(display_prompt).strip()
    return val if val else default


def scaffold_lab_research():
    sub_areas = [
        "detection-engineering",
        "network-architecture",
        "container-security",
        "vuln-reproduction",
    ]
    sub_area = prompt_choice("Select lab research category:", sub_areas)
    title = prompt_string("Enter lab research title")
    if not title:
        print("Title cannot be empty. Aborted.")
        sys.exit(1)

    default_slug = slugify(title)
    slug = prompt_string("Directory slug", default_slug)
    author = prompt_string("Author", "ajax")
    today = datetime.date.today().isoformat()

    target_dir = DOCS_DIR / "lab-research" / sub_area / slug
    assets_dir = target_dir / "assets"
    index_file = target_dir / "index.md"

    if target_dir.exists():
        print(f"Error: Target directory already exists: {target_dir}")
        sys.exit(1)

    template_file = TEMPLATES_DIR / "lab-research-template.md"
    if not template_file.exists():
        print(f"Error: Template not found at {template_file}")
        sys.exit(1)

    template_content = template_file.read_text(encoding="utf-8")
    content = template_content.replace('title: ""', f'title: "{title}"')
    content = content.replace('slug: ""', f'slug: "{slug}"')
    content = content.replace('category: ""', f'category: "{sub_area}"')
    content = content.replace('date_created: ""', f'date_created: "{today}"')
    content = content.replace('author: ""', f'author: "{author}"')
    content = content.replace("# [Lab Title]", f"# {title}")

    target_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)
    index_file.write_text(content, encoding="utf-8")

    print(f"\nCreated lab research bundle at:")
    print(f"  {index_file}")
    print(f"  {assets_dir}/")


def scaffold_ctf():
    platforms = ["hackthebox", "tryhackme", "picoctf", "vulnhub", "general"]
    platform = prompt_choice("Select CTF platform:", platforms)
    title = prompt_string("Enter challenge or machine name")
    if not title:
        print("Title cannot be empty. Aborted.")
        sys.exit(1)

    default_slug = slugify(title)
    slug = prompt_string("Directory slug", default_slug)
    category = prompt_string("Discipline category (e.g., web-security, pwn, rev, forensics)", "network-security")
    difficulty = prompt_string("Difficulty (Easy, Medium, Hard, Insane)", "Medium")
    author = prompt_string("Author", "ajax")
    today = datetime.date.today().isoformat()

    target_dir = DOCS_DIR / "ctf" / slug
    assets_dir = target_dir / "assets"
    index_file = target_dir / "index.md"

    if target_dir.exists():
        print(f"Error: Target directory already exists: {target_dir}")
        sys.exit(1)

    template_file = TEMPLATES_DIR / "writeup-template.md"
    if not template_file.exists():
        print(f"Error: Template not found at {template_file}")
        sys.exit(1)

    template_content = template_file.read_text(encoding="utf-8")
    content = template_content.replace('title: ""', f'title: "{title}"')
    content = content.replace('slug: ""', f'slug: "{slug}"')
    content = content.replace('platform: ""', f'platform: "{platform}"')
    content = content.replace('category: ""', f'category: "{category}"')
    content = content.replace('difficulty: ""', f'difficulty: "{difficulty}"')
    content = content.replace('date_created: ""', f'date_created: "{today}"')
    content = content.replace('author: ""', f'author: "{author}"')
    content = content.replace("# [Challenge Title]", f"# {title}")

    target_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)
    index_file.write_text(content, encoding="utf-8")

    print(f"\nCreated CTF writeup bundle at:")
    print(f"  {index_file}")
    print(f"  {assets_dir}/")


def scaffold_scratchpad():
    title = prompt_string("Enter scratchpad topic or machine name")
    if not title:
        print("Title cannot be empty. Aborted.")
        sys.exit(1)

    default_slug = slugify(title)
    if not default_slug.endswith("-notes"):
        default_slug = f"{default_slug}-notes"
    slug = prompt_string("Directory name in drafts/scratchpad", default_slug)
    category = prompt_string("Discipline category (e.g. detection-engineering, web-security)", "detection-engineering")
    author = prompt_string("Author", "ajax")
    today = datetime.date.today().isoformat()

    target_dir = DRAFTS_DIR / "scratchpad" / slug
    index_file = target_dir / "index.md"

    if target_dir.exists():
        print(f"Error: Target directory already exists: {target_dir}")
        sys.exit(1)

    template_file = TEMPLATES_DIR / "scratchpad-index-template.md"
    if not template_file.exists():
        print(f"Error: Template not found at {template_file}")
        sys.exit(1)

    template_content = template_file.read_text(encoding="utf-8")
    content = template_content.replace('title: "[Topic / Machine Name] - Scratchpad Hub"', f'title: "{title} - Scratchpad Hub"')
    content = content.replace('category: "lab-research"', f'category: "{category}"')
    content = content.replace('date_created: "YYYY-MM-DD"', f'date_created: "{today}"')
    content = content.replace('author: "ajax"', f'author: "{author}"')
    content = content.replace("# [Topic / Machine Name] - Scratchpad Hub (Index)", f"# {title} - Scratchpad Hub (Index)")

    target_dir.mkdir(parents=True, exist_ok=True)
    index_file.write_text(content, encoding="utf-8")

    print(f"\nCreated scratchpad hub at:")
    print(f"  {index_file}")


def main():
    print("CySec Quill - Writeup Scaffolding Utility")
    types = ["Lab Research (docs/lab-research)", "CTF Writeup (docs/ctf)", "Scratchpad Hub (drafts/scratchpad)"]
    selected = prompt_choice("Select writeup type to scaffold:", types)

    if "Lab Research" in selected:
        scaffold_lab_research()
    elif "CTF" in selected:
        scaffold_ctf()
    elif "Scratchpad" in selected:
        scaffold_scratchpad()


if __name__ == "__main__":
    main()
