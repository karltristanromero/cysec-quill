---
title: "Index Generator Guide"
description: "Workflow guidance for scripts/generate_index.py"
---

# Index Generator (`generate_index.py`)

## Purpose
Scans all markdown files with YAML frontmatter in `docs/` and `drafts/` to populate the published and in-progress tables in `README.md`.

## Execution

```bash
python3 scripts/generate_index.py
```

## Workflow Context
- Run locally whenever frontmatter metadata (e.g., status, title, category) is updated.
- Also runs automatically in GitHub Actions on push to `sandbox` or `main`.
