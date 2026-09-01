from apps.services.code_runner import CodeRunner


def test_run_python_correct_output():
    runner = CodeRunner()
    code = "print(2 + 2)"
    output, had_error = runner.run_python(code, stdin_data="")

    assert output == "4"
    assert had_error is False

def test_run_python_syntax_error():
    runner = CodeRunner()
    code = "print(2 + )"  # Syntax error
    output, had_error = runner.run_python(code, stdin_data="")

    assert "SyntaxError" in output
    assert had_error is True