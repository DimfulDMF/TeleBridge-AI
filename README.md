# 🌉 TeleBridge AI

> Connect ChatGPT to your personal Telegram account through a local open-source bridge.

**TeleBridge AI** lets ChatGPT interact with your personal Telegram account while your Telegram session stays on your own computer.

It can:

- 💬 Read recent Telegram messages
- 🔎 Search message history
- ✉️ Send messages
- ↩️ Reply to messages
- 📋 List your chats
- 🖥️ Run on Windows, Linux and Raspberry Pi
- 🔐 Keep your Telegram session local
- 🔓 Work as an open-source bridge between ChatGPT and Telegram

---

# 🧠 How it works

TeleBridge does **not** give ChatGPT your Telegram session directly.

Instead, it uses Google Sheets as a command queue.

```text
You
 ↓
ChatGPT
 ↓
Google Sheets
 ↓
Google Apps Script
 ↓
bridge.py on your computer
 ↓
Telethon
 ↓
Telegram
```

When ChatGPT wants to perform an action, it creates a command in the Google Sheet.

Example:

```text
send | @username | Hello! | pending
```

Your local `bridge.py` sees the command, executes it through Telegram, and writes the result back.

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
- ChatGPT with Google Drive access

---

# 🚀 Step 1 — Download TeleBridge AI

Clone the repository:

```bash
git clone https://github.com/DimfulDMF/TeleBridge-AI.git
cd TeleBridge-AI
```

Or download the repository as a ZIP from GitHub.

---

# 🐍 Step 2 — Install Python dependencies

## Windows

Open PowerShell inside the project folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

---

## Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

# 🔑 Step 3 — Get Telegram API ID and API Hash

Open:

**https://my.telegram.org**

Log in with your Telegram account.

Then open:

```text
API development tools
```

Create an application.

Telegram will give you:

```text
API ID
API Hash
```

Example:

```text
API ID: 12345678
API Hash: 0123456789abcdef0123456789abcdef
```

⚠️ Keep your API Hash private.

---

# ☁️ Step 4 — Create the Google Sheet

This is the part that connects ChatGPT with your local bridge.

Open Google Sheets and create a new spreadsheet.

Name it:

```text
TeleBridge AI
```

Inside the spreadsheet, create a sheet named:

```text
Commands
```

The first row must contain exactly:

| id | command | target | text | status | result |
|---|---|---|---|---|---|

So the sheet should look like this:

```text
A          B          C          D          E          F
id         command    target     text       status     result
```

Do not rename these columns.

---

# 🔗 Step 5 — Add Google Apps Script

Open the same Google Sheet.

Go to:

```text
Extensions
→ Apps Script
```

A new Apps Script editor will open.

Delete all default code.

Open the file:

```text
apps_script.gs
```

from this repository.

Copy the entire contents and paste them into the Apps Script editor.

Then click:

```text
Save
```

---

# 🌐 Step 6 — Deploy Apps Script as a Web App

Inside Apps Script, click:

```text
Deploy
→ New deployment
```

Click the gear icon and choose:

```text
Web app
```

Use:

```text
Execute as:
Me
```

For access, choose the option that allows the Web App to be accessed by your bridge.

Then click:

```text
Deploy
```

Google may ask you to authorize the script.

Approve the permissions.

After deployment, Google gives you a URL similar to:

```text
https://script.google.com/macros/s/XXXXXXXXXXXX/exec
```

Copy this URL.

You will need it in `bridge.py`.

---

# 🔐 Step 7 — First launch and automatic bridge setup

Start TeleBridge.

## Windows

```powershell
python bridge.py
```

## Linux

```bash
python3 bridge.py
```

On the first launch, TeleBridge asks for:

```text
Telegram API ID
Telegram API HASH
Google Apps Script Web App URL
```

Example:

```text
Telegram API ID: 12345678
Telegram API HASH:
Google Apps Script Web App URL: https://script.google.com/macros/s/XXXXX/exec
```

TeleBridge then automatically:

1. generates a secure random bridge secret;
2. sends the secret to your Apps Script;
3. stores the secret in Apps Script;
4. saves your local configuration in:

```text
telebridge_config.json
```

You do **not** need to manually create or paste the bridge secret.

After that, your Telegram login starts.

---

# 📱 Step 8 — Log in to Telegram

Telethon may ask:

```text
Please enter your phone:
```

Enter your Telegram phone number.

Example:

```text
+12345678900
```

Telegram sends you a login code.

Enter the code.

If your account uses Telegram 2FA, Telethon asks:

```text
Please enter your password:
```

Enter your Telegram 2FA password.

After successful login you should see something like:

```text
✅ Telegram authorized
✅ Google bridge connected
✅ Waiting for AI commands...
```

Telethon also creates a local `.session` file.

That file keeps your Telegram login active.

---

# 🤖 Step 9 — Connect Google Drive to ChatGPT

Now ChatGPT must be able to access the Google Sheet.

Open ChatGPT.

Go to:

```text
Settings
→ Apps
→ Google Drive
→ Connect
```

Sign in with the **same Google account** where you created the `TeleBridge AI` spreadsheet.

Allow ChatGPT to access your Google Drive.

After that, ChatGPT should be able to see and edit the spreadsheet.

---

# 🧩 Step 10 — Tell ChatGPT how TeleBridge works

Start a new ChatGPT conversation.

Send this prompt:

