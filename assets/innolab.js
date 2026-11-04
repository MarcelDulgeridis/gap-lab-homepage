/* InnoLab: Format-Slider (Progressive Enhancement). Ohne JavaScript stehen alle Formate untereinander. */
(function () {
  var root = document.querySelector("[data-slider]");
  if (!root) return;
  var tabs = Array.prototype.slice.call(root.querySelectorAll(".il-tabs a"));
  var panels = Array.prototype.slice.call(root.querySelectorAll(".il-format"));
  var prev = root.querySelector("[data-prev]"), next = root.querySelector("[data-next]"), count = root.querySelector("[data-count]");
  var tablist = root.querySelector(".il-tabs ol");
  if (!tabs.length || tabs.length !== panels.length) return;
  root.classList.add("is-js");
  tablist.setAttribute("role", "tablist");
  var cur = -1;

  function idxOf(id) { for (var i = 0; i < panels.length; i++) if (panels[i].id === id) return i; return -1; }

  function show(i, opts) {
    opts = opts || {};
    if (i < 0) i = panels.length - 1;
    if (i >= panels.length) i = 0;
    cur = i;
    panels.forEach(function (p, k) { p.hidden = k !== i; p.setAttribute("role", "tabpanel"); p.setAttribute("aria-labelledby", "tab-" + p.id); });
    tabs.forEach(function (t, k) {
      t.id = "tab-" + panels[k].id;
      t.setAttribute("role", "tab");
      t.setAttribute("aria-selected", k === i ? "true" : "false");
      t.setAttribute("aria-controls", panels[k].id);
      t.tabIndex = k === i ? 0 : -1;
      t.classList.toggle("on", k === i);
    });
    if (count) count.textContent = "Format " + (i + 1) + " von " + panels.length;
    if (opts.focus) tabs[i].focus();
    if (opts.hash !== false && history.replaceState) history.replaceState(null, "", "#" + panels[i].id);
    if (opts.scroll) {
      var top = root.getBoundingClientRect().top + window.pageYOffset - (document.querySelector(".site-header") ? document.querySelector(".site-header").offsetHeight : 0) - 12;
      window.scrollTo({ top: top, behavior: "auto" });
    }
  }

  tabs.forEach(function (t, k) {
    t.addEventListener("click", function (e) { e.preventDefault(); show(k, { scroll: false }); });
    t.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); show(cur + 1, { focus: true }); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); show(cur - 1, { focus: true }); }
      else if (e.key === "Home") { e.preventDefault(); show(0, { focus: true }); }
      else if (e.key === "End") { e.preventDefault(); show(panels.length - 1, { focus: true }); }
    });
  });
  if (prev) prev.addEventListener("click", function () { show(cur - 1); });
  if (next) next.addEventListener("click", function () { show(cur + 1); });

  // Links auf ein Format (Hero, Übersicht, andere Seiten) öffnen das Format und springen zum Slider
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[href^='#']");
    if (!a || root.contains(a) && a.closest(".il-tabs")) return;
    var i = idxOf(a.getAttribute("href").slice(1));
    if (a.getAttribute("href") === "#formate") { e.preventDefault(); show(cur < 0 ? 0 : cur, { scroll: true }); return; }
    if (i >= 0) { e.preventDefault(); show(i, { scroll: true }); }
  });
  window.addEventListener("hashchange", function () {
    var i = idxOf(location.hash.slice(1));
    if (i >= 0) show(i, { scroll: true, hash: false });
  });

  var start = idxOf(location.hash.slice(1));
  show(start >= 0 ? start : 0, { hash: false });
  if (start >= 0) setTimeout(function () { show(start, { scroll: true, hash: false }); }, 60);
})();
