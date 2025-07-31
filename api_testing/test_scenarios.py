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
from utilities.utils import get_logger

logger = get_logger("test_logger")

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
    logger.info(f"Running test_create_user with data: {data}")
    response = request("POST", "users", data=data)

    logger.info(f"Response status: {response.status_code}")
    logger.info(f"Response body: {response.text}")

    assert response.status_code in [201, 400, 422]

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
    logger.info(f"Running test_get_user with user_id: {user_id}")
    response = request("GET", f"users/{user_id}")

    logger.info(f"Response status: {response.status_code}")
    logger.info(f"Response body: {response.text}")

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
    logger.info(f"Running test_update_user with user_id: {user_id} and update_data: {update_data}")
    response = request("PUT", f"users/{user_id}", data=update_data)

    logger.info(f"Response status: {response.status_code}")
    logger.info(f"Response body: {response.text}")

    if user_id == 999:
        assert response.status_code in [404, 400, 422]
    else:
        assert response.status_code == 200
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
    logger.info(f"Running test_delete_user_twice with user_id: {user_id}")
    response1 = request("DELETE", f"users/{user_id}")
    logger.info(f"First deletion response: {response1.status_code}")

    response2 = request("DELETE", f"users/{user_id}")
    logger.info(f"Second deletion response: {response2.status_code}")

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
    logger.info("Running test_response_time_under_500ms for user_id 2")
    start = time.time()
    response = request("GET", "users/2")
    end = time.time()

    elapsed_time = end - start
    logger.info(f"Response status: {response.status_code}")
    logger.info(f"Response time: {elapsed_time:.3f} seconds")

    assert response.status_code == 200
    assert elapsed_time < 0.5, f"Response took too long: {elapsed_time:.2f}s"


# --------------------------
# CONCURRENT USERS SCENARIO
# --------------------------
def test_concurrent_reads():
    """
    Simulate high load by concurrently fetching multiple users.
    Ensures thread safety and performance under light concurrency.
    """
    ids = concurrent_user_ids()
    logger.info(f"Running test_concurrent_reads with IDs: {ids}")
    responses = []

    def fetch(uid):
        resp = request("GET", f"users/{uid}")
        logger.info(f"Fetched user {uid}, status: {resp.status_code}")
        responses.append(resp)

    threads = [threading.Thread(target=fetch, args=(i,)) for i in ids]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert all(resp.status_code == 200 for resp in responses)
