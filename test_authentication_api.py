import unittest
from unittest.mock import patch
from auth_module import authenticate_user, get_facebook_user, get_google_user

class TestAuthenticationAPI(unittest.TestCase):

    @patch('app.auth_module.requests.post')  # Update this line with the correct module path
    def test_authenticate_user_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'token': 'fake_token'}
        response = authenticate_user('test_user', 'test_password')
        self.assertEqual(response['token'], 'fake_token')

    @patch('app.auth_module.requests.post')  # Update this line with the correct module path
    def test_authenticate_user_failure(self, mock_post):
        mock_post.return_value.status_code = 401
        response = authenticate_user('test_user', 'wrong_password')
        self.assertIsNone(response)

    @patch('app.auth_module.requests.get')  # Update this line with the correct module path
    def test_get_facebook_user_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'id': '12345', 'name': 'Test User'}
        response = get_facebook_user('fake_token')
        self.assertEqual(response['id'], '12345')
        self.assertEqual(response['name'], 'Test User')

    @patch('app.auth_module.requests.get')  # Update this line with the correct module path
    def test_get_facebook_user_failure(self, mock_get):
        mock_get.return_value.status_code = 401
        response = get_facebook_user('fake_token')
        self.assertIsNone(response)

    @patch('app.auth_module.requests.get')  # Update this line with the correct module path
    def test_get_google_user_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'sub': '12345', 'name': 'Test User'}
        response = get_google_user('fake_token')
        self.assertEqual(response['sub'], '12345')
        self.assertEqual(response['name'], 'Test User')

    @patch('app.auth_module.requests.get')  # Update this line with the correct module path
    def test_get_google_user_failure(self, mock_get):
        mock_get.return_value.status_code = 401
        response = get_google_user('fake_token')
        self.assertIsNone(response)

if __name__ == '__main__':
    unittest.main()