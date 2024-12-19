import sqlite3
from pathlib import Path

def connect_db():
    """Connects to the SQLite database."""
    DB_FILENAME = Path(__file__).parent.parent / "data" / "sandra.db"
    db_already_exists = DB_FILENAME.exists()

    conn = sqlite3.connect(DB_FILENAME)
    db_was_just_created = not db_already_exists
    return conn, db_was_just_created

def initialize_db(conn):
    """Initializes the database with tables and default data."""
    cursor = conn.cursor()

    # Create necessary tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS energy_storage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            technology TEXT,
            capacity REAL,
            efficiency REAL,
            status TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS real_time_monitoring (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parameter TEXT,
            value REAL,
            unit TEXT,
            timestamp TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sector TEXT,
            description TEXT,
            impact TEXT
        )
    """)

    conn.commit()

def load_table(conn, table_name):
    """Loads data from a specific table in the database."""
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    return data, columns

"""
Database management module for the SANDRA Streamlit app.

This module handles all interactions with the SQLite database, including
connection, initialization, data insertion, retrieval, updating, and deletion.
"""

import sqlite3
from pathlib import Path


def connect_db(db_name="sandra.db"):
    """
    Establish a connection to the SQLite database.

    Parameters:
        db_name (str): The name of the database file.

    Returns:
        sqlite3.Connection: A connection object to the SQLite database.
    """
    db_path = Path(__file__).parent / db_name
    conn = sqlite3.connect(db_path)
    return conn


def initialize_db(conn):
    """
    Initialize the database with required tables.

    Parameters:
        conn (sqlite3.Connection): A connection object to the SQLite database.
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sandra (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feature TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()


def insert_data(conn, feature, description, status):
    """
    Insert a new record into the database.

    Parameters:
        conn (sqlite3.Connection): A connection object to the SQLite database.
        feature (str): The feature name.
        description (str): A description of the feature.
        status (str): The status of the feature (e.g., "active", "inactive").
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO sandra (feature, description, status)
        VALUES (?, ?, ?)
        """,
        (feature, description, status),
    )
    conn.commit()


def fetch_data(conn):
    """
    Retrieve all records from the database.

    Parameters:
        conn (sqlite3.Connection): A connection object to the SQLite database.

    Returns:
        list of tuples: A list of all records in the database.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sandra")
    records = cursor.fetchall()
    return records


def update_data(conn, record_id, feature=None, description=None, status=None):
    """
    Update an existing record in the database.

    Parameters:
        conn (sqlite3.Connection): A connection object to the SQLite database.
        record_id (int): The ID of the record to update.
        feature (str): The new feature name (optional).
        description (str): The new description (optional).
        status (str): The new status (optional).
    """
    cursor = conn.cursor()
    updates = []
    parameters = []

    if feature:
        updates.append("feature = ?")
        parameters.append(feature)
    if description:
        updates.append("description = ?")
        parameters.append(description)
    if status:
        updates.append("status = ?")
        parameters.append(status)

    parameters.append(record_id)

    query = f"UPDATE sandra SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, parameters)
    conn.commit()


def delete_data(conn, record_id):
    """
    Delete a record from the database.

    Parameters:
        conn (sqlite3.Connection): A connection object to the SQLite database.
        record_id (int): The ID of the record to delete.
    """
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sandra WHERE id = ?", (record_id,))
    conn.commit()


if __name__ == "__main__":
    # For testing purposes
    connection = connect_db()
    initialize_db(connection)
    print("Database initialized.")
    connection.close()


import sqlite3

# Connect to the SQLite database
def connect_db():
    conn = sqlite3.connect('data/sandra.db')
    return conn

# Function to update data in the database
def update_data(id, new_value):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Example: Update a record with the given ID
    cursor.execute("UPDATE table_name SET column_name = ? WHERE id = ?", (new_value, id))
    
    # Commit and close the connection
    conn.commit()
    conn.close()

# Function to retrieve data from the database
def get_data():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM table_name")
    data = cursor.fetchall()
    
    conn.close()
    return data
import sqlite3

# Connect to the SQLite database
def connect_db():
    conn = sqlite3.connect('data/sandra.db')
    return conn

# Function to create a table
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS table_name (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            column1 TEXT,
            column2 INTEGER,
            column3 REAL
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert data into the table
def insert_data(column1, column2, column3):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO table_name (column1, column2, column3) 
        VALUES (?, ?, ?)
    ''', (column1, column2, column3))
    conn.commit()
    conn.close()

# Function to retrieve data from the table
def get_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM table_name")
    data = cursor.fetchall()
    conn.close()
    return data

# Function to update data in the table
def update_data(id, column1, column2, column3):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE table_name
        SET column1 = ?, column2 = ?, column3 = ?
        WHERE id = ?
    ''', (column1, column2, column3, id))
    conn.commit()
    conn.close()

# Function to delete data from the table
def delete_data(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM table_name WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# Function to commit changes (for transactional purposes)
def commit_changes():
    conn = connect_db()
    conn.commit()
    conn.close()

# Function to drop a table
def drop_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS table_name")
    conn.commit()
    conn.close()

