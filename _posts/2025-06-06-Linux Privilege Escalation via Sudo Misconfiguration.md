---
title: "Linux Privilege Escalation via Sudo Misconfiguration"
description: "Sudo misconfigurations on Linux systems provide a common vector for privilege escalation. Attackers exploit overly permissive sudo rules to gain root-level access."
date: 2025-06-06T10:00:00+05:30
categories:
  - linux
  - hacking
  - privilege escalation
tags:
  - linux
  - sudo
  - privilege escalation
  - linux security
  - pentesting
---

Sudo misconfigurations on Linux systems provide a common vector for privilege escalation. Attackers exploit overly permissive sudo rules to gain root-level access.

## How It Happens

If a user can run commands as root without password or with unrestricted arguments, they might execute arbitrary commands as root.

## Examples

- Running `/bin/bash` with sudo:  
  ```bash
  sudo /bin/bash
  ```
- Using allowed commands with shell escapes:
  ```bash
  sudo vim -c ':!sh'
  ```
- Exploiting vulnerable scripts run via sudo:

## Detection & Mitigation
- Regularly audit /etc/sudoers and sudoers.d files

- Limit commands users can run with sudo

- Avoid NOPASSWD for dangerous commands

Misconfigured sudo is a low-hanging fruit in many Linux privilege escalation scenarios.

## References:

- GTFOBins: Sudo

- Linux Privilege Escalation Guide by Pentest Academy