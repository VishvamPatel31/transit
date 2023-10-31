import sqlite3
from flask import Flask
from bcrypt import checkpw
from utils.encryption_utils import encrypt_password
from database_files.database import *
import threading
import csv

app = Flask(__name__)

app.config['SECRET_KEY'] = 'abdc1234'

#Method to create tables initially if not exists at the launch of the application.
def instantiate_user_tables(dbobj: Database):

    #Defining dictionary with the schema of users table#
    table_users="users"
    columns_users = {'id':"INTEGER PRIMARY KEY",
                     'email':"TEXT UNIQUE",
                     'password':"TEXT",
                     'first_name':"TEXT",
                     'last_name':"TEXT",
                     'birthdate':"DATE",
                     'avolta_license':"INTEGER UNIQUE",
                     'question1':"INTEGER",
                     'answer1':"TEXT",
                     'question2':"INTEGER",
                     'answer2':"TEXT",
                     'question3':"INTEGER",
                     'answer3':"TEXT"}
    
#defining dictionary with the schema of questions table
    table_questions = "questions"
    columns_questions = {'question_id': "INTEGER PRIMARY KEY", 
                         'question': "TEXT"}
    

    try:
        dbobj.create_table(table_users,columns_users)
        dbobj.create_table(table_questions,columns_questions)
    except Exception as e:
        print("An error occurred while creating tables",e.args[0])


def instantiate_vehicle_tables(dbobj: Database):

    # Creates table with brand names 
    car_schema = {
        'id': "INTEGER PRIMARY KEY",
        'brand': "TEXT"
    }

    dbobj.create_table('Car_Brands', car_schema)

    brand_names = [
    {'brand': 'Toyota'},
    {'brand': 'Chevy'},
    {'brand': 'Nissan'}
    ]

    for value in brand_names:
        dbobj.create(value,'Car_Brands')
    
    # Loops over each brand and creates individual tables
    Car_Brands = [
        'Toyota',
        'Nissan',
        'Chevy',
    ]

    model_schema ={
        'id': "INTEGER PRIMARY KEY",
        'model': "TEXT",
        'year': "INTEGER"
    }

    for brand in Car_Brands:
        model_table = f"{brand}_Cars"
        dbobj.create_table(model_table, model_schema)

def instantiate_read_csv(dbobj: Database):
    # reads a CSV file for input into models table
    with open('models.csv','r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            brand = row['brand']
            model = row['model']
            year = row['year']

            # Construct the table to insert data into thier respective brands
            model_table = f"{brand}_Cars"

            #Insert the data
            dbobj.create({'model':model, 'year':year},model_table)
            



