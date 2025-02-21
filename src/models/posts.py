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
