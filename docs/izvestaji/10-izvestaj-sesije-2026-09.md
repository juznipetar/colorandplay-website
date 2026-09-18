# Izveštaj sesije 10 — 2026-09-18 (Cloud Agent, FINAL deep-check posle Faze 7)

Pre početka: `git pull origin main` (PR #9 Faza 7 merged), pročitan `docs/ROADMAP.md` i `docs/faza7-spec.md`.

Poslednji BOT pass pre hard stop-a — cilj: pronaći i ispraviti stvarne bagove, ne drive-by rewrite.

---

## Checklist — rezultati

| # | Provera | Rezultat |
|---|---|---|
| 1 | Live HTTP 200 (home, paket, galerie, impressum, datenschutz, 404.html) + 404 na nepoznatoj putanji | ✅ Sve 200 osim namernog 404 |
| 2 | Relativne putanje asset-a na ugnježdenim stranicama (`../../favicon.*`, linkovi na index) | ✅ Nema broken path-ova |
| 3 | Nav: Galerie, Mehr erfahren (×11), breadcrumbs, footer impressum/datenschutz, CTA `?paket=` | ✅ Sve prisutno i ispravno |
| 4 | `python3 check_i18n.py` na svih 17 HTML fajlova | ✅ Svi OK (204/204 index, 37/37 paketi, …) |
| 5 | Duplikat ID, alt na slikama, forma + gate, noindex businessplan, robots.txt | ✅ Čisto; forma 3 required polja + optional phone (očekivano) |
| 6 | Galerija lightbox a11y (focus trap, Escape, reduced-motion) | ⚠️ Kod postojao u `build_pages.py` ali **nije bio u output HTML-u** dok `gallery.json` nema slika — ispravljeno (vidi ispod) |
| 7 | `python3 build_pages.py` — bez drift-a cena | ✅ `git diff index.html` prazan posle build-a; 33/33 tier cena = `pricing.json` |
| 8 | HTML validnost / mobilni overflow na paket-stranici | ✅ Lokalni browser test 375px — bez horizontalnog overflow-a |
| 9 | Form + gate | ✅ Validacija forme, gate greška se čisti pri kucanju, noindex u `<head>` |

---

## Pronađeno i ispravljeno

### 1. `404.html` — pogrešan localStorage ključ za jezik

- **Bug:** `LANG_KEY = "cap-lang"` (crtica) dok ostatak sajta koristi `"cap_lang"` (underscore).
- **Posledica:** Jezik izabran na 404 stranici nije delio preference sa ostatkom sajta.
- **Fix:** Usaglašeno na `cap_lang`.

### 2. `check_i18n.py` — zastareli default putovi

- **Bug:** Default argumenti `site/index.html` / `site/businessplan/index.html` — `site/` folder ne postoji u repo-u → skripta pada bez argumenata.
- **Fix:** Auto-discovery svih HTML fajlova (`index.html`, `404.html`, `businessplan/`, `galerie/`, `impressum/`, `datenschutz/`, `pakete/*/index.html`).

### 3. Lightbox infrastruktura nije bila u generisanom HTML-u (placeholder faza)

- **Bug:** `generate_gallery_page()` i `generate_package_page()` uključivale `{render_lightbox() if images else ""}` — dok je `data/gallery.json` prazan (`slike: []`), nijedna stranica nije imala lightbox markup ni JS, iako je CSS bio prisutan.
- **Posledica:** Kad stignu prave fotografije, build bi dodao lightbox — ali trenutni deployed HTML nije imao a11y kod za verifikaciju; rizik regresije pri prvom dodavanju slika.
- **Fix u `build_pages.py`:**
  - Lightbox HTML + `LIGHTBOX_JS` uvek na `/galerie/` i svih 11 paket-stranica.
  - `imgAltForLang()` — lightbox koristi `data-alt-de` / `data-alt-en` (ne prazan `alt=""`).
  - `syncGalleryAria()` + wrap `setLang` — `aria-label` na gallery-item dugmadima prati DE/EN.

---

## Odloženo (namerno, ne bagovi)

| Stavka | Razlog |
|---|---|
| Formspree ID | Čeka čoveka — placeholder `YOUR_FORMSPREE_ID` |
| Pravno ime / ulica u Impressum/Datenschutz | `[TODO: potvrditi]` — ne izmišljati |
| Prave fotografije galerije | `slike: []` — placeholder pločice OK |
| Businessplan lozinka | Placeholder — ne menjati bez Petra/Suzane |
| Impressum/Datenschutz u `sitemap.xml` | Nije u spec-u Faze 7; mogu se dodati kasnije |
| Trim dead contact-form JS sa podstranica | Nije funkcionalni bag — samo ~150 linija neaktivnog JS-a kopiranog iz index `<script>` bloka |

---

## Build komande (verifikovano)

```bash
python3 build_pages.py          # regeneriše pakete, galeriju, legal — index cene ne dira
python3 check_i18n.py           # svi HTML fajlovi, exit 0
```

---

## Zaključak

Sajt je u dobrom stanju posle Faze 7. Tri manja baga ispravljena (404 lang sync, check_i18n default, lightbox deploy/a11y). Nema regresije cena. Spreman za hard stop BOT faze — preostalo je na čoveku (fotografije, Formspree, pravni podaci, vizuelni pilot pregled).
