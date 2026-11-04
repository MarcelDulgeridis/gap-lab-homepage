/* Layout-QA: läuft nur im lokalen Test (tools/layout_qa.py), nie auf der Live-Seite. */
(function () {
  function run() {
    var out = [], vw = document.documentElement.clientWidth, H = document.documentElement.scrollHeight;
    function sel(e) { var s = e.tagName.toLowerCase(); if (e.id) s += "#" + e.id; var c = (e.getAttribute("class") || "").trim().split(/\s+/).slice(0, 2).join("."); if (c) s += "." + c; return s; }
    function skip(e) { return e.closest(".table-wrap,.sr-only,svg,script,style,noscript,[hidden],.skip-link"); }
    var all = Array.prototype.slice.call(document.body.querySelectorAll("*")).filter(function (e) { return !skip(e); });
    var sw = document.documentElement.scrollWidth;
    if (sw > vw + 1) out.push(["overflow-page", "scrollWidth " + sw + " > " + vw]);
    // Elemente rechts/links außerhalb
    all.forEach(function (e) {
      var r = e.getBoundingClientRect(); if (!r.width || !r.height) return;
      var cs = getComputedStyle(e); if (cs.visibility === "hidden" || cs.display === "none") return;
      if (r.right > vw + 1.5 && cs.position !== "fixed") out.push(["off-right", sel(e) + " right=" + Math.round(r.right)]);
      if (r.left < -1.5) out.push(["off-left", sel(e) + " left=" + Math.round(r.left)]);
      if (!e.matches(".hero,.page-hero") && (cs.overflow === "hidden" || cs.overflowX === "hidden") && e.scrollWidth > e.clientWidth + 2 && e.clientWidth > 0 && !/^(svg|img)$/i.test(e.tagName)) out.push(["clipped-x", sel(e) + " " + e.scrollWidth + ">" + e.clientWidth]);
      if (!e.matches(".hero,.page-hero") && (cs.overflow === "hidden" || cs.overflowY === "hidden") && e.scrollHeight > e.clientHeight + 2 && e.clientHeight > 0 && !/^(svg|img)$/i.test(e.tagName)) out.push(["clipped-y", sel(e) + " " + e.scrollHeight + ">" + e.clientHeight]);
    });
    // Text-Blätter
    var leaves = all.filter(function (e) {
      if (e.children.length && Array.prototype.some.call(e.children, function (c) { return !/^(br|wbr|i|em|b|strong|a|span|small|sup|sub|abbr|svg|img)$/i.test(c.tagName) && !skip(c); })) return false;
      return Array.prototype.some.call(e.childNodes, function (n) { return n.nodeType === 3 && n.textContent.trim(); });
    });
    function bg(e) {
      var el = e;
      while (el && el !== document.documentElement) {
        var cs = getComputedStyle(el);
        if (cs.backgroundImage !== "none") return null;
        var m = cs.backgroundColor.match(/rgba?\(([^)]+)\)/);
        if (m) { var p = m[1].split(",").map(parseFloat); if (p.length < 4 || p[3] > 0.95) return p; }
        el = el.parentElement;
      }
      return [251, 248, 242];
    }
    function lum(p) { var f = function (c) { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); }; return 0.2126 * f(p[0]) + 0.7152 * f(p[1]) + 0.0722 * f(p[2]); }
    var seen = {};
    leaves.forEach(function (e) {
      var r = e.getBoundingClientRect(); if (!r.width || !r.height) return;
      var cs = getComputedStyle(e); if (cs.visibility === "hidden" || cs.display === "none" || cs.opacity === "0") return;
      var fs = parseFloat(cs.fontSize);
      if (fs < 12) out.push(["font-small", sel(e) + " " + fs + "px"]);
      var b = bg(e), m = cs.color.match(/rgba?\(([^)]+)\)/);
      if (b && m) {
        var fg = m[1].split(",").map(parseFloat); if (fg.length === 4 && fg[3] < 1) { fg = [0, 1, 2].map(function (i) { return fg[i] * fg[3] + b[i] * (1 - fg[3]); }); }
        var l1 = lum(fg), l2 = lum(b), cr = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
        var large = fs >= 24 || (fs >= 18.66 && parseInt(cs.fontWeight) >= 700);
        if (cr < (large ? 3 : 4.5)) { var key = sel(e) + cr.toFixed(1); if (!seen[key]) { seen[key] = 1; out.push(["contrast", sel(e) + " " + cr.toFixed(2) + " (" + fs + "px) \"" + e.textContent.trim().slice(0, 30) + "\""]); } }
      }
    });
    // Überlappungen Text-Text
    var rects = leaves.filter(function (e) { var d = e.closest("details:not([open])"); return !d || e.matches("summary,summary *"); }).map(function (e) { var r = e.getBoundingClientRect(); return { e: e, r: r }; }).filter(function (o) { var cs = getComputedStyle(o.e); return o.r.width > 4 && o.r.height > 4 && cs.visibility !== "hidden" && cs.display !== "inline"; });
    for (var i = 0; i < rects.length; i++) for (var j = i + 1; j < rects.length; j++) {
      var a = rects[i], c = rects[j];
      if (a.e.contains(c.e) || c.e.contains(a.e)) continue;
      var ix = Math.min(a.r.right, c.r.right) - Math.max(a.r.left, c.r.left), iy = Math.min(a.r.bottom, c.r.bottom) - Math.max(a.r.top, c.r.top);
      if (ix > 3 && iy > 3) { var ar = Math.min(a.r.width * a.r.height, c.r.width * c.r.height); if (ix * iy > 0.2 * ar) out.push(["overlap", sel(a.e) + " <> " + sel(c.e) + " @y" + Math.round(a.r.top + window.scrollY)]); }
    }
    // Bilder
    Array.prototype.forEach.call(document.images, function (im) {
      if (skip(im)) return; var r = im.getBoundingClientRect(); if (!r.width) return;
      if (im.complete && !im.naturalWidth) out.push(["img-broken", im.getAttribute("src")]);
      else if (im.naturalWidth) {
        if (r.width > im.naturalWidth * 1.6) out.push(["img-upscaled", im.getAttribute("src") + " " + Math.round(r.width) + ">" + im.naturalWidth]);
        var cs = getComputedStyle(im); if (cs.objectFit === "fill" || cs.objectFit === "") { var d = Math.abs((r.width / r.height) / (im.naturalWidth / im.naturalHeight) - 1); if (d > 0.04) out.push(["img-distorted", im.getAttribute("src") + " " + (d * 100).toFixed(0) + "%"]); }
      }
    });
    // Tippflächen (Mobil)
    if (vw <= 820) Array.prototype.forEach.call(document.querySelectorAll("button,.btn,.site-nav a,summary,.nav-toggle,.v-az a,.chips a"), function (e) {
      if (skip(e)) return; var r = e.getBoundingClientRect(); if (!r.width) return; if (r.height < 40 || r.width < 40) out.push(["tap-small", sel(e) + " " + Math.round(r.width) + "x" + Math.round(r.height)]);
    });
    // Kopfzeile bricht um
    var hd = document.querySelector(".site-header"); if (hd && vw > 900 && hd.getBoundingClientRect().height > 90) out.push(["header-wrap", "Höhe " + Math.round(hd.getBoundingClientRect().height)]);
    // Überschriften: Einzelwort-Zeile (Witwe) in h1/h2
    document.querySelectorAll("h1,h2").forEach(function (h) { if (skip(h)) return; var r = document.createRange(); r.selectNodeContents(h); var rc = Array.prototype.slice.call(r.getClientRects()); var lines = {}; rc.forEach(function (x) { lines[Math.round(x.top)] = (lines[Math.round(x.top)] || 0) + x.width; }); var ks = Object.keys(lines); if (ks.length > 2) { var last = lines[ks[ks.length - 1]], tot = h.getBoundingClientRect().width; if (last < tot * 0.18) out.push(["heading-widow", sel(h) + " \"" + h.textContent.trim().slice(0, 40) + "\""]); } });
    var pre = document.createElement("pre"); pre.id = "qa-out"; pre.textContent = JSON.stringify({ h: H, vw: vw, issues: out }); document.body.appendChild(pre);
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { setTimeout(run, 300); }); else window.addEventListener("load", function () { setTimeout(run, 500); });
})();
