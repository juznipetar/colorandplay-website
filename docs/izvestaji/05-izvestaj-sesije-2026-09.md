# Izveštaj sesije 05 — 2026-09-18 (Cloud Agent, Composer 2.5)

Pre nastavka: `git pull origin main`, `python3 check_i18n.py index.html businessplan/index.html`.

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

## Verifikacija

```bash
python3 check_i18n.py index.html businessplan/index.html
```

## ROADMAP

Označena odluka o paleti (ranije „čeka korisnika“ u izveštaju 04).
