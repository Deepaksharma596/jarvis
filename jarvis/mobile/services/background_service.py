"""
background_service.py - Android Foreground Service Wrapper for JARVIS Mobile
"""
import time
import logging
from mobile.wake_listener import MobileWakeListener
from core.agent import JARVISAgent
from voice.text_to_speech import tts_engine

class JARVISBackgroundService:
    """Foreground Android Service maintaining JARVIS background wake word listener."""

    def __init__(self):
        self.agent = JARVISAgent()
        self.listener = MobileWakeListener(on_wake_detected=self._on_jarvis_awakened)
        self.is_running = False

    def start_service(self):
        """Start background execution and notification service."""
        if self.is_running:
            return
        self.is_running = True
        self.listener.start()
        logging.info("[BackgroundService] JARVIS Mobile Service activated. Listening for 'Jarvis' in background...")

    def stop_service(self):
        """Stop background service."""
        self.is_running = False
        self.listener.stop()
        logging.info("[BackgroundService] JARVIS Mobile Service stopped.")

    def _on_jarvis_awakened(self):
        """Called when user says 'Jarvis' anywhere on phone."""
        tts_engine.speak("Yes? Listening...")
        # Listen for follow-up command
        from voice.speech_to_text import stt_engine
        cmd = stt_engine.listen_and_transcribe(timeout=5.0)
        if cmd:
            response_text, _ = self.agent.process_request(cmd)
            tts_engine.speak(response_text)

if __name__ == "__main__":
    service = JARVISBackgroundService()
    service.start_service()
    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        service.stop_service()
