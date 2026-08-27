from apps import models
from apps.repository.problem_repository import ProblemRepository
from apps.repository.submission_repository import SubmissionRepository
from apps.services.code_runner import CodeRunner
from apps.models import SubmissionStatus
from typing import cast


class SubmissionService:
    def __init__(
        self,
        problem_repo: ProblemRepository,
        submission_repo: SubmissionRepository,
        code_runner: CodeRunner,
    ):
        self.problem_repo = problem_repo
        self.submission_repo = submission_repo
        self.code_runner = code_runner

    def submit(self, user_id: int, problem_id: int, code: str, language: str) -> models.Submission:
        problem = self.problem_repo.get_by_id(problem_id)
        if not problem:
            raise ValueError("Problem not found")

        if language == "python":
            output, had_error = self.code_runner.run_python(
                code, cast(str, problem.test_input))

            if had_error:
                status_result = SubmissionStatus.RUNTIME_ERROR
            elif output == problem.expected_output.strip():
                status_result = SubmissionStatus.ACCEPTED
            else:
                status_result = SubmissionStatus.WRONG_ANSWER
        else:
            output, status_result = "Language not supported yet", SubmissionStatus.PENDING

        submission = models.Submission(
            user_id=user_id,
            problem_id=problem_id,
            code=code,
            language=language,
            status=status_result,
            output=output,
        )

        return self.submission_repo.create(submission)
