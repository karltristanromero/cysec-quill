#!/usr/bin/env python3
"""
verify_assets.py — Verifies modular asset integrity across docs/ and drafts/.
Checks that:
1. All markdown images reference valid files in the local ./assets/ folder.
2. No local absolute filesystem paths (e.g., file:/// or /home/...) exist.
3. Detects unreferenced/orphaned images stored inside assets/ directories.

Usage:
    python3 scripts/verify_assets.py [--fix-orphans]
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"

# Regex for markdown image syntax: ![alt](path)
IMG_MD_RE = re.compile(r"!\[(.*?)\]\((.*?)\)")
# Regex for HTML img tags: <img src="..." />
IMG_HTML_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)


def check_markdown_file(md_path: Path) -> tuple[list[str], set[Path]]:
    errors = []
    referenced_files = set()
    content = md_path.read_text(encoding="utf-8")
    parent_dir = md_path.parent

    # Collect image references
    all_refs = []
    for match in IMG_MD_RE.finditer(content):
        all_refs.append(match.group(2).strip())
    for match in IMG_HTML_RE.finditer(content):
        all_refs.append(match.group(1).strip())

    for ref in all_refs:
        # Ignore external web links
        if ref.startswith("http://") or ref.startswith("https://"):
            continue

        # Check for bad absolute system paths
        if ref.startswith("file://") or ref.startswith("/home/") or ref.startswith("C:\\"):
            errors.append(f"Absolute local path detected in {md_path.name}: {ref}")
            continue

        # Strip URL query or fragment if present
        cleaned_ref = ref.split("?")[0].split("#")[0]
        resolved_asset = (parent_dir / cleaned_ref).resolve()

        if not resolved_asset.exists():
            errors.append(f"Missing referenced asset: {ref} in {md_path.relative_to(REPO_ROOT)}")
        else:
            referenced_files.add(resolved_asset)

    return errors, referenced_files


def main():
    parser = argparse.ArgumentParser(description="Verify modular asset integrity and broken image links.")
    parser.add_argument("--scan-drafts", action="store_true", help="Also check drafts/ directory")
    args = parser.parse_args()

    scan_dirs = [DOCS_DIR]
    if args.scan_drafts:
        scan_dirs.append(REPO_ROOT / "drafts")

    md_files = []
    for d in scan_dirs:
        if d.exists():
            md_files.extend(d.rglob("*.md"))

    print(f"Asset Verification: Checking {len(md_files)} markdown file(s)...")

    total_errors = 0
    all_referenced_assets: set[Path] = set()
    existing_asset_files: set[Path] = set()

    for d in scan_dirs:
        for asset_dir in d.rglob("assets"):
            if asset_dir.is_dir():
                for item in asset_dir.iterdir():
                    if item.is_file() and not item.name.startswith("."):
                        existing_asset_files.add(item.resolve())

    for md_file in md_files:
        errors, refs = check_markdown_file(md_file)
        all_referenced_assets.update(refs)
        if errors:
            for err in errors:
                total_errors += 1
                print(f"[ERROR] {err}")

    # Check for orphan files in assets/
    orphans = existing_asset_files - all_referenced_assets
    if orphans:
        print(f"\n[NOTICE] {len(orphans)} unreferenced (orphan) asset file(s) found in assets/ folders:")
        for orphan in sorted(orphans):
            print(f"  - {orphan.relative_to(REPO_ROOT)}")

    if total_errors > 0:
        print(f"\nAsset validation failed with {total_errors} error(s).")
        sys.exit(1)
    else:
        print("\nAsset validation passed: All referenced local assets resolve correctly.")
        sys.exit(0)


if __name__ == "__main__":
    main()
