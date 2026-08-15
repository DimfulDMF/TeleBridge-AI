# 🌉 TeleBridge AI

> **Your Telegram. Your machine. Your AI bridge.**

**TeleBridge AI** is an open-source local bridge that lets ChatGPT work with your personal Telegram account.

Read conversations, search messages, generate context-aware replies, send messages and much more — while your Telegram session stays on **your own computer**.

> **Don't learn commands. Just talk to ChatGPT normally.**

---

## ✨ Features

- 💬 Read Telegram conversations
- 🔎 Search messages and chats
- 🌍 Search across Telegram dialogs
- ✉️ Send messages
- ↩️ Reply to messages
- 📋 List your chats
- 🧠 Use Telegram through natural-language requests
- 🎨 Make completely custom AI requests using your real conversations
- 🎂 Generate birthday messages based on the style of a chat
- ✍️ Create replies that match the tone of a conversation
- 📚 Summarize chats and catch up on missed messages
- 🔍 Find information hidden in old conversations
- 🤖 Combine multiple Telegram operations automatically
- 🪟 Windows support
- 🐧 Linux support
- 🥧 Raspberry Pi support
- 🔐 Local Telegram authentication
- 🔓 Open source
- 🧭 ChatGPT-guided installation

---

## 🧠 The Main Idea

TeleBridge is **not a fixed command interface**.

Commands like:

```text
read
search
send
reply
chats
global_search
```

are only used internally between ChatGPT and TeleBridge.

### You don't need to learn them.

Instead of writing something like:

```text
read | Alex | 50
```

just tell ChatGPT:

> Read my recent conversation with Alex and tell me what we were talking about.

You can make much more advanced requests too:

> Read my latest messages with Alex and write a birthday message for him in the same style we normally use.

> Look at my conversation with Alex and suggest a natural reply to his last message.

> Find where Tim sent me the Minecraft server IP.

> Read the last 50 messages with Alex and tell me if I forgot to answer anything important.

> Catch me up on everything important I missed in this chat.

ChatGPT decides which TeleBridge operations are needed.

For example:

```text
"Write Alex a birthday message in our usual style."

              ↓

Read recent conversation
              ↓
Understand context and style
              ↓
Generate an original message
              ↓
Show the message to you
              ↓
Send it if requested
```

**TeleBridge commands are tools — not limitations on what you can ask.**

---

## ⚙️ How It Works

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

ChatGPT creates internal commands in a Google Sheet.

Your local `bridge.py` receives those commands and performs the required Telegram operations.

The results are written back to the sheet, allowing ChatGPT to use your Telegram conversations as context for your request.

Your Telegram `.session` stays on **your computer**.

---

# 🚀 Installation

TeleBridge includes an interactive ChatGPT setup assistant.

Instead of configuring everything manually, ChatGPT guides you through the installation and performs supported setup actions automatically.

---

## 1. Download TeleBridge AI

Clone the repository:

```bash
git clone https://github.com/DimfulDMF/TeleBridge-AI.git
cd TeleBridge-AI
```

Or download the repository as a ZIP from GitHub.

### Project files

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

## 2. Start the Setup Assistant

Open:

```text
SETUP_PROMPT.txt
```

Copy **all** of its contents.

Open a new ChatGPT conversation and paste the prompt.

ChatGPT should first ask:

```text
| Choose your language before setup started |
| Выберите язык перед началом настройки |

🇷🇺 Русский
🇬🇧 English
```

Choose your language.

ChatGPT will guide you through the rest of the installation **one step at a time**.

---

## 3. Connect Google Drive

TeleBridge uses Google Sheets as the bridge between ChatGPT and your local computer.

The setup assistant will check whether Google Drive is connected.

If it isn't, ChatGPT will first attempt to initiate the Google Drive connection flow.

You may only need to approve the connection.

If automatic connection is unavailable, use:

```text
ChatGPT
→ Settings
→ Apps
→ Google Drive
→ Connect
```

Connect the Google account you want to use with TeleBridge.

---

## 4. Automatic Spreadsheet Setup

When Google Drive write access is available, ChatGPT automatically creates:

```text
TeleBridge AI
└── Commands
```

