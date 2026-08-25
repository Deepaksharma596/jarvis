"""
banking_guard.py - Strict Security Guard for Excluding Banking & Financial Apps
"""
import logging
from typing import Tuple, List

# Blacklist of Banking, UPI, Payment, Wallet, and Financial Package Names & App Titles
BANKING_PACKAGE_BLACKLIST = {
    # UPI & Mobile Wallets
    "com.google.android.apps.nfc.pay",        # Google Pay
    "com.phonepe.app",                         # PhonePe
    "net.one97.paytm",                        # Paytm
    "in.org.npci.upiapp",                      # BHIM UPI
    "com.amazon.mShop.android.shopping",       # Amazon Pay
    "com.dreamplug.android.cred",              # CRED
    "com.mobikwik_new",                       # MobiKwik
    "com.freecharge.android",                  # Freecharge

    # Major Indian & Global Banks
    "com.sbi.lotusintouch",                    # YONO SBI
    "com.sbi.upi",                             # YONO Lite / SBI Pay
    "com.hdfcbank.mobilebanking",              # HDFC Bank MobileBanking
    "com.icicibank.mobilebanking",             # ICICI iMobile
    "com.csam.icici.bank.imobile",             # ICICI iMobile Pay
    "com.axis.mobile",                         # Axis Mobile
    "com.kotak.mbanking",                      # Kotak Bank
    "com.bankofbaroda.mconnect",               # BOB World
    "com.canarabank.mobikwik",                 # Canara ai1
    "com.pnb.pnbone",                          # PNB ONE
    "com.unionbank.mconnect",                  # Vyom Union Bank
    "com.indusind.mobile",                     # IndusMobile
    "com.idfcfirstbank.mobilebanking",         # IDFC FIRST Bank
    "com.rblbank.mobank",                      # RBL MoBank

    # International Financial & Crypto
    "com.paypal.android.p2pmobile",            # PayPal
    "com.revolut.revolut",                     # Revolut
    "com.wise.android",                        # Wise
    "com.coinbase.android",                    # Coinbase
    "com.binance.dev",                         # Binance
}

BANKING_KEYWORDS = [
    "bank", "banking", "yono", "gpay", "google pay", "phonepe", "paytm",
    "bhim", "upi", "cred", "wallet", "passbook", "statement", "netbanking",
    "credit card", "debit card", "atm pin", "cvv", "otp"
]

class BankingGuard:
    """Security guard ensuring JARVIS never reads or automates banking/financial applications."""

    @classmethod
    def is_banking_package(cls, package_name: str) -> bool:
        """Check if package name matches blacklisted financial apps."""
        if not package_name:
            return False
        pkg_lower = package_name.lower().strip()
        return any(b_pkg in pkg_lower for b_pkg in BANKING_PACKAGE_BLACKLIST)

    @classmethod
    def is_banking_title_or_query(cls, text: str) -> bool:
        """Check if app title or user target query involves financial/banking terms."""
        if not text:
            return False
        txt_lower = text.lower().strip()
        return any(kw in txt_lower for kw in BANKING_KEYWORDS)

    @classmethod
    def validate_action(cls, target_name: str, package_name: str = "") -> Tuple[bool, str]:
        """
        Validate whether an automation action is safe.
        Returns (is_allowed, reason)
        """
        if cls.is_banking_package(package_name):
            reason = f"SECURITY BLOCK: Access to banking package '{package_name}' is strictly prohibited."
            logging.warning(f"[BankingGuard] {reason}")
            return False, reason

        if cls.is_banking_title_or_query(target_name):
            reason = f"SECURITY BLOCK: Target '{target_name}' involves protected banking/financial operations."
            logging.warning(f"[BankingGuard] {reason}")
            return False, reason

        return True, "Action allowed."
