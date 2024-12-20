import sqlite3
import pandas as pd
import streamlit as st
import altair as alt

# Database connection and initialization
def connect_db():
    conn = sqlite3.connect("sand_battery.db")
    return conn

def initialize_db(conn):
    cursor = conn.cursor()
    # Create tables if they don't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS energy_storage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS real_time_monitoring (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )
    """)
    conn.commit()

# Add data
def add_data(conn, table_name, name, description):
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {table_name} (name, description) VALUES (?, ?)", (name, description))
    conn.commit()

# Fetch data
def fetch_data(conn, table_name):
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, conn)

# Update data
def update_data(conn, table_name, record_id, name, description):
    cursor = conn.cursor()
    cursor.execute(f"""
        UPDATE {table_name}
        SET name = ?, description = ?
        WHERE id = ?
    """, (name, description, record_id))
    conn.commit()

# Delete data
def delete_data(conn, table_name, record_id):
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (record_id,))
    conn.commit()

# Search data
def search_data(conn, table_name, keyword):
    query = f"SELECT * FROM {table_name} WHERE name LIKE ? OR description LIKE ?"
    return pd.read_sql(query, conn, params=(f"%{keyword}%", f"%{keyword}%"))

# Streamlit App
st.title("Sandra: Sand Battery Solutions Database")

# Sidebar for navigation
nav = st.sidebar.radio("Navigation", ["Database Overview", "Add Data", "Update Data", "Delete Data", "Search Data", "Visualizations"])

# Connect to database and initialize
conn = connect_db()
initialize_db(conn)

if nav == "Database Overview":
    st.header("Database Overview")
    tables = ["energy_storage", "real_time_monitoring", "applications"]
    for table in tables:
        st.subheader(table.capitalize())
        data = fetch_data(conn, table)
        st.dataframe(data)

elif nav == "Add Data":
    st.header("Add Data")
    table = st.selectbox("Choose a table to add data", ["energy_storage", "real_time_monitoring", "applications"])
    name = st.text_input("Name")
    description = st.text_area("Description")
    if st.button("Add Data"):
        if name and description:
            add_data(conn, table, name, description)
            st.success(f"Data added to {table}")
        else:
            st.error("All fields are required!")

elif nav == "Update Data":
    st.header("Update Data")
    table = st.selectbox("Choose a table to update data", ["energy_storage", "real_time_monitoring", "applications"])
    data = fetch_data(conn, table)
    if not data.empty:
        st.dataframe(data)
        record_id = st.number_input("Enter ID of the record to update", min_value=1, step=1)
        name = st.text_input("Updated Name")
        description = st.text_area("Updated Description")
        if st.button("Update Data"):
            if name and description:
                update_data(conn, table, record_id, name, description)
                st.success("Data updated successfully")
            else:
                st.error("All fields are required!")
    else:
        st.warning("No data available in the table")

elif nav == "Delete Data":
    st.header("Delete Data")
    table = st.selectbox("Choose a table to delete data", ["energy_storage", "real_time_monitoring", "applications"])
    data = fetch_data(conn, table)
    if not data.empty:
        st.dataframe(data)
        record_id = st.number_input("Enter ID of the record to delete", min_value=1, step=1)
        if st.button("Delete Data"):
            delete_data(conn, table, record_id)
            st.success("Data deleted successfully")
    else:
        st.warning("No data available in the table")

elif nav == "Search Data":
    st.header("Search Data")
    table = st.selectbox("Choose a table to search data", ["energy_storage", "real_time_monitoring", "applications"])
    keyword = st.text_input("Enter a keyword to search")
    if st.button("Search"):
        data = search_data(conn, table, keyword)
        if not data.empty:
            st.dataframe(data)
        else:
            st.warning("No matching records found")

elif nav == "Visualizations":
    st.header("Visualizations")
    table = st.selectbox("Choose a table to visualize", ["energy_storage", "real_time_monitoring", "applications"])
    data = fetch_data(conn, table)
    if not data.empty:
        chart = alt.Chart(data).mark_bar().encode(
            x="id:O",
            y=alt.Y("name:N", sort=None),
            tooltip=["name", "description"]
        ).interactive()
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("No data available to visualize")
