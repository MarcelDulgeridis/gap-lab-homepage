"""InnoLab: Portfolio von fünf Formaten (Innovation, Change, Personalentwicklung). Quelle aller Inhalte, Zahlen und Preise:
Portfolio-One-Pager und Preisliste (Stand September 2026), Autor: Dr. Oliver Meschkat. Marktdaten tragen die dort genannten Quellen.
Der Aufbau folgt der Kundenreise: Problem, Lösung, Formate mit Ablauf, Forschung, Zusammenarbeit, Preise, FAQ."""
from siteinfo import SITE, PARTNERS
from helpers import esc, url_of, ARROW, faq_block, cta_band, section, head, answer_box, strip_tags

SD = SITE["parent_url"]
PATH = "/innolab"
DAY, FLAT = 2500, 800


def eur(n):
    return f"{n:,.0f}".replace(",", ".") + " €"


# ------------------------------------------------------------------ Formate
FORMATS = [
    {
        "id": "sprint", "no": "01", "name": "InnoLab Sprint", "kind": "Innovationswoche",
        "days": 5, "price": 13300, "pp": "ca. 1.108 €", "people": "8–12 Teilnehmende", "dur": "5 Tage vor Ort",
        "tag1": "Ideen entstehen nicht im Meeting.", "tag2": "Sondern am Prototyp.",
        "teaser": "Fünf Tage, in denen Ihre Teams eine echte Fragestellung bis zum präsentationsfähigen Prototyp entwickeln.",
        "intro": "Design Thinking gibt den Prozess vor, LEGO® Serious Play® macht Ideen greifbar, OKR setzt das Ziel. Wissensinputs bleiben kurz, der Großteil der Zeit gehört der Anwendung. Am fünften Tag pitchen die Teams vor Ihrer Geschäftsführung.",
        "problem": "Innovation bleibt Absicht: Ideen entstehen in Meetings, aber nicht als Prototyp, Geschäftsmodell und Entscheidungsvorlage.",
        "ablauf_head": "Fünf Tage, ein Spannungsbogen nach dem Design-Thinking-Prozess",
        "ablauf": [
            ("Tag 1 · Challenge", "Kreative Zerstörung", "Fragestellung schärfen, Ziele nach OKR vereinbaren, erster Bau mit LEGO® Serious Play®."),
            ("Tag 2 · Verstehen", "Kunde und Markt", "Persona, Kaufmotive, PESTEL, Five Forces, Point of View."),
            ("Tag 3 · Ideen", "Vom Einfall zum Modell", "Brainwriting, Morphologischer Kasten, Walt-Disney-Methode, Prototyp in 3D."),
            ("Tag 4 · Umsetzen", "Geschäftsmodell", "Business Model Canvas, Nutzenpyramide, Kernbotschaften, Kanban und Scrum."),
            ("Tag 5 · Pitch", "Die Höhle der Löwen", "Fünf-Minuten-Pitch vor Entscheidern, gemeinsame Bewertung, Transferplan."),
        ],
        "nutzen": [
            ("Prototypen statt Folien.", "Nach fünf Tagen liegen ausgearbeitete Lösungsansätze für Ihre eigene Fragestellung vor, mit Geschäftsmodell und Pitch."),
            ("Future Skills im Ernstfall.", "Kreatives und analytisches Denken, Problemlösen und Zusammenarbeit werden an einer echten Aufgabe trainiert, nicht an Fallbeispielen."),
            ("Teams über Grenzen hinweg.", "Wechselnde Gruppen und Moderation auf Augenhöhe schaffen Verbindungen, die über die Woche hinaus tragen."),
        ],
        "facts": [
            ("Für wen", "Nachwuchs- und Führungskräfte, Trainees, Auszubildende, interdisziplinäre Projektteams"),
            ("Ergebnis", "Prototyp · Business Model Canvas · Pitch · Transferplan mit Verantwortlichen"),
            ("Voraussetzung", "Ein flexibel nutzbarer Raum, eine echte Fragestellung, Entscheider am Pitch-Tag"),
        ],
        "forschung": "Erprobt in 12 Seminarwochen im Education Innovation Lab. Die Mehrheit der Befragten bewertete Kreativität, Zusammenarbeit und Freude am Lernen mit gut oder sehr gut.",
        "einstieg": ("Challenge-Klärung", "60 Minuten, kostenfrei", "Wir schärfen gemeinsam die Fragestellung und klären, welche Teams die Woche tragen."),
        "faq_short": "Fünf Tage vor Ort, 8 bis 12 Teilnehmende, Prototyp und Pitch vor der Geschäftsführung am fünften Tag.",
    },
    {
        "id": "design", "no": "02", "name": "InnoLab Design", "kind": "Lernraumberatung",
        "days": 3, "price": 8300, "pp": None, "people": "Projektteam", "dur": "3 Tage vor Ort",
        "tag1": "Ein Raum ist keine Kulisse.", "tag2": "Sondern ein Lernwerkzeug.",
        "teaser": "Wir analysieren Ihre Schulungs-, Meeting- oder Projekträume und entwickeln mit den Nutzenden ein Konzept für ein Innovation Lab, priorisiert nach Wirkung und Budget.",
        "intro": "Grundlage ist ein Reifegradmodell mit fünf Stufen, von Flexibilität und Akustik über Ergonomie und Licht bis zur digitalen Konnektivität. Im Realexperiment zeigte sich: Wirksame Veränderungen müssen nicht teuer sein. Farbe, Sitzlandschaften und beschreibbare Wände kosten wenig und verändern viel.",
        "problem": "Innovationsräume entstehen vielerorts, Erfahrung mit ihrer Gestaltung ist selten, Scheitern häufig. Investitionen fallen oft ohne Begründung nach Nutzen und Kosten.",
        "ablauf_head": "Drei Tage, ein entscheidungsreifes Konzept",
        "ablauf": [
            ("Tag 1 · Ist-Analyse", "Reifegrad sichtbar machen", "Begehung, Bewertung aller Gestaltungsparameter, Kurzbefragung der Nutzenden."),
            ("Tag 2 · Co-Design", "Betroffene zu Beteiligten", "Workshop mit allen Nutzergruppen, Zielbild je Parameter, erste Entwürfe."),
            ("Tag 3 · Roadmap", "Wirkung vor Aufwand", "Kosten-Nutzen-Bewertung, Priorisierung nach Eisenhower, Quick Wins und Ausbaustufen."),
            ("Ergebnis", "Entscheidungsvorlage", "Reifegradprofil, Maßnahmenplan und Budgetrahmen, für Geschäftsführung oder Förderantrag."),
        ],
        "nutzen": [
            ("Investitionen mit Begründung.", "Jede Maßnahme ist nach Nutzen für die Lernenden und nach Kosten bewertet, nachvollziehbar für Controlling und Leitung."),
            ("Akzeptanz statt Widerstand.", "Wer mitgestaltet, nutzt den Raum. Bewährtes bleibt dort, wo es gebraucht wird, auch für erfahrene Lehrende."),
            ("Ein Raum, der mitwächst.", "Das Reifegradmodell macht Fortschritt messbar und lässt sich intern als Veränderungsgeschichte kommunizieren."),
        ],
        "facts": [
            ("Für wen", "Bildungszentren, Kammern, Akademien, HR- und L&D-Abteilungen, Unternehmen mit Projektflächen"),
            ("Ergebnis", "Reifegradprofil · Zielbild · priorisierte Roadmap · Budgetrahmen"),
            ("Optional", "Umsetzungsbegleitung und Evaluation nach dem ersten Betriebsquartal"),
        ],
        "forschung": "Im Realexperiment wurde ein über Jahrzehnte kaum veränderter Seminarraum mit überschaubarem Budget umgebaut und dauerhaft als Education Innovation Lab betrieben. Die Ergebnisse überzeugten die Leitung, weitere Räume umzurüsten.",
        "einstieg": ("Raumbegehung und Erstgespräch", "½ Tag vor Ort, 1.250 €, bei Beauftragung angerechnet", "Ein halber Tag vor Ort, um Ausgangslage, Nutzergruppen und Ziel zu klären."),
        "faq_short": "Drei Tage vor Ort mit Nutzenden, Trainern, IT und Facility Management; Ergebnis ist eine Entscheidungsvorlage mit Reifegradprofil, Maßnahmenplan und Budgetrahmen.",
    },
    {
        "id": "learning-design", "no": "03", "name": "Learning Design 4.0", "kind": "Train the Trainer",
        "days": 3, "price": 8300, "pp": "ca. 692 €", "people": "6–12 Teilnehmende", "dur": "3 Tage vor Ort",
        "tag1": "Wissen wird nicht übertragen.", "tag2": "Sondern konstruiert.",
        "teaser": "Für Ausbildende, interne Trainer und Dozierende, die ihre Lernformate vom Frontalunterricht zu aktivem, spielerischem und kompetenzorientiertem Lernen weiterentwickeln wollen.",
        "intro": "Die Teilnehmenden erleben jede Methode zuerst selbst und übertragen sie dann auf ein eigenes Seminar. Am Ende steht ein überarbeitetes Lernformat, das im nächsten Durchlauf eingesetzt werden kann.",
        "problem": "Bildungspersonal wird zur strategischen Frage, doch Seminare bestehen noch zu oft aus Stoffvermittlung. Ausgangspunkt im Realexperiment: 50 bis 70 Prozent der Unterrichtszeit waren Frontalunterricht.",
        "ablauf_head": "Sechs Module, vom Erleben zum eigenen Format (Ermöglichungsdidaktik statt Stoffvermittlung)",
        "ablauf": [
            ("Modul 1", "Constructive Alignment", "Lernziele, Methoden und Prüfung aus einem Guss gestalten."),
            ("Modul 2", "Dramaturgie", "Spannungsbogen über Tage, Inputs von höchstens 20 bis 30 Minuten."),
            ("Modul 3", "Game-Based Learning", "Zwölf Erfolgsfaktoren für Spiele mit Lernwirkung, inklusive LEGO® Serious Play®."),
            ("Modul 4", "Methodenkoffer", "Rund 40 erprobte Kreativ-, Analyse- und Reflexionsmethoden gezielt auswählen."),
            ("Modul 5", "Lernen auf Augenhöhe", "Moderation, Pausenautonomie, Fehlerkultur und emotionale Intelligenz im Seminar."),
            ("Transfer", "Erproben und evaluieren", "Eigenes Format überarbeiten, im Team testen, mit Feedback auswerten."),
        ],
        "nutzen": [
            ("Aktivierung statt Frontalunterricht.", "Lernende arbeiten selbst an Aufgaben mit Praxisbezug, das erhöht Beteiligung und Verankerung."),
            ("Sofort einsetzbar.", "Jede Person verlässt das Training mit einem überarbeiteten Format und dem passenden Methodenkoffer."),
            ("Wirkung, die sich zeigen lässt.", "Evaluationsbausteine machen Lernerfolg sichtbar, intern und gegenüber Auftraggebern."),
        ],
        "facts": [
            ("Für wen", "Ausbildende nach AEVO, interne Trainer, Dozierende an Akademien und Kammern, L&D-Teams"),
            ("Ergebnis", "Überarbeitetes Lernformat · Methodenkoffer · Evaluationsbogen · Transferplan"),
            ("Ergänzung", "Hospitation und Feedback im ersten Durchlauf des neuen Formats"),
        ],
        "forschung": "Das neu konzipierte Format setzt auf Anwendung statt Frontalunterricht und wurde von Ausbildenden anderer Fachbereiche bereits aufgegriffen.",
        "einstieg": ("Format-Check eines Seminars", "kostenfrei", "Wir sichten ein bestehendes Konzept Ihrer Wahl und zeigen drei konkrete Ansatzpunkte."),
        "faq_short": "Drei Tage vor Ort, 6 bis 12 Teilnehmende, Ergebnis ist ein überarbeitetes eigenes Lernformat mit Methodenkoffer.",
    },
    {
        "id": "change-leadership", "no": "04", "name": "Change Leadership", "kind": "Führungskräftetraining",
        "days": 3, "price": 8300, "pp": "ca. 692 €", "people": "8–14 Teilnehmende", "dur": "2 + 1 Tage vor Ort",
        "tag1": "Wandel scheitert selten am Konzept.", "tag2": "Sondern an dem, was er Menschen abverlangt.",
        "teaser": "Für Führungskräfte und Change Agents, die Innovationen nicht nur beschließen, sondern im Team zum Tragen bringen.",
        "intro": "Das Training verbindet Innovations- und Change-Management: Widerstände erkennen und einordnen, Veränderung verständlich kommunizieren, eine Fehlerkultur etablieren. Ein Transfertag nach sechs Wochen sichert die Umsetzung am eigenen Vorhaben.",
        "problem": "Veränderungsmüdigkeit ist in den Belegschaften angekommen. Ohne strategisches Commitment, Ressourcen und motivierte Change Agents entsteht keine Innovation.",
        "ablauf_head": "Fünf Bausteine: zwei Trainingstage und ein Transfertag (wollen, können, dürfen)",
        "ablauf": [
            ("Standort", "Innovationstypen", "Aktiv, passiv, reaktiv oder zufällig: Wo steht Ihre Organisation?"),
            ("Diagnose", "Widerstand verstehen", "Nicht-Wissen und Nicht-Wollen, sachliche, machtpolitische und persönliche Gründe."),
            ("Haltung", "Emotionale Intelligenz", "Gefühle erkennen, Sinn vermitteln, psychologische Sicherheit schaffen."),
            ("Kommunikation", "Change-Kommunikation", "Storytelling, Kernbotschaften, schnelle Erfolge sichtbar machen."),
            ("Nach 6 Wochen", "Transfertag", "Eigenes Vorhaben reflektieren, nachsteuern, Fehlerkultur verankern."),
        ],
        "nutzen": [
            ("Beteiligte statt Betroffene.", "Führungskräfte binden ihr Team früh ein und reduzieren Reibungsverluste in der Umsetzung."),
            ("Klarheit statt Informationsflut.", "Botschaften, die die Führungskraft selbst versteht und trägt, die Voraussetzung für Vertrauen."),
            ("Umsetzung statt Absicht.", "Jede Person arbeitet an einem realen Vorhaben und verlässt das Training mit einem konkreten nächsten Schritt."),
        ],
        "facts": [
            ("Für wen", "Führungskräfte aller Ebenen, Projektleitungen, Innovations- und Change-Verantwortliche, Multiplikatoren"),
            ("Ergebnis", "Stakeholder- und Widerstandsanalyse · Kommunikationsplan · persönlicher Change-Fahrplan"),
            ("Methoden", "Fallarbeit, LEGO® Serious Play®, Rollenspiel, kollegiale Beratung"),
        ],
        "forschung": "Die Promotion zeigt: Ohne strategisches Commitment, Ressourcen und motivierte Change Agents entsteht keine Innovation. Das Training setzt bei denen an, die Wandel im Alltag tragen.",
        "einstieg": ("Vorgespräch zu Ihrem Vorhaben", "kostenfrei", "Wir klären Ausgangslage, Zielgruppe und das Vorhaben, an dem trainiert wird."),
        "faq_short": "Zwei Trainingstage plus ein Transfertag nach sechs Wochen, 8 bis 14 Teilnehmende, Arbeit an einem eigenen Vorhaben.",
    },
    {
        "id": "scorecard", "no": "05", "name": "Innovation Scorecard", "kind": "Strategieworkshop",
        "days": 2, "price": 5800, "pp": None, "people": "4–10 Teilnehmende", "dur": "2 Tage vor Ort",
        "tag1": "Innovation braucht keinen Glauben.", "tag2": "Sondern Kennzahlen.",
        "teaser": "Für Geschäftsführung, Innovations-, HR- und Bildungsverantwortliche, die Innovation Labs, Lernformate oder Innovationsprogramme strategisch verankern und ihren Erfolg belegen wollen.",
        "intro": "Innovation Labs scheitern häufig an drei Punkten: fehlende Ausrichtung am Geschäft, fehlende Kennzahlen und unausgewogene Teams. Der Workshop adressiert alle drei und liefert ein Steuerungsset, das zu Ihrem Controlling passt.",
        "problem": "Die Budgets steigen, die Steuerung hält nicht Schritt. Erfolgreiche betriebliche Weiterbildung braucht eine klare strategische Ausrichtung, die noch nicht alle Unternehmen besitzen.",
        "ablauf_head": "Vier Arbeitsblöcke an zwei Tagen, mit Ihren Entscheidern an Ihren Zahlen",
        "ablauf": [
            ("Tag 1 · Vormittag", "Standortbestimmung", "Innovationstyp, bestehende Aktivitäten, Check an 13 empirisch abgeleiteten Erfolgsfaktoren."),
            ("Tag 1 · Nachmittag", "Strategie und Mandat", "Vision, Mission, Zielgruppen, und was mit Ergebnissen geschieht: Kerngeschäft, Inkubator oder Stopp."),
            ("Tag 2 · Vormittag", "Kennzahlen", "Prozessbegleitende Bewertung, Nutzungs-, Lern- und Marktkennzahlen, Evaluation auf Mikro- und Makroebene."),
            ("Tag 2 · Nachmittag", "Business Case", "Kosten-Nutzen-Rechnung, Reifegrad-Roadmap, Entscheidungsvorlage und Förderlogik."),
        ],
        "nutzen": [
            ("Daten statt Bauchgefühl.", "Ein schlankes Kennzahlenset zeigt, ob Lab, Programm und Lernformate wirken, und wo nachgesteuert werden muss."),
            ("Rückhalt statt Rechtfertigung.", "Eine belastbare Vorlage für Geschäftsführung, Aufsichtsgremien oder Fördergeber."),
            ("Ressourcen, die bleiben.", "Strategisches Commitment und langfristige Mittel, die Grundvoraussetzung aller weiteren Erfolgsfaktoren."),
        ],
        "facts": [
            ("Für wen", "Geschäftsführung, Innovations-, HR- und Bildungsverantwortliche, Controlling"),
            ("Ergebnis", "Innovation Scorecard · Strategie-Canvas · Reifegrad-Roadmap · Entscheidungsvorlage"),
            ("Kombinierbar", "Als Auftakt vor InnoLab Design oder zur Wirkungsmessung nach dem InnoLab Sprint"),
        ],
        "forschung": "Im Realexperiment dienten die Evaluationsergebnisse als Argumentationsbasis: Die Leitung genehmigte weitere Investitionen und die Teilnahme an einer Förderausschreibung des Bundesforschungsministeriums.",
        "einstieg": ("Erfolgsfaktoren-Check", "90 Minuten, kostenfrei", "Wir spiegeln Ihre Innovationsaktivitäten an den 13 Erfolgsfaktoren und zeigen die größte Lücke."),
        "faq_short": "Zwei Tage vor Ort mit 4 bis 10 Teilnehmenden aus Geschäftsführung, Innovation, HR, Bildung und Controlling; Ergebnis ist eine Innovation Scorecard samt Entscheidungsvorlage.",
    },
]
for f in FORMATS:
    assert f["days"] * DAY + FLAT == f["price"] or f["id"] == "change-leadership", f["id"]
    if f["id"] == "change-leadership":
        assert 3 * DAY + FLAT == f["price"]

