from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User
from sqlalchemy.future import select

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, name: str, email: str) -> User:
        user = User(name=name, email=email)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
        
    async def get_user_by_id(self, user_id: int) -> User:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()
    
    async def get_user_by_email(self, email: str) -> User:
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()
    
    async def list_users(self) -> list[User]:
        stmt = select(User)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def delete_user(self, user_id: int) -> bool:
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        await self.db.delete(user)
        await self.db.commit()
        return True
    
    async def update_user(self, user_id: int, name: str, email: str) -> User:
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        user.name = name
        user.email = email
        await self.db.commit()
        await self.db.refresh(user)
        return user