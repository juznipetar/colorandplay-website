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
- [ ] **Custom 404 stranica** — GitHub Pages trenutno servira default prazan
      404. Kratka DE/EN stranica u brend stilu ("Diese Seite gibt's nicht —
      zurueck zur Startseite") sa linkom na `/`. Mala stvar, ali losi prvi
      utisak kod pokvarenog linka ili tipfelera u URL-u.
- [ ] **"Koji paket odgovara nama?" mini-kviz** — 3-4 kratka pitanja (broj
      osoba, prilika: rodjendan/firma/spoj, budzet) → JS bez backend-a scroll-uje
      i istice preporuceni tier medju postojecih 11 paketa. Igrivo, uklapa se u
      "Play" brend ton, nula rizika po postojeci sadrzaj (cist dodatak, ne
      menja cene/tekst).
- [ ] **Print stylesheet za `businessplan/index.html`** — `@media print` da
      Herr Alig moze cist da odstampa/PDF-uje stranicu za sastanak (bez topbar-a,
      gate-a, dekorativnih blob-ova; teal umesto svetlih boja za bolji crno-belo
      ispis).
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

---

**Napomena za bota:** faze 1-3 se mogu raditi paralelno gde nema zavisnosti (npr.
Faza 2 ne ceka Fazu 1). Faza 1 stavke koje trazes od coveka (GitHub repo, domena)
BLOKIRAJU deploy, ali ne blokiraju rad na sadrzaju/kvalitetu (Faza 2, 3). Ako nesto
u ovom roadmapu vise nije tacno (npr. cene su vec finalizovane, ili je korisnik
promenio smer), STANI i pitaj umesto da nastavis sa zastarelim planom.
