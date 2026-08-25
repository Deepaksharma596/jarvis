"""
wake_listener.py - Mobile Background Wake Word Listener for "Jarvis"
"""
import time
import threading
import logging
from typing import Callable, Optional
from voice.speech_to_text import stt_engine
from config.settings import settings

class MobileWakeListener:
    """Continuously listens for 'Jarvis' in the background on mobile."""

    def __init__(self, on_wake_detected: Callable[[], None]):
        self.on_wake_detected = on_wake_detected
        self._listening = False
        self._thread: Optional[threading.Thread] = None

    def start(self):
        """Start background mobile wake word loop."""
        if self._listening:
            return
        self._listening = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        logging.info("[MobileWakeListener] Background listener started for 'Jarvis'...")

    def stop(self):
        """Stop background mobile listener."""
        self._listening = False

    def _loop(self):
        target = "jarvis"

        while self._listening:
            transcription = stt_engine.listen_and_transcribe(timeout=3.0, phrase_time_limit=4.0)
            if transcription:
                txt_lower = transcription.lower()
                if target in txt_lower:
                    logging.info(f"[MobileWakeListener] 'Jarvis' wake word detected in: '{transcription}'!")
                    self.on_wake_detected()
            time.sleep(0.2)
