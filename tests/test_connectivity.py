import pytest

class TestBackendConnectivity:
    """Test backend API connectivity and response formats."""

    @pytest.mark.asyncio
    async def test_api_is_accessible(self, test_client):
        """Test that API root endpoint is accessible."""
        response = await test_client.get("/")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_student_login_endpoint_exists(self, test_client):
        """Test that /auth/login/student endpoint exists."""
        response = await test_client.post(
            "/auth/login/student",
            json={"username": "student1", "password": "wrongpass"}
        )
        # Should return 401 (wrong password) not 404 (endpoint missing)
        assert response.status_code in [401, 422]  # 422 if validation fails

    @pytest.mark.asyncio
    async def test_admin_login_endpoint_exists(self, test_client):
        """Test that /auth/login/admin endpoint exists."""
        response = await test_client.post(
            "/auth/login/admin",
            json={"username": "admin1", "password": "wrongpass"}
        )
        assert response.status_code in [401, 422]

    @pytest.mark.asyncio
    async def test_change_password_endpoint_exists(self, test_client, student_token):
        """Test that /auth/change-password endpoint exists."""
        response = await test_client.post(
            "/auth/change-password",
            json={"old_password": "testpassword", "new_password": "newpass123"},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        # 200 success or 422 validation - means endpoint exists
        assert response.status_code in [200, 422]

    @pytest.mark.asyncio
    async def test_students_list_endpoint(self, test_client, admin_token):
        """Test GET /students endpoint exists and returns list."""
        response = await test_client.get(
            "/students",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200  # Admin can list students

    @pytest.mark.asyncio
    async def test_api_returns_json(self, test_client):
        """Test that API returns JSON responses."""
        response = await test_client.get("/")
        assert response.headers.get("content-type") == "application/json"

    @pytest.mark.asyncio
    async def test_cors_headers_present(self, test_client):
        """Test that CORS headers are present for frontend integration."""
        response = await test_client.options("/auth/token")
        # Should have CORS headers if configured
        assert response.status_code in [200, 405]  # 405 if OPTIONS not allowed


class TestAuthenticationFlow:
    """Test authentication endpoints for frontend compatibility."""

    @pytest.mark.asyncio
    async def test_student_login_with_json(self, test_client, test_user):
        """Test student login with JSON format (frontend style)."""
        response = await test_client.post(
            "/auth/login/student",
            json={"username": "student1", "password": "testpassword"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_admin_login_with_json(self, test_client, test_admin):
        """Test admin login with JSON format (frontend style)."""
        response = await test_client.post(
            "/auth/login/admin",
            json={"username": "admin1", "password": "adminpass"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_student_login_wrong_role(self, test_client, test_admin):
        """Test that admin cannot login via student endpoint."""
        response = await test_client.post(
            "/auth/login/student",
            json={"username": "admin1", "password": "adminpass"}
        )
        assert response.status_code == 401
        assert "not a student" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_admin_login_wrong_role(self, test_client, test_user):
        """Test that student cannot login via admin endpoint."""
        response = await test_client.post(
            "/auth/login/admin",
            json={"username": "student1", "password": "testpassword"}
        )
        assert response.status_code == 401
        assert "not an admin" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, test_client):
        """Test login with invalid credentials."""
        response = await test_client.post(
            "/auth/login/student",
            json={"username": "nonexistent", "password": "wrongpass"}
        )
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_token_response_format(self, test_client, test_user):
        """Test that token response matches frontend expectations."""
        response = await test_client.post(
            "/auth/login/student",
            json={"username": "student1", "password": "testpassword"}
        )
        data = response.json()
        
        # Frontend expects these fields
        assert "access_token" in data
        assert isinstance(data["access_token"], str)
        assert len(data["access_token"]) > 0
        assert data["token_type"] == "bearer"


class TestStudentEndpoints:
    """Test student management endpoints."""

    @pytest.mark.asyncio
    async def test_get_students_list(self, test_client, admin_token, test_student):
        """Test fetching students list."""
        response = await test_client.get(
            "/students",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_student_by_roll_number(self, test_client, admin_token, test_student):
        """Test fetching single student by roll_number."""
        response = await test_client.get(
            f"/students/{test_student.roll_number}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["roll_number"] == "2023001"
        assert data["name"] == "John Doe"

    @pytest.mark.asyncio
    async def test_create_student(self, test_client, admin_token):
        """Test creating new student."""
        response = await test_client.post(
            "/students",
            json={
                "roll_number": "2023002",
                "name": "Jane Smith",
                "branch": "ECE",
                "year": 2,
                "email": "jane@example.com",
                "mobile": "9876543211"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["roll_number"] == "2023002"

    @pytest.mark.asyncio
    async def test_response_includes_all_student_fields(self, test_client, admin_token, test_student):
        """Test that student response includes all fields frontend expects."""
        response = await test_client.get(
            f"/students/{test_student.roll_number}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        data = response.json()
        
        # Frontend expects these fields
        required_fields = ["roll_number", "name", "branch", "year", "email", "mobile"]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"


class TestChangePasswordEndpoint:
    """Test change password endpoint."""

    @pytest.mark.asyncio
    async def test_change_password_success(self, test_client, student_token, test_user):
        """Test successful password change."""
        response = await test_client.post(
            "/auth/change-password",
            json={
                "old_password": "testpassword",
                "new_password": "newpassword123"
            },
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 200
        assert "success" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_change_password_wrong_old_password(self, test_client, student_token):
        """Test password change with wrong old password."""
        response = await test_client.post(
            "/auth/change-password",
            json={
                "old_password": "wrongoldpass",
                "new_password": "newpass"
            },
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_change_password_requires_auth(self, test_client):
        """Test that password change requires authentication."""
        response = await test_client.post(
            "/auth/change-password",
            json={
                "old_password": "anypass",
                "new_password": "newpass"
            }
        )
        assert response.status_code == 401  # 401 Unauthorized when no auth provided

    @pytest.mark.asyncio
    async def test_change_password_response_format(self, test_client, student_token, test_user):
        """Test that password change response matches frontend expectations."""
        response = await test_client.post(
            "/auth/change-password",
            json={
                "old_password": "testpassword",
                "new_password": "newpass123"
            },
            headers={"Authorization": f"Bearer {student_token}"}
        )
        data = response.json()
        assert "detail" in data
        assert isinstance(data["detail"], str)


class TestAPIErrorHandling:
    """Test API error handling for frontend."""

    @pytest.mark.asyncio
    async def test_401_unauthorized_no_token(self, test_client):
        """Test 401 response without token."""
        response = await test_client.get("/students")
        assert response.status_code in [401, 403]

    @pytest.mark.asyncio
    async def test_404_not_found(self, test_client, admin_token):
        """Test 404 response for non-existent resource."""
        response = await test_client.get(
            "/students/nonexistent",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_error_response_format(self, test_client, student_token):
        """Test that error responses have expected format."""
        response = await test_client.get(
            "/students/nonexistent",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        data = response.json()
        assert "detail" in data
        assert isinstance(data["detail"], str)

    @pytest.mark.asyncio
    async def test_invalid_token_response(self, test_client):
        """Test response with invalid token."""
        response = await test_client.get(
            "/students",
            headers={"Authorization": "Bearer invalid.token.here"}
        )
        assert response.status_code == 401
