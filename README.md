# 🌉 TeleBridge AI

> **Connect ChatGPT to your personal Telegram account.**

**TeleBridge AI** is an open-source local bridge that allows ChatGPT to interact with your personal Telegram account.

Ask ChatGPT to read your conversations, search message history, send messages, reply to people, or list your chats — while the actual Telegram connection stays on your own computer.

### ✨ Features

- 💬 Read recent Telegram messages
- 🔎 Search message history
- ✉️ Send messages
- ↩️ Reply to messages
- 📋 List your chats
- 🤖 Control Telegram using natural-language requests in ChatGPT
- 🖥️ Runs locally on Windows and Linux
- 🥧 Works on Raspberry Pi
- 🔓 Fully open source
- 🔐 Telegram session stays on your machine

---

# 🧠 How It Works

TeleBridge separates the AI from your Telegram authentication.

```text
┌───────────────┐
│    ChatGPT    │
└───────┬───────┘
        │
        │ Google Drive / Sheets
        ▼
┌───────────────────────┐
│ Google Apps Script    │
│ + Command Queue       │
└───────────┬───────────┘
            │
            │ Polling
            ▼
┌───────────────────────┐
│     TeleBridge AI     │
│       bridge.py       │
│                       │
│   Your PC / Server    │
└───────────┬───────────┘
            │
            │ Telethon
            ▼
┌───────────────────────┐
│       Telegram        │
│   Personal Account    │
└───────────────────────┘
```

ChatGPT creates a command in Google Sheets.

`bridge.py` running on your computer receives the command and executes it through Telegram using Telethon.

The result is written back to the command queue, where ChatGPT can read it.

```text
You
 ↓
ChatGPT
 ↓
Google Sheets
 ↓
bridge.py
 ↓
Telegram
 ↓
bridge.py
 ↓
Google Sheets
 ↓
ChatGPT
```

---

# 📦 Requirements

You need:

- Windows 10/11 or Linux
- Python 3.9+
- Telegram account
- Telegram API ID
- Telegram API Hash
- Google account
- Google Sheets
- Google Apps Script
- ChatGPT with compatible Google Drive/Sheets access

Recommended:

- Python 3.11+
- Git
- A computer that can remain online while you use the bridge

---

# 🚀 Installation

## 1. Download TeleBridge AI

Clone the repository:

```bash
git clone https://github.com/DimfulDMF/TeleBridge-AI.git
cd TeleBridge-AI
```

You can also download the repository as a ZIP from GitHub and extract it.

---

# 🐍 2. Install Python Dependencies

Using a virtual environment is recommended.

## Windows

Open PowerShell inside the TeleBridge AI folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell doesn't allow activation, use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

---

## Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

---

# 🔑 3. Get Telegram API Credentials

TeleBridge uses Telegram's client API through Telethon.

Open:

**https://my.telegram.org**

Log in with your Telegram account.

Then open:

```text
API development tools
```

Create an application.

Telegram will provide:

```text
API ID
API Hash
```

Example:

```text
API_ID=12345678
API_HASH=0123456789abcdef0123456789abcdef
```

⚠️ **Never publish your real API Hash.**

---

# ☁️ 4. Create the Google Command Queue

Create a new Google Spreadsheet.

Name it:

```text
TeleBridge AI
```

Create a sheet named:

```text
Commands
```

Add the following columns to the first row:

| id | command | target | text | status | result |
|---|---|---|---|---|---|

The bridge uses this sheet as a command queue.

A new command starts with:

```text
pending
```

When `bridge.py` receives it:

```text
processing
```

When the command finishes:

```text
done
```

If something fails:

```text
error
```

---

# 🔗 5. Install Google Apps Script

Open your **TeleBridge AI** spreadsheet.

Go to:

```text
Extensions
→ Apps Script
```

Delete the default example code.

Open:

```text
apps_script.gs
```

from this repository and copy its contents into the Apps Script editor.

---

# 🔐 6. Create a Bridge Secret

The bridge uses a secret to prevent random requests from accessing the command endpoint.

Create a long random value.

For example:

