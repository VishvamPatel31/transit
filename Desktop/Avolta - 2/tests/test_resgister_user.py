import pytest
import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import app

@pytest.fixture
def client():
    # Create a test client using the Flask application
    with app.test_client() as client:
        yield client

def test_register_user_success(client):
    # Define test data for registration
    data = {
        "email": "test@example.com",
        "password": "password123",
        "first_name": "John",
        "last_name": "Doe",
        "birthdate": "2000-01-01",
        "avolta_license": 12345,
        "question1": 1,
        "answer1": "Answer1",
        "question2": 2,
        "answer2": "Answer2",
        "question3": 3,
        "answer3": "Answer3"
    }

    # Send a POST request to the /register endpoint with the test data
    response = client.post('/register', json=data)

    # Check if the response status code is 200 (success)
    assert response.status_code == 200

    # Check the response JSON to ensure registration was successful
    data = response.get_json()
    assert data['message'] == 'User registered successfully'


def test_register_user_duplicate_email(client):
    # Define test data with an email that already exists in the database
    data = {
        "email": "test@gmail.com",
        "password": "password123",
        "first_name": "Jane",
        "last_name": "Smith",
        "birthdate": "1995-05-05",
        "avolta_license": 54321,
        "question1": 1,
        "answer1": "Answer1",
        "question2": 2,
        "answer2": "Answer2",
        "question3": 3,
        "answer3": "Answer3"
    }

    # Send a POST request to the /register endpoint with the test data
    response = client.post('/register', json=data)

    # Check if the response status code is 200 (success)
    assert response.status_code == 200

    # Check the response JSON to ensure registration failed due to duplicate email
    data = response.get_json()
    assert data['error'] == 'Username already exists'    

# Run the tests
if __name__ == '__main__':
    pytest.main()


