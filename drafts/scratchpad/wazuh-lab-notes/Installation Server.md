# Wazuh Server Installation

Automated all-in-one assistant installation command:

```bash
curl -sO https://packages.wazuh.com/4.14/wazuh-install.sh && sudo bash ./wazuh-install.sh -a
```

## Default Credentials
* **User:** `admin`
* **Password:** `2?Fz5YJCAmG.yyHh+Jvg3ap8lGbz8aFu`

---

## Related Notes
* **Virtual Machine Setup:** [[Virtual Machine Configuration]] – Specs, Netplan static IP, and VirtualBox port forwarding.
* **Installation Troubleshooting:** [[Troubleshoot VM Server Installation]] – Resolving disk space exhaustion, DPKG package errors, and re-running with `-o`.
* **Network Troubleshooting:** [[Troubleshoot Network Connectivity]] – Diagnosing host-to-guest NAT Network routing issues.
* **Agent Setup:** [[Agent]] – Debian agent deployment and version matching.
