# Virtual Machine Configuration: Wazuh Server

## 1. Overview & System Specifications

The Wazuh Server runs inside an Ubuntu Server virtual machine hosted on VirtualBox to act as the centralized SIEM manager, indexer, and dashboard.

### VM Specifications
* **Base OS:** Ubuntu Server (Minimized installation)
* **vCPUs:** 2 vCPUs
* **Memory:** 8 GB RAM
* **Storage:** 40 GB VDI (expanded from initial 30 GB; see [[Troubleshoot VM Server Installation]])
* **Hostname / Domain:** `wazuh-server`
* **Administrative User:** `karl` (Name: `wazuh-karl`)
* **SSH Authentication:** OpenSSH Server configured with GitHub SSH Keys

---

## 2. VirtualBox Headless VM Management

Manage the Wazuh Server VM from the Fedora host CLI using `VBoxManage`:

* **Start VM (Headless):**
  ```bash
  vboxmanage startvm "Wazuh Server" --type headless
  ```

* **Graceful Shutdown (ACPI):**
  ```bash
  vboxmanage controlvm "Wazuh Server" acpipowerbutton
  ```

---

## 3. VirtualBox Network Configuration

To isolate the lab environment from the physical host while preserving internet access and inter-VM communication, a dedicated NAT Network is used (for troubleshooting connectivity, see [[Troubleshoot Network Connectivity]]).

### NAT Network Parameters (`WazuhLab`)
* **Network Name:** `WazuhLab`
* **Subnet:** `10.10.10.0/24`
* **Gateway IP:** `10.10.10.1`
* **DHCP:** Enabled

### VM Adapter Settings
* Updated the network adapter of **Wazuh Server** in VirtualBox settings from default **NAT** to **NAT Network**, selecting `WazuhLab`.

---

## 4. Guest Static IP Configuration (Netplan)

The server requires a persistent static IP within the `WazuhLab` subnet to reliably serve as the manager and dashboard.

### Step 1: Configure Netplan
Edit the Netplan configuration file (e.g., `/etc/netplan/01-netcfg.yaml` or `/etc/netplan/50-cloud-init.yaml`):

```bash
sudo nano /etc/netplan/01-netcfg.yaml
```

Add the following configuration:

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s3:
      dhcp4: no
      addresses:
        - 10.10.10.10/24
      routes:
        - to: default
          via: 10.10.10.1
      nameservers:
        addresses: [1.1.1.1, 8.8.8.8]
```

### Step 2: Apply the Configuration
Apply the updated Netplan profile:

```bash
sudo netplan apply
```

---

## 5. Port Forwarding Configuration

Port forwarding rules are created on the VirtualBox NAT Network (`WazuhLab`) to allow access to the server's web dashboard, agent endpoints, and SSH administration directly from `127.0.0.1` on the Fedora host.

| Rule Name | Protocol | Host IP | Host Port | Guest IP | Guest Port | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **WazuhWeb** | TCP | `127.0.0.1` | `8443` | `10.10.10.10` | `443` | Wazuh Dashboard Web UI |
| **WazuhAuth** | TCP | `127.0.0.1` | `1515` | `10.10.10.10` | `1515` | Wazuh Agent Registration Service (`wazuh-authd`) |
| **WazuhData** | TCP | `127.0.0.1` | `1514` | `10.10.10.10` | `1514` | Wazuh Agent Telemetry / Event Data Stream |
| **SSH** | TCP | `127.0.0.1` | `2222` | `10.10.10.10` | `22` | Host SSH Administration |

### Command to Apply Rules via VBoxManage (Host)
```bash
VBoxManage natnetwork modify --netname WazuhLab --port-forward-4 "WazuhWeb:tcp:[127.0.0.1]:8443:[10.10.10.10]:443"
VBoxManage natnetwork modify --netname WazuhLab --port-forward-4 "WazuhAuth:tcp:[127.0.0.1]:1515:[10.10.10.10]:1515"
VBoxManage natnetwork modify --netname WazuhLab --port-forward-4 "WazuhData:tcp:[127.0.0.1]:1514:[10.10.10.10]:1514"
VBoxManage natnetwork modify --netname WazuhLab --port-forward-4 "SSH:tcp:[127.0.0.1]:2222:[10.10.10.10]:22"
```

---

## 6. SSH Access & Verification

### Step 1: Verify SSH Service on Ubuntu Server Guest
Check the service status:

```bash
sudo systemctl status ssh --no-pager
```

### Step 2: Connect from Fedora Host
Connect using the forwarded port `2222`:

```bash
ssh -p 2222 karl@127.0.0.1
```

---

## 7. Related Notes & References

* **Server Deployment:** [[Installation Server]] – Installation commands and web dashboard credentials.
* **Storage Troubleshooting:** [[Troubleshoot VM Server Installation]] – Resolution for disk saturation, partition expansion, and package purge.
* **Network Troubleshooting:** [[Troubleshoot Network Connectivity]] – Diagnostics for host gateway, DNS, and NAT routing issues.
* **Target Integration:** [[Agent]] – Debian agent deployment, port forwarding, and version conflict resolution.
