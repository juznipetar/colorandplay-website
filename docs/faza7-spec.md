# Faza 7 — Tehnicka specifikacija (galerija + pakete stranice)

Ovaj fajl je tehnicki pratilac za `docs/ROADMAP.md` Faza 7 — daje TACNE sablone,
seme podataka i isecke koda, tako da 11 paket-stranica ispadnu medjusobno
konzistentne bez obzira ko (koja sesija bota) ih pravi. `ROADMAP.md` ostaje
izvor istine za REDOSLED i status; ovaj fajl je izvor istine za TACAN OBLIK.

Napravljeno u sesiji 08 (cloud agent) kao deo "budi pametan, nastavi plan"
zahteva — `data/pricing.json` je vec popunjen pravim, live podacima (ekstraktovano
direktno iz `index.html` 18.09.2026, ne rucno prekucano — nula rizika od greske
u transkripciji). Bot treba da ga PROVERI (brzo, ne mora ponovo da kuca) pre
upotrebe u build skripti.

---

## 1) `data/pricing.json` — vec napravljen, pravi podaci

Jedan zapis po paketu (11 ukupno), redosled isti kao na `index.html#pakete`.
Struktura (videti sam fajl za kompletan sadrzaj):

```json
{
  "pakete": [
    {
      "slug": "kindergeburtstage",
      "naziv_de": "Kindergeburtstage",
      "naziv_en": "Kids' Birthdays",
      "tag_de": "4–12 Jahre · bis 10 Kinder",
      "tag_en": "Ages 4–12 · up to 10 kids",
      "tiers": [
        {
          "naziv": "Basic",
          "cena": "CHF 390",
          "cena_broj": 390,
          "je_dodatak": false,
          "jedinica_de": "",
          "jedinica_en": "",
          "popular": false,
          "pogodnosti": [
            {"de": "90 Minuten, bis 8 Kinder", "en": "90 minutes, up to 8 kids"}
          ]
        }
      ]
    }
  ]
}
```

- `cena_broj` — cist broj za buduce racunanje/sortiranje (npr. `priceRange` u
  JSON-LD, vidi sekciju 5).
- `je_dodatak` — `true` samo za Plus-Angebot (cene sa `+` prefiksom, oznacavaju
  dodatak na osnovnu cenu drugog paketa, ne samostalnu cenu).
- `jedinica_de`/`jedinica_en` — prazno kad je cena flat (npr. Kindergeburtstage,
  Geschenkgutscheine), inace ` / Pers.`, ` / Monat`, ` / Tag / Kind` itd.
- `popular` — `true` na tacno jednom tier-u po paketu (uvek srednji, "Advance")
  — koristi se za `.tier.popular` CSS klasu, isto kao na pocetnoj.

**VAZNO:** kad se cena promeni bilo gde (pocetna ILI paket-stranica), menja se
SAMO ovaj JSON, pa se build skripta ponovo pokrene. Rucno menjanje cene direktno
u generisanom HTML-u se GUBI pri sledecem build-u — to je cela poenta.

## 2) `data/gallery.json` — vec napravljen, prazna semа spremna

```json
{
  "slike": [
    {
      "fajl": "assets/galerie/primer-naziv-fajla.jpg",
      "alt_de": "Kratak opis na nemackom",
      "alt_en": "Short description in English",
      "tagovi": ["kindergeburtstage", "atelje"],
      "je_hero_za": null
    }
  ]
}
```

- `tagovi` — isti slug-ovi kao u `pricing.json` (koja slika ide na koju
  paket-stranicu) plus opsti tagovi za glavnu galeriju: `atelje`, `radionica`,
  `gotovi-radovi`, `grupa`.
- `je_hero_za` — slug paketa ako je ova slika hero-slika te paket-stranice,
  inace `null`. Najvise JEDNA slika po paketu sme imati `je_hero_za` postavljen
  na taj slug (build skripta treba da ovo proveri i javi gresku ako ima dve).
- **Fajl je namerno prazan** (`slike: []`) dok prave fotografije ne stignu —
  vidi STROGE GRANICE u BOT-INSTRUKCIJE.md. Placeholder prikaz (sekcija 6 ispod)
  radi i bez ijednog zapisa ovde.

## 3) HTML struktura paket-stranice (`/pakete/<slug>/index.html`)

Svaka stranica je i dalje **potpuno samostalan fajl** (isti princip kao
`index.html`/`businessplan/index.html` — nema shared CSS/JS fajla). Prakticno:

1. Kopiraj CEO `<head>` blok (ukljucujuci `<style>` sa `:root` promenljivama)
   iz `index.html` — identican dizajn sistem, samo promeni `<title>`/
   `<meta description>` (vidi sekciju 5) i relativne putanje do favicon-a
   (`../../favicon.svg` umesto `favicon.svg`, jer je stranica dva nivoa dublje).
