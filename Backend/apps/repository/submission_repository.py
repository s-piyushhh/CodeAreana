from sqlalchemy.orm import Session
from apps import models

class SubmissionRepository:
    def __init__(self, db):
        self.db = db
    
    def get_by_id(self, submission_id: int) -> models.Submission | None:
        return self.db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    
    def get_by_user(self, user_id: int) -> list[models.Submission]:
        return self.db.query(models.Submission).filter(models.Submission.user_id == user_id).all()
    
    def create(self, submission: models.Submission) -> models.Submission:
        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)
        return submission