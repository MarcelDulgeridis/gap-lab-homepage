/* THE GAP Lab — Interaktionen v2. Externe Datei, keine Abhängigkeiten, CSP-konform. */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  function seen(els, cb, opts) {
    if (!("IntersectionObserver" in window)) { els.forEach(cb); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { cb(e.target); io.unobserve(e.target); } });
    }, opts || { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    els.forEach(function (e) { io.observe(e); });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.documentElement.classList.add("js");

    /* Header: Schatten + Fortschritt */
    var header = $(".site-header");
    if (header) {
      var bar = document.createElement("span");
      bar.className = "hdr-progress"; bar.setAttribute("aria-hidden", "true");
      header.appendChild(bar);
      var onScroll = function () {
        var h = document.documentElement;
        bar.style.transform = "scaleX(" + Math.min(1, h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight)) + ")";
        header.classList.toggle("is-scrolled", h.scrollTop > 8);
      };
      addEventListener("scroll", onScroll, { passive: true }); onScroll();
    }

    /* Einblendung */
    var targets = $$(".section-head,.v-break,.v-stage,.v-frow,.v-panel,.card,.partner,.partner-wide,.v-timeline li,.answer,.v-facts>div,.faq details,.v-term,.v-ofield,.il-format,.v-cflow>*,.contact-list");
    targets.forEach(function (el, i) { el.classList.add("rv"); el.style.setProperty("--d", ((i % 4) * 0.07).toFixed(2) + "s"); });
    seen($$(".rv"), function (el) { el.classList.add("is-in"); });
    setTimeout(function () { $$(".rv").forEach(function (el) { el.classList.add("is-in"); }); }, 3500);

    /* Zahlen hochzählen */
    seen($$(".v-nums b"), function (el) {
      var txt = el.textContent;
      if (reduce) return;
      var parts = txt.split(/(\d+)/);
      var t0 = performance.now(), dur = 1400;
      (function f(t) {
        var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
        el.textContent = parts.map(function (s) { return /^\d+$/.test(s) ? Math.round(+s * e) : s; }).join("");
        if (p < 1) requestAnimationFrame(f); else el.textContent = txt;
      })(t0);
    }, { threshold: 0.6 });

    /* KI-Gap-Balken, Zeitleiste */
    seen($$(".v-gapdemo,.v-timeline"), function (el) { el.classList.add("is-in"); }, { threshold: 0.35 });

    /* Ticker */
    var tk = $(".tk-t");
    if (tk && !reduce) {
      var lines = tk.getAttribute("data-lines").split("|"), i = 0;
      setInterval(function () {
        tk.classList.add("is-out");
        setTimeout(function () { i = (i + 1) % lines.length; tk.textContent = lines[i]; tk.classList.remove("is-out"); }, 400);
      }, 3800);
    }

    /* Hero: Brücke bauen */
    var rg = $("#hv-range");
    if (rg) {
      var planks = $$(".hv-bridge i"), st = $(".hv-state");
      var set = function (v) {
        var n = Math.round((v / 100) * planks.length);
        planks.forEach(function (p, k) { p.classList.toggle("on", k < n); });
        st.textContent = st.getAttribute("data-s" + (v >= 96 ? 2 : v >= 30 ? 1 : 0));
      };
      rg.addEventListener("input", function () { set(+rg.value); });
      set(+rg.value);
      if (!reduce) {
        var v = 12, dir = 1;
        var timer = setInterval(function () { v += dir * 1.2; if (v > 100) { v = 100; dir = -1; } if (v < 8) { v = 8; dir = 1; } rg.value = v; set(v); }, 70);
        var stop = function () { clearInterval(timer); };
        rg.addEventListener("pointerdown", stop); rg.addEventListener("keydown", stop);
        setTimeout(stop, 12000);
      }
      var stage = $(".hv-stage"), card = $(".hv-card");
      if (!reduce && matchMedia("(hover:hover)").matches) {
        stage.addEventListener("pointermove", function (e) {
          var b = stage.getBoundingClientRect(), x = (e.clientX - b.left) / b.width - 0.5, y = (e.clientY - b.top) / b.height - 0.5;
          card.style.transform = "rotateY(" + (x * 6) + "deg) rotateX(" + (-y * 5) + "deg)";
        });
        stage.addEventListener("pointerleave", function () { card.style.transform = ""; });
      }
    }
  });
})();
