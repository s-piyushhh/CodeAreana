from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from typing import cast
from apps.database import get_db
from apps import schemas, models
from apps.auth import get_current_user
from apps.repository.problem_repository import ProblemRepository
from apps.repository.submission_repository import SubmissionRepository
from apps.services.code_runner import CodeRunner
from apps.services.submission_service import SubmissionService

router = APIRouter(prefix="/submissions", tags=["submissions"])


@router.post("/", response_model=schemas.SubmissionOut, status_code=status.HTTP_201_CREATED)
def submit_solution(
    submission_in: schemas.SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    service = SubmissionService(
        problem_repo=ProblemRepository(db),
        submission_repo=SubmissionRepository(db),
        code_runner=CodeRunner(),
    )
    try:
        return service.submit(
            user_id=cast(int, current_user.id),
            problem_id=submission_in.problem_id,
            code=submission_in.code,
            language=submission_in.language,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/me", response_model=List[schemas.SubmissionOut])
def my_submissions(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    repo = SubmissionRepository(db)
    return repo.get_by_user(cast(int, current_user.id))


@router.get("/{submission_id}", response_model=schemas.SubmissionOut)
def get_submission(submission_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    repo = SubmissionRepository(db)
    submission = repo.get_by_id(submission_id)
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")

    # your turn: if submission.user_id != current_user.id AND current_user is not admin -> 403
    # then: return submission
    if cast(int, submission.user_id) != cast(int,current_user.id) and not cast(bool, current_user.is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this submission")
    return submission