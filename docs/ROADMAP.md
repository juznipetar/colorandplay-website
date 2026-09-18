# Color and Play — Website Roadmap

> Ovaj fajl prati konvenciju "roadmap rezima" (agent prati docs/ROADMAP.md; kad nema
> otvorenog zadatka, istrazuje i planira sledeci korak). Svaka stavka ima: ko je radi
> (COVEK / BOT), status, i jasnu definiciju "gotovo je kad...".
>
> Prati se preporuceni redosled faza odozgo na dole. BOT preskace stavke oznacene
> COVEK i prelazi na sledecu BOT stavku bez blokiranja celog toka.
>
> **Model: koristi ISKLJUCIVO Composer 2.5 za sav rad na ovom projektu** (vidi
> `docs/BOT-INSTRUKCIJE.md`, sekcija "OBAVEZNO — model", za pun detalj).

## Faza 0 — Fondacija (GOTOVO)

- [x] Poslovni plan za vlasnika lokala (Artifact + 2× PDF, DE/EN) — v5, sa Paket-Portfolio 2.1
- [x] Javna marketing stranica `index.html` — v1 (osnovna verzija)
- [x] Javna marketing stranica `index.html` — v2 (premium ton, tier paketi, animacije, count-up statistika)
- [x] Zasticena stranica `businessplan/index.html` (client-side lozinka + noindex)
- [x] `robots.txt`, `DEPLOY.md`

(Napomena o putanjama: ovaj repo nema `site/` podfolder — sve je na root nivou.
Vidi `docs/ARHITEKTURA.md` "Struktura fajlova" za objasnjenje zasto se `site/`
ipak pominje u starijim beleskama i u cloud dev projektu.)

## Faza 1 — Deploy & infrastruktura

- [x] **BOT:** GitHub repo napravljen (`juznipetar/colorandplay-website`, public),
      repo sadrzaj pushovan na `main`, GitHub Pages ukljucen i verifikovan (HTTP 200).
      Live na `https://juznipetar.github.io/colorandplay-website/`. Uradjeno
      direktno iz cloud sesije preko Desktop Commander-a (vec autentifikovan
      `gh` CLI nadjen na racunaru) — nije trazilo COVEK korak.
- [ ] **COVEK:** Kupiti .ch domenu na 1 godinu (preporuka: Hostpoint ili Infomaniak)
- [ ] **BOT (posle domene):** Napraviti `CNAME` fajl u root-u sa kupljenom domenom,
      uputiti korisnika koje DNS zapise da doda kod registrara (vidi DEPLOY.md
      korak 4). Ukljuciti "Enforce HTTPS" u Settings → Pages.
- [ ] **BOT:** Promeniti pristupni kod za businessplan stranicu sa placeholder-a
      `ColorPlay2026` na nesto sto Suzana/Petar odaberu (menja se u `build_site.py`,
      pa se skripta ponovo pokrene). Gotovo je kad je stari kod vise ne radi.
      I dalje otvoreno — repo je public, pa je hash trenutno vidljiv u izvornom
      kodu (view-source), samo hash ne plaintext, ali svejedno promeniti pre
      slanja linka Aligu.
- [ ] **BOT (opciono, jaca zastita):** Podesiti Cloudflare (besplatno) ispred GitHub
      Pages-a i Cloudflare Access na putanji `/businessplan/*` sa pravim
      email-based login-om. Vidi napomenu u `DEPLOY.md` sekcija 6.

## Faza 2 — Kvalitet i tehnicka higijena (BOT, samostalno)

- [x] Dodati `favicon.ico` / `favicon.svg` / `apple-touch-icon` (brend dot-logo u
      teal/gold, generisan sa PIL — teal zaobljeni kvadrat + gold tacka)
- [x] Dodati Open Graph i Twitter Card meta tagove (`og:title`, `og:description`,
      `og:image` [custom 1200×630 slika], `twitter:card`) u `<head>` oba fajla
