---
layout: splash
title: "Vault"
permalink: /vault/
author: "sado"
---

<div id="vault-unlock" class="unlock-container" style="max-width: 500px; margin: 2rem auto; text-align: center;">
  <input id="master-password" type="password" placeholder="Enter master password" class="unlock-input" 
         style="width: 100%; padding: 0.8rem; margin-bottom: 1rem; font-family: monospace; 
                background: #2a2a2a; color: white; border: 1px solid #444; border-radius: 4px;"
         autofocus>
  <button onclick="unlockVault()" class="unlock-button" 
          style="width: 100%; padding: 0.8rem; background: #f4c6c2; color: #2a2a2a; 
                 border: none; cursor: pointer; border-radius: 4px; font-weight: bold;">
    Unlock Vault
  </button>
  <p id="vault-status" style="margin-top: 1rem; color: #f4c6c2; min-height: 1.5rem;"></p>
</div>

<div id="vault-content" style="max-width: 800px; margin: 2rem auto; display: none;"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
<script>
// Auto-focus password field on page load
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('master-password').focus();
});

// Handle Enter key
document.getElementById('master-password').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') unlockVault();
});

async function unlockVault() {
    const password = document.getElementById('master-password').value;
    const status = document.getElementById('vault-status');
    const content = document.getElementById('vault-content');
    const unlockContainer = document.getElementById('vault-unlock');
    
    if (!password) {
        status.textContent = "Please enter the master password";
        return;
    }

    try {
        const response = await fetch('/_pages/vault_data.enc');
        const encryptedData = await response.text();
        
        // Parse the encrypted data
        const encrypted = CryptoJS.enc.Base64.parse(encryptedData);
        const salt = CryptoJS.lib.WordArray.create(encrypted.words.slice(2, 4), 8);
        const ciphertext = CryptoJS.lib.WordArray.create(encrypted.words.slice(4), encrypted.sigBytes - 16);
        
        // Derive key and IV
        const keyiv = CryptoJS.EvpKDF(password, salt, {
            keySize: 48/4,
            iterations: 1,
            hasher: CryptoJS.algo.MD5
        });
        
        const key = CryptoJS.lib.WordArray.create(keyiv.words.slice(0, 8));
        const iv = CryptoJS.lib.WordArray.create(keyiv.words.slice(8, 12));

        // Decrypt
        const decrypted = CryptoJS.AES.decrypt(
            { ciphertext: ciphertext },
            key,
            { 
                iv: iv,
                padding: CryptoJS.pad.Pkcs7,
                mode: CryptoJS.mode.CBC
            }
        );

        const decryptedText = decrypted.toString(CryptoJS.enc.Utf8);
        if (!decryptedText || !decryptedText.includes('VAULT_START')) {
            throw new Error("Invalid password or corrupted data");
        }

        // Hide the unlock form
        unlockContainer.style.display = 'none';
        
        // Extract and display the content
        const vaultContent = decryptedText.split('VAULT_START')[1].split('VAULT_END')[0];
        content.innerHTML = `
            <div style="background: #2a2a2a; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.2);">
                <h2 style="margin: 0 0 1.5rem; color: #f4c6c2; padding-bottom: 0.5rem; border-bottom: 1px solid #444; font-size: 1.5rem;">
                    Locked Posts
                </h2>
                <div style="margin-top: 1rem; max-height: 70vh; overflow-y: auto; padding-right: 0.5rem;">
                    ${vaultContent}
                </div>
            </div>
        `;
        content.style.display = 'block';
        status.textContent = '';
        
        // Add copy functionality
        document.querySelectorAll('.copy-btn').forEach(btn => {
            btn.onclick = function() {
                const text = this.getAttribute('data-password');
                navigator.clipboard.writeText(text).then(() => {
                    const original = this.textContent;
                    this.textContent = 'Copied!';
                    this.style.background = '#4CAF50';
                    setTimeout(() => {
                        this.textContent = original;
                        this.style.background = '#3a3a3a';
                    }, 2000);
                });
            };
        });
        
    } catch (err) {
        console.error('Decryption error:', err);
        status.textContent = "Incorrect password or corrupted vault";
        content.style.display = 'none';
    }
}
</script>