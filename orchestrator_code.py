from agents.planner import planner
from agents.coder import coder
from agents.reviewer import reviewer
from confidence import compute_confidence
from sandbox import execute_code
from language_utils import normalize_language


def clean_code(code: str):
    if not code:
        return ""

    code = code.replace("```python", "")
    code = code.replace("```cpp", "")
    code = code.replace("```c++", "")
    code = code.replace("```c", "")
    code = code.replace("```java", "")
    code = code.replace("```javascript", "")
    code = code.replace("```html", "")
    code = code.replace("```", "")

    return code.strip()


def run_code_pipeline(problem: str, language: str):

    try:
        language = normalize_language(language)
    except Exception:
        return "Unsupported language"

    # ===== Planner =====
    try:
        plan = planner(problem)
    except Exception:
        plan = None

    # ===== Coder =====
    try:
        generated_code = coder(problem, language, plan)
    except Exception:
        generated_code = None

    if not generated_code:
        return "Cannot generate code"

    # ===== Reviewer =====
    try:
        reviewed_code = reviewer(generated_code, language)
    except Exception:
        reviewed_code = generated_code

    # ===== Sandbox =====
    try:
        execute_code(reviewed_code, language)
    except Exception:
        pass

    # ===== Confidence =====
    try:
        compute_confidence(problem, reviewed_code)
    except Exception:
        pass

    return clean_code(reviewed_code)