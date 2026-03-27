"""
Tests for authentication endpoints
"""
import pytest
from httpx import AsyncClient


class TestAuthenticationEndpoints:
    """Test suite for /auth endpoints"""
    
    @pytest.mark.asyncio
    async def test_root_endpoint(self, client: AsyncClient):
        """Test root endpoint returns healthy response"""
        response = await client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "E-Student Cell API is running"}
    
    @pytest.mark.asyncio
    async def test_login_student_success(self, client: AsyncClient, test_user_student):
        """Test successful student login"""
        response = await client.post(
            "/auth/login/student",
            json={
                "username": "student_test",
                "password": "StudentPassword123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    @pytest.mark.asyncio
    async def test_login_student_wrong_password(self, client: AsyncClient, test_user_student):
        """Test student login with wrong password"""
        response = await client.post(
            "/auth/login/student",
            json={
                "username": "student_test",
                "password": "WrongPassword"
            }
        )
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_login_student_nonexistent_user(self, client: AsyncClient):
        """Test student login with non-existent user"""
        response = await client.post(
            "/auth/login/student",
            json={
                "username": "nonexistent",
                "password": "password"
            }
        )
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_login_admin_success(self, client: AsyncClient, test_user_admin):
        """Test successful admin login"""
        response = await client.post(
            "/auth/login/admin",
            json={
                "username": "admin_test",
                "password": "AdminPassword123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    @pytest.mark.asyncio
    async def test_login_admin_with_student_account(self, client: AsyncClient, test_user_student):
        """Test admin login fails with student account"""
        response = await client.post(
            "/auth/login/admin",
            json={
                "username": "student_test",
                "password": "StudentPassword123"
            }
        )
        assert response.status_code == 401
        assert "not an admin account" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_login_student_with_admin_account(self, client: AsyncClient, test_user_admin):
        """Test student login fails with admin account"""
        response = await client.post(
            "/auth/login/student",
            json={
                "username": "admin_test",
                "password": "AdminPassword123"
            }
        )
        assert response.status_code == 401
        assert "not a student account" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_change_password_success(self, client: AsyncClient, test_user_student):
        """Test successful password change"""
        # First, login to get token
        login_response = await client.post(
            "/auth/login/student",
            json={
                "username": "student_test",
                "password": "StudentPassword123"
            }
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        
        # Change password
        response = await client.post(
            "/auth/change-password",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "old_password": "StudentPassword123",
                "new_password": "NewPassword123!"
            }
        )
        assert response.status_code == 200
        assert "Password changed successfully" in response.json()["detail"]
        
        # Verify old password doesn't work
        old_password_response = await client.post(
            "/auth/login/student",
            json={
                "username": "student_test",
                "password": "StudentPassword123"
            }
        )
        assert old_password_response.status_code == 401
        
        # Verify new password works
        new_password_response = await client.post(
            "/auth/login/student",
            json={
                "username": "student_test",
                "password": "NewPassword123!"
            }
        )
        assert new_password_response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_change_password_wrong_old_password(self, client: AsyncClient, test_user_student):
        """Test password change with wrong old password"""
        # Login
        login_response = await client.post(
            "/auth/login/student",
            json={
                "username": "student_test",
                "password": "StudentPassword123"
            }
        )
        token = login_response.json()["access_token"]
        
        # Try to change with wrong old password
        response = await client.post(
            "/auth/change-password",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "old_password": "WrongPassword",
                "new_password": "NewPassword123!"
            }
        )
        assert response.status_code == 401
        assert "Incorrect password" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_change_password_without_authentication(self, client: AsyncClient):
        """Test change password endpoint requires authentication"""
        response = await client.post(
            "/auth/change-password",
            json={
                "old_password": "old",
                "new_password": "new"
            }
        )
        assert response.status_code == 403  # Forbidden - no auth header
    
    @pytest.mark.asyncio
    async def test_token_endpoint_with_form_data(self, client: AsyncClient, test_user_student):
        """Test OAuth2 token endpoint with form data"""
        response = await client.post(
            "/auth/token",
            data={
                "username": "student_test",
                "password": "StudentPassword123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