- [x] Dodati `sitemap.xml` za `index.html` (businessplan stranica NE ide u
      sitemap — ostaje van indeksiranja), i referencu na njega u `robots.txt`
- [x] Provera i18n parova — skripta `check_i18n.py` (u repo root-u) proverava da
      svaki `data-lang="de"` ima par `data-lang="en"` i obrnuto. Oba fajla OK
      (188/188 na index.html, 158/158 na businessplan/index.html)
- [x] **Bug nadjen i ispravljen (deep check 2026-09-18):** `build_site.py` je
      ubacivao `<title>`, `<meta name="description">`, `<meta name="robots"
      content="noindex,nofollow">` i font `<link>`-ove direktno u `<body>`
      umesto u `<head>` — jer `pitch.html` (izvor za Artifact) je "goli" fragment
      bez `<head>`/`<body>` strukture, a skripta ga je samo omotala bez pravog
      razdvajanja. Najvaznija posledica: `noindex` meta tag NIJE bio pouzdano
      u `<head>` gde ga crawleri ocekuju — bas na stranici cija je cela svrha da
      ostane van pretrage. Ispravljeno: `build_site.py` sada eksplicitno deli
      fragment na head-deo i body-deo. Verifikovano sa `tidy -e` (HTML5
      validator) — čisto na oba fajla, i sa Playwright testom da `noindex` meta
      sad postoji u `<head>` i da lozinka-gate i dalje radi ispravno.
- [x] Uklonjen slucajan `Claude outputs/colorandplay-site.zip` fajl iz git repo-a
      (ostao je u folderu od ranijeg preuzimanja, `git add -A` ga je slucajno
      pokupio u prvi deploy commit) — dodat `.gitignore` da se to ne ponovi.
- [x] Provera linkova, tipfelera (DE i EN), i da `mailto:` link ima ispravnu
      email adresu — rucno procitan vidljiv DE/EN marketing copy na `index.html`
      (jedan jasan DE ispravak: „vom frühen Nachmittag“); `mailto:` i tekst u
      businessplan-u konzistentno koriste `suzana.androvic@gmail.com`
- [x] Provera pristupacnosti (accessibility): kontrast boja (minimalne lokalne
      korekcije `--ink-faint`, kicker na `--ink-soft`), `alt`/dekorativni elementi,
      tab-navigacija i `:focus-visible`, heading redosled (h4→h3), skip link,
      ARIA na lang toggle i businessplan gate, `prefers-reduced-motion` prosiren
      (pulse/glow). Lighthouse Accessibility: 94→100 (lokalno posle fix-a).
      Odlozeno: globalna `--sage`/`--gold` odluka ako se koriste za tekst.
- [x] Performance provera (Lighthouse) — cilj 90+ Performance i SEO: live pre
      91/100, lokalno posle 99/100 (async fonts, manje font-weight varijanti).
