const sidebar = document.querySelector(".sidebar");
const mobileBtn = document.getElementById("mobileMenuBtn");

if (sidebar && mobileBtn) {
  mobileBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    sidebar.classList.toggle("visible");
    document.body.classList.toggle("sidebar-open");
  });

  document.addEventListener("click", (e) => {
    if (
      sidebar.classList.contains("visible") &&
      !sidebar.contains(e.target) &&
      !mobileBtn.contains(e.target)
    ) {
      sidebar.classList.remove("visible");
      document.body.classList.remove("sidebar-open");
    }
  });
}