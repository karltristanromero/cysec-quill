# Contributor Workflow and Runbook

This document defines the standard end-to-end operational lifecycle for authors working inside **CySec Quill**. It covers research capture in **Obsidian**, asset organization, publication formatting, and automated **Git / CI/CD** indexing.

---

## High-Level Architecture Lifecycle

```
[ Phase 1: Exploration ]
      │
      ▼
drafts/scratchpad/<topic>-notes/
  ├── notes, configs, snippets (wikilinked)
  └── index.md (MOC with status: "WIP")
      │
      ▼ (Synthesize & Promote)
[ Phase 2: Production Staging ]
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
[ Phase 4: SDLC Branching & Release Pipeline ]
  ├── Commit & push to "sandbox" branch (Pre-production validation & CI check)
  └── Pull Request / Merge to "main" (Production release)
```

---

## Phase 1: Scratchpad & Lab Research (WIP)

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

> **Note:**
> * Having `status: "WIP"` ensures `python3 scripts/generate_index.py` automatically features this in the **In-Progress Drafts & Experiments (WIP)** table in `README.md`.
> * The `index.md` file serves as the single connection point (Map of Content / MOC) for Obsidian's graph without polluting individual raw notes.

### 3. Take Raw Notes in Obsidian
* Create individual notes inside `drafts/scratchpad/kerberos-attacks/` (e.g., `reconnaissance.md`, `asreproast.md`).
* Link them together using Obsidian wikilinks: `[[asreproast]]`, `[[reconnaissance]]`.
* Save temporary network scans (`.nmap`, `.pcap`) in `drafts/raw-scans/` (these are ignored by Git per `.gitignore`).

---

## Phase 2: Synthesizing into a Published Writeup

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

> **Obsidian Configuration:** Because `.obsidian/app.json` has `"propertiesInDocument": "hidden"`, this YAML block remains hidden when reading or editing inside Obsidian. You will see the markdown heading `# Active Directory...`.

### 4. Modular Assets Convention
* Save screenshots directly in `docs/lab-research/<category>/<slug>/assets/` (e.g., `assets/asreproast-bloodhound.png`).
* Reference them using relative markdown paths:
  ```markdown
  ![BloodHound Analysis](assets/asreproast-bloodhound.png)
  ```
* Avoid absolute paths or shared root directories for writeup images.

---

## Phase 3: Lifecycle Transition & Connecting Notes

Connect the scratchpad to the finished output:

1. **Link Scratchpad Hub to Output:**  
   In `drafts/scratchpad/kerberos-attacks/index.md`, update the published link:
   ```markdown
   > **Published Output:** [[docs/lab-research/detection-engineering/kerberos-roasting-telemetry/index|Active Directory Kerberos Telemetry: Detecting AS-REP Roasting & Kerberoasting]]
   ```

2. **Retire the Scratchpad from WIP:**  
   Change the hub note's frontmatter status:
   ```yaml
   status: "Completed" # Excludes it from the active WIP table in README.md
   ```

3. **Link Boundary Rule:**  
   Keep `docs/` free of outbound links pointing into `drafts/`. In Obsidian, navigating to the published writeup will display the scratchpad hub in the **Backlinks** pane and **Graph View** via inbound link detection.

---

## Phase 4: SDLC Branching & Release Workflow

All writeups follow a standard release lifecycle: work is validated on a pre-production branch (`sandbox`) before being merged into the production trunk (`main`) via a GitHub Pull Request.

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
* Keys (`.pem`, `.key`, `id_rsa`), environment files (`.env`), and scan dumps (`.pcap`, `.nmap`) should not appear as untracked files (ignored by `.gitignore`).

### 3. Switch to or Create the `sandbox` Branch
Ensure all draft and writeup work is developed on `sandbox`:

```bash
git checkout -B sandbox
```

### 4. Stage & Commit Content to `sandbox`
Commit your content changes:

```bash
git add docs/ drafts/ README.md
git commit -m "feat(detection): publish kerberos roasting telemetry writeup"
```

### 5. Deploy to `sandbox` & Validate
Push to the remote `sandbox` branch:

```bash
git push -u origin sandbox
```

* The GitHub Actions workflow (`.github/workflows/update-readme.yml`) runs on `sandbox`.
* Review your changes, generated tables, and assets on GitHub under the `sandbox` branch.

### 6. Promote to `main` via GitHub Pull Request
Once validated on GitHub:
1. Open a **Pull Request** on GitHub: `sandbox` -> `main`.
2. Review the diff and complete the merge on GitHub.
3. Switch back to `main` locally and pull the newly merged changes to keep your local branch synchronized:

```bash
git checkout main
git pull origin main
```

---

## Quick Reference Cheat Sheet

| Task | Location | Command / Action |
| :--- | :--- | :--- |
| **Start raw lab testing** | `drafts/scratchpad/<topic>/` | Create folder + `index.md` (`status: "WIP"`) |
| **Store raw pcap/nmap** | `drafts/raw-scans/` | Drop files directly (gitignored automatically) |
| **Create published writeup** | `docs/lab-research/<cat>/<slug>/` | Copy from `templates/` to `index.md` |
| **Save screenshots** | `.../<slug>/assets/` | Relative links: `![Alt](assets/img.png)` |
| **Mark draft completed** | `drafts/scratchpad/<topic>/index.md` | Set `status: "Completed"` |
| **Update README locally** | Repo Root | `python3 scripts/generate_index.py` |
| **Work on sandbox branch** | Repo Root | `git checkout -B sandbox && git commit -m "..."` |
| **Deploy & test on sandbox** | Repo Root | `git push -u origin sandbox` |
| **Merge via GitHub PR** | GitHub Web UI | Open PR: `sandbox` -> `main`, review & merge |
| **Sync local main** | Repo Root | `git checkout main && git pull origin main` |
