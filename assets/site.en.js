(function () {
  document.documentElement.classList.add("js");
  document.addEventListener("DOMContentLoaded", function () {
    var header = document.querySelector(".site-header");
    var toggle = document.querySelector(".nav-toggle");
    if (!header || !toggle) return;
    function setOpen(open) {
      header.setAttribute("data-open", open ? "true" : "false");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.textContent = open ? "Schließen" : "Menü";
    }
    toggle.addEventListener("click", function () {
      setOpen(header.getAttribute("data-open") !== "true");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && header.getAttribute("data-open") === "true") {
        setOpen(false);
        toggle.focus();
      }
    });
    header.querySelectorAll(".site-nav a").forEach(function (a) {
      a.addEventListener("click", function () { setOpen(false); });
    });
  });
})();
