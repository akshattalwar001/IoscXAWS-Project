let studentId = null;

let isStudentNew = false;
let studentData = null;
let classificationExists = false;
let parentExists = false;
let financialExists = false;
let documentsExists = false;
let nocExists = false;
let placementExists = false;
let acadocsExists = false;

function getPhotoUrl(photo_path) {
  if (!photo_path) return null;
  if (photo_path.startsWith("http://") || photo_path.startsWith("https://")) {
    return photo_path;
  }
  return `${API}${photo_path.startsWith('/') ? '' : '/'}${photo_path}`;
}

function toggleCustomScholarship(value) {
  const group = document.getElementById("customScholarshipGroup");
  group.style.display = value === "Other" ? "block" : "none";
}

async function loadProfile() {
  try {
    const me = await apiFetch(`/auth/me`);
    const enrollNo = me.enrollment_number || me.username;
    
    if (!enrollNo) {
        window.location.href = 'login.html';
        return;
    }
    studentId = enrollNo;

    // Fallback UI
    const el = document.getElementById("enrollmentNumber"); if (el) el.textContent = studentId;
    document.getElementById("profileMeta").textContent = "Data Not entered";

    try {
      studentData = await apiFetch(`/students/${studentId}`);
      isStudentNew = false;
    } catch (e) {
      isStudentNew = true;
      studentData = { roll_number: studentId, name: 'Data Not entered', branch: 'Data Not entered', year: 1, email: '', mobile: '' };
    }

    renderBasicInfo(studentData);
    renderClassification(studentData.classification);
    renderParent(studentData.parent_details);
    renderFinancial(studentData.financial_info);
    renderInternships(studentData.internships);
    renderResearch(studentData.research_papers);
    renderDocuments(studentData.documents);
    renderNoc(studentData.noc_records);
    renderPlacement(studentData.placement);
    renderAcadocs(studentData.academic_documents);

    classificationExists = !!studentData.classification;
    parentExists = !!studentData.parent_details;
    financialExists = !!studentData.financial_info;
    documentsExists = !!studentData.documents;
    nocExists = !!studentData.noc_records;
    placementExists = !!studentData.placement;
    acadocsExists = !!studentData.academic_documents;
  } catch (e) {
    const errEl = document.getElementById("enrollmentNumber"); if (errEl) errEl.textContent = "Error loading student";
  }
}