BUNDLES = [
    ("InnoLab Journey", "Innovation Scorecard, dann InnoLab Design, dann InnoLab Sprint: von der Strategie über den Raum zur Innovationswoche.", 24700, 27400),
    ("Change & Learning", "Change Leadership und Learning Design 4.0: Führungskräfte und Lehrende gemeinsam auf den Wandel vorbereiten.", 14900, 16600),
]
assert 5800 + 8300 + 13300 == 27400 and 8300 + 8300 == 16600

FAQS = [
    ("Was ist InnoLab?",
     "<p>InnoLab ist ein Portfolio aus fünf Formaten für Innovation, Change und Personalentwicklung, die bei Ihnen vor Ort stattfinden: "
     "<a href=\"#sprint\">InnoLab Sprint</a> (Innovationswoche), <a href=\"#design\">InnoLab Design</a> (Lernraumberatung), "
     "<a href=\"#learning-design\">Learning Design 4.0</a> (Train the Trainer), <a href=\"#change-leadership\">Change Leadership</a> (Führungskräftetraining) "
     "und <a href=\"#scorecard\">Innovation Scorecard</a> (Strategieworkshop). Die Formate wurden in einem Education Innovation Lab konzipiert und evaluiert.</p>"),
    ("Was kostet InnoLab?",
     "<p>Alle Formate gibt es zum Festpreis, netto zzgl. gesetzlicher MwSt.: Innovation Scorecard 5.800 €, InnoLab Design, Learning Design 4.0 und Change Leadership je 8.300 €, InnoLab Sprint 13.300 €. "
     "Der Preis setzt sich aus 2.500 € je Tag vor Ort und 800 € Pauschale für Konzeption, Organisation und Reisezeit zusammen. Zusätzlich fallen Fahrtkosten (0,40 € je km) und Hotel nach Aufwand an. "
     "Die Bündel InnoLab Journey (24.700 €) und Change &amp; Learning (14.900 €) sparen rund 10 %. Details: <a href=\"#preise\">Preise und Pakete</a>.</p>"),
    ("Welches Format passt zu uns?",
     "<p>Der Sprint passt, wenn Teams an einer echten Fragestellung bis zum Prototyp arbeiten sollen. InnoLab Design passt, wenn Räume zum Lernwerkzeug werden sollen. "
     "Learning Design 4.0 passt für Ausbildende und Trainer, Change Leadership für Führungskräfte und Change Agents, die Scorecard für die Geschäftsführung, die Innovation mit Kennzahlen steuern will. "
     "Im kostenfreien Einstieg klären wir gemeinsam, womit Sie beginnen.</p>"),
    ("Wie läuft eine Zusammenarbeit ab?",
     "<p>Am Anfang steht ein kostenfreier Einstieg, zum Beispiel eine Challenge-Klärung in 60 Minuten oder ein Erfolgsfaktoren-Check in 90 Minuten. "
     "Danach erhalten Sie ein Festpreisangebot, abgestimmt auf Ihre Ausgangslage. Die Durchführung findet bei Ihnen vor Ort statt, am Ende stehen konkrete Ergebnisse wie Prototyp, Entscheidungsvorlage oder Transferplan.</p>"),
    ("Wo und mit wie vielen Personen findet InnoLab statt?",
     "<p>Alle Formate finden bei Ihnen vor Ort statt. Raum und Verpflegung stellen Sie. Die Gruppengrößen: InnoLab Sprint 8 bis 12, Learning Design 4.0 6 bis 12, Change Leadership 8 bis 14, Innovation Scorecard 4 bis 10 Teilnehmende; InnoLab Design arbeitet mit einem Projektteam und den Nutzergruppen des Raums.</p>"),
    ("Was brauchen wir als Voraussetzung?",
     "<p>Für den InnoLab Sprint: einen flexibel nutzbaren Raum, eine echte Fragestellung und Entscheider am Pitch-Tag. Für Change Leadership: ein reales Vorhaben, an dem trainiert wird. "
     "Für Learning Design 4.0: ein eigenes Seminar, das überarbeitet wird. Das klären wir im kostenfreien Einstieg.</p>"),
    ("Sind die Formate förderfähig?",
     "<p>Eine Förderfähigkeit über INQA-Coaching für kleine und mittlere Unternehmen ist auf Anfrage möglich. Das Programm des Bundesarbeitsministeriums unterstützt KMU ausdrücklich beim Aufbau von Lern- und Experimentierräumen. Ob Ihr Vorhaben förderfähig ist, prüfen wir gemeinsam im Vorgespräch.</p>"),
    ("Gibt es Rabatte?",
     "<p>Ja: 15 % für einen zweiten Durchlauf desselben Formats, 20 % ab dem dritten Durchlauf oder bei einem Rahmenvertrag, 15 % für Kammern, Bildungsträger und die öffentliche Hand. "
     "Learning Design 4.0 gibt es zusätzlich als offenes Seminar ab 6 Teilnehmenden für 990 € pro Person.</p>"),
    ("Wie sind Zahlung und Stornierung geregelt?",
     "<p>Die Zahlung erfolgt zu 50 % bei Beauftragung und zu 50 % nach Durchführung. Die Stornierung ist bis 8 Wochen vorher kostenfrei, bis 4 Wochen vorher fallen 50 % an, danach 90 %. "
     "Ein Ersatztermin innerhalb von 6 Monaten ist einmalig kostenfrei.</p>"),
    ("Wer führt InnoLab durch?",
     "<p>Dr. Oliver Meschkat, Partner für Innovation und Change. Er hat über die Leistungsfähigkeit deutscher Innovation Labs promoviert und ist seit 2010 als Trainer und Berater tätig. "
     "Anbieter der Formate ist die Schubart &amp; Dulgeridis GmbH, die Muttergesellschaft von THE GAP Lab.</p>"),
]


