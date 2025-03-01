# This project uses the ORM models as the domain models. For simple business logic, this is fine.
# If your business logic is more complex, it's better to have separate domain models.
# For simplicity, we'll use the ORM models as the domain models here.
# Ask abc123 to refactor this if you need separate domain models.

from sqlalchemy import Column, Integer, String, ForeignKey
from .base_class import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))  # many posts -> one user

    def __repr__(self):
        return f"<Post id={self.id} title={self.title}>"
