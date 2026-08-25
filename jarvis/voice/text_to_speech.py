"""
text_to_speech.py - Async & Offline Text-to-Speech Engine for JARVIS
"""
import os
import asyncio
import threading
import tempfile
import logging
from typing import Optional
from core.provider_interface import TTSProvider
from config.settings import settings

try:
    import edge_tts
    import pygame
    HAS_EDGE_TTS = True
except ImportError:
    HAS_EDGE_TTS = False

try:
    import pyttsx3
    HAS_PYTTSX3 = True
except ImportError:
    HAS_PYTTSX3 = False

class TTSEngine(TTSProvider):
    """High-quality natural neural voice synthesis with offline pyttsx3 fallback."""

    def __init__(self):
        self._is_speaking = False
        self._stop_requested = False
        self._thread: Optional[threading.Thread] = None

        if HAS_EDGE_TTS:
            try:
                pygame.mixer.init()
            except Exception as e:
                logging.warning(f"[TTS] Pygame mixer init warning: {e}")

    def speak(self, text: str, voice: str = None, rate: int = None, volume: float = None) -> None:
        """Asynchronously speak text."""
        if not text or not text.strip():
            return

        self.stop()
        self._stop_requested = False
        self._is_speaking = True

        v_voice = voice or settings.tts_voice
        v_rate = rate or settings.tts_rate
        v_vol = volume or settings.tts_volume

        self._thread = threading.Thread(
            target=self._run_speech,
            args=(text, v_voice, v_rate, v_vol),
            daemon=True
        )
        self._thread.start()

    def _run_speech(self, text: str, voice: str, rate: int, volume: float):
        # 1. Try Edge-TTS (high quality neural voice)
        if HAS_EDGE_TTS and not settings.mock_mode:
            try:
                asyncio.run(self._speak_edge_tts(text, voice, rate, volume))
                self._is_speaking = False
                return
            except Exception as e:
                logging.warning(f"[TTS] Edge-TTS playback failed: {e}. Falling back to PyTTSx3.")

        # 2. Try PyTTSx3 Offline Fallback
        if HAS_PYTTSX3 and not settings.mock_mode:
            try:
                engine = pyttsx3.init()
                engine.setProperty("rate", rate)
                engine.setProperty("volume", volume)
                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                logging.error(f"[TTS] PyTTSx3 playback failed: {e}")

        self._is_speaking = False

    async def _speak_edge_tts(self, text: str, voice: str, rate: int, volume: float):
        rate_str = f"+{rate - 150}%" if rate >= 150 else f"{rate - 150}%"
        vol_str = f"+{int((volume - 1.0) * 100)}%" if volume >= 1.0 else f"{int((volume - 1.0) * 100)}%"
        
        communicate = edge_tts.Communicate(text, voice, rate=rate_str, volume=vol_str)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tmp_path = fp.name

        try:
            await communicate.save(tmp_path)
            if self._stop_requested:
                return

            if pygame.mixer.get_init():
                pygame.mixer.music.load(tmp_path)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    if self._stop_requested:
                        pygame.mixer.music.stop()
                        break
                    await asyncio.sleep(0.05)
                pygame.mixer.music.unload()
        finally:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

    def stop(self) -> None:
        """Interrupt and stop speech immediately."""
        self._stop_requested = True
        if HAS_EDGE_TTS and pygame.mixer.get_init():
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass
        self._is_speaking = False

    def is_speaking(self) -> bool:
        return self._is_speaking

# Singleton TTS Instance
tts_engine = TTSEngine()
