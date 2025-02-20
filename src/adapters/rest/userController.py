from flask import Blueprint, request, jsonify
from data.mock import MOCK_USERS

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
              role:
                type: string
    """
    return jsonify(MOCK_USERS)

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
            role:
              type: string
      404:
        description: User not found.
        schema:
          type: object
          properties:
            error:
              type: string
    """
    user = next((user for user in MOCK_USERS if user['id'] == user_id), None)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

@user_bp.route('/', methods=['POST'])
def create_user():
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
            role:
              type: string
          required:
            - name
            - role
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
            role:
              type: string
    """
    data = request.json
    new_user = {
        'id': len(MOCK_USERS) + 1,
        'name': data.get('name'),
        'role': data.get('role')
    }
    MOCK_USERS.append(new_user)
    return jsonify(new_user), 201

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
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
            role:
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
            role:
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
    user = next((user for user in MOCK_USERS if user['id'] == user_id), None)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    user['name'] = data.get('name', user['name'])
    user['role'] = data.get('role', user['role'])
    return jsonify(user)
