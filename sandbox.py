import subprocess
import tempfile
import os
from language_utils import normalize_language


def execute_code(code: str, language: str):

    try:
        language = normalize_language(language)
    except ValueError as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "returncode": 1,
            "executed_code": code
        }

    try:

        # =========================
        # PYTHON
        # =========================
        if language == "python":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
                f.write(code.encode())
                filename = f.name

            result = subprocess.run(
                ["python3", filename],
                capture_output=True,
                text=True,
                timeout=5
            )

        # =========================
        # JAVASCRIPT
        # =========================
        elif language == "javascript":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".js") as f:
                f.write(code.encode())
                filename = f.name

            result = subprocess.run(
                ["node", filename],
                capture_output=True,
                text=True,
                timeout=5
            )

        # =========================
        # C++
        # =========================
        elif language == "c++":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp") as f:
                f.write(code.encode())
                source = f.name

            binary = source.replace(".cpp", "")

            compile_process = subprocess.run(
                ["g++", source, "-O2", "-o", binary],
                capture_output=True,
                text=True
            )

            if compile_process.returncode != 0:
                return {
                    "stdout": "",
                    "stderr": compile_process.stderr,
                    "returncode": 1,
                    "executed_code": code
                }

            result = subprocess.run(
                [binary],
                capture_output=True,
                text=True,
                timeout=5
            )

        # =========================
        # JAVA
        # =========================
        elif language == "java":
            with tempfile.TemporaryDirectory() as tmpdir:
                filepath = os.path.join(tmpdir, "Main.java")

                with open(filepath, "w") as f:
                    f.write(code)

                compile_process = subprocess.run(
                    ["javac", filepath],
                    capture_output=True,
                    text=True
                )

                if compile_process.returncode != 0:
                    return {
                        "stdout": "",
                        "stderr": compile_process.stderr,
                        "returncode": 1,
                        "executed_code": code
                    }

                result = subprocess.run(
                    ["java", "-cp", tmpdir, "Main"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

        else:
            return {
                "stdout": "",
                "stderr": f"Unsupported language: {language}",
                "returncode": 1,
                "executed_code": code
            }

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "executed_code": code
        }

    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "Execution timed out",
            "returncode": 1,
            "executed_code": code
        }

    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "returncode": 1,
            "executed_code": code
        }


# Backward compatibility
run_code_safely = execute_code