#!/bin/bash

# دریافت اطلاعات حساب کاربری از کاربر
read -p "Please enter your API ID: " api_id
read -p "Please enter your API Hash: " api_hash
read -p "Please enter your phone number: " phone_number
read -p "Please enter the channel username (e.g., @channelusername): " channel_username

# ایجاد یک فایل پایتون موقت با اطلاعات کاربر
cat << EOF > temp_script.py
from telethon import TelegramClient, events
import asyncio
import re
import base64
import json

api_id = "$api_id"
api_hash = "$api_hash"
phone_number = "$phone_number"
channel_username = "$channel_username"

client = TelegramClient('session_name', api_id, api_hash)

vmess_pattern = r'vmess://\S+'
vless_ss_pattern = r'(vless://\S+|ss://\S+)'

@client.on(events.NewMessage)
async def handler(event):
    message = event.message.message
    
    vmess_matches = re.findall(vmess_pattern, message)
    for match in vmess_matches:
        decoded_data = base64.b64decode(match[8:]).decode('utf-8')
        config = json.loads(decoded_data)
        config['ps'] = '@subHiddify'
        modified_data = base64.b64encode(json.dumps(config).encode('utf-8')).decode('utf-8')
        modified_vmess = f'vmess://{modified_data}'
        await client.send_message(channel_username, f'`{modified_vmess}`')
    
    vless_ss_matches = re.findall(vless_ss_pattern, message)
    for match in vless_ss_matches:
        if '#' in match:
            parts = match.split('#')
            if len(parts) > 1:
                parts[-1] = '@subHiddify'
                modified_vless_ss = '#'.join(parts)
                await client.send_message(channel_username, f'`{modified_vless_ss}`')

async def main():
    await client.start(phone=phone_number)
    print("Client Created and Online")
    await client.run_until_disconnected()

client.loop.run_until_complete(main())
EOF

# اجرای اسکریپت پایتون
python3 temp_script.py

# حذف فایل پایتون موقت
rm temp_script.py