# ------------------------------------------------------------------ Bausteine
def stat(num, unit, text, source):
    return (f'<div class="il-stat"><p class="il-num">{num}<span>{unit}</span></p><p>{text}</p>'
            f'<p class="il-src">Quelle: {source}</p></div>')


def problem_rows():
    rows = [
        ("Ideen bleiben Folien.", "Innovation entsteht im Meeting, nicht am Prototyp. Es fehlen Geschäftsmodell und Entscheidungsvorlage.", "sprint"),
        ("Der Raum arbeitet gegen das Lernen.", "Innovationsräume entstehen vielerorts, Erfahrung mit ihrer Gestaltung ist selten.", "design"),
        ("Seminare vermitteln Stoff.", "Im Ausgangsfall waren 50 bis 70 Prozent der Unterrichtszeit Frontalunterricht.", "learning-design"),
        ("Wandel stockt im Team.", "85 % der Befragten berichten von akuter Veränderungsmüdigkeit. Führungskräfte sind die wichtigsten Botschafter.", "change-leadership"),
        ("Innovation lässt sich nicht belegen.", "Labs scheitern an fehlender Ausrichtung am Geschäft, fehlenden Kennzahlen und unausgewogenen Teams.", "scorecard"),
    ]
    fm = {f["id"]: f for f in FORMATS}
    lis = []
    for sym, cause, fid in rows:
        f = fm[fid]
        lis.append(
            '<li class="il-prow">'
            f'<div><span class="il-lab">Problem</span><strong>{esc(sym)}</strong></div>'
            f'<div><span class="il-lab">Ursache</span><p>{esc(cause)}</p></div>'
            f'<div><span class="il-lab">InnoLab-Antwort</span><a href="#{fid}"><strong>{esc(f["name"])}</strong>'
            f'<span>{esc(f["kind"])} · {esc(f["dur"])}</span></a></div></li>'
        )
    return '<ol class="il-problems">' + "".join(lis) + "</ol>"