- [x] **BOT:** Primena Playful Pastel / Manus palete sa
      [bojaprica-ewkzvomb.manus.space](https://bojaprica-ewkzvomb.manus.space)
      — hex map u `:root` na `index.html` i `businessplan/index.html`, dark mode
      usklađen, lokalne WCAG korekcije (CTA/teal tekst). Detalji u
      `docs/izvestaji/05-izvestaj-sesije-2026-09.md` (sekcija Paleta).
- [x] **Deep polish (sesija 05, 2026-09-18):** scroll-margin za sticky nav,
      mobilna nav traka, validan jedan `<legend>`, forma field-level greške,
      trustbar cena bez „CHF 0“ flash-a, gate error clear on type, reduced-motion
      hover transform. Detalji: `docs/izvestaji/05-izvestaj-sesije-2026-09.md`
      (sekcija Deep polish).

## Faza 3 — Prosirenje paketa (BOT)

- [x] Dodati tier strukturu (Basic / Advance / All Inclusive) i za preostale
      kategorije koje trenutno imaju samo jednu cenu: Grundangebot, Solo-Abend
      (Offenes Atelier), Familie/Paare/Senioren, Plus-Angebot, Geschenkgutscheine,
      Ferien-Workshops. Koristiti isti `.tiers`/`.tier` CSS obrazac kao postojecih
      5 kategorija (vidi `docs/ARHITEKTURA.md`). Uradjeno 2026-09-18 — svih 11
      paketa sada ima 3 tier-a na marketing stranici.
- [x] Razmotriti pravi upitni formular (umesto samo `mailto:`) — Formspree
      kontakt forma u `#kontakt` (name, email, message, optional phone), placeholder
      `YOUR_FORMSPREE_ID`, mailto fallback; uputstvo u `DEPLOY.md` sekcija 7
- [x] Istraziti opciju pravog booking/kalendar sistema (npr. Calendly embed) za
      "Termin anfragen" — predlog u `docs/predlog-calendly.md` (bez embed-a na sajtu)

## Faza 4 — Jedan izvor istine za cene (BOT, tehnicki dug)

Trenutno cene i paketi postoje rucno upisani na DVA mesta: `index.html`
(marketing stranica) i `pitch.html` → `businessplan/index.html` (biznis plan
za vlasnika). Kad se prave/finalne cene odrede, lako je da se zaboravi izmeniti oba
mesta i da se brojevi razmimoilaze.

- [ ] Napraviti `data/pricing.json` kao jedini izvor istine za sve pakete/tier-ove
- [ ] Prepraviti `build_site.py` (i ekvivalent za marketing stranicu) da generisu
      HTML iz tog JSON-a, umesto rucno kucanog HTML-a
- [ ] Gotovo je kad izmena jedne cene u `pricing.json` + ponovno pokretanje build
      skripte azurira I marketing stranicu I businessplan stranicu konzistentno

## Faza 5 — Van trenutnog obima (samo za buducnost, ne raditi bez eksplicitnog OK)

- Pravi online booking + placanje (zahteva pravi backend/servis, npr. Stripe +
  kalendar sistem — ozbiljna odluka o troskovima i provizijama)
- CRM / lista klijenata
- Email marketing (newsletter prijava)

## Faza 6 — Kreativne nove ideje (predlog, sesija 06, 2026-09-18)

Posle deep-check-a sesija 02-05 (sve potvrdjeno live, bez regresija — vidi
`docs/izvestaji/06-izvestaj-sesije-2026-09.md`). Ideje ispod NISU obavezne —
predlog je da BOT uzme (a) odmah, jednu po jednu, bez cekanja na coveka, a (b)
samo posle eksplicitnog OK od Petra/Suzane.

### (a) BOT moze odmah, bez zavisnosti

- [x] **Favicon/OG slike usaglasene sa novom paletom** — `favicon-16/32/192/512.png`,
      `favicon.ico`, `apple-touch-icon.png`, `og-image.png` su i dalje koristili
      staru teal/gold paletu iako je `favicon.svg` i sajt vec presli na Playful
      Pastel (sesija 05). Regenerisano i zamenjeno u ovoj sesiji (cloud agent,
      PIL) — sad su svi na `--teal #0b8e8b` / `--gold #f5cb50` / mist halo.
- [ ] **Impressum + Datenschutzerklaerung stranice.** Za komercijalni sajt u
      Svajcarskoj ovo nije opciono (OR/UWG identifikacija firme + revDSG za
      podatke koje kontakt forma/Formspree obradjuje). Predlog: `/impressum/`
      i `/datenschutz/` (DE/EN), link u footer-u oba HTML fajla. Sadrzaj:
      pravno ime, adresa, email, ko obradjuje podatke (Formspree, GitHub
      Pages), koja prava korisnik ima. Bot moze napisati nacrt teksta, ali
      **pravno ime firme / tacna adresa mora potvrditi covek** pre nego sto
      ide live — dodati kao vidljiv `[TODO: potvrditi]` placeholder ako fali.
- [ ] **JSON-LD structured data (schema.org LocalBusiness)** na `index.html` —
      ime, adresa (Baar, Kanton Zug), tip usluge, cenovni raspon, radno vreme
      ako postoji. Besplatan lokalni SEO potez (Google lokalni rezultati za
      "Kindergeburtstag Baar", "Malatelier Zug" i sl.), ne dira vizuelni dizajn.
- [x] **Custom 404 stranica** — `404.html` u root-u, DE/EN (data-lang + lang
      toggle), Playful Pastel stil, link `./` na start. GitHub Pages automatski
      servira za nepoznate putanje.
- [ ] **"Koji paket odgovara nama?" mini-kviz** — 3-4 kratka pitanja (broj
      osoba, prilika: rodjendan/firma/spoj, budzet) → JS bez backend-a scroll-uje
      i istice preporuceni tier medju postojecih 11 paketa. Igrivo, uklapa se u
      "Play" brend ton, nula rizika po postojeci sadrzaj (cist dodatak, ne
      menja cene/tekst).
- [x] **Print stylesheet za `businessplan/index.html`** — `@media print` sakriva
      topbar, gate, lang toggle i livebadge; teal/tamni tekst za B&W ispis;
      tabele i poglavlja sa `break-inside: avoid`.
- [ ] **Vizuelni preview generator za poklon vaucer** (Geschenkgutscheine paket
      vec postoji u cenovniku) — mali klijentski prikaz (ime primaoca, iznos,
      brend dizajn) koji se moze odstampati/sacuvati kao PDF pre nego sto se
      posalje. Direktno vezano za postojeci prihodni paket, ne izmisljena
      funkcija.

### (b) Ceka eksplicitno OK od Petra/Suzane pre nego sto se radi

- **Analytics** (npr. Plausible ili GoatCounter — privacy-friendly, bez
  cookie banner-a) — trenutno nema nikakve vidljivosti u saobracaj. Treba
  odluka o alatu + nalog.
- **Testimonials/recenzije sekcija** — samo ako Suzana ima stvarne izjave
  klijenata za deljenje. Bot ne sme izmisljati recenzije ni citate.
- **Instagram/social embed** — treba pravi handle/nalog da se poveze.
- **Blog/News sekcija** (sezonski workshopi, akcije) — SEO korisno, ali
  zahteva redovan sadrzaj; pitanje da li Suzana zeli tu obavezu.
- **Francuski jezik (FR)** — Svajcarska ima 4 jezika; Baar/Zug je nemacko
  govorno podrucje pa nizak prioritet, ali ako cilja i frankofone
  turiste/expate u okolini Ciriha, treci jezik je moguc dodatak.

## Faza 7 — Galerija + pojedinacna stranica za svaki paket (VELIKO prosirenje — korisnikova originalna vizija, sesija 08, 2026-09-18)

Korisnik je eksplicitno trazio da sajt bude kompleksniji: (1) prava galerija
slika, (2) svaki od 11 paketa dobija SVOJU stranicu sa slikama i detaljnim
objasnjenjem, ne samo karticu na pocetnoj. Ovo nije mala izmena — sajt prelazi
iz jednostranicnog (sve na `index.html` sa anchor-ima) u pravi vise-stranicni
sajt (~12+ novih HTML fajlova). Zbog obima, raditi INKREMENTALNO po redosledu
ispod, ne sve odjednom u jednom PR-u.

### 7.0 — Preduslov, mora ici PRVO: Faza 4 (data/pricing.json + lokalni build sistem)

Do sada je Faza 4 bila "tehnicki dug, radi kad ima vremena" — sada je BLOKIRAJUCI
preduslov. Razlog: cim postoji 11 paket-stranica + pocetna, cena/tier podatak
postoji na **12 mesta** koja se moraju rucno drzati sinhronizovanim — bez jednog
izvora istine je pitanje vremena kad ce se brojevi razmimoici.

Preporuceni pristup (u duhu vec postojeceg `build_site.py` obrasca za
businessplan, ne uvodi se nista fundamentalno novo):
- `data/pricing.json` — jedan zapis po paketu: slug, naziv (DE/EN), tag/uslov,
  3 tier-a (naziv, cena, per-jedinica, lista pogodnosti DE/EN, da li je "popular")
- `data/gallery.json` — jedan zapis po slici: fajl, alt tekst (DE/EN), tag-ovi
  (koji paket/paketi je slika relevantna za)
- `templates/` folder sa deljenim delovima (nav/header/footer/script) + template
  za paket-stranicu — prost Python string-template ili Jinja2, ne pravi framework
- Skripta (npr. `build_pages.py`) koja iz JSON-a + template-a generise:
  - `.signature`/`.tiers` blokove na `index.html` (pakete sekcija)
  - svih 11 `/pakete/<slug>/index.html` stranica
  - `/galerie/index.html`
  - `sitemap.xml` (dodaje nove URL-ove automatski)

**Vazna napomena o principu iz ARHITEKTURA.md** ("nema build koraka, nema
framework-a"): ovo se NE krsi. Princip se odnosi na to sta GitHub Pages servira
— i dalje cisti staticki HTML, nula pokretnih delova na serveru. Build skripta
se pokrece LOKALNO (na racunaru bota) PRE `git commit`, generisani HTML se
commituje kao obican fajl kao i do sad. Ovo JESTE ona "eksplicitna odluka" na
koju ARHITEKTURA.md upucuje kad sajt naraste dovoljno da opravda automatizaciju
— sad je taj trenutak.

### 7.1 — Galerija (`/galerie/index.html`)

- Responzivna mreza fotografija + lightbox (klik za uvecanje), lazy-loading,
  alt tekst DE/EN po slici (iz `data/gallery.json`)
- Link u glavnoj navigaciji (topbar), DE "Galerie" / EN "Gallery"
- **KLJUCNI OTVOREN PROBLEM — prave fotografije ateljea ne postoje jos.** Sajt
  trenutno nema nijednu pravu fotografiju (samo CSS/SVG dekoracije). Isti princip
  kao kod izmisljenih recenzija (vidi STROGE GRANICE u BOT-INSTRUKCIJE.md): **bot
  ne sme koristiti generican stock-foto materijal predstavljen kao da je iz
  pravog ateljea.** To bi bilo neposteno prema buducim mustarijama, isto kao
  lazna recenzija.
- Sta bot MOZE odmah bez pravih slika: kompletnu grid+lightbox infrastrukturu,
  sa jasno obelezenim placeholder pločicama (brend-stil dekorativni blob/boja
  motiv, isti posten "Folgt in Kürze" princip kao kod adrese) — tako da dodavanje
  pravih slika kasnije znaci samo: ubaci fajlove u `/assets/galerie/`, dodaj po
  jedan red u `data/gallery.json`, ponovo pokreni build skriptu. Nula izmena koda.
- Preporuka za coveka (upisati u izvestaj, ne odluciti sam): **bar 15-20 fotografija
  za pocetak** — enterijer ateljea, radionica u toku, gotovi radovi, grupe u akciji.
  Ne mora profesionalni foto-shoot, mogu i telefonom snimljene, bitno je da su
  prave.

### 7.2 — Pojedinacna stranica za svaki paket (`/pakete/<slug>/index.html`)

Predlozeni slug-ovi (11, redosled kao na pocetnoj):

| Paket | Slug |
|---|---|
| Kindergeburtstage | `kindergeburtstage` |
| Firmen & Teams | `firmen-teams` |
| Wine & Draw | `wine-draw` |
| Private Feiern | `private-feiern` |
| Art Club Mitgliedschaft | `art-club` |
| Grundangebot | `grundangebot` |
| Solo-Abend für Erwachsene | `solo-abend` |
| Familie · Paare · 60+ | `familie-paare-60plus` |
| Plus-Angebot | `plus-angebot` |
| Geschenkgutscheine | `geschenkgutscheine` |
| Ferien-Workshops | `ferien-workshops` |

Svaka stranica sadrzi:
- Hero slika relevantna za taj paket (iz galerije, po tag-u u `gallery.json`)
- Prosiren opis — detaljniji ablauf/agenda nego kratka kartica na pocetnoj
  (bot moze napisati NACRT na osnovu postojeceg teksta sa `index.html`, ali
  finalni ton/sadrzaj ide na pregled coveku pre nego sto ide live — isto pravilo
  kao za sav ostali marketing tekst)
- Tier tabela (Basic/Advance/All Inclusive) — **ucitana iz `pricing.json`, ne
  rucno prekucana** (to je cela poenta 7.0)
- Mini-galerija (3-6 slika specificnih za taj paket)
- Opciono: 2-4 FAQ stavke specificne za paket
- CTA dugme nazad na `index.html#kontakt`, sa paketom vec predizabranim (npr.
  `?paket=kindergeburtstage` query parametar koji JS na pocetnoj cita i popuni
  polje u formi)
- Breadcrumb nazad: "‹ Zuruck zu allen Paketen" → `index.html#pakete`
- Isti i18n mehanizam (DE/EN parovi) kao ostatak sajta — `check_i18n.py` mora
  proci i za ove nove fajlove
- Sopstveni `<title>`/`<meta description>` po paketu (npr. "Kindergeburtstag
  Malen in Baar | Color and Play") — realan SEO dobitak za long-tail pretrage,
  nesto sto jedna zajednicka pocetna stranica ne moze da pokrije

### 7.3 — Povezivanje sa postojecim sajtom

- Svaka `.signature`/`.tiers` grupa na `index.html#pakete` dobija dugme "Mehr
  erfahren" / "Learn more" → odgovarajuca `/pakete/<slug>/` stranica
- Topbar navigacija dobija link "Galerie"/"Gallery"
- `sitemap.xml` prosiriti sa svih 12 novih URL-ova (11 paket stranica + galerija)
- Postojeca `404.html` (Faza 6a) automatski pokriva slucaj los kucanog URL-a
  novih stranica — samo proveriti da linkovi rade pre merge-a

### 7.4 — Sta bot moze odmah vs. sta ceka coveka

**BOT moze odmah, redosledom:**
1. `data/pricing.json` + `data/gallery.json` + build skripta (7.0) — preduslov
2. HTML/CSS template za paket-stranicu, testiran na JEDNOM paketu kao pilot
   (predlog: Kindergeburtstage, najjaci postojeci paket) — cim covek odobri
   izgled pilota, repliciraj na preostalih 10
3. Galerija infrastruktura (7.1) sa placeholder plocicama
4. Breadcrumb/navigacija/sitemap prosirenje (7.3)

**Ceka coveka:**
- Prave fotografije (7.1) — najveci blokator za finalni izgled, ali bot ne
  treba da ceka na njih da pocne 7.0-7.3 sa placeholder-ima
- Odobrenje prosirenog teksta/opisa po paketu ako se menja ton u odnosu na
  postojeci sadrzaj

**Napomena o obimu:** ovo je realno vise sesija posla, ne jedna — ne pokusavati
zavrsiti sve u jednom PR-u. Prvo 7.0 (preduslov), zatim 1 pilot stranica na
odobrenje, tek onda ostatak + galerija.

---

**Napomena za bota:** faze 1-3 se mogu raditi paralelno gde nema zavisnosti (npr.
Faza 2 ne ceka Fazu 1). Faza 1 stavke koje trazes od coveka (GitHub repo, domena)
BLOKIRAJU deploy, ali ne blokiraju rad na sadrzaju/kvalitetu (Faza 2, 3). Ako nesto
u ovom roadmapu vise nije tacno (npr. cene su vec finalizovane, ili je korisnik
promenio smer), STANI i pitaj umesto da nastavis sa zastarelim planom.
