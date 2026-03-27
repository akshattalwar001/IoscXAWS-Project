"""
Tests for student endpoints
"""
import pytest
from httpx import AsyncClient
from app.services.authHelper import RoleEnum, create_new_user


class TestStudentEndpoints:
    """Test suite for /students endpoints"""
    
    @pytest.mark.asyncio
    async def test_create_student(self, client: AsyncClient, test_db):
        """Test creating a new student"""
        response = await client.post(
            "/students",
            json={
                "roll_number": "2023002",
                "name": "Jane Smith",
                "branch": "ECE",
                "year": 2,
                "email": "jane@example.com",
                "mobile": "9899999999"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["roll_number"] == "2023002"
        assert data["name"] == "Jane Smith"
        assert data["branch"] == "ECE"
        assert data["year"] == 2
    
    @pytest.mark.asyncio
    async def test_get_all_students(self, client: AsyncClient, test_student):
        """Test retrieving all students"""
        response = await client.get("/students")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        # Check that our test student is in the list
        roll_numbers = [s["roll_number"] for s in data]
        assert "2023001" in roll_numbers
    
    @pytest.mark.asyncio
    async def test_get_student_by_roll_number(self, client: AsyncClient, test_student):
        """Test retrieving a student by roll number"""
        response = await client.get("/students/2023001")
        assert response.status_code == 200
        data = response.json()
        assert data["roll_number"] == "2023001"
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
    
    @pytest.mark.asyncio
    async def test_get_nonexistent_student(self, client: AsyncClient):
        """Test retrieving non-existent student returns 404"""
        response = await client.get("/students/9999999")
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_update_student(self, client: AsyncClient, test_student):
        """Test updating a student"""
        response = await client.put(
            "/students/2023001",
            json={
                "name": "John Updated",
                "branch": "IT",
                "year": 4,
                "email": "john.updated@example.com",
                "mobile": "9888888888"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "John Updated"
        assert data["branch"] == "IT"
        assert data["year"] == 4
        
        # Verify update persisted
        verify_response = await client.get("/students/2023001")
        verify_data = verify_response.json()
        assert verify_data["name"] == "John Updated"
        assert verify_data["branch"] == "IT"
    
    @pytest.mark.asyncio
    async def test_delete_student(self, client: AsyncClient, test_student):
        """Test deleting a student"""
        # Verify student exists
        response = await client.get("/students/2023001")
        assert response.status_code == 200
        
        # Delete student
        delete_response = await client.delete("/students/2023001")
        assert delete_response.status_code == 200
        assert "deleted" in delete_response.json()["detail"].lower()
        
        # Verify student is deleted
        verify_response = await client.get("/students/2023001")
        assert verify_response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_get_students_by_branch(self, client: AsyncClient, test_db):
        """Test filtering students by branch"""
        # Create multiple students with different branches
        await client.post(
            "/students",
            json={
                "roll_number": "2023010",
                "name": "CSE Student",
                "branch": "CSE",
                "year": 1,
                "email": "cse@example.com",
                "mobile": "9111111111"
            }
        )
        await client.post(
            "/students",
            json={
                "roll_number": "2023011",
                "name": "ECE Student",
                "branch": "ECE",
                "year": 1,
                "email": "ece@example.com",
                "mobile": "9222222222"
            }
        )
        
        # Filter by branch
        response = await client.get("/students?branch=CSE")
        assert response.status_code == 200
        data = response.json()
        for student in data:
            assert student["branch"] == "CSE"
    
    @pytest.mark.asyncio
    async def test_get_students_by_year(self, client: AsyncClient, test_db):
        """Test filtering students by year"""
        # Create students with different years
        await client.post(
            "/students",
            json={
                "roll_number": "2023020",
                "name": "Year 3 Student",
                "branch": "CSE",
                "year": 3,
                "email": "year3@example.com",
                "mobile": "9333333333"
            }
        )
        
        # Filter by year
        response = await client.get("/students?year=3")
        assert response.status_code == 200
        data = response.json()
        for student in data:
            assert student["year"] == 3


class TestStudentProfileEndpoints:
    """Test suite for student profile-related endpoints"""
    
    @pytest.mark.asyncio
    async def test_add_student_classification(self, client: AsyncClient, test_student):
        """Test adding classification to student"""
        response = await client.post(
            "/students/2023001/classification",
            json={
                "category": "General",
                "is_hosteller": True,
                "sports_quota": False,
                "is_disabled": False,
                "is_single_child": False,
                "ncc": True,
                "nss": False
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "General"
        assert data["is_hosteller"] is True
        assert data["ncc"] is True
    
    @pytest.mark.asyncio
    async def test_add_parent_details(self, client: AsyncClient, test_student):
        """Test adding parent details"""
        response = await client.post(
            "/students/2023001/parent",
            json={
                "parent_name": "Mr. Doe",
                "profession": "Engineer",
                "contact_number": "9999999990",
                "email": "parent@example.com"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["parent_name"] == "Mr. Doe"
        assert data["profession"] == "Engineer"
    
    @pytest.mark.asyncio
    async def test_add_financial_info(self, client: AsyncClient, test_student):
        """Test adding financial information"""
        response = await client.post(
            "/students/2023001/financial",
            json={
                "has_loan": False,
                "scholarship_type": "EWS",
                "scholarship_amount": "50000"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["has_loan"] is False
        assert data["scholarship_type"] == "EWS"
