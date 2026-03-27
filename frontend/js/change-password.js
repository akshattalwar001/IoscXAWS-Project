const API = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') 
  ? "http://localhost:8000" 
  : "https://estudent-cell.onrender.com";

// Password strength check
function checkPasswordStrength(password) {
  const strengthBar = document.getElementById('strengthBar');
  const strengthText = document.getElementById('strengthText');
  
  if (!password) {
    strengthBar.className = 'strength-bar';
    strengthText.textContent = 'Password strength: -';
    return;
  }
  
  let strength = 0;
  
  // Length check
  if (password.length >= 8) strength++;
  if (password.length >= 12) strength++;
  
  // Uppercase and lowercase
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
  
  // Numbers
  if (/[0-9]/.test(password)) strength++;
  
  // Special characters
  if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) strength++;
  
  // Determine strength level
  let level = 'weak';
  let className = 'weak';
  
  if (strength >= 4) {
    level = 'Strong';
    className = 'strong';
  } else if (strength >= 2) {
    level = 'Fair';
    className = 'fair';
  } else {
    level = 'Weak';
    className = 'weak';
  }
  
  strengthBar.className = `strength-bar ${className}`;
  strengthText.textContent = `Password strength: ${level}`;
}

// Show alert
function showAlert(message, type = 'error') {
  const alertBox = document.getElementById('alertBox');
  alertBox.textContent = message;
  alertBox.className = `alert show alert-${type}`;
  
  if (type === 'success') {
    setTimeout(() => {
      alertBox.classList.remove('show');
    }, 3000);
  }
}

// Submit change password form
async function submitChangePassword(e) {
  e.preventDefault();
  
  const currentPassword = document.getElementById('currentPassword').value;
  const newPassword = document.getElementById('newPassword').value;
  const confirmPassword = document.getElementById('confirmPassword').value;
  const submitBtn = document.getElementById('submitBtn');
  
  // Validation
  if (!currentPassword || !newPassword || !confirmPassword) {
    showAlert('Please fill in all fields', 'error');
    return;
  }
  
  if (newPassword !== confirmPassword) {
    showAlert('New passwords do not match', 'error');
    return;
  }
  
  if (newPassword.length < 8) {
    showAlert('New password must be at least 8 characters', 'error');
    return;
  }
  
  if (currentPassword === newPassword) {
    showAlert('New password must be different from current password', 'error');
    return;
  }
  
  submitBtn.disabled = true;
  
  try {
    const token = localStorage.getItem('token');
    
    if (!token) {
      showAlert('No authentication token found. Please login again.', 'error');
      window.location.href = 'login.html';
      return;
    }
    
    const response = await fetch(`${API}/auth/change-password`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        old_password: currentPassword,
        new_password: newPassword
      })
    });
    
    if (!response.ok) {
      const error = await response.json();
      showAlert(error.detail || 'Failed to change password', 'error');
      submitBtn.disabled = false;
      return;
    }
    
    // Update flag and redirect
    localStorage.setItem('must_change_password', 'false');
    showAlert('Password changed successfully! Redirecting...', 'success');
    
    setTimeout(() => {
      window.location.href = 'dashboard2.html';
    }, 1500);
  } catch (error) {
    console.error('Change password error:', error);
    showAlert('Connection error. Please try again.', 'error');
    submitBtn.disabled = false;
  }
}

// Check authentication on load
window.addEventListener('DOMContentLoaded', () => {
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');
  
  if (!token || role !== 'student') {
    window.location.href = 'login.html';
  }
});
