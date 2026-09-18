# Izveštaj sesije 07 — 2026-09-18 (Cloud Agent, Faza 6a)

Pre nastavka: `git pull origin main`, `python3 check_i18n.py businessplan/index.html`.

---

## Urađeno u ovoj sesiji

### Sesija A — 404 + print stylesheet (main)

1. **`404.html` (root)** — GitHub Pages custom 404 u Playful Pastel stilu
   (paper/cream/teal/coral/yellow/mist). DE/EN preko `data-lang` + lang toggle
   (isti `cap-lang` localStorage ključ kao glavni sajt). Link na start: `./`.
   `noindex` meta — ne dira `robots.txt`.
2. **Print stylesheet** — `@media print` u `businessplan/index.html`: sakriveni
   `#bp-gate`, `.topbar`, `.langtoggle`, `.pdfhint`, `.livebadge`; B&W-prijateljski
   teal/tamni tekst; `break-inside: avoid` na poglavljima i tabelama. Nema izmena
   finansijskih brojeva ni gate lozinke.
3. **ROADMAP** — Faza 6 (a): Custom 404 i Print stylesheet označeni `[x]`.

### Sesija B — JSON-LD LocalBusiness (PR #8)

**Faza 6 (a): JSON-LD structured data (schema.org LocalBusiness)** na
`index.html`.

- Jedan `<script type="application/ld+json">` blok u `<head>`, posle Twitter
  Card meta tagova.
- `@type`: `LocalBusiness` (Kreativatelier — nema potrebe za podtipom
  ArtGallery).
- Uključeni samo podaci već prisutni na sajtu:
  - **name:** Color and Play
  - **description:** ista formulacija kao `meta name="description"` (DE)
  - **url:** `https://juznipetar.github.io/colorandplay-website/`
  - **email:** `suzana.androvic@gmail.com` (mailto u `#kontakt`)
  - **image:** postojeći `og-image.png` (već referenciran u OG tagovima)
  - **address:** `PostalAddress` sa `addressLocality` Baar,
    `addressRegion` Kanton Zug, `addressCountry` CH — **bez** `streetAddress`
    (sajt kaže „Folgt in Kürze“)
  - **priceRange:** `CHF 39 - CHF 600` (od najniže vidljive cene na stranici
    do All-Inclusive Kindergeburtstag)
  - **openingHoursSpecification:** Di–Fr 15:00–21:00, Sa 11:00–20:00,
    So 10:00–21:00; ponedeljak isključen (zatvoren na sajtu)
- Namerno **nije** dodato: ulica, telefon, ocene/recenzije, izmišljeni geo
  koordinati.

4. **ROADMAP** — Faza 6 (a): JSON-LD LocalBusiness označen `[x]`.

## Verifikacija

```bash
python3 check_i18n.py index.html businessplan/index.html
# index.html: de=188 en=188  [OK]
# businessplan/index.html: de=158 en=158  [OK]
```

- `404.html` nema `i18n` klasu na elementima (samo `data-lang`) — van opsega
  `check_i18n.py` skripte; DE/EN parovi ručno provereni (3+3 tekst bloka)
- JSON-LD je u `<head>` i ne koristi `.i18n` / `data-lang` — i18n brojači
  nepromenjeni.

## Šta je sledeće (Faza 6a, preostalo)

- Impressum + Datenschutz (čeka pravno ime/adresu od čoveka)
- Paket-kviz, vaučer preview generator
