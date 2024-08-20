#!/bin/bash

# Install necessary tools
sudo apt-get update
sudo apt-get install -y curl jq

# Get the user's phone number
read -p "Enter your phone number: " phone_number

# Validate the phone number (only digits and length between 10 to 15)
if [[ ! $phone_number =~ ^[0-9]+$ ]] || [[ ${#phone_number} -lt 10 ]] || [[ ${#phone_number} -gt 15 ]]; then
    echo "Invalid phone number. Please try again."
    exit 1
fi

# Send request to Telegram API to get the verification code
response=$(curl -s -X POST https://my.telegram.org/auth/send_code -d "phone_number=$phone_number")
phone_code_hash=$(echo $response | jq -r '.phone_code_hash')

if [[ $phone_code_hash == "null" ]]; then
    echo "Failed to send verification code. Please try again."
    exit 1
fi

# Get the verification code from the user
read -p "Enter the verification code sent to your phone: " phone_code

# Verify the phone number
auth_response=$(curl -s -X POST https://my.telegram.org/auth/sign_in -d "phone_number=$phone_number" -d "phone_code_hash=$phone_code_hash" -d "phone_code=$phone_code")

# Check if the login was successful
if [[ $(echo $auth_response | jq -r '.user') != "null" ]]; then
    echo "Login successful."

    # Generate random names and descriptions for the application
    app_title="App_$(date +%s)"
    app_short_name="AppShort_$(date +%s)"
    app_url="https://example.com"
    app_platform="web"
    app_desc="This is a random app description."

    # Send request to create a new application
    create_app_response=$(curl -s -X POST https://my.telegram.org/apps/create -d "hash=$(echo $auth_response | jq -r '.hash')" -d "app_title=$app_title" -d "app_short_name=$app_short_name" -d "app_url=$app_url" -d "app_platform=$app_platform" -d "app_desc=$app_desc")

    # Check if the application creation was successful
    if [[ $(echo $create_app_response | jq -r '.app_id') != "null" ]]; then
        # Get the API ID and API Hash
        api_id=$(echo $create_app_response | jq -r '.app_id')
        api_hash=$(echo $create_app_response | jq -r '.app_hash')

        echo "API ID: $api_id"
        echo "API Hash: $api_hash"
    else
        echo "Failed to create application. Please try again."
    fi
else
    echo "Login failed. Please try again."
fi
