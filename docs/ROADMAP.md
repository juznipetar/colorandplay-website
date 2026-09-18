# Color and Play — Website Roadmap

> Ovaj fajl prati konvenciju "roadmap rezima" (agent prati docs/ROADMAP.md; kad nema
> otvorenog zadatka, istrazuje i planira sledeci korak). Svaka stavka ima: ko je radi
> (COVEK / BOT), status, i jasnu definiciju "gotovo je kad...".
>
> Prati se preporuceni redosled faza odozgo na dole. BOT preskace stavke oznacene
> COVEK i prelazi na sledecu BOT stavku bez blokiranja celog toka.

## Faza 0 — Fondacija (GOTOVO)

- [x] Poslovni plan za vlasnika lokala (Artifact + 2× PDF, DE/EN) — v5, sa Paket-Portfolio 2.1
- [x] Javna marketing stranica `site/index.html` — v1 (osnovna verzija)
- [x] Javna marketing stranica `site/index.html` — v2 (premium ton, tier paketi, animacije, count-up statistika)
- [x] Zasticena stranica `site/businessplan/index.html` (client-side lozinka + noindex)
- [x] `site/robots.txt`, `site/DEPLOY.md`

## Faza 1 — Deploy & infrastruktura

- [ ] **COVEK:** Napraviti GitHub repo (npr. `colorandplay-website`)
- [ ] **COVEK:** Kupiti .ch domenu na 1 godinu (preporuka: Hostpoint ili Infomaniak)
- [ ] **BOT:** Kad repo postoji — pushovati sadrzaj `site/` na `main` granu
      (vidi `site/DEPLOY.md` koraci 1-2). Gotovo je kad GitHub Pages URL
      (`https://<user>.github.io/<repo>/`) prikazuje javnu stranicu.
- [ ] **BOT (posle domene):** Napraviti `CNAME` fajl u root-u sa kupljenom domenom,
      uputiti korisnika koje DNS zapise da doda kod registrara (vidi DEPLOY.md
      korak 4). Ukljuciti "Enforce HTTPS" u Settings → Pages.
- [ ] **BOT:** Promeniti pristupni kod za businessplan stranicu sa placeholder-a
      `ColorPlay2026` na nesto sto Suzana/Petar odaberu (menja se u `build_site.py`,
      pa se skripta ponovo pokrene). Gotovo je kad je stari kod vise ne radi.
- [ ] **BOT (opciono, jaca zastita):** Podesiti Cloudflare (besplatno) ispred GitHub
      Pages-a i Cloudflare Access na putanji `/businessplan/*` sa pravim
      email-based login-om. Vidi napomenu u `DEPLOY.md` sekcija 6.

## Faza 2 — Kvalitet i tehnicka higijena (BOT, samostalno)

- [ ] Dodati `favicon.ico` / `apple-touch-icon` (brend dot-logo u teal/gold, trenutno
      sajt nema nikakvu ikonicu u tabu)
- [ ] Dodati Open Graph i Twitter Card meta tagove (`og:title`, `og:description`,
      `og:image`, `twitter:card`) u `<head>` oba fajla, da link lepo izgleda kad se
      deli u WhatsApp-u/Instagramu
- [ ] Dodati `sitemap.xml` za `site/index.html` (businessplan stranica NE ide u
      sitemap — ostaje van indeksiranja)
- [ ] Provera i18n parova: svaki element sa `data-lang="de"` mora imati par
      `data-lang="en"` i obrnuto — mali skript koji to proveri automatski i javi
      nesparene stringove
- [ ] Provera linkova, tipfelera (DE i EN), i da `mailto:` link ima ispravnu
      email adresu
- [ ] Provera pristupacnosti (accessibility): kontrast boja, `alt` tekstovi,
      tab-navigacija kroz formu i dugmad, `prefers-reduced-motion` ponasanje
      (vec je implementirano — samo potvrditi da radi)
- [ ] Performance provera (Lighthouse ili slicno) — cilj: 90+ na Performance i SEO

## Faza 3 — Prosirenje paketa (BOT)

- [ ] Dodati tier strukturu (Basic / Advance / All Inclusive) i za preostale
      kategorije koje trenutno imaju samo jednu cenu: Grundangebot, Solo-Abend
      (Offenes Atelier), Familie/Paare/Senioren, Plus-Angebot, Geschenkgutscheine,
      Ferien-Workshops. Koristiti isti `.tiers`/`.tier` CSS obrazac kao postojecih
      5 kategorija (vidi `docs/ARHITEKTURA.md`)
- [ ] Razmotriti pravi upitni formular (umesto samo `mailto:`) — npr. Formspree
      (besplatan tier, bez sopstvenog servera) koji salje upit direktno na mail
- [ ] Istraziti opciju pravog booking/kalendar sistema (npr. Calendly embed) za
      "Termin anfragen" — SAMO istraziti i predloziti, ne implementirati bez
      dogovora, jer to je poslovna odluka (placanje, provizija, itd.)

## Faza 4 — Jedan izvor istine za cene (BOT, tehnicki dug)

Trenutno cene i paketi postoje rucno upisani na DVA mesta: `site/index.html`
(marketing stranica) i `pitch.html` → `site/businessplan/index.html` (biznis plan
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