2. Kopiraj topbar/nav iz `index.html` (linkovi postaju `../../index.html#pakete`
   itd. — relativni nazad na pocetnu).
3. Novi sadrzaj (specifican za ovu stranicu):

```html
<main id="main">
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <a href="../../index.html#pakete">
      <span class="i18n" data-lang="de">‹ Zurück zu allen Paketen</span>
      <span class="i18n" data-lang="en" hidden>‹ Back to all packages</span>
    </a>
  </nav>

  <section class="block wrap reveal pkg-hero">
    <img class="pkg-hero-img" src="../../assets/galerie/PLACEHOLDER.jpg"
         alt="" width="1200" height="675" loading="eager">
    <!-- alt="" prazan namerno dok nema prave hero slike + je_hero_za u gallery.json;
         kad ima prave slike, alt dolazi iz gallery.json alt_de/alt_en -->
    <span class="kicker i18n" data-lang="de">{{ tag_de }}</span>
    <span class="kicker i18n" data-lang="en" hidden>{{ tag_en }}</span>
    <h1 class="i18n" data-lang="de">{{ naziv_de }}</h1>
    <h1 class="i18n" data-lang="en" hidden>{{ naziv_en }}</h1>
    <p class="lead i18n" data-lang="de">{{ prosireni_opis_de }}</p>
    <p class="lead i18n" data-lang="en" hidden>{{ prosireni_opis_en }}</p>
  </section>

  <section class="block wrap reveal">
    <div class="tiers reveal-stagger reveal">
      <!-- identican .tier markup kao na pocetnoj, generisan iz pricing.json
           za ovaj slug — kopiraj obrazac iz ARHITEKTURA.md "Tier pricing
           komponenta" -->
    </div>
  </section>

  <section class="block wrap reveal pkg-gallery">
    <h2 class="i18n" data-lang="de">Impressionen</h2>
    <h2 class="i18n" data-lang="en" hidden>Impressions</h2>
    <!-- mini-galerija: slike iz gallery.json gde tagovi sadrzi ovaj slug,
         max 6, isti grid/lightbox obrazac kao glavna galerija (sekcija 6) -->
  </section>

  <section class="block wrap reveal pkg-cta">
    <a class="cta" href="../../index.html?paket={{ slug }}#kontakt">
      <span class="i18n" data-lang="de">Jetzt anfragen</span>
      <span class="i18n" data-lang="en" hidden>Enquire now</span>
    </a>
  </section>
</main>
```

`{{ ... }}` oznake su mesta koja build skripta popunjava iz `pricing.json`
(ili rucno pisanog opisa — vidi sekciju 4). Ne moraju bukvalno biti Jinja2
sintaksa, to je samo oznaka mesta u ovom spec dokumentu.

## 4) Prosireni opis po paketu — NIJE u pricing.json, pise se posebno

`pricing.json` namerno NEMA polje za dugi marketing opis — to je tekst koji
treba pazljivo napisati (i odobriti kod coveka), ne generisati mehanicki iz
cena. Predlog: `data/opisi.json`, jedan zapis po slugu:

```json
{
  "kindergeburtstage": {
    "opis_de": "...",
    "opis_en": "...",
    "faq": [
      {"pitanje_de": "...", "odgovor_de": "...", "pitanje_en": "...", "odgovor_en": "..."}
    ]
  }
}
```

Bot pise NACRT ovog teksta (na osnovu postojeceg `tag_de`/`tag_en` i
`pogodnosti` iz `pricing.json`, prosiruje u 2-4 recenice), ali ide u
`docs/izvestaji/` na pregled coveku PRE nego sto se stranica pusti live —
isto pravilo kao sav ostali marketing tekst (vidi BOT-INSTRUKCIJE.md).

## 5) SEO — `<title>`/meta description/JSON-LD po paket-stranici

```html
<title>{{ naziv_de }} in Baar | Color and Play</title>
<meta name="description" content="{{ naziv_de }} bei Color and Play in Baar — {{ tag_de }}. Ab {{ najniza_cena }}.">
```

