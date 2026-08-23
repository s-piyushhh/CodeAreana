from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
from apps.models import DifficultyLevel, SubmissionStatus


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    is_admin: bool
    created_at: datetime


class ProblemCreate(BaseModel):
    title: str
    description: str
    difficulty: DifficultyLevel
    sample_input: str
    sample_output: str
    test_input: str
    expected_output: str


class ProblemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    difficulty: DifficultyLevel
    sample_input: str
    sample_output: str
    created_at: datetime


class SubmissionCreate(BaseModel):
    problem_id: int
    code: str
    language: str


class SubmissionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    problem_id: int
    output: Optional[str] = None
    code: str
    submitted_at: datetime
    status: SubmissionStatus
