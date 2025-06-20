import os
import re
import base64
import secrets
from pathlib import Path
from yaml import safe_dump
from slugify import slugify
from Crypto.Cipher import AES
from Crypto.Hash import MD5
import yaml

LOCKED_DIR = "_locked"
INDEX_PATH = os.path.join(LOCKED_DIR, ".locked_index")
DATA_FILE = "_data/locked.yml"

Path(DATA_FILE).parent.mkdir(exist_ok=True)

def evpkdf(password: bytes, salt: bytes, key_size=32, iv_size=16):
    d = b''
    while len(d) < key_size + iv_size:
        d_i = MD5.new(d[-16:] + password + salt).digest() if d else MD5.new(password + salt).digest()
        d += d_i
    return d[:key_size], d[key_size:key_size + iv_size]

def cryptojs_encrypt(plaintext: str, password: str) -> str:
    salt = os.urandom(8)
    key, iv = evpkdf(password.encode(), salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pad_len = 16 - (len(plaintext.encode()) % 16)
    padded = plaintext.encode() + bytes([pad_len] * pad_len)
    ct = cipher.encrypt(padded)
    return base64.b64encode(b'Salted__' + salt + ct).decode()

def extract_frontmatter(md_text):
    match = re.match(r'^---\n(.*?)\n---\n', md_text, re.DOTALL)
    if not match:
        return {}
    frontmatter = {}
    for line in match.group(1).splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip().strip('"').strip("'")
    return frontmatter

def write_decryptor_html(slug, enc_filename):
    html_path = os.path.join(LOCKED_DIR, f"{slug}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(f"""---
layout: splash
permalink: /locked/{slug}.html
---

<script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

<div class="unlock-container">
  <input id="pw" type="password" placeholder="Enter password" class="unlock-input" autofocus />
  <button class="unlock-button" onclick="decrypt()">Unlock</button>
</div>
<p id="status" class="unlock-error"></p>
<hr>
<div id="content"></div>

<script>
document.getElementById("pw").addEventListener("keypress", function(e) {{
  if (e.key === "Enter") decrypt();
}});

async function decrypt() {{
  const pw = document.getElementById("pw").value;
  const status = document.getElementById("status");
  status.textContent = "";
  try {{
    const res = await fetch("{enc_filename}");
    const encData = await res.text();
    const raw = CryptoJS.AES.decrypt(encData, pw);
    const dec = raw.toString(CryptoJS.enc.Utf8);
    if (!dec) throw "Decryption failed: incorrect password or corrupted file.";
    const cleaned = dec.replace(/^---[\\s\\S]*?---\\s*/, '');  // strips frontmatter
    document.querySelector(".unlock-container").style.display = "none";
    document.getElementById("status").style.display = "none";
    document.getElementById("content").innerHTML = marked.parse(cleaned);

  }} catch (err) {{
    status.textContent = err.toString();
  }}
}}
</script>
""")

def process_locked():
    entries = []
    metadata = []

    # Load existing passwords to avoid regenerating
    existing = {}
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, "r", encoding="utf-8") as idx:
            for line in idx:
                if ':' in line:
                    fname, pwd = line.strip().split(":", 1)
                    existing[fname] = pwd

    for file in os.listdir(LOCKED_DIR):
        if file.endswith(".md"):
            if file in existing:
                print(f"Skipping {file} (already encrypted)")
                continue

            path = os.path.join(LOCKED_DIR, file)
            with open(path, "r", encoding="utf-8") as f:
                plaintext = f.read()

            front = extract_frontmatter(plaintext)
            title = front.get("title", file.replace(".md", ""))
            description = front.get("description", "")
            slug = slugify(title)

            password = secrets.token_urlsafe(24)
            encrypted = cryptojs_encrypt(plaintext, password)

            enc_path = os.path.join(LOCKED_DIR, f"{slug}.enc")
            with open(enc_path, "w", encoding="utf-8") as f:
                f.write(encrypted)

            write_decryptor_html(slug, f"{slug}.enc")

            entries.append(f"{file}:{password}")
            metadata.append({
                "title": title,
                "description": description
            })

            print(f"{file} → {slug}.enc + {slug}.html")

    # Append only new entries
    with open(INDEX_PATH, "a", encoding="utf-8") as idx:
        for e in entries:
            idx.write(e + "\n")

    # Load old metadata if exists
    old_metadata = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as yml:
            old_metadata = yaml.safe_load(yml) or []

    # Build a dictionary to update/merge entries
    meta_dict = {item['title']: item for item in old_metadata if 'title' in item}
    for item in metadata:
        meta_dict[item['title']] = item  # update or insert

    # Dump the merged result
    with open(DATA_FILE, "w", encoding="utf-8") as yml:
        safe_dump(list(meta_dict.values()), yml, sort_keys=False)


    print(f"\n{len(entries)} new posts encrypted. Skipped existing.")

if __name__ == "__main__":
    process_locked()
