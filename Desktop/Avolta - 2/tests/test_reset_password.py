import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import app

@pytest.fixture
def client():
    # test client
    with app.test_client() as client:
        yield client

def test_reset_password_success(client):
    # test data for resetting the password
    data = {
        "email": "test@example.com"
    }

    response = client.post('/reset_password', json=data)

    assert response.status_code == 200

    data = response.get_json()
    assert data['message'] == 'Reset email has been sent.'

def test_reset_password_user_not_found(client):
    # test data for resetting the password with a nonexistent email
    data = {
        "email": "nonexistent@example.com"
    }

    response = client.post('/reset_password', json=data)

    assert response.status_code == 404

    data = response.get_json()
    assert data['message'] == 'User not found'

def test_reset_password_email_send_failure(client):
    # test data for resetting the password with email send failure
    data = {
        "email": "test@example.com"
    }
    response = client.post('/reset_password', json=data)

    assert response.status_code == 500

    data = response.get_json()
    assert data['message'] == 'Failed to send reset email.'

if __name__ == '__main__':
    pytest.main()