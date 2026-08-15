# 🌉 TeleBridge AI

> **Connect ChatGPT to your personal Telegram account through a local, open-source bridge.**

TeleBridge AI lets ChatGPT read, search and send Telegram messages while your Telegram session stays on your own computer.

### ✨ Features

- 💬 Read recent messages
- 🔎 Search chats and history
- ✉️ Send messages
- ↩️ Reply to messages
- 📋 List dialogs
- 🖥️ Windows / Linux / Raspberry Pi
- 🔓 Open source
- 🔐 Telegram `.session` stays local

---

## 🧠 How it works

```text
ChatGPT
   ↓
Google Drive / Sheets
   ↓
Google Apps Script
   ↓
bridge.py on your computer
   ↓
Telethon
   ↓
Your Telegram account
```

ChatGPT writes a command to the `Commands` sheet. Your local bridge executes it through Telegram and writes the result back.

---

# 🚀 Setup

## 1. Install

```bash
git clone https://github.com/DimfulDMF/TeleBridge-AI.git
cd TeleBridge-AI
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 2. Get Telegram API credentials

Open **https://my.telegram.org** → sign in → **API development tools** → create an app.

Copy your:

```text
API ID
API Hash
```

Keep the API Hash private.

---

## 3. Create the Google bridge

Create a Google Spreadsheet named **TeleBridge AI**.

Open:

```text
Extensions → Apps Script
```

Replace the default code with `apps_script.gs` from this repository.

Then:

```text
Deploy → New deployment → Web app
```

Copy the Web App URL ending in `/exec`.

### 🔐 Automatic secret setup

You no longer need to manually generate or paste `BRIDGE_SECRET`.

On first launch, `bridge.py` automatically:

1. generates a strong random secret;
2. registers it in Apps Script;
3. saves it locally with your other settings.

Run the bridge after deploying Apps Script to complete the one-time pairing.

---

## 4. First launch

### Windows

```powershell
python bridge.py
```

### Linux

```bash
python3 bridge.py
```

TeleBridge asks for:

```text
Telegram API ID
Telegram API HASH
Google Apps Script Web App URL
```

It then creates `telebridge_config.json` and remembers these settings.

Telethon will then ask for:

```text
Phone number
Telegram login code
2FA password (if enabled)
```

A successful startup looks like:

```text
✅ Bridge secret registered automatically.
✅ Configuration saved to telebridge_config.json.
✅ Telegram authorized
✅ Google bridge connected
✅ Waiting for AI commands...
```

Next time, just run `python bridge.py` again — no API ID, Hash, URL or bridge-secret setup is needed.

> To pair a new machine, run `resetTeleBridgeSecret()` manually in Apps Script and delete the local `telebridge_config.json`.

---

# 🤖 Connect ChatGPT

In ChatGPT open:

```text
Settings → Apps → Google Drive → Connect
```

Connect the Google account containing the **TeleBridge AI** spreadsheet.

Then tell ChatGPT:

```text
Use my Google Sheet named "TeleBridge AI" as my Telegram command bridge.

The Commands sheet uses:
id | command | target | text | status | result

Create commands with a unique id and status "pending".
Wait for bridge.py to execute them and then read the result.

Supported commands:
chats
read
search
global_search
send
reply
```

Examples:

```text
Show my Telegram chats.
Read my latest messages with Alex.
Search my chat with Alex for "Minecraft".
Send @username: Happy birthday! 🎉
```

> Google Drive app availability and write access can depend on your ChatGPT account and current product configuration.

---

# 🛠 Commands

| Command | Purpose |
|---|---|
| `chats` | List dialogs |
| `read` | Read recent text messages |
| `search` | Search one chat |
| `global_search` | Search across dialogs |
| `send` | Send a message |
| `reply` | Reply to a message |

For `reply`:

```text
target = chat
text = MESSAGE_ID|your reply
```

---

# 🔐 Security

Telegram authentication happens locally. ChatGPT does **not** need your login code, 2FA password or `.session` file.

Never publish:

```text
telebridge_config.json
*.session
*.session-journal
Telegram API Hash
Telegram login codes
Telegram 2FA password
```

Recommended `.gitignore`:

```gitignore
telebridge_config.json
*.session
*.session-journal
.venv/
venv/
__pycache__/
*.pyc
```

Open source lets you inspect what the bridge does, but it does not make software immune to bugs. Protect your local configuration and Telegram session.

---

# 🖥️ Platforms

- 🪟 Windows
- 🐧 Linux
- 🥧 Raspberry Pi / Linux ARM

---

# ⚠️ Disclaimer

TeleBridge AI is experimental and is **not affiliated with Telegram or OpenAI**.

Messages are sent from your real Telegram account. Do not use TeleBridge for spam, harassment, unsolicited bulk messaging or other abuse. Follow Telegram's Terms of Service.

---

# 💸 Support the Project

**❤️ https://donatex.gg/donate/dimful1209**

---

# ⭐ TeleBridge AI

### Your Telegram. Your machine. Your AI bridge.

**Open source · Local-first · Under your control**
