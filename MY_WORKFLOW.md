# 🚀 Human Contributor Workflow & Runbook
<!-- AI NOTE: This document is a human-facing operational runbook. AI coding assistants do NOT need to ingest or read this file automatically on every prompt or task unless explicitly requested by the user. -->

This document defines the standard end-to-end operational lifecycle for human authors working inside **CySec Quill**. It bridges raw research capture in **Obsidian**, modular asset organization, publication scaffolding, and automated **Git / CI/CD** indexing.

---

## 🧭 High-Level Architecture Lifecycle

```
[ Phase 1: Exploration ]
      │
      ▼
drafts/scratchpad/<topic>-notes/
  ├── notes, configs, snippets (wikilinked)
  └── index.md (MOC with status: "WIP")
      │
      ▼ (Synthesize & Promote)
[ Phase 2: Production ]
      │
      ▼
docs/lab-research/<category>/<writeup-slug>/
  ├── index.md (Full writeup + YAML frontmatter: status: "Published")
  └── assets/ (Local screenshots & diagrams)
      │
      ▼
[ Phase 3: Lifecycle Transition ]
  └── Update drafts/scratchpad/<topic>-notes/index.md: status: "Completed"
      │
      ▼
[ Phase 4: Version Control & CI/CD ]
  └── git commit & push ──► GitHub Actions auto-updates README tables
```

---

## 🛠️ Phase 1: Scratchpad & Lab Research (WIP)

All live testing, command dumps, and unrefined notes belong in `drafts/scratchpad/`.

### 1. Create a Scratchpad Topic Hub
From your terminal or Obsidian:

```bash
mkdir -p drafts/scratchpad/kerberos-attacks
```

### 2. Initialize the Hub Note (`index.md`)
Create `drafts/scratchpad/kerberos-attacks/index.md`:

```markdown
---
title: "Active Directory Kerberos Abuse & Telemetry"
category: "detection-engineering"
tags: ["kerberos", "roasting", "active-directory", "scratchpad"]
status: "WIP"
date_created: "2026-11-01"
author: "ajax"
---

# Active Directory Kerberos Abuse & Telemetry (Hub)

> Working scratchpad and experiment logs.
> **Published Writeup:** *TBD*

## Notes & Logs
* [[reconnaissance]] — SPN enumeration queries
* [[asreproast]] — Impacket AS-REP roasting execution
* [[detection]] — Windows Event ID 4768 / 4769 filter tuning
```

> **Why this matters:**
> * Having `status: "WIP"` ensures `python3 scripts/generate_index.py` automatically features this in the **In-Progress Drafts & Experiments (WIP)** table in `README.md`.
> * The `index.md` file serves as the single connection point (Map of Content / MOC) for Obsidian's graph without polluting individual raw notes.

### 3. Take Raw Notes in Obsidian
* Create individual notes inside `drafts/scratchpad/kerberos-attacks/` (e.g., `reconnaissance.md`, `asreproast.md`).
* Freely link them together using Obsidian wikilinks: `[[asreproast]]`, `[[reconnaissance]]`.
* Save temporary network scans (`.nmap`, `.pcap`) in `drafts/raw-scans/` (these are automatically ignored by Git per `.gitignore`).

---

## 📝 Phase 2: Synthesizing into a Published Writeup

Once experiments are validated, promote the research into the public `docs/` tree.

### 1. Scaffold the Modular Directory
Writeups use a slug directory containing `index.md` and a dedicated local `assets/` subfolder:

```bash
# Example: Lab research
mkdir -p docs/lab-research/detection-engineering/kerberos-roasting-telemetry/assets

# Example: CTF challenge
mkdir -p docs/ctf/htb-monitored/assets
```

### 2. Copy the Appropriate Blueprint
```bash
# For lab research:
cp templates/lab-research-template.md docs/lab-research/detection-engineering/kerberos-roasting-telemetry/index.md

# For CTFs:
cp templates/writeup-template.md docs/ctf/htb-monitored/index.md
```

### 3. Populate YAML Frontmatter
Open `index.md` and complete the header:

