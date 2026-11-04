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
      { id: "strategy", no: "01", label: "Strategie & Zielbild",
        prompt: "KI ist Teil unserer Strategie, mit klaren Zielen für Effizienz, Qualität oder Kundenmehrwert, nicht nur ein Tooltest.",
        why: "Ohne Zielbild bleiben KI-Initiativen Stückwerk und konkurrieren um dieselben Ressourcen.",
        action: "KI-Zielbild für die nächsten 12 Monate in drei messbare Outcomes und zwei bewusste Nicht-Ziele übersetzen." },
      { id: "usecases", no: "02", label: "Anwendungsfälle",
        prompt: "Wir haben konkrete KI-Anwendungsfälle, priorisiert nach Nutzen, Aufwand und Risiko.",
        why: "Wer alles gleichzeitig pilotiert, kann am Ende nichts belegen.",
        action: "Fünf Kandidaten auf einer Nutzen-Umsetzbarkeits-Matrix bewerten und genau einen Piloten mit Erfolgskriterium starten." },
      { id: "data", no: "03", label: "Daten & Systeme",
        prompt: "Dokumente und Daten liegen strukturiert vor, unsere Systeme sind integriert und Zugriffsrechte geklärt.",
        why: "KI ist nur so gut wie die Daten, auf die sie zugreifen darf.",
        action: "Für den priorisierten Anwendungsfall Datenquellen, Qualität und Zugriffsrechte prüfen und die größte Lücke schließen." },
      { id: "governance", no: "04", label: "Governance & Recht",
        prompt: "Es gibt verbindliche Regeln zur KI-Nutzung: freigegebene Tools, Datenschutz, Vertraulichkeit und Prüfpflichten.",
        why: "Fehlen klare Regeln, entsteht Schatten-KI mit Haftungs- und Reputationsrisiko.",
        action: "Eine einseitige KI-Nutzungsrichtlinie mit Tool-Freigabeliste, Datenklassen und Vier-Augen-Regel verabschieden." },
      { id: "skills", no: "05", label: "Kompetenzen",
        prompt: "Mitarbeitende können KI sicher anwenden und Ergebnisse fachlich prüfen. Es gibt Schulungen und Ansprechpersonen.",
        why: "Die EU-KI-Verordnung verlangt KI-Kompetenz. Ohne sie steigt das Risiko von Fehlanwendung.",
        action: "Rollenbasierte Kurzschulung an echten Arbeitssituationen aufsetzen und je Team eine:n KI-Multiplikator:in benennen." },
      { id: "leadership", no: "06", label: "Führung & Change",
        prompt: "Die Führung unterstützt KI sichtbar, bindet Mitarbeitende ein und adressiert Sorgen offen.",
        why: "Ohne sichtbare Führung verliert jede KI-Initiative nach dem Kick-off an Dynamik.",
        action: "Ein gemeinsames Führungsnarrativ formulieren: Warum KI, was ändert sich, was bleibt. Dazu ein offenes Q&A-Format." },
      { id: "adoption", no: "07", label: "Nutzung im Alltag",
        prompt: "KI wird im Arbeitsalltag tatsächlich genutzt. Nutzung und Abbruchgründe sind sichtbar.",
        why: "Bereitgestellt ist nicht genutzt. Ohne Nutzungsdaten bleibt Wirkung eine Annahme.",
        action: "Vier Wochen lang Nutzung und Abbruchgründe getrennt erfassen und in einem festen Review besprechen." },
      { id: "impact", no: "08", label: "Wirkung & Business Case",
        prompt: "Für KI-Vorhaben gibt es Baseline, Zielwert und KPIs zu Zeit, Qualität, Kosten oder Risiko.",
        why: "Ohne Baseline lässt sich weder Wirkung belegen noch die nächste Investition begründen.",
        action: "Für den Piloten Baseline, Zielwert, Datenquelle und Review-Termin festlegen, bevor er startet." }
    ];

    var SCALE = ["Gar nicht", "Ansatzweise", "Teilweise", "Weitgehend", "Voll"];
    var PEOPLE = ["skills", "leadership", "adoption"];

    var OFFERS = {
      essential: { eyebrow: "Nächster sinnvoller Schritt", name: "Essential Management-Baseline",
        reason: "Ihre Basis ist tragfähig. Eine strukturierte Management-Baseline mit 90-Tage-Pfad macht Fortschritt messbar, bevor Sie skalieren." },
      professional: { eyebrow: "Mehrperspektive empfohlen", name: "THE GAP Professional",
        reason: "Ihr Ergebnis hängt an der Frage, wie Ihr Team wirklich denkt. Professional misst Management- und Mitarbeitendensicht getrennt und anonym und macht den echten Gap sichtbar." },
      executive: { eyebrow: "Expert Validation empfohlen", name: "Executive Review",
        reason: "Das Signal ist deutlich. Bevor weiter in KI investiert wird, sollten Ausgangsbild, Prioritäten und Risiken gemeinsam validiert werden." },
      diagnostic: { eyebrow: "Ursachenklärung empfohlen", name: "Dual Perspective Diagnostic",
        reason: "Das Signal ist kritisch. Ursachen, Perspektivdifferenzen, Risiken und wirtschaftliches Exposure sollten belastbar geprüft werden, nicht geschätzt." }
    };

    var LEVELS = {
      Focused: { title: "KI-ready mit klaren Hebeln", copy: "Ihre Organisation hat eine starke Basis. Jetzt geht es darum, Wirkung zu belegen und zu skalieren." },
      Material: { title: "Auf dem Weg, mit Bremsen", copy: "Die Richtung stimmt, aber einzelne Felder bremsen spürbar, bevor KI im Alltag Wirkung entfaltet." },
      High: { title: "Das Fundament fehlt noch", copy: "KI-Ambition und organisatorische Realität liegen deutlich auseinander. Investitionen laufen Gefahr, zu verpuffen." },
      Critical: { title: "Frühe Phase mit Risiko", copy: "Bevor weitere KI-Tools ausgerollt werden, braucht es Zielbild, Regeln und Befähigung." }
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
    function teamFail(err) { console.warn("[THE GAP] Team-Modus:", err); teamError("Das Teambild ist gerade nicht erreichbar. Bitte versuchen Sie es später erneut."); }

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
        if (!r.ok && r.reason === "full") { teamError("Dieses Team ist bereits voll (10 von 10). Für größere Gruppen gibt es THE GAP Professional."); }
        else if (!r.ok) { teamError("Dieser Team-Link ist ungültig oder abgelaufen."); return; }
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
        if (!r.ok) { teamError("Dieser Team-Link ist ungültig oder abgelaufen."); teamData = null; }
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
      $("teamMailBtn").href = "mailto:?subject=" + encodeURIComponent("Unser KI-Teambild: 3 Minuten, anonym") +
        "&body=" + encodeURIComponent(teamInviteText() + "\n\n" + teamUrl(code) + "\n\nEs werden keine Namen oder E-Mail-Adressen gespeichert. Das Teambild zeigt nur Durchschnittswerte, erst ab 5 Antworten.");
      var d = teamData || { count: 1, max: CONFIG.teamMax, ready: false };
      var left = Math.max(0, CONFIG.teamMinGroup - d.count);
      $("teamTitle").textContent = d.ready ? "Ihr Teambild" : "Noch " + left + (left === 1 ? " Antwort" : " Antworten") + " bis zum Teambild";
      $("teamCopy").textContent = d.ready
        ? "Anonymer Durchschnitt aus " + d.published_n + " Antworten. Das Bild wird bei 5, 8 und 10 Antworten aktualisiert, damit sich keine einzelne Antwort zurückrechnen lässt."
        : "Teilen Sie den Link mit Ihrem Team, in Teams, Slack oder per E-Mail. Sobald 5 Personen geantwortet haben, sehen alle das anonyme Teambild.";
      var bars = "";
      for (var i = 0; i < CONFIG.teamMax; i++) bars += '<i class="' + (i < d.count ? "on" : "") + (i === CONFIG.teamMinGroup - 1 ? " min" : "") + '"></i>';
      $("teamProgress").innerHTML = bars;
      $("teamCount").textContent = d.count + " von " + d.max + " Antworten";
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
        return '<div class="t-row' + (x === top && x.spread > 0 ? " hot" : "") + '"><span class="lbl">' + x.label + '<small>Streuung ±' + x.spread + '</small></span>' +
          '<span class="t-bar"><u data-l="' + lo + '" data-w="' + (hi - lo) + '"></u><i data-w="' + x.mean + '"></i><em data-l="' + x.me + '"></em></span>' +
          '<span class="val">Team ' + x.mean + '</span></div>';
      }).join("");
      Array.prototype.forEach.call($("teamRows").querySelectorAll("[data-l],[data-w]"), function (el) {
        if (el.hasAttribute("data-l")) el.style.left = el.getAttribute("data-l") + "%";
        if (el.hasAttribute("data-w")) el.style.width = el.getAttribute("data-w") + "%";
      });
    }
    function teamInviteText() {
      return "Ich habe für unser Team einen anonymen KI-Readiness Check angelegt (3 Minuten, ohne Login). Ab 5 Antworten sehen wir gemeinsam, wo wir stehen:";
    }
    function shareTeam() {
      var url = teamUrl(teamCode());
      var text = teamInviteText();
      if (navigator.share) { navigator.share({ title: "KI-Teambild · THE GAP", text: text, url: url }).catch(function () {}); return; }
      copyTeam();
    }
    function copyTeam() {
      var url = teamUrl(teamCode());
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(function () { toast("Team-Link kopiert."); }, function () { $("teamLink").select(); });
      } else $("teamLink").select();
    }

    function inviteUrl() {
      var base = CONFIG.shareUrl || (location.origin + location.pathname);
      var code = SIGNALS.map(function (q) { return state.self[q.id] || 0; }).join("");
      return base + "?vs=" + code + "&utm_source=colleague&utm_medium=referral&utm_campaign=ki-readiness-check";
    }
    function inviteText() {
      return VS
        ? "Ich habe den KI-Readiness Check auch gemacht. Über diesen Link siehst du unseren Vergleich:"
        : "Ich habe gerade den KI-Readiness Check von THE GAP gemacht (3 Minuten). Machst du ihn auch? Danach sehen wir, wo wir unsere Organisation unterschiedlich einschätzen:";
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
      if (r.gap < 10) return "<b>Sie erwarten kaum Unterschiede zwischen Ihrer Sicht und der Ihres Teams.</b> Das ist möglich, aber selten. In echten Messungen liegen Management und Mitarbeitende häufig deutlich auseinander. Ob das bei Ihnen auch so ist, zeigt nur eine echte Befragung.";
      if (dir > 0) return "<b>Sie vermuten, dass Ihr Team die Lage im Schnitt " + dir + " Punkte schlechter bewertet als Sie.</b> Genau diese Lücke ist ein starker Frühindikator für Widerstände und ungenutzte Tools. Die eigentliche Frage ist, ob sie in Wirklichkeit größer ist.";
      if (dir < 0) return "<b>Sie vermuten, dass Ihr Team weiter ist als Sie selbst.</b> Das kann auf Schatten-KI hindeuten: Mitarbeitende nutzen KI, bevor Regeln und Ziele stehen.";
      return "<b>Ihr Gap liegt in einzelnen Feldern, nicht im Durchschnitt.</b> Dort, wo Sichten auseinanderlaufen, entstehen typischerweise Reibung und Verzögerung.";
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
      $("qAnswered").textContent = doneCount() + " von 8 beantwortet";
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
        ? (s === t ? "Kein Unterschied in diesem Signal." : 'Gap in diesem Signal: <b>' + Math.abs(s - t) * 25 + ' Punkte</b>')
        : "";
      $("backBtn").disabled = state.step === 0;
      $("nextBtn").disabled = !complete(q);
      $("nextBtn").innerHTML = (state.step === SIGNALS.length - 1 ? "Ergebnis anzeigen" : "Weiter") + ' <span aria-hidden="true">→</span>';
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
      $("hotLabel").textContent = r.hot.label + " · " + Math.abs(r.hot.diff) + " Punkte";
      $("hotText").textContent = r.hot.diff === 0 ? "In keinem Signal erwarten Sie einen Unterschied."
        : r.hot.diff > 0 ? "Hier vermuten Sie die größte Distanz zwischen Ihrer Sicht und dem Erleben Ihres Teams."
        : "Hier schätzen Sie Ihr Team deutlich weiter ein als sich selbst.";
      $("printDate").textContent = new Date().toLocaleDateString("de-DE", { day: "2-digit", month: "long", year: "numeric" });
      renderCompare(r);
      renderTeam();
      if (teamCode() && state.teamJoined && state.teamJoined[teamCode()] && !teamData) loadTeam();
      $("mailBtn").href = "mailto:?subject=" + encodeURIComponent("KI-Readiness Check: wollen wir uns vergleichen?") +
        "&body=" + encodeURIComponent(inviteText() + "\n\n" + inviteUrl());

      $("gateWrap").hidden = state.unlocked;
      $("report").hidden = !state.unlocked;
      $("printBtn").hidden = !state.unlocked;
      if (!state.unlocked) return;

      $("rows").innerHTML = r.rows.map(function (x) {
        var hot = x.id === r.hot.id && x.diff !== 0;
        return '<div class="row' + (hot ? " hot" : "") + '"><span class="row-label">' + x.label + '<small>Sie ' + x.self + ' · Team ' + x.team + '</small></span>' +
          '<span class="bars"><span class="bar self"><i data-w="' + x.self + '"></i></span><span class="bar team"><i data-w="' + x.team + '"></i></span></span>' +
          '<span class="row-gap">' + Math.abs(x.diff) + '<small>Gap</small></span></div>';
      }).join("");
      var phases = ["Tag 0–30", "Tag 31–60", "Tag 61–90"];
      $("plan").innerHTML = r.low3.map(function (x, i) {
        return '<li><b>' + phases[i] + '</b><h4>' + x.label + '</h4><p>' + x.action + '</p></li>';
      }).join("");
      $("offerEyebrow").textContent = r.offer.eyebrow;
      $("offerName").textContent = r.offer.name;
      $("offerReason").textContent = r.offer.reason;
      $("offerBtn").innerHTML = "Ergebnis besprechen " + '<span aria-hidden="true">↗</span>';
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          Array.prototype.forEach.call(document.querySelectorAll(".bar i"), function (el) { el.style.width = el.getAttribute("data-w") + "%"; });
        });
      });
    }

    function renderCompare(r) {
      $("compare").hidden = !VS;
      $("shareTitle").firstChild.nodeValue = VS ? "Vergleich zurückschicken" : "Liegen Sie richtig mit Ihrem Team?";
      $("shareText").textContent = VS
        ? "Schicken Sie den Link an die Person zurück, die Sie eingeladen hat. Dann sieht sie denselben Vergleich."
        : "Schicken Sie den Check an eine Kollegin oder einen Kollegen. Nach drei Minuten sehen beide, wo Ihre Einschätzungen auseinanderliegen. Ihr Ergebnis reist im Link mit, sonst nichts.";
      $("shareBtn").innerHTML = (VS ? "Vergleich zurückschicken" : "Kolleg:in einladen") + ' <span aria-hidden="true">→</span>';
      if (!VS) return;
      var rows = r.rows.map(function (x) { var t = VS.answers[x.id] * 25; return { label: x.label, me: x.self, them: t, d: Math.abs(x.self - t) }; });
      var them = Math.round(rows.reduce(function (a, x) { return a + x.them; }, 0) / rows.length);
      var diff = Math.round(rows.reduce(function (a, x) { return a + x.d; }, 0) / rows.length);
      var top = rows.slice().sort(function (a, b) { return b.d - a.d; })[0];
      $("compareTitle").textContent = diff < 10 ? "Sie sehen Ihre Organisation sehr ähnlich" : diff < 25 ? "Sie sehen Ihre Organisation unterschiedlich" : "Sie sehen zwei verschiedene Organisationen";
      $("cmpMe").textContent = r.score;
      $("cmpThem").textContent = them;
      $("cmpDiff").textContent = diff;
      $("compareText").textContent = top.d === 0
        ? "In keinem Signal liegen Sie auseinander. Spannend wird es, wenn Sie Mitarbeitende ohne Führungsrolle dazunehmen."
        : "Am weitesten auseinander liegen Sie bei „" + top.label + "“ (" + top.d + " Punkte). Schon zwei Personen sehen dieselbe Organisation unterschiedlich. Bei 50 oder 500 Mitarbeitenden wird dieser Unterschied zur Steuerungsfrage.";
      $("compareRows").innerHTML = rows.map(function (x) {
        return '<div class="row' + (x === top && x.d ? " hot" : "") + '"><span class="row-label">' + x.label + '<small>Sie ' + x.me + ' · Kolleg:in ' + x.them + '</small></span>' +
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
        navigator.share({ title: "KI-Readiness Check · THE GAP", text: text, url: url }).catch(function () {});
        return;
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text + " " + url).then(
          function () { toast("Einladung kopiert. Einfach in Teams, Slack oder eine Nachricht einfügen."); },
          function () { window.prompt("Link kopieren:", url); });
      } else window.prompt("Link kopieren:", url);
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
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) { leadError("Bitte eine gültige E-Mail-Adresse angeben."); $("email").focus(); return; }
      if (!$("consent").checked) { leadError("Bitte bestätigen Sie Ihr Einverständnis, damit wir die Auswertung speichern dürfen."); return; }
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
      btn.textContent = "Wird freigeschaltet …";
      function done() {
        state.unlocked = true;
        state.email = email;
        render(false);
        toast("Freigeschaltet. Ihre vollständige Auswertung steht unten.");
        $("report").scrollIntoView({ behavior: "smooth", block: "start" });
      }
      function fail(err) {
        queueLocally(payload, String(err && err.message || err));
        console.warn("[THE GAP] Lead-Insert fehlgeschlagen:", err);
        btn.disabled = false;
        btn.innerHTML = 'Erneut versuchen <span aria-hidden="true">→</span>';
        leadError("Das Speichern hat nicht funktioniert. Bitte erneut versuchen oder schreiben Sie uns direkt.");
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
