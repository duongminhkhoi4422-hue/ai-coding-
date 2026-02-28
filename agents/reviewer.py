from llm_clients import call_llm
from language_utils import normalize_language


def reviewer(code: str, language: str):

    if not code:
        return None

    try:
        language = normalize_language(language)
    except ValueError:
        return code

    system_prompt = f"""
You are a strict senior code reviewer.

Language: {language}

If the code is correct:
Return the SAME code.

If incorrect:
Return a FIXED version of the complete code.

Rules:
- Return ONLY code
- No explanation
- No markdown
"""

    result = call_llm(system_prompt, code)

    if not result:
        print("❌ Reviewer LLM failed")
        return code

    return result.strip()