```yaml
---
title: "Active Directory Kerberos Telemetry: Detecting AS-REP Roasting & Kerberoasting"
slug: "kerberos-roasting-telemetry"
category: "detection-engineering"
tags: ["active-directory", "kerberos", "detection", "windows", "splunk"]
status: "Published"
date_created: "2026-11-01"
date_published: "2026-11-02"
author: "ajax"
lab_environment:
  platform: "Proxmox"
  topology: "AD Lab Domain (192.168.50.0/24)"
  hosts:
    - { role: "DC", hostname: "DC01", ip: "192.168.50.10", os: "Windows Server 2022" }
    - { role: "Attacker", hostname: "kali", ip: "192.168.50.70", os: "Kali Linux" }
---
```

> **Obsidian Tip:** Because `.obsidian/app.json` has `"propertiesInDocument": "hidden"`, this YAML block remains invisible when reading or editing inside Obsidian. You will only see the clean markdown heading `# Active Directory...`.

### 4. Modular Assets Convention
* Save screenshots directly in `docs/lab-research/<category>/<slug>/assets/` (e.g., `assets/asreproast-bloodhound.png`).
* Reference them using relative markdown paths:
  ```markdown
  ![BloodHound Analysis](assets/asreproast-bloodhound.png)
  ```
* **Never** use absolute paths or a monolithic root image dump.

---

## 🔄 Phase 3: Lifecycle Transition & Connecting Notes

Now connect the scratchpad to the finished output:

1. **Link Scratchpad Hub to Output:**  
   In `drafts/scratchpad/kerberos-attacks/index.md`, update the published link:
   ```markdown
   > **🎯 Published Output:** [[docs/lab-research/detection-engineering/kerberos-roasting-telemetry/index|Active Directory Kerberos Telemetry: Detecting AS-REP Roasting & Kerberoasting]]
   ```

2. **Retire the Scratchpad from WIP:**  
   Change the hub note's frontmatter status:
   ```yaml
   status: "Completed" # Excludes it from the active WIP table in README.md
   ```

3. **Privacy Rule:**  
   Keep `docs/` clean of outbound links into `drafts/`. In Obsidian, navigating to the published writeup will automatically show the scratchpad hub in the **Backlinks** pane and **Graph View** via inbound link detection.

---

## ⚡ Phase 4: Local Preview & Git Workflow

### 1. Test Index Generation Locally (Optional)
Run the generator script to verify table updates:

```bash
python3 scripts/generate_index.py
```
* The writeup moves to **Published Writeups & Research**.
* The completed scratchpad is removed from **In-Progress Drafts & Experiments (WIP)**.

### 2. Security Check Before Commit
Run `git status` to verify no sensitive data or dumps were tracked:

```bash
git status
```
* Keys (`.pem`, `.key`, `id_rsa`), environment files (`.env`), and scan dumps (`.pcap`, `.nmap`) should **not** appear as untracked files (shielded by `.gitignore`).

### 3. Stage & Commit Content
Commit your content changes:

```bash
git add docs/ drafts/
git commit -m "feat(detection): publish kerberos roasting telemetry writeup"
```

### 4. Push & CI/CD Automation
Push to the remote repository:

```bash
git push origin main
```

* The GitHub Actions workflow (`.github/workflows/update-readme.yml`) triggers automatically on push to `main` when markdown files change.
* The action runs `scripts/generate_index.py` in the runner and commits any updated table modifications via `github-actions[bot]`.

---

## 📋 Quick Reference Cheat Sheet

| Task | Location | Command / Action |
| :--- | :--- | :--- |
| **Start raw lab testing** | `drafts/scratchpad/<topic>/` | Create folder + `index.md` (`status: "WIP"`) |
| **Store raw pcap/nmap** | `drafts/raw-scans/` | Drop files directly (gitignored automatically) |
| **Create published writeup** | `docs/lab-research/<cat>/<slug>/` | Copy from `templates/` to `index.md` |
| **Save screenshots** | `.../<slug>/assets/` | Relative links: `![Alt](assets/img.png)` |
| **Mark draft completed** | `drafts/scratchpad/<topic>/index.md` | Set `status: "Completed"` |
| **Update README locally** | Repo Root | `python3 scripts/generate_index.py` |
| **Trigger automated indexing**| Repo Root | `git push origin main` |
