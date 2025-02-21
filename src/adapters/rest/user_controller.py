from flask import Blueprint, request, jsonify
from services.user_service import get_all_users, get_user_by_id, create_user as service_create_user, update_user as service_update_user

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
def get_users():
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
    users = get_all_users()
    return jsonify(users)

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
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
    user_serialized = get_user_by_id(user_id)
    if user_serialized is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user_serialized)

@user_bp.route('/', methods=['POST'])
def create_user_endpoint():
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
    data = request.json
    name = data.get('name')
    email = data.get('email')
    new_user_serialized = service_create_user(name, email)
    return jsonify(new_user_serialized), 201

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user_endpoint(user_id):
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
    data = request.json
    name = data.get('name')
    email = data.get('email')
    updated_user_serialized = service_update_user(user_id, name, email)
    if updated_user_serialized is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(updated_user_serialized)
