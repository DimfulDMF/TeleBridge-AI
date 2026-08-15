# 🌉 TeleBridge AI

> Connect an AI assistant to your personal Telegram account — locally, securely, and under your control.

**TeleBridge AI** is an experimental open-source bridge that allows an AI assistant to interact with your personal Telegram account through a locally running client.

Instead of using a Telegram bot account, TeleBridge AI uses a Telegram **user session** through [Telethon](https://github.com/LonamiWebs/Telethon), allowing the bridge to work with chats that are already available to your Telegram account.

The bridge can:

- 💬 List your Telegram chats
- 📖 Read recent messages
- 🔎 Search message history
- ✉️ Send messages
- ↩️ Reply to messages
- 🖥️ Run locally on Windows or Linux
- 🔐 Keep your Telegram session on your own machine
- 🤖 Act as a gateway between Telegram and an AI assistant

---

## ⚠️ Project Status

TeleBridge AI is currently an **experimental proof of concept / MVP**.

It is intended for development, experimentation, and personal automation.

The project is **not affiliated with Telegram or OpenAI**.

You are responsible for using it in accordance with Telegram's Terms of Service and applicable platform policies.

---

# 🧠 How It Works

TeleBridge AI separates the AI assistant from your Telegram credentials.

The AI does **not** need direct access to your Telegram `.session` file.

Instead, commands travel through a small command transport layer.

```text
┌──────────────────────┐
│     AI Assistant     │
│      / ChatGPT       │
└──────────┬───────────┘
           │
           │ commands
           ▼
┌──────────────────────┐
│   Command Transport  │
│                      │
│ Google Apps Script   │
│ + Google Sheets      │
└──────────┬───────────┘
           │
           │ polling
           ▼
┌──────────────────────┐
│    TeleBridge AI     │
│      bridge.py       │
│                      │
│ Windows / Linux      │
└──────────┬───────────┘
           │
           │ Telethon
           ▼
┌──────────────────────┐
│       Telegram       │
│   Personal Account   │
└──────────────────────┘
```

Responses travel back through the same path:

```text
Telegram
   ↓
bridge.py
   ↓
Command Transport
   ↓
AI Assistant
```

This design means the machine running TeleBridge AI remains the component that actually authenticates with Telegram and performs Telegram operations.

---

# ✨ Features

### Telegram

TeleBridge AI currently supports operations such as:

```text
chats
read
search
send
reply
```

Examples:

```text
chats
```

Returns available Telegram dialogs.

```text
read | John
```

Returns recent text messages from a chat.

```text
search | John | birthday
```

Searches messages in a conversation.

```text
send | @username | Happy birthday! 🎉
```

Sends a message.

```text
reply | @username | MESSAGE_ID | Sounds good!
```

Replies to a specific message.

---

# 🔐 Security Model

TeleBridge AI was designed so that Telegram authentication remains local.

Your:

- Telegram login code
- Telegram 2FA password
- `.session` file
- API hash
- bridge secret

should **never be committed to GitHub**.

The Telegram session is stored on the computer running `bridge.py`.

```text
AI Assistant
      │
      │ command
      ▼
Bridge transport
      │
      ▼
YOUR COMPUTER
┌─────────────────────┐
│ Telegram .session   │
│ Telegram API keys   │
│ bridge.py           │
└─────────────────────┘
      │
      ▼
Telegram
```

## Never publish

Do not commit files such as:

```text
.env
*.session
*.session-journal
```

Never hard-code real credentials into a public repository.

---

# 📋 Requirements

You will need:

- Windows 10/11 **or** a modern Linux distribution
- Python 3.9+
- A Telegram account
- Telegram API ID
- Telegram API Hash
- A Google account
- Google Sheets
- Google Apps Script

Recommended:

- Python 3.11+
- Git
- A machine that can remain running while the bridge is needed

---

# 1️⃣ Clone TeleBridge AI

## Windows

Open **PowerShell**:

```powershell
git clone https://github.com/DimfulDMF/TeleBridge-AI.git
cd TeleBridge-AI
```

If Git is not installed, you can download the repository as a ZIP from GitHub and extract it.

---

## Linux

Open a terminal:

```bash
git clone https://github.com/DimfulDMF/TeleBridge-AI.git
cd TeleBridge-AI
```

---

# 2️⃣ Create a Python Virtual Environment

Using a virtual environment is strongly recommended.

## Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can alternatively use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

---

## Linux

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

---

# 3️⃣ Install Dependencies

With the virtual environment activated:

## Windows

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Linux

```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

The main dependencies are:

```text
telethon
requests
```

---

# 4️⃣ Get Telegram API Credentials

TeleBridge AI uses Telegram's client API through Telethon.

Open:

**https://my.telegram.org**

Sign in with your Telegram account.

Then:

1. Open **API development tools**
2. Create an application
3. Copy your **API ID**
4. Copy your **API Hash**

You should receive values similar to:

```text
API_ID=12345678
API_HASH=0123456789abcdef0123456789abcdef
```

⚠️ These values are private.

Do not publish your real API Hash.

---

# 5️⃣ Create the Command Queue

Create a new Google Spreadsheet.

Create a sheet named:

```text
Commands
```

The first row must contain:

| id | command | target | text | status | result |
|---|---|---|---|---|---|

For example:

```text
id | command | target | text | status | result
```

Commands waiting for the local bridge use:

```text
status = pending
```

When the bridge picks up a command, it becomes:

```text
processing
```

After execution:

```text
done
```

or:

```text
error
```

---

# 6️⃣ Install the Google Apps Script Bridge

Inside your Google Sheet:

```text
Extensions
→ Apps Script
```

Delete the default example code.

Copy the contents of:

```text
apps_script.gs
```

from this repository into the Apps Script editor.

---

# 7️⃣ Create a Bridge Secret

The bridge endpoint must not be left completely unprotected.

Generate a long random secret.

Example format:

```text
3f41a842c18e4e0c9a4c63e02e27d2e94d2b93a4
```

Do **not** use this example.

Generate your own value.

Set it in your Apps Script configuration according to the instructions in `apps_script.gs`.

The same secret must later be configured on the computer running TeleBridge AI.

---

# 8️⃣ Deploy Google Apps Script

In Apps Script:

```text
Deploy
→ New deployment
```

Select:

```text
Web app
```

Configure the deployment so the bridge can access the endpoint.

Deploy it.

Google will give you a URL similar to:

```text
https://script.google.com/macros/s/DEPLOYMENT_ID/exec
```

Save this URL.

This is your:

```text
BRIDGE_URL
```

---

# 9️⃣ Configure TeleBridge AI

Create your environment configuration.

Copy:

```text
.env.example
```

to:

```text
.env
```

Then configure your values.

Example:

```env
TG_API_ID=12345678
TG_API_HASH=YOUR_TELEGRAM_API_HASH

BRIDGE_URL=https://script.google.com/macros/s/YOUR_DEPLOYMENT_ID/exec
BRIDGE_SECRET=YOUR_RANDOM_BRIDGE_SECRET
```

Replace every example value with your own.

Never commit `.env`.

---

# 🔟 Start TeleBridge AI

## Windows

With the virtual environment active:

```powershell
python bridge.py
```

---

## Linux

```bash
python3 bridge.py
```

On first launch, Telethon may ask:

```text
Please enter your phone (or bot token):
```

Enter your Telegram phone number.

Example:

```text
+12345678900
```

Telegram will send you a login code.

Enter it when requested.

If your account uses Telegram 2FA, Telethon will also ask:

```text
Please enter your password:
```

Enter your Telegram 2FA password.

After successful authentication you should see something similar to:

```text
Telegram authorized

Name: Example
Username: @example
ID: 123456789
```

Telethon will create a local session file.

For example:

```text
telegram.session
```

From that point, you normally won't need to enter the Telegram login code every time.

---

# ✅ Bridge Connection

After Telegram authentication, TeleBridge AI tests the command transport.

A successful connection should look similar to:

```text
Telegram authorized
Bridge connected

Waiting for commands...
```

The bridge will periodically request pending commands from the Apps Script endpoint.

---

# 📨 Command Lifecycle

Suppose the AI wants to send:

```text
Hello!
```

to:

```text
@example
```

A command is created:

```text
ID:
cmd-001

COMMAND:
send

TARGET:
@example

TEXT:
Hello!

STATUS:
pending
```

The local bridge sees it:

```text
▶ send | @example | Hello!
```

TeleBridge executes the command through Telethon.

The row is then updated:

```text
STATUS:
done
```

and a result is returned.

---

# 🔎 Reading Messages

A read command might look like:

```text
command = read
target = John
```

The local client resolves the dialog and reads recent messages.

Example result:

```text
[10521] John: Hey
[10522] You: What's up?
[10523] John: Are you free tonight?
```

Media-only messages may be omitted depending on the bridge configuration.

---

# 🔍 Searching Telegram

Search can be performed inside Telegram dialogs.

Example:

```text
command = search
target = John
text = minecraft
```

Possible result:

```text
[9281] John: wanna play minecraft?
[10332] You: minecraft server is online
```

---

# ✉️ Sending Messages

Example:

```text
command = send
target = @example
text = Happy birthday! 🎉
```

The message is sent from **your Telegram account**, not from a Telegram bot.

⚠️ This means commands with write access should be treated carefully.

---

# ↩️ Replies

A reply operation can reference an existing Telegram message ID.

Example:

```text
command = reply
target = @example
text = 10523|Sure, let's go!
```

The exact wire format depends on the version of `bridge.py`.

---

# 🪟 Running Automatically on Windows

If you want TeleBridge AI to start automatically, you can use **Task Scheduler**.

Open:

```text
Task Scheduler
```

Choose:

```text
Create Task
```

Configure a trigger such as:

```text
At log on
```

For the program, select the Python executable inside your virtual environment:

```text
C:\path\to\TeleBridge-AI\.venv\Scripts\python.exe
```

Arguments:

```text
bridge.py
```

Start in:

```text
C:\path\to\TeleBridge-AI
```

After login, Windows can automatically start the bridge.

---

# 🐧 Running as a Linux Service

For an always-on Linux machine, `systemd` is recommended.

Create:

```bash
sudo nano /etc/systemd/system/telebridge.service
```

Example configuration:

```ini
[Unit]
Description=TeleBridge AI
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=YOUR_USER
WorkingDirectory=/home/YOUR_USER/TeleBridge-AI
ExecStart=/home/YOUR_USER/TeleBridge-AI/.venv/bin/python bridge.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Replace:

```text
YOUR_USER
```

with your Linux username.

Then run:

```bash
sudo systemctl daemon-reload
sudo systemctl enable telebridge
sudo systemctl start telebridge
```

Check status:

```bash
sudo systemctl status telebridge
```

View logs:

```bash
journalctl -u telebridge -f
```

---

# 🥧 Raspberry Pi

TeleBridge AI can also run on a Raspberry Pi running Raspberry Pi OS or another Linux distribution.

Installation is essentially identical to Linux:

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

A Raspberry Pi can be useful as an always-on local Telegram gateway.

---

# 🧰 Troubleshooting

## `ModuleNotFoundError: telethon`

Install dependencies:

```bash
pip install -r requirements.txt
```

or:

```bash
pip install telethon requests
```

---

## Telegram asks for a login code every time

Make sure the `.session` file is not being deleted.

The session file should remain in the working directory unless another session path has been configured.

---

## Apps Script returns Unauthorized

Check:

```text
BRIDGE_SECRET
```

The value configured locally must exactly match the value configured for the Apps Script bridge.

---

## Bridge cannot connect

Verify the Apps Script deployment URL.

It should normally end with:

```text
/exec
```

Also verify that the deployment is accessible using the account/access configuration you selected.

---

## Commands remain `pending`

Check whether `bridge.py` is currently running.

You should see:

```text
Waiting for commands...
```

Also check:

- internet connection
- Apps Script URL
- bridge secret
- spreadsheet structure
- Apps Script deployment

---

## Commands remain `processing`

This usually means the bridge received the command but did not successfully return the result.

Check the local bridge console for errors.

---

## Telegram connection fails

Verify:

```text
TG_API_ID
TG_API_HASH
```

Also make sure Telegram's API is reachable from your network.

---

# 🛡️ Security Recommendations

If you intend to use TeleBridge AI beyond experimentation:

### 1. Protect the bridge secret

Use a cryptographically random value.

Do not use:

```text
password
123456
telebridge
secret
```

---

### 2. Never upload Telegram sessions

Add this to `.gitignore`:

```gitignore
*.session
*.session-journal
```

A Telegram session can provide access to your account.

Treat it like a credential.

---

### 3. Never expose your API hash

Keep it inside local configuration.

---

### 4. Restrict write commands

Operations such as:

```text
send
reply
```

perform real actions from your Telegram account.

For production use, consider implementing confirmation before executing write operations.

For example:

```text
AI requests SEND
       ↓
Pending confirmation
       ↓
User approves
       ↓
Telegram message sent
```

---

### 5. Add replay protection

Each command should have a unique ID.

The local bridge should avoid executing the same command twice.

---

### 6. Consider command expiration

Old commands should not execute unexpectedly after a machine reconnects.

A production implementation should include timestamps and expiration.

---

# 🗺️ Roadmap

Possible future improvements:

- [ ] Better authentication
- [ ] Encrypted command payloads
- [ ] Command expiration
- [ ] User confirmation for write actions
- [ ] Message pagination
- [ ] Media support
- [ ] File downloads
- [ ] Voice message transcription
- [ ] Telegram message links
- [ ] Multiple Telegram accounts
- [ ] Multiple AI clients
- [ ] Web dashboard
- [ ] Docker support
- [ ] Native REST gateway
- [ ] WebSocket transport
- [ ] Replace Google Sheets with a dedicated message queue
- [ ] Plugin/tool API for AI assistants
- [ ] Discord adapter
- [ ] WhatsApp adapter
- [ ] Signal adapter

---

# 🧩 Why a Local Bridge?

Giving a remote AI service a Telegram session would be a significant security risk.

TeleBridge AI takes another approach:

```text
Remote AI
   │
   │ restricted commands
   ▼
Transport
   │
   ▼
Local trusted process
   │
   │ Telegram credentials stay here
   ▼
Telegram
```

This creates a separation between:

**Reasoning / AI**

and:

**Authentication / execution**

The AI can request an operation while the trusted local process remains responsible for actually interacting with Telegram.

---

# 💡 Example Use Cases

TeleBridge AI can be used experimentally for:

- summarizing conversations
- finding old messages
- drafting replies
- sending approved messages
- searching personal Telegram history
- personal AI assistants
- local automation
- message organization
- notification workflows

---

# ⚖️ Responsible Use

TeleBridge AI operates through a personal Telegram account.

Do not use it for:

- spam
- unsolicited bulk messaging
- harassment
- account abuse
- bypassing Telegram restrictions
- automated behavior that violates Telegram's Terms of Service

Telegram may limit or ban accounts that abuse its API.

Use conservative rate limits and keep a human in control of important actions.

---

# 📁 Repository Structure

```text
TeleBridge-AI/
│
├── bridge.py
│   └── Local Telegram client and command executor
│
├── apps_script.gs
│   └── Google Apps Script transport endpoint
│
├── requirements.txt
│   └── Python dependencies
│
├── .env.example
│   └── Example configuration
│
├── .gitignore
│   └── Prevents credentials/session files from being committed
│
└── README.md
    └── Documentation
```

---

# 🤝 Contributing

Contributions, experiments, bug reports, and improvements are welcome.

If you find a bug, open an Issue.

For larger changes:

```bash
git checkout -b feature/my-feature
```

Make your changes and submit a Pull Request.

Please never include real Telegram credentials or session files in issues, commits, screenshots, or pull requests.

---

# 📜 License

A license has not yet been selected.

Before accepting external contributions or distributing the project widely, consider adding an open-source license such as MIT, Apache-2.0, or GPL-3.0.

---

# ⭐ TeleBridge AI

**Your Telegram. Your machine. Your AI bridge.**

```text
AI ↔ Local Bridge ↔ Telegram
```

If you find the project interesting, consider giving the repository a ⭐.

💸Donate - https://donatex.gg/donate/dimful1209