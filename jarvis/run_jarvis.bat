@echo off
title JARVIS AI Desktop Voice Assistant
echo Starting JARVIS Assistant...
cd /d "%~dp0"
python main.py %*
pause
