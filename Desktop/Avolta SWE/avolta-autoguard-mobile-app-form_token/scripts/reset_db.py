import sqlite3

def reset_database(db_name):
    # Connect to the database
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Fetch the list of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Drop each table
    for table_name in tables:
        drop_table_query = f"DROP TABLE {table_name[0]}"
        cursor.execute(drop_table_query)

    # Close the database connection
    cursor.close()
    connection.close()

if __name__ == "__main__":
    db_name = input("Enter the name of the SQLite3 database you want to reset: ")
    reset_database(db_name)
    print(f"The database '{db_name}' has been reset.")
