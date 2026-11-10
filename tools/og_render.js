// Rendert die Social-Bilder (1200x630) aus HTML-Dateien. Aufruf über tools/make_og_v2.py.
// Benötigt Node mit Playwright (npm i playwright). Eingabe: JSON-Datei mit [{html, out}].
const { chromium } = require("playwright");
const fs = require("fs");
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  for (const j of jobs) {
    await page.goto("file://" + j.html, { waitUntil: "load" });
    await page.waitForFunction(() => window.__fit === true, null, { timeout: 10000 });
    await page.screenshot({ path: j.out, type: "jpeg", quality: 86 });
    console.log("neu:", j.out);
  }
  await browser.close();
})();
