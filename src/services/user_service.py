from data_access.user_repo import UserRepository
from database.db import connect_to_database
from config import DATABASE_URL

SessionLocal = connect_to_database(DATABASE_URL)


def get_all_users():
    db = SessionLocal()
    try:
        user_repo = UserRepository(db)
        users = user_repo.list_users()
        return [{"id": user.id, "name": user.name, "email": user.email} for user in users]
    finally:
        db.close()


def get_user_by_id(user_id):
    db = SessionLocal()
    try:
        user_repo = UserRepository(db)
        user_obj = user_repo.get_user_by_id(user_id)
        if user_obj is None:
            return None
        return {"id": user_obj.id, "name": user_obj.name, "email": user_obj.email}
    finally:
        db.close()


def create_user(name, email):
    db = SessionLocal()
    try:
        user_repo = UserRepository(db)
        new_user_obj = user_repo.create_user(name, email)
        return {"id": new_user_obj.id, "name": new_user_obj.name, "email": new_user_obj.email}
    finally:
        db.close()


def update_user(user_id, name, email):
    db = SessionLocal()
    try:
        user_repo = UserRepository(db)
        updated_user_obj = user_repo.update_user(user_id, name, email)
        if updated_user_obj is None:
            return None
        return {"id": updated_user_obj.id, "name": updated_user_obj.name, "email": updated_user_obj.email}
    finally:
        db.close() 