from orchestrator import run_code_pipeline

def pretty_print(result):
    print("\n" + "="*60)

    if "error" in result:
        print("❌ ERROR:", result["error"])
        return

    print("📌 PLAN:")
    print(result.get("plan"))

    print("\n💻 GENERATED CODE:")
    print(result.get("code"))

    print("\n🖥 SANDBOX RESULT:")
    sandbox = result.get("sandbox", {})
    print("Return Code:", sandbox.get("returncode"))
    print("STDOUT:\n", sandbox.get("stdout"))
    print("STDERR:\n", sandbox.get("stderr"))

    print("\n🎯 CONFIDENCE:", result.get("confidence"))
    print("="*60)


if __name__ == "__main__":

    # 🔥 Test case 1: simple python function
    problem = "Write a Python function that returns the factorial of a number and print factorial(5)."

    result = run_code_pipeline(problem, language="python")

    pretty_print(result)