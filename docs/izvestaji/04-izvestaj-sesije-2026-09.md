# Izveštaj sesije 04 — 2026-09-18 (Cloud Agent, Composer 2.5)

Pre nastavka: `git log`, `git status`, `python3 check_i18n.py index.html businessplan/index.html`.

## Šta je urađeno

### A) DE/EN tipfelera + mailto

- Ručno pročitan vidljiv marketing copy na `index.html` (DE i EN).
- **Ispravka:** DE „von frühem Nachmittag“ → „vom frühen Nachmittag“ (jasna gramatička greška).
- Ostali tekstovi: bez daljih očiglednih tipfelera; ton nije prepisivan.
- **mailto:** `suzana.androvic@gmail.com` — ista adresa u `index.html` (CTA + fallback) i `businessplan/index.html`; nije izmišljana nova adresa.

### B) Kontakt formular (Formspree)

- U `#kontakt`: forma (name, email, message, optional phone) sa `action="https://formspree.io/f/YOUR_FORMSPREE_ID"`.
- Dizajn usklađen sa postojećim CSS varijablama (`.contact-form`, `.infocard`), tab-fokus, `aria-live` status, `prefers-reduced-motion` na input tranzicijama.
- JS: `fetch` POST na Formspree; poruka ako ID još nije zamenjen; mailto CTA ostaje u sidebar-u.
- **DEPLOY.md** sekcija 7: koraci za Petara/Suzanu (besplatan Formspree nalog, zamena ID-ja).

### C) Calendly (samo istraživanje)

- `docs/predlog-calendly.md`: opcije embeda, cene/provizije, hibridni model sa formularom, alternative, preporučen sledeći korak — **bez implementacije** na sajtu.

### Dokumentacija

- `docs/ROADMAP.md`: označene završene stavke (tipfelera/mailto, Formspree, Calendly predlog).

## Verifikacija

- `python3 check_i18n.py index.html businessplan/index.html` — mora biti OK pre merge-a.

## Šta ostaje otvoreno (nije u ovom PR-u)

- Faza 2: puna accessibility revizija, Lighthouse performance.
- Faza 3: tier proširenje za preostalih 6 paketa.
- Faza 1: COVEK — domena, nova businessplan lozinka, Cloudflare Access (opciono).
- **COVEK:** Formspree nalog + zamena `YOUR_FORMSPREE_ID` u `index.html`.
- **COVEK:** Odluka o Calendly pilotu (vidi `docs/predlog-calendly.md`).

## Šta korisnik treba da odluči

1. Kreirati Formspree formu i zameniti placeholder ID (uputstvo u DEPLOY.md).
2. Da li i kada uvesti Calendly (embed tek posle pilota).
3. I dalje: boja paleta, nova lozinka businessplan-a, .ch domena.
