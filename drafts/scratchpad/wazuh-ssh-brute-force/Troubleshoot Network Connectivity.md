# Documentation: Troubleshooting Ubuntu Server Internet Connectivity in VirtualBox on Fedora

## 1. Objective

Restore internet connectivity on an Ubuntu Server virtual machine running in VirtualBox so that `apt update` can access Ubuntu package repositories.

Root cause identified: The Fedora host had an incorrect IPv4 default gateway configuration. Its IP address was `192.168.1.10/24`, but its configured gateway was `192.168.1.0`, which is the network address rather than a normal router gateway. The host was subsequently configured to obtain its IPv4 settings automatically through DHCP.

## 2. Initial diagnosis — Ubuntu Server guest

Run these commands inside the Ubuntu Server VM.

### Step 1: Inspect the guest's IP configuration

```
ip -br address
```

Check the network interface and assigned IP address.

Then inspect the routing table:

```
ip route
```

Initial configuration:

```
default via 10.10.10.1 dev enp0s3
```

The VM was configured to use `10.10.10.1` as its default gateway.

### Step 2: Inspect the guest's neighbor table

```
ip neigh show
```

Or inspect the gateway specifically:

```
ip neigh show 10.10.10.1
```

This checks whether the guest has discovered the gateway's MAC address. The initial output included:

```
10.10.10.1 lladdr 52:54:00:12:35:00 DELAY
```

### Step 3: Check DNS resolution

```
cat /etc/resolv.conf
```

The guest used the local `systemd-resolved` stub:

```
nameserver 127.0.0.53
```

Inspect the active DNS configuration:

```
resolvectl status
```

Test name resolution:

```
resolvectl query archive.ubuntu.com
```

Initial result:

```
resolve call failed: Lookup failed due to system error: No route to host
```

This indicated a connectivity problem beyond simply having the wrong DNS hostname.

### Step 4: Test direct internet access

```
curl -I --connect-timeout 5 http://1.1.1.1
```

Test the Ubuntu archive:

```
curl -I --connect-timeout 5 http://archive.ubuntu.com/ubuntu/
```

Both requests timed out, so the investigation continued on the Fedora host.

## 3. Diagnose the VirtualBox NAT Network

Run these commands on the Fedora host.

### Step 1: Inspect VirtualBox NAT Network configuration

```
VBoxManage list natnetworks
```

The relevant network was configured as follows:

```
Name:        WazuhLab
Enabled:     Yes
Network:     10.10.10.0/24
Gateway:     10.10.10.1
DHCP Server: Yes
IPv6:        No
```

The NAT Network was enabled, and its subnet matched the Ubuntu VM's network.

### Step 2: Inspect the VM's network adapter

```
VBoxManage showvminfo "Wazuh Server" --details
```

The relevant adapter settings were:

- Adapter 1 attached to NAT Network `WazuhLab`.
    
- Cable connected.
    
- Adapter type `82540EM`.
    
- Adapter 2 disabled.
    

To filter the output for network-related details:

```
VBoxManage showvminfo "Wazuh Server" --details | grep -iE 'NIC|MAC|NAT|cable|adapter'
```

The VirtualBox configuration appeared consistent with the guest's network settings. However, this alone did not prove that the host had working internet connectivity.

## 4. Diagnose the Fedora host's internet connection

### Step 1: Inspect network interfaces

```
ip -br address
```

Initial relevant output:

```
enp5s0 UP 192.168.1.10/24
```

The active Ethernet interface was `enp5s0`.

### Step 2: Inspect the routing table

```
ip route
```

Initial output:

```
default via 192.168.1.0 dev enp5s0 proto static metric 20100
192.168.1.0/24 dev enp5s0 proto kernel scope link src 192.168.1.10 metric 100
```

The default gateway was incorrectly set to `192.168.1.0`.

### Step 3: Inspect the active NetworkManager connection

```
nmcli connection show --active
```

The active connection was:

```
Wired connection 2
```

Inspect its IP configuration:

```
nmcli -f GENERAL.CONNECTION,IP4.ADDRESS,IP4.GATEWAY,IP4.ROUTE device show enp5s0
```

This confirmed that the active connection had the incorrect address and gateway configuration.

### Step 4: Inspect neighboring devices

```
ip neigh show dev enp5s0
```

Initial relevant output:

```
192.168.8.1 lladdr d8:42:f7:45:d0:83 STALE
192.168.1.0 INCOMPLETE
```

The neighbor table showed a router at `192.168.8.1`, while the host's IPv4 configuration was using the `192.168.1.0/24` subnet.