def journey():
    def node(cls, label, name, meta):
        return f'<li class="il-node {cls}"><span class="il-lab">{label}</span><strong>{name}</strong><span>{meta}</span></li>'
    j = ('<div class="il-journey"><h3>InnoLab Journey <span>Strategie → Raum → Innovationswoche</span></h3><ol>'
         + node("", "Schritt 1 · 2 Tage", "Innovation Scorecard", "Ausrichten, messen, steuern")
         + node("", "Schritt 2 · 3 Tage", "InnoLab Design", "Raum analysieren und mitgestalten")
         + node("", "Schritt 3 · 5 Tage", "InnoLab Sprint", "Verstehen, bauen, pitchen")
         + f'</ol><p class="il-bundle-price"><strong>{eur(24700)}</strong> statt {eur(27400)} netto, rund 10 % Vorteil</p></div>')
    c = ('<div class="il-journey il-journey-2"><h3>Change &amp; Learning <span>Führung und Lehre gemeinsam</span></h3><ol>'
         + node("", "Format A · 2 + 1 Tage", "Change Leadership", "Führungskräfte tragen den Wandel")
         + node("", "Format B · 3 Tage", "Learning Design 4.0", "Lehrende gestalten aktives Lernen")
         + f'</ol><p class="il-bundle-price"><strong>{eur(14900)}</strong> statt {eur(16600)} netto</p></div>')
    return '<div class="il-journeys">' + j + c + "</div>"


