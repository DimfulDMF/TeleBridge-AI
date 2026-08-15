# 🌉 TeleBridge AI

> Connect ChatGPT to your personal Telegram account.

**TeleBridge AI** is an open-source local bridge that allows ChatGPT to read, search and send Telegram messages through your own Telegram account.

Your Telegram session stays on **your computer**.

---

## ✨ Features

- 💬 Read recent Telegram messages
- 🔎 Search messages in a chat
- 🌍 Search across Telegram dialogs
- ✉️ Send messages
- ↩️ Reply to messages
- 📋 List your Telegram chats
- 🪟 Windows support
- 🐧 Linux support
- 🥧 Raspberry Pi support
- 🔐 Local Telegram authentication
- 🔓 Open source
- 🤖 ChatGPT-guided installation

---

# 🧠 How does it work?

```text
You
 ↓
ChatGPT
 ↓
Google Drive / Google Sheets
 ↓
Google Apps Script
 ↓
bridge.py
 ↓
Telethon
 ↓
Telegram
```

ChatGPT writes commands into a Google Sheet.

Your local `bridge.py` receives those commands, executes them through your Telegram account and sends the result back.

Your Telegram `.session` file stays on your computer.

---

# 🚀 Installation

TeleBridge AI includes an interactive setup prompt.

Instead of manually configuring the Google Sheet, you can let **ChatGPT do most of the setup for you**.

---

## 1. Download TeleBridge AI

Clone the repository:

```bash
git clone https://github.com/DimfulDMF/TeleBridge-AI.git
cd TeleBridge-AI
```

Or download the repository as a ZIP from GitHub.

The project contains:

```text
TeleBridge-AI/
├── bridge.py
├── COPY_TO_APPS_SCRIPT.txt
├── SETUP_PROMPT.txt
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🤖 2. Start the ChatGPT Setup Assistant

Open:

```text
SETUP_PROMPT.txt
```

Copy **ALL** text from the file.

Open a new ChatGPT conversation and paste it.

The first response should be:

```text
| Choose your language before setup started |
| Выберите язык перед началом настройки |

🇷🇺 Русский
🇬🇧 English
```

Choose your language.

From this point, ChatGPT will guide you through the installation.

---

# ☁️ 3. Google Drive

TeleBridge uses a Google Sheet as the bridge between ChatGPT and your computer.

After you choose a language, ChatGPT will check whether it can access Google Drive.

If Google Drive is not connected, ChatGPT should first attempt to initiate the Google Drive connection/authorization flow for you.

You may only need to confirm the connection in the ChatGPT interface.

If automatic connection is unavailable, use:

```text
ChatGPT
→ Settings
→ Apps
→ Google Drive
→ Connect
```

Connect the Google account that you want to use with TeleBridge.

---

# 📊 4. Automatic Spreadsheet Setup

After Google Drive is connected, ChatGPT will attempt to create:

```text
TeleBridge AI
```

with a sheet/tab named:

```text
Commands
```

and these columns:

```text
id | command | target | text | status | result
```

You should **not need to create these columns manually** when Google Drive write access is available.

If your ChatGPT account does not currently allow Google Drive write actions, the setup assistant will tell you what must be created manually.

---

# ⚙️ 5. Google Apps Script

After the spreadsheet is ready, ChatGPT will tell you to open it.

Inside Google Sheets:

```text
Extensions
→ Apps Script
```

Now open this file from TeleBridge:

```text
COPY_TO_APPS_SCRIPT.txt
```

Copy **ALL** of its contents.

Return to Google Apps Script.

Delete the default code and paste the TeleBridge code.

Then press:

```text
Save
```

You do not need to edit the code.

---

# 🌐 6. Deploy the Bridge

Inside Google Apps Script:

```text
Deploy
→ New deployment
```

Choose:

```text
Web app
```

Set:

```text
Execute as:
Me
```

Choose an access option that allows the local TeleBridge program to call the Web App.

Then press:

```text
Deploy
```

Google may ask you to authorize your own Apps Script project.

Complete the authorization.

After deployment, Google gives you a Web App URL similar to:

```text
https://script.google.com/macros/s/XXXXXXXXXXXX/exec
```

Copy it.

⚠️ The URL used by TeleBridge must be the deployed Web App URL ending in:

```text
/exec
```

---

# 🔑 7. Get Telegram API Credentials

Open:

```text
https://my.telegram.org
```

Sign in using your Telegram account.

Open:

```text
API development tools
```

Create an application if necessary.

You need:

```text
API ID
API Hash
```

⚠️ Keep your API Hash private.

Do **not** send your API Hash, login code or 2FA password to ChatGPT.

They are entered locally.

---

# 🐍 8. Install TeleBridge

## 🪟 Windows

Open PowerShell in the TeleBridge folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Then:

```powershell
python bridge.py
```

---

## 🐧 Linux

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python3 bridge.py
```

---

