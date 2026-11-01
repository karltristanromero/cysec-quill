### 1. Diagnosing the Disk Exhaustion

- **Initial Failure:** During dashboard installation, `dpkg` crashed with `cannot copy extracted data... paste subprocess was killed by signal (Broken pipe)`.
    
- **Root Cause:** A fresh Ubuntu install partitioned only a small segment of disk space without LVM, running out of room when attempting to unpack `wazuh-dashboard` (~1 GB of Node.js libraries and mapping files).
    
- **Partition Check:** Running `sudo growpart /dev/sda 2` returned `NOCHANGE: partition 2 could only be grown by 2015 [fudge=2048]`, confirming the underlying virtual disk itself was fully saturated.
    

### 2. Expanding Virtual Storage and Filesystem

- **Virtual Medium Resize:** The VM was powered down, and the virtual hard drive (`.vdi`) was expanded to **40 GB** via VirtualBox (`VBoxManage modifymedium --resize 40960` or Virtual Media Manager).
    
- **Partition Expansion:** Booted back into the system and expanded the partition into the newly unallocated disk sectors:
    
    Bash
    
    ```
    sudo growpart /dev/sda 2
    ```
    
- **Filesystem Resizing:** Resized the active `ext4` filesystem online so the OS could immediately utilize the new 40 GB boundary:
    
    Bash
    
    ```
    sudo resize2fs /dev/sda2
    ```
    
- **Verification:** `df -h /` verified over 25+ GB of free storage.
    

### 3. Setting Up the Swap Safety Cushion

- Created and enabled a **2 GB dedicated swap file** to prevent memory exhaustion and broken pipes during large package decompression:
    
    Bash
    
    ```
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    ```
    
- Cleaned out orphaned kernel headers (`linux-headers-*`) via `sudo apt autoremove --purge` to reclaim extra space.
    

### 4. Overcoming Broken Package States & Downgrade Conflicts

- **Downgrade Block:** Re-running the installer triggered `E: Packages were downgraded and -y was used without --allow-downgrades`, followed by `ERROR: Wazuh manager already installed`.
    
- **The `pi` State:** Running `dpkg -l | grep wazuh` revealed `wazuh-manager` stuck in the **`pi`** flag (**p**urge requested, but **i**nstallation/reinstallation required). Because the package's maintainer scripts were corrupted or missing, standard `apt-get purge` refused to run.
    
- **Metadata Wipe & Force Purge:**
    
    - Deleted the failing maintainer scripts directly from the DPKG database:
        
        Bash
        
        ```
        sudo rm -f /var/lib/dpkg/info/wazuh-manager.*
        ```
        
    - Forced `dpkg` to completely drop the record without triggering script hooks:
        
        Bash
        
        ```
        sudo dpkg --purge --force-all wazuh-manager
        ```
        
    - Removed leftover directories and cached archives (`/var/ossec`, `/etc/ossec-init.conf`, and `/var/cache/apt/archives/*`).
        

### 5. Executing the All-in-One Installation

- With the disk expanded, swap active, and the DPKG database completely clean (`dpkg -l | grep wazuh` returning empty), the automated assistant was executed with the overwrite flag (refer to [[Installation Server]] for default installation instructions and access credentials):
    
    Bash
    
    ```
    sudo bash wazuh-install.sh -a -o
    ```
    
- **Final Result:** Successfully deployed all components cleanly:
    
    - **Wazuh Indexer** (OpenSearch with certificates)
        
    - **Wazuh Manager** & **Filebeat**
        
    - **Wazuh Dashboard** (unpacked without disk or memory issues)
        

### Next Verification Step

Verify that all three core services are up and active:

Bash

```
sudo systemctl status wazuh-manager wazuh-indexer wazuh-dashboard --no-pager
```

You can now log into your dashboard at `[https://127.0.0.1:8443](https://127.0.0.1:8443)` (via your port-forwarded NAT) or `https://<VM_IP>` using the credentials printed in the installer summary or saved in `/root/wazuh-install-files/wazuh-passwords.txt`.

---

### Related Notes
* **VM Setup:** [[Virtual Machine Configuration]] – VM specifications, Netplan IP setup, and port forwarding rules.
* **Server Install:** [[Installation Server]] – Command and default administrator credentials.
* **Agent Integration:** [[Agent]] – Debian agent setup and version matching.