def format_block(f):
    steps = "".join(
        f'<li><span class="il-lab">{esc(a)}</span><strong>{esc(b)}</strong><span>{esc(c)}</span></li>' for a, b, c in f["ablauf"]
    )
    nutzen = "".join(f"<li><strong>{esc(a)}</strong><span>{esc(b)}</span></li>" for a, b in f["nutzen"])
    facts = "".join(f"<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>" for a, b in f["facts"])
    en, ed, et = f["einstieg"]
    pp = f' · {esc(f["pp"])} pro Person*' if f["pp"] else ""
    return f"""<article class="il-format" id="{f['id']}" aria-labelledby="{f['id']}-h">
<header class="il-fhead">
<p class="il-kicker">Format {f['no']} von 05 · {esc(f['kind'])}</p>
<h3 id="{f['id']}-h">{esc(f['name'])}</h3>
<p class="il-claim"><span>{esc(f['tag1'])}</span> <em>{esc(f['tag2'])}</em></p>
<ul class="chips il-chips"><li>{esc(f['dur'])}</li><li>{esc(f['people'])}</li><li>Festpreis {eur(f['price'])} netto</li></ul>
</header>
<div class="il-fgrid">
<div class="il-fmain">
<p class="il-lead">{esc(f['teaser'])}</p>
<p>{esc(f['intro'])}</p>
<div class="il-ask"><span class="il-lab">Das Problem dahinter</span><p>{esc(f['problem'])}</p></div>
<h4>{esc(f['ablauf_head'])}</h4>
<ol class="il-steps">{steps}</ol>
<dl class="defs il-defs il-defs-main">{facts}</dl>
</div>
<aside class="il-fside">
<div class="il-box"><h4>Was Sie davon haben</h4><ul class="il-benefits">{nutzen}</ul></div>
<div class="il-box il-research"><span class="il-lab">Aus der Forschung in die Praxis</span><p>{esc(f['forschung'])}</p></div>
<div class="il-box il-price"><span class="il-lab">Paketpreis</span><p class="il-big">{eur(f['price'])} <small>netto{pp}</small></p>
<p class="il-in"><strong>Einstieg: {esc(en)}</strong> <span>({esc(ed)})</span><br>{esc(et)}</p>
<a class="btn btn-gold" href="/kontakt">Einstieg anfragen {ARROW}</a></div>
</aside>
</div>
</article>"""


def price_table():
    rows = []
    for f in FORMATS:
        pp = esc(f["pp"]) if f["pp"] else "–"
        rows.append(f'<tr><td>{f["no"]}</td><th scope="row"><a href="#{f["id"]}">{esc(f["name"])}</a></th><td>{esc(f["kind"])}</td>'
                    f'<td>{esc(f["dur"].replace(" vor Ort", ""))}</td><td>{esc(f["people"].replace(" Teilnehmende", ""))}</td>'
                    f'<td class="il-r"><strong>{eur(f["price"])}</strong></td><td class="il-r">{pp}</td></tr>')
    return ('<div class="table-wrap"><table class="il-table"><caption class="il-cap">Die fünf Formate, alle Preise netto zzgl. gesetzlicher MwSt.</caption><thead><tr>'
            '<th scope="col">Nr.</th><th scope="col">Produkt</th><th scope="col">Format</th><th scope="col">Dauer</th><th scope="col">Teilnehmende</th>'
            '<th scope="col" class="il-r">Paketpreis</th><th scope="col" class="il-r">Pro Person*</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>"
            '<p class="small muted">* Rechnerischer Wert bei 12 Teilnehmenden. Paketpreis inklusive Pauschale für Konzeption, Organisation und Reisezeit.</p>')


