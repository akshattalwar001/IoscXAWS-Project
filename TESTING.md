# 🧪 Backend & Frontend Connectivity Testing Guide

## Overview
This testing suite verifies that the backend API works correctly and that the frontend JavaScript can properly communicate with it.

## Test Files

### 1. `tests/conftest.py`
**Purpose**: Shared test fixtures and configuration
- Test database setup (SQLite in-memory)
- Async client for HTTP testing
- User fixtures (student, admin)
- Authentication token fixtures

### 2. `tests/test_connectivity.py`
**Purpose**: Backend API connectivity and response format tests
- Backend API accessibility
- Authentication endpoint verification
- Student endpoints functionality
- Password change endpoint
- Error handling and status codes

### 3. `tests/test_frontend_connectivity.py`
**Purpose**: Frontend-specific compatibility tests
- Tests that frontend JavaScript can work with API
- Verifies request/response format matches frontend expectations
- Tests JSON response structures
- Validates error handling for frontend

## Getting Started

### Step 1: Install Test Dependencies
```bash
pip install pytest pytest-asyncio httpx aiosqlite
```

### Step 2: Run All Tests
```bash
pytest tests/ -v
```

### Step 3: Run Specific Test Groups

#### Test Backend Connectivity Only
```bash
pytest tests/test_connectivity.py -v
```

#### Test Frontend Compatibility Only
```bash
pytest tests/test_frontend_connectivity.py -v
```

#### Test Specific Test Class
```bash
# Test authentication flow
pytest tests/test_connectivity.py::TestAuthenticationFlow -v

# Test student endpoints
pytest tests/test_connectivity.py::TestStudentEndpoints -v

# Test frontend login integration
pytest tests/test_frontend_connectivity.py::TestFrontendLoginJS -v
```

#### Test Specific Test Case
```bash
# Test student login endpoint
pytest tests/test_connectivity.py::TestAuthenticationFlow::test_student_login_with_json -v

# Test student profile loading
pytest tests/test_frontend_connectivity.py::TestFrontendProfileJS::test_frontend_load_student_profile -v
```

## Understanding the Tests

### Backend Connectivity Tests (`test_connectivity.py`)

#### TestBackendConnectivity
Verifies basic API accessibility:
- ✅ API root endpoint responds
- ✅ Student login endpoint exists
- ✅ Admin login endpoint exists
- ✅ Password change endpoint exists
- ✅ Students list endpoint exists
- ✅ API returns JSON (not HTML)
- ✅ CORS headers present (if configured)

