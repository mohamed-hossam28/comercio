
import pytest
from fastapi.testclient import TestClient
from models.users import User
from sqlalchemy.orm import Session
from controller import verify_password


class TestUserRegistration:    
    def test_register_user_successfully(self, client: TestClient, db_session: Session):
        response = client.post(
            "/register-user",
            data={
                "first_name": "Jane",
                "last_name": "Smith",
                "dob": "1995-05-15",
                "email": "jane.smith@test.com",
                "password": "SecurePassword123",
                "sex": "F",
                "phone": "+1987654321",
                "country": "Canada"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "Registration successful" in data["message"]
        
        # Verify user was created in database
        user = db_session.query(User).filter(User.email == "jane.smith@test.com").first()
        assert user is not None
        assert user.first_name == "Jane"
    
    def test_register_user_password_is_hashed(self, client: TestClient, db_session: Session):
        plain_password = "MySecretPassword123"
        response = client.post(
            "/register-user",
            data={
                "first_name": "Secure",
                "last_name": "User",
                "dob": "1990-01-01",
                "email": "secure@test.com",
                "password": plain_password,
                "sex": "M",
                "phone": "+1111111111",
                "country": "USA"
            }
        )
        
        assert response.status_code == 200
        
        user = db_session.query(User).filter(User.email == "secure@test.com").first()
        assert user.password != plain_password
        assert verify_password(plain_password, user.password)
    
    def test_register_user_duplicate_email_fails(self, client: TestClient, sample_user: User):
        response = client.post(
            "/register-user",
            data={
                "first_name": "Duplicate",
                "last_name": "User",
                "dob": "1990-01-01",
                "email": sample_user.email,  # Same as existing user
                "password": "Password123",
                "sex": "M",
                "phone": "+1222222222",
                "country": "USA"
            }
        )
        
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "already registered" in data["message"].lower()
    
    def test_register_user_missing_required_fields(self, client: TestClient):
        # Missing password field
        response = client.post(
            "/register-user",
            data={
                "first_name": "Incomplete",
                "last_name": "User",
                "email": "incomplete@test.com"
                # Missing other required fields
            }
        )
        
        assert response.status_code == 422


class TestUserLogin:    
    def test_login_with_valid_credentials(self, client: TestClient, sample_user: User):
        response = client.post(
            "/login",
            data={
                "email": sample_user.email,
                "password": "TestPassword123"  # From sample_user fixture
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "user_name" in data
        assert data["user_name"] == sample_user.first_name
        
        assert "session_token" in response.cookies
        assert response.cookies["session_token"] != ""
    
    def test_login_with_invalid_email(self, client: TestClient):
        response = client.post(
            "/login",
            data={
                "email": "nonexistent@test.com",
                "password": "SomePassword123"
            }
        )
        
        assert response.status_code == 401
        data = response.json()
        assert "Invalid email or password" in data["message"]
    
    def test_login_with_invalid_password(self, client: TestClient, sample_user: User):
        response = client.post(
            "/login",
            data={
                "email": sample_user.email,
                "password": "WrongPassword123"
            }
        )
        
        assert response.status_code == 401
        data = response.json()
        assert "Invalid email or password" in data["message"]


class TestGetCurrentUser:    
    def test_get_current_user_when_authenticated(self, authenticated_client: TestClient, sample_user: User):
        response = authenticated_client.get("/me")
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == sample_user.id
        assert data["email"] == sample_user.email
        assert data["first_name"] == sample_user.first_name
        assert data["last_name"] == sample_user.last_name
    
    def test_get_current_user_when_not_authenticated(self, client: TestClient):
        response = client.get("/me")
        assert response.status_code == 401
        data = response.json()
        assert "Not authenticated" in data["message"]
    
class TestUpdateProfile:    
    def test_update_profile_when_authenticated(self, authenticated_client: TestClient, sample_user: User, db_session: Session):
        response = authenticated_client.put(
            "/update-profile",
            data={
                "first_name": "UpdatedName",
                "phone": "+9999999999"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "updated successfully" in data["message"].lower()
        db_session.refresh(sample_user)
        assert sample_user.first_name == "UpdatedName"
        assert sample_user.phone == "+9999999999"
    
    def test_update_profile_when_not_authenticated(self, client: TestClient):
        response = client.put(
            "/update-profile",
            data={
                "first_name": "Unauthorized"
            }
        )
        
        assert response.status_code == 401
        data = response.json()
        assert "Not authenticated" in data["message"]


class TestLogout:    
    def test_logout_clears_session_cookie(self, authenticated_client: TestClient):
        response = authenticated_client.post("/logout")
        assert response.status_code == 200
        data = response.json()
        assert "Logged out" in data["message"]