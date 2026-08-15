# 🌉 TeleBridge AI

TeleBridge AI connects ChatGPT to your personal Telegram account through a local open-source bridge.

**ChatGPT → Google Sheet → Apps Script → bridge.py → Telegram**

Your Telegram session stays on your computer.

## Features

- Read recent messages
- Search chats
- Send and reply to messages
- List Telegram dialogs
- Windows / Linux / Raspberry Pi
- Automatic bridge-secret pairing
- Open source

# 🚀 Easy Setup

## 1. Download

```bash
git clone https://github.com/DimfulDMF/TeleBridge-AI.git
cd TeleBridge-AI
```

Or download the ZIP.

Important files:

```text
bridge.py
COPY_TO_APPS_SCRIPT.txt
SETUP_PROMPT.txt
requirements.txt
README.md
```

## 2. Connect Google Drive to ChatGPT

Open:

```text
ChatGPT → Settings → Apps → Google Drive → Connect
```

Connect the Google account you want to use.

## 3. Let ChatGPT guide the setup

Open `SETUP_PROMPT.txt`, copy **all** text and send it to ChatGPT.

ChatGPT first asks:

```text
| Choose your language before setup started |
| Выберите язык перед началом настройки |

🇷🇺 Русский
🇬🇧 English
```

After you choose, ChatGPT guides the installation.

When Google Drive write access is available, ChatGPT creates the spreadsheet automatically:

```text
TeleBridge AI
└── Commands
```

with:

```text
id | command | target | text | status | result
```

You do not need to type the columns manually.

# ☁️ Apps Script

ChatGPT will tell you to open:

```text
TeleBridge AI → Extensions → Apps Script
```

Open `COPY_TO_APPS_SCRIPT.txt` from this repository and copy **all** text.

In Apps Script:

```text
Delete default code → Paste → Save
```

Then:

```text
Deploy → New deployment → Web app
```

Use:

```text
Execute as: Me
```

Choose an access setting that allows your local bridge to call the deployed Web App, deploy it, and authorize your own script if Google asks.

Copy the Web App URL. It must end in `/exec`.

# 🔑 Telegram API

Open `my.telegram.org` → **API development tools** → create an application.

You need:

```text
API ID
API Hash
```

Keep the API Hash private.

# 🐍 Install & Run

### Windows

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python bridge.py
```

### Linux / Raspberry Pi

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 bridge.py
```

# 🔐 First Run

`bridge.py` asks locally for:

```text
Telegram API ID
Telegram API HASH
Google Apps Script Web App URL
```

It then automatically generates a secure `BRIDGE_SECRET`, pairs it with Apps Script, and stores configuration in:

```text
telebridge_config.json
```

Telegram may then ask locally for your phone number, login code, and 2FA password.

Successful startup:

```text
✅ Telegram authorized
✅ Google bridge connected
✅ Waiting for ChatGPT commands...
```

Keep `bridge.py` running.

# 💬 Usage

After setup, ask ChatGPT naturally:

```text
Show my Telegram chats.
Read my latest messages with Alex.
Search my chat with Alex for Minecraft.
Send @username: Hello!
```

Supported commands:

| Command | Action |
|---|---|
| `chats` | List dialogs |
| `read` | Read messages |
| `search` | Search one chat |
| `global_search` | Search dialogs |
| `send` | Send a message |
| `reply` | Reply to a message |

Status flow:

```text
pending → processing → done
```

# 🔄 Pair a New Computer

In Apps Script run:

```text
resetTeleBridgeSecret
```

Delete local `telebridge_config.json`, then run `bridge.py` again.

# 🔐 Security

Never share or upload:

```text
telebridge_config.json
*.session
*.session-journal
Telegram API Hash
Telegram login codes
Telegram 2FA password
BRIDGE_SECRET
```

Treat `.session` like a password.

# ⚠️ Disclaimer

TeleBridge AI is experimental and is not affiliated with Telegram or OpenAI. Do not use it for spam, harassment, unsolicited bulk messaging, or account abuse.

# 💸 Support

❤️ donatex.gg/donate/dimful1209

# ⭐ TeleBridge AI

**Your Telegram. Your machine. Your AI bridge.**
