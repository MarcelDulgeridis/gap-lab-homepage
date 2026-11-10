(function () {
    "use strict";

    var CONFIG = {
      supabaseUrl: "https://sglvltcqxovsfyagbgmi.supabase.co",
      supabaseKey: "sb_publishable_FKbVgnP943mmN9LxQ4KNNQ_DOEKcF9u",
      table: "ki_check_leads",
      assessment: "ki-readiness-check",
      contactUrl: "/kontakt",
      teamMax: 10,
      teamMinGroup: 5,
      // Öffentliche Adresse dieser Seite (für den Teilen-Link). Leer = aktuelle Adresse.
      shareUrl: ""
    };

    var SIGNALS = [
      { id: "strategy", no: "01", label: "Strategy & Vision",
        prompt: "AI is part of our strategy, with clear goals for efficiency, quality or customer value, not just a tool trial.",
        why: "Without a clear vision, AI initiatives remain piecemeal and compete for the same resources.",
        action: "Translate the AI vision for the next 12 months into three measurable outcomes and two deliberate non-goals." },
      { id: "usecases", no: "02", label: "Use Cases",
        prompt: "We have concrete AI use cases, prioritised by benefit, effort and risk.",
        why: "If you pilot everything at once, you cannot prove anything in the end.",
        action: "Assess five candidates on a benefit–feasibility matrix and launch exactly one pilot with a success criterion." },
      { id: "data", no: "03", label: "Data & Systems",
        prompt: "Documents and data are structured, our systems are integrated and access rights are clearly defined.",
        why: "AI is only as good as the data it is allowed to access.",
        action: "For the prioritised use case, review data sources, quality and access rights and close the biggest gap." },
      { id: "governance", no: "04", label: "Governance & Legal",
        prompt: "There are binding rules for AI use: approved tools, data protection, confidentiality and review obligations.",
        why: "Without clear rules, shadow AI emerges, with liability and reputational risk.",
        action: "Adopt a one-page AI usage policy with an approved tools list, data classes and a four-eyes rule." },
      { id: "skills", no: "05", label: "Skills",
        prompt: "Employees can use AI safely and check results for accuracy. Training and points of contact are in place.",
        why: "The EU AI Act requires AI literacy. Without it, the risk of misuse increases.",
        action: "Set up short role-based training using real work situations and appoint an AI champion in each team." },
      { id: "leadership", no: "06", label: "Leadership & Change",
        prompt: "Leadership visibly supports AI, involves employees and addresses concerns openly.",
        why: "Without visible leadership, every AI initiative loses momentum after the kick-off.",
        action: "Formulate a shared leadership narrative: why AI, what changes, what stays the same. Add an open Q&A format." },
      { id: "adoption", no: "07", label: "Everyday Use",
        prompt: "AI is actually used in everyday work. Usage and reasons for abandoning it are visible.",
        why: "Available is not the same as used. Without usage data, impact remains an assumption.",
        action: "Track usage and reasons for abandonment separately for four weeks and discuss them in a regular review." },
      { id: "impact", no: "08", label: "Impact & Business Case",
        prompt: "AI initiatives have a baseline, target value and KPIs for time, quality, cost or risk.",
        why: "Without a baseline, you can neither prove impact nor justify the next investment.",
        action: "Set the baseline, target value, data source and review date for the pilot before it starts." }
    ];

    var SCALE = ["Not at all", "Slightly", "Partly", "Largely", "Fully"];
    var PEOPLE = ["skills", "leadership", "adoption"];

    var OFFERS = {
      essential: { eyebrow: "Next sensible step", name: "Essential management baseline",
        reason: "Your foundation is solid. A structured management baseline with a 90-day path makes progress measurable before you scale." },
      professional: { eyebrow: "Multi-perspective view recommended", name: "THE GAP Professional",
        reason: "Your result hinges on how your team really thinks. Professional measures management and employee perspectives separately and anonymously, and reveals the real gap." },
      executive: { eyebrow: "Expert validation recommended", name: "Executive Review",
        reason: "The signal is clear. Before investing further in AI, the starting position, priorities and risks should be validated together." },
      diagnostic: { eyebrow: "Root-cause analysis recommended", name: "Dual Perspective Diagnostic",
        reason: "The signal is critical. Causes, differences in perspective, risks and economic exposure should be examined rigorously, not estimated." }
    };

    var LEVELS = {
      Focused: { title: "AI-ready with clear levers", copy: "Your organisation has a strong foundation. The next step is to prove impact and scale." },
      Material: { title: "On track, but held back", copy: "The direction is right, but some areas are noticeably holding things back before AI can make an impact in everyday work." },
      High: { title: "The foundation is still missing", copy: "AI ambition and organisational reality are far apart. Investments risk fizzling out." },
      Critical: { title: "Early stage with risk", copy: "Before rolling out further AI tools, you need a vision, rules and enablement." }
    };

    var STORE_KEY = "the-gap-ki-check-v1";
    var LEAD_QUEUE_KEY = "the-gap-sa-leads";
    var $ = function (id) { return document.getElementById(id); };
    var state = load() || fresh();
    var tracking = captureTracking();
    var VS = parseVs();
    var TEAM = parseTeam();
    var teamData = null;

    function fresh() { return { view: "landing", step: 0, self: {}, team: {}, unlocked: false, email: "" }; }
    function load() {
      try { var s = JSON.parse(localStorage.getItem(STORE_KEY)); return s && s.self ? s : null; } catch (e) { return null; }
    }
    function save() { try { localStorage.setItem(STORE_KEY, JSON.stringify(state)); } catch (e) {} }
    function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
    function complete(q) { return state.self[q.id] !== undefined && state.team[q.id] !== undefined; }
    function doneCount() { return SIGNALS.filter(complete).length; }

    // UTM-Parameter und LinkedIn-Klick-ID merken, damit sie auch nach Neuladen mit dem Lead gespeichert werden
    function captureTracking() {
      var p = new URLSearchParams(location.search), t = {};
      ["utm_source", "utm_medium", "utm_campaign", "utm_content", "ref", "li_fat_id"].forEach(function (k) { if (p.get(k)) t[k] = p.get(k).slice(0, 80); });
      try {
        if (Object.keys(t).length) sessionStorage.setItem("the-gap-utm", JSON.stringify(t));
        else t = JSON.parse(sessionStorage.getItem("the-gap-utm") || "{}");
      } catch (e) {}
      return t;
    }
    function referrerString() {
      var t = tracking;
      if (t.utm_source || t.utm_campaign) return [t.utm_source, t.utm_medium, t.utm_campaign, t.utm_content].map(function (x) { return x || "-"; }).join("|").slice(0, 200);
      return (t.ref || document.referrer || "").slice(0, 200) || null;
    }

    // Vergleich ohne Backend: Die Eigeneinschätzung der einladenden Person steckt als 8 Ziffern im Link (?vs=31213320)
    function parseVs() {
      var raw = new URLSearchParams(location.search).get("vs");
      try {
        if (raw && /^[0-4]{8}$/.test(raw)) sessionStorage.setItem("the-gap-vs", raw);
        else raw = sessionStorage.getItem("the-gap-vs");
      } catch (e) {}
      if (!raw || !/^[0-4]{8}$/.test(raw)) return null;
      var vs = {};
      SIGNALS.forEach(function (q, i) { vs[q.id] = Number(raw.charAt(i)); });
      return { raw: raw, answers: vs };
    }
    // Team-Modus: anonymes Teambild über Supabase-Funktionen (siehe THE-GAP-KI-Check-Team-Modus.sql)
    function parseTeam() {
      var raw = new URLSearchParams(location.search).get("team");
      try {
        if (raw && /^[A-HJ-NP-Z2-9]{10}$/i.test(raw)) sessionStorage.setItem("the-gap-team", raw.toUpperCase());
        else raw = sessionStorage.getItem("the-gap-team");
      } catch (e) {}
      return raw && /^[A-HJ-NP-Z2-9]{10}$/i.test(raw) ? raw.toUpperCase() : null;
    }
    function rpc(fn, args) {
      return fetch(CONFIG.supabaseUrl.replace(/\/+$/, "") + "/rest/v1/rpc/" + fn, {
        method: "POST",
        headers: { "apikey": CONFIG.supabaseKey, "Content-Type": "application/json" },
        body: JSON.stringify(args)
      }).then(function (res) {
        if (!res.ok) return res.text().then(function (t) { throw new Error("HTTP " + res.status + " " + t.slice(0, 160)); });
        return res.json();
      });
    }
    function selfCode() { return SIGNALS.map(function (q) { return state.self[q.id] || 0; }).join(""); }
    function teamCode() { return state.teamCode || TEAM; }
    function teamUrl(code) {
      var base = CONFIG.shareUrl || (location.origin + location.pathname);
      return base + "?team=" + code + "&utm_source=team&utm_medium=referral&utm_campaign=ki-readiness-check";
    }
    function teamError(msg) { $("teamError").textContent = msg; $("teamError").hidden = !msg; }
    function teamFail(err) { console.warn("[THE GAP] Team mode:", err); teamError("The team snapshot is currently unavailable. Please try again later."); }

    function createTeam() {
      var btn = $("teamCreateBtn");
      btn.disabled = true;
      teamError("");
      rpc("create_check_team", { p_label: null }).then(function (code) {
        state.teamCode = code;
        return submitTeam(code);
      }).catch(function (e) { btn.disabled = false; teamFail(e); });
    }
    function submitTeam(code) {
      return rpc("submit_check_team_response", { p_code: code, p_answers: selfCode() }).then(function (r) {
        if (!r.ok && r.reason === "full") { teamError("This team is already full (10 of 10). For larger groups, there is THE GAP Professional."); }
        else if (!r.ok) { teamError("This team link is invalid or has expired."); return; }
        state.teamJoined = state.teamJoined || {};
        state.teamJoined[code] = true;
        save();
        return loadTeam();
      });
    }
    function loadTeam() {
      var code = teamCode();
      if (!code) return Promise.resolve();
      return rpc("get_check_team_result", { p_code: code }).then(function (r) {
        if (!r.ok) { teamError("This team link is invalid or has expired."); teamData = null; }
        else { teamData = r; teamError(""); }
        renderTeam();
      }).catch(teamFail);
    }
    function renderTeam() {
      var code = teamCode();
      var joined = code && state.teamJoined && state.teamJoined[code];
      $("teamStart").hidden = !!code;
      $("teamJoin").hidden = !(code && !joined);
      $("teamLive").hidden = !(code && joined);
      if (!(code && joined)) return;
      $("teamLink").value = teamUrl(code);
      $("teamMailBtn").href = "mailto:?subject=" + encodeURIComponent("Our AI team picture: 3 minutes, anonymous") +
        "&body=" + encodeURIComponent(teamInviteText() + "\n\n" + teamUrl(code) + "\n\nNo names or email addresses are stored. The team picture only shows averages, and only once there are 5 responses.");
      var d = teamData || { count: 1, max: CONFIG.teamMax, ready: false };
      var left = Math.max(0, CONFIG.teamMinGroup - d.count);
      $("teamTitle").textContent = d.ready ? "Your team snapshot" : "" + left + (left === 1 ? " response" : " responses") + " to go until the team picture";
      $("teamCopy").textContent = d.ready
        ? "Anonymous average of " + d.published_n + " responses. The snapshot is updated at 5, 8 and 10 responses so that no individual response can be traced back."
        : "Share the link with your team, in Teams, Slack or by email. As soon as 5 people have responded, everyone sees the anonymous team snapshot.";
      var bars = "";
      for (var i = 0; i < CONFIG.teamMax; i++) bars += '<i class="' + (i < d.count ? "on" : "") + (i === CONFIG.teamMinGroup - 1 ? " min" : "") + '"></i>';
      $("teamProgress").innerHTML = bars;
      $("teamCount").textContent = d.count + " of " + d.max + " responses";
      $("teamLinkWrap").hidden = d.count >= d.max;
      $("teamResult").hidden = !d.ready;
      if (!d.ready) return;
      var me = SIGNALS.map(function (q) { return (state.self[q.id] || 0) * 25; });
      var sig = d.signals.map(function (x, k) { return { label: SIGNALS[k].label, mean: x.mean, spread: x.spread, me: me[k] }; });
      var top = sig.slice().sort(function (a, b) { return b.spread - a.spread; })[0];
      $("teamScore").textContent = Math.round(sig.reduce(function (a, x) { return a + x.mean; }, 0) / sig.length);
      $("teamMe").textContent = Math.round(me.reduce(function (a, x) { return a + x; }, 0) / me.length);
      $("teamSplit").textContent = top.label;
      $("teamRows").innerHTML = sig.map(function (x) {
        var lo = Math.max(0, x.mean - x.spread), hi = Math.min(100, x.mean + x.spread);
        return '<div class="t-row' + (x === top && x.spread > 0 ? " hot" : "") + '"><span class="lbl">' + x.label + '<small>Spread ±' + x.spread + '</small></span>' +
          '<span class="t-bar"><u data-l="' + lo + '" data-w="' + (hi - lo) + '"></u><i data-w="' + x.mean + '"></i><em data-l="' + x.me + '"></em></span>' +
          '<span class="val">Team ' + x.mean + '</span></div>';
      }).join("");
      Array.prototype.forEach.call($("teamRows").querySelectorAll("[data-l],[data-w]"), function (el) {
        if (el.hasAttribute("data-l")) el.style.left = el.getAttribute("data-l") + "%";
        if (el.hasAttribute("data-w")) el.style.width = el.getAttribute("data-w") + "%";
      });
    }
    function teamInviteText() {
      return "I have set up an anonymous AI Readiness Check for our team (3 minutes, no login). Once there are 5 responses, we can see together where we stand:";
    }
    function shareTeam() {
      var url = teamUrl(teamCode());
      var text = teamInviteText();
      if (navigator.share) { navigator.share({ title: "AI team picture · THE GAP", text: text, url: url }).catch(function () {}); return; }
      copyTeam();
    }
    function copyTeam() {
      var url = teamUrl(teamCode());
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(function () { toast("Team link copied."); }, function () { $("teamLink").select(); });
      } else $("teamLink").select();
    }

    function inviteUrl() {
      var base = CONFIG.shareUrl || (location.origin + location.pathname);
      var code = SIGNALS.map(function (q) { return state.self[q.id] || 0; }).join("");
      return base + "?vs=" + code + "&utm_source=colleague&utm_medium=referral&utm_campaign=ki-readiness-check";
    }
    function inviteText() {
      return VS
        ? "I have taken the AI Readiness Check too. Use this link to see our comparison:"
        : "I have just taken the AI Readiness Check by THE GAP (3 minutes). Will you take it too? Afterwards we can see where we assess our organisation differently:";
    }

    function result() {
      var rows = SIGNALS.map(function (q) {
        var s = (state.self[q.id] || 0) * 25, t = (state.team[q.id] || 0) * 25;
        return { id: q.id, no: q.no, label: q.label, action: q.action, why: q.why, self: s, team: t, diff: s - t };
      });
      var avg = function (k) { return Math.round(rows.reduce(function (a, r) { return a + r[k]; }, 0) / rows.length); };
      var score = avg("self"), teamScore = avg("team");
      var gap = Math.round(rows.reduce(function (a, r) { return a + Math.abs(r.diff); }, 0) / rows.length);
      var byScore = rows.slice().sort(function (a, b) { return a.self - b.self || a.no.localeCompare(b.no); });
      var hot = rows.slice().sort(function (a, b) { return Math.abs(b.diff) - Math.abs(a.diff) || a.no.localeCompare(b.no); })[0];
      var level = score >= 75 ? "Focused" : score >= 55 ? "Material" : score >= 35 ? "High" : "Critical";
      var offer = (100 - score) >= 65 ? OFFERS.diagnostic
        : (gap >= 20 || PEOPLE.indexOf(byScore[0].id) !== -1) ? OFFERS.professional
        : (100 - score) >= 45 ? OFFERS.executive : OFFERS.essential;
      return { rows: rows, score: score, teamScore: teamScore, gap: gap, prio: byScore[0], low3: byScore.slice(0, 3), hot: hot, level: level, offer: offer };
    }

    function gapInsight(r) {
      var dir = r.score - r.teamScore;
      if (r.gap < 10) return "<b>You expect hardly any difference between your view and your team’s.</b> That is possible, but rare. In real measurements, management and employees often diverge significantly. Only a real survey can show whether that is the case for you.";
      if (dir > 0) return "<b>You assume that, on average, your team rates the situation " + dir + " points lower than you do.</b> This very gap is a strong early indicator of resistance and unused tools. The real question is whether it is actually larger.";
      if (dir < 0) return "<b>You assume your team is further ahead than you are.</b> This may point to shadow AI: employees using AI before rules and goals are in place.";
      return "<b>Your gap lies in individual areas, not in the average.</b> Where perspectives diverge, friction and delays typically arise.";
    }

    function scaleHtml(name, value) {
      return SCALE.map(function (label, i) {
        var id = name + i;
        return '<div class="opt"><input type="radio" name="' + name + '" id="' + id + '" value="' + i + '"' + (value === i ? " checked" : "") + '>' +
          '<label for="' + id + '"><span class="opt-val">' + i + '</span><span class="opt-label">' + label + '</span></label></div>';
      }).join("");
    }

    function renderQuestion(focus) {
      var q = SIGNALS[state.step];
      var s = state.self[q.id], t = state.team[q.id];
      $("qCounter").textContent = "Signal " + q.no + " / 08";
      $("qAnswered").textContent = doneCount() + " of 8 answered";
      $("progress").setAttribute("aria-valuenow", String(doneCount()));
      $("progress").innerHTML = SIGNALS.map(function (x, i) {
        return '<i class="' + (complete(x) ? "on" : i === state.step ? "cur" : "") + '"></i>';
      }).join("");
      $("qLabel").textContent = q.label;
      $("qTitle").textContent = q.prompt;
      $("qWhy").textContent = q.why;
      $("scaleSelf").querySelector(".scale").innerHTML = scaleHtml("self", s);
      $("scaleTeam").querySelector(".scale").innerHTML = scaleHtml("team", t);
      $("qGap").innerHTML = s !== undefined && t !== undefined
        ? (s === t ? "No difference in this signal." : 'Gap in this signal: <b>' + Math.abs(s - t) * 25 + ' points</b>')
        : "";
      $("backBtn").disabled = state.step === 0;
      $("nextBtn").disabled = !complete(q);
      $("nextBtn").innerHTML = (state.step === SIGNALS.length - 1 ? "Show result" : "Next") + ' <span aria-hidden="true">→</span>';
      if (focus) $("qTitle").focus({ preventScroll: true });
    }

    function renderResult() {
      var r = result(), L = LEVELS[r.level];
      $("score").textContent = r.score;
      $("gap").textContent = r.gap;
      $("resTitle").textContent = L.title;
      $("resCopy").textContent = L.copy;
      $("gapInsight").innerHTML = gapInsight(r);
      $("prioLabel").textContent = r.prio.label + " · " + r.prio.self;
      $("prioAction").textContent = r.prio.action;
      $("hotLabel").textContent = r.hot.label + " · " + Math.abs(r.hot.diff) + " points";
      $("hotText").textContent = r.hot.diff === 0 ? "You do not expect a difference in any signal."
        : r.hot.diff > 0 ? "This is where you suspect the greatest distance between your view and your team’s experience."
        : "Here you rate your team as considerably further ahead than yourself.";
      $("printDate").textContent = new Date().toLocaleDateString("en-GB", { day: "2-digit", month: "long", year: "numeric" });
      renderCompare(r);
      renderTeam();
      if (teamCode() && state.teamJoined && state.teamJoined[teamCode()] && !teamData) loadTeam();
      $("mailBtn").href = "mailto:?subject=" + encodeURIComponent("AI Readiness Check: shall we compare?") +
        "&body=" + encodeURIComponent(inviteText() + "\n\n" + inviteUrl());

      $("gateWrap").hidden = state.unlocked;
      $("report").hidden = !state.unlocked;
      $("printBtn").hidden = !state.unlocked;
      if (!state.unlocked) return;

      $("rows").innerHTML = r.rows.map(function (x) {
        var hot = x.id === r.hot.id && x.diff !== 0;
        return '<div class="row' + (hot ? " hot" : "") + '"><span class="row-label">' + x.label + '<small>You ' + x.self + ' · Team ' + x.team + '</small></span>' +
          '<span class="bars"><span class="bar self"><i data-w="' + x.self + '"></i></span><span class="bar team"><i data-w="' + x.team + '"></i></span></span>' +
          '<span class="row-gap">' + Math.abs(x.diff) + '<small>Gap</small></span></div>';
      }).join("");
      var phases = ["Days 0–30", "Days 31–60", "Days 61–90"];
      $("plan").innerHTML = r.low3.map(function (x, i) {
        return '<li><b>' + phases[i] + '</b><h4>' + x.label + '</h4><p>' + x.action + '</p></li>';
      }).join("");
      $("offerEyebrow").textContent = r.offer.eyebrow;
      $("offerName").textContent = r.offer.name;
      $("offerReason").textContent = r.offer.reason;
      $("offerBtn").innerHTML = "Discuss the result " + '<span aria-hidden="true">↗</span>';
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          Array.prototype.forEach.call(document.querySelectorAll(".bar i"), function (el) { el.style.width = el.getAttribute("data-w") + "%"; });
        });
      });
    }

    function renderCompare(r) {
      $("compare").hidden = !VS;
      $("shareTitle").firstChild.nodeValue = VS ? "Send comparison back" : "Are you right about your team?";
      $("shareText").textContent = VS
        ? "Send the link back to the person who invited you. They will then see the same comparison."
        : "Send the check to a colleague. After three minutes, you will both see where your assessments differ. Only your result travels with the link, nothing else.";
      $("shareBtn").innerHTML = (VS ? "Send comparison back" : "Invite a colleague") + ' <span aria-hidden="true">→</span>';
      if (!VS) return;
      var rows = r.rows.map(function (x) { var t = VS.answers[x.id] * 25; return { label: x.label, me: x.self, them: t, d: Math.abs(x.self - t) }; });
      var them = Math.round(rows.reduce(function (a, x) { return a + x.them; }, 0) / rows.length);
      var diff = Math.round(rows.reduce(function (a, x) { return a + x.d; }, 0) / rows.length);
      var top = rows.slice().sort(function (a, b) { return b.d - a.d; })[0];
      $("compareTitle").textContent = diff < 10 ? "You see your organisation very similarly" : diff < 25 ? "You see your organisation differently" : "You see two different organisations";
      $("cmpMe").textContent = r.score;
      $("cmpThem").textContent = them;
      $("cmpDiff").textContent = diff;
      $("compareText").textContent = top.d === 0
        ? "You do not differ on any signal. It gets interesting when you include employees without a leadership role."
        : "You are furthest apart on “" + top.label + "“ (" + top.d + " points). Even two people see the same organisation differently. With 50 or 500 employees, this difference becomes a management issue.";
      $("compareRows").innerHTML = rows.map(function (x) {
        return '<div class="row' + (x === top && x.d ? " hot" : "") + '"><span class="row-label">' + x.label + '<small>You ' + x.me + ' · Colleague ' + x.them + '</small></span>' +
          '<span class="bars"><span class="bar self"><i data-w="' + x.me + '"></i></span><span class="bar them"><i data-w="' + x.them + '"></i></span></span>' +
          '<span class="row-gap">' + x.d + '<small>Δ</small></span></div>';
      }).join("");
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          Array.prototype.forEach.call(document.querySelectorAll("#compareRows .bar i"), function (el) { el.style.width = el.getAttribute("data-w") + "%"; });
        });
      });
    }

    function render(focus) {
      var inCheck = state.view !== "landing";
      $("vsBanner").hidden = !VS || !!TEAM;
      $("teamBanner").hidden = !TEAM;
      $("landing").hidden = inCheck;
      $("check").hidden = !inCheck;
      $("viewQuestion").hidden = state.view !== "question";
      $("viewResult").hidden = state.view !== "result";
      if (state.view === "question") renderQuestion(focus);
      if (state.view === "result") renderResult();
      save();
    }

    function go(view) {
      state.view = view;
      render(true);
      window.scrollTo({ top: 0, behavior: "auto" });
      if (view === "result") $("resTitle").focus({ preventScroll: true });
    }

    function start() {
      if (doneCount() === SIGNALS.length) { go("result"); return; }
      state.step = Math.max(0, SIGNALS.findIndex(function (q) { return !complete(q); }));
      go("question");
    }

    function setAnswer(kind, v) {
      var q = SIGNALS[state.step];
      state[kind][q.id] = v;
      render(false);
      if (complete(q) && state.step < SIGNALS.length - 1) {
        var at = state.step;
        setTimeout(function () { if (state.step === at && state.view === "question") next(); }, 450);
      }
    }

    function next() {
      if (!complete(SIGNALS[state.step])) return;
      if (state.step < SIGNALS.length - 1) { state.step += 1; render(true); scrollToPanel(); return; }
      go("result");
    }
    function back() { if (state.step > 0) { state.step -= 1; render(true); scrollToPanel(); } }
    function scrollToPanel() {
      var hd = document.querySelector(".site-header"), off = (hd ? hd.offsetHeight : 0) + 12;
      var top = $("viewQuestion").getBoundingClientRect().top;
      if (top < off) window.scrollTo({ top: window.scrollY + top - off, behavior: "auto" });
    }

    function toast(msg) {
      var t = $("toast");
      t.textContent = msg;
      t.classList.add("show");
      clearTimeout(toast.timer);
      toast.timer = setTimeout(function () { t.classList.remove("show"); }, 4200);
    }

    // Handy: natives Teilen-Menü (Teams, WhatsApp, Mail …). Desktop: Link kopieren.
    function share() {
      var url = inviteUrl(), text = inviteText();
      if (navigator.share) {
        navigator.share({ title: "AI Readiness Check · THE GAP", text: text, url: url }).catch(function () {});
        return;
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text + " " + url).then(
          function () { toast("Invitation copied. Simply paste it into Teams, Slack or a message."); },
          function () { window.prompt("Copy link:", url); });
      } else window.prompt("Copy link:", url);
    }

    function queueLocally(payload, reason) {
      try {
        var list = JSON.parse(localStorage.getItem(LEAD_QUEUE_KEY) || "[]");
        list.push(Object.assign({ queued_reason: reason }, payload));
        localStorage.setItem(LEAD_QUEUE_KEY, JSON.stringify(list));
      } catch (e) {}
    }
    function leadError(msg) { $("leadError").textContent = msg; $("leadError").hidden = !msg; }

    function saveLead(e) {
      e.preventDefault();
      var email = $("email").value.trim().toLowerCase();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) { leadError("Please enter a valid email address."); $("email").focus(); return; }
      if (!$("consent").checked) { leadError("Please confirm your consent so that we may store your report."); return; }
      leadError("");

      var r = result();
      var answers = { site: location.hostname, self: {}, team: {}, team_score: r.teamScore, role: $("role").value || null, tracking: tracking, compared_with: VS ? VS.raw : null, team_code: teamCode() || null };
      r.rows.forEach(function (x) { answers.self[x.id] = state.self[x.id]; answers.team[x.id] = state.team[x.id]; });
      var payload = {
        email: email,
        organisation: $("org").value.trim() || null,
        consent: true,
        assessment: CONFIG.assessment,
        score: r.score,
        gap: r.gap,
        level: r.level,
        priority: r.prio.label,
        recommended_offer: r.offer.name,
        answers: answers,
        referrer: referrerString()
      };

      var btn = $("leadBtn");
      btn.disabled = true;
      btn.textContent = "Unlocking …";
      function done() {
        state.unlocked = true;
        state.email = email;
        render(false);
        toast("Unlocked. Your full report is below.");
        $("report").scrollIntoView({ behavior: "smooth", block: "start" });
      }
      function fail(err) {
        queueLocally(payload, String(err && err.message || err));
        console.warn("[THE GAP] Lead insert failed:", err);
        btn.disabled = false;
        btn.innerHTML = 'Try again <span aria-hidden="true">→</span>';
        leadError("Saving did not work. Please try again or contact us directly.");
      }
      if (!CONFIG.supabaseUrl || !CONFIG.supabaseKey) { queueLocally(payload, "supabase-not-configured"); done(); return; }
      fetch(CONFIG.supabaseUrl.replace(/\/+$/, "") + "/rest/v1/" + CONFIG.table, {
        method: "POST",
        headers: { "apikey": CONFIG.supabaseKey, "Content-Type": "application/json", "Prefer": "return=minimal" },
        body: JSON.stringify(payload)
      }).then(function (res) {
        if (!res.ok) return res.text().then(function (t) { throw new Error("HTTP " + res.status + " " + t.slice(0, 200)); });
        done();
      }).catch(fail);
    }

    $("fieldList").innerHTML = SIGNALS.map(function (q) { return '<li><b>' + q.no + '</b><span>' + esc(q.label) + '</span></li>'; }).join("");
    Array.prototype.forEach.call(document.querySelectorAll("[data-start]"), function (b) { b.addEventListener("click", start); });
    $("scaleSelf").addEventListener("change", function (e) { setAnswer("self", Number(e.target.value)); });
    $("scaleTeam").addEventListener("change", function (e) { setAnswer("team", Number(e.target.value)); });
    $("nextBtn").addEventListener("click", next);
    $("backBtn").addEventListener("click", back);
    $("shareBtn").addEventListener("click", share);
    $("leadForm").addEventListener("submit", saveLead);
    $("printBtn").addEventListener("click", function () { window.print(); });
    $("teamCreateBtn").addEventListener("click", createTeam);
    $("teamJoinBtn").addEventListener("click", function () { $("teamJoinBtn").disabled = true; submitTeam(TEAM).catch(function (e) { $("teamJoinBtn").disabled = false; teamFail(e); }); });
    $("teamShareBtn").addEventListener("click", shareTeam);
    $("teamCopyBtn").addEventListener("click", copyTeam);
    $("teamRefreshBtn").addEventListener("click", loadTeam);
    $("teamProBtn").addEventListener("click", function () { location.href = CONFIG.contactUrl + "?source=ki-readiness-check-team"; });
    $("offerBtn").addEventListener("click", function () {
      var q = "source=ki-readiness-check" + (tracking.utm_campaign ? "&utm_campaign=" + encodeURIComponent(tracking.utm_campaign) : "");
      location.href = CONFIG.contactUrl + "?" + q;
    });
    $("restartBtn").addEventListener("click", function () { var u = state.unlocked, m = state.email; state = fresh(); state.unlocked = u; state.email = m; go("landing"); });
    ["email", "consent"].forEach(function (id) { $(id).addEventListener("input", function () { leadError(""); }); });

    document.addEventListener("keydown", function (e) {
      if (state.view !== "question" || e.metaKey || e.ctrlKey || e.altKey) return;
      if (e.key === "ArrowRight" && !$("nextBtn").disabled) { e.preventDefault(); next(); }
      else if (e.key === "ArrowLeft" && e.target.type !== "radio") { e.preventDefault(); back(); }
    });

    if (state.view === "question" && doneCount() === 0 && state.step === 0 && !Object.keys(state.self).length) state.view = "landing";
    render(false);
  }());
