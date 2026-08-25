"""
audio_utils.py - Audio Hardware Enumeration & Processing Utilities
"""
import logging
from typing import List, Dict

try:
    import sounddevice as sd
    HAS_SOUNDDEVICE = True
except ImportError:
    HAS_SOUNDDEVICE = False

class AudioHardwareManager:
    """Enumerates available microphone and speaker hardware devices."""

    @staticmethod
    def list_microphones() -> List[Dict[str, Any]]:
        """Return list of input audio devices."""
        if not HAS_SOUNDDEVICE:
            return [{"id": 0, "name": "Default System Microphone"}]
        devices = []
        try:
            for idx, dev in enumerate(sd.query_devices()):
                if dev.get("max_input_channels", 0) > 0:
                    devices.append({"id": idx, "name": dev.get("name", f"Mic {idx}")})
        except Exception as e:
            logging.warning(f"[AudioHardware] Microphones query failed: {e}")
            devices = [{"id": 0, "name": "Default System Microphone"}]
        return devices

    @staticmethod
    def list_speakers() -> List[Dict[str, Any]]:
        """Return list of output audio devices."""
        if not HAS_SOUNDDEVICE:
            return [{"id": 0, "name": "Default System Speaker"}]
        devices = []
        try:
            for idx, dev in enumerate(sd.query_devices()):
                if dev.get("max_output_channels", 0) > 0:
                    devices.append({"id": idx, "name": dev.get("name", f"Speaker {idx}")})
        except Exception as e:
            logging.warning(f"[AudioHardware] Speakers query failed: {e}")
            devices = [{"id": 0, "name": "Default System Speaker"}]
        return devices