function renderBasicInfo(s) {
  const el = document.getElementById("enrollmentNumber"); if (el) el.textContent = s.roll_number;
  document.getElementById("profileMeta").textContent = `${s.name} · ${s.branch} · Year ${s.year}`;

  const headerPhoto = document.getElementById("headerProfilePhoto");
  if (headerPhoto) {
    if (s.photo_path) {
      headerPhoto.innerHTML = `<img src="${getPhotoUrl(s.photo_path)}" alt="${s.name}" style="width: 100%; height: 100%; object-fit: cover;">`;
    } else {
      headerPhoto.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`;
    }
  }

  document.getElementById("basicInfoView").innerHTML = `
    <div class="section-header">
      <h3 class="section-title">Basic Info</h3>
    </div>
    <div style="margin-bottom: 20px;">
      ${s.photo_path ? `<img src="${getPhotoUrl(s.photo_path)}" alt="Profile Photo" style="width: 150px; height: 150px; border-radius: 5px; object-fit: cover;">` : `<div style="width:150px;height:150px;background:#eee;border-radius:5px;display:flex;align-items:center;justify-content:center;color:#999;">No Photo</div>`}
    </div>
    <div class="info-grid">
      <div class="info-item"><span class="info-label">Roll Number</span><span class="info-value mono">${s.roll_number}</span></div>
      <div class="info-item"><span class="info-label">Name</span><span class="info-value">${s.name}</span></div>
      <div class="info-item"><span class="info-label">Branch</span><span class="info-value">${s.branch}</span></div>
      <div class="info-item"><span class="info-label">Year</span><span class="info-value">Year ${s.year}</span></div>
      <div class="info-item"><span class="info-label">Email</span><span class="info-value">${s.email}</span></div>
      <div class="info-item"><span class="info-label">Mobile</span><span class="info-value mono">${s.mobile}</span></div>
      <div class="info-item"><span class="info-label">Address</span><span class="info-value">${s.address || '—'}</span></div>
    </div>
  `;
}

function renderClassification(c) {
  const el = document.getElementById("classificationView");
  if (!c) { el.innerHTML = '<p class="no-data">No classification added yet.</p>'; return; }
  el.innerHTML = `
    <div class="info-grid">
      <div class="info-item"><span class="info-label">Category</span><span class="info-value">${c.category}</span></div>
      <div class="info-item"><span class="info-label">Hosteller</span><span class="info-value">${boolDisplay(c.is_hosteller)}</span></div>
      <div class="info-item"><span class="info-label">Sports Quota</span><span class="info-value">${boolDisplay(c.sports_quota)}</span></div>
      <div class="info-item"><span class="info-label">Disabled</span><span class="info-value">${boolDisplay(c.is_disabled)}</span></div>
      <div class="info-item"><span class="info-label">Single Child</span><span class="info-value">${boolDisplay(c.is_single_child)}</span></div>
      <div class="info-item"><span class="info-label">NCC</span><span class="info-value">${boolDisplay(c.ncc)}</span></div>
      <div class="info-item"><span class="info-label">NSS</span><span class="info-value">${boolDisplay(c.nss)}</span></div>
    </div>
  `;
}

function renderParent(p) {
  const el = document.getElementById("parentView");
  if (!p) { el.innerHTML = '<p class="no-data">No parent details added yet.</p>'; return; }
  el.innerHTML = `
    <div class="info-grid">
      <div class="info-item"><span class="info-label">Father Name</span><span class="info-value">${p.father_name || '—'}</span></div>
      <div class="info-item"><span class="info-label">Father Profession</span><span class="info-value">${p.father_profession || '—'}</span></div>
      <div class="info-item"><span class="info-label">Father Contact</span><span class="info-value mono">${p.father_contact || '—'}</span></div>
      <div class="info-item"><span class="info-label">Father Email</span><span class="info-value">${p.father_email || '—'}</span></div>
      <div class="info-item"><span class="info-label">Mother Name</span><span class="info-value">${p.mother_name || '—'}</span></div>
      <div class="info-item"><span class="info-label">Mother Profession</span><span class="info-value">${p.mother_profession || '—'}</span></div>
      <div class="info-item"><span class="info-label">Mother Contact</span><span class="info-value mono">${p.mother_contact || '—'}</span></div>
      <div class="info-item"><span class="info-label">Mother Email</span><span class="info-value">${p.mother_email || '—'}</span></div>
    </div>
  `;
}

function renderFinancial(f) {
  const el = document.getElementById("financialView");
  if (!f) { el.innerHTML = '<p class="no-data">No financial info added yet.</p>'; return; }
  el.innerHTML = `
    <div class="info-grid">
      <div class="info-item"><span class="info-label">Has Loan</span><span class="info-value">${boolDisplay(f.has_loan)}</span></div>
      <div class="info-item"><span class="info-label">Scholarship</span><span class="info-value">${f.scholarship_type}</span></div>
      <div class="info-item"><span class="info-label">Amount</span><span class="info-value mono">${f.scholarship_amount ? '₹' + f.scholarship_amount : '—'}</span></div>
    </div>
  `;
}

function renderInternships(list) {
  const el = document.getElementById("internshipsView");
  if (!list || list.length === 0) { el.innerHTML = '<p class="no-data">No internships added yet.</p>'; return; }
  el.innerHTML = `<div class="items-list">${list.map(i => `
    <div class="item-row">
      <div class="item-info">
        <div class="item-title">${i.company_name}</div>
        <div class="item-meta">
          <span>${i.internship_type}</span>
          <span>${i.duration || '—'}</span>
          <span>${i.has_stipend ? '₹' + i.stipend_amount : 'No Stipend'}</span>
        </div>
      </div>
      <div class="item-actions">
        <button class="btn btn-danger btn-sm" onclick="deleteInternship(${i.id})">Delete</button>
      </div>
    </div>
  `).join("")}</div>`;
}

function renderResearch(list) {
  const el = document.getElementById("researchView");
  if (!list || list.length === 0) { el.innerHTML = '<p class="no-data">No research papers added yet.</p>'; return; }
  el.innerHTML = `<div class="items-list">${list.map(r => `
    <div class="item-row">
      <div class="item-info">
        <div class="item-title">${r.title}</div>
        <div class="item-meta">
          <span>${r.paper_type}</span>
          <span>${r.year || '—'}</span>
          <span>${r.is_presentation ? 'Presentation' : 'Paper'}</span>
        </div>
      </div>
      <div class="item-actions">
        <button class="btn btn-danger btn-sm" onclick="deleteResearch(${r.id})">Delete</button>
      </div>
    </div>
  `).join("")}</div>`;
}

function renderDocuments(d) {
  const el = document.getElementById("documentsView");
  if (!d) { el.innerHTML = '<p class="no-data">No document record added yet.</p>'; return; }
  function dlBtn(label, type, path) {
    if (!path) return `<span style="color:#666;">No file uploaded</span>`;
    return `<a href="${API}/students/${studentId}/documents/download/${type}" class="btn btn-ghost btn-sm" download style="text-decoration:none;">⬇ Download ${label}</a>`;
  }
  const dlA = document.getElementById("dl_aadhaar");
  const dlP = document.getElementById("dl_pan");
  const dlI = document.getElementById("dl_id_card");
  if (dlA) { if (d.aadhaar_path) { dlA.href = `${API}/${d.aadhaar_path}`; dlA.download = d.aadhaar_path.split('/').pop(); dlA.style.display = ""; } else dlA.style.display = "none"; }
  if (dlP) { if (d.pan_path) { dlP.href = `${API}/${d.pan_path}`; dlP.download = d.pan_path.split('/').pop(); dlP.style.display = ""; } else dlP.style.display = "none"; }
  if (dlI) { if (d.id_card_path) { dlI.href = `${API}/${d.id_card_path}`; dlI.download = d.id_card_path.split('/').pop(); dlI.style.display = ""; } else dlI.style.display = "none"; }
  el.innerHTML = `
    <div class="info-grid">
      <div class="info-item"><span class="info-label">Aadhaar Verified</span><span class="info-value">${boolDisplay(d.aadhaar_verified)}</span></div>
      <div class="info-item"><span class="info-label">PAN Verified</span><span class="info-value">${boolDisplay(d.pan_verified)}</span></div>
      <div class="info-item"><span class="info-label">ID Card Verified</span><span class="info-value">${boolDisplay(d.id_card_verified)}</span></div>
      <div class="info-item"><span class="info-label">Library Card</span><span class="info-value">${boolDisplay(d.library_card)}</span></div>
    </div>
    <div style="margin-top:16px;">
      <h4 style="margin-bottom:10px;color:#aaa;font-size:0.85rem;text-transform:uppercase;letter-spacing:0.05em;">Uploaded Files</h4>
      <div style="display:flex;gap:12px;flex-wrap:wrap;">
        ${dlBtn("Aadhaar", "aadhaar", d.aadhaar_path)}
        ${dlBtn("PAN", "pan", d.pan_path)}
        ${dlBtn("ID Card", "id_card", d.id_card_path)}
      </div>
    </div>
  `;
}

function renderNoc(n) {
  const el = document.getElementById("nocView");
  if (!n) { el.innerHTML = '<p class="no-data">No NOC record added yet.</p>'; return; }
  el.innerHTML = `
    <div class="info-grid">
      <div class="info-item"><span class="info-label">BL Dept</span><span class="info-value">${boolDisplay(n.noc_bl_dept)}</span></div>
      <div class="info-item"><span class="info-label">Internet Internship</span><span class="info-value">${boolDisplay(n.noc_internet_internship)}</span></div>
      <div class="info-item"><span class="info-label">NCC</span><span class="info-value">${boolDisplay(n.noc_ncc)}</span></div>
      <div class="info-item"><span class="info-label">NSS</span><span class="info-value">${boolDisplay(n.noc_nss)}</span></div>
      <div class="info-item"><span class="info-label">INSS</span><span class="info-value">${boolDisplay(n.noc_inss)}</span></div>
    </div>
  `;
}

function renderPlacement(p) {
  const el = document.getElementById("placementView");
  if (!p) { el.innerHTML = '<p class="no-data">No placement record added yet.</p>'; return; }
  el.innerHTML = `
    <div class="info-grid">
      <div class="info-item"><span class="info-label">Internal Training</span><span class="info-value">${boolDisplay(p.internal_training)}</span></div>
      <div class="info-item"><span class="info-label">Placed</span><span class="info-value">${boolDisplay(p.is_placed)}</span></div>
      <div class="info-item"><span class="info-label">Company</span><span class="info-value">${p.company_name || '—'}</span></div>
      <div class="info-item"><span class="info-label">Package</span><span class="info-value mono">${p.package ? p.package + ' LPA' : '—'}</span></div>
      <div class="info-item"><span class="info-label">Higher Studies</span><span class="info-value">${boolDisplay(p.opted_higher_studies)}</span></div>
      <div class="info-item"><span class="info-label">Entrepreneurship</span><span class="info-value">${boolDisplay(p.opted_entrepreneurship)}</span></div>
    </div>
  `;
}

function renderAcadocs(a) {
  const el = document.getElementById("acadocsView");
  if (!a) { el.innerHTML = '<p class="no-data">No academic documents record added yet.</p>'; return; }
  function dlBtn(label, type, path) {
    if (!path) return `<span style="color:#666;">No file uploaded</span>`;
    return `<a href="${API}/${path}" class="btn btn-ghost btn-sm" download style="text-decoration:none;">⬇ Download ${label}</a>`;
  }
  el.innerHTML = `
    <div class="info-grid">
      <div class="info-item"><span class="info-label">All Marksheets</span><span class="info-value">${boolDisplay(a.all_marksheets)}</span></div>
      <div class="info-item"><span class="info-label">Provisional Cert</span><span class="info-value">${boolDisplay(a.provisional_cert)}</span></div>
      <div class="info-item"><span class="info-label">Is Lost</span><span class="info-value">${boolDisplay(a.is_lost)}</span></div>
    </div>
    <div style="margin-top:16px;">
      <h4 style="margin-bottom:10px;color:#aaa;font-size:0.85rem;text-transform:uppercase;letter-spacing:0.05em;">Uploaded Files</h4>
      <div style="display:flex;gap:12px;flex-wrap:wrap;">
        ${dlBtn("Marksheets", "marksheets", a.marksheets_path)}
        ${dlBtn("Provisional Cert", "provisional_cert", a.provisional_cert_path)}
      </div>
      <h4 style="margin:16px 0 10px;color:#aaa;font-size:0.85rem;text-transform:uppercase;letter-spacing:0.05em;">Semester Marksheets</h4>
      <div style="display:flex;gap:12px;flex-wrap:wrap;">
        ${[1,2,3,4,5,6,7,8].map(i => dlBtn(`Sem ${i}`, `sem${i}_marksheet`, a[`sem${i}_marksheet`])).join("")}
      </div>
    </div>
  `;
}

document.querySelectorAll(".tab-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
    document.querySelectorAll(".tab-panel").forEach(p => p.classList.add("hidden"));
    btn.classList.add("active");
    document.getElementById("tab-" + btn.dataset.tab).classList.remove("hidden");
  });
});

document.getElementById("editBasicBtn").addEventListener("click", () => {
  document.getElementById("basicInfoView").classList.add("hidden");
  document.getElementById("basicInfoEdit").classList.remove("hidden");
  document.getElementById("edit_name").value = studentData.name !== 'Data Not entered' ? studentData.name : '';
  document.getElementById("edit_branch").value = studentData.branch !== 'Data Not entered' ? studentData.branch : 'AIDS';
  document.getElementById("edit_year").value = studentData.year || 1;
  document.getElementById("edit_email").value = studentData.email || '';
  document.getElementById("edit_mobile").value = studentData.mobile || '';
  document.getElementById("edit_address").value = studentData.address || "";
});

document.getElementById("cancelEditBasic").addEventListener("click", () => {
  document.getElementById("basicInfoView").classList.remove("hidden");
  document.getElementById("basicInfoEdit").classList.add("hidden");
});

document.getElementById("saveBasicBtn").addEventListener("click", async () => {
  try {
    const payload = {
      roll_number: studentId,
      name: document.getElementById("edit_name").value,
      branch: document.getElementById("edit_branch").value,
      year: parseInt(document.getElementById("edit_year").value),
      email: document.getElementById("edit_email").value,
      mobile: document.getElementById("edit_mobile").value,
      address: document.getElementById("edit_address").value || null,
    };

    let updated;
    if (isStudentNew) {
      updated = await apiFetch(`/students`, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      isStudentNew = false;
    } else {
      updated = await apiFetch(`/students/${studentId}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      });
    }

    studentData = { ...studentData, ...updated };
    renderBasicInfo(studentData);
    document.getElementById("basicInfoView").classList.remove("hidden");
    document.getElementById("basicInfoEdit").classList.add("hidden");
    showAlert("profileAlert", "Basic info updated.", "success");
  } catch (e) {
    showAlert("profileAlert", e.message, "error");
  }
});

