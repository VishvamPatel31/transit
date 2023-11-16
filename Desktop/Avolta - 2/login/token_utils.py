from itsdangerous import BadSignature, URLSafeTimedSerializer as Serializer
from flask import url_for, jsonify, Flask
from flask_mail import Mail, Message


def verify_reset_token(app, token):
    with app.app_context():
        # Create a serializer using your app's SECRET_KEY
        serializer = Serializer(app.config['SECRET_KEY'])

        try:
            # Deserialize and verify the token
            user_id = serializer.loads(token, salt=app.config['SECRET_KEY'], max_age=600)  # 600 seconds (10 minutes) expiration
            return user_id[0]
        except BadSignature:
            return None


def generate_token(app, user_id, expires_sec=300):
    with app.app_context():
        # Generate a secure token
        serializer = Serializer(app.config['SECRET_KEY'], expires_sec)
        token = serializer.dumps(user_id, salt=app.config['SECRET_KEY'])
        return token



def send_mail(app: Flask, user_id, email):
    with app.app_context():

        mail = Mail(app)

        token = generate_token(app, user_id)

        # To be fixed
        reset_link = url_for("change_password", token=token, _external=True)

        subject = "Password Reset Request"
        message_body = f"Click the following link to reset your password: {reset_link}"

        try:
            msg = Message(subject=subject, body=message_body, sender='varundivitest@gmail.com', recipients=[email])
            mail.send(msg)
            return jsonify({"message": "Reset email has been sent."})
        except Exception as e:
            return jsonify({"message": f"Failed to send reset email: {e}"}), 500
