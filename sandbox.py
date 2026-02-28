import subprocess
import tempfile
import os
import shutil
from language_utils import normalize_language


TIMEOUT = 5


def execute_code(code: str, language: str):

    try:
        language = normalize_language(language)
    except ValueError as e:
        return error_response(str(e), code)

    try:
        with tempfile.TemporaryDirectory() as tmpdir:

            # =========================
            # PYTHON
            # =========================
            if language == "python":
                filepath = os.path.join(tmpdir, "main.py")
                with open(filepath, "w") as f:
                    f.write(code)

                result = run_process(
                    ["python3", filepath]
                )

            # =========================
            # JAVASCRIPT
            # =========================
            elif language == "javascript":
                filepath = os.path.join(tmpdir, "main.js")
                with open(filepath, "w") as f:
                    f.write(code)

                result = run_process(
                    ["node", filepath]
                )

            # =========================
            # C
            # =========================
            elif language == "c":
                source = os.path.join(tmpdir, "main.c")
                binary = os.path.join(tmpdir, "main")

                with open(source, "w") as f:
                    f.write(code)

                compile_process = subprocess.run(
                    ["gcc", source, "-O2", "-o", binary],
                    capture_output=True,
                    text=True
                )

                if compile_process.returncode != 0:
                    return error_response(compile_process.stderr, code)

                result = run_process([binary])

            # =========================
            # C++
            # =========================
            elif language == "c++":
                source = os.path.join(tmpdir, "main.cpp")
                binary = os.path.join(tmpdir, "main")

                with open(source, "w") as f:
                    f.write(code)

                compile_process = subprocess.run(
                    ["g++", source, "-O2", "-o", binary],
                    capture_output=True,
                    text=True
                )

                if compile_process.returncode != 0:
                    return error_response(compile_process.stderr, code)

                result = run_process([binary])

            # =========================
            # JAVA
            # =========================
            elif language == "java":
                source = os.path.join(tmpdir, "Main.java")

                with open(source, "w") as f:
                    f.write(code)

                compile_process = subprocess.run(
                    ["javac", source],
                    capture_output=True,
                    text=True
                )

                if compile_process.returncode != 0:
                    return error_response(compile_process.stderr, code)

                result = run_process(
                    ["java", "-cp", tmpdir, "Main"]
                )

            # =========================
            # HTML
            # =========================
            elif language == "html":
                # HTML không execute — chỉ trả về content
                return {
                    "stdout": code,
                    "stderr": "",
                    "returncode": 0,
                    "executed_code": code
                }

            else:
                return error_response(f"Unsupported language: {language}", code)

            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "executed_code": code
            }

    except subprocess.TimeoutExpired:
        return error_response("Execution timed out", code)

    except Exception as e:
        return error_response(str(e), code)


def run_process(command):
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=TIMEOUT
    )


def error_response(message, code):
    return {
        "stdout": "",
        "stderr": message,
        "returncode": 1,
        "executed_code": code
    }


# Backward compatibility
run_code_safely = execute_code