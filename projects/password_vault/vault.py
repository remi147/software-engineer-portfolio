#!/usr/bin/env python3
"""
Secure Password Vault
======================
AES-256 encrypted local password manager using Fernet symmetric
encryption with PBKDF2HMAC key derivation.

User Story: As a security-conscious user, I want a local encrypted
vault so that my passwords are never stored in plain text.
"""

import argparse
import base64
import json
import os
import sys
from getpass import getpass
from pathlib import Path
from typing import Dict, Optional

try:
    from cryptography.fernet import Fernet, InvalidToken
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
except ImportError:
    print("Install dependencies: pip install cryptography")
    sys.exit(1)


VAULT_FILE = Path.home() / ".secure_vault.enc"
SALT_FILE = Path.home() / ".vault_salt"
ITERATIONS = 390_000  # OWASP recommended minimum for PBKDF2-SHA256


class CryptoEngine:
    """Handles key derivation and encryption/decryption."""

    @staticmethod
    def derive_key(password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=ITERATIONS,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))

    @staticmethod
    def get_or_create_salt(salt_path: Path) -> bytes:
        if salt_path.exists():
            return salt_path.read_bytes()
        salt = os.urandom(32)
        salt_path.write_bytes(salt)
        salt_path.chmod(0o600)
        return salt


class PasswordVault:
    """
    Encrypted password storage with master-key authentication.
    Sprint 2 deliverable: CRUD operations on vault entries.
    """

    def __init__(self, master_password: str,
                 vault_path: Path = VAULT_FILE,
                 salt_path: Path = SALT_FILE):
        salt = CryptoEngine.get_or_create_salt(salt_path)
        key = CryptoEngine.derive_key(master_password, salt)
        self.fernet = Fernet(key)
        self.vault_path = vault_path
        self._data: Dict[str, dict] = self._load()

    def _load(self) -> Dict[str, dict]:
        if not self.vault_path.exists():
            return {}
        try:
            encrypted = self.vault_path.read_bytes()
            decrypted = self.fernet.decrypt(encrypted)
            return json.loads(decrypted.decode("utf-8"))
        except InvalidToken:
            print("❌ Wrong master password or corrupted vault.")
            sys.exit(1)

    def _save(self):
        raw = json.dumps(self._data, indent=2).encode("utf-8")
        encrypted = self.fernet.encrypt(raw)
        self.vault_path.write_bytes(encrypted)
        self.vault_path.chmod(0o600)

    def add(self, service: str, username: str, password: str, notes: str = "") -> None:
        self._data[service] = {
            "username": username,
            "password": password,
            "notes": notes
        }
        self._save()
        print(f"✅ '{service}' saved.")

    def get(self, service: str) -> Optional[dict]:
        return self._data.get(service)

    def delete(self, service: str) -> bool:
        if service in self._data:
            del self._data[service]
            self._save()
            return True
        return False

    def list_services(self) -> list:
        return sorted(self._data.keys())

    def search(self, query: str) -> list:
        q = query.lower()
        return [s for s in self._data if q in s.lower()]


def main():
    parser = argparse.ArgumentParser(description="🔐 Secure Password Vault")
    sub = parser.add_subparsers(dest="cmd")

    add_p = sub.add_parser("add", help="Add or update a credential")
    add_p.add_argument("service")
    add_p.add_argument("username")
    add_p.add_argument("--notes", default="")

    sub.add_parser("list", help="List all services")

    get_p = sub.add_parser("get", help="Retrieve a credential")
    get_p.add_argument("service")

    del_p = sub.add_parser("delete", help="Delete a credential")
    del_p.add_argument("service")

    search_p = sub.add_parser("search", help="Search services")
    search_p.add_argument("query")

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help(); return

    master = getpass("🔑 Master password: ")
    vault = PasswordVault(master)

    if args.cmd == "add":
        pwd = getpass(f"Password for {args.service}: ")
        vault.add(args.service, args.username, pwd, args.notes)
    elif args.cmd == "get":
        entry = vault.get(args.service)
        if entry:
            print(f"  Service:  {args.service}")
            print(f"  Username: {entry['username']}")
            print(f"  Password: {entry['password']}")
            if entry['notes']:
                print(f"  Notes:    {entry['notes']}")
        else:
            print(f"❌ '{args.service}' not found.")
    elif args.cmd == "list":
        services = vault.list_services()
        print(f"\n🗂  {len(services)} service(s) in vault:")
        for s in services:
            print(f"  • {s}")
    elif args.cmd == "delete":
        ok = vault.delete(args.service)
        print(f"✅ Deleted." if ok else f"❌ '{args.service}' not found.")
    elif args.cmd == "search":
        results = vault.search(args.query)
        print(f"Found: {', '.join(results) or 'No matches.'}")


if __name__ == "__main__":
    main()