```text
Use my Google Sheet named "TeleBridge AI" as my Telegram bridge.

The sheet named "Commands" contains:

id | command | target | text | status | result

To execute a Telegram action:

1. Create a new row.
2. Generate a unique id.
3. Put the command in the "command" column.
4. Put the chat name, username or Telegram ID in "target".
5. Put message text or search text in "text".
6. Set status to "pending".
7. Wait for bridge.py to process the command.
8. Read the "result" column after status changes to "done" or "error".

Supported commands:

chats
read
search
global_search
send
reply
```

After that, you can talk normally.

For example:

```text
Show my Telegram chats.
```

```text
Read my latest messages with Alex.
```

```text
Search my chat with Alex for "Minecraft".
```

```text
Send @username: Happy birthday! 🎉
```

---

# 💬 Supported commands

## `chats`

Lists Telegram dialogs.

Example row:

```text
id: cmd-001
command: chats
target:
text:
status: pending
```

---

## `read`

Reads recent messages from a chat.

Example:

```text
id: cmd-002
command: read
target: Alex
text:
status: pending
```

---

## `search`

Searches messages inside one chat.

Example:

```text
id: cmd-003
command: search
target: Alex
text: Minecraft
status: pending
```

---

## `global_search`

Searches across multiple Telegram dialogs.

Example:

```text
id: cmd-004
command: global_search
target:
text: birthday
status: pending
```

---

## `send`

Sends a Telegram message from your account.

Example:

```text
id: cmd-005
command: send
target: @username
text: Hello!
status: pending
```

---

## `reply`

Replies to a specific Telegram message.

Format:

```text
target = chat
text = MESSAGE_ID|reply text
```

Example:

```text
id: cmd-006
command: reply
target: Alex
text: 12345|Sounds good!
status: pending
```

---

# 🔄 Command status

TeleBridge uses these statuses:

```text
pending
```

The command is waiting.

```text
processing
```

The local bridge has received it.

```text
done
```

The command finished successfully.

```text
error
```

The command failed.

---

# 🔁 Running TeleBridge again

After first setup, TeleBridge remembers:

```text
Telegram API ID
Telegram API Hash
Apps Script URL
Bridge Secret
```

in:

```text
telebridge_config.json
```

So the next launch is simply:

```bash
python bridge.py
```

You do not need to enter the setup information again.

---

# 🔄 Pairing a new computer

The Apps Script allows automatic bridge setup only once.

If you want to connect a new computer:

1. Open Apps Script.
2. Run:

```javascript
resetTeleBridgeSecret()
```

3. Delete:

```text
telebridge_config.json
```

on the old/new local installation.

4. Run:

```bash
python bridge.py
```

again.

A new secret will be generated automatically.

---

# 🔐 Security

Your Telegram login happens locally.

ChatGPT does **not** receive:

```text
Telegram login code
Telegram 2FA password
Telegram .session file
Telegram API Hash
```

However, your local files are sensitive.

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

Treat your Telegram `.session` file like a password.

---

# 🖥 Supported platforms

TeleBridge AI is designed for:

- 🪟 Windows
- 🐧 Linux
- 🥧 Raspberry Pi / Linux ARM

---

# 🥧 Raspberry Pi

On Raspberry Pi OS:

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

# 🛠 Troubleshooting

## `ModuleNotFoundError: telethon`

Run:

```bash
pip install -r requirements.txt
```

---

## Google bridge says `Unauthorized`

Most likely the bridge secret is different.

Run:

```javascript
resetTeleBridgeSecret()
```

in Apps Script.

Then delete:

```text
telebridge_config.json
```

and start `bridge.py` again.

---

## `Bridge already configured`

Apps Script already has a secret stored.

Run:

```javascript
resetTeleBridgeSecret()
```

Then start TeleBridge again.

---

## Commands stay `pending`

Check that:

```text
bridge.py
```

is running.

Also check:

- internet connection
- Apps Script Web App URL
- Google deployment permissions
- correct Google Sheet
- correct `Commands` sheet name

---

## Commands stay `processing`

The bridge received the command but probably failed during execution.

Check the terminal running `bridge.py`.

---

## ChatGPT cannot see the Google Sheet

Make sure:

- Google Drive is connected in ChatGPT;
- you connected the correct Google account;
- the spreadsheet is named `TeleBridge AI`;
- ChatGPT has permission to access it.

---

## ChatGPT can read but cannot write to the sheet

Google Drive app permissions can vary by ChatGPT account, plan, region, or current product configuration.

If write access is unavailable, the current Google Sheets bridge cannot create commands directly.

---

# 📁 Project structure

```text
TeleBridge-AI/
├── bridge.py
├── apps_script.gs
├── requirements.txt
├── .gitignore
└── README.md
```

Local files created after setup:

```text
telebridge_config.json
my_account.session
```

These should **not** be uploaded to GitHub.

---

# ⚠️ Disclaimer

TeleBridge AI is an experimental open-source project.

It is **not affiliated with Telegram or OpenAI**.

Messages sent through TeleBridge are sent from your real Telegram account.

Do not use it for:

- spam
- unsolicited bulk messaging
- harassment
- account abuse
- bypassing Telegram restrictions

Follow Telegram's Terms of Service.

---

# 💸 Support the Project

If you like TeleBridge AI and want to support development:

**❤️ https://donatex.gg/donate/dimful1209**

---

# ⭐ TeleBridge AI

### Your Telegram. Your machine. Your AI bridge.

```text
AI ↔ Local Bridge ↔ Telegram
```

**Open source · Local-first · Under your control**