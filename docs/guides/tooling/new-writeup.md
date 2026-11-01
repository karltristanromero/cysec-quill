---
title: "New Writeup Scaffolder Guide"
description: "Workflow guidance for scripts/new_writeup.py"
---

# New Writeup Scaffolder (`new_writeup.py`)

## Purpose
Interactively creates new writeup bundles, creates necessary subdirectories (`assets/`), and pre-fills YAML frontmatter from existing templates.

## Execution

```bash
python3 scripts/new_writeup.py
```

## Supported Types
1. **Lab Research:** Scaffolds into `docs/lab-research/<sub_area>/<slug>/`.
2. **CTF Writeups:** Scaffolds into `docs/ctf/<slug>/`.
3. **Scratchpad Hubs:** Scaffolds into `drafts/scratchpad/<slug>/`.

## Workflow Context
Run when starting a new lab or challenge to avoid manual directory creation and frontmatter formatting mistakes.
