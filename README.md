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

## Redesign v2 (live seit 10. November 2026)

Das Redesign ist Standard: `python3 tools/build.py` erzeugt alle Seiten im neuen Design.
Gestaltung: `assets/v2.css`, `assets/v2.js`, `tools/v2.py` (Icons, Seitenkopf-Visuals, schwebende Leiste) und
`tools/v2_home.py` (Startseite: Brücken-Hero, Leitung mit Lecks, Stufen-Etagen, Fokus-Perspektiven, InnoLab vorher/nachher
und Zeitraster, KI-Cockpit, Zeitleiste, Begriffs-Explorer). Alle Inhalte stammen aus den bestehenden Modulen, Preise nur auf /innolab.

* `python3 tools/build.py --preview` erzeugt zusätzlich eine Vorschau unter `preview/` (`noindex`), z. B. für neue Entwürfe.
* `python3 tools/build.py --legacy` erzeugt das alte Design (nur zum Vergleich, nicht deployen).
* `python3 tools/make_og_v2.py` erzeugt die Social-Bilder (1200x630) im neuen Design, plattformunabhängig (Node + Playwright). Texte aus `tools/seo_meta.py`; die og:image-URLs tragen einen Versionsparameter, damit LinkedIn & Co. neue Bilder laden.

## Englische Fassung (/en)

Jede deutsche Seite hat eine englische Entsprechung unter `/en/…` (z. B. `/leistungen` → `/en/services`). Umschalter DE | EN
in der Kopfzeile, auf dem Handy im Menü. Die englischen Seiten entstehen beim Build automatisch aus den fertigen deutschen Seiten:

* `tools/i18n.py`: Übersetzung der erzeugten HTML-Seiten über einen Katalog, Adresszuordnung (`SLUGS`), hreflang de/en/x-default,
  `og:locale` en_GB, JSON-LD auf Englisch, eigene Skriptfassungen `assets/*.en.js`, Hinweis „nur die deutsche Fassung ist verbindlich“
  auf Impressum und Datenschutz.
* `tools/i18n/en.json`: Katalog (Schlüssel = deutscher Text, Wert = englischer Text). Platzhalter `<g0>…</g0>` und `<x0/>` exakt übernehmen,
  Skripttexte mit Präfix `js:`.
* `tools/i18n/STYLE.md`: Styleguide und Glossar (britisches Englisch, feste Begriffe, Preisformat `€13,300`).
* Neue oder geänderte deutsche Texte: `python3 tools/build.py --i18n-todo` schreibt die fehlenden Einträge nach `tools/i18n/todo_en.json`
  (wird nicht eingecheckt). Übersetzen, in `en.json` eintragen, neu bauen. Der Build meldet die Zahl fehlender Übersetzungen;
  fehlende Texte bleiben bis dahin deutsch.
* Social-Bilder: `python3 tools/make_og_v2.py` erzeugt zu jedem Motiv auch die englische Fassung `og-*.en.jpg`.

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

* Pro Seite: eigener Title, Description, Canonical, hreflang (de, en, x-default), Open Graph, Twitter Card, Breadcrumbs.
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

## Textvarianten

- **Aktuell (live):** stark reduzierte Fassung („Wesentliches“), kurze Aussagesätze, Details in Unterseiten und Glossar.
- **Archiv der kompakten Fassung (erste Reduktion):** Tag `archive/kompakt-v1-2026-11-04` (Branch `archiv-kompakt-v1-2026-11-04`).
- **Archiv der ausführlichen Fassung:** Git-Tag `archive/volltext-2026-11-04` (und Branch `archiv-volltext-2026-11-04`).
  Wiederherstellen: `git checkout archive/volltext-2026-11-04 -- .` (dann `python3 tools/build.py`).
- **Archiv vor dem visuellen Relaunch:** Tag `archive/kompakt-v2-2026-11-04` (Branch `archiv-kompakt-v2-2026-11-04`).
- **Archiv vor Überarbeitung von Leistungen, Über uns, InnoLab:** Tag `archive/relaunch-v1-2026-11-04` (Branch `archiv-relaunch-v1-2026-11-04`).
- **Archiv vor Abstände/InnoLab-Slider/FAQ-Suche:** Tag `archive/unterseiten-v1-2026-11-04` (Branch `archiv-unterseiten-v1-2026-11-04`).

## Werkzeuge (tools/, nicht im Deployment)
- `python3 tools/build.py`: erzeugt alle Seiten, Sitemap, robots.txt, llms.txt, llms-full.txt (Änderungsdatum je Seite aus `tools/lastmod.json`).
- `python3 tools/audit.py` und `python3 tools/check_site.py`: Marken-, Preis-, Schema-, Link-, Titel- und Beschreibungsprüfung.
- `python3 tools/layout_qa.py --widths 500,820,1280`: Layoutprüfung in Headless-Chrome.
- `python3 tools/make_og.py`: Social-Bilder aus `tools/seo_meta.py` (nur geänderte Texte werden neu gerendert).
- `python3 tools/verify_live.py`: Abgleich Live-Seite gegen lokalen Stand nach dem Push.
- SEO-Titel, Beschreibungen, Themen-Entitäten und Social-Bild-Texte je Seite stehen zentral in `tools/seo_meta.py`.
