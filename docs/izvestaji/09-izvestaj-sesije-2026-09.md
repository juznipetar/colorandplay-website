# Izveštaj sesije 09 — 2026-09-18 (Cloud Agent, Faza 7 implementacija)

Pre početka: `git pull origin main`, pročitan `docs/faza7-spec.md`, `docs/ROADMAP.md` Faza 7.

---

## Šta je urađeno

### A) Faza 7.0 — build sistem

1. **`data/opisi.json`** — prošireni marketing opis (DE/EN) + 3–4 FAQ po svih 11 slug-ova.
   **NACRT** — Petar/Suzana treba da pregledaju ton pre nego što se tretira kao finalni copy.

2. **`build_pages.py`** — lokalna skripta (pokretanje: `python3 build_pages.py` iz repo root-a):
   - Čita `pricing.json`, `gallery.json`, `opisi.json`
   - Regeneriše blok između `<!-- BUILD:PACKAGES-START/END -->` na `index.html` (tiers + „Mehr erfahren“)
   - Generiše `/pakete/<slug>/index.html` (svih 11)
   - Generiše `/galerie/index.html` sa placeholder pločicama
   - Generiše `/impressum/` i `/datenschutz/` nacrte
   - Ažurira `sitemap.xml`

3. **Success gate:** `git diff index.html` posle build-a ne menja cene — samo struktura (sig-head-left, Mehr erfahren linkovi). Provereno: Kindergeburtstage CHF 390/480/600 ostaje identično.

### B) Paket-stranice (svih 11)

Po `faza7-spec.md`: breadcrumb, hero placeholder (blob gradient), tiers iz JSON, mini-galerija placeholder, FAQ iz opisi.json, CTA `../../index.html?paket=<slug>#kontakt`, Service JSON-LD, i18n parovi.

### C) Galerija `/galerie/`

Grid + accessible lightbox (focus trap, Escape, aria-labels, reduced-motion). Placeholder: „Fotos folgen in Kürze“ / „Photos coming soon“ — bez stock fotografija.

### D) Faza 6a — Impressum + Datenschutz (nacrti)

`/impressum/index.html` i `/datenschutz/index.html` DE/EN sa vidljivim `[TODO: potvrditi]` za pravno ime i tačnu ulicu. Datenschutz pominje Formspree i GitHub Pages. Linkovi u footer-u na index i podstranicama.

### E) Povezivanje sa index.html

- Nav: Galerie/Gallery
- „Mehr erfahren“ / „Learn more“ na svakoj signature grupi
- **`?paket=` mehanizam:** hidden polje `contact-paket` (name=`paket` za Formspree), `sessionStorage` (`cap_paket`), prefilled poruka „Interesse am Paket: …“ / „Interested in package: …“, scroll na `#kontakt` kad je u URL-u

### F) i18n

`python3 check_i18n.py` na svih 16 HTML fajlova — **svi OK**.

---

## Šta čeka na čoveka

1. **Pregled `data/opisi.json`** — marketing ton i FAQ pre go-live
2. **Vizuelni pregled** bar jedne paket-stranice (pilot: Kindergeburtstage)
3. **`[TODO: potvrditi]`** — pravno ime firme i tačna ulica u Impressum/Datenschutz
4. **15–20 pravih fotografija** ateljea za `data/gallery.json` + `/assets/galerie/`
5. Formspree ID, businessplan lozinka, domena — nepromenjeno iz ranijih faza

---

## Kako pokrenuti build

```bash
cd /path/to/colorandplay-website
python3 build_pages.py
python3 check_i18n.py index.html businessplan/index.html galerie/index.html impressum/index.html datenschutz/index.html pakete/*/index.html
git add -A && git commit ...
```

Posle izmene cene: menjati **samo** `data/pricing.json`, pa `python3 build_pages.py`.
