let allStudents = [];
let deleteTargetId = null;

function getPhotoUrl(photo_path) {
  if (!photo_path) return null;
  if (photo_path.startsWith("http://") || photo_path.startsWith("https://")) {
    return photo_path;
  }
  return `${API}/${photo_path}`;
}

async function loadStudents(branch = "", year = "") {
  const tbody = document.getElementById("studentsTableBody");
  tbody.innerHTML = '<tr><td colspan="7" class="table-empty">Loading...</td></tr>';

  try {
    let url = "/students";
    const params = new URLSearchParams();
    if (branch) params.append("branch", branch);
    if (year) params.append("year", year);
    if (params.toString()) url += "?" + params.toString();

    allStudents = await apiFetch(url);
    renderTable(allStudents);
  } catch (e) {
    tbody.innerHTML = `<tr><td colspan="7" class="table-empty">Error: ${e.message}</td></tr>`;
  }
}

function renderTable(students) {
  const tbody = document.getElementById("studentsTableBody");

  if (students.length === 0) {
    tbody.innerHTML = '<tr><td colspan="8" class="table-empty">No students found</td></tr>';
    return;
  }

  tbody.innerHTML = students.map(s => `
    <tr>
      <td>
        ${s.photo_path
          ? `<img src="${getPhotoUrl(s.photo_path)}" class="student-photo" alt="${s.name}"/>`
          : `<div class="student-photo-placeholder">${s.name.charAt(0).toUpperCase()}</div>`
        }
      </td>
      <td><span class="roll-badge">${s.roll_number}</span></td>
      <td>${s.name}</td>
      <td><span class="branch-badge">${s.branch}</span></td>
      <td><span class="year-badge">Year ${s.year}</span></td>
      <td>${s.email}</td>
      <td>${s.mobile}</td>
      <td>
        <div class="action-btns">
          <a href="profile.html?id=${s.id}" class="btn btn-ghost btn-sm">View</a>
          <button class="btn btn-danger btn-sm" onclick="promptDelete(${s.id})">Delete</button>
        </div>
      </td>
    </tr>
  `).join("");
}
document.getElementById("searchInput").addEventListener("input", (e) => {
  const query = e.target.value.toLowerCase().trim();
  if (!query) {
    renderTable(allStudents);
    return;
  }
  const filtered = allStudents.filter(s =>
    s.name.toLowerCase().includes(query) ||
    s.roll_number.toLowerCase().includes(query)
  );
  renderTable(filtered);
});

function promptDelete(id) {
  deleteTargetId = String(id);
  document.getElementById("deleteModal").classList.add("visible");
}

document.getElementById("cancelDelete").addEventListener("click", () => {
  deleteTargetId = null;
  document.getElementById("deleteModal").classList.remove("visible");
});

document.getElementById("confirmDelete").addEventListener("click", async () => {
  if (!deleteTargetId) return;
  try {
    await apiFetch(`/students/${deleteTargetId}`, { method: "DELETE" });
    document.getElementById("deleteModal").classList.remove("visible");
    deleteTargetId = null;
    loadStudents();
  } catch (e) {
    alert("Delete failed: " + e.message);
  }
});

document.getElementById("applyFilters").addEventListener("click", () => {
  const branch = document.getElementById("filterBranch").value;
  const year = document.getElementById("filterYear").value;
  loadStudents(branch, year);
});

document.getElementById("clearFilters").addEventListener("click", () => {
  document.getElementById("filterBranch").value = "";
  document.getElementById("filterYear").value = "";
  loadStudents();
});

document.getElementById("downloadPdfBtn").addEventListener("click", () => {
  try {
    const doc = new window.jsPDF();
    
    doc.text("Student List", 14, 15);
    
    const query = document.getElementById("searchInput").value.toLowerCase().trim();
    let studentsToPrint = allStudents;
    if (query) {
      studentsToPrint = allStudents.filter(s =>
        s.name.toLowerCase().includes(query) ||
        s.roll_number.toLowerCase().includes(query)
      );
    }
    
    const headers = [["Roll Number", "Name", "Branch", "Year", "Email", "Mobile"]];
    const data = studentsToPrint.map(s => [
      s.roll_number || "-",
      s.name || "-",
      s.branch || "-",
      s.year || "-",
      s.email || "-",
      s.mobile || "-"
    ]);

    doc.autoTable({
      head: headers,
      body: data,
      startY: 20,
      styles: { fontSize: 8 },
      headStyles: { fillColor: [79, 70, 229] }
    });

    doc.save("students_list.pdf");
  } catch (err) {
    console.error(err);
    alert("An error occurred while generating the PDF: " + err.message);
  }
});

loadStudents();