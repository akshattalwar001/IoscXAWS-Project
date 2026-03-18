document.getElementById("submitBtn").addEventListener("click", async () => {
  const btn = document.getElementById("submitBtn");

  const body = {
    roll_number: document.getElementById("roll_number").value.trim(),
    name: document.getElementById("name").value.trim(),
    branch: document.getElementById("branch").value,
    year: parseInt(document.getElementById("year").value),
    email: document.getElementById("email").value.trim(),
    mobile: document.getElementById("mobile").value.trim(),
    address: document.getElementById("address").value.trim() || null,
  };

  if (!body.roll_number || !body.name || !body.branch || !body.year || !body.email || !body.mobile) {
    showAlert("formAlert", "Please fill all required fields.", "error");
    return;
  }

  btn.textContent = "Creating...";
  btn.disabled = true;

  try {
    const student = await apiFetch("/students", {
      method: "POST",
      body: JSON.stringify(body),
    });
    showAlert("formAlert", `Student created successfully! ID: ${student.id}`, "success");
    setTimeout(() => {
      window.location.href = `profile.html?id=${student.id}`;
    }, 1000);
  } catch (e) {
    showAlert("formAlert", e.message, "error");
    btn.textContent = "Create Student";
    btn.disabled = false;
  }
});