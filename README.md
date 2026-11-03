# CySec Quill

> Personal cybersecurity repository for lab research notes, detection engineering experiments, and CTF writeups.

---
![margo-guryan](/assets/global/margo-guryan.jpeg)
## Repository Structure

```
cysec-quill/
├── docs/                          # Primary public content tree (SSG-ready)
│   ├── ctf/                       # CTF writeups (flat, unpopulated)
│   ├── categories/                # Broad discipline buckets
│   │   ├── network-security/
│   │   ├── web-security/
│   │   ├── digital-forensics/
│   │   └── blue-team-soc/
│   └── lab-research/              # Granular lab focus areas
│       ├── network-architecture/
│       ├── detection-engineering/
│       ├── container-security/
│       └── vuln-reproduction/
├── drafts/                        # Work-in-progress notes (tracked)
│   ├── raw-scans/
│   └── scratchpad/
├── templates/                     # Frontmatter-ready blueprints
├── assets/global/                 # Shared repo graphics & badges
├── scripts/                       # Automation tooling
└── .github/workflows/             # CI/CD pipelines
```

> **Convention:** Every writeup stores its screenshots in a local `assets/` subfolder adjacent to its markdown file (e.g., `writeup-slug/assets/poc.png`).

---

## Writeup Index

<!-- WRITEUP_TABLE_START -->

### Published Writeups & Research

| Research / Writeup | Category | Published |
| :--- | :--- | :--- |
| [Host-Based Telemetry and Dynamic Defense: SSH Brute-Force Detection in Wazuh](docs/lab-research/detection-engineering/wazuh-ssh-brute-force/index.md) | `detection-engineering` | 2026-10-31 |

### In-Progress Drafts & Experiments (WIP)

*No drafts or WIP items yet.*

<!-- WRITEUP_TABLE_END -->

---

## Quick Start

### Using a template

```bash
# New CTF writeup
cp templates/writeup-template.md docs/ctf/challenge-name/index.md
mkdir -p docs/ctf/challenge-name/assets/

# New lab research note
cp templates/lab-research-template.md docs/lab-research/detection-engineering/lab-name/index.md
mkdir -p docs/lab-research/detection-engineering/lab-name/assets/
```

### Regenerate the index

```bash
python3 scripts/generate_index.py
```

The GitHub Actions workflow also runs this automatically on push to `sandbox` or `main` when markdown files change.

---

## License

This repository contains personal research notes and educational cybersecurity content.
