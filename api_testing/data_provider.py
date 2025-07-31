# This module provides reusable test data sets for parameterized testing.

def user_creation_data():
    """
    Returns a list of dictionaries representing different user creation payloads:
    - Valid user with both 'name' and 'job'
    - User missing the 'job' field
    - User missing the 'name' field
    - User with an extra unexpected field 'extra'
    This data set allows testing both positive and negative create user scenarios.
    """
    return [
        {"name": "Alice", "job": "Engineer"},              # Valid data
        {"name": "Bob"},                                   # Missing job
        {"job": "Manager"},                                # Missing name
        {"name": "Eve", "job": "QA", "extra": "invalid"},  # Extra field
    ]

def user_update_data():
    """
    Returns a list of tuples (user_id, update_payload) for testing user updates.
    Includes:
    - A valid update to an existing user (user_id=2)
    - An attempt to update a non-existent user (user_id=999)
    This tests both success and failure update scenarios.
    """
    return [
        (2, {"name": "Updated Name", "job": "Updated Job"}),  # Existing user
        (9999, {"name": "Ghost", "job": "NonExistent"}),       # Non-existent user
    ]

def user_ids():
    """
    Returns a list of user IDs for GET request testing.
    Includes:
    - An existing user ID (2)
    - A non-existent user ID (999)
    """
    return [2, 999]

def concurrent_user_ids():
    """
    Returns a list of user IDs for simulating concurrent GET requests.
    Useful for performance and concurrency tests.
    """
    return [1, 2, 3, 4, 5]
