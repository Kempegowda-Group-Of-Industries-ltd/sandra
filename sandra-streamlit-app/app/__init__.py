"""
Initialization file for the SANDRA Streamlit app package.

This package contains the main application code, database management functions, and utility scripts.
"""

# Import key components from the package
from .sandra_app import run_app
from .database import (
    connect_db,
    initialize_db,
    insert_data,
    fetch_data,
    update_data,
    delete_data,
)
from .utils import format_data, generate_charts

# Define the package-level metadata
__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Package-level functions (if any)
def start_app():
    """
    Start the SANDRA Streamlit app.
    """
    run_app()

# Expose important modules and functions at the package level
__all__ = [
    "run_app",
    "connect_db",
    "initialize_db",
    "insert_data",
    "fetch_data",
    "update_data",
    "delete_data",
    "format_data",
    "generate_charts",
    "start_app",
]
