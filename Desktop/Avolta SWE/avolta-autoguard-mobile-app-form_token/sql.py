import sqlite3
from flask import Flask
from bcrypt import checkpw
from utils.encryption_utils import encrypt_password
from database_files.database import *
import threading

app = Flask(__name__)

app.config['SECRET_KEY'] = 'abdc1234'




def register_user(dbobj: Database, email, password, first_name, last_name, birthdate, avolta_license, question1, answer1,  question2, answer2, question3, answer3 ): 
    try: 
        hashed_password = encrypt_password(password)

        ##creating dictionary to pass the parameters to the methods in database class##
        params = {'email':email,'password': hashed_password,'first_name': first_name,'last_name': last_name,'birthdate': birthdate,'avolta_license': avolta_license,'question1': question1,'answer1': answer1,'question2': question2,'answer2': answer2,'question3': question3,'answer3': answer3}
        table = 'users'
        
        ##Corresponding method call in database.py##
        return dbobj.create(params,table)    #Returns true if successfully registered. Else False.
    
    except sqlite3.IntegrityError:
        # This exception will occur if the username already exists in the database
        return False

                       
        
def authentication_check(dbobj: Database,email, password):
    data = []
    # Use parameterized queries to avoid SQL injection
    try:
        
        ##creating dictionary to pass the parameters to the methods in database class##
        params = {'email':email}
        table = 'users'

        ##Corresponding method call in database.py##
        data = dbobj.read(params,table)   ##Corresponding method call in database.py##

    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])

    # If no data is returned, then the email and password is incorrect (user does not exist)
    # else print id of the user
    if len(data) == 0:
        print("User not found")
        return False
    else:
        # Incorrectly indexed
        hashed_password = data[0][2]
        print("Entered: " + str(password.encode("utf-8")))
        print("Actual:" + str(hashed_password.encode("utf-8")))
        if checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
            return data[0][0]
        else:
            return False


def verify_user(dbobj: Database,email):
    try:

        ##creating dictionary to pass the parameters to the methods in database class##
        params = {'email':email}
        table = 'users'

        ##Corresponding method call in database.py##
        result = dbobj.read(params,table)
        return result[0] if len(result)!=0 else "" 
        
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])