def price_chart():
    top = max(f["price"] for f in FORMATS)
    rows = []
    for f in FORMATS:
        w = round(f["price"] / top * 100, 1)
        days = "".join("<i></i>" for _ in range(f["days"]))
        rows.append(
            f'<li><a class="il-pn" href="#{f["id"]}">{esc(f["name"])}</a>'
            f'<span class="il-pd" role="img" aria-label="{f["days"]} Tage vor Ort">{days}</span>'
            f'<svg class="il-pb" viewBox="0 0 100 10" preserveAspectRatio="none" role="img" aria-label="Paketpreis {eur(f["price"])}"><rect class="tr" width="100" height="10"/><rect class="fg" width="{w}" height="10"/></svg>'
            f'<strong class="il-pv">{eur(f["price"])}</strong></li>')
    return ('<figure class="il-pchart"><figcaption><strong>Dauer und Paketpreis im Vergleich</strong>'
            '<span>Jedes Quadrat steht für einen Tag vor Ort. Die Balken beginnen bei 0 € und zeigen den Festpreis netto.</span></figcaption>'
            f'<ul>{"".join(rows)}</ul></figure>')


def bundles():
    cards = []
    for name, text, price, was in BUNDLES:
        cards.append(f'<div class="card il-bundle"><span class="tag">Bündel · rund 10 % Vorteil</span><h3>{esc(name)}</h3><p>{esc(text)}</p>'
                     f'<p class="il-big">{eur(price)} <small>statt {eur(was)} netto</small></p></div>')
    return '<div class="grid grid-2">' + "".join(cards) + "</div>"