### Step 5: Confirm that the host could not access the internet

```
curl -4 -I --connect-timeout 5 https://archive.ubuntu.com/ubuntu/
```

Test direct connectivity separately:

```
curl -4 -I --connect-timeout 5 https://1.1.1.1
```

Both failed, confirming that the issue affected the Fedora host as well as the Ubuntu VM.

## 5. Configure Fedora to obtain IPv4 settings through DHCP

Important: These commands replace the connection's manual IPv4 settings with automatic configuration. Use them when the router provides DHCP, as it did in this case.

### Step 1: Change the NetworkManager profile

```
sudo nmcli connection modify "Wired connection 2" \
  ipv4.method auto \
  ipv4.addresses "" \
  ipv4.gateway "" \
  ipv4.dns ""
```

This configures the connection to obtain its IPv4 address, gateway, and DNS servers automatically instead of using the incorrect static settings.

### Step 2: Reactivate the connection

```
sudo nmcli connection up "Wired connection 2"
```

This applies the configuration and requests updated network settings. Reactivating a network connection may temporarily interrupt connectivity.

### Step 3: Verify the new IP address

```
ip -4 address show enp5s0
```

The host received:

```
192.168.8.164/24
```

### Step 4: Verify the default gateway

```
ip route
```

The corrected default route used:

```
default via 192.168.8.1 dev enp5s0
```

### Step 5: Verify the assigned gateway and DNS servers

```
nmcli -f IP4.ADDRESS,IP4.GATEWAY,IP4.DNS device show enp5s0
```

The resulting configuration was:

|Setting|Value|
|---|---|
|IPv4 address|`192.168.8.164/24`|
|Default gateway|`192.168.8.1`|
|DNS server 1|`192.168.8.1`|
|DNS server 2|`114.114.114.114`|

## 6. Verify connectivity after configuration

Run these tests on Fedora in order.

### Step 1: Test communication with the router

```
ping -c 4 192.168.8.1
```

### Step 2: Test direct internet connectivity

```
ping -c 4 1.1.1.1
```

A successful response confirms that the host can reach the external IP address using ICMP.

### Step 3: Test access to the Ubuntu package archive

```
curl -4 -I --connect-timeout 10 https://archive.ubuntu.com/ubuntu/
```

An HTTP response confirms that the host can establish an HTTP connection to the archive. A response such as `200`, `301`, or even `403` indicates that the server was reached, although the status codes have different meanings.

## 7. Verify Ubuntu Server package access

After confirming that Fedora has internet access, return to the Ubuntu Server VM.

### Step 1: Update package indexes

```
sudo apt update
```

This refreshes the package lists from the configured repositories.

### Step 2: Confirm the guest's routing configuration if needed

```
ip route
```

Expected default route:

```
default via 10.10.10.1 dev enp0s3
```

### Step 3: Retest DNS resolution if needed

```
resolvectl query archive.ubuntu.com
```

### Step 4: Retest the archive connection if needed

```
curl -I --connect-timeout 10 https://archive.ubuntu.com/ubuntu/
```

## 8. Final configuration summary

### Fedora host

- Interface: `enp5s0`
    
- Connection: `Wired connection 2`
    
- IPv4 method: DHCP
    
- IPv4 address: `192.168.8.164/24`
    
- Gateway: `192.168.8.1`
    
- DNS: `192.168.8.1`, `114.114.114.114`
    
    ### Ubuntu Server VM
    
- Interface: `enp0s3`
    
- IPv4 address: `10.10.10.10/24`
    
- Default gateway: `10.10.10.1`
    
- VirtualBox network: `WazuhLab`
    
- Network mode: NAT Network
    
    ### Resolution
    
    The Fedora host's incorrect static IPv4 gateway was replaced with DHCP-provided network settings. Once host connectivity was restored, Ubuntu Server could access its package repositories through the VirtualBox NAT Network.
    

Key lesson: When a VM cannot access the internet, verify the guest's IP address, routing, DNS, and virtual network first. Then test the host's own internet connectivity. If the host itself cannot reach external addresses, correct that issue before changing the VM's NAT configuration or firewall settings.

---

## 9. Related Notes

* **VM Configuration:** [[Virtual Machine Configuration]] – Details on the `WazuhLab` NAT Network and Netplan static IP configuration.
* **Agent Deployment:** [[Agent]] – Configuration and port forwarding for guest agents.
* **Installation Troubleshooting:** [[Troubleshoot VM Server Installation]] – Fixing disk exhaustion and broken packages during Wazuh setup.
