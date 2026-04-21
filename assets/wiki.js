(function () {
  const body = document.body;
  const toggle = document.querySelector("[data-nav-toggle]");
  const searchInput = document.querySelector("[data-search-input]");
  const searchResults = document.querySelector("[data-search-results]");
  let searchIndex = [];

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  if (toggle) {
    toggle.addEventListener("click", function () {
      const isOpen = body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", String(isOpen));
    });
  }

  document.addEventListener("click", function (event) {
    if (!body.classList.contains("nav-open")) {
      return;
    }
    const sidebar = document.getElementById("wiki-sidebar");
    if (!sidebar || sidebar.contains(event.target) || event.target === toggle) {
      return;
    }
    body.classList.remove("nav-open");
    if (toggle) {
      toggle.setAttribute("aria-expanded", "false");
    }
  });

  if (!searchInput || !searchResults) {
    return;
  }

  fetch("/assets/wiki-search.json")
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      searchIndex = data;
    })
    .catch(function () {
      searchIndex = [];
    });

  function renderResults(query) {
    const normalized = query.trim().toLowerCase();
    if (!normalized) {
      searchResults.hidden = true;
      searchResults.innerHTML = "";
      return;
    }

    const terms = normalized.split(/\s+/g);
    const matches = searchIndex
      .filter(function (entry) {
        return terms.every(function (term) {
          return entry.text.includes(term);
        });
      })
      .slice(0, 8);

    if (!matches.length) {
      searchResults.innerHTML = '<div class="search-empty">No pages matched that query.</div>';
      searchResults.hidden = false;
      return;
    }

    searchResults.innerHTML = matches
      .map(function (entry) {
        return (
          '<a class="search-result" href="' +
          escapeHtml(entry.url) +
          '">' +
          "<strong>" +
          escapeHtml(entry.title) +
          "</strong>" +
          "<span>" +
          escapeHtml(entry.section) +
          (entry.summary ? " — " + escapeHtml(entry.summary) : "") +
          "</span>" +
          "</a>"
        );
      })
      .join("");
    searchResults.hidden = false;
  }

  searchInput.addEventListener("input", function () {
    renderResults(searchInput.value);
  });

  searchInput.addEventListener("focus", function () {
    if (searchInput.value.trim()) {
      renderResults(searchInput.value);
    }
  });

  document.addEventListener("keydown", function (event) {
    const target = event.target;
    const isEditable =
      target &&
      (target.tagName === "INPUT" ||
        target.tagName === "TEXTAREA" ||
        target.isContentEditable);

    if (event.key === "/" && !isEditable) {
      event.preventDefault();
      searchInput.focus();
      searchInput.select();
    }

    if (event.key === "Escape") {
      searchResults.hidden = true;
      if (body.classList.contains("nav-open")) {
        body.classList.remove("nav-open");
        if (toggle) {
          toggle.setAttribute("aria-expanded", "false");
        }
      }
    }
  });

  document.addEventListener("click", function (event) {
    if (searchResults.hidden) {
      return;
    }
    if (event.target === searchInput || searchResults.contains(event.target)) {
      return;
    }
    searchResults.hidden = true;
  });
})();
