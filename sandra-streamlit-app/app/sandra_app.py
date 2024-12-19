import sqlite3
import pandas as pd
import streamlit as st
from pathlib import Path

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
                ("Lithium Battery", 500, 90, "Operational"),
                ("Flow Battery", 1500, 80, "Operational"),
                ("Solid State Battery", 1200, 95, "Under Testing"),
                ("Sodium-Ion Battery", 800, 75, "Operational"),
                ("Lead-Acid Battery", 400, 70, "Operational"),
                ("Zinc-Air Battery", 600, 78, "Operational"),
                ("Nickel-Metal Hydride Battery", 700, 85, "Operational"),
                ("Vanadium Redox Flow Battery", 2000, 70, "Operational"),
                ("Supercapacitor", 100, 90, "Operational"),
                ("Aluminum-Ion Battery", 1100, 88, "Under Development"),
                ("Magnesium-Ion Battery", 500, 82, "Under Testing"),
                ("Lithium-Sulfur Battery", 950, 92, "Under Development"),
                ("Graphene Supercapacitor", 150, 85, "Operational"),
                ("Hybrid Capacitor", 200, 80, "Operational"),
                ("Bromine Flow Battery", 1800, 80, "Operational"),
                ("Molten Salt Battery", 2500, 65, "Under Testing"),
                ("Flexible Battery", 300, 90, "Under Development"),
                ("Iron-Air Battery", 1200, 78, "Under Development")
            ]
        )
        conn.commit()

    # Insert default data for applications if empty
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

    # Connect to the database and initialize if necessary
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
def search_data(conn, table_name, column_name, query):
    """Search for data in a specific column of a table."""
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} WHERE {column_name} LIKE ?", ('%' + query + '%',))
    data = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    return pd.DataFrame(data, columns=columns)

# In Streamlit UI, add search functionality
search_query = st.text_input("Search Data:")
if search_query:
    st.subheader(f"Search Results for '{search_query}'")
    energy_storage_df = search_data(conn, "energy_storage", "technology", search_query)
    st.dataframe(energy_storage_df)


# Dynamic Data Visualization with Altair
st.header("Data Visualization")

# Load energy storage data
energy_storage_df = load_table(conn, "energy_storage")

# Bar Chart for comparing efficiency and capacity
st.subheader("Energy Storage: Efficiency vs Capacity")
chart = alt.Chart(energy_storage_df).mark_bar().encode(
    x='technology:N',
    y='capacity:Q',
    color='technology:N',
    tooltip=['technology:N', 'capacity:Q', 'efficiency:Q']
).properties(
    title='Energy Storage Capacity and Efficiency'
)
st.altair_chart(chart, use_container_width=True)

def update_entry(conn, table_name, entry_id, updated_values):
    """Update a specific entry in the database."""
    cursor = conn.cursor()
    columns = ", ".join([f"{key} = ?" for key in updated_values.keys()])
    values = tuple(updated_values.values()) + (entry_id,)
    cursor.execute(f"UPDATE {table_name} SET {columns} WHERE id = ?", values)
    conn.commit()

# Streamlit UI for updating data
st.subheader("Update Data")

# Choose table and entry to update
table_name = st.selectbox("Select Table", ["energy_storage", "real_time_monitoring", "applications"])
entry_id = st.number_input("Entry ID", min_value=1)

if table_name == "energy_storage":
    tech = st.text_input("Technology")
    capacity = st.number_input("Capacity (kWh)")
    efficiency = st.number_input("Efficiency (%)")
    status = st.text_input("Status")

    if st.button("Update Entry"):
        updated_values = {
            "technology": tech,
            "capacity": capacity,
            "efficiency": efficiency,
            "status": status
        }
        update_entry(conn, "energy_storage", entry_id, updated_values)
        st.success(f"Entry with ID {entry_id} updated successfully!")

def delete_entry(conn, table_name, entry_id):
    """Delete an entry from a table."""
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (entry_id,))
    conn.commit()

# Streamlit UI for deleting data
st.subheader("Delete Data Entry")
entry_id = st.number_input("Entry ID", min_value=1)

if st.button("Delete Entry"):
    delete_entry(conn, "energy_storage", entry_id)
    st.success(f"Entry with ID {entry_id} deleted successfully!")


def export_to_csv(df, filename):
    """Export a DataFrame to a CSV file."""
    df.to_csv(filename, index=False)

# Streamlit UI for exporting data
st.subheader("Export Data to CSV")
if st.button("Export Energy Storage Data"):
    energy_storage_df = load_table(conn, "energy_storage")
    export_to_csv(energy_storage_df, "energy_storage_data.csv")
    st.success("Data exported as energy_storage_data.csv")


import time

# Real-Time Monitoring Dashboard
def get_real_time_data(conn):
    """Fetch latest data from real-time monitoring."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM real_time_monitoring ORDER BY timestamp DESC LIMIT 1")
    data = cursor.fetchone()
    return data

st.header("Real-Time Monitoring Dashboard")
while True:
    real_time_data = get_real_time_data(conn)
    st.write(f"Latest Data: {real_time_data}")
    time.sleep(5)  # Refresh every 5 seconds