document.getElementById("classificationBtn").addEventListener("click", () => {
  const form = document.getElementById("classificationForm");
  form.classList.toggle("hidden");
  if (!form.classList.contains("hidden") && classificationExists && studentData.classification) {
    const c = studentData.classification;
    document.getElementById("cl_category").value = c.category;
    document.getElementById("cl_is_hosteller").value = c.is_hosteller.toString();
    document.getElementById("cl_sports_quota").value = c.sports_quota.toString();
    document.getElementById("cl_is_disabled").value = c.is_disabled.toString();
    document.getElementById("cl_is_single_child").value = c.is_single_child.toString();
    document.getElementById("cl_ncc").value = c.ncc.toString();
    document.getElementById("cl_nss").value = c.nss.toString();
  }
});

document.getElementById("cancelClassification").addEventListener("click", () => {
  document.getElementById("classificationForm").classList.add("hidden");
});

document.getElementById("saveClassification").addEventListener("click", async () => {
  const body = {
    category: document.getElementById("cl_category").value,
    is_hosteller: document.getElementById("cl_is_hosteller").value === "true",
    sports_quota: document.getElementById("cl_sports_quota").value === "true",
    is_disabled: document.getElementById("cl_is_disabled").value === "true",
    is_single_child: document.getElementById("cl_is_single_child").value === "true",
    ncc: document.getElementById("cl_ncc").value === "true",
    nss: document.getElementById("cl_nss").value === "true",
  };
  try {
    const method = classificationExists ? "PUT" : "POST";
    const result = await apiFetch(`/students/${studentId}/classification`, { method, body: JSON.stringify(body) });
    studentData.classification = result;
    classificationExists = true;
    renderClassification(result);
    document.getElementById("classificationForm").classList.add("hidden");
    showAlert("profileAlert", "Classification saved.", "success");
  } catch (e) {
    showAlert("profileAlert", e.message, "error");
  }
});

