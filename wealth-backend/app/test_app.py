import sys
sys.path.append('C:/Users/nerve/Desktop/WealthWarden/wealth-backend')
from config import TestingConfig
from app import create_app, db
from app.models import User, Account
import json
import unittest

class WealthWardenTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_registration(self):
        response = self.client.post('/register', json={
            'email': 'test@example.com',
            'password': 'test'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', response.get_data(as_text=True))

    def test_user_registration_duplicate_email(self):
        self.client.post('/register', json={
            'email': 'test@example.com',
            'password': 'test'
        })
        response = self.client.post('/register', json={
            'email': 'test@example.com',
            'password': 'test2'
        })
        self.assertEqual(response.status_code, 409)

    def test_user_login(self):
        self.client.post('/register', json={
            'email': 'login@example.com',
            'password': 'login'
        })
        response = self.client.post('/login', json={
            'email': 'login@example.com',
            'password': 'login'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.get_data(as_text=True))

    def test_account_creation(self):
        # Register a new user
        self.client.post('/register', json={
            'email': 'account_test@example.com',
            'password': 'testpassword'
        })

        # Log in to get the access token
        login_response = self.client.post('/login', json={
            'email': 'account_test@example.com',
            'password': 'testpassword'
        })
        data = json.loads(login_response.get_data(as_text=True))
        access_token = data['access_token']

        # Use the token to create a new account
        response = self.client.post('/account', 
                                    json={'account_type': 'savings'},
                                    headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Account created successfully', response.get_data(as_text=True))

# Additional tests for other routes and error cases can be added here

if __name__ == '__main__':
    unittest.main()