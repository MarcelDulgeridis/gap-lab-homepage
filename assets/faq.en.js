/* FAQ: Volltextsuche, Themenfilter, alle öffnen/schließen, Direktlinks. Ohne JavaScript bleibt die Liste vollständig sichtbar. */
(function () {
  "use strict";
  var root = document.querySelector("[data-faq]");
  if (!root) return;

  var input = root.querySelector(".faq-search");
  var chips = Array.prototype.slice.call(root.querySelectorAll(".faq-cats button"));
  var groups = Array.prototype.slice.call(root.querySelectorAll(".faq-group"));
  var items = Array.prototype.slice.call(root.querySelectorAll(".faq details"));
  var count = root.querySelector("[data-count]");
  var empty = root.querySelector("[data-empty]");
  var toggle = root.querySelector("[data-toggle]");
  var reset = root.querySelector("[data-reset]");
  var total = items.length;
  var cat = "all";

  function norm(s) {
    return String(s).toLowerCase().replace(/\u00a0/g, " ")
      .replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss")
      .replace(/[̀-ͯ]/g, "");
  }

  var index = items.map(function (d) {
    return { el: d, cat: d.getAttribute("data-cat"), text: norm(d.textContent) };
  });

  function terms() {
    return norm(input.value).split(/\s+/).filter(Boolean);
  }

  function apply() {
    var t = terms();
    var shown = 0;
    index.forEach(function (it) {
      var okCat = cat === "all" || it.cat === cat;
      var okText = t.every(function (w) { return it.text.indexOf(w) !== -1; });
      var ok = okCat && okText;
      it.el.hidden = !ok;
      if (ok) shown++;
    });
    groups.forEach(function (g) {
      var any = g.querySelector("details:not([hidden])");
      g.hidden = !any;
    });
    count.textContent = (t.length || cat !== "all")
      ? shown + " of " + total + " questions"
      : total + " questions";
    empty.hidden = shown !== 0;
    var active = t.length > 0 || cat !== "all";
    reset.hidden = !active;
    toggle.hidden = shown === 0;
    syncToggle();
  }

  function visibleItems() {
    return items.filter(function (d) { return !d.hidden; });
  }

  function syncToggle() {
    var vis = visibleItems();
    var allOpen = vis.length > 0 && vis.every(function (d) { return d.open; });
    toggle.textContent = allOpen ? "Close all" : "Open all";
    toggle.setAttribute("data-state", allOpen ? "open" : "closed");
  }

  function setCat(c) {
    cat = c;
    chips.forEach(function (b) {
      b.setAttribute("aria-pressed", b.getAttribute("data-cat") === c ? "true" : "false");
    });
    apply();
  }

  input.addEventListener("input", apply);
  input.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && input.value) { input.value = ""; apply(); }
  });
  chips.forEach(function (b) {
    b.addEventListener("click", function () { setCat(b.getAttribute("data-cat")); });
  });
  toggle.addEventListener("click", function () {
    var open = toggle.getAttribute("data-state") !== "open";
    visibleItems().forEach(function (d) { d.open = open; });
    syncToggle();
  });
  reset.addEventListener("click", function () {
    input.value = "";
    setCat("all");
    input.focus();
  });
  items.forEach(function (d) { d.addEventListener("toggle", syncToggle); });

  function openFromHash() {
    var id = decodeURIComponent((location.hash || "").slice(1));
    if (!id) return;
    var el = document.getElementById(id);
    if (!el || el.tagName !== "DETAILS") return;
    if (el.hidden) { input.value = ""; setCat("all"); }
    el.open = true;
    el.classList.add("is-target");
    el.scrollIntoView({ block: "start" });
  }

  var q = new URLSearchParams(location.search).get("q");
  if (q) input.value = q;
  root.classList.add("is-js");
  apply();
  openFromHash();
  window.addEventListener("hashchange", openFromHash);
})();
