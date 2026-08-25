"""
android_automation.py - Android Device Control & Automation Engine
"""
import os
import time
import logging
from typing import Optional, List, Dict
from mobile.banking_guard import BankingGuard

try:
    from jnius import autoclass, cast
    HAS_PYJNIUS = True
except ImportError:
    HAS_PYJNIUS = False

class AndroidAutomation:
    """Wrapper for Android device automation via Pyjnius and Android APIs."""

    @staticmethod
    def launch_app(app_name_or_package: str) -> Tuple[bool, str]:
        """Launch Android application by package name or common app title."""
        # 1. Banking Security Check
        allowed, reason = BankingGuard.validate_action(app_name_or_package, app_name_or_package)
        if not allowed:
            return False, reason

        if not HAS_PYJNIUS:
            msg = f"[MOCK MOBILE] Would launch Android app '{app_name_or_package}'"
            logging.info(msg)
            return True, msg

        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            context = PythonActivity.mActivity
            package_manager = context.getPackageManager()

            intent = package_manager.getLaunchIntentForPackage(app_name_or_package)
            if intent:
                context.startActivity(intent)
                return True, f"Launched Android app '{app_name_or_package}'."
            return False, f"App package '{app_name_or_package}' not found on device."
        except Exception as e:
            return False, f"Failed to launch app on Android: {e}"

    @staticmethod
    def make_call(phone_number: str) -> Tuple[bool, str]:
        """Initiate phone call."""
        allowed, reason = BankingGuard.validate_action(phone_number)
        if not allowed:
            return False, reason

        if not HAS_PYJNIUS:
            return True, f"[MOCK MOBILE] Initiated call to {phone_number}"

        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            
            intent = Intent(Intent.ACTION_CALL)
            intent.setData(Uri.parse(f"tel:{phone_number}"))
            PythonActivity.mActivity.startActivity(intent)
            return True, f"Calling {phone_number}..."
        except Exception as e:
            return False, f"Failed to make call: {e}"

    @staticmethod
    def send_sms(phone_number: str, message: str) -> Tuple[bool, str]:
        """Send SMS message."""
        allowed, reason = BankingGuard.validate_action(message)
        if not allowed:
            return False, reason

        if not HAS_PYJNIUS:
            return True, f"[MOCK MOBILE] Sent SMS to {phone_number}: '{message}'"

        try:
            SmsManager = autoclass('android.telephony.SmsManager')
            sms = SmsManager.getDefault()
            sms.sendTextMessage(phone_number, None, message, None, None)
            return True, f"Sent SMS to {phone_number}."
        except Exception as e:
            return False, f"Failed to send SMS: {e}"

    @staticmethod
    def adjust_volume(action: str = "up") -> Tuple[bool, str]:
        """Adjust system volume."""
        if not HAS_PYJNIUS:
            return True, f"[MOCK MOBILE] Adjusted volume ({action})"

        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Context = autoclass('android.content.Context')
            AudioManager = autoclass('android.media.AudioManager')

            audio_mgr = cast(AudioManager, PythonActivity.mActivity.getSystemService(Context.AUDIO_SERVICE))
            flag = AudioManager.ADJUST_RAISE if action == "up" else AudioManager.ADJUST_LOWER
            audio_mgr.adjustStreamVolume(AudioManager.STREAM_MUSIC, flag, AudioManager.FLAG_SHOW_UI)
            return True, f"Volume {action}."
        except Exception as e:
            return False, f"Failed to adjust volume: {e}"
