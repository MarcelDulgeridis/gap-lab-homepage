"""FAQ-Seite mit Suche und Kategorienfilter (Progressive Enhancement: ohne JavaScript stehen alle Fragen sichtbar untereinander).
Alle Antworten stammen aus den Seiten der Website. Preise stehen nur auf der InnoLab-Seite."""
import json
import re
import unicodedata

from siteinfo import SITE
from helpers import esc, cta_band, page_hero, section, head
import pages_core as C

SD = SITE["parent_url"]
MAIL, TEL = C.MAIL, C.TEL


def _slug(s):
    s = unicodedata.normalize("NFKD", s.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss"))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60]


A = lambda path, text: f'<a href="{path}">{text}</a>'

CATS = [
    ("unternehmen", "Unternehmen", [
        ("Was macht die The Gap Lab GmbH?", "<p>Sie konzipiert, entwickelt, führt durch und vermarktet Maßnahmen der Personalentwicklung. Schwerpunkte sind " + A("/fokusfelder/verhandlungsfuehrung", "Verhandlungsführung &amp; Rhetorik") + ", " + A("/fokusfelder/leadership-organisation", "Leadership &amp; Organisation") + " sowie " + A("/fokusfelder/finance-transformation", "Finance &amp; Transformation") + ". Das Ziel: Strategie kommt im Arbeitsalltag an.</p>"),
        ("Wer steht hinter THE GAP Lab?", "<p>Geschäftsführer ist Prof. Dr. Constantin Schubart, Partner sind Dr. Oliver Meschkat und Prof. Dr. Marcel Dulgeridis. Zwei von ihnen sind Professoren für Betriebswirtschaftslehre an der IU Internationalen Hochschule, einer ist promoviert und auf Verhandlungsführung spezialisiert. Profile: " + A("/ueber-uns", "Über uns") + ".</p>"),
        ("Wie unterscheiden sich THE GAP Lab und die Schubart &amp; Dulgeridis GmbH?", f"<p>Die Schubart &amp; Dulgeridis GmbH bietet forschungsbasierte Beratung und Diagnostik (THE GAP, Pulse-Check, Upskilling, Coaching, Recruiting). THE GAP Lab entwickelt und führt Maßnahmen der Personalentwicklung durch. Beide stehen im Verbund, THE GAP Lab ist die Tochtergesellschaft: <a href=\"{SD}\">schubart-dulgeridis.de</a>.</p>"),
        ("Für wen ist das Angebot gedacht?", "<p>Für Geschäftsleitungen, Personalverantwortliche und Führungskräfte, die Entwicklung gezielt planen, durchführen oder einkaufen. Auch Kammern, Bildungsträger und Akademien nutzen die " + A("/innolab", "InnoLab-Formate") + ".</p>"),
        ("Wo sitzt THE GAP Lab?", f"<p>In {SITE['city']} ({SITE['street']}, {SITE['zip']}). Die vollständigen Firmenangaben stehen im " + A("/impressum", "Impressum") + ".</p>"),
        ("Was ist mit „Gap“ gemeint?", "<p>Der Abstand zwischen dem, was beschlossen wird, und dem, was im Arbeitsalltag ankommt. An dieser Stelle gehen Strategie, Führung und Wirkung verloren. Die Maßnahmen von THE GAP Lab setzen dort an.</p>"),
    ]),
    ("leistungen", "Leistungen", [
        ("Was bietet The Gap Lab an?", "<p>Maßnahmen der Personalentwicklung in vier Stufen: " + A("/leistungen#konzeption", "Konzeption") + ", " + A("/leistungen#entwicklung", "Entwicklung") + ", " + A("/leistungen#durchfuehrung", "Durchführung") + " und " + A("/leistungen#vermarktung", "Vermarktung") + ". Inhaltlich arbeiten die Partner in drei Fokusfeldern.</p>"),
        ("Muss ich alle vier Stufen beauftragen?", "<p>Nein. Eine Stufe, mehrere Stufen oder die ganze Kette: Das klären wir im kostenlosen Erstgespräch anhand Ihrer Ausgangslage.</p>"),
        ("Welche Ergebnisse erhalte ich?", "<p>Je nach Stufe ein Konzept mit Zielen und Erfolgskriterien, Materialien und Übungen, eine durchgeführte Maßnahme mit Auswertung oder eine verständliche Angebotsbeschreibung. Den genauen Umfang halten wir im Angebot fest. Übersicht: " + A("/leistungen", "Leistungen") + ".</p>"),
        ("Bieten Sie auch Diagnostik an?", f"<p>Diagnostik wie THE GAP und der Pulse-Check gehört zur Schubart &amp; Dulgeridis GmbH: <a href=\"{SD}the-gap\">schubart-dulgeridis.de/the-gap</a>. THE GAP Lab konzentriert sich auf Maßnahmen der Personalentwicklung.</p>"),
        ("Was bedeuten die Leitfragen der vier Stufen?", "<p>Konzeption: Was soll die Maßnahme bewirken, und für wen? Entwicklung: Wie wird aus dem Konzept Praxis für die Teilnehmenden? Durchführung: In welchem Format wirkt die Maßnahme am besten? Vermarktung: Wie werden Nutzen und Zielgruppe verständlich?</p>"),
    ]),
    ("fokusfelder", "Fokusfelder", [
        ("Was ist Verhandlungsführung?", "<p>Die zielgerichtete Vorbereitung, Steuerung und Auswertung von Verhandlungen. Ziel sind Ergebnisse, die die eigenen Interessen wahren und für die Gegenseite tragfähig genug sind, um umgesetzt zu werden. " + A("/fokusfelder/verhandlungsfuehrung", "Mehr zum Fokusfeld") + ".</p>"),
        ("Was bedeuten BATNA und ZOPA?", "<p>BATNA ist die beste Alternative ohne Einigung (Best Alternative to a Negotiated Agreement), ZOPA der Bereich, in dem beide Seiten zustimmen könnten (Zone of Possible Agreement). Beide Begriffe erklärt das " + A("/glossar", "Glossar") + ".</p>"),
        ("Worin unterscheiden sich Verhandlungsführung und Rhetorik?", "<p>Verhandlungsführung betrifft Strategie und Vorbereitung: Ziele, Alternativen, Spielräume und Gesprächsverlauf. Rhetorik betrifft die Wirkung: Aufbau von Argumenten, Wortwahl und Auftreten. Beides ergänzt sich.</p>"),
        ("Was bedeutet Leadership &amp; Organisation?", "<p>Führung wird nicht als Eigenschaft einzelner Personen verstanden, sondern als Zusammenspiel aus Strategie, Kultur, Rollen und Entscheidungswegen. Ziel sind klare Erwartungen und Entscheidungen, die im Alltag ankommen. " + A("/fokusfelder/leadership-organisation", "Mehr zum Fokusfeld") + ".</p>"),
        ("Brauche ich vorab eine Diagnostik?", f"<p>Nicht zwingend. Wer den Abstand zwischen Führungsanspruch und Arbeitsalltag zuerst messen möchte, findet <a href=\"{SD}the-gap\">THE GAP</a> bei der Schubart &amp; Dulgeridis GmbH. Maßnahmen lassen sich aber auch ohne vorherige Diagnostik konzipieren.</p>"),
        ("Was umfasst Finance &amp; Transformation?", "<p>Finanzverständnis (Rechnungswesen, Kennzahlen, Wirtschaftlichkeit) verbunden mit der Umsetzung von Veränderung, damit Entscheidungen strategisch plausibel und wirtschaftlich belastbar sind. " + A("/fokusfelder/finance-transformation", "Mehr zum Fokusfeld") + ".</p>"),
        ("Brauchen Führungskräfte betriebswirtschaftliche Vorkenntnisse?", "<p>Nein. Maßnahmen lassen sich an das Vorwissen der Zielgruppe anpassen. Ziel ist Verständnis, nicht Buchführung.</p>"),
        ("Worin unterscheiden sich Gewinn und Cashflow?", "<p>Der Gewinn ist das Ergebnis der Erfolgsrechnung eines Zeitraums, der Cashflow der Saldo tatsächlicher Zahlungen. Beide können stark voneinander abweichen, etwa wenn Rechnungen erst später bezahlt werden.</p>"),
    ]),
    ("innolab", "InnoLab", [
        ("Was ist InnoLab?", "<p>Ein Baukasten aus fünf Workshop-Formaten für Innovation, Change und Lernen, die bei Ihnen vor Ort stattfinden. Jedes Format löst eine typische Aufgabe und endet mit einem Ergebnis, das Sie weiterverwenden. " + A("/innolab", "Zur InnoLab-Seite") + ".</p>"),
        ("Welche fünf Formate gibt es?", "<p>" + A("/innolab#sprint", "InnoLab Sprint") + " (Innovationswoche, 5 Tage), " + A("/innolab#design", "InnoLab Design") + " (Lernraumberatung, 3 Tage), " + A("/innolab#learning-design", "Learning Design 4.0") + " (Train the Trainer, 3 Tage), " + A("/innolab#change-leadership", "Change Leadership") + " (Führungskräftetraining, 2 + 1 Tage) und " + A("/innolab#scorecard", "Innovation Scorecard") + " (Strategieworkshop, 2 Tage).</p>"),
        ("Welches InnoLab-Format passt zu uns?", "<p>Der Sprint passt für Prototypen an einer echten Fragestellung, Design für Lernräume, Learning Design 4.0 für Ausbildende und Trainer, Change Leadership für Führungskräfte und Change Agents, die Scorecard für die Steuerung von Innovation mit Kennzahlen. Im kostenfreien Einstieg klären wir das gemeinsam.</p>"),
        ("Wo und wie lange findet InnoLab statt?", "<p>Alle Formate finden bei Ihnen vor Ort statt und dauern zwischen zwei und fünf Tagen. Raum und Verpflegung stellen Sie, Konzeption, Organisation und Reisezeit sind im Paketpreis enthalten.</p>"),
        ("Was brauchen wir als Voraussetzung?", "<p>Je nach Format: einen flexibel nutzbaren Raum, eine echte Fragestellung und Entscheider am Pitch-Tag (Sprint), ein reales Vorhaben (Change Leadership) oder ein eigenes Seminar, das überarbeitet wird (Learning Design 4.0). Das klären wir im Einstieg.</p>"),
        ("Wie sind Preise, Zahlung und Storno geregelt?", "<p>Alle Preise und Konditionen stehen auf der InnoLab-Seite im Abschnitt " + A("/innolab#preise", "Preise") + ".</p>"),
        ("Sind die InnoLab-Formate förderfähig?", "<p>Eine Förderfähigkeit über INQA-Coaching für kleine und mittlere Unternehmen ist auf Anfrage möglich. Ob Ihr Vorhaben förderfähig ist, prüfen wir im Vorgespräch.</p>"),
        ("Wer führt InnoLab durch?", f"<p>Dr. Oliver Meschkat, Partner für Innovation und Change. Er hat über die Leistungsfähigkeit deutscher Innovation Labs promoviert und ist seit 2010 als Trainer und Berater tätig. Anbieter der Formate ist die <a href=\"{SD}\">Schubart &amp; Dulgeridis GmbH</a>, die Muttergesellschaft von THE GAP Lab.</p>"),
    ]),
    ("ki", "KI-Readiness Check", [
        ("Was ist der KI-Readiness Check?", "<p>Ein kostenloser Check, der in drei Minuten acht Signale zur KI-Reife Ihrer Organisation abfragt, die Sicht von Management und Mitarbeitenden vergleicht und den KI-Gap sowie das wichtigste Handlungsfeld zeigt. " + A("/ki-readiness", "Zum Check") + ".</p>"),
        ("Wie lange dauert der Check, und was kostet er?", "<p>Er dauert etwa drei Minuten, ist kostenlos und braucht kein Login. Das Ergebnis erscheint sofort.</p>"),
        ("Was passiert mit meinen Antworten im Check?", "<p>Ihre Antworten bleiben in Ihrem Browser. Nur wenn Sie die vollständige Auswertung freischalten, speichern wir E-Mail-Adresse, Organisation und Ergebnis, um Ihnen eine Einordnung anzubieten. Details: " + A("/datenschutz#ki-readiness-check", "Datenschutzerklärung") + ".</p>"),
        ("Wie belastbar ist das Ergebnis?", "<p>Es ist eine ehrliche Selbsteinschätzung aus einer Perspektive und damit ein Orientierungssignal, keine Zertifizierung. Wie groß der Gap wirklich ist, zeigt erst die echte Befragung von Führung und Mitarbeitenden.</p>"),
    ]),
    ("zusammenarbeit", "Zusammenarbeit", [
        ("Wie kommt eine Zusammenarbeit zustande?", "<p>Am Anfang steht ein kostenloses Erstgespräch (20 bis 30 Minuten, Microsoft Teams) zu Anlass, Ziel und Zielgruppe. Danach erhalten Sie ein Angebot mit klarem Leistungsumfang. Termin: " + A("/kontakt", "Kontakt") + ".</p>"),
        ("Was kostet eine Zusammenarbeit?", "<p>Nach dem Erstgespräch erhalten Sie ein individuelles Angebot nach Umfang. Die Preise der " + A("/innolab#preise", "InnoLab-Formate") + " stehen auf der InnoLab-Seite.</p>"),
        ("Wie läuft eine Maßnahme ab?", "<p>In vier Schritten: Erstgespräch (Anlass, Ziel, Zielgruppe), Konzept (Ziele, Inhalte, Format, Erfolgskriterien), Umsetzung (Entwicklung und Durchführung) und Auswertung (Wirkung prüfen, nächste Schritte klären).</p>"),
    ]),
    ("kontakt", "Kontakt und Datenschutz", [
        ("Wie erreiche ich THE GAP Lab?", f"<p>Per E-Mail an {MAIL} oder telefonisch unter {TEL}. E-Mail und Telefon werden in der Aufbauphase gemeinsam mit der Muttergesellschaft genutzt.</p>"),
        ("Mit wem kann ich ein Erstgespräch führen?", "<p>Mit Constantin Schubart, Oliver Meschkat oder Marcel Dulgeridis. Gebucht wird über deren Kalender bei der Schubart &amp; Dulgeridis GmbH, freie Zeiten sind live sichtbar. Nach der Buchung erhalten Sie eine Outlook-Einladung mit Microsoft-Teams-Link.</p>"),
        ("Was passiert mit meinen Daten bei der Terminbuchung?", f"<p>Mit dem Klick auf „Termin wählen“ wechseln Sie zur Website der Muttergesellschaft. Dort gilt deren <a href=\"{SD}datenschutz\">Datenschutzerklärung</a>.</p>"),
        ("Setzt die Website Cookies oder Tracking ein?", "<p>Nein. Die Website setzt keine Cookies und keine Analyse- oder Marketing-Dienste ein. Eine Ausnahme ist der KI-Readiness Check, der den Zwischenstand lokal in Ihrem Browser speichert. Alles dazu in der " + A("/datenschutz", "Datenschutzerklärung") + ".</p>"),
    ]),
]

ALL = [(c, q, a) for c, _t, items in CATS for q, a in items]
FAQ_ALL_PAGE = [(q, a) for _c, q, a in ALL]


def build_body(page):
    total = len(ALL)
    chips = '<li><button type="button" data-cat="all" aria-pressed="true">Alle <small>' + str(total) + "</small></button></li>" + "".join(
        f'<li><button type="button" data-cat="{c}" aria-pressed="false">{esc(t)} <small>{len(items)}</small></button></li>' for c, t, items in CATS)
    groups = ""
    for c, t, items in CATS:
        det = "".join(
            f'<details id="f-{_slug(q)}" data-cat="{c}"><summary>{q}</summary><div class="answer-body">{a}</div></details>' for q, a in items)
        groups += f'<section class="faq-group" data-cat="{c}" aria-labelledby="g-{c}"><h2 id="g-{c}">{esc(t)}</h2><div class="faq">{det}</div></section>'
    tool = (
        '<div class="faq-tool" data-faq>'
        '<div class="faq-controls">'
        '<label class="sr-only" for="faq-q">Fragen durchsuchen</label>'
        '<input id="faq-q" class="faq-search" type="search" placeholder="Frage oder Stichwort suchen, zum Beispiel BATNA, Preise, Datenschutz" autocomplete="off" enterkeyhint="search">'
        f'<ul class="faq-cats" aria-label="Nach Thema filtern">{chips}</ul>'
        f'<div class="faq-meta"><span class="faq-count" data-count aria-live="polite">{total} Fragen</span>'
        '<button type="button" class="faq-link" data-toggle hidden>Alle öffnen</button>'
        '<button type="button" class="faq-link" data-reset hidden>Zurücksetzen</button></div>'
        "</div>"
        '<p class="faq-empty" data-empty hidden>Keine Treffer. Schreiben Sie uns an ' + MAIL + " oder buchen Sie ein " + A("/kontakt", "Erstgespräch") + ".</p>"
        f'<div class="faq-groups">{groups}</div></div>')
    return (
        page_hero(page, "Häufige Fragen zu THE GAP Lab", f"{total} Antworten zu Unternehmen, Angebot, Fokusfeldern, InnoLab und Kontakt.")
        + section(tool, "", "")
        + cta_band("Weitere Fragen klären wir im Erstgespräch.", "Kostenlos, 20 bis 30 Minuten.")
    )


def faq():
    page = {
        "path": "/faq", "short": "FAQ",
        "title": "FAQ — Häufige Fragen zu THE GAP Lab",
        "description": f"{len(ALL)} Antworten zu THE GAP Lab: Angebot, Fokusfelder, InnoLab, KI-Readiness Check, Zusammenarbeit und Datenschutz. Mit Suche und Themenfilter.",
        "priority": "0.8", "llms_group": "Unternehmen", "faqs": FAQ_ALL_PAGE,
        "speakable": True, "speakable_selector": [".page-hero .lead"],
        "styles": ["/assets/faq.css"], "scripts": ["/assets/faq.js"],
    }
    page["body"] = build_body(page)
    return page
