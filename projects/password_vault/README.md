# 🔐 Secure Password Vault

## User Story
> *As a security-conscious user, I want a local AES-256 encrypted vault so that my passwords are never stored in plain text.*

## Sprint Delivery
| Sprint | Goal | Status |
|--------|------|--------|
| Sprint 1 | Crypto engine + key derivation | ✅ Done |
| Sprint 2 | CRUD operations + persistence | ✅ Done |
| Sprint 3 | CLI + search + delete | ✅ Done |

## Security Design
- **Encryption:** AES-256 via Fernet (symmetric)
- **Key Derivation:** PBKDF2HMAC-SHA256, 390,000 iterations (OWASP 2023)
- **Salt:** 32 random bytes, stored separately at `~/.vault_salt`
- **File permissions:** `chmod 600` on vault and salt files

## Usage
```bash
pip install cryptography
python vault.py add github myusername
python vault.py get github
python vault.py list
python vault.py search git
python vault.py delete github
```
