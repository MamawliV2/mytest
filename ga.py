import requests
import random
import string

def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def create_telegram_app(phone_number):
    session = requests.Session()
    
    # مرحله ورود به سایت تلگرام
    login_url = 'https://my.telegram.org/auth/login'
    login_data = {
        'phone': phone_number
    }
    session.post(login_url, data=login_data)
    
    # مرحله دریافت کد تایید (این مرحله نیاز به تعامل کاربر دارد)
    code = input("Enter the code you received: ")
    code_url = 'https://my.telegram.org/auth/login'
    code_data = {
        'phone': phone_number,
        'random_hash': code
    }
    session.post(code_url, data=code_data)
    
    # مرحله ایجاد اپلیکیشن
    create_app_url = 'https://my.telegram.org/apps'
    app_data = {
        'app_title': generate_random_string(10),
        'app_shortname': generate_random_string(10),
        'app_url': 'http://example.com',
        'app_platform': 'android',
        'app_desc': generate_random_string(20)
    }
    response = session.post(create_app_url, data=app_data)
    
    # استخراج API ID و API Hash
    api_id = response.json().get('app_id')
    api_hash = response.json().get('app_hash')
    
    return api_id, api_hash

phone_number = input("Enter your phone number: ")
api_id, api_hash = create_telegram_app(phone_number)
print(f"API ID: {api_id}")
print(f"API Hash: {api_hash}")
