import sqlite3

def view_database(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Display the contents of each table
    for table_name in tables:
        table_name = table_name[0]
        print(f"\nTable: {table_name}\n" + "-"*40)

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        print(', '.join(column_names))

        # Fetch and display rows
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    cursor.close()
    connection.close()

if __name__ == "__main__":
    db_name = input("Enter the name of the SQLite3 database you want to view: ")
    view_database(db_name)
