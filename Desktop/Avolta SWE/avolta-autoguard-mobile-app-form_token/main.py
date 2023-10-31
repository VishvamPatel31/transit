"""File containing the functions related to Flask API endpoints"""

from flask import Flask, request, jsonify, render_template, url_for
from sql import *  # Import the function from sql.py
from utils.generate_token import *  # Import the function from sql.py
from table_instantiation import *
from database_files.database import SqliteUserDatabase  # Import the SqliteDatabase class
from flask_mail import Mail, Message
import threading

app = Flask(__name__)
user_db = SqliteUserDatabase("user_db.db")
vehicle_db = SqliteUserDatabase("vehicle_db.db")


database_connections = threading.local()

def get_db():
    db = getattr(database_connections, 'db', None)
    if db is None:
        db = database_connections.db = SqliteUserDatabase("new_db.db")
    return db

instantiate_user_tables(user_db)
instantiate_vehicle_tables(vehicle_db)
instantiate_read_csv(vehicle_db)
# register_user(db, 'varun.divi@avoltacanada.com',
#               'avoltapassword321',
#               'Varun4',
#               'Divi4',
#               '1969-1-1',
#               '12345678',
#               'What is your favorite color?',
#               'yellow',
#               'What is your first car?',
#               'gtr',
#               'Where were you born?',
#               'va',)

# Configured flask mail settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # Gmail SMTP port
app.config['MAIL_USE_TLS'] = True  # Uses TLS for secure connection
app.config['MAIL_USERNAME'] = 'varundivi@gmail.com'
app.config['MAIL_PASSWORD'] = 'hunamytiijfqsmoy'
app.config['MAIL_DEFAULT_SENDER'] = 'varundivi@gmail.com'  # Your Gmail email address


mail = Mail(app)


@app.route("/", methods=["GET"])
def index():
    return render_template("home.html")


@app.route("/login", methods = ['GET'])
def login_entry():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    # db = get_db()
    email = request.form.get('email')
    password = request.form.get('password')

    result = authentication_check(user_db, email, password)
    
    if result:
        return jsonify({
            'message': 'User login successfully',
            'user_id': email
        })
    else:
        return jsonify({'error': 'User login failed'})


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    # db = get_db()
    data = request.json

    data = request.json
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    birthdate = data.get('birthdate')
    avolta_licence = data.get('avolta_licence')
    question1 = "First Car?"
    answer1 = data.get('answer1')
    question2 = "Favorite Color?"
    answer2 = data.get('answer2')
    question3 = "Birthplace?"
    answer3 = data.get('answer3')

    # Pass the retrieved values to the register_user function
    if register_user(user_db, email, password, first_name, last_name, birthdate, avolta_licence, question1, answer1, question2, answer2, question3, answer3):
        return jsonify({'message': 'User registered successfully'})
    else:
        return jsonify({'error': 'Username already exists'})



@app.route("/test/", methods=["GET","POST"])
def test():
    if request.method == 'GET':
        return "Got"
    elif request.method == 'POST':
        response = {
            "METHOD": "POST",
            "message": "hello",
        }
        return jsonify(response)
    else:
        return "not"



@app.route("/change_password/<token>", methods=["GET"])
def change_password(token):
    user_id = verify_reset_token(token)

    if user_id:
        # If token is valid, render a password reset form
        return render_template("reset_login.html", token=token)
    else:
        return jsonify({"message": "Invalid or expired token."}), 400



@app.route("/change_password/<token>", methods=["POST"])
def update_password(token): 
    # db = get_db()
    user_id = verify_reset_token(token)

    if user_id is None:
        return jsonify({"message": "Invalid or expired token. Please request a new password reset link."}), 400

    if user_id:
        new_password = request.form.get('new_password')
        hashed_password = encrypt_password(new_password)

        try: 
            user_db.cursor.execute("UPDATE users SET password = ? WHERE email = ?", (hashed_password, user_id))
            user_db.database.commit()
            return jsonify({"message": "Password changed successfully"}) 
        except Exception as e: 
            print(f"Error changing password: {str(e)}")
            return jsonify({"error": "Failed to change password"}), 500


@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    # db = get_db()
    if request.method == "GET":
        return render_template("reset_password.html")

    if request.method == "POST":
        email = request.form.get("email")
        user_id = verify_user(user_db, email)

        if user_id is not None:
            token = generate_token(user_id)

            # To be fixed
            reset_link = url_for("change_password", token=token, _external=True)

            subject = "Password Reset Request"
            message_body = f"Click the following link to reset your password: {reset_link}"

            try:
                msg = Message(subject=subject, body = message_body, sender= 'varundivitest@gmail.com', recipients= [email])
                mail.send(msg)
                return jsonify({"message": "Reset email has been sent."})
            except Exception as e:
                return jsonify({"message": f"Failed to send reset email: {e}"}), 500
        else:
            return jsonify({"message": "User not found."}), 404
       


if __name__ == "__main__":
    app.run(port=5000)
