#!/bin/bash

# نصب ابزارهای مورد نیاز
sudo apt-get update
sudo apt-get install -y curl jq

# دریافت شماره موبایل از کاربر
read -p "شماره موبایل خود را وارد کنید: " phone_number

# بررسی اعتبار شماره موبایل
if [[ ! $phone_number =~ ^[0-9]{10,15}$ ]]; then
    echo "شماره موبایل نامعتبر است. لطفاً دوباره تلاش کنید."
    exit 1
fi

# ارسال درخواست به API تلگرام برای دریافت کد تایید
response=$(curl -s -X POST https://my.telegram.org/auth/send_code -d "phone_number=$phone_number")
phone_code_hash=$(echo $response | jq -r '.phone_code_hash')

if [[ $phone_code_hash == "null" ]]; then
    echo "ارسال کد تایید ناموفق بود. لطفاً دوباره تلاش کنید."
    exit 1
fi

# دریافت کد تایید از کاربر
read -p "کد تایید ارسال شده به موبایل خود را وارد کنید: " phone_code

# تایید شماره موبایل
auth_response=$(curl -s -X POST https://my.telegram.org/auth/sign_in -d "phone_number=$phone_number" -d "phone_code_hash=$phone_code_hash" -d "phone_code=$phone_code")

# بررسی موفقیت آمیز بودن ورود
if [[ $(echo $auth_response | jq -r '.user') != "null" ]]; then
    echo "ورود موفقیت آمیز بود."

    # تولید نام و توضیحات تصادفی برای اپلیکیشن
    app_title="App_$(date +%s)"
    app_short_name="AppShort_$(date +%s)"
    app_url="https://example.com"
    app_platform="web"
    app_desc="This is a random app description."

    # ارسال درخواست برای ایجاد اپلیکیشن جدید
    create_app_response=$(curl -s -X POST https://my.telegram.org/apps/create -d "hash=$(echo $auth_response | jq -r '.hash')" -d "app_title=$app_title" -d "app_short_name=$app_short_name" -d "app_url=$app_url" -d "app_platform=$app_platform" -d "app_desc=$app_desc")

    # بررسی موفقیت آمیز بودن ایجاد اپلیکیشن
    if [[ $(echo $create_app_response | jq -r '.app_id') != "null" ]]; then
        # دریافت API ID و API Hash
        api_id=$(echo $create_app_response | jq -r '.app_id')
        api_hash=$(echo $create_app_response | jq -r '.app_hash')

        echo "API ID: $api_id"
        echo "API Hash: $api_hash"
    else
        echo "ایجاد اپلیکیشن ناموفق بود. لطفاً دوباره تلاش کنید."
    fi
else
    echo "ورود ناموفق بود. لطفاً دوباره تلاش کنید."
fi
