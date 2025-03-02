from data_access.user_repo import UserRepository

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()
    
    async def get_all_users(self):
        users = await self.user_repo.list_users()
        return users

    async def get_user_by_id(self, user_id):
        user_obj = await self.user_repo.get_user_by_id(user_id)
        return user_obj

    async def create_user(self, name, email):
        new_user_obj = await self.user_repo.create_user(name, email)
        return new_user_obj

    async def update_user(self, user_id, name, email):
        updated_user_obj = await self.user_repo.update_user(user_id, name, email)
        return updated_user_obj

# Create a singleton instance
user_service = UserService()

# Convenience functions that use the singleton instance
async def get_all_users():
    return await user_service.get_all_users()

async def get_user_by_id(user_id):
    return await user_service.get_user_by_id(user_id)

async def create_user(name, email):
    return await user_service.create_user(name, email)

async def update_user(user_id, name, email):
    return await user_service.update_user(user_id, name, email) 