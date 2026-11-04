"""FAQ, Impressum, Datenschutz, 404. Rechtstexte: sachlich, nur tatsächlich eingesetzte Technik.
Vor Veröffentlichung/Änderung juristisch prüfen lassen (siehe README)."""
from siteinfo import SITE
from helpers import esc, ARROW, faq_block, cta_band, page_hero, section, head, answer_box
from pages_core import FAQ_COMPANY, FAQ_COOPERATION, FAQ_CONTACT, FAQ_ALL, MAIL, TEL

SD = SITE["parent_url"]


def faq():
    page = {
        "path": "/faq", "short": "FAQ",
        "title": "FAQ — Häufige Fragen zu THE GAP Lab",
        "description": "Antworten auf häufige Fragen: Was macht THE GAP Lab, wer steht dahinter, wie läuft eine Zusammenarbeit ab und wie komme ich zum Erstgespräch?",
        "priority": "0.7", "llms_group": "Unternehmen", "faqs": FAQ_ALL,
    }
    page["body"] = (
        page_hero(page, "Häufige Fragen zu THE GAP Lab",
                  "Kurze Antworten zu Unternehmen, Zusammenarbeit und Kontakt. Wenn Ihre Frage fehlt, schreiben Sie uns.")
        + section(head("Unternehmen", "Über die Gesellschaft", "") + faq_block(FAQ_COMPANY), "", "")
        + section(head("Zusammenarbeit", "Ablauf und Kosten", "") + faq_block(FAQ_COOPERATION), "section-white", "")
        + section(head("Kontakt", "Erreichbarkeit und Termine", "") + faq_block(FAQ_CONTACT), "", "")
        + cta_band("Weitere Fragen klären wir im Erstgespräch.", "Im Erstgespräch beantworten wir sie direkt, kostenlos und unverbindlich.")
    )
    return page


def impressum():
    page = {
        "path": "/impressum", "short": "Impressum",
        "title": "Impressum — THE GAP Lab (The Gap Lab GmbH)",
        "description": "Impressum der The Gap Lab GmbH, Altdorf bei Nürnberg: Anschrift, Geschäftsführer, Handelsregister HRB 46649 (Amtsgericht Nürnberg) und Kontakt.",
        "priority": "0.3", "changefreq": "yearly", "show_stand": False, "llms_group": "Rechtliches",
    }
    page["body"] = (
        page_hero(page, "Impressum")
        + section(f"""<div class="prose">
<h2>Angaben gemäß § 5 DDG</h2>
<p><strong>{SITE['legal_name']}</strong> (Marke: THE GAP Lab)<br>{SITE['street']}<br>{SITE['zip']} {SITE['city']}<br>Deutschland</p>

<h2>Vertretung</h2>
<p>Vertreten durch den Geschäftsführer: Prof. Dr. Constantin Schubart (einzelvertretungsberechtigt).</p>

<h2>Kontakt</h2>
<p>E-Mail: {MAIL}<br>Telefon: {TEL}</p>
<p class="muted">Während der Aufbauphase werden E-Mail und Telefon gemeinsam mit der Muttergesellschaft genutzt.</p>

<h2>Registereintrag</h2>
<p>Eintragung im Handelsregister B des {SITE['court_gen']}<br>Registernummer: {SITE['hrb']}<br>Tag der Eintragung: {SITE['registered']}</p>

<h2>Umsatzsteuer-Identifikationsnummer</h2>
<p>Die Angabe folgt, sobald die Umsatzsteuer-Identifikationsnummer gemäß § 27a Umsatzsteuergesetz erteilt ist.</p>

<h2>Verbund</h2>
<p>The Gap Lab GmbH ist eine Tochtergesellschaft der <a href="{SD}impressum">Schubart &amp; Dulgeridis GmbH</a>, {SITE['street']}, {SITE['zip']} {SITE['city']} ({'HRB 46037'}, {SITE['court']}).</p>
</div>""", "", ""))
    return page


