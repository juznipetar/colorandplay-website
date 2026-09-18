# Izveštaj sesije 03 — 2026-09-18 (Cloud Agent)

Pre nego što nastaviš, **mašinski proveri stanje**: `git log --oneline -5`,
`python3 check_i18n.py index.html businessplan/index.html`.

Bazirano na grani `cursor/extend-tier-pricing-faza3-bc77` (Faza 3 tier rad).

## Šta je urađeno u ovoj sesiji

### 1. Accessibility audit + ispravke

**Lighthouse (live, pre izmena):** Accessibility 94 — dva konkretna problema
(kontrast, redosled naslova).

**Ispravljeno (oba HTML fajla gde je relevantno):**

| Oblast | Izmena |
|---|---|
| Kontrast | `--ink-faint` u light modu: `#8B9389` → `#6B746C` (WCAG AA na `--bg`); `.kicker` / `.chapter-kicker` koriste `--ink-soft` umesto `--sage`; footer i fineprint koriste `--ink-soft` |
| Redosled naslova | `index.html`: kartice „Warum" i koraci „Ablauf" — `h4` → `h3` (više nema preskakanja h2→h4) |
| Fokus | Globalni `:focus-visible` outline (teal) na linkovima, dugmadima, inputima |
| Skip link | DE/EN „Zum Inhalt springen" / „Skip to content" na `index.html` |
| Semantika | `<main id="main">` omotač na marketing stranici |
| Lang toggle | `aria-label` na grupi (DE/EN) i na dugmadima (`Deutsch` / `English`) |
| Navigacija | `aria-label` na `<nav>` |
| Brand link | `aria-label` + `aria-hidden` na dekorativnoj tački |
| `prefers-reduced-motion` | Dodato gašenje `.brandmark .dot` pulse i `.tier .badge` glow animacija (businessplan: `.fade-in`) |
| Businessplan gate | `role="dialog"`, `aria-modal`, `aria-labelledby/describedby`, `<label for>`, `role="alert"` na grešci, `aria-invalid` + fokus na input pri pogrešnom kodu, auto-fokus na lozinku pri učitavanju |

**Potvrđeno / nije bilo problema:**

- Nema `<img>` bez `alt` (sajt koristi CSS/SVG dekoracije sa `aria-hidden`)
- `prefers-reduced-motion` za scroll-reveal, blob i count-up već radio — proširen
- i18n toggle već imao `aria-pressed` — zadržano

**Odloženo (za odluku vlasnika brenda):**

- `--sage` token i dalje postoji u paleti ali se ne koristi za sitan uppercase tekst
  koji pada ispod AA — čeka potvrdu da li se menja globalno ili ostaje samo za
  dekorativne elemente
- `--gold` na `--bg` (2.47:1) — koristi se samo za dekorativnu brend-tačku, ne za
  čitljiv tekst; nije menjano

### 2. Performance

**Lighthouse (live, pre izmena):** Performance 91, SEO 100.

**Lighthouse (lokalno posle izmena):** Performance 99, Accessibility 100, SEO 100,
Best Practices 100.

| Oblast | Izmena |
|---|---|
| Google Fonts | Async učitavanje (`preload` + `media="print" onload`); smanjen broj
  font-weight varijanti (samo korišćene: Fraunces 600 + italic 600, Work Sans
  400/500/600, IBM Plex Mono 400/500/600) |
| Render-blocking | Font CSS više ne blokira first paint |

Nije dirano: `og-image.png` (129 KB, 1200×630 — odgovarajuća veličina za OG),
favicon set (već mali PNG-ovi).

### 3. Tipfelera (lagani prolaz)

Automatski scan za uobičajene EN greške — nije nađeno. Nema jasnih DE/EN
tipfelera u marketing tekstu; puno ručno čitanje reč-po-reč i dalje nije urađeno
(vidi ROADMAP).

### 4. i18n

`check_i18n.py` — index.html 179/179, businessplan 158/158 OK (novi par: skip link).

## Lighthouse rezime

| Metrika | Pre (live) | Posle (lokalno) |
|---|---:|---:|
| Performance | 91 | 99 |
| Accessibility | 94 | 100 |
| SEO | 100 | 100 |
| Best Practices | 100 | 100 |

Napomena: „posle" merenje je na lokalnom HTTP serveru sa istim HTML-om koji ide u
PR; live GitHub Pages će pokazati slične rezultate posle merge-a i deploy-a.

## Šta i dalje čeka

- **COVEK:** Nova lozinka businessplan, odluka o paleti, .ch domena
- **BOT:** Formspree/Calendly istraživanje (Faza 3), `pricing.json` (Faza 4)
- **Faza 2:** Puno ručno čitanje DE/EN teksta na tipfelere (nije urađeno u ovoj sesiji)
