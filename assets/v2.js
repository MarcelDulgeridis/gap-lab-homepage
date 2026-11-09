/* THE GAP Lab — Interaktionen v2. Externe Datei, keine Abhängigkeiten, CSP-konform
   (Werte werden ausschließlich über classList/dataset/CSSOM gesetzt, keine style-Attribute im Markup). */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var hover = window.matchMedia && matchMedia("(hover:hover)").matches;

  function seen(els, cb, opts) {
    if (!els.length) return;
    if (!("IntersectionObserver" in window)) { els.forEach(cb); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { cb(e.target); io.unobserve(e.target); } });
    }, opts || { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    els.forEach(function (e) { io.observe(e); });
  }
  function tabs(btns, panes, onSel) {
    var sel = function (i) {
      btns.forEach(function (b, k) { b.classList.toggle("on", k === i); b.setAttribute("aria-selected", k === i ? "true" : "false"); b.tabIndex = k === i ? 0 : -1; });
      panes.forEach(function (p, k) { p.classList.toggle("on", k === i); p.hidden = k !== i; });
      if (onSel) onSel(i);
    };
    btns.forEach(function (b, k) {
      b.addEventListener("click", function () { sel(k); });
      b.addEventListener("keydown", function (e) {
        var d = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
        if (!d) return;
        e.preventDefault(); var n = (k + d + btns.length) % btns.length; btns[n].focus(); sel(n);
      });
    });
    return sel;
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.documentElement.classList.add("js");

    /* ---------- Kopf: Fortschritt, Scrollspy ---------- */
    var header = $(".site-header"), bar;
    if (header) {
      bar = document.createElement("span");
      bar.className = "hdr-progress"; bar.setAttribute("aria-hidden", "true");
      header.appendChild(bar);
    }
    var spy = $$(".snav-links a"), spyT = spy.map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); });
    var fbar = $(".x-fbar"), footer = $(".site-footer");
    var onScroll = function () {
      var h = document.documentElement, y = h.scrollTop;
      if (bar) bar.style.transform = "scaleX(" + Math.min(1, y / Math.max(1, h.scrollHeight - h.clientHeight)) + ")";
      var cur = -1;
      spyT.forEach(function (t, i) { if (t && t.getBoundingClientRect().top < innerHeight * 0.4) cur = i; });
      spy.forEach(function (a, i) { a.classList.toggle("is-cur", i === cur); });
      if (fbar) {
        var nearEnd = footer && footer.getBoundingClientRect().top < innerHeight;
        var on = y > 700 && !nearEnd;
        fbar.classList.toggle("is-on", on);
        fbar.setAttribute("aria-hidden", on ? "false" : "true");
        $$("a,button", fbar).forEach(function (el) { el.tabIndex = on ? 0 : -1; });
      }
    };
    addEventListener("scroll", onScroll, { passive: true }); onScroll();
    var top = $(".x-top");
    if (top) top.addEventListener("click", function () { scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

    /* ---------- Einblendung ---------- */
    $$(".section-head,.v-break,.v-stage,.v-frow,.v-panel,.card,.partner,.partner-wide,.v-timeline li,.answer,.v-facts>div,.faq details,.v-term,.v-ofield,.il-format,.contact-list,.v-stack-in>*,.v-phases>*,.v-situ>*,.v-cflow>*,.v-fc,.v-decide li,.v-matrix>*,.defs>div,.v-related>*")
      .forEach(function (el) { if (!el.closest(".x-tile")) el.classList.add("rv"); });
    var rv = $$(".x-rv,.x-reveal,.rv");
    rv.forEach(function (el, i) { el.style.setProperty("--d", ((i % 4) * 0.07).toFixed(2) + "s"); });
    $$(".x-hero .x-reveal").forEach(function (el, i) { el.style.setProperty("--d", (i * 0.08).toFixed(2) + "s"); });
    seen(rv, function (el) { el.classList.add("is-in"); });
    setTimeout(function () { rv.forEach(function (el) { el.classList.add("is-in"); }); }, 4000);

    /* ---------- Zahlen hochzählen ---------- */
    seen($$(".x-count,.v-nums b"), function (el) {
      if (reduce) return;
      var txt = el.textContent, parts = txt.split(/(\d+)/), t0 = performance.now(), dur = 1400;
      (function f(t) {
        var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
        el.textContent = parts.map(function (s) { return /^\d+$/.test(s) ? Math.round(+s * e) : s; }).join("");
        if (p < 1) requestAnimationFrame(f); else el.textContent = txt;
      })(t0);
    }, { threshold: 0.6 });

    /* ---------- Ticker ---------- */
    var tk = $(".x-tk");
    if (tk && !reduce) {
      var lines = tk.getAttribute("data-lines").split("|"), li = 0;
      setInterval(function () {
        tk.classList.add("is-out");
        setTimeout(function () { li = (li + 1) % lines.length; tk.textContent = lines[li]; tk.classList.remove("is-out"); }, 400);
      }, 3800);
    }

    /* ---------- Hero: Brücke aus vier Stufen ---------- */
    var rg = $("#x-range");
    if (rg) {
      var planks = $$(".x-plank"), st = $(".x-state"), out = $(".x-outv"), render = $(".x-render");
      var setB = function (v) {
        planks.forEach(function (p, k) { p.classList.toggle("on", k < v); });
        out.textContent = v + " / 4";
        var names = $(".x-planks").getAttribute("data-names").split("|");
        st.textContent = v >= 4 ? st.getAttribute("data-s2") : v === 0 ? st.getAttribute("data-s0") : "Stufe " + v + " · " + names[v - 1];
        render.classList.toggle("is-done", v >= 4);
      };
      rg.addEventListener("input", function () { setB(+rg.value); });
      setB(+rg.value);
      if (!reduce) {
        var auto = setInterval(function () { var v = +rg.value; if (v >= 4) { clearInterval(auto); return; } rg.value = v + 1; setB(v + 1); }, 1300);
        ["pointerdown", "keydown"].forEach(function (ev) { rg.addEventListener(ev, function () { clearInterval(auto); }); });
      }
      var stage = $(".x-stage");
      if (stage && !reduce && hover) {
        stage.addEventListener("pointermove", function (e) {
          var b = stage.getBoundingClientRect(), x = (e.clientX - b.left) / b.width - 0.5, y = (e.clientY - b.top) / b.height - 0.5;
          render.style.transform = "rotateY(" + (x * 5) + "deg) rotateX(" + (-y * 4) + "deg)";
        });
        stage.addEventListener("pointerleave", function () { render.style.transform = ""; });
      }
    }

    /* ---------- Problem: Leitung mit Lecks ---------- */
    var pipe = $(".x-pipe-wrap");
    if (pipe) {
      var sw = $(".x-switch", pipe);
      sw.addEventListener("click", function () {
        var closed = pipe.getAttribute("data-state") !== "closed";
        pipe.setAttribute("data-state", closed ? "closed" : "open");
        sw.setAttribute("aria-pressed", closed ? "true" : "false");
      });
      var leaks = $$(".x-leak"), cards = $$(".x-break");
      var hot = function (i, on) {
        leaks.forEach(function (l) { l.classList.toggle("is-hot", on && +l.dataset.i === i); });
        cards.forEach(function (c) { c.classList.toggle("is-hot", on && +c.dataset.i === i); });
      };
      cards.concat(leaks).forEach(function (el) {
        var i = +el.dataset.i;
        el.addEventListener("mouseenter", function () { hot(i, true); });
        el.addEventListener("mouseleave", function () { hot(i, false); });
        el.addEventListener("focusin", function () { hot(i, true); });
        el.addEventListener("focusout", function () { hot(i, false); });
      });
    }

    /* ---------- Vier Stufen: Etagen ---------- */
    var floors = $$(".x-floor");
    if (floors.length) {
      var ordered = floors.slice().sort(function (a, b) { return +a.dataset.i - +b.dataset.i; });
      tabs(ordered, $$(".x-panel"));
      var chain = $(".x-chainbtn"), tower = $(".x-tower");
      chain.addEventListener("click", function () {
        var on = tower.classList.toggle("is-chain");
        chain.setAttribute("aria-pressed", on ? "true" : "false");
      });
    }

    /* ---------- Fokusfelder: Venn, Perspektiven, Wegweiser ---------- */
    var ptabs = $$(".x-ptab");
    if (ptabs.length) {
      var venn = $(".x-venn"), circles = $$(".x-vc"), situs = $$(".x-situ");
      var fs = ptabs.map(function (b) { return b.dataset.f; });
      var selF = tabs(ptabs, $$(".x-pane"), function (i) {
        venn.classList.add("has-sel");
        circles.forEach(function (c) { c.classList.toggle("is-sel", c.dataset.f === fs[i]); });
      });
      circles.forEach(function (c) {
        c.addEventListener("click", function () { selF(fs.indexOf(c.dataset.f)); });
      });
      situs.forEach(function (s) {
        s.addEventListener("click", function () {
          situs.forEach(function (o) { o.classList.toggle("on", o === s); });
          selF(fs.indexOf(s.dataset.f));
          var p = $(".x-persp"); if (p && p.getBoundingClientRect().top < 0) p.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "center" });
        });
      });
    }

    /* ---------- Vorher / Nachher ---------- */
    var cmp = $(".x-cmp"), cr = $("#x-cmp");
    if (cmp && cr) {
      var setC = function (v) { cmp.style.setProperty("--p", v / 100); cmp.classList.toggle("show-a", v < 60); cmp.classList.toggle("show-b", v > 40); };
      cr.addEventListener("input", function () { setC(+cr.value); });
      $$(".x-cmp-ctl button").forEach(function (b) { b.addEventListener("click", function () { cr.value = b.dataset.to; setC(+cr.value); }); });
      setC(0);
      if (!reduce) seen([cmp], function () {
        var t0 = performance.now(), touched = false;
        cr.addEventListener("pointerdown", function () { touched = true; });
        (function f(t) {
          if (touched) return;
          var p = Math.min(1, (t - t0) / 2600), v = Math.round((1 - Math.cos(p * Math.PI)) * 50);
          cr.value = v; setC(v);
          if (p < 1) requestAnimationFrame(f);
        })(t0);
      }, { threshold: 0.5 });
    }

    /* ---------- KI-Ringe ---------- */
    seen($$(".x-r-val"), function (c) {
      var v = +c.getAttribute("data-v");
      c.style.strokeDashoffset = String(314.16 * (1 - v / 100));
    }, { threshold: 0.4 });

    /* ---------- Zeitleisten, Balken ---------- */
    seen($$(".x-time,.v-gapdemo,.v-timeline,.x-gantt,.x-scale"), function (el) { el.classList.add("is-in"); }, { threshold: 0.35 });

    /* ---------- Fachbegriffe ---------- */
    var terms = $$(".x-term"), defs = $$(".x-def");
    terms.forEach(function (t) {
      t.addEventListener("click", function () {
        terms.forEach(function (o) { var on = o === t; o.classList.toggle("on", on); o.setAttribute("aria-pressed", on ? "true" : "false"); });
        defs.forEach(function (d) { var on = d.dataset.t === t.dataset.t; d.classList.toggle("on", on); d.hidden = !on; });
      });
    });
  });
})();
