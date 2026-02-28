import json
import re
from llm_clients import call_llm
from language_utils import normalize_language


def extract_json(raw):
    if not raw:
        return None

    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        return None

    try:
        return json.loads(match.group())
    except Exception:
        return None


def coder(input_data, language="python"):

    try:
        language = normalize_language(language)
    except ValueError:
        return None

    if isinstance(input_data, dict):
        user_prompt = json.dumps(input_data, indent=2)
    else:
        user_prompt = str(input_data)

    system_prompt = f"""
You are a professional software engineer.

Task:
Generate complete runnable {language} code.

Rules:
- Return ONLY JSON
- No explanation
- No markdown
- Format:

{{
  "code": "complete runnable {language} code"
}}
"""

    raw = call_llm(system_prompt, user_prompt, temperature=0.2)

    if not raw:
        print("❌ Coder LLM failed")
        return None

    result = extract_json(raw)

    if not result or "code" not in result:
        print("❌ Invalid JSON from LLM")
        print("RAW OUTPUT:\n", raw)
        return None

    return result