import asyncio
import json
import os
import secrets
from getpass import getpass
from pathlib import Path

import requests
from telethon import TelegramClient


CONFIG_FILE = Path(__file__).with_name("telebridge_config.json")
DEFAULT_SESSION = "my_account"
DEFAULT_POLL_INTERVAL = 3


def save_config(config):
    CONFIG_FILE.write_text(
        json.dumps(config, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    try:
        os.chmod(CONFIG_FILE, 0o600)
    except Exception:
        pass


def load_config():
    if not CONFIG_FILE.exists():
        return None

    try:
        data = json.loads(
            CONFIG_FILE.read_text(encoding="utf-8")
        )
    except Exception:
        return None

    required = (
        "telegram_api_id",
        "telegram_api_hash",
        "webapp_url",
        "bridge_secret",
    )

    return data if all(data.get(k) for k in required) else None


def first_setup():
    print()
    print("==============================")
    print("      TeleBridge AI Setup")
    print("==============================")
    print()

    while True:
        raw = input("Telegram API ID: ").strip()

        if raw.isdigit():
            api_id = int(raw)
            break

        print("[ERROR] API ID must be a number")

    while True:
        api_hash = getpass("Telegram API HASH: ").strip()

        if api_hash:
            break

        print("[ERROR] API HASH cannot be empty")

    while True:
        webapp_url = input(
            "Google Apps Script Web App URL: "
        ).strip()

        if (
            webapp_url.startswith("https://script.google.com/")
            and "/exec" in webapp_url
        ):
            break

        print("[ERROR] Invalid Apps Script Web App URL")

    bridge_secret = secrets.token_urlsafe(48)

    print()
    print("[OK] Generated secure bridge secret")
    print("[INFO] Pairing with Google Apps Script...")

    try:
        r = requests.post(
            webapp_url,
            json={
                "action": "setup",
                "secret": bridge_secret,
            },
            timeout=30,
        )

        r.raise_for_status()
        data = r.json()

    except Exception as exc:
        raise SystemExit(
            f"[ERROR] Automatic bridge setup failed: {exc}"
        )

    if not data.get("ok"):
        raise SystemExit(
            "[ERROR] Apps Script rejected setup: "
            + str(data.get("error") or data)
        )

    config = {
        "telegram_api_id": api_id,
        "telegram_api_hash": api_hash,
        "webapp_url": webapp_url,
        "bridge_secret": bridge_secret,
        "session_name": DEFAULT_SESSION,
        "poll_interval": DEFAULT_POLL_INTERVAL,
    }

    save_config(config)

    print("[OK] Bridge secret paired automatically")
    print(
        f"[OK] Configuration saved to {CONFIG_FILE.name}"
    )
    print()

    return config


def get_config():
    return load_config() or first_setup()


def bridge_get(url, secret):
    try:
        r = requests.get(
            url,
            params={
                "action": "pending",
                "secret": secret,
            },
            timeout=30,
        )

        r.raise_for_status()

        return r.json()

    except Exception as exc:
        print(
            "[ERROR] Bridge GET:",
            type(exc).__name__,
            exc,
        )

        return None


def bridge_result(
    url,
    secret,
    command_id,
    ok,
    result,
):
    try:
        r = requests.post(
            url,
            json={
                "action": "result",
                "secret": secret,
                "id": command_id,
                "ok": bool(ok),
                "result": str(result),
            },
            timeout=30,
        )

        r.raise_for_status()

        return r.json()

    except Exception as exc:
        print(
            "[ERROR] Bridge POST:",
            type(exc).__name__,
            exc,
        )

        return None


async def resolve_target(client, target):
    target = target.strip()

    if not target:
        raise ValueError("Target is empty")

    if target.lstrip("-").isdigit():
        return await client.get_entity(
            int(target)
        )

    try:
        return await client.get_entity(target)

    except Exception:
        pass

    target_lower = target.lower()

    async for dialog in client.iter_dialogs():
        dialog_name = (
            dialog.name or ""
        ).strip().lower()

        if dialog_name == target_lower:
            return dialog.entity

    async for dialog in client.iter_dialogs():
        dialog_name = (
            dialog.name or ""
        ).strip().lower()

        if target_lower in dialog_name:
            return dialog.entity

    raise ValueError(
        f"Chat not found: {target}"
    )


async def sender_name(msg):
    try:
        sender = await msg.get_sender()

        if sender:
            return (
                getattr(
                    sender,
                    "first_name",
                    None,
                )
                or getattr(
                    sender,
                    "title",
                    None,
                )
                or getattr(
                    sender,
                    "username",
                    None,
                )
                or str(
                    getattr(
                        sender,
                        "id",
                        "?",
                    )
                )
            )

    except Exception:
        pass

    return "?"


async def cmd_chats(client):
    out = []

    async for dialog in client.iter_dialogs(
        limit=100
    ):
        username = getattr(
            dialog.entity,
            "username",
            None,
        )

        line = (
            f"{dialog.id} | {dialog.name}"
        )

        if username:
            line += f" | @{username}"

        out.append(line)

    return "\n".join(out)


async def cmd_read(
    client,
    target,
    limit=40,
):
    entity = await resolve_target(
        client,
        target,
    )

    out = []

    async for msg in client.iter_messages(
        entity,
        limit=limit,
    ):
        if not msg.message:
            continue

        name = await sender_name(msg)

        text = (
            msg.message
            .replace("\n", " ")
            .strip()
        )

        out.append(
            f"[{msg.id}] {name}: {text}"
        )

    out.reverse()

    if not out:
        return "No text messages."

    return "\n".join(out)


async def cmd_search(
    client,
    target,
    query,
):
    query = query.strip()

    if not query:
        raise ValueError("Empty query")

    entity = await resolve_target(
        client,
        target,
    )

    out = []

    async for msg in client.iter_messages(
        entity,
        search=query,
        limit=100,
    ):
        if not msg.message:
            continue

        name = await sender_name(msg)

        text = (
            msg.message
            .replace("\n", " ")
            .strip()
        )

        out.append(
            f"[{msg.id}] {name}: {text}"
        )

    out.reverse()

    if not out:
        return "Nothing found."

    return "\n".join(out)


async def cmd_global_search(
    client,
    query,
):
    query = query.strip()

    if not query:
        raise ValueError("Empty query")

    out = []

    async for dialog in client.iter_dialogs():
        try:
            async for msg in client.iter_messages(
                dialog.entity,
                search=query,
                limit=10,
            ):
                if not msg.message:
                    continue

                text = (
                    msg.message
                    .replace("\n", " ")
                    .strip()
                )

                out.append(
                    f"{dialog.name} | "
                    f"[{msg.id}] {text}"
                )

                if len(out) >= 100:
                    return "\n".join(out)

        except Exception:
            continue

    if not out:
        return "Nothing found."

    return "\n".join(out)


async def cmd_send(
    client,
    target,
    text,
):
    text = text.strip()

    if not text:
        raise ValueError("Empty message")

    entity = await resolve_target(
        client,
        target,
    )

    msg = await client.send_message(
        entity,
        text,
    )

    return (
        f"Sent. message_id={msg.id}"
    )


async def cmd_reply(
    client,
    target,
    data,
):
    if "|" not in data:
        raise ValueError(
            "Reply format: message_id|text"
        )

    message_id, text = data.split(
        "|",
        1,
    )

    message_id = message_id.strip()
    text = text.strip()

    if not message_id.isdigit():
        raise ValueError(
            "Invalid message_id"
        )

    if not text:
        raise ValueError(
            "Empty reply text"
        )

    entity = await resolve_target(
        client,
        target,
    )

    msg = await client.send_message(
        entity,
        text,
        reply_to=int(message_id),
    )

    return (
        f"Reply sent. message_id={msg.id}"
    )


async def execute(
    client,
    command,
    target,
    text,
):
    command = command.strip().lower()

    if command == "chats":
        return await cmd_chats(client)

    if command == "read":
        return await cmd_read(
            client,
            target,
        )

    if command == "search":
        return await cmd_search(
            client,
            target,
            text,
        )

    if command == "global_search":
        return await cmd_global_search(
            client,
            text,
        )

    if command == "send":
        return await cmd_send(
            client,
            target,
            text,
        )

    if command == "reply":
        return await cmd_reply(
            client,
            target,
            text,
        )

    raise ValueError(
        f"Unknown command: {command}"
    )


async def main():
    config = get_config()

    api_id = int(
        config["telegram_api_id"]
    )

    api_hash = config[
        "telegram_api_hash"
    ]

    url = config[
        "webapp_url"
    ]

    secret = config[
        "bridge_secret"
    ]

    session = config.get(
        "session_name",
        DEFAULT_SESSION,
    )

    poll = int(
        config.get(
            "poll_interval",
            DEFAULT_POLL_INTERVAL,
        )
    )

    print()
    print("==============================")
    print("        TeleBridge AI")
    print("==============================")
    print()

    client = TelegramClient(
        session,
        api_id,
        api_hash,
    )

    print(
        "[INFO] Connecting to Telegram..."
    )

    await client.start()

    me = await client.get_me()

    print()
    print("[OK] Telegram authorized")
    print(
        "Name:",
        me.first_name or "Unknown",
    )

    if me.username:
        print(
            "Username: @" + me.username
        )

    print("ID:", me.id)

    try:
        r = requests.get(
            url,
            params={
                "action": "ping",
                "secret": secret,
            },
            timeout=30,
        )

        r.raise_for_status()

        data = r.json()

        if data.get("ok"):
            print(
                "[OK] Google bridge connected"
            )
        else:
            print(
                "[WARNING] Bridge:",
                data,
            )

    except Exception as exc:
        print(
            "[ERROR] Google bridge unavailable:",
            exc,
        )

    print()
    print(
        "[OK] Waiting for ChatGPT commands..."
    )
    print()

    try:
        while True:
            cmd = bridge_get(
                url,
                secret,
            )

            if not cmd:
                await asyncio.sleep(poll)
                continue

            if not cmd.get("ok"):
                print(
                    "[WARNING] Bridge:",
                    cmd,
                )

                await asyncio.sleep(poll)
                continue

            if not cmd.get("found"):
                await asyncio.sleep(poll)
                continue

            command_id = str(
                cmd.get("id", "")
            )

            command = str(
                cmd.get("command", "")
            )

            target = str(
                cmd.get("target", "")
            )

            text = str(
                cmd.get("text", "")
            )

            print(
                f"[COMMAND] {command} | "
                f"{target} | {text[:80]}"
            )

            try:
                result = str(
                    await execute(
                        client,
                        command,
                        target,
                        text,
                    )
                )[:45000]

                bridge_result(
                    url,
                    secret,
                    command_id,
                    True,
                    result,
                )

                print("[OK] Done")

            except Exception as exc:
                error = (
                    f"{type(exc).__name__}: "
                    f"{exc}"
                )

                bridge_result(
                    url,
                    secret,
                    command_id,
                    False,
                    error,
                )

                print(
                    "[ERROR]",
                    error,
                )

            await asyncio.sleep(1)

    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())