```text
YOUR_LONG_RANDOM_SECRET
```

⚠️ Do not actually use that example.

Generate your own random secret and configure it in the Apps Script.

The same secret will also be used by `bridge.py`.

Never publish your real `BRIDGE_SECRET`.

---

# 🌐 7. Deploy Apps Script

Inside Google Apps Script:

```text
Deploy
→ New deployment
→ Web app
```

Configure the deployment and deploy it.

Google will provide a URL similar to:

```text
https://script.google.com/macros/s/YOUR_DEPLOYMENT_ID/exec
```

Save this URL.

This is your:

```text
BRIDGE_URL
```

---

# ⚙️ 8. Configure TeleBridge

TeleBridge needs four important values:

```text
TG_API_ID
TG_API_HASH
BRIDGE_URL
BRIDGE_SECRET
```

If your version uses `.env`, copy:

```text
.env.example
```

to:

```text
.env
```

Example:

```env
TG_API_ID=12345678
TG_API_HASH=YOUR_TELEGRAM_API_HASH

BRIDGE_URL=https://script.google.com/macros/s/YOUR_DEPLOYMENT_ID/exec
BRIDGE_SECRET=YOUR_RANDOM_BRIDGE_SECRET
```

Replace the examples with your own values.

⚠️ Never upload your real `.env` file to GitHub.

---

# ▶️ 9. Start TeleBridge AI

## Windows

```powershell
python bridge.py
```

## Linux

```bash
python3 bridge.py
```

---

# 📱 10. First Telegram Login

The first time TeleBridge starts, Telethon may ask:

```text
Please enter your phone (or bot token):
```

Enter your Telegram phone number.

Example:

```text
+12345678900
```

Telegram will send you an authorization code.

Enter the code.

If Telegram 2FA is enabled, you will also see:

```text
Please enter your password:
```

Enter your Telegram 2FA password.

After successful authorization you should see something similar to:

```text
✅ Telegram authorized

Name: Example
Username: @example
ID: 123456789

✅ Google bridge connected

Waiting for commands...
```

Telethon creates a local `.session` file.

This allows TeleBridge to reconnect without asking for a Telegram login code every time.

---

# 🤖 11. Connect ChatGPT

Now connect ChatGPT to the Google account containing your TeleBridge spreadsheet.

In ChatGPT open:

```text
Settings
→ Apps
→ Google Drive
→ Connect
```

Sign in using the Google account containing:

```text
TeleBridge AI
```

Grant the required permissions.

ChatGPT should now be able to access the spreadsheet used by TeleBridge.

> **Note:** Connected-app availability and write permissions can depend on your ChatGPT plan, region, account, and current ChatGPT product configuration.

---

# 🧩 12. Tell ChatGPT How to Use TeleBridge

Start a new ChatGPT conversation.

You can give ChatGPT a prompt like this:

```text
Use my Google Sheet named "TeleBridge AI" as my Telegram command bridge.

The "Commands" sheet contains these columns:

id | command | target | text | status | result

To perform a Telegram operation, add a new command with a unique ID
and set its status to "pending".

bridge.py will receive the command, execute it locally through Telegram,
and write the result back into the result column.

Wait until the command finishes before reading its result.

Supported commands:

chats
read
search
send
reply
```

After that, you can use natural requests.

For example:

```text
Show me my Telegram chats.
```

Or:

```text
Read my latest messages with Alex.
```

Or:

```text
Search my conversation with Alex for "Minecraft".
```

Or:

```text
Send @username: Happy birthday! 🎉
```

ChatGPT creates the command, and your local TeleBridge executes it.

---

# 💬 Supported Commands

## `chats`

Lists Telegram dialogs.

Example:

```text
command: chats
status: pending
```

---

## `read`

Reads recent messages from a chat.

Example:

```text
command: read
target: Alex
status: pending
```

---

## `search`

Searches message history.

Example:

```text
command: search
target: Alex
text: Minecraft
status: pending
```

---

## `send`

Sends a real Telegram message from your account.

Example:

```text
command: send
target: @username
text: Hello!
status: pending
```

---

