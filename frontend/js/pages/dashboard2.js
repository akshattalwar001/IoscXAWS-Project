// Student Dashboard Logic

async function loadStudentData() {
  try {
    const token = localStorage.getItem('token');
    
    if (!token) {
      window.location.href = 'login.html';
      return;
    }

    // Get current user info
    const user = await apiFetch(`/auth/me`);
    const enrollment_number = user.enrollment_number || user.username;

    // Set fallback values first
    document.getElementById('enrollmentNumber').textContent = enrollment_number || 'Data Not entered';
    document.getElementById('studentName').textContent = 'Enter Data in My Profile';
    document.getElementById('studentBranch').textContent = 'Enter Data in My Profile';
    document.getElementById('studentYear').textContent = 'Enter Data in My Profile';

    // Try to fetch student data if enrollment number exists
    if (enrollment_number) {
        try {
          const student = await apiFetch(`/students/${enrollment_number}`);

          document.getElementById('enrollmentNumber').textContent = student.roll_number || enrollment_number;
          document.getElementById('studentName').textContent = student.name || 'Enter Data in My Profile';
          document.getElementById('studentBranch').textContent = student.branch || 'Enter Data in My Profile';
          document.getElementById('studentYear').textContent = student.year || 'Enter Data in My Profile';
          const headerPhoto = document.getElementById('headerProfilePhoto');
          if (headerPhoto && student.photo_path) {
            const photoUrl = student.photo_path.startsWith('http') ? student.photo_path : `${API}${student.photo_path.startsWith('/') ? '' : '/'}${student.photo_path}`;
            headerPhoto.innerHTML = `<img src="${photoUrl}" alt="${student.name}" style="width: 100%; height: 100%; object-fit: cover;">`;
          }

          // Calculate Profile Completion
          console.log("Student Data:", student); let completed = 0;
          const totalDocs = 10;
          if (student.classification) completed++;
          if (student.parent_details) completed++;
          if (student.academic_records) completed++;
          if (student.financial_info) completed++;
          if (student.internships && student.internships.length > 0) completed++;
          if (student.research_papers && student.research_papers.length > 0) completed++;
          if (student.documents) completed++;
          if (student.noc_records) completed++;
          if (student.placement) completed++;
          if (student.academic_documents) completed++;

          let pcent = Math.round((completed / totalDocs) * 100); console.log("Calculated pcent:", pcent);
          const chartEl = document.getElementById('profileCompletionChart');
          const textEl = document.getElementById('profileCompletionText');
          if (chartEl && textEl) {
            chartEl.style.background = `conic-gradient(var(--accent) ${pcent}%, var(--bg-3) 0%)`;
            textEl.textContent = `${pcent}%`;
          }
        } catch (error) {
          console.log('Could not fetch student details:', error);
          document.getElementById('studentName').textContent = "Err: " + error.message;
          // If the profile fetch fails, the enrollment number should remain set from line 22
        }
    }
  } catch (error) {
    console.error('Error loading student data:', error);
  }
}

// Show account settings
function showAccountSettings() {
  alert('Account settings will be available soon. You can currently change your password in your profile settings.');
}

// Load data on page load
document.addEventListener('DOMContentLoaded', () => {
  // Check if user is logged in as student
  const role = localStorage.getItem('role');
  const token = localStorage.getItem('token');
  
  if (!token || role !== 'student') {
    window.location.href = 'login.html';
    return;
  }

  loadStudentData();
});
