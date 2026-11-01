---
title: "Image Compressor Guide"
description: "Workflow guidance for scripts/optimize_images.py"
---

# Image Compressor (`optimize_images.py`)

## Purpose
Compresses screenshot images stored in writeup `assets/` subdirectories to prevent Git repository bloat and ensure fast load times.

## Execution

```bash
# Standard optimization
python3 scripts/optimize_images.py

# Custom max-width and quality parameters
python3 scripts/optimize_images.py --max-width 1600 --quality 80
```

## Workflow Context
Run after capturing screenshots and pasting them into the local writeup `./assets/` directory, prior to staging with Git.