## 🥧 Raspberry Pi

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

# 🔐 9. First Launch

On the first launch, `bridge.py` asks locally for:

```text
Telegram API ID:
Telegram API HASH:
Google Apps Script Web App URL:
```

Enter the information directly into the terminal.

Do **not** send these credentials to ChatGPT.

TeleBridge automatically:

```text
✓ generates a secure BRIDGE_SECRET
✓ registers the secret in Apps Script
✓ saves your configuration locally
```

The configuration is stored in:

```text
telebridge_config.json
```

You do not need to manually generate or copy the bridge secret.

---

# 📱 10. Telegram Login

Telethon may ask locally for:

```text
Phone number
Telegram login code
2FA password
```

Enter these directly into your terminal.

After successful authorization you should see:

```text
✅ Telegram authorized
✅ Google bridge connected
✅ Waiting for ChatGPT commands...
```

Keep `bridge.py` running while using TeleBridge.

---

# 🧪 11. Automatic Test

Return to the ChatGPT conversation where you ran `SETUP_PROMPT.txt`.

Tell ChatGPT that the bridge is running.

ChatGPT should create a safe test command:

```text
command: chats
status: pending
```

Your local bridge should detect it:

```text
▶ chats
✅ Done
```

ChatGPT can then read the result from the spreadsheet.

If the chat list is returned successfully:

```text
🎉 TeleBridge AI is connected!
```

---

# 💬 Using TeleBridge

After installation, you can talk naturally.

For example:

```text
Show my Telegram chats.
```

```text
Read my latest 40 messages with Alex.
```

```text
Search my chat with Alex for Minecraft.
```

```text
Send @username: Hello!
```

```text
Reply to message 12345 in Alex chat with: Sounds good!
```

ChatGPT converts your request into a TeleBridge command.

---

# 🛠 Supported Commands

| Command | Description |
|---|---|
| `chats` | List Telegram dialogs |
| `read` | Read recent messages |
| `search` | Search one chat |
| `global_search` | Search dialogs |
| `send` | Send a message |
| `reply` | Reply to a message |

---

# 📡 Command Format

The `Commands` sheet uses:

```text
id | command | target | text | status | result
```

Example:

```text
abc123 | send | @username | Hello! | pending |
```

TeleBridge changes:

```text
pending
↓
processing
↓
done
```

The result appears in:

```text
result
```

If something fails:

```text
error
```

is used instead.

---

# 🔁 Starting TeleBridge Again

After the first setup, your settings are remembered.

Simply run:

### Windows

```powershell
python bridge.py
```

### Linux / Raspberry Pi

```bash
python3 bridge.py
```

You normally do not need to enter API ID, API Hash or the Apps Script URL again.

---

# 🔄 Pairing Another Computer

TeleBridge's automatic secret setup is intentionally one-time.

To pair another installation:

Open your Apps Script project.

Run:

```text
resetTeleBridgeSecret
```

Then delete locally:

```text
telebridge_config.json
```

Run:

```bash
python bridge.py
```

again.

TeleBridge generates a new secret.

---

# 🔐 Security

Never publish or send:

```text
telebridge_config.json
*.session
*.session-journal

Telegram API Hash
Telegram login code
Telegram 2FA password
BRIDGE_SECRET
```

Your Telegram `.session` file represents an authenticated Telegram session.

**Treat it like a password.**

The repository should contain:

```gitignore
telebridge_config.json
*.session
*.session-journal

.venv/
venv/

__pycache__/
*.pyc
```

---

# 🛠 Troubleshooting

## Command stays `pending`

Make sure:

```text
bridge.py
```

is running.

---

## `Google bridge unavailable`

Check:

```text
Internet connection
Apps Script deployment
Web App permissions
Web App /exec URL
```

---

## `Bridge already configured`

Open Apps Script and run:

```text
resetTeleBridgeSecret
```

Then delete:

```text
telebridge_config.json
```

and start TeleBridge again.

---

## ChatGPT cannot create the spreadsheet

Make sure Google Drive is connected.

If ChatGPT cannot perform Google Drive write actions on your current account/configuration, follow the setup assistant's manual fallback.

---

## Telegram asks for login every launch

Make sure the Telegram:

```text
.session
```

file is not being deleted.

---

# ⚠️ Disclaimer

TeleBridge AI is an experimental open-source project.

It is **not affiliated with Telegram, Google or OpenAI**.

TeleBridge operates through your real Telegram account.

Do not use it for:

- spam
- harassment
- unsolicited bulk messaging
- account abuse
- bypassing Telegram restrictions

Follow Telegram's Terms of Service.

---

# 💸 Support TeleBridge AI

❤️ Support development:

```text
https://donatex.gg/donate/dimful1209
```

---

# ⭐ TeleBridge AI

### Your Telegram. Your machine. Your AI bridge.

```text
ChatGPT ↔ TeleBridge ↔ Telegram
```

**Open source · Local-first · Under your control**