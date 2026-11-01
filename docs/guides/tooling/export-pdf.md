---
title: "PDF & Report Exporter Guide"
description: "Workflow guidance for scripts/export_pdf.py"
---

# PDF & Report Exporter (`export_pdf.py`)

## Purpose
Renders a markdown writeup into a structured, print-ready HTML document and automatically triggers headless rendering to generate a standalone PDF report.

## Execution

```bash
# Export writeup to default PDF location
python3 scripts/export_pdf.py docs/lab-research/detection-engineering/wazuh-ssh-brute-force/index.md

# Specify custom output path
python3 scripts/export_pdf.py docs/lab-research/detection-engineering/wazuh-ssh-brute-force/index.md reports/wazuh-lab.pdf
```

## Workflow Context
Run when you need an exportable technical report for portfolios, recruiters, or offline documentation.
