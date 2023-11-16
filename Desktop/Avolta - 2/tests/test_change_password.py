# test_app.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import app
import json

#The method checks if change password is successful. (Upon providing valid userid)
def test_change_password():
    with app.test_client() as client:
        data = {"new_password": "new_password"}
        valid_userid = 1
        response = client.post(f'/change_password/{valid_userid}', json=data)

        assert response.status_code == 200, f"Test Failed. Response code received: {response.status_code}"
        response_data = json.loads(response.data.decode('utf-8'))
        assert response_data['message'] == 'Password changed successfully', f"Test Failed. Received message: {response_data['message']}"


#The method checks if we are receiving error code 404 if an invalid userid is passed.
def test_change_password_failure():
     with app.test_client() as client:
        data = {"new_password": "new_password"}
        response = client.post('/change_password/abcdef', json=data)  #invalid userid which is not available in the database

        assert response.status_code == 400, 'Test Failed'





if __name__ == '__main__':
    app.run()
