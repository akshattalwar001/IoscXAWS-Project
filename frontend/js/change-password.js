const API = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') 
  ? "http://localhost:8000" 
  : "https://ggsipuedc.in";

// Toggle password visibility
function togglePasswordVisibility(inputId, eyeIconId, eyeOffIconId) {
  const input = document.getElementById(inputId);
  const eyeIcon = document.getElementById(eyeIconId);
  const eyeOffIcon = document.getElementById(eyeOffIconId);
  
  if (input.type === 'password') {
    input.type = 'text';
    eyeIcon.style.display = 'none';
    eyeOffIcon.style.display = 'block';
  } else {
    input.type = 'password';
    eyeIcon.style.display = 'block';
    eyeOffIcon.style.display = 'none';
  }
}

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
  
  if (password.length >= 8) strength++;
  if (password.length >= 12) strength++;
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
  if (/[0-9]/.test(password)) strength++;
  if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) strength++;
  
  let level, className;
  
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

// Extract a readable error message from any API response shape
async function extractErrorMessage(response, fallback = 'Something went wrong. Please try again.') {
  try {
    const data = await response.json();
    if (typeof data === 'string') return data;
    if (typeof data.detail === 'string') return data.detail;
    if (Array.isArray(data.detail)) return data.detail.map(e => e.msg || JSON.stringify(e)).join(', ');
    if (typeof data.message === 'string') return data.message;
    if (typeof data.error === 'string') return data.error;
    return JSON.stringify(data);
  } catch {
    return fallback;
  }
}

// Submit change password form
async function submitChangePassword(e) {
  e.preventDefault();
  
  const currentPassword = document.getElementById('currentPassword').value;
  const newPassword = document.getElementById('newPassword').value;
  const confirmPassword = document.getElementById('confirmPassword').value;
  const submitBtn = document.getElementById('submitBtn');
  
  if (!currentPassword || !newPassword || !confirmPassword) {
    showAlert('Please fill in all password fields', 'error');
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

    const pwdResponse = await fetch(`${API}/account/change-password`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ old_password: currentPassword, new_password: newPassword })
    });
    
    if (!pwdResponse.ok) {
      const message = await extractErrorMessage(pwdResponse, 'Failed to change password');
      showAlert(message, 'error');
      submitBtn.disabled = false;
      return;
    }
    
localStorage.setItem('must_change_password', 'false');
showAlert('Password changed successfully! Redirecting...', 'success');

setTimeout(() => {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
  window.location.href = 'login.html';
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

// Theme Toggle Functionality
document.addEventListener('DOMContentLoaded', () => {
  const THEME_KEY = "theme-preference";
  const themeToggle = document.getElementById("themeToggle");
  const themeLabel = document.getElementById("themeLabel");
  const htmlElement = document.documentElement;
  
  function initTheme() {
    const savedTheme = localStorage.getItem(THEME_KEY) || "light";
    if (savedTheme === "dark") {
      htmlElement.classList.add("dark-mode");
      if (themeLabel) themeLabel.textContent = "Dark";
    } else {
      htmlElement.classList.remove("dark-mode");
      if (themeLabel) themeLabel.textContent = "Light";
    }
  }
  
  function toggleTheme() {
    const isDarkMode = htmlElement.classList.toggle("dark-mode");
    const theme = isDarkMode ? "dark" : "light";
    localStorage.setItem(THEME_KEY, theme);
    if (themeLabel) themeLabel.textContent = isDarkMode ? "Dark" : "Light";
  }
  
  if (themeToggle) {
    themeToggle.addEventListener("click", toggleTheme);
  }
  
  initTheme();
});