# type: ignore[import]
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship  # type: ignore[import]
from datetime import datetime
import enum
from apps.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # one User -> many Submissions
    submissions = relationship("Submission", back_populates="user")


class DifficultyLevel(str, enum.Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(Enum(DifficultyLevel),
                        default=DifficultyLevel.EASY, nullable=False)

    # sample input/output shown to the user on the problem page
    sample_input = Column(Text, nullable=True)
    sample_output = Column(Text, nullable=True)

    # hidden test case used to actually judge submissions (kept simple for now:
    # one input -> one expected output per problem)
    test_input = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # one Problem -> many Submissions
    submissions = relationship("Submission", back_populates="problem")


class SubmissionStatus(str, enum.Enum):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    WRONG_ANSWER = "Wrong Answer"
    RUNTIME_ERROR = "Runtime Error"


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)

    # foreign keys -> this is what makes the relationship() calls above work
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)

    code = Column(Text, nullable=False)
    language = Column(String, default="python")
    status = Column(Enum(SubmissionStatus), default=SubmissionStatus.PENDING)
    output = Column(Text, nullable=True)

    submitted_at = Column(DateTime, default=datetime.utcnow)

    # back-references so submission.user and submission.problem work directly
    user = relationship("User", back_populates="submissions")
    problem = relationship("Problem", back_populates="submissions")
