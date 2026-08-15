import asyncio
import os
from getpass import getpass

import requests
from telethon import TelegramClient

API_ID = int(os.getenv('TELEGRAM_API_ID', '0'))
API_HASH = os.getenv('TELEGRAM_API_HASH', '').strip()
WEBAPP_URL = os.getenv('TELEBRIDGE_WEBAPP_URL', '').strip()
BRIDGE_SECRET = os.getenv('TELEBRIDGE_SECRET', '').strip()
POLL_INTERVAL = int(os.getenv('TELEBRIDGE_POLL_INTERVAL', '3'))
SESSION_NAME = os.getenv('TELEBRIDGE_SESSION', 'my_account')


def require_config():
    global API_ID, API_HASH

    if not API_ID:
        raw = input('Telegram API ID: ').strip()
        if not raw.isdigit():
            raise SystemExit('Invalid API ID')
        API_ID = int(raw)

    if not API_HASH:
        API_HASH = getpass('Telegram API HASH: ').strip()

    if not WEBAPP_URL:
        raise SystemExit('Missing TELEBRIDGE_WEBAPP_URL')

    if not BRIDGE_SECRET:
        raise SystemExit('Missing TELEBRIDGE_SECRET')


def bridge_get():
    try:
        r = requests.get(
            WEBAPP_URL,
            params={'action': 'pending', 'secret': BRIDGE_SECRET},
            timeout=30,
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print('â Bridge GET:', type(e).__name__, e)
        return None


def bridge_result(command_id, ok, result):
    try:
        r = requests.post(
            WEBAPP_URL,
            json={
                'action': 'result',
                'secret': BRIDGE_SECRET,
                'id': command_id,
                'ok': ok,
                'result': result,
            },
            timeout=30,
        )
        r.raise_for_status()
        try:
            return r.json()
        except Exception:
            return None
    except Exception as e:
        print('â Bridge POST:', type(e).__name__, e)
        return None


async def resolve_target(client, target):
    target = target.strip()
    if not target:
        raise ValueError('Target is empty')

    if target.lstrip('-').isdigit():
        return await client.get_entity(int(target))

    try:
        return await client.get_entity(target)
    except Exception:
        pass

    target_lower = target.lower()

    async for dialog in client.iter_dialogs():
        name = (dialog.name or '').strip().lower()
        if name == target_lower:
            return dialog.entity

    async for dialog in client.iter_dialogs():
        name = (dialog.name or '').strip().lower()
        if target_lower in name:
            return dialog.entity

    raise ValueError(f'Chat not found: {target}')


async def cmd_chats(client):
    out = []
    async for dialog in client.iter_dialogs(limit=100):
        username = getattr(dialog.entity, 'username', None)
        line = f'{dialog.id} | {dialog.name}'
        if username:
            line += f' | @{username}'
        out.append(line)
    return '\n'.join(out)


async def cmd_read(client, target, limit=40):
    entity = await resolve_target(client, target)
    out = []

    async for msg in client.iter_messages(entity, limit=limit):
        if not msg.message:
            continue

        sender_name = '?'
        try:
            sender = await msg.get_sender()
            if sender:
                sender_name = (
                    getattr(sender, 'first_name', None)
                    or getattr(sender, 'title', None)
                    or getattr(sender, 'username', None)
                    or str(getattr(sender, 'id', '?'))
                )
        except Exception:
            pass

        text = msg.message.replace('\n', ' ').strip()
        out.append(f'[{msg.id}] {sender_name}: {text}')

    out.reverse()
    return '\n'.join(out) if out else 'No text messages.'


async def cmd_search(client, target, query):
    query = query.strip()
    if not query:
        raise ValueError('Empty query')

    entity = await resolve_target(client, target)
    out = []

    async for msg in client.iter_messages(entity, search=query, limit=100):
        if msg.message:
            text = msg.message.replace('\n', ' ').strip()
            out.append(f'[{msg.id}] {text}')

    return '\n'.join(out) if out else 'Nothing found.'


async def cmd_global_search(client, query):
    query = query.strip()
    if not query:
        raise ValueError('Empty query')

    out = []
    async for dialog in client.iter_dialogs():
        try:
            async for msg in client.iter_messages(dialog.entity, search=query, limit=10):
                if not msg.message:
                    continue
                text = msg.message.replace('\n', ' ').strip()
                out.append(f'{dialog.name} | [{msg.id}] {text}')
                if len(out) >= 100:
                    return '\n'.join(out)
        except Exception:
            continue

    return '\n'.join(out) if out else 'Nothing found.'


async def cmd_send(client, target, text):
    text = text.strip()
    if not text:
        raise ValueError('Empty message')

    entity = await resolve_target(client, target)
    msg = await client.send_message(entity, text)
    return f'Sent. message_id={msg.id}'


async def cmd_reply(client, target, data):
    if '|' not in data:
        raise ValueError('Reply format: message_id|text')

    message_id, text = data.split('|', 1)
    message_id = message_id.strip()
    text = text.strip()

    if not message_id.isdigit():
        raise ValueError('Invalid message_id')
    if not text:
        raise ValueError('Empty reply text')

    entity = await resolve_target(client, target)
    msg = await client.send_message(entity, text, reply_to=int(message_id))
    return f'Reply sent. message_id={msg.id}'


async def execute(client, command, target, text):
    command = command.strip().lower()

    if command == 'chats':
        return await cmd_chats(client)
    if command == 'read':
        return await cmd_read(client, target)
    if command == 'search':
        return await cmd_search(client, target, text)
    if command == 'global_search':
        return await cmd_global_search(client, text)
    if command == 'send':
        return await cmd_send(client, target, text)
    if command == 'reply':
        return await cmd_reply(client, target, text)

    raise ValueError(f'Unknown command: {command}')


async def main():
    require_config()

    print('==============================')
    print('      TeleBridge AI')
    print('==============================')

    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()

    me = await client.get_me()
    print('â Telegram authorized')
    print('Name:', me.first_name)
    if me.username:
        print('Username: @' + me.username)
    print('ID:', me.id)

    try:
        r = requests.get(
            WEBAPP_URL,
            params={'action': 'ping', 'secret': BRIDGE_SECRET},
            timeout=30,
        )
        ping = r.json()
        if ping.get('ok'):
            print('â Bridge connected')
        else:
            print('â ï¸ Bridge:', ping)
    except Exception as e:
        print('â Bridge unavailable:', e)

    print('â Waiting for AI commands...')

    try:
        while True:
            cmd = bridge_get()

            if not cmd:
                await asyncio.sleep(POLL_INTERVAL)
                continue

            if not cmd.get('ok'):
                print('â ï¸ Bridge:', cmd)
                await asyncio.sleep(POLL_INTERVAL)
                continue

            if not cmd.get('found'):
                await asyncio.sleep(POLL_INTERVAL)
                continue

            command_id = str(cmd.get('id', ''))
            command = str(cmd.get('command', ''))
            target = str(cmd.get('target', ''))
            text = str(cmd.get('text', ''))

            print(f'â¶ {command} | {target} | {text[:80]}')

            try:
                result = await execute(client, command, target, text)
                result = str(result)[:45000]
                bridge_result(command_id, True, result)
                print('â Done')
            except Exception as e:
                error = f'{type(e).__name__}: {e}'
                bridge_result(command_id, False, error)
                print('â', error)

            await asyncio.sleep(1)
    finally:
        await client.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
