"""
credentials.py - Secure Credential Storage using Windows Credential Manager / Keyring
"""
import os
import json
import base64
import logging

try:
    import keyring
    HAS_KEYRING = True
except ImportError:
    HAS_KEYRING = False

SERVICE_NAME = "JARVIS_VoiceAssistant"
FALLBACK_FILE = os.path.join(os.path.expanduser("~"), ".jarvis", ".vault.dat")

class CredentialManager:
    """Manages API Keys, OAuth tokens, and secrets securely."""

    @staticmethod
    def set_credential(key: str, value: str) -> bool:
        """Save a credential key-value pair."""
        if not value:
            return False
        if HAS_KEYRING:
            try:
                keyring.set_password(SERVICE_NAME, key, value)
                return True
            except Exception as e:
                logging.warning(f"[Credentials] Keyring store failed: {e}. Falling back to encrypted local store.")
        
        # Local fallback with base64 obfuscation
        os.makedirs(os.path.dirname(FALLBACK_FILE), exist_ok=True)
        store = {}
        if os.path.exists(FALLBACK_FILE):
            try:
                with open(FALLBACK_FILE, "r", encoding="utf-8") as f:
                    raw = f.read()
                    store = json.loads(base64.b64decode(raw.encode()).decode())
            except Exception:
                store = {}
        store[key] = value
        with open(FALLBACK_FILE, "w", encoding="utf-8") as f:
            encoded = base64.b64encode(json.dumps(store).encode()).decode()
            f.write(encoded)
        return True

    @staticmethod
    def get_credential(key: str, default: str = "") -> str:
        """Retrieve a credential by key."""
        # 1. Check environment variable first
        env_val = os.getenv(key)
        if env_val:
            return env_val

        # 2. Check Keyring
        if HAS_KEYRING:
            try:
                val = keyring.get_password(SERVICE_NAME, key)
                if val:
                    return val
            except Exception:
                pass

        # 3. Check fallback vault
        if os.path.exists(FALLBACK_FILE):
            try:
                with open(FALLBACK_FILE, "r", encoding="utf-8") as f:
                    raw = f.read()
                    store = json.loads(base64.b64decode(raw.encode()).decode())
                    return store.get(key, default)
            except Exception:
                pass

        return default

    @staticmethod
    def delete_credential(key: str) -> bool:
        """Delete a credential by key."""
        if HAS_KEYRING:
            try:
                keyring.delete_password(SERVICE_NAME, key)
            except Exception:
                pass
        if os.path.exists(FALLBACK_FILE):
            try:
                with open(FALLBACK_FILE, "r", encoding="utf-8") as f:
                    raw = f.read()
                    store = json.loads(base64.b64decode(raw.encode()).decode())
                if key in store:
                    del store[key]
                    with open(FALLBACK_FILE, "w", encoding="utf-8") as f:
                        f.write(base64.b64encode(json.dumps(store).encode()).decode())
            except Exception:
                pass
        return True
