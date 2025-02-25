import pytest

from src.services.user_service import get_all_users
import src.database.db as db


class DummySession:
    async def __aenter__(self):
        return 'dummy_db'

    async def __aexit__(self, exc_type, exc, tb):
        pass


class DummyUserRepo:
    def __init__(self, db):
        self.db = db

    async def list_users(self):
        return ['user1', 'user2']


@pytest.fixture(autouse=True)
def patch_db_and_repo(monkeypatch):
    # Patch get_async_session to return our dummy session
    monkeypatch.setattr(db, 'get_async_session', lambda read_only: DummySession())
    # Patch UserRepository in user_service to use our dummy repo
    monkeypatch.setattr('src.services.user_service.UserRepository', DummyUserRepo)


@pytest.mark.asyncio
async def test_get_all_users():
    users = await get_all_users()
    assert users == ['user1', 'user2'] 