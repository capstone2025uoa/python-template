from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.user_service import get_all_users, get_user_by_id, create_user as service_create_user, update_user as service_update_user

router = APIRouter()

class User(BaseModel):
    id: int
    name: str
    email: str

class UserCreate(BaseModel):
    name: str
    email: str

@router.get("/", response_model=list[User])
async def get_users():
    """
    Retrieve a list of all users.
    ---
    responses:
      200:
        description: A list of users.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              email:
                type: string
    """
    users = await get_all_users()
    return users

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    """
    Retrieve a user by ID.
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: The ID of the user to retrieve.
    responses:
      200:
        description: A user object.
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            email:
              type: string
      404:
        description: User not found.
        schema:
          type: object
          properties:
            error:
              type: string
    """
    user_serialized = await get_user_by_id(user_id)
    if user_serialized is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_serialized

@router.post("/", response_model=User, status_code=201)
async def create_user_endpoint(user: UserCreate):
    """
    Create a new user.
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
          required:
            - name
            - email
    responses:
      201:
        description: User created successfully.
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            email:
              type: string
    """
    new_user_serialized = await service_create_user(user.name, user.email)
    return new_user_serialized

@router.put("/{user_id}", response_model=User)
async def update_user_endpoint(user_id: int, user: UserCreate):
    """
    Update an existing user.
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: The ID of the user to update.
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
    responses:
      200:
        description: User updated successfully.
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            email:
              type: string
      404:
        description: User not found.
        schema:
          type: object
          properties:
            error:
              type: string
    """
    updated_user_serialized = await service_update_user(user_id, user.name, user.email)
    if updated_user_serialized is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user_serialized
