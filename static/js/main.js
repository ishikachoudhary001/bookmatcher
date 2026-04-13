// ===================== MAIN.JS =====================
// Handles search bar behavior, smooth navigation, and small UI animations.

document.addEventListener("DOMContentLoaded", () => {
  const searchBar = document.querySelector(".search-bar input");

  // Enter key triggers search form
  if (searchBar) {
    searchBar.addEventListener("keypress", function (e) {
      if (e.key === "Enter") {
        this.form.submit();
      }
    });
  }

  // Smooth scroll for internal links (optional enhancement)
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      document.querySelector(this.getAttribute("href")).scrollIntoView({
        behavior: "smooth"
      });
    });
  });
});
