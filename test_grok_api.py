import requests
import json
import os

# 配置
BASE_URL = "https://vlbbwuag.us-east-1.clawcloudrun.com"

PASSWORD = os.environ.get("PASSWORD", "woyaow800cA")

def test_models():
    print("--- 测试模型列表 ---")
    headers = {"Authorization": f"Bearer {PASSWORD}"}
    try:
        response = requests.get(f"{BASE_URL}/v1/models", headers=headers)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            models = data.get("data", [])
            grok_models = [m["id"] for m in models if m["id"].startswith("grok-")]
            print(f"总模型数: {len(models)}")
            print(f"找到 Grok 模型: {grok_models}")
        else:
            print(f"错误响应: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")

def test_chat():
    print("\n--- 测试 Grok 聊天 (流式) ---")
    headers = {
        "Authorization": f"Bearer {PASSWORD}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "grok-3-fast",
        "messages": [{"role": "user", "content": "你好"}],
        "stream": True
    }
    try:
        response = requests.post(
            f"{BASE_URL}/v1/chat/completions", 
            headers=headers, 
            json=payload, 
            stream=True,
            timeout=60
        )
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("收到流式响应:")
            for line in response.iter_lines():
                if line:
                    line_text = line.decode('utf-8')
                    if line_text.startswith("data: "):
                        data_str = line_text[6:]
                        if data_str.strip() == "[DONE]":
                            print("\n[完成]")
                            break
                        try:
                            data = json.loads(data_str)
                            if "choices" in data and len(data["choices"]) > 0:
                                delta = data["choices"][0].get("delta", {})
                                content = delta.get("content", "")
                                print(content, end="", flush=True)
                        except Exception as e:
                            # 忽略解析错误（可能是非 JSON 行）
                            pass
        else:
            print(f"错误响应: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    print(f"当前测试密码: {PASSWORD}")
    test_models()
    test_chat()
