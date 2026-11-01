---
title: "Asset & Link Validator Guide"
description: "Workflow guidance for scripts/verify_assets.py"
---

# Asset & Link Validator (`verify_assets.py`)

## Purpose
Validates that all image links in markdown files resolve to existing local files inside adjacent `./assets/` folders, checks against system absolute paths, and detects unreferenced orphan assets.

## Execution

```bash
# Validate docs/ directory
python3 scripts/verify_assets.py

# Include drafts/ directory in scan
python3 scripts/verify_assets.py --scan-drafts
```

## Workflow Context
Run prior to pushing writeups to verify that images will render correctly on GitHub and SSG documentation platforms without broken links.
