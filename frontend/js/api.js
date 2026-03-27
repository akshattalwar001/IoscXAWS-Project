const API = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
  ? "http://localhost:8000"
  : "https://estudent-cell.onrender.com";

async function apiFetch(path, options = {}) {
  const res = await fetch(API + path, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(err.detail || "Request failed");
  }
  return res.json();
}
async function checkApiStatus() {
  const el = document.getElementById("apiStatus");
  try {
    await fetch(API + "/");
    el.className = "api-status online";
    el.querySelector(".status-text").textContent = "API Online";
  } catch {
    el.className = "api-status offline";
    el.querySelector(".status-text").textContent = "API Offline";
  }
}

checkApiStatus();

function showAlert(containerId, message, type = "success") {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
  setTimeout(() => { el.innerHTML = ""; }, 4000);
}

function boolDisplay(val) {
  return val
    ? '<span class="bool-yes">✓ Yes</span>'
    : '<span class="bool-no">— No</span>';
}

document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.querySelector(".sidebar");
  const sidebarToggle = document.getElementById("sidebarToggle");
  const navItems = document.querySelectorAll(".sidebar-nav a");
  const body = document.documentElement.parentElement;
  
  const STORAGE_KEY = "sidebar-collapsed";
  const BREAKPOINT = 980;
  
  // Initialize sidebar state from localStorage
  function initSidebar() {
    const isCollapsed = localStorage.getItem(STORAGE_KEY) === "true";
    const isMobile = window.innerWidth <= BREAKPOINT;
    
    if (isMobile) {
      sidebar.classList.add("mobile-drawer");
      sidebar.classList.remove("collapsed", "visible");
    } else {
      sidebar.classList.remove("mobile-drawer", "visible");
      body.classList.remove("sidebar-open");
      if (isCollapsed) {
        sidebar.classList.add("collapsed");
      } else {
        sidebar.classList.remove("collapsed");
      }
    }
  }
  
  // Toggle sidebar collapsed state (desktop only)
  function toggleSidebarCollapse() {
    const isMobile = window.innerWidth <= BREAKPOINT;
    if (isMobile) return;
    
    sidebar.classList.toggle("collapsed");
    const isCollapsed = sidebar.classList.contains("collapsed");
    localStorage.setItem(STORAGE_KEY, isCollapsed);
  }
  
  // Toggle sidebar visibility (mobile drawer)
  function toggleSidebarMobile() {
    const isMobile = window.innerWidth <= BREAKPOINT;
    if (!isMobile) return;
    
    sidebar.classList.toggle("visible");
    body.classList.toggle("sidebar-open");
  }
  
  // Close sidebar on mobile when nav item is clicked
  function closeMobileSidebar() {
    const isMobile = window.innerWidth <= BREAKPOINT;
    if (isMobile) {
      sidebar.classList.remove("visible");
      body.classList.remove("sidebar-open");
    }
  }
  
  // Handle window resize
  function handleResize() {
    const body = document.documentElement.parentElement;
    const isMobile = window.innerWidth <= BREAKPOINT;
    
    if (isMobile && !sidebar.classList.contains("mobile-drawer")) {
      sidebar.classList.add("mobile-drawer");
      sidebar.classList.remove("collapsed", "visible");
      body.classList.remove("sidebar-open");
    } else if (!isMobile && sidebar.classList.contains("mobile-drawer")) {
      sidebar.classList.remove("mobile-drawer", "visible");
      body.classList.remove("sidebar-open");
      const isCollapsed = localStorage.getItem(STORAGE_KEY) === "true";
      if (isCollapsed) {
        sidebar.classList.add("collapsed");
      } else {
        sidebar.classList.remove("collapsed");
      }
    }
  }
  
  // Event listeners
  const mobileMenuToggle = document.getElementById("mobileMenuToggle");
  if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener("click", () => {
      const isMobile = window.innerWidth <= BREAKPOINT;
      if (isMobile) {
        toggleSidebarMobile();
      }
    });
  }
  
  if (sidebarToggle) {
    sidebarToggle.addEventListener("click", () => {
      const isMobile = window.innerWidth <= BREAKPOINT;
      if (isMobile) {
        toggleSidebarMobile();
      } else {
        toggleSidebarCollapse();
      }
    });
  }
  
  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      if (confirm("Are you sure you want to logout?")) {
        window.location.href = "/login";
      }
    });
  }
  
  navItems.forEach(item => {
    item.addEventListener("click", closeMobileSidebar);
  });
  
  // Close sidebar when clicking the overlay backdrop
  if (body) {
    body.addEventListener("click", (e) => {
      const isMobile = window.innerWidth <= BREAKPOINT;
      if (isMobile && sidebar.classList.contains("visible") && e.target === body) {
        closeMobileSidebar();
      }
    });
  }
  
  // Theme Toggle Functionality
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
  
  // Initialize theme on page load
  initTheme();
  
  window.addEventListener("resize", handleResize);
  
  // Initialize
  if (sidebar) {
    initSidebar();
  }
});