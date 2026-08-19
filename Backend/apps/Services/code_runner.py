import subprocess
import tempfile
import os

JUDGE_TIMEOUT_SECONDS = 5


class CodeRunner:
    """Runs untrusted code in a subprocess and captures its output.
    NOTE: subprocess isolation is not enough for production — swap for
    Docker-per-submission before deploying publicly."""

    def run_python(self, code: str, stdin_data: str) -> tuple[str, bool]:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            script_path = f.name

        try:
            result = subprocess.run(
                ["python3", script_path],
                input=stdin_data,
                capture_output=True,
                text=True,
                timeout=JUDGE_TIMEOUT_SECONDS,
            )
            if result.returncode != 0:
                return result.stderr.strip(), True
            return result.stdout.strip(), False
        except subprocess.TimeoutExpired:
            return "Time Limit Exceeded", True
        finally:
            os.remove(script_path)
