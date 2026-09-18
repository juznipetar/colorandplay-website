# Izveštaj sesije 05 — 2026-09-18 (Cloud Agent, Composer 2.5)

Pre nastavka: `git pull origin main`, `python3 check_i18n.py index.html businessplan/index.html`.

---

## Paleta — Playful Pastel / Manus (user-approved)

Izvor istine: [bojaprica-ewkzvomb.manus.space](https://bojaprica-ewkzvomb.manus.space)

Ekstrahovani `:root` tokeni sa reference sajta:

| Manus token | Hex | Mapiranje na postojeći Cap token |
|-------------|-----|----------------------------------|
| `--paper` | `#f7f1e7` | `--bg` |
| `--cream` | `#fffaf2` | `--surface` |
| (warm) | `#fff8ec` | `--surface-2` |
| (paper tint) | `#ede4d6` | `--surface-3` |
| `--ink` | `#20201c` | `--ink` |
| `--muted-ink` | `#5f5e56` | `--ink-soft` |
| (a11y faint) | `#6B6A62` | `--ink-faint` (zadržan AA kontrast na `--bg`) |
| `--teal` | `#0b8e8b` | `--teal` |
| `--teal-deep` | `#056866` | `--teal-deep` |
| `--mist` | `#dcebe5` | `--teal-soft`, `--sage` |
| `--yellow` | `#f5cb50` | `--gold` |
| (gold soft) | `#faedc4` | `--gold-soft` |
| `--coral` | `#ef7059` | `--coral` |
| (coral soft) | `#fde8e2` | `--coral-soft` |
| `--line` | `#20201c29` | `--line` |
| (line strong) | `#20201c47` | `--line-strong` |

Ista `:root` definicija (duplirano po `docs/ARHITEKTURA.md`) primenjena u `index.html` i `businessplan/index.html`.

### Dark mode

Dark override-i zadržavaju postojeću strukturu (`prefers-color-scheme` + `data-theme="dark"`), sa brand nijansama (`--gold: #f5cb50`, `--coral` blago posvetljena). `--teal-deep` u dark modu ostaje svetla nijansa za tekst; solid dugmad koriste fiksni `#056866` (WCAG AA sa belim tekstom).

### Kontrast (lokalne korekcije)

- Tekst na svetlim pozadinama: `em`, tagovi, checkmark-i → `--teal-deep` umesto `--teal`.
- CTA / skip-link / badge / gate dugmad: pozadina `--teal-deep` (light) ili `#056866` (dark).
- `.chip.med` tekst: `#6b4f0a` na novom `--gold-soft`.

### Favicon / OG

- `favicon.svg`: ažuriran na `#0b8e8b` / `#dcebe5` / `#f5cb50`.
- `og-image.png` i generisani PNG/ICO favicon set **nisu** u repo-u na ovom VM-u — nisu regenerisani; meta tagovi i dalje referenciraju postojeće fajlove na GitHub Pages.

---

## Deep polish — bugfix / a11y / form UX (bez promene `:root` tokena)

Posle merge PR #4; paleta primenjena odvojeno (gore). Ovaj PR dira samo layout, HTML validnost, form UX i gate ponašanje — **nema izmena `:root` hex vrednosti**.

### Automatske provere (pre fix-a)

| Provera | Rezultat |
|---------|----------|
| Live HTTP 200 (`/` i `/businessplan/`) | OK |
| `python3 check_i18n.py index.html businessplan/index.html` | OK (188/188, 158/158) |
| Duplikat `id` atributa | 0 |
| Broken internal anchors | 0 |
| Missing `alt` na `<img>` | N/A (nema slika u HTML-u) |
| `robots.txt` `Disallow: /businessplan/` | OK (live i repo) |
| `noindex` u `<head>` businessplan-a | OK |
| html5lib parse oba fajla | OK |
| Lokalni asset linkovi (favicon, og-image) | OK |

### Bugovi pronađeni i ispravljeni

#### `index.html`

1. **Sticky header prekriva anchor sekcije** — `scroll-padding-top` / `scroll-margin-top` (~72px) za `#pakete`, `#ablauf`, `#standort`, `#kontakt`, `#main`.
2. **Mobilna navigacija nedostupna** — `.navlinks` horizontalni scroll ispod branda (Pakete, Ablauf, Standort, Termin sichern).
3. **Trustbar „ab CHF 0“ flash** — statična cena `CHF 39` (bez count-up na prefiksiranom broju).
4. **Nevažeći HTML: dva `<legend>` u jednom `<fieldset>`** — spojeno u jedan `<legend>` sa DE/EN `.i18n` spanovima.
5. **Kontakt forma — validacija UX** — `.field.is-invalid`, `aria-invalid`, fokus na prvo nevalidno polje; clear on input.
6. **Formspree placeholder poruka** — `.form-status.warn` (informativno); ID nije menjan.
7. **`prefers-reduced-motion`** — hover `transform` off na `.cta`, `.prop`, `.tier`, `.step`, `.offercard`.

#### `businessplan/index.html`

8. **Gate greška ostaje posle pogrešnog koda** — `input` listener sakriva `#bp-err` i resetuje `aria-invalid`.

### Svesno odloženo

- **Formspree ID** — i dalje `YOUR_FORMSPREE_ID` (COVEK — `DEPLOY.md` §7).
- **Businessplan lozinka** — placeholder `ColorPlay2026`.
- **Nema novih DE/EN tipfelera** na ovom pass-u.

---

## Verifikacija

```bash
python3 check_i18n.py index.html businessplan/index.html
```

- html5lib parse — OK
- Gate, lang toggle, forma (prazno / placeholder / mailto) — smoke test u browseru

## ROADMAP

Označena odluka o paleti (ranije „čeka korisnika“ u izveštaju 04) i deep polish stavka u Fazi 2.

## Šta korisnik treba da odluči (nepromenjeno)

1. Formspree nalog + zamena placeholder ID-ja (`DEPLOY.md` §7).
2. Nova businessplan lozinka pre slanja linka Aligu.
3. Calendly pilot (`docs/predlog-calendly.md`).
