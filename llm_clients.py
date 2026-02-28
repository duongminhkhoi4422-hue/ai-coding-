import requests
import json
import os
import time

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("QWEN_API_KEY")

TIMEOUT = 60
MAX_RETRIES = 3

def call_llm(system_prompt, user_prompt, max_tokens=800, temperature=0.3, model="qwen/qwen-2.5-14b-instruct"):

    if not API_KEY:
        print("🔥 API key missing")
        return None

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-app.onrender.com",
        "X-Title": "AI Competition Project"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                API_URL,
                headers=headers,
                json=payload,
                timeout=TIMEOUT
            )

            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]

            else:
                print("🔥 API ERROR:", response.text)

        except Exception as e:
            print("🔥 LLM Exception:", e)

        time.sleep(2)

    return None


def call_llm_json(system_prompt, user_prompt, max_tokens=800, temperature=0.3, model="qwen/qwen-2.5-14b-instruct"):

    raw = call_llm(system_prompt, user_prompt, max_tokens, temperature, model)

    if not raw:
        return None

    try:
        return json.loads(raw)
    except:
        print("⚠️ JSON parse failed")
        print(raw)
        return None