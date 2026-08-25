"""
constants.py - Enums and global constants for JARVIS Assistant
"""
from enum import Enum

class PermissionLevel(str, Enum):
    SAFE = "SAFE"        # Can execute automatically without asking
    CONFIRM = "CONFIRM"  # Requires explicit user confirmation
    BLOCKED = "BLOCKED"  # Strictly prohibited / dangerous actions

class ConfirmationMode(str, Enum):
    STRICT = "STRICT"      # Confirm every external action
    BALANCED = "BALANCED"  # Confirm messages, emails, calls, file deletion, system changes
    TRUSTED = "TRUSTED"    # Auto-execute safe & pre-approved actions

class AIProviderType(str, Enum):
    GEMINI = "gemini"
    OPENAI = "openai"
    OLLAMA = "ollama"
    MOCK = "mock"

class SpeechProviderType(str, Enum):
    WHISPER_LOCAL = "whisper_local"
    GOOGLE_WEB = "google_web"
    MOCK = "mock"

class TTSProviderType(str, Enum):
    EDGE_TTS = "edge_tts"
    PYTTSX3 = "pyttsx3"
    MOCK = "mock"

# Global emergency stop key combination
EMERGENCY_STOP_HOTKEY = "ctrl+shift+esc"
