from sqlalchemy.orm import Session
from apps import models


class ProblemRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, problem_id: int) -> models.Problem | None:
        return self.db.query(models.Problem).filter(models.Problem.id == problem_id).first()
        
    def get_all(self) -> list[models.Problem]:
        return self.db.query(models.Problem).all()

    def create(self, problem: models.Problem) -> models.Problem:
        # your code here — remember: add, commit, refresh, return
        self.db.add(problem)
        self.db.commit()
        self.db.refresh(problem)
        return problem