document.getElementById("parentBtn").addEventListener("click", () => {
  const form = document.getElementById("parentForm");
  form.classList.toggle("hidden");
  if (!form.classList.contains("hidden") && parentExists && studentData.parent_details) {
    const p = studentData.parent_details;
    document.getElementById("p_father_name").value = p.father_name || "";
    document.getElementById("p_father_profession").value = p.father_profession || "";
    document.getElementById("p_father_contact").value = p.father_contact || "";
    document.getElementById("p_father_email").value = p.father_email || "";
    document.getElementById("p_mother_name").value = p.mother_name || "";
    document.getElementById("p_mother_profession").value = p.mother_profession || "";
    document.getElementById("p_mother_contact").value = p.mother_contact || "";
    document.getElementById("p_mother_email").value = p.mother_email || "";
  }
});

document.getElementById("cancelParent").addEventListener("click", () => {
  document.getElementById("parentForm").classList.add("hidden");
});

document.getElementById("saveParent").addEventListener("click", async () => {
  const body = {
    father_name: document.getElementById("p_father_name").value || null,
    father_profession: document.getElementById("p_father_profession").value || null,
    father_contact: document.getElementById("p_father_contact").value || null,
    father_email: document.getElementById("p_father_email").value || null,
    mother_name: document.getElementById("p_mother_name").value || null,
    mother_profession: document.getElementById("p_mother_profession").value || null,
    mother_contact: document.getElementById("p_mother_contact").value || null,
    mother_email: document.getElementById("p_mother_email").value || null,
  };
  try {
    const method = parentExists ? "PUT" : "POST";
    const result = await apiFetch(`/students/${studentId}/parent`, { method, body: JSON.stringify(body) });
    studentData.parent_details = result;
    parentExists = true;
    renderParent(result);
    document.getElementById("parentForm").classList.add("hidden");
    showAlert("profileAlert", "Parent details saved.", "success");
  } catch (e) {
    showAlert("profileAlert", e.message, "error");
  }
});

