import requests
import json
import os
import time

API_URL = "https://openrouter.ai/api/v1/chat/completions"
TIMEOUT = 60
MAX_RETRIES = 3


def call_llm(system_prompt, user_prompt,
             max_tokens=800,
             temperature=0.3,
             model="Qwen/Qwen2.5-72B-Instruct"):  # 🔥 đổi model cho chắc

    api_key = os.getenv("QWEN_API_KEY")
    print("API KEY:", api_key)

    if not api_key:
        print("🔥 API key missing")
        return None

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
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
            print(f"\n🚀 Attempt {attempt + 1}")
            response = requests.post(
                API_URL,
                headers=headers,
                json=payload,
                timeout=TIMEOUT
            )

            print("STATUS CODE:", response.status_code)
            print("RAW RESPONSE:", response.text)

            if response.status_code != 200:
                return None

            data = response.json()
            return data["choices"][0]["message"]["content"]

        except Exception as e:
            print("🔥 LLM Exception:", e)

        time.sleep(2)

    return None


def call_llm_json(system_prompt, user_prompt,
                  max_tokens=800,
                  temperature=0.3,
                  model="qwen/qwen-2.5-14b-instruct"):

    raw = call_llm(system_prompt, user_prompt,
                   max_tokens, temperature, model)

    if not raw:
        return None

    try:
        return json.loads(raw)
    except Exception:
        print("⚠️ JSON parse failed")
        print("RAW CONTENT:", raw)
        return None