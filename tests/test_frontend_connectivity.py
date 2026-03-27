"""
Frontend Compatibility Tests
Tests that verify frontend JavaScript code can properly interact with backend API.
"""
import pytest
import json

class TestFrontendLoginJS:
    """Test that frontend login.js can work with our API."""

    @pytest.mark.asyncio
    async def test_frontend_student_login_request_format(self, test_client, test_user):
        """
        Simulate frontend login.js sending student login request.
        Frontend code: frontend/js/login.js line 63
        """
        # This is what frontend sends (JSON format)
        frontend_request = {
            "username": "student1",
            "password": "testpassword"
        }
        
        response = await test_client.post(
            "/auth/login/student",
            json=frontend_request
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Frontend expects token in localStorage
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_frontend_admin_login_request_format(self, test_client, test_admin):
        """
        Simulate frontend login.js sending admin login request.
        Frontend code: frontend/js/login.js line 83
        """
        frontend_request = {
            "username": "admin1",
            "password": "adminpass"
        }
        
        response = await test_client.post(
            "/auth/login/admin",
            json=frontend_request
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    @pytest.mark.asyncio
    async def test_frontend_login_error_handling(self, test_client):
        """
        Test frontend can handle login errors.
        Frontend expects 401 status and detail message.
        """
        response = await test_client.post(
            "/auth/login/student",
            json={"username": "student1", "password": "wrongpass"}
        )
        
        assert response.status_code == 401
        data = response.json()
        
        # Frontend shows this error message
        assert "detail" in data
        assert isinstance(data["detail"], str)


class TestFrontendChangePasswordJS:
    """Test that frontend change-password.js can work with our API."""

    @pytest.mark.asyncio
    async def test_frontend_change_password_request_format(self, test_client, student_token, test_user):
        """
        Simulate frontend change-password.js sending request.
        Frontend code: frontend/js/change-password.js line 109
        """
        # This is what frontend sends
        frontend_request = {
            "old_password": "testpassword",
            "new_password": "newpass123"
        }
        
        response = await test_client.post(
            "/auth/change-password",
            json=frontend_request,
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "detail" in data

    @pytest.mark.asyncio
    async def test_frontend_change_password_error_response(self, test_client, student_token):
        """Test frontend can handle password change errors."""
        response = await test_client.post(
            "/auth/change-password",
            json={
                "old_password": "wrongoldpass",
                "new_password": "newpass"
            },
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data


class TestFrontendStudentsJS:
    """Test that frontend students.js can work with our API."""

    @pytest.mark.asyncio
    async def test_frontend_get_students_list(self, test_client, admin_token, test_student):
        """
        Simulate frontend students.js fetching students list.
        Frontend code: frontend/js/pages/students.js line 14-20
        """
        response = await test_client.get(
            "/students",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # Frontend expects each student to have these fields
        if len(data) > 0:
            student = data[0]
            required_fields = ["roll_number", "name", "branch", "year", "email", "mobile"]
            for field in required_fields:
                assert field in student, f"Frontend expects field: {field}"

    @pytest.mark.asyncio
    async def test_frontend_student_profile_link(self, test_client, admin_token, test_student):
        """
        Test that student profile link uses correct ID.
        Frontend code: frontend/js/pages/students.js line 53
        Changed from id=${s.id} to id=${s.roll_number}
        """
        # Get students list (admin only)
        response = await test_client.get(
            "/students",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Frontend extracts roll_number for profile link
        student = next((s for s in data if s["roll_number"] == "2023001"), None)
        assert student is not None
        
        # Frontend navigates to profile.html?id=${s.roll_number}
        profile_response = await test_client.get(
            f"/students/{student['roll_number']}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert profile_response.status_code == 200

    @pytest.mark.asyncio
    async def test_frontend_delete_student_request(self, test_client, admin_token, test_student):
        """
        Simulate frontend deleting a student.
        Frontend code: frontend/js/pages/students.js line 54
        """
        # Delete student with roll_number (not id)
        response = await test_client.delete(
            f"/students/{test_student.roll_number}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code in [200, 204]

    @pytest.mark.asyncio
    async def test_frontend_add_student_request(self, test_client, admin_token):
        """
        Simulate frontend submitting add-student form.
        Frontend code: frontend/js/pages/add-student.js
        """
        # This is what frontend sends from form
        frontend_request = {
            "roll_number": "2023099",
            "name": "New Student",
            "branch": "CSE",
            "year": 1,
            "email": "new@example.com",
            "mobile": "9876543212",
            "address": "Some Address"
        }
        
        response = await test_client.post(
            "/students",
            json=frontend_request,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["roll_number"] == "2023099"


class TestFrontendProfileJS:
    """Test that frontend profile.js can work with our API."""

    @pytest.mark.asyncio
    async def test_frontend_load_student_profile(self, test_client, admin_token, test_student):
        """
        Simulate frontend profile.js loading student profile.
        Frontend code: frontend/js/pages/profile.js line 25-29
        """
        # Frontend gets URL parameter: profile.html?id=2023001
        student_id = "2023001"  # roll_number used as ID
        
        response = await test_client.get(
            f"/students/{student_id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Frontend expects all these fields from renderBasicInfo
        expected_fields = ["roll_number", "name", "branch", "year", "email", "mobile"]
        for field in expected_fields:
            assert field in data, f"Profile expects: {field}"

    @pytest.mark.asyncio
    async def test_frontend_profile_response_structure(self, test_client, admin_token, test_student):
        """Test that profile response structure matches frontend expectations."""
        response = await test_client.get(
            f"/students/{test_student.roll_number}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        data = response.json()
        
        # Frontend renderBasicInfo uses these specific fields
        assert isinstance(data["roll_number"], str)
        assert isinstance(data["name"], str)
        assert isinstance(data["branch"], str)
        assert isinstance(data["year"], int)
        assert isinstance(data["email"], str)
        assert isinstance(data["mobile"], str)


class TestAPIResponseFormat:
    """Test that API responses match expected JSON format from frontend."""

    @pytest.mark.asyncio
    async def test_json_content_type(self, test_client):
        """All responses should be JSON."""
        response = await test_client.get("/")
        assert "application/json" in response.headers.get("content-type", "")

    @pytest.mark.asyncio
    async def test_error_response_structure(self, test_client):
        """Error responses should have consistent structure."""
        response = await test_client.get("/students")  # No auth
        
        # Should have 401/403
        assert response.status_code in [401, 403, 422]
        data = response.json()
        
        # Frontend expects detail field
        assert "detail" in data

    @pytest.mark.asyncio
    async def test_token_response_structure(self, test_client, test_user):
        """Token response should match OAuth2 standard."""
        response = await test_client.post(
            "/auth/login/student",
            json={"username": "student1", "password": "testpassword"}
        )
        
        data = response.json()
        
        # OAuth2 standard
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert isinstance(data["access_token"], str)


class TestFrontendAPIConfiguration:
    """Test that frontend API configuration will work correctly."""

    @pytest.mark.asyncio
    async def test_api_root_endpoint_accessible(self, test_client):
        """Frontend might check if API is accessible."""
        response = await test_client.get("/")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_api_responds_with_json_not_html(self, test_client):
        """Frontend expects JSON, not HTML error pages."""
        response = await test_client.get("/nonexistent")
        
        # Should return JSON error, not HTML
        try:
            data = response.json()
            assert "detail" in data
        except:
            # If not JSON, check it's not HTML
            assert not response.text.startswith("<html")

    @pytest.mark.asyncio
    async def test_multiple_requests_use_same_session(self, test_client, admin_token, test_student):
        """Frontend reuses token for multiple requests in session."""
        
        # First request (admin listing students)
        response1 = await test_client.get(
            "/students",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response1.status_code == 200
        
        # Second request with same token (admin accessing student profile)
        response2 = await test_client.get(
            f"/students/{test_student.roll_number}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response2.status_code == 200
        
        # Both work - token is valid for multiple requests
