"""
provider_interface.py - Abstract Provider Interfaces for JARVIS
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class AIProvider(ABC):
    """Abstract interface for LLM / AI Reasoning Providers."""
    
    @abstractmethod
    def generate_response(self, prompt: str, system_prompt: str = "", history: Optional[List[Dict[str, str]]] = None) -> str:
        """Generate textual response."""
        pass

    @abstractmethod
    def select_tools(self, user_request: str, available_tools: List[Dict[str, Any]], history: Optional[List[Dict[str, str]]] = None) -> List[Dict[str, Any]]:
        """Select tool calls (name and kwargs) for given request."""
        pass

class SpeechProvider(ABC):
    """Abstract interface for Speech-to-Text Providers."""
    
    @abstractmethod
    def listen_and_transcribe(self, timeout: float = 5.0) -> Optional[str]:
        """Listen from audio stream and return transcribed string."""
        pass

class TTSProvider(ABC):
    """Abstract interface for Text-to-Speech Providers."""
    
    @abstractmethod
    def speak(self, text: str, voice: str = None, rate: int = 175, volume: float = 1.0) -> None:
        """Speak given text asynchronously or synchronously."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stop current speech output immediately."""
        pass
