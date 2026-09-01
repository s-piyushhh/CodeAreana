from sqlalchemy.orm import Session
from apps import models


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> models.User | None:
        return self.db.query(models.User).filter(models.User.username == username).first()

    def get_by_username_or_email(self, username: str, email: str) -> models.User | None:
        return self.db.query(models.User).filter((models.User.username == username) | (models.User.email == email)).first()
    
    def create(self, user: models.User) -> models.User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user