#### TestAuthenticationFlow
Tests the three authentication endpoints:
- ✅ `/auth/login/student` - Student JSON login
- ✅ `/auth/login/admin` - Admin JSON login
- ✅ `/auth/change-password` - Change password for authenticated users
- ✅ Role validation (student can't use admin endpoint)
- ✅ Token response format matches OAuth2

#### TestStudentEndpoints
Tests CRUD operations:
- ✅ GET `/students` - List all students
- ✅ GET `/students/{roll_number}` - Get single student
- ✅ POST `/students` - Create new student
- ✅ Response includes all expected fields

#### TestChangePasswordEndpoint
Tests password change:
- ✅ Successfully change password with correct old password
- ✅ Reject change with wrong old password
- ✅ Require authentication
- ✅ Return proper response format

#### TestAPIErrorHandling
Tests error responses:
- ✅ 401 Unauthorized without token
- ✅ 404 Not Found for missing resources
- ✅ Error messages are JSON with detail field
- ✅ Invalid tokens are rejected

### Frontend Compatibility Tests (`test_frontend_connectivity.py`)

#### TestFrontendLoginJS
Simulates `frontend/js/login.js`:
- ✅ Student login with JSON format
- ✅ Admin login with JSON format
- ✅ Error response format matches expectations

#### TestFrontendChangePasswordJS
Simulates `frontend/js/change-password.js`:
- ✅ Change password request format
- ✅ Error handling

#### TestFrontendStudentsJS
Simulates `frontend/js/pages/students.js`:
- ✅ Fetch students list
- ✅ Profile link uses roll_number (not id)
- ✅ Delete student request format
- ✅ Add student request format

#### TestFrontendProfileJS
Simulates `frontend/js/pages/profile.js`:
- ✅ Load student profile by roll_number
- ✅ Response includes all profile fields
- ✅ Data types match frontend expectations

#### TestAPIResponseFormat
Validates JSON response structure:
- ✅ All responses are JSON
- ✅ Error responses have consistent structure
- ✅ Token responses follow OAuth2 standard

#### TestFrontendAPIConfiguration
Tests API configuration:
- ✅ API is accessible
- ✅ Responses are JSON (not HTML)
- ✅ Multiple requests work with same token

## Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run Backend Tests Only
```bash
pytest tests/test_connectivity.py -v
```

### Run Frontend Compatibility Tests Only
```bash
pytest tests/test_frontend_connectivity.py -v
```

### Run with Coverage Report
```bash
pytest tests/ --cov=app --cov-report=term-missing
```

### Run Specific Test Class
```bash
pytest tests/test_connectivity.py::TestAuthenticationFlow -v
```

### Run Single Test
```bash
pytest tests/test_connectivity.py::TestAuthenticationFlow::test_student_login_with_json -v
```

### Run and Stop on First Failure
```bash
pytest tests/ -x
```

### Run with Detailed Output
```bash
pytest tests/ -vv -s
```

## Test Output Examples

### Successful Tests
```
tests/test_connectivity.py::TestAuthenticationFlow::test_student_login_with_json PASSED
tests/test_frontend_connectivity.py::TestFrontendProfileJS::test_frontend_load_student_profile PASSED
======================== 2 passed in 0.05s ========================
```

### Failed Test
```
tests/test_connectivity.py::TestStudentEndpoints::test_get_students_list FAILED
AssertionError: assert 404 == 200
```

## Troubleshooting

### Tests Fail with "Cannot connect to database"
**Solution**: Tests use in-memory SQLite database. No setup needed. If error persists:
```bash
pip install aiosqlite
```

### Tests Fail with "Module not found"
**Solution**: Install all requirements:
```bash
pip install -r requirements.txt
pip install pytest pytest-asyncio httpx aiosqlite
```

### Tests Hang or Timeout
**Solution**: Check event loop configuration. Reset with:
```bash
pytest tests/ --co -q  # Verify test collection
pytest tests/ -p no:asyncio  # Disable asyncio auto-use
```

### Specific Test Fails
Run with more verbose output and full stack trace:
```bash
pytest tests/test_connectivity.py::TestAuthenticationFlow::test_student_login_with_json -vv --tb=long
```

## Integration Test Workflows

### Complete Login Flow
```bash
pytest tests/test_frontend_connectivity.py::TestFrontendLoginJS -v
```

### Complete Student Management Flow
```bash
pytest tests/test_frontend_connectivity.py::TestFrontendStudentsJS -v
```

### Complete Profile Access Flow
```bash
pytest tests/test_frontend_connectivity.py::TestFrontendProfileJS -v
```

## Continuous Integration Setup

Add to `.github/workflows/tests.yml`:
```yaml
name: Run Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: pip install pytest pytest-asyncio httpx aiosqlite
      - run: pytest tests/ -v
```

## Extending Tests

To add a new test:

```python
@pytest.mark.asyncio
async def test_new_endpoint(self, test_client, student_token):
    """Test description."""
    response = await test_client.get(
        "/new-endpoint",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "expected_field" in data
```

Add to appropriate test class in:
- `test_connectivity.py` - for backend/API tests
- `test_frontend_connectivity.py` - for frontend compatibility

## Performance Profiling

See which tests are slowest:
```bash
pytest tests/ --durations=10
```

## Test Coverage

Generate HTML coverage report:
```bash
pip install pytest-cov
pytest tests/ --cov=app --cov-report=html
# Open: htmlcov/index.html
```

View coverage in terminal:
```bash
pytest tests/ --cov=app --cov-report=term-missing
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `pytest tests/ -v` | Run all tests with verbose output |
| `pytest tests/test_connectivity.py -v` | Run backend tests only |
| `pytest tests/test_frontend_connectivity.py -v` | Run frontend tests only |
| `pytest tests/ -x` | Stop on first failure |
| `pytest tests/ -k student` | Run tests matching "student" |
| `pytest tests/ --collect-only` | List all tests without running |
| `pytest tests/ -vv -s` | Very verbose with print statements |
| `pytest tests/ --tb=short` | Short traceback format |

---

**All tests verify that the frontend can successfully interact with the backend API.**
```

### Run Tests with Coverage
First install coverage:
```bash
pip install pytest-cov
```

Then run:
```bash
pytest --cov=app --cov-report=html
```

### Run Only Async Tests
```bash
pytest -m asyncio
```

## Test Structure

### conftest.py
Global pytest configuration with fixtures:
- `event_loop` - Event loop for async tests
- `test_db` - Test database session
- `client` - Async HTTP test client with dependency overrides
- `test_user_admin` - Pre-created admin user
- `test_user_student` - Pre-created student user
- `test_student` - Pre-created student record

### test_auth.py
Tests for authentication endpoints:
- Student login (`/auth/login/student`)
- Admin login (`/auth/login/admin`)
- Password change (`/auth/change-password`)
- OAuth2 token endpoint (`/auth/token`)
- Error cases and validation

### test_student.py
Tests for student endpoints:
- Create student (`POST /students`)
- Get all students (`GET /students`)
- Get student by roll number (`GET /students/{roll_number}`)
- Update student (`PUT /students/{roll_number}`)
- Delete student (`DELETE /students/{roll_number}`)
- Filter students by branch and year
- Student profile endpoints (classification, parent, financial)

## Test Coverage

### Current Test Coverage
- ✅ Authentication (11 tests)
- ✅ Student CRUD (9 tests)
- ✅ Student profiles (3 tests)

**Total: 23 tests**

### What's Tested
- ✅ Successful login for students and admins
- ✅ Role-based access control (student can't login as admin)
- ✅ Password change functionality
- ✅ Password verification on login
- ✅ Student CRUD operations (Create, Read, Update, Delete)
- ✅ Filtering and search
- ✅ Adding student profile data
- ✅ Error handling (401, 403, 404 errors)
- ✅ Authentication required endpoints

## Debugging Tests

### Run with Print Output
```bash
pytest -s test_auth.py::TestAuthenticationEndpoints::test_login_student_success
```

The `-s` flag shows print statements and logging output.

### Drop into Debugger on Failure
```bash
pytest --pdb test_auth.py
```

### Show Local Variables on Failure
```bash
pytest -l test_auth.py
```

## Common Issues

### "database does not exist" Error
**Solution**: Make sure your test database is created or use an in-memory database:
```python
TEST_DATABASE_URL=sqlite+aiosqlite:///:memory:
```

### AsyncIO Event Loop Error
**Solution**: This is handled by the `event_loop` fixture in conftest.py. If you still get errors, ensure `pytest-asyncio` is installed:
```bash
pip install --upgrade pytest-asyncio
```

### Import Errors
**Solution**: Make sure you're running pytest from the project root directory:
```bash
cd /path/to/IoscXAWS-Project
pytest
```

## Continuous Integration

For CI/CD pipelines, use:
```bash
pytest --cov=app --cov-report=xml --junit-xml=junit.xml
```

This generates:
- `junit.xml` - Test results in JUnit format
- Coverage report in XML format for CI tools

## Writing New Tests

Example test structure:
```python
import pytest
from httpx import AsyncClient

class TestNewFeature:
    """Test suite for new feature"""
    
    @pytest.mark.asyncio
    async def test_some_functionality(self, client: AsyncClient, test_user_student):
        """Test description"""
        # Setup
        test_data = {...}
        
        # Execute
        response = await client.post("/endpoint", json=test_data)
        
        # Assert
        assert response.status_code == 200
        assert response.json()["key"] == "value"
```

## Best Practices

1. **Use fixtures**: Leverage conftest.py fixtures for common setup
2. **Name tests clearly**: `test_<action>_<condition>_<expected_result>`
3. **Test error cases**: Include negative tests (401, 404, etc.)
4. **Keep tests isolated**: Each test should be independent
5. **Use parametrize for similar tests**: 
   ```python
   @pytest.mark.parametrize("username,password,expected", [
       ("user1", "pass1", 200),
       ("user1", "wrong", 401),
   ])
   ```

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [httpx documentation](https://www.python-httpx.org/)
