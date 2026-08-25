# 📱 JARVIS Mobile — Android APK Compilation Guide

Why does Buildozer say `Unknown command/target android` on Windows native Command Prompt / PowerShell?

> **Technical Reason**: Buildozer relies on the Android SDK & NDK toolchain (`python-for-android`), which requires a **Linux/POSIX environment**. Buildozer automatically disables the `android` target when run natively on Windows without WSL or Linux.

---

## 🚀 3 Easy Ways to Build `JARVIS_Mobile.apk`

### Option 1: Google Colab (Free 1-Click Online Build — Recommended)

1. Open [Google Colab](https://colab.research.google.com/).
2. Open [`mobile/build_apk_colab.ipynb`](file:///d:/gk%20cil/jarvis/mobile/build_apk_colab.ipynb).
3. Run all cells. It will compile `JARVIS_Mobile-1.0.0-debug.apk` online and automatically download it to your browser!

---

### Option 2: Windows Subsystem for Linux (WSL)

1. Open PowerShell as Administrator and install WSL Ubuntu:
   ```powershell
   wsl --install -d Ubuntu
   ```
2. Open Ubuntu terminal and navigate to project folder:
   ```bash
   cd /mnt/d/gk\ cil/jarvis/mobile
   ```
3. Install buildozer and compile APK:
   ```bash
   sudo apt update && sudo apt install -y build-essential ccache git libffi-dev libssl-dev python3-dev zip unzip zlib1g-dev openjdk-17-jdk
   pip install buildozer cython
   buildozer android debug
   ```

---

### Option 3: GitHub Actions (Automated CI Build)

1. Push your repository to GitHub.
2. Go to the **Actions** tab in your GitHub repository.
3. Select **Build JARVIS Mobile APK** and click **Run workflow**.
4. Download the compiled `.apk` artifact directly from GitHub releases!
