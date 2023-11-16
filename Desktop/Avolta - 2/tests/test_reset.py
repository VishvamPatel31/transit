import pytest
import pytest
import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import app, jsonify  # Import your Flask app from 'main.py'


@pytest.fixture
def client():
    with app.app_context():  # Push the app context for mail sending
        with app.test_client() as client:
            yield client

def test_reset_password_get(client):
    # Send a GET request to the /reset_password endpoint
    response = client.get('/reset_password')

    # Check if the response status code is 200 (success)
    assert response.status_code == 200

# Use the patch decorator to replace the 'verify_user' and 'send_mail' functions with mocks
def test_reset_password_post_success(client):
    # Send a POST request to the /reset_password endpoint with test email
    response = client.post('/reset_password', data={"email": "test@gmail.com"})

    # Check if the response status code is 200 (success)
    assert response.status_code == 200

    # Check the response JSON to ensure the reset email was sent
    data = response.get_json()
    assert data['message'] == 'Reset email has been sent.'

def test_reset_password_post_user_not_found(client):
    # Send a POST request to the /reset_password endpoint with test email
    response = client.post('/reset_password', data={"email": "nonexistent@gmail.com"})

    # Check if the response status code is 404 (Not Found)
    assert response.status_code == 404

    # Check the response JSON to ensure the user was not found
    data = response.get_json()
    assert data['message'] == 'User not found.'

if __name__ == '__main__':
    pytest.main()
