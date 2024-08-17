from telethon import TelegramClient, events
import asyncio
import re
import base64
import json

# دریافت اطلاعات حساب کاربری از کاربر
api_id = input("Please enter your API ID: ")
api_hash = input("Please enter your API Hash: ")
phone_number = input("Please enter your phone number: ")
channel_username = input("Please enter the channel username (e.g., @channelusername): ")

# ایجاد یک کلاینت تلگرام
client = TelegramClient('session_name', api_id, api_hash)

# الگوهای کانفیگ V2rayng
vmess_pattern = r'vmess://\S+'
vless_ss_pattern = r'(vless://\S+|ss://\S+)'

@client.on(events.NewMessage)
async def handler(event):
    message = event.message.message
    
    # بررسی کانفیگ‌های Vmess
    vmess_matches = re.findall(vmess_pattern, message)
    for match in vmess_matches:
        # Decode the base64 vmess link
        decoded_data = base64.b64decode(match[8:]).decode('utf-8')
        config = json.loads(decoded_data)
        
        # Modify the remarks
        config['ps'] = '@subHiddify'
        
        # Encode back to base64
        modified_data = base64.b64encode(json.dumps(config).encode('utf-8')).decode('utf-8')
        modified_vmess = f'vmess://{modified_data}'
        
        # Send the modified vmess link to the channel
        await client.send_message(channel_username, modified_vmess)
    
    # بررسی کانفیگ‌های Vless و Ss
    vless_ss_matches = re.findall(vless_ss_pattern, message)
    for match in vless_ss_matches:
        if '#' in match:
            parts = match.split('#')
            if len(parts) > 1:
                parts[-1] = '@subHiddify'
                modified_vless_ss = '#'.join(parts)
                await client.send_message(channel_username, modified_vless_ss)

async def main():
    # اتصال به حساب کاربری
    await client.start(phone=phone_number)
    print("Client Created and Online")

    # نگه داشتن کلاینت آنلاین
    await client.run_until_disconnected()

# اجرای برنامه
client.loop.run_until_complete(main())
