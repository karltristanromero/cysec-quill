---
title: "Wazuh SIEM Lab Research & Scratchpad Notes"
category: "detection-engineering"
tags: ["wazuh", "siem", "ssh", "lab-notes", "scratchpad"]
status: "Completed"
date_created: "2026-10-30"
author: "ajax"
---

# Wazuh SIEM Lab Research & Scratchpad (Index)

> Central hub and Map of Content (MOC) for all raw lab notes, VM configs, and troubleshooting records.
> 
> **Published Output:** [[docs/lab-research/detection-engineering/wazuh-ssh-brute-force/index|Host-Based Telemetry and Dynamic Defense: SSH Brute-Force Detection in Wazuh]]

---

## Infrastructure & Setup Notes
* [[Virtual Machine Configuration]] — VirtualBox VM specifications, Netplan static IP, and NAT port-forwarding rules.
* [[Installation Server]] — Wazuh server assistant deployment, dashboard credentials, and service setup.
* [[Agent]] — Debian 12 agent deployment, OpenSSH service configuration, and daemon verification.

## Troubleshooting Logs
* [[Troubleshoot Network Connectivity]] — Resolving host gateway misconfigurations and guest NAT connectivity.
* [[Troubleshoot VM Server Installation]] — Disk space saturation, virtual drive expansion, and DPKG error recovery.

## Proof of Concept & Attack Simulations
* [[POC - ssh brute forcing]] — Step-by-step SSH dictionary attack logs, `sshd-session` decoder analysis, and Active Response testing.
