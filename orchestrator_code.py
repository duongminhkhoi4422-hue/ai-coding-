from agents.planner import planner
from agents.coder import coder
from agents.reviewer import reviewer
from sandbox import run_code_safely
from confidence import compute_confidence


def run_code_pipeline(problem, language="python"):

    # 1️⃣ Planner
    plan = planner(problem)
    if not plan:
        return {"error": "Planner failed"}

    # 2️⃣ Code generation
    coder_result = coder(problem, language=language)

    if not coder_result:
        return {"error": "Code generation failed"}

    # 🔥 Handle both dict or string
    if isinstance(coder_result, dict):
        code = coder_result.get("code")
    else:
        code = coder_result

    if not code:
        return {"error": "Empty code returned"}

    # 3️⃣ Sandbox execution
    sandbox_result = run_code_safely(code, language)
    sandbox_success = sandbox_result.get("returncode", 1) == 0

    # 4️⃣ Review
    review = reviewer(code, language=language)

    if isinstance(review, str):
        reviewer_approved = "APPROVED" in review.upper()
    else:
        reviewer_approved = review.get("approved", False)

    # 5️⃣ Confidence (REAL scoring)
    confidence = compute_confidence(
        dual_agreement=True,
        symbolic_pass=False,
        numeric_pass=False,
        sandbox_success=sandbox_success,
        reviewer_approved=reviewer_approved
    )

    return {
        "plan": plan,
        "code": code,
        "sandbox": sandbox_result,
        "confidence": confidence
    }