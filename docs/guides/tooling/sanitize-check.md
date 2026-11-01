---
title: "Sanitization & Secret Scanner Guide"
description: "Workflow guidance for scripts/sanitize_check.py"
---

# Sanitization & Secret Scanner (`sanitize_check.py`)

## Purpose
Scans staged or targeted markdown files for OPSEC violations, unmasked private keys, live CTF flags, or credential strings before pushing to remote repositories.

## Execution

```bash
# Scan specific file or directory
python3 scripts/sanitize_check.py docs/lab-research/

# Full repository scan
python3 scripts/sanitize_check.py --all
```

## Workflow Context
Run as part of the pre-commit review before checking out or pushing changes to `sandbox`.
