import requests
import json


# 请替换为您的实际API端点和密码
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
    "file_uri": "https://generativelanguage.googleapis.com/v1beta/files/v2c50xwc7saj",
    "file_mime_type": "video/mp4"
}

try:
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    response.raise_for_status()  # 如果状态码不为2xx，则引发异常

    print("请求成功！")
    print("响应:", response.json())

except requests.exceptions.RequestException as e:
    print(f"发生错误: {e}")


# --- 文件上传接口测试 ---
# print("\n--- 开始测试文件上传 ---")
# UPLOAD_URL = "http://127.0.0.1:7860/v1/files"
# # 重要：请将 "YOUR_FILE_PATH_HERE" 替换为您的实际文件路径 (例如: "C:/images/my_image.png")
# FILE_PATH = "C:/Users/Administrator/Desktop/Child.mp4"

# upload_headers = {
#     "Authorization": f"Bearer {PASSWORD}"
# }

# # 可选：您可以为上传到Gemini的文件提供一个显示名称
# # upload_data = {
# #     "display_name": "my-test-file"
# # }

# try:
#     with open(FILE_PATH, "rb") as f:
#         files_payload = {'file': f}
#         response = requests.post(UPLOAD_URL, headers=upload_headers, files=files_payload)
#         response.raise_for_status()  # 如果状态码不为2xx，则引发异常

#         print("文件上传成功！")
#         print("上传文件详情:", response.json())

# except FileNotFoundError:
#     print(f"上传错误: 文件未在路径 '{FILE_PATH}' 找到。")
#     print("请更新脚本中的 FILE_PATH 变量为有效路径。")
# except requests.exceptions.RequestException as e:
#     print(f"文件上传时发生错误: {e}")
#     if e.response is not None:
#         print(f"状态码: {e.response.status_code}")
#         print(f"响应体: {e.response.text}")
# # e.status_code}")
#         print(f"响应体: {e.response.text}")
