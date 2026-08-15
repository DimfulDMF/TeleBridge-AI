# TeleBridge AI

Connect ChatGPT or another AI assistant to your personal Telegram account through a lightweight local bridge.

TeleBridge AI is an experimental proof-of-concept that lets an AI issue structured commands to a local Telegram client and receive results back. The local client uses your own Telegram session, while sensitive Telegram credentials and the `.session` file stay on your device.

## Architecture

```text
AI assistant
    ↓
Command transport
(for example Google Sheets + Apps Script)
    ↓
Local bridge
(iSH / Linux / Raspberry Pi)
    ↓
Telethon
    ↓
Personal Telegram account
```

Results travel back through the same transport.

## Features

- List Telegram dialogs
- Read recent text messages
- Search messages in one chat
- Search across dialogs
- Send messages
- Reply to a specific message
- Works with a personal Telegram account through Telethon
- Can run locally on iSH, Linux or Raspberry Pi
- Keeps Telegram `.session` local

## Repository files

- `bridge.py` — local Telegram bridge
- `apps_script.gs` — Google Apps Script transport endpoint
- `requirements.txt` — Python dependencies
- `.env.example` — example configuration
- `.gitignore` — prevents secrets/session files from being committed

## Setup

### 1. Create a Google Sheet

Create a sheet with these columns in row 1:

```text
id | command | target | text | status | result
```

### 2. Deploy Apps Script

Open **Extensions → Apps Script**, paste `apps_script.gs`, then replace:

```js
const SHEET_ID = "PASTE_YOUR_GOOGLE_SHEET_ID";
const BRIDGE_SECRET = "CHANGE_ME_TO_A_LONG_RANDOM_SECRET";
```

Deploy it as a **Web app** and copy the `/exec` URL.

### 3. Configure the local bridge

Install dependencies:

```bash
pip install -r requirements.txt
```

Set environment variables, for example:

```bash
export TELEGRAM_API_ID='12345678'
export TELEGRAM_API_HASH='your_api_hash'
export TELEBRIDGE_WEBAPP_URL='https://script.google.com/macros/s/.../exec'
export TELEBRIDGE_SECRET='your_long_random_secret'
```

Then run:

```bash
python3 bridge.py
```

On first Telegram login, Telethon may ask for your phone number, login code and 2FA password. The session is then stored locally and reused.

## Supported commands

The current transport expects these command names:

```text
chats
read
search
global_search
send
reply
```

Examples of spreadsheet rows:

```text
cmd-001 | chats         |          |                 | pending |
cmd-002 | read          | Tim      |                 | pending |
cmd-003 | search        | Tim      | minecraft       | pending |
cmd-004 | global_search |          | invoice         | pending |
cmd-005 | send          | @user    | happy birthday! | pending |
cmd-006 | reply         | Tim      | 12345|got it     | pending |
```

## Security

Never commit or publish:

- Telegram API hash
- phone number
- Telegram login code
- 2FA password
- `.session` files
- bridge secret
- private deployment configuration

Use a long random bridge secret and rotate it if it is ever exposed.

## Notes

This is an experimental MVP. The Google Sheets transport is intentionally simple and is useful for prototyping. A production version should use stronger authentication, idempotency, explicit user confirmation for write actions, proper rate limiting, encrypted secret storage, and a dedicated queue/API.

## Disclaimer

This project is not affiliated with Telegram or OpenAI. Use it responsibly and follow the terms of the services you connect.