document.getElementById("financialBtn").addEventListener("click", () => {
  const form = document.getElementById("financialForm");
  form.classList.toggle("hidden");
  if (!form.classList.contains("hidden") && financialExists && studentData.financial_info) {
    const f = studentData.financial_info;
    document.getElementById("fi_has_loan").value = f.has_loan.toString();
    const knownTypes = ["None", "EWS", "SC", "Private", "Other"];
    if (knownTypes.includes(f.scholarship_type)) {
      document.getElementById("fi_scholarship_type").value = f.scholarship_type;
    } else {
      document.getElementById("fi_scholarship_type").value = "Other";
      document.getElementById("fi_scholarship_custom").value = f.scholarship_type;
      document.getElementById("customScholarshipGroup").style.display = "block";
    }
    document.getElementById("fi_scholarship_amount").value = f.scholarship_amount || "";
  }
});

document.getElementById("cancelFinancial").addEventListener("click", () => {
  document.getElementById("financialForm").classList.add("hidden");
});

document.getElementById("saveFinancial").addEventListener("click", async () => {
  const scholarshipType = document.getElementById("fi_scholarship_type").value;
  const customScholarship = document.getElementById("fi_scholarship_custom")?.value.trim() || "";
  const body = {
    has_loan: document.getElementById("fi_has_loan").value === "true",
    scholarship_type: scholarshipType === "Other" && customScholarship ? customScholarship : scholarshipType,
    scholarship_amount: document.getElementById("fi_scholarship_amount").value || null,
  };
  try {
    const method = financialExists ? "PUT" : "POST";
    const result = await apiFetch(`/students/${studentId}/financial`, { method, body: JSON.stringify(body) });
    studentData.financial_info = result;
    financialExists = true;
    renderFinancial(result);
    document.getElementById("financialForm").classList.add("hidden");
    showAlert("profileAlert", "Financial info saved.", "success");
  } catch (e) {
    showAlert("profileAlert", e.message, "error");
  }
});

