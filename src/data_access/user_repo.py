from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User
from sqlalchemy.future import select
from database.db import get_async_session

class UserRepository:
    def __init__(self):
        pass
        
    async def _get_db(self, read_only=True):
        """Get a database session"""
        return await get_async_session(read_only=read_only)

    async def create_user(self, name: str, email: str) -> User:
        async with await self._get_db(read_only=False) as db:
            user = User(name=name, email=email)
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user
        
    async def get_user_by_id(self, user_id: int) -> User:
        async with await self._get_db(read_only=True) as db:
            stmt = select(User).where(User.id == user_id)
            result = await db.execute(stmt)
            return result.scalars().first()
    
    async def get_user_by_email(self, email: str) -> User:
        async with await self._get_db(read_only=True) as db:
            stmt = select(User).where(User.email == email)
            result = await db.execute(stmt)
            return result.scalars().first()
    
    async def list_users(self) -> list[User]:
        async with await self._get_db(read_only=True) as db:
            stmt = select(User)
            result = await db.execute(stmt)
            return result.scalars().all()
    
    async def delete_user(self, user_id: int) -> bool:
        async with await self._get_db(read_only=False) as db:
            stmt = select(User).where(User.id == user_id)
            result = await db.execute(stmt)
            user = result.scalars().first()
            if not user:
                return False
            await db.delete(user)
            await db.commit()
            return True
    
    async def update_user(self, user_id: int, name: str, email: str) -> User:
        async with await self._get_db(read_only=False) as db:
            stmt = select(User).where(User.id == user_id)
            result = await db.execute(stmt)
            user = result.scalars().first()
            if not user:
                return None
            user.name = name
            user.email = email
            await db.commit()
            await db.refresh(user)
            return user