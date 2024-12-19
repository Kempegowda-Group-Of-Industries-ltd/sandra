"""
Utility module for the SANDRA Streamlit app.

This module provides helper functions for common operations such as
data validation, formatting, and user feedback.
"""

import re


def validate_feature_name(feature_name):
    """
    Validate the feature name input.

    Parameters:
        feature_name (str): The feature name to validate.

    Returns:
        bool: True if the feature name is valid, False otherwise.
    """
    if not feature_name or len(feature_name.strip()) == 0:
        return False
    return True


def validate_status(status):
    """
    Validate the status input.

    Parameters:
        status (str): The status to validate.

    Returns:
        bool: True if the status is valid, False otherwise.
    """
    valid_statuses = ["active", "inactive", "pending", "archived"]
    return status.lower() in valid_statuses


def format_description(description):
    """
    Format the description text by stripping unnecessary whitespace.

    Parameters:
        description (str): The description to format.

    Returns:
        str: The formatted description.
    """
    return description.strip()


def validate_description(description):
    """
    Validate the description input.

    Parameters:
        description (str): The description to validate.

    Returns:
        bool: True if the description is valid, False otherwise.
    """
    if not description or len(description.strip()) < 10:
        return False
    return True


def show_feedback(message, feedback_type="info"):
    """
    Display feedback to the user.

    Parameters:
        message (str): The feedback message to display.
        feedback_type (str): The type of feedback, e.g., "info", "success", "warning", "error".
    """
    if feedback_type == "success":
        print(f"[SUCCESS]: {message}")
    elif feedback_type == "error":
        print(f"[ERROR]: {message}")
    elif feedback_type == "warning":
        print(f"[WARNING]: {message}")
    else:
        print(f"[INFO]: {message}")


def extract_id_from_input(input_str):
    """
    Extract a numeric ID from a user-provided input string.

    Parameters:
        input_str (str): The input string containing the ID.

    Returns:
        int or None: The extracted ID, or None if no valid ID is found.
    """
    match = re.search(r'\b\d+\b', input_str)
    return int(match.group()) if match else None


if __name__ == "__main__":
    # Testing the utility functions
    print("Validating feature name:", validate_feature_name("Energy Storage"))  # True
    print("Validating invalid status:", validate_status("unknown"))  # False
    print("Formatting description:", format_description("  A valid description.  "))  # "A valid description."
    print("Validating description:", validate_description("Too short"))  # False
    print("Extracting ID from input:", extract_id_from_input("Delete ID 123"))  # 123
