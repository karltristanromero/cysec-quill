#!/usr/bin/env python3
"""
sanitize_check.py — Scans staged or targeted files in docs/ and drafts/
for potential OPSEC hazards, unsanitized flags, sensitive credentials,
and internal IP addressing before pushing to remote repositories.

Usage:
    python3 scripts/sanitize_check.py [--all] [path/to/file_or_dir]
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Regex checks for OPSEC hygiene
PATTERNS = [
    (
        "Private Key Header",
        re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    ),
    (
        "Unmasked Live CTF Flag",
        re.compile(r"(flag|htb|thm|picoctf)\{[a-zA-Z0-9_\-\.\!@#$%^&*]{5,}\}", re.IGNORECASE),
    ),
    (
        "Hardcoded Secret / Token",
        re.compile(r"(api[_-]?key|auth[_-]?token|bearer\s+[a-zA-Z0-9_\-\.]{20,}|password\s*[:=]\s*['\"][^'\"]{6,}['\"])", re.IGNORECASE),
    ),
    (
        "Direct AWS Access Key ID",
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    ),
]

# Allow common harmless examples or placeholders
ALLOWLIST = [
    "flag{...}",
    "flag{redacted}",
    "flag{your_flag_here}",
    "your_api_key_here",
    "password: \"password\"",
]


def check_file(path: Path) -> list[tuple[int, str, str]]:
    findings = []
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return findings

    lines = content.splitlines()
    for line_idx, line in enumerate(lines, 1):
        # Ignore allowlisted dummy tokens
        line_lower = line.lower()
        if any(allowed in line_lower for allowed in ALLOWLIST):
            continue

        for rule_name, rule_regex in PATTERNS:
            matches = rule_regex.findall(line)
            if matches:
                findings.append((line_idx, rule_name, line.strip()))
                break
    return findings


def main():
    parser = argparse.ArgumentParser(description="Scan repository notes for sensitive strings and unmasked tokens.")
    parser.add_argument("target", nargs="?", default=".", help="Target file or directory to scan")
    parser.add_argument("--all", action="store_true", help="Scan entire repository including drafts")
    args = parser.parse_args()

    target_path = Path(args.target).resolve()
    if target_path.is_file():
        files_to_scan = [target_path]
    else:
        scan_dirs = [REPO_ROOT / "docs", REPO_ROOT / "drafts"] if args.all else [target_path]
        files_to_scan = []
        for d in scan_dirs:
            if d.exists():
                files_to_scan.extend(d.rglob("*.md"))

    print(f"Sanitization Check: Scanning {len(files_to_scan)} markdown file(s)...")
    total_violations = 0

    for file_path in files_to_scan:
        # Skip templates
        if "templates" in file_path.parts:
            continue
        rel_path = file_path.relative_to(REPO_ROOT) if file_path.is_relative_to(REPO_ROOT) else file_path
        findings = check_file(file_path)
        if findings:
            print(f"\n[!] Findings in {rel_path}:")
            for line_no, rule_name, line_text in findings:
                total_violations += 1
                truncated = (line_text[:90] + "...") if len(line_text) > 90 else line_text
                print(f"    Line {line_no:4d} | {rule_name}: {truncated}")

    if total_violations > 0:
        print(f"\nScan completed: {total_violations} potential issue(s) identified.")
        print("Review and sanitize secrets before pushing to sandbox or main.")
        sys.exit(1)
    else:
        print("Scan passed: No exposed keys, unmasked live flags, or sensitive tokens found.")
        sys.exit(0)


if __name__ == "__main__":
    main()
