from data_access.user_repo import UserRepository
from database.db import get_async_session


async def get_all_users():
    async with await get_async_session(read_only=True) as db:
        user_repo = UserRepository(db)
        users = await user_repo.list_users()
        return users


async def get_user_by_id(user_id):
    async with await get_async_session(read_only=True) as db:
        user_repo = UserRepository(db)
        user_obj = await user_repo.get_user_by_id(user_id)
        return user_obj


async def create_user(name, email):
    async with await get_async_session(read_only=False) as db:
        user_repo = UserRepository(db)
        new_user_obj = await user_repo.create_user(name, email)
        return new_user_obj


async def update_user(user_id, name, email):
    async with await get_async_session(read_only=False) as db:
        user_repo = UserRepository(db)
        updated_user_obj = await user_repo.update_user(user_id, name, email)
        return updated_user_obj 