JSON-LD (isti obrazac kao `LocalBusiness` na pocetnoj, vec live — vidi
`docs/izvestaji/07-izvestaj-sesije-2026-09.md`), dodatno `Service` po
paket-stranici:

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "{{ naziv_de }}",
  "provider": {"@type": "LocalBusiness", "name": "Color and Play"},
  "areaServed": "Baar, Kanton Zug",
  "offers": {
    "@type": "AggregateOffer",
    "priceCurrency": "CHF",
    "lowPrice": "{{ min cena_broj medju tier-ovima }}",
    "highPrice": "{{ max cena_broj medju tier-ovima }}"
  }
}
```

`lowPrice`/`highPrice` se racunaju direktno iz `pricing.json` `cena_broj` polja
— nista rucno.

## 6) Galerija — grid + lightbox, pristupacnost (OBAVEZNO, ne opciono)

Sajt trenutno ima Lighthouse Accessibility 100 (sesija 03) — nova komponenta
NE SME to da pokvari. Minimalni zahtevi:

- Svaka slika u gridu je `<button>` (ne `<img>` direktno klikabilna) sa
  `aria-label` = alt tekst te slike, otvara lightbox.
- Lightbox je `<dialog>` ili `<div role="dialog" aria-modal="true">` sa fokusom
  zarobljenim unutra dok je otvoren (focus trap), `Escape` zatvara, `Tab`
  ne izlazi napolje.
- Strelice levo/desno (ako ih ima) su prava dugmad sa `aria-label`
  ("Vorheriges Bild"/"Nächstes Bild" DE, "Previous image"/"Next image" EN).
- Fokus se vraca na dugme koje je otvorilo lightbox kad se on zatvori.
- `prefers-reduced-motion` — lightbox otvaranje/zatvaranje bez animacije kad je
  ovo podeseno (isti obrazac kao ostatak sajta, vidi ARHITEKTURA.md
  "Animacije").
- Slike imaju `loading="lazy"` OSIM prve/hero slike u vidljivom delu (`eager`).
- Svaka `<img>` ima eksplicitan `width`/`height` (ili `aspect-ratio` u CSS)
  da se izbegne layout shift (CLS) — bitno za Lighthouse Performance (trenutno
  99, vidi sesija 03).

Placeholder stanje (dok `gallery.json` `slike` niz nema prave unose): prikazi
brend-stil dekorativne pločice (isti `.blob`/gradient motiv kao hero sekcija
na pocetnoj) sa tekstom DE "Fotos folgen in Kürze" / EN "Photos coming soon" —
NE prazan beli prostor, NE stock-foto.

## 7) Slike — format i konvencija imenovanja (za kad prave fotografije stignu)

- Format: original JPEG/HEIC sa telefona je OK kao ulaz; build skripta (ili
  bot rucno) konvertuje u `.webp` (manji fajl, Lighthouse Performance bonus)
  sa `.jpg` fallback-om ako treba (`<picture>` element) — nije obavezno za
  pocetak, samo preporuka ako vreme dozvoljava.
- Max sirina 1600px za hero slike, 800px za galerija-grid thumbnove — nema
  potrebe za vecim na web-u, samo usporava load.
- Naziv fajla: `<slug>-01.jpg`, `<slug>-02.jpg` za slike specificne za paket
  (npr. `kindergeburtstage-01.jpg`), ili `atelje-01.jpg`/`radionica-01.jpg` za
  opste. Lokacija: `/assets/galerie/`.

## 8) `sitemap.xml` — novi unosi

Jedan `<url>` blok po novoj stranici (11 paket-stranica + `/galerie/`), isti
obrazac kao postojeci unosi za `index.html`. `<priority>` predlog: `0.7` za
paket-stranice, `0.6` za galeriju (pocetna ostaje `1.0`).

## 9) Definicija "gotovo je kad..." za Fazu 7 (redom)

1. **7.0 gotovo kad:** `build_pages.py` postoji, cita `pricing.json` +
   `gallery.json` + `opisi.json`, i uspesno regenerise `.tiers` blokove na
   `index.html` IDENTICNE trenutnim (provera: `git diff` posle build-a na
   `index.html` je prazan/nula-linija — ako build promeni nesto neocekivano,
   znaci da skripta ne replicira postojeci HTML tacno, treba ispraviti pre
   nego sto se nastavi na paket-stranice).
2. **Pilot gotovo kad:** jedna paket-stranica (Kindergeburtstage) postoji,
   prolazi `check_i18n.py`, `tidy -e` bez pravih gresaka, Lighthouse
   Accessibility/Performance ne padaju ispod trenutnih (100/99), i covek je
   vizuelno odobrio izgled.
3. **Ostatak gotovo kad:** svih 11 paket-stranica postoji istim obrascem kao
   pilot, `sitemap.xml` azuriran, linkovi sa pocetne (`.signature` "Mehr
   erfahren" dugmad) rade, `404.html` testiran na namerno pogresnom URL-u.
4. **Galerija gotovo kad:** `/galerie/index.html` postoji sa grid/lightbox
   (radi i sa praznim `gallery.json` — placeholder stanje), link u nav-u radi.
