import requests
import json

# Replace with your actual API endpoint and password
API_URL = "http://127.0.0.1:7860/v1/chat/completions"
PASSWORD = "123"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {PASSWORD}"
}

data = {
    "model": "gemini-2.5-flash",
    "messages": [
        {"role": "user", "content": "这个视频主人公是什么动物，描述一下每一个分镜"}
    ],
    "file_uri": "https://youtube.com/shorts/uKvarHcJSZk?si=9hCozH5a49zQLeey"
}

try:
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    response.raise_for_status()  # Raise an exception for bad status codes

    print("Request successful!")
    print("Response:", response.json())

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