document.getElementById("addInternshipBtn").addEventListener("click", () => {
  document.getElementById("internshipForm").classList.toggle("hidden");
});

document.getElementById("cancelInternship").addEventListener("click", () => {
  document.getElementById("internshipForm").classList.add("hidden");
});

document.getElementById("saveInternship").addEventListener("click", async () => {
  const body = {
    internship_type: document.getElementById("int_type").value,
    company_name: document.getElementById("int_company").value,
    duration: document.getElementById("int_duration").value || null,
    has_stipend: document.getElementById("int_has_stipend").value === "true",
    stipend_amount: document.getElementById("int_stipend_amount").value || null,
  };
  try {
    const result = await apiFetch(`/students/${studentId}/internships`, { method: "POST", body: JSON.stringify(body) });
    studentData.internships = [...(studentData.internships || []), result];
    renderInternships(studentData.internships);
    document.getElementById("internshipForm").classList.add("hidden");
    showAlert("profileAlert", "Internship added.", "success");
  } catch (e) {
    showAlert("profileAlert", e.message, "error");
  }
});

async function deleteInternship(id) {
  if (!confirm("Delete this internship?")) return;
  try {
    id = String(id);
    await apiFetch(`/internships/${id}`, { method: "DELETE" });
    studentData.internships = studentData.internships.filter(i => String(i.id) !== id);
    renderInternships(studentData.internships);
    showAlert("profileAlert", "Internship deleted.", "success");
  } catch (e) {
    showAlert("profileAlert", e.message, "error");
  }
}

document.getElementById("addResearchBtn").addEventListener("click", () => {
  document.getElementById("researchForm").classList.toggle("hidden");
});

document.getElementById("cancelResearch").addEventListener("click", () => {
  document.getElementById("researchForm").classList.add("hidden");
});

document.getElementById("saveResearch").addEventListener("click", async () => {
  const body = {
    title: document.getElementById("rp_title").value,
    paper_type: document.getElementById("rp_type").value,
    is_presentation: document.getElementById("rp_is_presentation").value === "true",
    year: document.getElementById("rp_year").value ? parseInt(document.getElementById("rp_year").value) : null,
  };
  try {
    const result = await apiFetch(`/students/${studentId}/research`, { method: "POST", body: JSON.stringify(body) });
    studentData.research_papers = [...(studentData.research_papers || []), result];
    renderResearch(studentData.research_papers);
    document.getElementById("researchForm").classList.add("hidden");
    showAlert("profileAlert", "Research paper added.", "success");
  } catch (e) {
    showAlert("profileAlert", e.message, "error");
  }
});

async function deleteResearch(id) {
  if (!confirm("Delete this research paper?")) return;
  try {
    id = String(id);
    await apiFetch(`/research/${id}`, { method: "DELETE" });
    studentData.research_papers = studentData.research_papers.filter(r => String(r.id) !== id);
    renderResearch(studentData.research_papers);
    showAlert("profileAlert", "Research paper deleted.", "success");
  } catch (e) {
    showAlert("profileAlert", e.message, "error");
  }
}

document.getElementById("documentsBtn").addEventListener("click", () => {
  const form = document.getElementById("documentsForm");
  form.classList.toggle("hidden");
  if (!form.classList.contains("hidden") && documentsExists && studentData.documents) {
    const d = studentData.documents;
    document.getElementById("doc_aadhaar_verified").value = d.aadhaar_verified.toString();
    document.getElementById("doc_pan_verified").value = d.pan_verified.toString();
    document.getElementById("doc_id_card_verified").value = d.id_card_verified.toString();
    document.getElementById("doc_library_card").value = d.library_card.toString();
  }
});

document.getElementById("cancelDocuments").addEventListener("click", () => {
  document.getElementById("documentsForm").classList.add("hidden");
});

document.getElementById("saveDocuments").addEventListener("click", async () => {
  const body = {
    aadhaar_verified: document.getElementById("doc_aadhaar_verified").value === "true",
    pan_verified: document.getElementById("doc_pan_verified").value === "true",
    id_card_verified: document.getElementById("doc_id_card_verified").value === "true",
    library_card: document.getElementById("doc_library_card").value === "true",
  };
  try {
    const method = documentsExists ? "PUT" : "POST";
    const result = await apiFetch(`/students/${studentId}/documents`, { method, body: JSON.stringify(body) });
    studentData.documents = result;
    documentsExists = true;
    renderDocuments(result);
    document.getElementById("documentsForm").classList.add("hidden");
    showAlert("profileAlert", "Documents saved.", "success");
  } catch (e) {
    showAlert("profileAlert", e.message, "error");
  }
});

