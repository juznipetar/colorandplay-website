# Color and Play — Arhitektura sajta

Tehnicka dokumentacija za svakog ko (covek ili bot) nastavlja rad na ovom sajtu.

## Struktura fajlova

**VAZNO:** ovaj git repo (`Desktop\Color & Play` na ovom racunaru,
`github.com/juznipetar/colorandplay-website`) ima sve na ROOT nivou — nema
`site/` podfoldera u samom repo-u. Kad ova dokumentacija (ili stariji izvestaji)
pominju `site/index.html`, misli se na putanju relativno u odnosu na cloud dev
projekat (vidi ispod) — u OVOM repo-u je to prosto `index.html`.

```
(repo root — Desktop\Color & Play)
  index.html              javna marketing stranica (deploy: /)
  businessplan/
    index.html             zasticena biznis-plan stranica (deploy: /businessplan/)
  robots.txt               blokira /businessplan/ za search engine crawlere, referencira sitemap.xml
  sitemap.xml              samo javna stranica, businessplan NIJE u sitemap-u
  favicon.svg, favicon.ico, favicon-16.png, favicon-32.png,
  favicon-192.png, favicon-512.png, apple-touch-icon.png    favicon set (teal/gold)
  og-image.png             1200x630 OG/Twitter preview slika
  check_i18n.py            proverava da li DE/EN parovi postoje (pokreni pre svakog commit-a)
  DEPLOY.md                uputstvo za GitHub Pages + domenu (za coveka)
  .gitignore                iskljucuje "Claude outputs/" (rezidual od file-delivery mehanizma)
  docs/
    ROADMAP.md              fazni plan rada (ovaj fajl prati "roadmap rezim")
    ARHITEKTURA.md           ovaj fajl
    BOT-INSTRUKCIJE.md       direktna instrukcija za automatizovanog agenta
  CNAME                    (dodaje se tek kad je domena kupljena — vidi DEPLOY.md)
```

Van ovog repo-a, u cloud dev projektu (Cowork sesija koja je ovo napravila —
NIJE na ovom racunaru osim ako ti neko eksplicitno prebaci te fajlove):
```
pitch.html          izvor sadrzaja za businessplan stranicu (identican sadrzaj)
build_site.py        generise site/businessplan/index.html iz pitch.html + lozinka-gate
                      (u cloud projektu se output stavlja u lokalni site/ podfolder
                      pre kopiranja u OVAJ repo — otud ime "site/" u starijim beleskama)
build_print.py        generise print.html (za PDF)
make_pdfs.py           generise oba PDF-a (DE/EN)
model.py                finansijski model (izvor brojeva u pitch.html)
```

Ako menjas `businessplan/index.html` sadrzaj, a nemas pristup `pitch.html` +
`build_site.py` na ovom racunaru, PITAJ korisnika da ti ih prebaci — ne
rekonstruisi build skriptu iz ovog fajla, kopiraj postojecu.

## Princip: oba HTML fajla su potpuno samostalna

Nema build koraka, nema npm/node zavisnosti, nema eksternih JS biblioteka osim
Google Fonts (ucitanih preko `<link>`). Sav CSS i JS je inline u `<style>`/`<script>`
tagovima unutar svakog fajla. Ovo je namerno: GitHub Pages servira staticke fajlove
1:1, bez build pipeline-a, sto znaci nula tacaka kvara pri deployu.

**Kad dodajes nesto novo, drzi se ovog principa** — ne uvodi bundler (Webpack/Vite)
ni framework (React/Vue) bez eksplicitnog dogovora. Ako sajt naraste do te mere da
je to opravdano, to je posebna odluka, ne nesto sto se radi usput.

## Dizajn sistem (CSS custom properties)

Oba fajla (`index.html`, `businessplan/index.html`) definisu ISTE `:root` promenljive
na vrhu `<style>` bloka — namerno duplirano (nema shared CSS fajla, jer bi to zahtevalo
build korak). Ako menjas boje/fontove, promeni na oba mesta ili napravi shared
`brand.css` i ukljuci ga sa `<link>` (jednostavna izmena, nije uradjena jos jer je
sajt mali).

```css
--bg / --surface / --surface-2 / --surface-3    pozadine (svetlije ka tamnijem)
--ink / --ink-soft / --ink-faint                 tekst (tamnije ka svetlijem)
--line / --line-strong                           linije/border-ovi
--teal / --teal-deep / --teal-soft               primarna boja brenda
--gold / --gold-soft                              akcentna boja (brand dot, badge glow)
--coral / --coral-soft                            akcentna boja (eyebrow, error stanja)
--sage                                             sekundarna akcentna (kicker tekst)
--font-display   Fraunces (naslovi, serif)
--font-body       Work Sans (telo teksta)
--font-mono       IBM Plex Mono (cene, cifre, labele)
```

Dark mode je automatski (`@media (prefers-color-scheme: dark)`) plus rucni override
(`:root[data-theme="dark"]` / `:root[data-theme="light"]`) — trenutno nista ne postavlja
`data-theme` atribut, pa sajt prati sistemsko podesavanje korisnika.

## i18n (DE/EN) mehanizam

Svaki element koji ima tekst u oba jezika je udvojen:
```html
<span class="i18n" data-lang="de">Tekst na nemackom</span>
<span class="i18n" data-lang="en" hidden>Text in English</span>
```
`setLang(lang)` (u `<script>` na dnu fajla) prolazi kroz sve `.i18n` elemente i
postavlja `hidden` na osnovu toga da li se `data-lang` poklapa sa izabranim jezikom.
Jezik se pamti u `localStorage` (kljuc `cap_lang`), pa se korisniku pamti izbor pri
sledecoj poseti.

