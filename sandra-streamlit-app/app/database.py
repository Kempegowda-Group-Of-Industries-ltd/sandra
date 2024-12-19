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