document.getElementById("nocBtn").addEventListener("click", () => {
  const form = document.getElementById("nocForm");
  form.classList.toggle("hidden");
  if (!form.classList.contains("hidden") && nocExists && studentData.noc_records) {
    const n = studentData.noc_records;
    document.getElementById("noc_bl_dept").value = n.noc_bl_dept.toString();
    document.getElementById("noc_internet_internship").value = n.noc_internet_internship.toString();
    document.getElementById("noc_ncc").value = n.noc_ncc.toString();
    document.getElementById("noc_nss").value = n.noc_nss.toString();
    document.getElementById("noc_inss").value = n.noc_inss.toString();
  }
});

document.getElementById("cancelNoc").addEventListener("click", () => {
  document.getElementById("nocForm").classList.add("hidden");
});

document.getElementById("saveNoc").addEventListener("click", async () => {
  const body = {
    noc_bl_dept: document.getElementById("noc_bl_dept").value === "true",
    noc_internet_internship: document.getElementById("noc_internet_internship").value === "true",
    noc_ncc: document.getElementById("noc_ncc").value === "true",
    noc_nss: document.getElementById("noc_nss").value === "true",
    noc_inss: document.getElementById("noc_inss").value === "true",
  };
  try {
    const method = nocExists ? "PUT" : "POST";
    const result = await apiFetch(`/students/${studentId}/noc`, { method, body: JSON.stringify(body) });
    studentData.noc_records = result;
    nocExists = true;
    renderNoc(result);
    document.getElementById("nocForm").classList.add("hidden");
    showAlert("profileAlert", "NOC records saved.", "success");
  } catch (e) {
    showAlert("profileAlert", e.message, "error");
  }
});

document.getElementById("placementBtn").addEventListener("click", () => {
  const form = document.getElementById("placementForm");
  form.classList.toggle("hidden");
  if (!form.classList.contains("hidden") && placementExists && studentData.placement) {
    const p = studentData.placement;
    document.getElementById("pl_internal_training").value = p.internal_training.toString();
    document.getElementById("pl_is_placed").value = p.is_placed.toString();
    document.getElementById("pl_company_name").value = p.company_name || "";
    document.getElementById("pl_package").value = p.package || "";
    document.getElementById("pl_higher_studies").value = p.opted_higher_studies.toString();
    document.getElementById("pl_entrepreneurship").value = p.opted_entrepreneurship.toString();
  }
});

document.getElementById("cancelPlacement").addEventListener("click", () => {
  document.getElementById("placementForm").classList.add("hidden");
});

document.getElementById("savePlacement").addEventListener("click", async () => {
  const body = {
    internal_training: document.getElementById("pl_internal_training").value === "true",
    is_placed: document.getElementById("pl_is_placed").value === "true",
    company_name: document.getElementById("pl_company_name").value || null,
    package: document.getElementById("pl_package").value || null,
    opted_higher_studies: document.getElementById("pl_higher_studies").value === "true",
    opted_entrepreneurship: document.getElementById("pl_entrepreneurship").value === "true",
  };
  try {
    const method = placementExists ? "PUT" : "POST";
    const result = await apiFetch(`/students/${studentId}/placement`, { method, body: JSON.stringify(body) });
    studentData.placement = result;
    placementExists = true;
    renderPlacement(result);
    document.getElementById("placementForm").classList.add("hidden");
    showAlert("profileAlert", "Placement saved.", "success");
  } catch (e) {
    showAlert("profileAlert", e.message, "error");
  }
});

document.getElementById("acadocsBtn").addEventListener("click", () => {
  const form = document.getElementById("acadocsForm");
  form.classList.toggle("hidden");
  if (!form.classList.contains("hidden") && acadocsExists && studentData.academic_documents) {
    const a = studentData.academic_documents;
    document.getElementById("ad_all_marksheets").value = a.all_marksheets.toString();
    document.getElementById("ad_provisional_cert").value = a.provisional_cert.toString();
    document.getElementById("ad_is_lost").value = a.is_lost.toString();
  }
});

document.getElementById("cancelAcadocs").addEventListener("click", () => {
  document.getElementById("acadocsForm").classList.add("hidden");
});

document.getElementById("saveAcadocs").addEventListener("click", async () => {
  const body = {
    all_marksheets: document.getElementById("ad_all_marksheets").value === "true",
    provisional_cert: document.getElementById("ad_provisional_cert").value === "true",
    is_lost: document.getElementById("ad_is_lost").value === "true",
  };
  try {
    const method = acadocsExists ? "PUT" : "POST";
    const result = await apiFetch(`/students/${studentId}/academic-documents`, { method, body: JSON.stringify(body) });
    studentData.academic_documents = result;
    acadocsExists = true;
    renderAcadocs(result);
    document.getElementById("acadocsForm").classList.add("hidden");
    showAlert("profileAlert", "Academic documents saved.", "success");
  } catch (e) {
    showAlert("profileAlert", e.message, "error");
  }
});

