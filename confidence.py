def compute_confidence(
    dual_agreement=False,
    symbolic_pass=False,
    numeric_pass=False,
    sandbox_success=False,
    reviewer_approved=False
):

    score = 0

    # Dual reasoning agreement
    if dual_agreement:
        score += 0.2

    # Symbolic verification
    if symbolic_pass:
        score += 0.2

    # Numeric verification
    if numeric_pass:
        score += 0.1

    # Code executed successfully
    if sandbox_success:
        score += 0.3

    # Reviewer approved
    if reviewer_approved:
        score += 0.2

    return round(score, 3)