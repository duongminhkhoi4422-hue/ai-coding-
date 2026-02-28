from llm_clients import call_llm
from language_utils import normalize_language


def reviewer(code: str, language: str = "python"):

    if not code:
        return None

    try:
        language = normalize_language(language)
    except ValueError as e:
        return {
            "approved": False,
            "reason": str(e)
        }

    system_prompt = f"""
You are a strict senior code reviewer.

Language: {language}

If the code is correct:
Respond with:
APPROVED

If incorrect:
Explain issues clearly.
Focus on:
- Logical errors
- Edge cases
- Runtime issues
- Performance problems

Be concise.
"""

    result = call_llm(system_prompt, code)

    if not result:
        print("❌ Reviewer LLM failed")
        return None

    return result.strip()