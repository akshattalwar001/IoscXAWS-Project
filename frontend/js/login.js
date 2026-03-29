document.addEventListener('DOMContentLoaded', () => {
  // ----------------------------------------------------
  // Session Recognition & Redirect
  // ----------------------------------------------------
  const token = localStorage.getItem('token');
  const savedRole = localStorage.getItem('role');

  if (token) {
    if (savedRole === 'admin') {
      window.location.href = 'admin-dashboard.html'; // Adjust to admin dashboard
    } else if (savedRole === 'student') {
      const mustChange = localStorage.getItem('must_change_password') === 'true';
      if (mustChange) {
        window.location.href = 'change-password.html';
      } else {
        window.location.href = 'dashboard2.html';
      }
    }
  }

  // ----------------------------------------------------
  // DOM Elements
  // ----------------------------------------------------
  const form = document.getElementById('loginForm');
  const usernameInput = document.getElementById('username');
  const passwordInput = document.getElementById('password');
  const usernameLabel = document.getElementById('usernameLabel');
  const alertBox = document.getElementById('alertBox');
  const submitBtn = document.getElementById('submitBtn');
  const btnText = document.getElementById('btnText');
  const togglePwdBtn = document.getElementById('togglePassword');
  const eyeIcon = document.getElementById('eyeIcon');
  const eyeOffIcon = document.getElementById('eyeOffIcon');
  const roleButtons = document.querySelectorAll('.role-btn');
  const rememberMeCheck = document.getElementById('rememberMe');
  const forgotPwdLink = document.querySelector('.forgot-pwd');

  let currentRole = 'student'; // Default role

  // Environment-based API determination
  const API_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') 
    ? "http://localhost:8000" 
    : "https://estudent-cell.onrender.com";

  // ----------------------------------------------------
  // Pre-fill Remember Me
  // ----------------------------------------------------
  const savedUsername = localStorage.getItem('savedUsername');
  if (savedUsername) {
    usernameInput.value = savedUsername;
    rememberMeCheck.checked = true;
  }

  // ----------------------------------------------------
  // Role Toggling Logic
  // ----------------------------------------------------
  roleButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault(); // Prevent accidental form triggers if any
      
      // Update UI state
      roleButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      // Update data state
      currentRole = btn.getAttribute('data-role');
      
      // Update form presentation based on role
      if (currentRole === 'student') {
        usernameLabel.textContent = 'Enrollment Number';
        usernameInput.placeholder = 'e.g., 5919051924';
      } else {
        usernameLabel.textContent = 'Admin ID ';
        usernameInput.placeholder = 'e.g., AdminIA100';
      }
      
      // Clear warnings / inputs on switch
      hideAlert();
      passwordInput.value = '';
      
      // Only clear username if Remember Me is not in effect for that role
      if (!savedUsername || !rememberMeCheck.checked) {
        usernameInput.value = '';
      }
    });
  });

  // ----------------------------------------------------
  // Password Visibility Toggle
  // ----------------------------------------------------
  togglePwdBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const isPassword = passwordInput.getAttribute('type') === 'password';
    passwordInput.setAttribute('type', isPassword ? 'text' : 'password');
    
    if (isPassword) {
      eyeIcon.style.display = 'none';
      eyeOffIcon.style.display = 'block';
    } else {
      eyeIcon.style.display = 'block';
      eyeOffIcon.style.display = 'none';
    }
  });

  // ----------------------------------------------------
  // Forgot Password
  // ----------------------------------------------------
  forgotPwdLink.addEventListener('click', (e) => {
    e.preventDefault();
    alert("If unchanged, the preset password is your Father's Name in ALL CAPS. Otherwise, contact Admin.");
  });

  // ----------------------------------------------------
  // Alert Helpers
  // ----------------------------------------------------
  function showAlert(message) {
    alertBox.textContent = message;
    alertBox.classList.add('show');
  }

  function hideAlert() {
    alertBox.textContent = '';
    alertBox.classList.remove('show');
  }

  // ----------------------------------------------------
  // Form Submission
  // ----------------------------------------------------
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    hideAlert();

    const username = usernameInput.value.trim();
    const password = passwordInput.value;

    // Client-side Validation
    if (!username || !password) {
      showAlert('All fields are required.');
      return;
    }

    // Set Loading State
    submitBtn.disabled = true;
    submitBtn.classList.add('loading');
    btnText.textContent = 'Logging in...';

    // Build endpoint dynamically
    const endpoint = currentRole === 'student' 
      ? `${API_URL}/auth/login/student` 
      : `${API_URL}/auth/login/admin`;

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
      });

      const data = await response.json();

      if (!response.ok) {
        // 4xx or 5xx Response
        throw new Error(data.detail || 'Invalid credentials');
      }

      // Handle Remember Me
      if (rememberMeCheck.checked) {
        localStorage.setItem('savedUsername', username);
      } else {
        localStorage.removeItem('savedUsername');
      }

      // Success - Store token & role
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('role', currentRole);
      
      // Optional: Handle must_change_password logic
      if (data.must_change_password !== undefined) {
        localStorage.setItem('must_change_password', data.must_change_password);
      }

      // Redirect based on role
      if (currentRole === 'admin') {
        window.location.href = 'admin-dashboard.html';
      } else {
        if (data.must_change_password) {
          window.location.href = 'change-password.html';
        } else {
          window.location.href = 'dashboard2.html';
        }
      }

    } catch (error) {
      console.error('Login error:', error);
      showAlert(error.message || 'Network error. Please try again later.');
    } finally {
      // Revert loading state if not redirecting immediately
      submitBtn.disabled = false;
      submitBtn.classList.remove('loading');
      btnText.textContent = 'Sign In';
    }
  });

});