**Pravilo:** kad dodajes novi tekst, UVEK dodaj oba jezika u paru. Skripta za proveru
i18n parova (Faza 2 u ROADMAP.md) ovo automatski proverava.

## Tier pricing komponenta (Basic/Advance/All Inclusive)

Ovo je novi obrazac dodat na zahtev korisnika (premium izgled, vise cenovnih nivoa).
HTML struktura za jednu grupu paketa:

```html
<div class="signature reveal">
  <div class="sig-head">
    <h3>Naziv paketa</h3>
    <span class="sig-tag">kratak opis/uslov</span>
  </div>
  <div class="tiers reveal-stagger reveal">
    <div class="tier" style="--i:0"> ... Basic ... </div>
    <div class="tier popular" style="--i:1">
      <span class="badge">Beliebt</span>
      ... Advance ...
    </div>
    <div class="tier" style="--i:2"> ... All Inclusive ... </div>
  </div>
</div>
```

- `.tier.popular` je uvek srednja kolona — vizuelno istaknuta (border boja, blagi
  gradijent, senka, na desktopu i malo podignuta). Ovo je namerna prodajna taktika
  (classic "decoy effect" pricing pattern) — srednja opcija deluje kao najbolja
  vrednost.
- `--i:N` na svakom `.tier`/`.offercard`/`.prop` elementu je redni broj koji CSS
  koristi za stagger-ovano pojavljivanje (`transition-delay: calc(var(--i,0) * 70ms)`)
  kad roditeljski `.reveal-stagger` dobije klasu `is-visible`.
- Da dodas NOVU grupu paketa sa tier-ovima: kopiraj ceo `.signature` blok, promeni
  tekst/cene, zadrzi `popular` na srednjoj koloni (ili je ukloni ako nema smisla
  isticati nijednu).

## Animacije

Sve animacije su cist CSS + `IntersectionObserver` (nema animacione biblioteke):

- **`.reveal`** — fade+slide-up kad element udje u viewport (scroll reveal)
- **`.reveal-stagger`** — deca unutar njega dobijaju postepeno kasnjenje (vidi `--i`)
- **`.blob`** — plutajuci obojeni krugovi u hero sekciji (`@keyframes float`),
  cisto dekorativno, `aria-hidden="true"`
- **count-up brojaci** — elementi sa `data-count="N"` (opciono `data-suffix="%"`)
  animiraju se od 0 do N kad udju u viewport (`animateCount()` funkcija)
- **hover efekti** — kartice (`.tier`, `.offercard`, `.prop`, `.step`) se blago
  podizu (`translateY`) i dobijaju jacu senku na hover

Sve animacije postuju `prefers-reduced-motion: reduce` — kad je to podeseno,
`.reveal` elementi su odmah vidljivi bez tranzicije, `.blob` se ne pomera, brojaci
odmah pokazuju finalnu vrednost. **Ne uklanjaj ovu proveru** — pristupacnost je
namerna odluka, ne slucajnost.

## Kako dodati potpuno nov paket (bez tier-ova, obican `.offercard`)

Kopiraj jedan `<div class="offercard">` blok iz sekcije "Weitere Angebote", promeni
`tag`/`h4`/`desc`/`price` (svaki u DE i EN paru), dodaj `style="--i:N"` sa sledecim
rednim brojem u toj grid-i za stagger animaciju.

## Zastita businessplan stranice — tehnicki detalji

`build_site.py` (van `site/` foldera) cita `pitch.html`, i:
1. Ubacuje `<meta name="robots" content="noindex, nofollow">`
2. Ubacuje CSS za `#bp-gate` (overlay sa lozinkom) i `#bp-content` (sakriven dok se
   ne unese tacna lozinka)
3. Racuna SHA-256 hash od `PASSWORD` promenljive na vrhu skripte i ubacuje ga u JS
   (`bpUnlock()` funkcija poredi hash unetog teksta sa ovim hash-om preko
   `crypto.subtle.digest`)
4. Cuva "otkljucano" stanje u `sessionStorage` (ne `localStorage`) — znaci da se
   lozinka trazi ponovo u novom tabu/sesiji, sto je namerno (ne zelimo trajno
   otkljucano stanje na deljenom racunaru)

**Ovo NIJE prava server-side autentikacija.** Neko ko otvori "View Source" i zna da
trazi `HASH` promenljivu i uporedi je sa recnikom hash-ova cestih lozinki bi teorijski
mogao da provali kod (rainbow table napad na jednostavnu lozinku). Za ovu svrhu
(privremeno deljenje sa jednim vlasnikom lokala, stranica se brise posle pregleda)
ovo je dovoljno. Za jace resenje vidi `DEPLOY.md` sekcija 6 (Cloudflare Access).

## Poznata ogranicenja / tehnicki dug

- Cene postoje na dva mesta rucno (marketing stranica + businessplan) — vidi
  ROADMAP.md Faza 4 za plan konsolidacije u jedan JSON izvor
- Nema pravog kontakt formulara, samo `mailto:` link — radi, ali ne loguje upite
  nigde niti radi validaciju
- Nema favicon/OG meta tagova jos (ROADMAP.md Faza 2)
- Tier struktura (Basic/Advance/All Inclusive) postoji za svih 11 paketa na
  marketing stranici (Faza 3 zavrsena 2026-09-18). Cene u `businessplan/index.html`
  i dalje su odvojene — vidi Faza 4 za plan konsolidacije.
