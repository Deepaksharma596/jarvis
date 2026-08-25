"""
test_banking_guard.py - Pytest unit tests for BankingGuard Security
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from mobile.banking_guard import BankingGuard

def test_banking_packages_blocked():
    blocked_packages = [
        "com.google.android.apps.nfc.pay",
        "com.phonepe.app",
        "net.one97.paytm",
        "com.sbi.lotusintouch",
        "com.hdfcbank.mobilebanking",
        "com.icicibank.mobilebanking",
        "com.dreamplug.android.cred"
    ]
    for pkg in blocked_packages:
        assert BankingGuard.is_banking_package(pkg) is True
        allowed, reason = BankingGuard.validate_action(pkg, pkg)
        assert allowed is False
        assert "SECURITY BLOCK" in reason

def test_banking_keywords_blocked():
    blocked_queries = [
        "Open GPay",
        "Check PhonePe balance",
        "Send money on Paytm",
        "Show YONO SBI passbook",
        "Read OTP SMS for bank"
    ]
    for query in blocked_queries:
        assert BankingGuard.is_banking_title_or_query(query) is True
        allowed, reason = BankingGuard.validate_action(query)
        assert allowed is False
        assert "SECURITY BLOCK" in reason

def test_non_banking_apps_allowed():
    allowed_apps = [
        "com.whatsapp",
        "com.google.android.youtube",
        "com.android.chrome",
        "Open WhatsApp",
        "Call Mom"
    ]
    for app in allowed_apps:
        allowed, _ = BankingGuard.validate_action(app)
        assert allowed is True
