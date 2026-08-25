"""
speech_to_text.py - Continuous & Push-to-Talk Speech Recognition Engine
"""
import logging
from typing import Optional
from core.provider_interface import SpeechProvider
from config.settings import settings

try:
    import speech_recognition as sr
    HAS_SR = True
except ImportError:
    HAS_SR = False

class STTEngine(SpeechProvider):
    """Speech Recognition supporting English, Hindi, and Hinglish commands."""

    def __init__(self):
        self.recognizer = sr.Recognizer() if HAS_SR else None
        self._mic_error_logged = False
        if self.recognizer:
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 1.0  # Seconds of silence to consider phrase complete

    def listen_and_transcribe(self, timeout: float = 5.0, phrase_time_limit: float = 10.0) -> Optional[str]:
        """Capture microphone input and transcribe to text string."""
        if not HAS_SR or settings.mock_mode:
            return None

        try:
            with sr.Microphone() as source:
                self._mic_error_logged = False
                logging.info("[STT] Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.4)
                logging.info("[STT] Listening for voice input...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

            logging.info("[STT] Transcribing audio...")
            lang = settings.stt_language
            text = self.recognizer.recognize_google(audio, language=lang)
            logging.info(f"[STT] Transcribed: '{text}'")
            return text
        except sr.WaitTimeoutError:
            logging.info("[STT] Listening timed out waiting for speech.")
            return None
        except sr.UnknownValueError:
            logging.info("[STT] Speech input could not be understood.")
            return None
        except OSError as e:
            if not self._mic_error_logged:
                logging.warning(f"[STT] Microphone access issue: {e}. Check mic hardware/permissions.")
                self._mic_error_logged = True
            return None
        except Exception as e:
            if not self._mic_error_logged:
                logging.warning(f"[STT] Error during speech recognition: {e}")
                self._mic_error_logged = True
            return None

# Singleton STT Engine
stt_engine = STTEngine()
