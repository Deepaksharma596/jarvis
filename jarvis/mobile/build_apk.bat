@echo off
title JARVIS Mobile APK Builder
echo Setting up Buildozer environment...
set PATH=%LOCALAPPDATA%\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts;%PATH%
cd /d "%~dp0"
python -m buildozer android debug %*
pause
