### Phase 1: Initial Setup & Configuration

#### Wazuh Manager (`10.10.10.10`)

- **Active Response Script Binding:** Added the `<command>` definition for `firewall-drop` inside `/var/ossec/etc/ossec.conf`.

- **Active Response Rule Assignment:** Initially declared an `<active-response>` block listening to rules `5710` and `5712` with a 180-second timeout.

- **Service Lifecycle:** Restarted `wazuh-manager` to apply rule evaluations.

#### Debian Agent (`10.10.10.5`)

- **Firewall Tooling:** Confirmed the presence of `iptables` and `nftables` binary packages required by the response binary.

- **Script Verification:** Confirmed executable permissions on `/var/ossec/active-response/bin/firewall-drop`.

- **Agent Response Directive:** Verified `<active-response><disabled>no</disabled></active-response>` was set in the agent's `/var/ossec/etc/ossec.conf`.

#### Kali Linux (`10.10.10.7` / Attacker)

- **Wordlist Extraction:** Uncompressed the default password list with `sudo gzip -d /usr/share/wordlists/rockyou.txt.gz`.

- **Host Verification:** Addressed `REMOTE HOST IDENTIFICATION HAS CHANGED` warnings by purging stale entries using `ssh-keygen -f ~/.ssh/known_hosts -R 10.10.10.5` (and port `2224` on the Fedora host).

### Phase 2: First Attack Simulation

#### Kali Linux (`10.10.10.7` / Attacker)

- **Brute-Force Execution:** Launched an automated dictionary attack against the target SSH port using `hydra -l root -P /usr/share/wordlists/rockyou.txt -t 4 ssh://10.10.10.5 -s 22`.

- **Halt State Observed:** Hydra aborted prematurely with `[ERROR] 1 target was disabled because of too many errors`, but no firewall drops appeared.

### Phase 3: Troubleshooting Log Pipelines & Decoder Mismatches

#### Debian Agent (`10.10.10.5`)

- **Identified Log Ingestion Failure:** Discovered that Debian Minimal logs exclusively to `systemd-journald` in memory and lacks `/var/log/auth.log` by default.
    
- **Rsyslog Deployment:** Installed and enabled `rsyslog` (`sudo apt install rsyslog`) to force persistent writing to `/var/log/auth.log`.
    
- **Log Collection Configuration:** Discovered `/var/log/auth.log` was omitted from the agent's `ossec.conf`; added the `<localfile>` block:
    
    XML
    
    ```
    <localfile>
      <log_format>syslog</log_format>
      <location>/var/log/auth.log</location>
    </localfile>
    ```
    
- **Agent Daemon Restart:** Restarted `wazuh-agent` and validated that `wazuh-logcollector` attached to `/var/log/auth.log` via `/var/ossec/logs/ossec.log`.

#### Wazuh Manager (`10.10.10.10`)

- **Log Testing & Pre-decoding:** Evaluated authentication failure strings with `/var/ossec/bin/wazuh-logtest`.
    
- **Identified Process & Rule Evolution:** Discovered that Debian 12 / modern OpenSSH uses `sshd-session` instead of `sshd`. Wazuh mapped authentication failures to **Rule `5760`** (and brute-force bursts to **Rule `5763`**) instead of legacy rules `5710`/`5712`.
    
- **Identified Attacker IP:** Confirmed the true source IP from the log decoder was `10.10.10.7`.
    
- **Updated Active Response Triggers:** Modified `/var/ossec/etc/ossec.conf` to include the correct rule IDs:
    
    XML
    
    ```
    <active-response>
      <command>firewall-drop</command>
      <location>local</location>
      <rules_id>5710, 5712, 5760, 5763</rules_id>
      <timeout>180</timeout>
    </active-response>
    ```
    
- **Manager Daemon Restart:** Restarted `wazuh-manager` to register the new rule hooks.
    

### Phase 4: Final Execution & Block Trigger

#### Kali Linux (`10.10.10.7` / Attacker)

- **Sequential Exploit Burst:** Fired a rapid sequential burst of failed SSH authentications via bash and `sshpass` against `10.10.10.5`.
    
- **Connection Drop:** Network connectivity to port 22 on the target abruptly timed out as packets were discarded.
    
#### Debian Agent (`10.10.10.5`)

- **Active Response Invocation:** `/var/ossec/logs/active-responses.log` recorded:
    ```
    ... /var/ossec/active-response/bin/firewall-drop add - 10.10.10.7 ... 5760
    ```
    
- **Kernel Firewall State:** Checked with `sudo iptables -L -n -v` and confirmed a dedicated `DROP` rule for source IP `10.10.10.7` actively accumulating dropped packet counts.
    
### Phase 5: Dashboard Verification & CLI Telemetry

#### Wazuh Manager (`10.10.10.10` / CLI)

- **Log Querying via `jq`:** Extracted formatted security alerts and active response objects from `/var/ossec/logs/alerts/alerts.json` showing:

    - Individual authentication failures (`rule.id: 5760`)
      
    - Brute force threshold breaches (`rule.id: 5763`)
      
    - Active response block action records (`rule.id: 651` / `data.command: firewall-drop`)

#### Wazuh Web Dashboard (`[https://127.0.0.1:8443](https://127.0.0.1:8443)`)

- **Endpoint Status:** Verified `debian-target` (`agent-karl` / ID `001`) status showed `Active`.
    
- **Tactics Aggregation:** Confirmed correlated spikes under the MITRE ATT&CK widget (**Initial Access: 18**, **Credential Access: 12**, **Privilege Escalation: 36**).
 
- **Event Navigation:** Located the raw tabular alerts via **Threat Hunting > Events** / MITRE panel drill-down.
