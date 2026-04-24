import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

# Arrange-Act-Assert (AAA) pattern is used in all tests

def test_get_activities():
    # Arrange: (nothing to arrange for this test)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_success():
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Signed up {email} for {activity}"
    # Clean up: remove the test email if needed
    activities[activity]["participants"].remove(email)

def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # already signed up
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student already signed up for this activity"

def test_signup_nonexistent_activity():
    # Arrange
    activity = "Nonexistent Club"
    email = "someone@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"

def test_root_redirect():
    # Arrange: (nothing to arrange)
    # Act
    response = client.get("/")
    # Assert
    assert response.status_code == 200 or response.status_code == 307 or response.status_code == 302
    # Should redirect to /static/index.html
    assert "/static/index.html" in str(response.url)
