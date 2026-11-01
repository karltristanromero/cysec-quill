# Repository Tooling and Automation Scripts

This index details the local utility scripts located in `scripts/` designed to support the research, drafting, validation, and publishing workflow in **CySec Quill**.

Detailed execution guides for each utility can be found in [`docs/guides/tooling/`](docs/guides/tooling/index.md).

---

## Tooling Index

| Script | Purpose | Common Command |
| :--- | :--- | :--- |
| [`generate_index.py`](scripts/generate_index.py) | Scans YAML frontmatter in `docs/` and `drafts/` to regenerate `README.md` tables. | `python3 scripts/generate_index.py` |
| [`new_writeup.py`](scripts/new_writeup.py) | Interactive CLI scaffolder that creates folders, sets up `assets/`, and populates templates. | `python3 scripts/new_writeup.py` |
| [`sanitize_check.py`](scripts/sanitize_check.py) | Pre-commit OPSEC scanner checking for private keys, unmasked live CTF flags, and credentials. | `python3 scripts/sanitize_check.py --all` |
| [`verify_assets.py`](scripts/verify_assets.py) | Broken image validator that checks local `./assets/` resolution and identifies orphan files. | `python3 scripts/verify_assets.py` |
| [`optimize_images.py`](scripts/optimize_images.py) | Compresses PNG/JPEG screenshots across writeup directories to maintain minimal Git repository weight. | `python3 scripts/optimize_images.py` |
| [`export_pdf.py`](scripts/export_pdf.py) | Renders standalone, print-formatted HTML/PDF reports from writeup markdown bundles. | `python3 scripts/export_pdf.py <path/to/index.md>` |

---

## Standard Pre-Commit Script Routine

Prior to committing and pushing research to the `sandbox` branch:

```bash
# 1. Check for broken image links
python3 scripts/verify_assets.py

# 2. Check for unsanitized secrets or live flags
python3 scripts/sanitize_check.py --all

# 3. Compress new screenshots
python3 scripts/optimize_images.py

# 4. Regenerate repository index tables
python3 scripts/generate_index.py
```
