from typing import Any, cast

from apps.services.submission_service import SubmissionService
from apps.services.code_runner import CodeRunner
from apps.models import Problem, SubmissionStatus


class FakeProblemRepository:
    def __init__(self, problem):
        self.problem = problem

    def get_by_id(self, problem_id):
        return self.problem


class FakeSubmissionRepository:
    def __init__(self):
        self.saved = None

    def create(self, submission):
        self.saved = submission
        return submission


def test_submit_accepted():
    # 1. build a fake Problem with test_input="2 3" and expected_output="5"
    problem = Problem(
        id=1,
        title="Test Problem",
        description="A simple test problem",
        test_input="2 3",
        expected_output="5",
    )
    # 2. build the service using FakeProblemRepository, FakeSubmissionRepository, CodeRunner()
    service = SubmissionService(
        problem_repo=cast(Any, FakeProblemRepository(problem)),
        submission_repo=cast(Any, FakeSubmissionRepository()),
        code_runner=CodeRunner(),
    )
    # 3. call service.submit(user_id=1, problem_id=1, code="a,b=map(int,input().split());print(a+b)", language="python")
    result = service.submit(
        user_id=1,
        problem_id=1,
        code="a,b=map(int,input().split());print(a+b)",
        language="python",
    )
    # 4. assert the result's status is SubmissionStatus.ACCEPTED
    assert cast(Any, result.status) == SubmissionStatus.ACCEPTED

def test_submit_wrong_answer():
    # 1. build a fake Problem with test_input="2 3" and expected_output="5"
    problem = Problem(
        id=1,
        title="Test Problem",
        description="A simple test problem",
        test_input="2 3",
        expected_output="5",
    )
    # 2. build the service using FakeProblemRepository, FakeSubmissionRepository, CodeRunner()
    service = SubmissionService(
        problem_repo=cast(Any, FakeProblemRepository(problem)),
        submission_repo=cast(Any, FakeSubmissionRepository()),
        code_runner=CodeRunner(),
    )
    # 3. call service.submit(user_id=1, problem_id=1, code="a,b=map(int,input().split());print(a*b)", language="python")
    result = service.submit(
        user_id=1,
        problem_id=1,
        code="a,b=map(int,input().split());print(a*b)",
        language="python",
    )
    # 4. assert the result's status is SubmissionStatus.WRONG_ANSWER
    assert cast(Any, result.status) == SubmissionStatus.WRONG_ANSWER