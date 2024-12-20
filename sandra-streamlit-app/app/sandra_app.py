import sqlite3
import pandas as pd
import streamlit as st
import altair as alt
import pandas as pd





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

if not data.empty:
      pie_chart = alt.Chart(data).mark_arc().encode(
        theta=alt.Theta(field="id", type="quantitative"),
        color=alt.Color(field="name", type="nominal"),
        tooltip=["name", "description"]
      ).properties(
          title="Distribution of Records by Name"
      )
      st.altair_chart(pie_chart, use_container_width=True)

  if not data.empty:
      scatter_plot = alt.Chart(data).mark_circle(size=100).encode(
        x=alt.X("id:O", axis=alt.Axis(title="ID")),
        y=alt.Y("name:N", axis=alt.Axis(title="Name")),
        color="name:N",
        tooltip=["name", "description"]
      ).interactive().properties(
        title="Scatter Plot of Records"
       )
      st.altair_chart(scatter_plot, use_container_width=True)
  if not data.empty:
       line_chart = alt.Chart(data).mark_line(point=True).encode(
        x=alt.X("id:O", axis=alt.Axis(title="ID")),
        y=alt.Y("id:Q", axis=alt.Axis(title="ID (Quantitative for Line)")),
        color="name:N",
        tooltip=["name", "description"]
     ).interactive().properties(
        title="Trend of IDs Across Records"
     )
      st.altair_chart(line_chart, use_container_width=True)

  if not data.empty:
      stacked_bar_chart = alt.Chart(data).mark_bar().encode(
        x=alt.X("name:N", axis=alt.Axis(title="Name")),
        y=alt.Y("id:Q", axis=alt.Axis(title="ID")),
        color="name:N",
        tooltip=["name", "description"]
     ).properties(
        title="Stacked Bar Chart of Names"
     )
     st.altair_chart(stacked_bar_chart, use_container_width=True)

  if not data.empty:
    heatmap = alt.Chart(data).mark_rect().encode(
        x=alt.X("name:N", axis=alt.Axis(title="Name")),
        y=alt.Y("id:O", axis=alt.Axis(title="ID")),
        color=alt.Color("id:Q", scale=alt.Scale(scheme="blues"), title="ID Value"),
        tooltip=["name", "description"]
    ).properties(
        title="Heatmap of IDs by Name"
    )
    st.altair_chart(heatmap, use_container_width=True)
  if not data.empty:
    area_chart = alt.Chart(data).mark_area(opacity=0.5).encode(
        x=alt.X("id:O", axis=alt.Axis(title="ID")),
        y=alt.Y("id:Q", axis=alt.Axis(title="ID Value")),
        color=alt.Color("name:N", legend=alt.Legend(title="Name")),
        tooltip=["name", "description"]
    ).properties(
        title="Area Chart of IDs by Name"
    )
    st.altair_chart(area_chart, use_container_width=True)

 if not data.empty:
    histogram = alt.Chart(data).mark_bar().encode(
        x=alt.X("id:Q", bin=True, axis=alt.Axis(title="ID Bins")),
        y=alt.Y("count():Q", axis=alt.Axis(title="Count")),
        color=alt.Color("name:N", legend=alt.Legend(title="Name")),
        tooltip=["name", "description"]
    ).properties(
        title="Histogram of IDs"
    )
    st.altair_chart(histogram, use_container_width=True)
 if not data.empty:
    brush = alt.selection(type="interval")

    scatter_with_brush = alt.Chart(data).mark_circle(size=100).encode(
        x=alt.X("id:O", axis=alt.Axis(title="ID")),
        y=alt.Y("id:Q", axis=alt.Axis(title="ID Value")),
        color=alt.condition(brush, "name:N", alt.value("lightgray")),
        tooltip=["name", "description"]
    ).add_selection(
        brush
    ).properties(
        title="Scatter Plot with Interactive Brush Filter"
    )

    st.altair_chart(scatter_with_brush, use_container_width=True)

  if not data.empty:
    bubble_chart = alt.Chart(data).mark_circle().encode(
        x=alt.X("id:Q", axis=alt.Axis(title="ID")),
        y=alt.Y("id:Q", axis=alt.Axis(title="ID Value")),
        size=alt.Size("id:Q", title="Size by ID"),
        color="name:N",
        tooltip=["name", "description"]
    ).properties(
        title="Bubble Chart of IDs by Name"
    )
    st.altair_chart(bubble_chart, use_container_width=True)

  if not data.empty:
    sorted_bar_chart = alt.Chart(data).mark_bar().encode(
        x=alt.X("id:Q", axis=alt.Axis(title="ID Value")),
        y=alt.Y("name:N", sort="-x", axis=alt.Axis(title="Name")),
        color="name:N",
        tooltip=["name", "description"]
    ).properties(
        title="Bar Chart Sorted by ID"
    )
    st.altair_chart(sorted_bar_chart, use_container_width=True)



 if not data.empty:
    text_chart = alt.Chart(data).mark_text(size=14).encode(
        x=alt.X("id:O", axis=alt.Axis(title="ID")),
        y=alt.Y("name:N", axis=alt.Axis(title="Name")),
        text="description:N",
        color=alt.Color("name:N", legend=alt.Legend(title="Name")),
        tooltip=["name", "description"]
    ).properties(
        title="Text Chart Displaying Descriptions"
    )
    st.altair_chart(text_chart, use_container_width=True)


