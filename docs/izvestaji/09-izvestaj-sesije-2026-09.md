# Izveštaj sesije 09 — 2026-09-18 (Cloud Agent, "nastavi sa izradom plana")

Pre nastavka: `git pull origin main`, `python3 check_i18n.py index.html businessplan/index.html`.

---

## Kontekst

Korisnik je posle prethodne sesije (Faza 7 upisana u ROADMAP kao prosa/opis)
rekao "nastavi sa izradom plana, budi pametan". Umesto da samo dodam još teksta
u ROADMAP.md, odlučeno je da najpametniji nastavak jeste da se ukloni što više
nejasnoće/ponovnog izmišljanja za bota — konkretni, odmah upotrebljivi
artefakti umesto još opisa. **Ovo je i dalje plan/scaffold, ne implementacija
sajta** — nijedna live stranica nije menjana osim postojećih planning
dokumenata i dva nova podatkovna fajla koje ništa na sajtu još ne učitava.

## Šta je napravljeno

### 1) `data/pricing.json` — pravi podaci, ne izmišljeni

Umesto da u spec-u samo opišem šemu, live `index.html` je programski
(Python + regex, ne ručno prekucavanje) parsiran i svih **11 paketa × 3
tier-a** izvučeno tačno onako kako trenutno stoje na sajtu — nazivi (DE/EN),
tagovi, cene, jedinice (` / Pers.`, ` / Monat`, ` / Tag / Kind`...), da li je
tier "popular", i sve pogodnosti po tier-u (DE/EN parovi). Provereno da je
ekstrakcija tačna (11 paketa, svaki sa tačno 3 tier-a, brojevi se poklapaju sa
poznatim iz `docs/izvestaji/02...md`). Ovo uklanja najveći rizik u Fazi 7.0 —
da bot ručno prekucava 33 cene i pritom negde pogreši ili zaboravi jedinicu.

### 2) `data/gallery.json` — spremna šema, namerno prazna

Struktura za galeriju (fajl, alt DE/EN, tagovi, hero-oznaka) postoji i radi sa
`slike: []` (placeholder stanje se oslanja na prazan niz, ne na fiktivne
unose) — kad prave fotografije stignu, dodavanje je čisto podatkovna izmena,
ne kod.

### 3) `docs/faza7-spec.md` (NOVO) — tehnički pratilac ROADMAP.md Faza 7

ROADMAP.md Faza 7 je opisivala ŠTA i ZAŠTO; ovaj fajl daje TAČAN OBLIK, da 11
paket-stranica ne ispadnu međusobno nekonzistentne u zavisnosti od toga koja
sesija bota koju pravi:

- Tačan HTML skelet za paket-stranicu (koji delovi se kopiraju 1:1 iz
  `index.html`, koji su novi)
- Konkretan JSON-LD `Service` šablon po paketu (cene računate direktno iz
  `pricing.json` `cena_broj`, ne ručno)
- Breadcrumb + CTA mehanizam: `?paket=<slug>` query parametar koji predizabere
  paket u kontakt formi na povratku na početnu
- Zahtevi pristupačnosti za galerija-lightbox (focus trap, ARIA, tastatura,
  `prefers-reduced-motion`) — eksplicitno, jer sajt trenutno ima Lighthouse
  Accessibility 100 i to ne sme da padne novom komponentom
- Konvencija imenovanja/veličine slika za kad prave fotografije stignu
- Tačna definicija "gotovo je kad..." za svaki pod-korak (7.0, pilot, ostatak,
  galerija) — uključujući proveru da build skripta ne menja postojeći
  `index.html` neočekivano (git diff mora biti prazan posle prvog build-a)

### 4) ROADMAP.md i ARHITEKTURA.md ažurirani

`Faza 7.0` sad pokazuje šta je već gotovo (`data/pricing.json`,
`data/gallery.json`, spec fajl) i šta ostaje (`data/opisi.json` za marketing
tekst po paketu, `build_pages.py` skripta). ARHITEKTURA.md upućuje na novi spec
fajl.

## Namerno NIJE urađeno u ovoj sesiji

- **Nijedna paket-stranica ni galerija stranica.** Korisnikov zahtev je bio
  "nastavi sa izradom PLANA" — ne "napravi stranice". `build_pages.py` i
  stvarni HTML izlaz ostaju posao bota, po redosledu iz ROADMAP.md.
- **`data/opisi.json`** (prošireni marketing tekst po paketu) — ovo namerno
  ostaje botu, jer taj tekst treba pažljivo pisati i ići na pregled čoveku
  pre nego što ide live, ne generisati mehanički u istoj sesiji gde se pravi
  tehnička infrastruktura.

## Šta i dalje čeka na čoveka (nepromenjeno + novo)

1. Formspree nalog, businessplan lozinka, Calendly odluka, .ch domena, tačna
   adresa ateljea — sve kao pre.
2. **Novo:** kad bot napravi `data/opisi.json` nacrt teksta, treba pregled pre
   nego što ide live.
3. **Novo:** kad bot napravi pilot paket-stranicu (Kindergeburtstage),
   potreban je vizuelni pregled/odobrenje pre replikacije na preostalih 10.
4. I dalje: bar 15-20 pravih fotografija ateljea za galeriju.
