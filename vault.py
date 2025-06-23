import os
import sys
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Hash import MD5
import base64

def evpkdf(password: bytes, salt: bytes, key_size=32, iv_size=16):
    d = d_i = b''
    while len(d) < key_size + iv_size:
        d_i = MD5.new(d_i + password + salt).digest()
        d += d_i
    return d[:key_size], d[key_size:key_size + iv_size]

def cryptojs_encrypt(plaintext: str, password: str) -> str:
    salt = os.urandom(8)
    key, iv = evpkdf(password.encode('utf-8'), salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pad_len = 16 - (len(plaintext) % 16)
    padded = plaintext.encode('utf-8') + bytes([pad_len] * pad_len)
    ct = cipher.encrypt(padded)
    return base64.b64encode(b'Salted__' + salt + ct).decode('utf-8')

def main():
    if len(sys.argv) != 2:
        print("Usage: python vault.py <master_password>")
        return

    master_password = sys.argv[1]
    index_file = Path("_locked/.locked_index")
    output_file = Path("_pages/vault_data.enc")
    
    if not index_file.exists():
        print("Error: .locked_index file not found")
        return

    # Read the index file
    with open(index_file, 'r', encoding='utf-8') as f:
        entries = [line.strip().split(':', 1) for line in f if ':' in line]

    # Generate the vault content
    vault_content = "VAULT_START\n"
    for filename, password in entries:
        vault_content += f'<div class="vault-entry" style="background: #2a2a2a; padding: 0.5rem; margin: 0.5rem 0; border-radius: 4px; display: flex; justify-content: space-between; align-items: center;">'
        vault_content += f'<span style="font-family: monospace;">{filename}</span>'
        vault_content += f'<div><span style="margin-right: 1rem; font-family: monospace; color: #f4c6c2;">{password}</span>'
        vault_content += f'<button class="copy-btn" data-password="{password}" style="background: #3a3a3a; border: none; color: white; padding: 0.25rem 0.5rem; border-radius: 3px; cursor: pointer;">Copy</button></div>'
        vault_content += '</div>\n'
    vault_content += "VAULT_END"

    # Encrypt and save
    encrypted = cryptojs_encrypt(vault_content, master_password)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(encrypted)

    print(f"Vault updated successfully at {output_file}")

if __name__ == "__main__":
    main()