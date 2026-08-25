# 🤖 JARVIS — Production-Quality AI Desktop Voice Assistant

**JARVIS** is a production-quality Windows desktop AI voice assistant built in Python. It understands natural language text and voice commands (in **English**, **Hindi**, and **Hinglish**), answers questions, and controls your computer through safe, observable, and permission-checked desktop and browser actions.

---

## ✨ Features

- 🎙️ **Voice System**: Continuous listening, Wake word ("Hey Assistant" / "Jarvis"), Push-to-talk, VAD noise handling, auto language detection (English, Hindi, Hinglish).
- 🗣️ **Text-to-Speech (TTS)**: High-quality natural neural voice synthesis (Edge-TTS) with PyTTSx3 offline fallback, speed & volume adjustments, interruptible playback.
- 🧠 **AI Orchestrator**: Modular LLM integration (Google Gemini, OpenAI GPT-4o, Ollama, and built-in intent engine) with strict JSON tool schemas.
- 🖥️ **Windows Desktop Control**: Application registry launcher (Brave, Chrome, WhatsApp, VS Code, Notepad, etc.), window management (switch, focus, min/max, close), native Windows UI Automation (`uiautomation`/`pywin32`), mouse & keyboard wrappers.
- 💬 **WhatsApp Automation**: Contact lookup, message composition, voice calling, file attachments, and recipient double-verification.
- 📧 **Gmail Integration**: Official Google Gmail REST API with OAuth2 authorization code flow and secure token storage via Windows Credential Manager.
- 🌐 **Brave/Chrome Browser Control**: Open URLs, search Google/YouTube, read DOM webpage text, scrape & summarize articles.
- 📁 **File Management**: Natural language file search, open, move, copy, rename, delete (strict user confirmation), PDF reader & summarizer.
- ⚙️ **System Control**: Volume control, brightness, CPU/RAM/Battery statistics, lock workstation, restart/shutdown (requires user confirmation).
- 🛡️ **3-Tier Permission Safety**: `SAFE` (auto execute), `CONFIRM` (user GUI prompt required), `BLOCKED` (prohibited actions). Confirmation modes: `Strict`, `Balanced`, `Trusted`.
- 🚨 **Global Emergency Stop**: Instant hotkey (`Ctrl+Shift+Esc`) to halt all running automations, mouse/keyboard inputs, and voice playback.
- 📋 **Multi-Step Task Planner**: Decomposes complex multi-intent requests into step-by-step plans visualized live in the GUI.
- 🔒 **Security & Audit Logging**: Redacted JSONL audit logger scrub secret API keys/passwords automatically. Stores secrets in Windows Credential Manager (`keyring`).
- 🧪 **Mock / Dry-Run Mode**: Full simulation engine allowing safe testing without moving real mouse or sending real messages (`python main.py --mock`).

---

## 🏗️ Modular Project Architecture