def datenschutz():
    page = {
        "path": "/datenschutz", "short": "Datenschutz",
        "title": "Datenschutzerklärung — THE GAP Lab",
        "description": "Datenschutzerklärung der The Gap Lab GmbH: keine Cookies, keine Tracking-Dienste, Hosting-Logfiles, Kontaktaufnahme, KI-Readiness Check, Ihre Rechte nach DSGVO.",
        "priority": "0.3", "changefreq": "yearly", "show_stand": False, "llms_group": "Rechtliches",
    }
    page["body"] = (
        page_hero(page, "Datenschutzerklärung", f"Stand: {SITE['modified_de']}")
        + section(f"""<div class="prose">
<h2>1. Verantwortlicher</h2>
<p>{SITE['legal_name']}, {SITE['street']}, {SITE['zip']} {SITE['city']}, vertreten durch den Geschäftsführer Prof. Dr. Constantin Schubart.<br>E-Mail: {MAIL}<br>Telefon: {TEL}</p>

<h2>2. Überblick</h2>
<p>Diese Website setzt keine Cookies und keine Analyse-, Tracking- oder Marketing-Dienste ein. Schriftarten und Bilder werden von gap-lab.de selbst ausgeliefert. Eine Ausnahme ist der <a href="#ki-readiness-check">KI-Readiness Check</a>: Er speichert Ihren Zwischenstand lokal im Browser und verbindet sich nur dann mit einem Datenbank-Dienst, wenn Sie eine Auswertung freischalten oder ein Teambild nutzen (Abschnitt 6).</p>

<h2>3. Hosting und Server-Logfiles</h2>
<p>Die Website wird bei Vercel Inc. (USA) gehostet. Beim Aufruf verarbeitet der Hosting-Anbieter technisch notwendige Zugriffsdaten: IP-Adresse, Datum und Uhrzeit, aufgerufene Seite, Referrer, Browsertyp und Statuscode. Zweck ist die Auslieferung, Stabilität und Sicherheit der Website. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an einem sicheren, funktionsfähigen Webauftritt). Die Daten werden nur so lange gespeichert, wie es für diesen Zweck erforderlich ist. Für die Datenübermittlung in die USA nutzen wir die vom Anbieter bereitgestellten Garantien nach Art. 44 ff. DSGVO.</p>

<h2>4. Kontaktaufnahme</h2>
<p>Wenn Sie uns per E-Mail oder Telefon kontaktieren, verarbeiten wir Ihre Angaben, um Ihre Anfrage zu bearbeiten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO (vorvertragliche Maßnahmen) bzw. lit. f DSGVO (Bearbeitung von Anfragen). Wir löschen die Daten, sobald die Anfrage erledigt ist und keine gesetzlichen Aufbewahrungspflichten entgegenstehen. Ein Klick auf einen E-Mail-Link öffnet lediglich Ihr lokales E-Mail-Programm; dabei werden keine Daten an uns übertragen.</p>

<h2>5. Terminbuchung</h2>
<p>Die Buchung eines Erstgesprächs erfolgt auf der Website unserer Muttergesellschaft, der <a href="{SD}">Schubart &amp; Dulgeridis GmbH</a>. Beim Klick auf „Termin wählen“ verlassen Sie gap-lab.de. Für die dortige Verarbeitung gilt deren <a href="{SD}datenschutz">Datenschutzerklärung</a>.</p>

<h2 id="ki-readiness-check">6. KI-Readiness Check</h2>
<p>Auf der Seite <a href="/ki-readiness">KI-Readiness Check</a> beantworten Sie acht Aussagen. Das Ergebnis berechnet Ihr Browser selbst; die Antworten verlassen dabei Ihr Gerät nicht.</p>
<p><strong>Lokale Speicherung.</strong> Damit Sie unterbrechen und fortsetzen können, speichert der Check Ihren Zwischenstand im lokalen Speicher (localStorage) und im Sitzungsspeicher (sessionStorage) Ihres Browsers, etwa Antworten, Ergebnis und gegebenenfalls Kampagnenparameter aus dem aufgerufenen Link. Diese Daten werden nicht an uns übertragen. Sie können sie jederzeit über die Einstellungen Ihres Browsers löschen.</p>
<p><strong>Freischaltung der Auswertung.</strong> Wenn Sie die vollständige Auswertung freischalten, übermitteln wir Ihre E-Mail-Adresse, Ihre Organisation, gegebenenfalls Ihre Rolle, Ihre Antwortwerte und das Ergebnis an einen Datenbank-Dienst (Supabase). Zweck ist, Ihnen eine Einordnung Ihres Ergebnisses anzubieten. Rechtsgrundlage ist Ihre Einwilligung nach Art. 6 Abs. 1 lit. a DSGVO, die Sie im Formular per Häkchen erteilen und jederzeit mit Wirkung für die Zukunft widerrufen können. Die Daten werden gemeinsam mit der Schubart &amp; Dulgeridis GmbH ({SD}) verarbeitet. Einen Newsletter versenden wir nicht.</p>
<p><strong>Teambild.</strong> Wenn Sie ein Teambild erstellen, werden nur die acht Antwortwerte ohne Name und ohne E-Mail-Adresse gespeichert. Sichtbar wird nur der Durchschnitt ab fünf Antworten. Die Daten werden nach 90 Tagen automatisch gelöscht.</p>
<p><strong>Einladung zum Vergleich.</strong> Der Einladungslink enthält Ihre acht Antwortwerte, aber keinen Namen und keine E-Mail-Adresse. Wen Sie einladen, entscheiden Sie selbst.</p>
<p>Beim Verbindungsaufbau zum Datenbank-Dienst werden technisch notwendige Verbindungsdaten (zum Beispiel die IP-Adresse) an dessen Server übertragen.</p>

<h2>7. Externe Links</h2>
<p>Diese Website verlinkt auf externe Seiten, zum Beispiel LinkedIn-Profile der Partner oder die Website der Muttergesellschaft. Es werden keine Plugins oder Einbettungen von Drittanbietern genutzt; Daten werden erst übertragen, wenn Sie einen Link anklicken. Für die verlinkten Seiten sind deren Betreiber verantwortlich.</p>

<h2>8. Ihre Rechte</h2>
<p>Sie haben das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) und Widerspruch gegen Verarbeitungen auf Grundlage berechtigter Interessen (Art. 21). Eine erteilte Einwilligung können Sie jederzeit mit Wirkung für die Zukunft widerrufen. Zur Ausübung Ihrer Rechte wenden Sie sich an die oben genannte Kontaktadresse.</p>
<p>Sie haben außerdem das Recht, sich bei einer Datenschutz-Aufsichtsbehörde zu beschweren. Zuständig für uns ist das Bayerische Landesamt für Datenschutzaufsicht (BayLDA), Promenade 18, 91522 Ansbach.</p>

<h2>9. Änderungen</h2>
<p>Wir passen diese Erklärung an, wenn sich Technik oder Rechtslage ändern. Es gilt die jeweils hier veröffentlichte Fassung.</p>
</div>""", "", ""))
    return page


def notfound():
    page = {
        "path": "/404", "short": "Seite nicht gefunden",
        "title": "Seite nicht gefunden — THE GAP Lab",
        "description": "Diese Seite existiert nicht oder wurde verschoben. Hier geht es zur Startseite, zu den Leistungen und zum Erstgespräch bei THE GAP Lab.",
        "robots": "noindex,follow", "sitemap": False, "show_stand": False,
    }
    page["body"] = (
        '<section class="center-page"><div class="container">'
        '<p class="eyebrow">Fehler 404</p><h1>Diese Seite gibt es nicht.</h1>'
        '<p class="lead">Der Link ist veraltet oder die Adresse wurde falsch eingegeben.</p>'
        f'<p><a class="btn" href="/">Zur Startseite {ARROW}</a></p>'
        "</div></section>"
    )
    return page


def build():
    return [faq(), impressum(), datenschutz(), notfound()]
