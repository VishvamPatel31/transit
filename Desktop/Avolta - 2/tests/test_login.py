from main import app
import pytest
import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


@pytest.fixture
def client():
    # Create a test client using the Flask application
    with app.test_client() as client:
        yield client


def test_login_success(client):
    # Define test data for a successful login
    data = {
        "email": "test@example.com",
        "password": "password123"
    }

    # Assuming we have previously registered this user, test login
    # Send a POST request to the /login endpoint with the test data
    response = client.post('/login', json=data)

    # Check if the response status code is 200 (success)
    assert response.status_code == 200

    # Check the response JSON to ensure login was successful
    data = response.get_json()
    assert data['message'] == 'User login successfully'


def test_login_missing_credentials(client):
    # Define test data with missing credentials
    data = {
        "email": "test@example.com"
    }

    # Send a POST request to the /login endpoint with missing password
    response = client.post('/login', json=data)

    # Check if the response status code is 400 (Bad Request)
    assert response.status_code == 400

    # Check the response JSON to ensure an error message is returned
    data = response.get_json()
    assert 'error' in data


def test_login_invalid_credentials(client):
    # Define test data with invalid credentials
    data = {
        "email": "test@example.com",
        "password": "incorrect_password"
    }

    # Send a POST request to the /login endpoint with incorrect password
    response = client.post('/login', json=data)

    # Check if the response status code is 401 (Unauthorized)
    assert response.status_code == 401

    # Check the response JSON to ensure login failed
    data = response.get_json()
    assert 'error' in data


# Run the tests
if __name__ == '__main__':
    pytest.main()