```
jarvis/
├── main.py                          # Main application entry point & CLI parser
├── requirements.txt                 # Complete Python dependencies
├── .env.example                     # Environment template
├── README.md                        # User manual & technical guide
├── run_jarvis.bat                   # Windows batch file launcher
├── config/
│   ├── settings.py                  # Settings dataclass & persistence (~/.jarvis/settings.json)
│   └── constants.py                 # Enums: PermissionLevel, ConfirmationMode, AIProviderType
├── core/
│   ├── agent.py                     # Central Orchestrator Agent
│   ├── planner.py                   # Multi-Step Task Decomposition Engine
│   ├── permissions.py               # 3-Tier Security Policy Manager
│   ├── memory.py                    # Conversation history & short-term entity resolver
│   ├── context.py                   # Windows active window & system status collector
│   └── provider_interface.py        # Abstract interfaces for AI, STT, TTS
├── voice/
│   ├── speech_to_text.py            # SpeechRecognition engine (English/Hindi/Hinglish)
│   ├── text_to_speech.py            # Async Edge-TTS + PyTTSx3 fallback
│   ├── wake_word.py                 # Background wake word listener ("Hey Assistant")
│   └── audio_utils.py               # Hardware mic/speaker manager
├── tools/
│   ├── base_tool.py                 # Base Tool class & ToolResult schema
│   ├── registry.py                  # Dynamic Tool Registry & execution validator
│   ├── desktop.py                   # App launcher, window switcher, focus, min/max
│   ├── browser.py                   # Brave/Chrome browser automation & webpage reader
│   ├── whatsapp.py                  # WhatsApp Desktop & Web messaging tool
│   ├── gmail.py                     # Gmail REST API & OAuth tool
│   ├── files.py                     # File search, open, create, delete, PDF reader
│   ├── system.py                    # Volume, brightness, battery, lock PC tools
│   ├── calendar.py                  # Reminders & local calendar scheduler
│   └── web_search.py                # Factual web research engine
├── automation/
│   ├── mouse.py                     # Safe mouse automation wrapper
│   ├── keyboard.py                  # Safe keyboard automation wrapper
│   ├── windows.py                   # Windows UI Automation & App Registry scanner
│   └── screenshots.py               # Screen capture & visual locator
├── ui/
│   ├── app.py                       # Main PyQt6 Desktop GUI
│   ├── tray.py                      # Windows System Tray Integration
│   ├── settings_dialog.py           # Configuration Settings Dialog
│   ├── components.py                # Animated avatar status, confirmation dialogs
│   └── styles.py                    # Dark glassmorphism QSS theme
├── security/
│   ├── credentials.py               # Windows Credential Manager integration
│   └── audit.py                     # Redacted audit logger
└── tests/
    ├── mock_mode.py                 # Dry-run command simulation runner
    ├── test_intent.py               # Intent detection unit tests
    ├── test_tools.py                # Tool registry unit tests
    └── test_permissions.py          # Safety permissions unit tests
```

---

## 🚀 Quick Setup Instructions for Windows

### 1. Requirements & Prerequisites
- **Windows 10 / 11**
- **Python 3.10+** (Python 3.11 recommended)
- Working Microphone & Speakers

### 2. Installation
Open PowerShell or Command Prompt in the project folder:
```bash
cd "d:\gk cil\jarvis"
pip install -r requirements.txt
```

### 3. Launching JARVIS
Double click `run_jarvis.bat` or run:
```bash
python main.py
```

To run in **Dry-Run / Simulation Mode** (no real mouse clicks or sent messages):
```bash
python main.py --mock
```

To execute a single command from CLI:
```bash
python main.py --text "Open Brave"
```

---

## 🗣️ Natural Language Command Examples

### Application Launcher & Desktop Control
- *"Open Brave."*
- *"Open WhatsApp."*
- *"Open VS Code."*
- *"Switch to Notepad."*
- *"Close Brave."*

### WhatsApp Automation
- *"WhatsApp Rahul: I'll reach at 7."*
- *"Send Priya good morning."*
- *"Call Rahul on WhatsApp."*

### Gmail Integration
- *"Check my latest emails."*
- *"Read the latest email."*
- *"Send email to Amit saying I'll send the report tomorrow."*

### Web Research & Browser Control
- *"Search Brave for CIL news."*
- *"Search YouTube for Python tutorials."*
- *"What is the capital of Australia?"*

### File Management & PDF Summarizer
- *"Find my PDF files."*
- *"Open Downloads folder."*
- *"Create a folder called CIL Preparation."*
- *"Read this PDF and summarize it."*

### System Control & Reminders
- *"Turn the volume down."*
- *"Set brightness to 80%."*
- *"Set a reminder for 7 PM to study."*
- *"Lock my laptop."*
- *"Get battery status."*

---

## 🧪 Running Automated Tests

Run the complete test suite via `pytest`:
```bash
pytest tests/ -v
```

Run command simulation dry-runs:
```bash
python tests/mock_mode.py
```

---

## 🛡️ Safety & Privacy Policy

1. **Explicit Tools Only**: The AI model is NEVER given unrestricted shell access. Every action is mediated through strongly typed tools with validated JSON schemas.
2. **Credential Redaction**: API keys and OAuth tokens are stored in Windows Credential Manager and automatically scrubbed from audit logs.
3. **Emergency Stop**: Pressing `Ctrl+Shift+Esc` instantly terminates all mouse/keyboard automations and TTS speech.
