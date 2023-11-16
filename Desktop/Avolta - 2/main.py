"""File containing the functions related to Flask API endpoints"""

from flask import Flask, render_template, request, jsonify
from data_access.database import SqliteDatabase
from data_access.login.user_sql import *
from utils.login.token_utils import verify_reset_token, send_mail
from utils.login.flask_utils import login_flask_setup

app = Flask(__name__, template_folder="webpages/templates")
login_flask_setup(app)

users_db = SqliteDatabase("users.db")

# Initilizes tables if not already made
instantiate_user_tables(users_db)


@app.route("/", methods=["GET"])
def index():
    return render_template("home.html")


@app.route("/login", methods=['GET'])
def login_entry():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    data = request.json  # Get JSON data sent from the client
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'error': 'Missing email or password'}), 400

    result = authentication_check(users_db, email, password)

    if result:
        return jsonify({
            'message': 'User login successfully',
            'user_id': result
        })
    else:
        return jsonify({'error': 'User login failed'}), 401


@app.route("/register", methods=["GET"])
def register_get():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_post():
    data = request.json
    registration_params = {
        'email',
        'password',
        'first_name',
        'last_name',
        'birthdate',
        'avolta_license',
        'question1',
        'answer1',
        'question2',
        'answer2',
        'question3',
        'answer3'
    }

    # Empty Dictionary for storing the retrieved data values
    extracted_values = {}

    # Extract values from data using the field mapping
    for param in registration_params:
        extracted_values[param] = data.get(param)

    # Passing the extracted values to the register_user function
    if register_user(users_db, extracted_values):
        return jsonify({'message': 'User registered successfully'})
    else:
        return jsonify({'error': 'Username already exists'})


@app.route("/change_password/<token>", methods=["GET"])
def change_password(token):
    user_id = verify_reset_token(app, token)

    if user_id:
        # If token is valid, render a password reset form
        return render_template("reset_login.html", token=token)
    else:
        return jsonify({"message": "Invalid or expired token."}), 400


@app.route("/change_password/<token>", methods=["POST"])
def update_password(token):
    user_id = verify_reset_token(app, token)

    if user_id is None:
        return jsonify({"message": "Invalid or expired token. Please request a new password reset link."}), 400

    if user_id:
        try:
            new_password = request.form.get('new_password')
            hashed_password = hash_password(new_password)
            # users_db.cursor.execute("UPDATE users SET password = ? WHERE email = ?", (hashed_password, user_id))
            # users_db.database.commit()
            return jsonify({"message": "Password changed successfully"})
        except Exception as e:
            print(f"Error changing password: {str(e)}")
            return jsonify({"error": "Failed to change password"}), 500


@app.route("/reset_password", methods=["GET"])
def reset_password_get():
    return render_template("reset_password.html")


@app.route("/reset_password", methods=["POST"])
def reset_password_post():
    email = request.form.get("email")
    
    params = {'email':email}
    table = 'users'

    ##Corresponding method call in database.py##
    result = users_db.read(params,table)
    user_id = result[0] if len(result)!=0 else None


    if user_id is not None:
        return send_mail(app, user_id, email)
    else:
        return jsonify({"message": "User not found."}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
