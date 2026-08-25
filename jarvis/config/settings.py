"""
settings.py - Application settings manager for JARVIS
"""
import os
import json
from dataclasses import dataclass, field, asdict
from typing import Dict, Any
from config.constants import ConfirmationMode, AIProviderType, SpeechProviderType, TTSProviderType

SETTINGS_DIR = os.path.join(os.path.expanduser("~"), ".jarvis")
SETTINGS_FILE = os.path.join(SETTINGS_DIR, "settings.json")

@dataclass
class Settings:
    # AI Config
    ai_provider: str = AIProviderType.GEMINI.value
    ai_model: str = "gemini-3.6-flash"
    ai_temperature: float = 0.2
    
    # Voice Config
    wake_word: str = "Hey Assistant"
    wake_word_enabled: bool = True
    stt_provider: str = SpeechProviderType.GOOGLE_WEB.value
    stt_language: str = "en-IN"  # Auto detect or default English/Hindi/Hinglish
    tts_provider: str = TTSProviderType.EDGE_TTS.value
    tts_voice: str = "en-US-AriaNeural"  # Fallback: hi-IN-SwaraNeural
    tts_rate: int = 175
    tts_volume: float = 1.0
    
    # Safety & Permissions
    confirmation_mode: str = ConfirmationMode.BALANCED.value
    trusted_contacts: list = field(default_factory=list)
    trusted_applications: list = field(default_factory=lambda: ["notepad", "calc", "cmd", "explorer"])
    
    # Automation & System
    browser_name: str = "brave"  # brave, chrome, edge
    automation_speed: float = 0.5  # delay in seconds for mouse/keyboard
    emergency_stop_enabled: bool = True
    mock_mode: bool = False
    
    # Theme & UI
    theme: str = "dark"
    start_minimized: bool = False
    
    def save(self):
        """Persist settings to JSON file."""
        os.makedirs(SETTINGS_DIR, exist_ok=True)
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=4)

    @classmethod
    def load(cls) -> "Settings":
        """Load settings from JSON file or return defaults."""
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
            except Exception as e:
                print(f"[Settings] Error loading settings, falling back to defaults: {e}")
        settings = cls()
        settings.save()
        return settings

# Global singleton settings instance
settings = Settings.load()
