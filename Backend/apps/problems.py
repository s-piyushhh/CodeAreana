from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apps.auth import get_current_admin
from apps.database import get_db
from apps import schemas, models
from apps.repository.problem_repository import ProblemRepository

router = APIRouter(prefix="/problems", tags=["problems"])

@router.get("/", response_model=List[schemas.ProblemOut])
def list_problems(db: Session = Depends(get_db)):
    repo = ProblemRepository(db)
    return repo.get_all()


@router.get("/{problem_id}", response_model=schemas.ProblemOut)
def get_problem(problem_id: int, db: Session = Depends(get_db)):
    repo = ProblemRepository(db)
    problem = repo.get_by_id(problem_id)
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Problem not found")
    return problem


@router.post("/", response_model=schemas.ProblemOut, status_code=status.HTTP_201_CREATED)
def create_problem(
    problem_in: schemas.ProblemCreate,
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    problem = models.Problem(**problem_in.model_dump())
    repo = ProblemRepository(db)
    return repo.create(problem)


@router.delete("/{problem_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_problem(
    problem_id: int,
    db: Session = Depends(get_db),
    _admin: models.User = Depends(get_current_admin),
):
    repo = ProblemRepository(db)
    problem = repo.get_by_id(problem_id)
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Problem not found")
    repo.delete(problem)
    return None
