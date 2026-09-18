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
      (134/134 na index.html, 158/158 na businessplan/index.html)
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
- [ ] Provera linkova, tipfelera (DE i EN), i da `mailto:` link ima ispravnu
      email adresu — linkovi/anchor-i provereni automatski (svi rade), tipfeleri
      NISU rucno citani rec-po-rec, ostaje otvoreno
- [ ] Provera pristupacnosti (accessibility): kontrast boja, `alt` tekstovi,
      tab-navigacija kroz formu i dugmad, `prefers-reduced-motion` ponasanje
      (vec je implementirano — samo potvrditi da radi). Osnovna provera uradjena
      (nema slika bez `alt`, nema duplih `id`-ova), puna accessibility revizija
      (kontrast, tab-order, screen reader) NIJE radjena
- [ ] Performance provera (Lighthouse ili slicno) — cilj: 90+ na Performance i SEO

## Faza 3 — Prosirenje paketa (BOT)

- [x] Dodati tier strukturu (Basic / Advance / All Inclusive) i za preostale
      kategorije koje trenutno imaju samo jednu cenu: Grundangebot, Solo-Abend
      (Offenes Atelier), Familie/Paare/Senioren, Plus-Angebot, Geschenkgutscheine,
      Ferien-Workshops. Koristiti isti `.tiers`/`.tier` CSS obrazac kao postojecih
      5 kategorija (vidi `docs/ARHITEKTURA.md`). Uradjeno 2026-09-18 — svih 11
      paketa sada ima 3 tier-a na marketing stranici.
- [ ] Razmotriti pravi upitni formular (umesto samo `mailto:`) — npr. Formspree
      (besplatan tier, bez sopstvenog servera) koji salje upit direktno na mail
- [ ] Istraziti opciju pravog booking/kalendar sistema (npr. Calendly embed) za
      "Termin anfragen" — SAMO istraziti i predloziti, ne implementirati bez
      dogovora, jer to je poslovna odluka (placanje, provizija, itd.)

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

---

**Napomena za bota:** faze 1-3 se mogu raditi paralelno gde nema zavisnosti (npr.
Faza 2 ne ceka Fazu 1). Faza 1 stavke koje trazes od coveka (GitHub repo, domena)
BLOKIRAJU deploy, ali ne blokiraju rad na sadrzaju/kvalitetu (Faza 2, 3). Ako nesto
u ovom roadmapu vise nije tacno (npr. cene su vec finalizovane, ili je korisnik
promenio smer), STANI i pitaj umesto da nastavis sa zastarelim planom.
