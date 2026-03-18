async function loadDashboard() {
  try {
    const stats = await apiFetch("/dashboard/stats");

    document.getElementById("totalStudents").textContent = stats.total_students;
    document.getElementById("hostellers").textContent = stats.hostellers;
    document.getElementById("dayScholars").textContent = stats.day_scholars;
    document.getElementById("placed").textContent = stats.placed_count;
    document.getElementById("ncc").textContent = stats.ncc_count;
    document.getElementById("nss").textContent = stats.nss_count;
    document.getElementById("loans").textContent = stats.loan_count;
    document.getElementById("internships").textContent = stats.internship_count;

    document.querySelectorAll(".stat-card").forEach(c => c.classList.remove("loading"));

    renderBarChart("branchChart", stats.branch_wise);
    renderBarChart("yearChart", stats.year_wise);
    renderBarChart("categoryChart", stats.category_breakdown);
    renderBarChart("scholarshipChart", stats.scholarship_breakdown);
  } catch (e) {
    console.error("Dashboard load failed:", e);
  }
}

function renderBarChart(containerId, data) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const entries = Object.entries(data);
  if (entries.length === 0) {
    container.innerHTML = '<p class="no-data">No data yet</p>';
    return;
  }

  const max = Math.max(...entries.map(([, v]) => v)) || 1;

  container.innerHTML = entries.map(([label, count]) => `
    <div class="bar-row">
      <span class="bar-label">${label}</span>
      <div class="bar-track">
        <div class="bar-fill" style="width: ${(count / max) * 100}%"></div>
      </div>
      <span class="bar-count">${count}</span>
    </div>
  `).join("");
}

loadDashboard();