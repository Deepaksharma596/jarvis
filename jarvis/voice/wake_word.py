"""
wake_word.py - Background Wake Word Detection Engine
"""
import time
import threading
import logging
from typing import Callable, Optional
from config.settings import settings
from voice.speech_to_text import stt_engine

class WakeWordDetector:
    """Continuously listens for configured wake word ('Hey Assistant' / 'Jarvis')."""

    def __init__(self, on_wake_detected: Callable[[], None]):
        self.on_wake_detected = on_wake_detected
        self._listening = False
        self._thread: Optional[threading.Thread] = None

    def start(self):
        """Start background wake word detection loop."""
        if self._listening:
            return
        self._listening = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        logging.info(f"[WakeWord] Listening thread started for wake word '{settings.wake_word}'...")

    def stop(self):
        """Stop background wake word loop."""
        self._listening = False

    def _loop(self):
        wake_word_lower = settings.wake_word.lower()
        alt_wake_word = "jarvis"

        while self._listening:
            if not settings.wake_word_enabled:
                time.sleep(1.0)
                continue

            transcription = stt_engine.listen_and_transcribe(timeout=3.0, phrase_time_limit=4.0)
            if transcription:
                txt_lower = transcription.lower()
                if wake_word_lower in txt_lower or alt_wake_word in txt_lower:
                    logging.info(f"[WakeWord] Wake word detected in: '{transcription}'!")
                    self.on_wake_detected()
            time.sleep(0.1)