with the following columns:

| id | command | target | text | status | result |
|---|---|---|---|---|---|

You **do not need to create the columns manually**.

If Google Drive write access isn't available in your current ChatGPT configuration, the setup assistant will provide the minimum manual fallback.

---

## 5. Add Google Apps Script

Open the created:

```text
TeleBridge AI
```

spreadsheet.

Then open:

```text
Extensions
→ Apps Script
```

In the downloaded TeleBridge repository, open:

```text
COPY_TO_APPS_SCRIPT.txt
```

Then:

1. Copy **all** text from `COPY_TO_APPS_SCRIPT.txt`
2. Return to Google Apps Script
3. Delete the default code
4. Paste the TeleBridge code
5. Click **Save**

You do **not** need to modify the code.

---

## 6. Deploy Apps Script

Inside Apps Script open:

```text
Deploy
→ New deployment
→ Web app
```

Set:

```text
Execute as:
Me
```

Choose an access option that allows your local TeleBridge program to call the deployed Web App.

Click:

```text
Deploy
```

Google may ask you to authorize your own Apps Script project.

Complete the authorization.

After deployment, Google gives you a URL similar to:

```text
https://script.google.com/macros/s/XXXXXXXXXXXX/exec
```

Copy it.

> ⚠️ The TeleBridge Web App URL must end in `/exec`.

---

## 7. Get Telegram API Credentials

Open:

```text
https://my.telegram.org
```

Sign in with your Telegram account.

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

> 🔐 **Keep your API Hash private.**

Never send your:

- API Hash
- Telegram login code
- Telegram 2FA password
- Telegram session file

to ChatGPT.

These values are entered locally.

---

## 8. Install TeleBridge

### 🪟 Windows

Open PowerShell inside the TeleBridge directory:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python bridge.py
```

If PowerShell prevents environment activation, use Command Prompt:

```cmd
.venv\Scripts\activate.bat
pip install -r requirements.txt
python bridge.py
```

### 🐧 Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 bridge.py
```

### 🥧 Raspberry Pi

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

## 9. First Launch

On the first launch, `bridge.py` asks locally for:

```text
Telegram API ID:
Telegram API HASH:
Google Apps Script Web App URL:
```

Enter these values directly into your terminal.

TeleBridge automatically:

- 🔐 Generates a secure random `BRIDGE_SECRET`
- 🔗 Registers it with Google Apps Script
- 💾 Saves your configuration locally

Configuration is stored in:

```text
telebridge_config.json
```

You do **not** need to manually create or copy the bridge secret.

---

## 10. Telegram Login

Telethon may ask locally for:

```text
Phone number
Telegram login code
2FA password
```

Enter these only in your local terminal.

After successful authorization you should see:

```text
✅ Telegram authorized
✅ Google bridge connected
✅ Waiting for ChatGPT commands...
```

Keep `bridge.py` running while using TeleBridge.

---

## 11. Test TeleBridge

Return to the ChatGPT conversation containing the setup assistant.

Tell ChatGPT that `bridge.py` is running.

ChatGPT will create a safe test command:

```text
command = chats
status = pending
```

TeleBridge should process it:

```text
pending
   ↓
processing
   ↓
done
```

If ChatGPT receives your Telegram dialog list:

### 🎉 TeleBridge AI is connected!

---

# 💬 Using TeleBridge

After installation, **forget about the internal commands**.

Talk to ChatGPT normally.

---

## 💬 Simple Requests

> Show my Telegram chats.

> Read my latest messages with Alex.

> Find messages about Minecraft in my chat with Alex.

---

## 🧠 Context-Aware Requests

> Read my recent chat with Alex and summarize what we've been talking about.

> Catch me up on the last 100 messages with Alex.

> Read our conversation and tell me whether I forgot to answer any questions.

> Tell me what we agreed to do this weekend.

---

## ✍️ AI Writing Using Your Real Conversations

> Read my chat with Alex and write a birthday message in the way we normally talk.

> Look at our recent messages and suggest a natural response to his last message.

> Read our conversation and write a funny reply that fits the vibe.

> Write a short apology that sounds natural for this conversation.

