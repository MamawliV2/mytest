from telethon import TelegramClient, events
import asyncio
import re

# دریافت اطلاعات حساب کاربری از کاربر
api_id = input("Please enter your API ID: ")
api_hash = input("Please enter your API Hash: ")
phone_number = input("Please enter your phone number: ")
channel_username = input("Please enter the channel username (e.g., @channelusername): ")

# ایجاد یک کلاینت تلگرام
client = TelegramClient('session_name', api_id, api_hash)

# الگوهای regex برای شناسایی کانفیگ‌های V2rayng
vmess_pattern = re.compile(r'vmess://[a-zA-Z0-9+/=]+')
vless_pattern = re.compile(r'vless://[a-zA-Z0-9+/=]+')

@client.on(events.NewMessage)
async def handler(event):
    message = event.message.message
    vmess_matches = vmess_pattern.findall(message)
    vless_matches = vless_pattern.findall(message)
    
    if vmess_matches or vless_matches:
        for match in vmess_matches + vless_matches:
            modified_match = f'@subHiddify {match}'
            await client.send_message(channel_username, modified_match)

async def main():
    # اتصال به حساب کاربری
    await client.start(phone=phone_number)
    print("Client Created and Online")
    
    # نگه داشتن کلاینت آنلاین
    await client.run_until_disconnected()

# اجرای برنامه
client.loop.run_until_complete(main())