async function uploadFile(endpoint, fieldName, fileInput) {
  const file = fileInput.files[0];
  if (!file) return false;
  const formData = new FormData();
  formData.append(fieldName, file);
  const res = await fetch(`${API}${endpoint}`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${localStorage.getItem("token")}`
    },
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Upload failed" }));
    throw new Error(err.detail);
  }
  return await res.json();
}

document.getElementById("saveBasicBtn").addEventListener("click", async () => {
  const photoFile = document.getElementById("upload_photo").files[0];
  const sigFile = document.getElementById("upload_signature").files[0];
  if (photoFile) {
    try {
      await uploadFile(`/students/${studentId}/photo`, "photo", document.getElementById("upload_photo"));
      showAlert("profileAlert", "Photo uploaded.", "success");
    } catch (e) {
      showAlert("profileAlert", "Photo upload failed: " + e.message, "error");
    }
  }
  if (sigFile) {
    try {
      await uploadFile(`/students/${studentId}/signature`, "signature", document.getElementById("upload_signature"));
      showAlert("profileAlert", "Signature uploaded.", "success");
    } catch (e) {
      showAlert("profileAlert", "Signature upload failed: " + e.message, "error");
    }
  }
}, { capture: true });

document.getElementById("uploadDocsBtn").addEventListener("click", async () => {
  const aadhaar = document.getElementById("upload_aadhaar");
  const pan = document.getElementById("upload_pan");
  const idCard = document.getElementById("upload_id_card");

  if (!aadhaar.files[0] && !pan.files[0] && !idCard.files[0]) {
    showAlert("profileAlert", "Please select at least one file to upload.", "error");
    return;
  }

  try {
    const formData = new FormData();
    if (aadhaar.files[0]) formData.append("aadhaar", aadhaar.files[0]);
    if (pan.files[0]) formData.append("pan", pan.files[0]);
    if (idCard.files[0]) formData.append("id_card", idCard.files[0]);

    const res = await fetch(`${API}/students/${studentId}/documents/upload`, {
      method: "POST",
      headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` },
      body: formData,
    });
    if (!res.ok) { const err = await res.json().catch(() => ({})); throw new Error(err.detail || "Upload failed"); }
    showAlert("profileAlert", "Document files uploaded successfully.", "success");
    aadhaar.value = ""; pan.value = ""; idCard.value = "";
  } catch (e) {
    showAlert("profileAlert", e.message, "error");
  }
});

document.getElementById("uploadAcadocsBtn").addEventListener("click", async () => {
  const provisional = document.getElementById("upload_provisional");
  const semInputs = [1,2,3,4,5,6,7,8].map(i => document.getElementById(`upload_sem${i}_marksheet`));
  const anySelected = (provisional && provisional.files[0]) || semInputs.some(el => el && el.files[0]);
  if (!anySelected) {
    showAlert("profileAlert", "Please select at least one file to upload.", "error");
    return;
  }
  try {
    const formData = new FormData();
    if (provisional && provisional.files[0]) formData.append("provisional_cert", provisional.files[0]);
    semInputs.forEach((el, idx) => { if (el && el.files[0]) formData.append(`sem${idx+1}_marksheet`, el.files[0]); });
    const res = await fetch(`${API}/students/${studentId}/academic-documents/upload`, {
      method: "POST",
      headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` },
      body: formData,
    });
    if (!res.ok) { const err = await res.json().catch(() => ({})); throw new Error(err.detail || "Upload failed"); }
    showAlert("profileAlert", "Academic files uploaded successfully.", "success");
    if (provisional) provisional.value = "";
    semInputs.forEach(el => { if (el) el.value = ""; });
  } catch (e) {
    showAlert("profileAlert", e.message, "error");
  }
});

loadProfile();

// Intercept all clicks to show Edit Notice popup
document.addEventListener("click", (e) => {
  if (e.target && e.target.tagName === "BUTTON") {
    const txt = e.target.textContent || "";
    if (txt.includes("Edit ") || txt.includes("Add / Edit")) {
      const modal = document.getElementById("editNoticeModal");
      if (modal) {
        modal.style.display = "flex";
      }
    }
  }
});

const closeNotice = document.getElementById("closeEditNoticeModal");
if (closeNotice) {
  closeNotice.addEventListener("click", () => {
    document.getElementById("editNoticeModal").style.display = "none";
  });
}