from pathlib import Path
import sqlite3
import streamlit as st
import pandas as pd

# Set up the Streamlit app configuration
st.set_page_config(
    page_title="SANDRA - Integrated Sand Battery Solution",
    page_icon=":battery:",
    layout="wide"
)

# -----------------------------------------------------------------------------
# Database setup functions
def connect_db():
    """Connects to the sqlite database."""
    DB_FILENAME = Path(__file__).parent / "sandra.db"
    db_already_exists = DB_FILENAME.exists()

    conn = sqlite3.connect(DB_FILENAME)
    db_was_just_created = not db_already_exists

    return conn, db_was_just_created

def initialize_db(conn):
    """Initializes the database with tables and default data."""
    cursor = conn.cursor()

    # Create tables for energy storage, real-time monitoring, and applications
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS energy_storage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            technology TEXT,
            capacity REAL,
            efficiency REAL,
            status TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS real_time_monitoring (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parameter TEXT,
            value REAL,
            unit TEXT,
            timestamp TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sector TEXT,
            description TEXT,
            impact TEXT
        )
        """
    )

    # Insert default data if tables are empty
    cursor.execute("SELECT COUNT(*) FROM energy_storage")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            """
            INSERT INTO energy_storage (technology, capacity, efficiency, status)
            VALUES (?, ?, ?, ?)
            """,
            [
                ("Sand Battery", 1000, 85, "Operational"),
                ("Lithium Battery", 500, 90, "Operational")
            ]
        )

    cursor.execute("SELECT COUNT(*) FROM applications")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            """
            INSERT INTO applications (sector, description, impact)
            VALUES (?, ?, ?)
            """,
            [
                ("Rural Electrification", "Off-grid energy storage for remote areas", "Improved energy access"),
                ("Urban Smart Grids", "Stabilize grid supply during peak hours", "Reduced energy wastage"),
                ("Industrial Use", "Heating processes for energy-intensive industries", "Lower fossil fuel dependence")
            ]
        )

    conn.commit()

# -----------------------------------------------------------------------------
# Load data from the database
def load_table(conn, table_name):
    """Loads data from a specific table in the database."""
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()

    columns = [description[0] for description in cursor.description]
    return pd.DataFrame(data, columns=columns)

# -----------------------------------------------------------------------------
# Streamlit UI Components
def display_dataframes(conn):
    """Displays the database tables as dataframes in the Streamlit app."""
    st.header("SANDRA Database Overview")

    # Display energy storage data
    st.subheader("Energy Storage")
    energy_storage_df = load_table(conn, "energy_storage")
    st.dataframe(energy_storage_df)

    # Display real-time monitoring data
    st.subheader("Real-Time Monitoring")
    monitoring_df = load_table(conn, "real_time_monitoring")
    st.dataframe(monitoring_df)

    # Display applications data
    st.subheader("Applications")
    applications_df = load_table(conn, "applications")
    st.dataframe(applications_df)

# -----------------------------------------------------------------------------
# Main Streamlit app logic
def main():
    st.title("SANDRA - Integrated Sand Battery Solution")

    conn, db_was_just_created = connect_db()

    if db_was_just_created:
        initialize_db(conn)

    st.sidebar.title("Navigation")
    options = ["Database Overview", "Add Data", "Update Data"]
    choice = st.sidebar.radio("Select an option", options)

    if choice == "Database Overview":
        display_dataframes(conn)

    elif choice == "Add Data":
        st.subheader("Add New Data")
        table_name = st.selectbox("Select Table", ["energy_storage", "real_time_monitoring", "applications"])

        if table_name == "energy_storage":
            tech = st.text_input("Technology")
            capacity = st.number_input("Capacity (kWh)", min_value=0.0)
            efficiency = st.number_input("Efficiency (%)", min_value=0.0, max_value=100.0)
            status = st.text_input("Status")
            if st.button("Add Entry"):
                conn.execute(
                    "INSERT INTO energy_storage (technology, capacity, efficiency, status) VALUES (?, ?, ?, ?)",
                    (tech, capacity, efficiency, status)
                )
                conn.commit()
                st.success("Entry added successfully!")

        elif table_name == "real_time_monitoring":
            param = st.text_input("Parameter")
            value = st.number_input("Value")
            unit = st.text_input("Unit")
            timestamp = st.text_input("Timestamp")
            if st.button("Add Entry"):
                conn.execute(
                    "INSERT INTO real_time_monitoring (parameter, value, unit, timestamp) VALUES (?, ?, ?, ?)",
                    (param, value, unit, timestamp)
                )
                conn.commit()
                st.success("Entry added successfully!")

        elif table_name == "applications":
            sector = st.text_input("Sector")
            description = st.text_area("Description")
            impact = st.text_area("Impact")
            if st.button("Add Entry"):
                conn.execute(
                    "INSERT INTO applications (sector, description, impact) VALUES (?, ?, ?)",
                    (sector, description, impact)
                )
                conn.commit()
                st.success("Entry added successfully!")

    elif choice == "Update Data":
        st.subheader("Update Existing Data")
        st.info("Feature coming soon!")

    conn.close()

if __name__ == "__main__":
    main()
