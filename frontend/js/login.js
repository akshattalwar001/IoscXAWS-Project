const API = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') 
  ? "http://localhost:8000" 
  : "https://estudent-cell.onrender.com";

let currentRole = 'student'; // Track current role

// Show/hide alert
function showAlert(message, type = 'error') {
  const alertBox = document.getElementById('alertBox');
  alertBox.textContent = message;
  alertBox.className = `alert show alert-${type}`;
  
  setTimeout(() => {
    alertBox.classList.remove('show');
  }, 5000);
}

// Switch between student and admin login
function switchRole(role) {
  currentRole = role;
  
  const studentForm = document.getElementById('studentForm');
  const adminForm = document.getElementById('adminForm');
  const studentTab = document.getElementById('studentTab');
  const adminTab = document.getElementById('adminTab');
  
  if (role === 'student') {
    studentForm.style.display = 'block';
    adminForm.classList.remove('show');
    studentTab.classList.add('active');
    adminTab.classList.remove('active');
  } else {
    studentForm.style.display = 'none';
    adminForm.classList.add('show');
    studentTab.classList.remove('active');
    adminTab.classList.add('active');
  }
  
  // Clear error messages
  document.getElementById('alertBox').classList.remove('show');
}

// Submit student login form
async function submitStudentLogin(e) {
  e.preventDefault();
  
  const enrollmentNumber = document.getElementById('enrollmentNumber').value.trim();
  const password = document.getElementById('studentPassword').value;
  const submitBtn = document.getElementById('studentSubmitBtn');
  
  if (!enrollmentNumber || !password) {
    showAlert('Please fill in all fields', 'error');
    return;
  }
  
  submitBtn.disabled = true;
  submitBtn.classList.add('loading');
  
  try {
    const response = await fetch(`${API}/auth/login/student`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        enrollment_number: enrollmentNumber,
        password: password
      })
    });
    
    if (!response.ok) {
      const error = await response.json();
      showAlert(error.detail || 'Invalid credentials', 'error');
      submitBtn.disabled = false;
      submitBtn.classList.remove('loading');
      return;
    }
    
    const data = await response.json();
    
    // Store token and user info
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('role', data.role);
    localStorage.setItem('must_change_password', data.must_change_password);
    
    // Redirect based on password change requirement
    if (data.must_change_password) {
      window.location.href = 'change-password.html';
    } else {
      window.location.href = 'dashboard2.html';
    }
  } catch (error) {
    console.error('Login error:', error);
    showAlert('Connection error. Please try again.', 'error');
    submitBtn.disabled = false;
    submitBtn.classList.remove('loading');
  }
}

// Submit admin login form
async function submitAdminLogin(e) {
  e.preventDefault();
  
  const adminId = document.getElementById('adminId').value.trim();
  const password = document.getElementById('adminPassword').value;
  const submitBtn = document.getElementById('adminSubmitBtn');
  
  if (!adminId || !password) {
    showAlert('Please fill in all fields', 'error');
    return;
  }
  
  submitBtn.disabled = true;
  submitBtn.classList.add('loading');
  
  try {
    const response = await fetch(`${API}/auth/login/admin`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        admin_id: adminId,
        password: password
      })
    });
    
    if (!response.ok) {
      const error = await response.json();
      showAlert(error.detail || 'Invalid admin credentials', 'error');
      submitBtn.disabled = false;
      submitBtn.classList.remove('loading');
      return;
    }
    
    const data = await response.json();
    
    // Store token and user info
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('role', data.role);
    localStorage.setItem('must_change_password', 'false');
    
    // Redirect to dashboard
    window.location.href = 'index.html';
  } catch (error) {
    console.error('Login error:', error);
    showAlert('Connection error. Please try again.', 'error');
    submitBtn.disabled = false;
    submitBtn.classList.remove('loading');
  }
}

// Check if user is already logged in
window.addEventListener('DOMContentLoaded', () => {
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');
  
  if (token) {
    // User already logged in, redirect to appropriate page
    if (role === 'admin') {
      window.location.href = 'index.html';
    } else if (role === 'student') {
      const mustChange = localStorage.getItem('must_change_password') === 'true';
      if (mustChange) {
        window.location.href = 'change-password.html';
      } else {
        window.location.href = 'dashboard2.html';
      }
    }
  }
});
