from data_access.user_repo import UserRepository
from database.db import get_session


def get_all_users():
    db = get_session(read_only=True)
    try:
        user_repo = UserRepository(db)
        users = user_repo.list_users()
        return [{"id": user.id, "name": user.name, "email": user.email} for user in users]
    finally:
        db.close()


def get_user_by_id(user_id):
    db = get_session(read_only=True)
    try:
        user_repo = UserRepository(db)
        user_obj = user_repo.get_user_by_id(user_id)
        if user_obj is None:
            return None
        return {"id": user_obj.id, "name": user_obj.name, "email": user_obj.email}
    finally:
        db.close()


def create_user(name, email):
    db = get_session(read_only=False)
    try:
        user_repo = UserRepository(db)
        new_user_obj = user_repo.create_user(name, email)
        return {"id": new_user_obj.id, "name": new_user_obj.name, "email": new_user_obj.email}
    finally:
        db.close()


def update_user(user_id, name, email):
    db = get_session(read_only=False)
    try:
        user_repo = UserRepository(db)
        updated_user_obj = user_repo.update_user(user_id, name, email)
        if updated_user_obj is None:
            return None
        return {"id": updated_user_obj.id, "name": updated_user_obj.name, "email": updated_user_obj.email}
    finally:
        db.close() 