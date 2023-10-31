"""Contains the classes for database functionality."""

from typing import Any
import sqlite3

class Database():
    """Abstract class representing a database function."""

    def read(self, params: dict, table: str) -> Any:
        """Given the lookup parameters, return the resulting value from the database in the matching table
        and return the result"""

        raise NotImplementedError

    def create(self, inputs: dict, table: str) -> bool:
        """Given the input parameters, create a new entry in the database from the database in the
        matching table and return a boolean based on the result"""
       
        raise NotImplementedError

    def update(self, old_params: dict, new_params: dict, table: str) -> bool:
        """Given the lookup parameters, find the old value in the matching table and update it with
        the new value and return a
        boolean based on the result"""

        raise NotImplementedError

    def delete(self, params: dict, table: str) -> bool:
        """Given the lookup parameters, return the matching value from the database in the matching table
        and return a boolean based on the result"""
        
        raise NotImplementedError

    def _check_table(self, name: str) -> bool:
        """Hidden method to be used to check if a table exists in this database"""

        raise NotImplementedError

    def create_table(self, name: str):
        """Hidden method to be used before doing any database work, if the table that is needed
        does not exist then create it"""

        raise NotImplementedError


class SqliteUserDatabase(Database):

    def __init__(self, name: str):
        # Initialize the SQLite database connection and cursor
        self.db_name = name

    def _connect(self):
        return sqlite3.connect(self.db_name)

    # TODO: implement the other methods

    def _check_table(self, name: str) -> bool:
        with self._connect() as conn:
            cursor = conn.cursor()
            query = f"SELECT name FROM sqlite_master WHERE type='table' AND name=?"
            cursor.execute(query, (name,))
            return bool(cursor.fetchone())

    def read(self, params: dict, table: str) -> Any:
        with self._connect() as conn:
            cursor = conn.cursor()
            if not self._check_table(table):
                print(f"Table '{table}' does not exist.")
                return None

            query = f"SELECT * FROM {table} WHERE "
            conditions, values = [], []
            for key, value in params.items():
                conditions.append(f"{key} = ?")
                values.append(value)

            query += " AND ".join(conditions)
            return cursor.execute(query, tuple(values)).fetchall()

    def create(self, inputs: dict, table: str) -> bool:
        with self._connect() as conn:
            cursor = conn.cursor()
            if not self._check_table(table):
                print(f"Table '{table}' does not exist.")
                return False

            keys = ", ".join(inputs.keys())
            placeholders = ", ".join(["?" for _ in inputs])
            values = tuple(inputs.values())
            query = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"
            try:
                cursor.execute(query, values)
                return True
            except sqlite3.IntegrityError:
                return False
     

    def update(self, old_params: dict, new_params: dict, table: str) -> bool:
        with self._connect() as conn:
            cursor = conn.cursor()
            if not self._check_table(table):
                print(f"Table '{table}' does not exist.")
                return False

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
                cursor.execute(query, tuple(update_values + where_values))
                return True
            except sqlite3.IntegrityError:
                return False

    def delete(self, params: dict, table: str) -> bool:
        with self._connect() as conn:
            cursor = conn.cursor()
            if not self._check_table(table):
                print(f"Table '{table}' does not exist.")
                return False

            conditions = []
            values = []

            for key, value in params.items():
                conditions.append(f"{key} = ?")
                values.append(value)

            query = f"DELETE FROM {table} WHERE {' AND '.join(conditions)}"
            try:
                cursor.execute(query, tuple(values))
                return True
            except sqlite3.IntegrityError:
                return False
        
    def create_table(self, name: str, columns: dict):
        with self._connect() as conn:
            cursor = conn.cursor()
            column_definitions = ', '.join([f"{col} {data_type}" for col, data_type in columns.items()])
            query = f"CREATE TABLE IF NOT EXISTS {name} ({column_definitions})"
            cursor.execute(query)

    def insert_data(self, table_name:str , values:dict):
        with self._connect() as conn:
            cursor = conn.cursor()
            columns = ','.join(values.keys())
            placeholders = ','.join(['?' for _ in values])
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, list(values.values()))
            

    