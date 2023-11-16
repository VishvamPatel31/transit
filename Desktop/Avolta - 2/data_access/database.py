"""Contains the classes for data_access functionality."""

from typing import Any
import sqlite3


class Database:
    """Abstract class representing a data_access function."""

    def read(self, params: dict, table: str) -> Any:
        """Given the lookup parameters, return the resulting value from the data_access in the matching table
        and return the result"""

        raise NotImplementedError

    def create(self, inputs: dict, table: str) -> bool:
        """Given the input parameters, create a new entry in the data_access from the data_access in the
        matching table and return a boolean based on the result"""

        raise NotImplementedError

    def update(self, old_params: dict, new_params: dict, table: str) -> bool:
        """Given the lookup parameters, find the old value in the matching table and update it with
        the new value and return a
        boolean based on the result"""

        raise NotImplementedError

    def delete(self, params: dict, table: str) -> bool:
        """Given the lookup parameters, return the matching value from the data_access in the matching table
        and return a boolean based on the result"""

        raise NotImplementedError

    def _check_table(self, name: str) -> bool:
        """Hidden method to be used to check if a table exists in this data_access"""

        raise NotImplementedError

    def create_table(self, name: str, columns: dict):
        """Hidden method to be used before doing any data_access work, if the table that is needed
        does not exist then create it"""

        raise NotImplementedError


class SqliteDatabase(Database):

    def __init__(self, name: str):
        # Initialize the connection name
        self.name = name

    def _check_table(self, name: str) -> bool:
        # Hidden method to be used to check if a table exists in this data_access
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        with sqlite3.connect(self.name) as database:
            cursor = database.cursor()
            cursor.execute(query, (name,))
            return bool(cursor.fetchone())

    def read(self, params: dict, table: str) -> Any:
        # Check if the specified table exists in the data_access
        if not self._check_table(table):
            print(f"Table '{table}' does not exist.")
            return None

        # Construct the SQL query to retrieve data based on parameters
        query = f"SELECT * FROM {table} WHERE "
        conditions = []
        values = []

        for key, value in params.items():
            conditions.append(f"{key} = ?")
            values.append(value)

        query += " AND ".join(conditions)
        with sqlite3.connect(self.name) as database:
            cursor = database.cursor()
            cursor.execute(query, tuple(values))
            result = cursor.fetchall()
        return result

    def create(self, inputs: dict, table: str) -> bool:
        # Check if the specified table exists in the data_access
        if not self._check_table(table):
            print(f"Table '{table}' does not exist.")
            return False

        # Prepare the query to insert data into the table
        keys = ", ".join(inputs.keys())
        placeholders = ", ".join(["?" for _ in inputs])
        values = tuple(inputs.values())

        query = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"
        try:
            # Execute the query and commit the transaction

            with sqlite3.connect(self.name) as database:
                cursor = database.cursor()
                cursor.execute(query, values)
                database.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update(self, old_params: dict, new_params: dict, table: str) -> bool:
        # Check if the specified table exists in the data_access
        if not self._check_table(table):
            print(f"Table '{table}' does not exist.")
            return False

        # Prepare the query to update data in the table
        update_conditions = []
        update_values = []

        for key, value in new_params.items():
            update_conditions.append(f"{key} = ?")
            update_values.append(value)

        where_conditions = []
        where_values = []

        for key, value in old_params.items():
            where_conditions.append(f"{key} = ?")
            where_values.append(value)

        query = f"UPDATE {table} SET {', '.join(update_conditions)} WHERE {' AND '.join(where_conditions)}"
        try:
            # Execute the query and commit the transaction

            with sqlite3.connect(self.name) as database:
                cursor = database.cursor()
                cursor.execute(query, tuple(update_values + where_values))
                database.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def delete(self, params: dict, table: str) -> bool:
        # Check if the specified table exists in the data_access
        if not self._check_table(table):
            print(f"Table '{table}' does not exist.")
            return False

        # Prepare the query to delete data from the table
        conditions = []
        values = []

        for key, value in params.items():
            conditions.append(f"{key} = ?")
            values.append(value)

        query = f"DELETE FROM {table} WHERE {' AND '.join(conditions)}"
        try:
            # Execute the query and commit the transaction
            with sqlite3.connect(self.name) as database:
                cursor = database.cursor()
                cursor.execute(query, tuple(values))
                database.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def create_table(self, name: str, columns: dict):
        # Construct the column definitions for the table
        column_definitions = ', '.join([f"{col} {data_type}" for col, data_type in columns.items()])

        # Prepare the query to create the table if it doesn't exist
        query = f"CREATE TABLE IF NOT EXISTS {name} ({column_definitions})"

        # Execute the query and commit the transaction
        try:

            with sqlite3.connect(self.name) as database:
                cursor = database.cursor()
                cursor.execute(query)
                database.commit()
            return True
        except sqlite3.IntegrityError:
            return False
