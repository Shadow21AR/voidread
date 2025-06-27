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

def write_decryptor_html(slug, enc_filename, plain_password=None):
    html_path = os.path.join(LOCKED_DIR, f"{slug}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(f"""---
layout: splash
permalink: /locked/{slug}.html
---

<script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/base16/onedark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<div class="unlock-container">
  <input id="pw" type="password" placeholder="Enter password" class="unlock-input" autofocus />
  <button class="unlock-button" onclick="decrypt()">Unlock</button>
</div>
{f'<p class="unlock-note">Password: <code>{plain_password}</code></p>' if plain_password else ''}
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
  const wrongPasswordMessages = ["The incantation falters. Try again, Beyonder.","The seal remains unbroken. The key is not right.","Your spirit wavers. That is not the true name.","Reality rejects your attempt. Perhaps a different Sequence?","The door to the fog remains shut."];

    try {{
    const res = await fetch("{enc_filename}");
    const b64 = await res.text();

    const raw = atob(b64);
    if (!raw.startsWith("Salted__")) throw new Error("Invalid file format.");

    const salt = CryptoJS.enc.Latin1.parse(raw.slice(8, 16));
    const ciphertext = CryptoJS.enc.Latin1.parse(raw.slice(16));

    const keyiv = CryptoJS.algo.EvpKDF.create({{ keySize: 256 / 32 + 128 / 32, iterations: 1 }}).compute(CryptoJS.enc.Utf8.parse(pw), salt);
    const key = CryptoJS.lib.WordArray.create(keyiv.words.slice(0, 8));
    const iv = CryptoJS.lib.WordArray.create(keyiv.words.slice(8, 12));

    const decrypted = CryptoJS.AES.decrypt({{ ciphertext }}, key, {{ iv, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 }});

    const dec = decrypted.toString(CryptoJS.enc.Utf8);
    if (!dec || !dec.trim().startsWith('---')) {{
      status.textContent = wrongPasswordMessages[Math.floor(Math.random() * wrongPasswordMessages.length)];
      return;
    }}

    const cleaned = dec.replace(/^---[\\s\\S]*?---\\s*/, '');
    document.querySelector(".unlock-container").style.display = "none";
    document.getElementById("status").style.display = "none";
    document.getElementById("content").innerHTML = marked.parse(cleaned);

    document.querySelectorAll('pre code').forEach((block) => {{
      hljs.highlightElement(block);
    }});
    document.querySelectorAll('pre').forEach((pre) => {{
    const button = document.createElement('button');
    button.innerHTML = '<span class="sr-only">Copy code</span><i class="far fa-fw fa-copy"></i><i class="fas fa-fw fa-check copied" style="display: none;"></i>';
    button.title = 'Copy to clipboard';
    button.onclick = () => {{
        const code = pre.querySelector('code');
        navigator.clipboard.writeText(code.innerText).then(() => {{
        button.querySelector('.copied').style.display = 'inline-block';
        setTimeout(() => (button.querySelector('.copied').style.display = 'none'), 1200);
        }}).catch(() => {{
        button.querySelector('.copied').style.display = 'none';
        setTimeout(() => (button.querySelector('.copied').style.display = 'none'), 1200);
        }});
    }};
    pre.style.position = 'relative';
    button.style.position = 'absolute';
    button.style.top = '0.5rem';
    button.style.right = '0.5rem';
    button.style.padding = '2px 6px';
    button.style.background = '#2a2a2a';
    button.style.color = '#fff';
    button.style.border = 'none';
    button.style.borderRadius = '4px';
    button.style.fontSize = '0.9em';
    button.style.cursor = 'pointer';
    button.style.opacity = '0.7';
    button.onmouseover = () => button.style.opacity = '1';
    button.onmouseleave = () => button.style.opacity = '0.7';
    pre.appendChild(button);
    }});
  }} catch (err) {{
    status.textContent = wrongPasswordMessages[Math.floor(Math.random() * wrongPasswordMessages.length)];
  }}
}}
</script>
""")

def process_locked():
    entries = []
    metadata = []

    existing = {}
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, "r", encoding="utf-8") as idx:
            for line in idx:
                if ':' in line:
                    fname, pwd = line.strip().split(":", 1)
                    existing[fname] = pwd

    for file in os.listdir(os.path.join(LOCKED_DIR, "src")):
        if file.endswith(".md"):
            path = os.path.join(LOCKED_DIR, "src", file)
            with open(path, "r", encoding="utf-8") as f:
                plaintext = f.read()

            front = extract_frontmatter(plaintext)
            title = front.get("title", file.replace(".md", ""))
            description = front.get("description", "")
            locked = front.get("locked", "true").lower() != "false"
            slug = slugify(title)

            if file in existing:
                password = existing[file]
                print(f"Rebuilding {file} using saved password.")
            else:
                password = secrets.token_urlsafe(24)
                entries.append(f"{file}:{password}")
                print(f"{file} → New password assigned.")

            # Always regenerate .enc and .html
            encrypted = cryptojs_encrypt(plaintext, password)
            enc_path = os.path.join(LOCKED_DIR, f"{slug}.enc")
            with open(enc_path, "w", encoding="utf-8") as f:
                f.write(encrypted)

            # write_decryptor_html(slug, f"{slug}.enc")
            write_decryptor_html(slug, f"{slug}.enc", password if not locked else None)

            metadata.append({
                "title": title,
                "description": description,
                "locked": locked
            })

            print(f"{file} → {slug}.enc + {slug}.html")

    with open(INDEX_PATH, "a", encoding="utf-8") as idx:
        for e in entries:
            idx.write(e + "\n")
    old_metadata = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as yml:
            old_metadata = yaml.safe_load(yml) or []

    meta_dict = {item['title']: item for item in old_metadata if 'title' in item}
    for item in metadata:
        meta_dict[item['title']] = item
    with open(DATA_FILE, "w", encoding="utf-8") as yml:
        safe_dump(list(meta_dict.values()), yml, sort_keys=False)

    print(f"\n{len(entries)} new posts encrypted. Skipped existing.")

if __name__ == "__main__":
    process_locked()