ChatGPT can use the actual conversation as context instead of generating a generic response.

---

## 🔎 Finding Information

> Find where Tim sent me the Minecraft server IP.

> Find what time Alex said we were meeting.

> Search our messages and tell me what game he recommended.

> Find the message where he sent me that website.

---

## 🤖 Multi-Step Requests

You can make requests involving multiple actions.

For example:

> Read my recent messages with Alex, understand how we normally talk, write him a birthday message in our style, and show it to me before sending.

ChatGPT can internally perform:

```text
Read conversation
       ↓
Analyze context
       ↓
Understand communication style
       ↓
Write message
       ↓
Show draft
       ↓
Send after your request
```

Another example:

> Find what Alex said about our Minecraft server and check whether he mentioned when he'll be online.

ChatGPT can internally:

```text
Search
  ↓
Read surrounding messages
  ↓
Search additional context
  ↓
Analyze
  ↓
Answer
```

### You are not limited to the examples in this README.

If ChatGPT understands your request and the necessary Telegram information or action is available through TeleBridge, **just ask naturally**.

---

# 🛠 Internal Commands

> **These commands are for ChatGPT and TeleBridge. You normally don't need to use them yourself.**

| Command | Description |
|---|---|
| `chats` | List Telegram dialogs |
| `read` | Read recent messages |
| `search` | Search messages inside one chat |
| `global_search` | Search across dialogs |
| `send` | Send a Telegram message |
| `reply` | Reply to a Telegram message |

The Google Sheet uses:

```text
id | command | target | text | status | result
```

Example:

```text
abc123 | send | @username | Hello! | pending |
```

Status flow:

```text
pending
   ↓
processing
   ↓
done
```

If execution fails:

```text
error
```

Again:

> **These commands are implementation details — not the way you have to talk to ChatGPT.**

---

# 🔁 Future Launches

After the initial setup, simply start TeleBridge.

### Windows

```powershell
python bridge.py
```

### Linux / Raspberry Pi

```bash
python3 bridge.py
```

Your configuration is remembered locally.

---

# 🔄 Pair a New Computer

Automatic secret registration is intentionally one-time.

To pair another installation:

1. Open Apps Script
2. Run `resetTeleBridgeSecret`
3. Delete local `telebridge_config.json`
4. Start `bridge.py` again

TeleBridge generates and registers a new secret automatically.

---

# 🔐 Security

Never publish or send:

```text
telebridge_config.json
*.session
*.session-journal

Telegram API Hash
Telegram login codes
Telegram 2FA password
BRIDGE_SECRET
```

Your Telegram `.session` represents an authenticated Telegram session.

> **Treat it like a password.**

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

---

# 🛠 Troubleshooting

### Command stays `pending`

Make sure `bridge.py` is running.

### `Google bridge unavailable`

Check:

- Internet connection
- Apps Script deployment
- Web App access settings
- Correct `/exec` URL

### `Bridge already configured`

Open Apps Script and run:

```text
resetTeleBridgeSecret
```

Delete:

```text
telebridge_config.json
```

Then start TeleBridge again.

### ChatGPT cannot create the spreadsheet

Make sure Google Drive is connected.

If ChatGPT doesn't currently have permission to create/edit Google Sheets, follow the setup assistant's manual fallback.

### Telegram asks for login every launch

Make sure your `.session` file is not being deleted.

---

# ⚠️ Disclaimer

TeleBridge AI is an experimental open-source project.

It is **not affiliated with Telegram, Google, or OpenAI**.

TeleBridge operates through your real Telegram account.

Do not use it for:

- Spam
- Harassment
- Unsolicited bulk messaging
- Account abuse
- Bypassing Telegram restrictions

Follow Telegram's Terms of Service.

---

# 💸 Support TeleBridge AI

If you like TeleBridge AI, you can support development:

**❤️ https://donatex.gg/donate/dimful1209**

---

# ⭐ TeleBridge AI

### Your Telegram. Your machine. Your AI bridge.

```text
You
 ↕
ChatGPT
 ↕
TeleBridge
 ↕
Telegram
```

**Open source · Local-first · Natural language · Under your control**