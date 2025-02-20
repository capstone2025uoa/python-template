from flask import Blueprint, request, jsonify
from data.mock import MOCK_USERS

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
def get_users():
    return jsonify(MOCK_USERS)

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in MOCK_USERS if user['id'] == user_id), None)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

@user_bp.route('/', methods=['POST'])
def create_user():
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
    data = request.json