## `reply`

Replies to an existing Telegram message.

The exact parameters depend on the current `bridge.py` command format.

---

# 🔐 Security

TeleBridge AI is **open source**.

You can inspect the source code yourself and see how Telegram authentication, commands, and network requests are handled.

Your Telegram authentication happens locally on the computer running `bridge.py`.

ChatGPT does **not need your Telegram `.session` file, Telegram login code, or 2FA password**.

However, no software should be considered magically immune to account theft or security vulnerabilities.

You are responsible for protecting your credentials.

### Never publish:

```text
*.session
*.session-journal
.env
Telegram API Hash
Telegram login codes
Telegram 2FA password
BRIDGE_SECRET
```

Your Telegram `.session` file is especially sensitive.

Anyone who obtains a valid authenticated session may potentially gain access to your Telegram account.

Treat it like a password.

---

# 🛡️ Recommended `.gitignore`

Make sure your repository contains:

```gitignore
.env
*.session
*.session-journal

__pycache__/
*.pyc

.venv/
venv/
```

---

# 🖥️ Supported Platforms

TeleBridge AI is designed for:

- 🪟 **Windows**
- 🐧 **Linux**
- 🥧 **Raspberry Pi / Linux ARM**

An always-on Linux computer or Raspberry Pi can be used to keep TeleBridge available continuously.

---

# 🥧 Raspberry Pi

Installation on Raspberry Pi OS is almost identical to Linux:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git

git clone https://github.com/DimfulDMF/TeleBridge-AI.git
cd TeleBridge-AI

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python3 bridge.py
```

---

# 🛠️ Troubleshooting

### `ModuleNotFoundError: telethon`

Run:

```bash
pip install -r requirements.txt
```

---

### Google Bridge says `Unauthorized`

Check that:

```text
BRIDGE_SECRET
```

is exactly the same in Apps Script and your local configuration.

---

### Commands stay `pending`

Make sure:

```text
bridge.py
```

is running.

Also check:

- Internet connection
- Apps Script URL
- Apps Script deployment
- `BRIDGE_SECRET`
- Google Sheet structure

---

### Command stays `processing`

The bridge probably received the command but failed before returning the result.

Check the terminal running:

```text
bridge.py
```

for an error.

---

### Telegram asks for authorization every time

Make sure your `.session` file is not being deleted.

---

# 📁 Project Structure

```text
TeleBridge-AI/
│
├── bridge.py
│   └── Local Telegram client and command executor
│
├── apps_script.gs
│   └── Google Apps Script command endpoint
│
├── requirements.txt
│   └── Python dependencies
│
├── .env.example
│   └── Example configuration
│
├── .gitignore
│   └── Protects credentials and session files
│
└── README.md
    └── Documentation
```

---

# 🗺️ Roadmap

Possible future improvements:

- [ ] Better command authentication
- [ ] Encrypted command payloads
- [ ] Confirmation before sending messages
- [ ] Message pagination
- [ ] Media support
- [ ] Multiple Telegram accounts
- [ ] Docker support
- [ ] Native REST gateway
- [ ] WebSocket transport
- [ ] Replace Google Sheets with a dedicated gateway
- [ ] Additional messenger adapters

---

# ⚠️ Disclaimer

TeleBridge AI is an experimental open-source project.

It is **not affiliated with Telegram or OpenAI**.

Messages sent using TeleBridge are sent from your real Telegram account.

Do not use the project for:

- spam
- unsolicited bulk messaging
- harassment
- account abuse
- bypassing Telegram restrictions

Use automation responsibly and follow Telegram's Terms of Service.

---

# 💸 Support the Project

If you like **TeleBridge AI** and want to support its development, you can leave a donation:

### ❤️ Donate

**https://donatex.gg/donate/dimful1209**

Every donation helps support further development of TeleBridge AI.

---

# ⭐ TeleBridge AI

### Your Telegram. Your machine. Your AI bridge.

```text
AI ↔ Local Bridge ↔ Telegram
```

**Open source · Local-first · Under your control**

If you find TeleBridge AI useful, consider giving the repository a ⭐.