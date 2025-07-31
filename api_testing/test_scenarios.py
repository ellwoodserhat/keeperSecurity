import pytest
import time
import threading

from utilities.httpReq import request
from api_testing.data_provider import (
    user_creation_data,
    user_update_data,
    user_ids,
    concurrent_user_ids
)

# ----------------------
# CREATE USER SCENARIOS
# ----------------------
@pytest.mark.parametrize("data", user_creation_data())
def test_create_user(data):
    """
    Test creating a user with various data sets:
    - Valid payload (name and job present)
    - Missing required fields (e.g., name or job)
    - Payload with extra unexpected fields
    """
    response = request("POST", "users", data=data)
    # API may respond with 201 (Created) or 400/422 (Bad Request / Validation Error)
    assert response.status_code in [201, 400, 422]

    # On success, check response contains an ID and echoes input
    if response.status_code == 201:
        assert "id" in response.json()
        for key in data:
            assert str(data[key]) in response.text


# ------------------
# READ USER SCENARIOS
# ------------------
@pytest.mark.parametrize("user_id", user_ids())
def test_get_user(user_id):
    """
    Test fetching a user by ID.
    - Valid ID should return 200 and include user data
    - Invalid ID should return 404
    """
    response = request("GET", f"users/{user_id}")
    if user_id == 999:
        assert response.status_code == 404
    else:
        assert response.status_code == 200
        assert "data" in response.json()


# ------------------
# UPDATE USER SCENARIOS
# ------------------
@pytest.mark.parametrize("user_id, update_data", user_update_data())
def test_update_user(user_id, update_data):
    """
    Test updating user by ID.
    - Existing user should be updated with status 200
    - Non-existent user should return 404 or similar
    """
    response = request("PUT", f"users/{user_id}", data=update_data)
    if user_id == 999:
        assert response.status_code in [404, 400, 422]
    else:
        assert response.status_code == 200
        # Check if returned payload contains updated fields
        for key in update_data:
            assert key in response.json()


# ---------------------
# DELETE USER SCENARIOS
# ---------------------
def test_delete_user_twice():
    """
    Test deleting the same user twice.
    - First deletion should return 204 (No Content)
    - Second deletion may return 204 or 404 depending on idempotency
    """
    user_id = 2
    response1 = request("DELETE", f"users/{user_id}")
    response2 = request("DELETE", f"users/{user_id}")
    assert response1.status_code == 204
    assert response2.status_code in [204, 404]


# ----------------------
# RESPONSE TIME SCENARIO
# ----------------------
def test_response_time_under_500ms():
    """
    Test that the response time of a GET call is under 500 milliseconds.
    This is a basic performance check.
    """
    start = time.time()
    response = request("GET", "users/2")
    end = time.time()
    assert response.status_code == 200
    assert (end - start) < 0.5, f"Response took too long: {end - start:.2f}s"


# --------------------------
# CONCURRENT USERS SCENARIO
# --------------------------
def test_concurrent_reads():
    """
    Simulate high load by concurrently fetching multiple users.
    Ensures thread safety and performance under light concurrency.
    """
    ids = concurrent_user_ids()
    responses = []

    def fetch(uid):
        responses.append(request("GET", f"users/{uid}"))

    threads = [threading.Thread(target=fetch, args=(i,)) for i in ids]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert all(resp.status_code == 200 for resp in responses)
