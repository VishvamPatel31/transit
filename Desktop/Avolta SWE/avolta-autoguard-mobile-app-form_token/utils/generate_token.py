from flask import Flask
from database_files.database import *
from itsdangerous import BadSignature, URLSafeTimedSerializer as Serializer

app = Flask(__name__)

app.config['SECRET_KEY'] = 'abdc1234'

def verify_reset_token(token):
    # Create a serializer using your app's SECRET_KEY
    serializer = Serializer(app.config['SECRET_KEY'])

    try:
        # Deserialize and verify the token
        user_id = serializer.loads(token, salt=app.config['SECRET_KEY'], max_age=300)  # 300 seconds (5 minutes) expiration
        return user_id[0]
    except BadSignature:
        return None

def generate_token(user_id, expires_sec = 300):
    # Generate a secure token
    serializer = Serializer(app.config['SECRET_KEY'], expires_sec)
    token = serializer.dumps(user_id, salt=app.config['SECRET_KEY'])
    return token