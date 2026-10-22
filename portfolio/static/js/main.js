// Small enhancements: mobile nav, scroll reveal, project filtering.
(function () {
  // Light / dark theme toggle (choice saved in localStorage)
  const themeBtn = document.querySelector(".theme-toggle");
  if (themeBtn) {
    themeBtn.addEventListener("click", () => {
      const root = document.documentElement;
      const dark = root.getAttribute("data-theme") === "dark";
      if (dark) root.removeAttribute("data-theme");
      else root.setAttribute("data-theme", "dark");
      try { localStorage.setItem("theme", dark ? "light" : "dark"); } catch (e) {}
    });
  }

  // Mobile nav toggle
  const toggle = document.querySelector(".nav-toggle");
  const links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", () => {
      const open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }

  // Reveal elements as they scroll into view
  const revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("visible");
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("visible"));
  }

  // Publication status filter (publications page)
  const statusBtns = document.querySelectorAll(".filter-btn[data-status]");
  const articles = document.querySelectorAll("#article-list .article");
  statusBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      statusBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      const s = btn.dataset.status;
      articles.forEach((a) => {
        const own = a.querySelector(".status").textContent.trim();
        a.classList.toggle("hidden", s !== "all" && own !== s);
      });
    });
  });

  // Project tag filter (projects page)
  const filterBtns = document.querySelectorAll(".filter-btn");
  const cards = document.querySelectorAll("#project-grid .project-card");
  filterBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      filterBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      const tag = btn.dataset.tag;
      cards.forEach((card) => {
        const tags = Array.from(card.querySelectorAll(".tags li")).map((li) => li.textContent.trim());
        card.classList.toggle("hidden", tag !== "all" && !tags.includes(tag));
      });
    });
  });
})();