def build_body():
    fm = {f["id"]: f for f in FORMATS}
    flow = "".join(
        f'<li><a href="#{f["id"]}"><strong>{esc(f["name"])}</strong><span>{esc(f["kind"])} · {esc(f["dur"])} · {eur(f["price"])}</span></a></li>'
        for f in FORMATS
    )
    hero = f"""<section class="hero il-hero"><div class="container hero-grid">
<div>
<nav class="breadcrumb" aria-label="Brotkrumen"><ol><li><a href="/">Start</a></li><li aria-current="page">InnoLab</li></ol></nav>
<p class="eyebrow">InnoLab · Innovation, Change, Personalentwicklung</p>
<h1>Innovation, die im Unternehmen <span class="accent">ankommt.</span> Nicht nur im Meeting.</h1>
<p class="lead">InnoLab bringt fünf erprobte Formate zu Ihnen vor Ort: von der Innovationswoche mit Prototyp und Pitch über Lernraumberatung und Train the Trainer bis zu Change Leadership und einer Innovation Scorecard. Zum Festpreis, mit konkreten Ergebnissen.</p>
<div class="hero-actions"><a class="btn btn-gold" href="/kontakt">Kostenfreien Einstieg anfragen {ARROW}</a><a class="link-arrow" href="#preise">Preise und Pakete {ARROW}</a></div>
<p class="hero-note">Fünf Formate · 2 bis 5 Tage vor Ort · Festpreis ab {eur(5800)} netto · Konzeption und Reisezeit inklusive</p>
</div>
<aside class="flow-card il-flow" aria-labelledby="il-flow-h"><h2 id="il-flow-h">Die fünf Formate im Überblick</h2><ol class="flow-list">{flow}</ol>
<div class="flow-foot"><strong>Nicht sicher, wo Sie anfangen?</strong>Im kostenfreien Einstieg klären wir Ausgangslage, Ziel und das passende Format.</div></aside>
</div></section>"""
    trust = """<section class="trust" aria-label="InnoLab in Zahlen"><div class="container"><div class="trust-grid">
<div class="trust-item"><strong>5 Formate</strong><span>Innovation, Raum, Lernen, Führung, Steuerung</span></div>
<div class="trust-item"><strong>Bei Ihnen vor Ort</strong><span>2 bis 5 Tage, Konzeption und Reisezeit im Preis</span></div>
<div class="trust-item"><strong>Festpreis ab 5.800&nbsp;€</strong><span>netto, Bündel mit rund 10 % Vorteil</span></div>
<div class="trust-item"><strong>124 Teilnehmende</strong><span>im Realexperiment über 10 Monate</span></div>
</div></div></section>"""
    answer = section(
        answer_box("Kurz erklärt",
                   "InnoLab ist das Portfolio für Unternehmen, Kammern und Bildungsträger, die Innovation nicht nur beschließen, sondern umsetzen wollen. "
                   "Sie wählen aus fünf Formaten (InnoLab Sprint, InnoLab Design, Learning Design 4.0, Change Leadership, Innovation Scorecard), "
                   "wir führen sie bei Ihnen vor Ort durch und Sie erhalten greifbare Ergebnisse: Prototyp, Entscheidungsvorlage, Lernformat, Change-Fahrplan oder Kennzahlenset.")
        + '<p class="il-note">Die Formate wurden im Rahmen einer Promotion zur Leistungsfähigkeit deutscher Innovation Labs konzipiert und in einem Education Innovation Lab evaluiert.</p>',
        "section-white il-tight", "")
    problem = section(
        head("1 · Das Problem", "Der Mittelstand innoviert wieder. Die Kompetenzlücke bleibt.",
             "Die Innovatorenquote im Mittelstand ist auf 41 % gestiegen, Produktinnovationen legen wieder zu. Zugleich nehmen Hemmnisse wie Bürokratie, Finanzierung und fehlende Kompetenzen weiter zu.", "problem-h")
        + '<div class="grid grid-4 il-stats">'
        + stat("41", " %", "Innovatorenquote im Mittelstand. Gleichzeitig wachsen Hemmnisse wie fehlende Kompetenzen.", "KfW-Innovationsbericht Mittelstand 2025")
        + stat("85", " %", "der befragten Kommunikationsverantwortlichen in der DACH-Region berichten von akuter Veränderungsmüdigkeit.", "Communications Heatmap 2025, FTI Consulting und Quadriga Hochschule Berlin")
        + stat("66", " %", "sehen Führungskräfte und interne Meinungsbildner als wichtigste Botschafter im Wandel.", "Communications Heatmap 2025")
        + stat("46,4", " Mrd. €", "investierte die Wirtschaft in Weiterbildung. Erfolgreich wird sie erst mit klarer strategischer Ausrichtung.", "IW-Weiterbildungserhebung 2023 (Bezugsjahr 2022)")
        + "</div>"
        + '<h3 class="il-h3">Fünf Bruchstellen, fünf Antworten</h3>' + problem_rows(),
        "", "problem-h")
    loesung = section(
        head("2 · Die Lösung", "Ein Portfolio, fünf Hebel: vom Mandat bis zum Prototyp.",
             "InnoLab setzt dort an, wo Innovation im Alltag scheitert. Jedes Format liefert ein konkretes Ergebnis und lässt sich allein oder in einer abgestimmten Folge buchen.", "loesung-h")
        + '<div class="grid grid-4 il-principles">'
        '<div class="card"><span class="tag">Prinzip 1</span><h3>Eine echte Aufgabe</h3><p>Gearbeitet wird an Ihrer eigenen Fragestellung, Ihrem Raum, Ihrem Seminar, nicht an Fallbeispielen.</p></div>'
        '<div class="card"><span class="tag">Prinzip 2</span><h3>Erst erleben, dann übertragen</h3><p>Wissensinputs bleiben kurz, der Großteil der Zeit gehört der Anwendung. Methoden werden zuerst selbst erlebt.</p></div>'
        '<div class="card"><span class="tag">Prinzip 3</span><h3>Ergebnis statt Teilnahme</h3><p>Prototyp, Canvas, Roadmap, Transferplan: Jedes Format endet mit Unterlagen, die weiter genutzt werden.</p></div>'
        '<div class="card"><span class="tag">Prinzip 4</span><h3>Forschungsbasiert</h3><p>Entwickelt und evaluiert in einem Education Innovation Lab, mit 124 Teilnehmenden über 10 Monate.</p></div>'
        "</div>"
        + '<h3 class="il-h3">Abgestimmte Folgen mit rund 10 % Vorteil</h3>' + journey(),
        "section-white", "loesung-h")
    formate_head = section(
        head("3 · Die Formate im Ablauf", "Jedes Format im Detail: Ablauf, Nutzen, Ergebnis, Preis.",
             "Springen Sie direkt zu Ihrem Thema oder gehen Sie die fünf Formate der Reihe nach durch."
             , "formate-h")
        + '<nav class="il-jump" aria-label="Formate"><ul class="chips">'
        + "".join(f'<li><a href="#{f["id"]}">{f["no"]} · {esc(f["name"])}</a></li>' for f in FORMATS) + "</ul></nav>",
        "il-tight", "formate-h")
    formate = "".join(
        f'<div class="il-fwrap {"il-alt" if i % 2 else ""}"><div class="container">{format_block(f)}</div></div>' for i, f in enumerate(FORMATS))
    om = PARTNERS["oliver-meschkat"]
    forschung = section(
        head("4 · Der Beleg", "Aus der Forschung in die Praxis.", "", "forschung-h")
        + '<div class="il-research-grid"><div>'
          '<p class="il-lead">Das Portfolio wurde in einem Education Innovation Lab konzipiert und evaluiert. Die Mehrheit der Befragten bewertete Kreativität, Zusammenarbeit und Freude am Lernen mit gut oder sehr gut.</p>'
          '<ul class="il-bignums"><li><strong>3</strong><span>qualitative Studien</span></li><li><strong>10</strong><span>Monate Realexperiment</span></li><li><strong>124</strong><span>Teilnehmende</span></li></ul>'
          '<p class="small">Im Realexperiment wurde ein über Jahrzehnte kaum veränderter Seminarraum mit überschaubarem Budget umgebaut. Die Ergebnisse überzeugten die Leitung, weitere Räume umzurüsten und sich um eine Förderung des Bundesforschungsministeriums zu bewerben.</p></div>'
          f'<article class="partner-wide il-person"><div class="photo"><img src="{esc(om["img"])}" alt="{esc(om["name"])}" width="448" height="448" loading="lazy" decoding="async"></div>'
          f'<div><span class="role">Partner · Innovation &amp; Change</span><h3>{esc(om["name"])}</h3>'
          "<p>Promotion zur Leistungsfähigkeit deutscher Innovation Labs. Trainer und Berater seit 2010. Konzipiert und leitet die InnoLab-Formate.</p>"
          f'<div class="hero-actions"><a class="link-arrow" href="{esc(om["sd_url"])}">Profil bei Schubart &amp; Dulgeridis</a><a class="link-arrow" href="{esc(om["linkedin"])}" rel="noopener noreferrer">LinkedIn</a></div></div></article>'
          "</div>",
        "section-cream", "forschung-h")
    ablauf = section(
        head("5 · Zusammenarbeit", "So kommen Sie von der ersten Frage zum Ergebnis.", "Klare Schritte, Festpreis, keine Überraschungen.", "ablauf-h")
        + '<ol class="steps il-coop">'
          "<li><strong>Kostenfreier Einstieg</strong><span>Challenge-Klärung (60 Min.), Format-Check, Vorgespräch oder Erfolgsfaktoren-Check (90 Min.). Bei InnoLab Design eine Raumbegehung (½ Tag, 1.250 €, bei Beauftragung angerechnet).</span></li>"
          "<li><strong>Festpreisangebot</strong><span>Nach dem Vorgespräch erhalten Sie ein Angebot, abgestimmt auf Ihre Ausgangslage, mit Leistungsumfang und Paketpreis.</span></li>"
          "<li><strong>Durchführung vor Ort</strong><span>Das Format findet bei Ihnen statt. Raum und Verpflegung stellen Sie, Konzeption, Organisation und Reisezeit sind im Preis enthalten.</span></li>"
          "<li><strong>Transfer und Wirkung</strong><span>Sie erhalten Ergebnisse und Transferplan. Optional: Wirkungsmessung nach drei Monaten sowie Hospitation oder zusätzlicher Transfertag.</span></li>"
          "</ol>",
        "section-white", "ablauf-h")
    preise = section(
        head("6 · Preise und Pakete", "Klare Pakete. Klare Preise.",
             "Alle Formate zum Festpreis, durchgeführt bei Ihnen vor Ort. Konzeption, Organisation und Reisezeit sind im Paketpreis enthalten. Alle Preise netto zzgl. gesetzlicher MwSt. Stand: September 2026.", "preise-h")
        + f'<div class="il-calc" role="group" aria-label="So entsteht der Preis"><div><span class="il-lab">Tage vor Ort, je Tag</span><strong>{eur(DAY)}</strong></div><span class="il-op" aria-hidden="true">+</span>'
          f'<div><span class="il-lab">Pauschale je Modul</span><strong>{eur(FLAT)}</strong><small>Konzeption, Organisation, Reisezeit</small></div><span class="il-op" aria-hidden="true">=</span>'
          f'<div class="il-calc-res"><span class="il-lab">Paketpreis</span><strong>ab {eur(5800)}</strong><small>zzgl. Fahrtkosten 0,40 € je km und Hotel nach Aufwand</small></div></div>'
        + price_chart() + price_table()
        + '<h3 class="il-h3">Bündel</h3>' + bundles()
        + '<div class="grid grid-3 il-extras">'
          '<div class="card"><h3>Einstieg</h3><ul class="il-list"><li>Challenge-Klärung, 60 Min. (Sprint): <strong>kostenfrei</strong></li><li>Format-Check (Learning Design 4.0): <strong>kostenfrei</strong></li><li>Vorgespräch (Change Leadership): <strong>kostenfrei</strong></li><li>Erfolgsfaktoren-Check, 90 Min. (Scorecard): <strong>kostenfrei</strong></li><li>Raumbegehung, ½ Tag (Design), bei Beauftragung angerechnet: <strong>1.250 €</strong></li></ul></div>'
          '<div class="card"><h3>Zusatzmodule</h3><ul class="il-list"><li>Wirkungsmessung nach drei Monaten: <strong>2.100 €</strong></li><li>Hospitation oder zusätzlicher Transfertag: <strong>2.500 €</strong></li><li>Co-Trainer ab 13 bzw. 15 Teilnehmenden, je Tag: <strong>1.300 €</strong></li><li>Zusätzlicher Trainer- oder Beratertag: <strong>2.500 €</strong></li></ul></div>'
          '<div class="card"><h3>Rabatte</h3><ul class="il-list"><li>Zweiter Durchlauf desselben Formats: <strong>−15 %</strong></li><li>Ab drittem Durchlauf oder Rahmenvertrag: <strong>−20 %</strong></li><li>Kammern, Bildungsträger, öffentliche Hand: <strong>−15 %</strong></li><li>Learning Design 4.0 als offenes Seminar, ab 6 Teilnehmenden: <strong>990 € p. P.</strong></li></ul></div>'
          "</div>"
        + '<div class="notice il-terms"><strong>Konditionen.</strong> Alle Preise netto zzgl. gesetzlicher MwSt. · Fahrtkosten 0,40 € je km, Hotel nach Aufwand · Raum und Verpflegung stellt der Kunde · '
          'Zahlung: 50 % bei Beauftragung, 50 % nach Durchführung · Storno: bis 8 Wochen vorher kostenfrei, bis 4 Wochen 50 %, danach 90 %; ein Ersatztermin innerhalb von 6 Monaten einmalig kostenfrei · '
          f'Förderfähigkeit über INQA-Coaching für KMU auf Anfrage. Anbieter und Vertragspartner ist die <a href="{SD}">Schubart &amp; Dulgeridis GmbH</a>, die Muttergesellschaft von THE GAP Lab.</div>',
        "section-cream", "preise-h")
    faq = section(head("7 · Häufige Fragen", "Kurz beantwortet", "", "faq-h") + faq_block(FAQS), "section-white", "faq-h")
    cta = cta_band("Machen Sie den nächsten Schritt.",
                   "Im kostenfreien Einstieg klären wir Ausgangslage, Ziel und das passende Format. Danach erhalten Sie ein Festpreisangebot.",
                   "Einstieg anfragen")
    problem = problem.replace("<section ", '<section id="problem" ', 1)
    loesung = loesung.replace("<section ", '<section id="loesung" ', 1)
    ablauf = ablauf.replace("<section ", '<section id="zusammenarbeit" ', 1)
    preise = preise.replace("<section ", '<section id="preise" ', 1)
    faq = faq.replace("<section ", '<section id="faq" ', 1)
    return '<div class="il">' + hero + trust + answer + problem + loesung + formate_head + formate + forschung + ablauf + preise + faq + cta + "</div>"


