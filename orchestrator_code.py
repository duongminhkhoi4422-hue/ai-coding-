from agents.planner import planner
from agents.coder import coder
from agents.reviewer import reviewer
from confidence import compute_confidence
from sandbox import execute_code


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

    # ===== Planner =====
    plan = planner(problem, language)

    # ===== Coder =====
    generated_code = coder(problem, language, plan)

    # ===== Reviewer =====
    reviewed_code = reviewer(problem, language, generated_code)

    # ===== Sandbox (optional execution test) =====
    try:
        execute_code(reviewed_code, language)
    except Exception:
        pass

    # ===== Confidence =====
    try:
        compute_confidence(problem, reviewed_code)
    except Exception:
        pass

    # ===== Return CLEAN CODE ONLY =====
    return clean_code(reviewed_code)