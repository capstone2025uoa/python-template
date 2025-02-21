from sqlalchemy.orm import Session
from models.users import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, name: str, email: str) -> User:
        user = User(name=name, email=email)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
        
    def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()
    
    def list_users(self) -> list[User]:
        return self.db.query(User).all()
    
    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True
    
    def update_user(self, user_id: int, name: str, email: str) -> User:
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        user.name = name
        user.email = email
        self.db.commit()
        self.db.refresh(user)
        return user