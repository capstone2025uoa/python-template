import unittest
import json
from flask import Flask
from unittest.mock import patch

# Import the blueprint from the controller
from adapters.rest.user_controller import user_bp

class UserControllerTestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        # Register the blueprint with a url prefix for testing
        app.register_blueprint(user_bp, url_prefix='/users')
        app.testing = True
        self.client = app.test_client()

    @patch('adapters.rest.user_controller.get_all_users')
    def test_get_users(self, mock_get_all_users):
        # Setup the return value for get_all_users
        user_list = [{"id": 1, "name": "Alice", "email": "alice@example.com"}]
        mock_get_all_users.return_value = user_list
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, user_list)

    @patch('adapters.rest.user_controller.get_user_by_id')
    def test_get_user_found(self, mock_get_user_by_id):
        # Setup the return value for an existing user
        user = {"id": 2, "name": "Bob", "email": "bob@example.com"}
        mock_get_user_by_id.return_value = user
        response = self.client.get('/users/2')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, user)

    @patch('adapters.rest.user_controller.get_user_by_id')
    def test_get_user_not_found(self, mock_get_user_by_id):
        # Setup the return value to simulate user not found
        mock_get_user_by_id.return_value = None
        response = self.client.get('/users/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data.get('error'), 'User not found')

    @patch('adapters.rest.user_controller.service_create_user')
    def test_create_user(self, mock_service_create_user):
        # Setup the return value for creating a new user
        new_user = {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
        mock_service_create_user.return_value = new_user
        payload = {"name": "Charlie", "email": "charlie@example.com"}
        response = self.client.post('/users/', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data, new_user)

    @patch('adapters.rest.user_controller.service_update_user')
    def test_update_user_found(self, mock_service_update_user):
        # Setup the return value for updating an existing user
        updated_user = {"id": 4, "name": "Diana", "email": "diana@example.com"}
        mock_service_update_user.return_value = updated_user
        payload = {"name": "Diana", "email": "diana@example.com"}
        response = self.client.put('/users/4', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, updated_user)

    @patch('adapters.rest.user_controller.service_update_user')
    def test_update_user_not_found(self, mock_service_update_user):
        # Simulate update failure when the user is not found
        mock_service_update_user.return_value = None
        payload = {"name": "Eve", "email": "eve@example.com"}
        response = self.client.put('/users/999', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data.get('error'), 'User not found')

if __name__ == '__main__':
    unittest.main()
