from telethon import TelegramClient, events
import asyncio
import re
import json
import base64

async def get_user_input(prompt):
    return input(prompt)

async def main():
    # دریافت اطلاعات حساب کاربری از کاربر
    api_id = await get_user_input("Please enter your API ID: ")
    api_hash = await get_user_input("Please enter your API Hash: ")
    phone_number = await get_user_input("Please enter your phone number: ")
    channel_username = await get_user_input("Please enter the channel username (e.g., @channelusername): ")

    # ایجاد یک کلاینت تلگرام
    client = TelegramClient('session_name', api_id, api_hash)

    # الگوهای regex برای شناسایی کانفیگ‌های V2rayng و Shadowsocks
    vmess_pattern = re.compile(r'vmess://[a-zA-Z0-9+/=]+')
    vless_pattern = re.compile(r'vless://[a-zA-Z0-9+/=]+')
    ss_pattern = re.compile(r'ss://[a-zA-Z0-9+/=]+')

    def modify_config(config_url, name):
        try:
            # Decode the base64 encoded config
            config_json = json.loads(base64.b64decode(config_url.split('://')[1]).decode('latin-1'))
            # Modify the name
            config_json['ps'] = name
            # Encode the config back to base64
            modified_config_url = config_url.split('://')[0] + '://' + base64.b64encode(json.dumps(config_json).encode('utf-8')).decode('utf-8')
            return modified_config_url
        except Exception as e:
            print(f"Error modifying config: {e}")
            return config_url

    @client.on(events.NewMessage)
    async def handler(event):
        message = event.message.message
        vmess_matches = vmess_pattern.findall(message)
        vless_matches = vless_pattern.findall(message)
        ss_matches = ss_pattern.findall(message)
        
        if vmess_matches or vless_matches or ss_matches:
            for match in vmess_matches + vless_matches + ss_matches:
                modified_match = modify_config(match, '@subHiddify')
                await client.send_message(channel_username, modified_match)

    # اتصال به حساب کاربری
    await client.start(phone=phone_number)
    print("Client Created and Online")
    
    # نگه داشتن کلاینت آنلاین
    await client.run_until_disconnected()

# اجرای برنامه
asyncio.run(main())
