import sqlite3
from bcrypt import checkpw
from utils.login.password_utils import hash_password, check_password
from data_access.database import Database

# Method to create tables initially if not exists at the launch of the application.
def instantiate_user_tables(dbobj: Database):
    # Defining dictionary with the schema of users table#
    table_users = "users"
    columns_users = {'id': "INTEGER PRIMARY KEY",
                     'email': "TEXT UNIQUE",
                     'password': "TEXT",
                     'first_name': "TEXT",
                     'last_name': "TEXT",
                     'birthdate': "DATE",
                     'avolta_license': "INTEGER UNIQUE",
                     'question1': "INTEGER",
                     'answer1': "TEXT",
                     'question2': "INTEGER",
                     'answer2': "TEXT",
                     'question3': "INTEGER",
                     'answer3': "TEXT"}

    # defining dictionary with the schema of questions table
    table_questions = "questions"
    columns_questions = {'question_id': "INTEGER PRIMARY KEY",
                         'question': "TEXT"}

    try:
        dbobj.create_table(table_users, columns_users)
        dbobj.create_table(table_questions, columns_questions)
    except Exception as e:
        print("An error occurred while creating tables", e.args[0])


def register_user(dbobj: Database, params):
    try:
        # Hash the password from the provided params
        hashed_password = hash_password(params.get('password'))
        params['password'] = hashed_password  # Update the password in the params dictionary

        table = 'users'

        return dbobj.create(params, table)  # Returns true if successfully registered. Else False.

    except sqlite3.IntegrityError:
        # This exception will occur if the email already exists in the database
        return False


def authentication_check(dbobj: Database, email, password):
    data = []
    # Use parameterized queries to avoid SQL injection
    try:

        # creating dictionary to pass the parameters to the methods in data_access class##
        params = {'email': email}
        table = 'users'

        # Corresponding method call in data_access.py##
        data = dbobj.read(params, table)  # Corresponding method call in data_access.py##

    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])

    # If no data is returned, then the email and password is incorrect (user does not exist)
    # else print id of the user
    if len(data) == 0:
        print("User not found")
        return False
    else:
        hashed_password = data[0][2]
        if check_password(password, hashed_password):
            return data[0][0]
        else:
            return False

def verify_user(dbobj: Database, email):
    try:

        # creating dictionary to pass the parameters to the methods in data_access class##
        params = {'email': email}
        table = 'users'

        # Corresponding method call in data_access.py##
        result = dbobj.read(params, table)
        return result[0] if len(result)!=0 else ""

    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