def schema_nodes():
    nodes = []
    for f in FORMATS:
        nodes.append({
            "@type": "Service", "@id": f"{url_of(PATH)}#{f['id']}", "name": f"{f['name']} ({f['kind']})",
            "description": f"{f['teaser']} {f['faq_short']}",
            "serviceType": f["kind"], "url": f"{url_of(PATH)}#{f['id']}",
            "provider": {"@id": SITE["parent_id"]},
            "offers": {"@type": "Offer", "price": str(f["price"]), "priceCurrency": "EUR",
                       "priceSpecification": {"@type": "PriceSpecification", "price": str(f["price"]), "priceCurrency": "EUR", "valueAddedTaxIncluded": False},
                       "availability": "https://schema.org/InStock"},
        })
    return nodes


def innolab():
    page = {
        "path": PATH, "short": "InnoLab",
        "title": "InnoLab: Innovationsformate für Unternehmen | THE GAP Lab",
        "og_title": "InnoLab: Innovation, die im Unternehmen ankommt",
        "description": "InnoLab: fünf Formate vor Ort für Innovation, Change und Personalentwicklung, vom Sprint mit Prototyp bis zur Innovation Scorecard. Festpreis ab 5.800 € netto.",
        "priority": "0.9", "llms_group": "Leistungen", "faqs": FAQS, "show_stand": False, "journey": "/innolab", "speakable": True, "modified": "2026-11-04",
        "og_image": "/assets/img/og-innolab.jpg", "og_image_height": 630,
        "og_alt": "InnoLab: Innovation, die im Unternehmen ankommt. Fünf Formate vor Ort, Festpreis ab 5.800 Euro netto.",
        "styles": ["/assets/innolab.css"], "schema_nodes": schema_nodes(),
    }
    page["body"] = build_body()
    return page


def build():
    return [innolab()]
