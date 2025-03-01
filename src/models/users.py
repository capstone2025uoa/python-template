# This project uses the ORM models as the domain models. For simple business logic, this is fine.
# If your business logic is more complex, it's better to have separate domain models.
# For simplicity, we'll use the ORM models as the domain models here.
# Ask abc123 to refactor this if you need separate domain models.

from sqlalchemy import Column, Integer, String
from .base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<User id={self.id} name={self.name} email={self.email}>"
