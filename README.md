# THE GAP Lab — gap-lab.de

Statische Unternehmenswebsite der **The Gap Lab GmbH** (Marke: THE GAP Lab), Altdorf bei Nürnberg, HRB 46649, Amtsgericht Nürnberg.
Kein Framework, kein Build-Schritt auf dem Server: Die Seiten werden lokal mit einem kleinen Python-Generator erzeugt und als fertige HTML-Dateien ausgeliefert (Vercel, Auto-Deploy bei Push auf `main`).

**Warum statisch?** Kürzeste Ladezeit (kein JS-Framework), strikte Content-Security-Policy ohne Inline-Code, keine Abhängigkeiten, einfache Pflege.

## Struktur

```
tools/siteinfo.py      Stammdaten (Firma, Register, Kontakt, Partner) — einzige Quelle für Firmenangaben
tools/pages_core.py    Start, Leistungen, Fokusfelder-Übersicht, Über uns, Kontakt + FAQ-Daten
tools/pages_fokus.py   Die drei Fokusfeld-Seiten
tools/pages_legal.py   FAQ, Impressum, Datenschutz, 404
tools/helpers.py       HTML-Bausteine (Hero, Karten, FAQ, CTA …)
tools/build.py         Generator: Seiten, Schema.org (JSON-LD), sitemap.xml, robots.txt, llms.txt, Cache-Busting
tools/audit.py         QA-Audit (Titel, Descriptions, H1, Links, Anker, JSON-LD, CSP-Verstöße, Alt-Texte)
tools/serve.py         Lokaler Server mit Clean URLs und den Security-Headern
assets/                site.css, site.js, Schriften (lokal, kein Google-Fonts-Abruf), Bilder
vercel.json            Clean URLs, Security-Header (CSP, HSTS …), Caching
```

## Arbeiten

```bash
python3 tools/build.py        # Seiten neu erzeugen (Root-Dateien werden überschrieben — nicht von Hand editieren)
python3 tools/audit.py        # QA-Audit, Exit-Code 1 bei Fehlern
python3 tools/serve.py 8960   # http://localhost:8960
git add -A && git commit && git push   # Deployment über Vercel (Projekt gap-lab-lp)
```

Die generierten `*.html`, `sitemap.xml`, `robots.txt` und `llms.txt` liegen im Repository, weil Vercel sie direkt ausliefert.
CSS/JS erhalten automatisch einen Hash als `?v=`-Parameter (immutable Caching, kein Stale-Cache nach Änderungen).

## Inhalte pflegen

* Firmen-/Registerdaten und Partnerprofile: `tools/siteinfo.py`
* Texte: `tools/pages_*.py` (HTML-Strings). Neue Seite = neue Funktion + Eintrag in `build()`.
* Nach jeder inhaltlichen Änderung `SITE["modified"]` / `modified_de` aktualisieren (steht sichtbar als „Stand“ und in `dateModified`).
* **Regel:** Nur belegte Angaben veröffentlichen (Handelsregister, veröffentlichte Profile). Keine Referenzen, Zahlen, Kunden oder Preise erfinden.

## SEO / GEO

* Pro Seite: eigener Title, Description, Canonical, hreflang (de, x-default), Open Graph, Twitter Card, Breadcrumbs.
* JSON-LD: `Organization` (mit Handelsregister-Kennung, Mutter-/Tochter-Beziehung zu schubart-dulgeridis.de), `WebSite`, `WebPage`/`AboutPage`/`ContactPage`/`CollectionPage`, `BreadcrumbList`, `Service`, `FAQPage`, `Person`.
* Answer-First-Boxen („Kurzantwort“) auf Leistungs- und Fokusfeldseiten, FAQ mit Seiten-Schema, `llms.txt`, KI-Crawler in `robots.txt` ausdrücklich erlaubt.
* Nach dem Livegang: Sitemap in Google Search Console und Bing Webmaster Tools einreichen.

## Sicherheit & Datenschutz

* Keine Cookies, keine Tracker, keine Drittanbieter-Requests (Schriften und Bilder lokal). Deshalb kein Cookie-Banner.
* CSP `default-src 'self'` (kein Inline-Code erlaubt), HSTS, `nosniff`, Referrer-/Permissions-Policy, `frame-ancestors 'none'`.
* Wird später ein Dienst eingebunden (Analytics, Karte, Formular, Newsletter), **vorher** Datenschutzerklärung, CSP und ggf. Consent anpassen.

## Formulare

Es gibt bewusst kein Kontaktformular: Anfragen laufen über E-Mail/Telefon, Termine über die Kalender der Partner auf schubart-dulgeridis.de. Ein eigenes Formular braucht ein Backend (serverseitige Validierung, Honeypot, Rate-Limiting, Zustellung) und eine angepasste Datenschutzerklärung.

## Analytics-Konzept (noch nicht aktiv)

Empfehlung: datenschutzfreundliches, cookieloses Tool; Events erst nach Anpassung von Datenschutz und CSP aktivieren.

| Event | Trigger | Bedeutung | Funnel | Gewicht |
|---|---|---|---|---|
| `page_view` | Seitenaufruf | Reichweite | Awareness | 1 |
| `service_view` | /leistungen, /fokusfelder/* | Interesse an Leistung | Consideration | 2 |
| `cta_click` | Klick „Erstgespräch vereinbaren“ | Kaufinteresse | Decision | 4 |
| `calendar_click` | Klick „Termin wählen“ (/kontakt) | Terminabsicht | Action | 8 |
| `contact_mail` / `contact_tel` | Klick mailto/tel | Direktanfrage | Action | 8 |
| `faq_open` | FAQ aufgeklappt | Informationsbedarf | Consideration | 1 |
| `outbound_click` | Link zu schubart-dulgeridis.de | Verbund-Interesse | Consideration | 1 |

## Offene Punkte (vor/nach Livegang prüfen)

Siehe Abschlussbericht: vollständiger Unternehmensgegenstand und Stammkapital (Registerauszug unvollständig), USt-IdNr., eigene E-Mail-Adresse @gap-lab.de, rechtliche Prüfung von Impressum und Datenschutz, Bestätigung der inhaltlichen Leistungsbeschreibung.
