# Izveštaj sesije 08 — 2026-09-18 (Cloud Agent)

Pre nastavka: `git pull origin main`, `python3 check_i18n.py index.html businessplan/index.html`.

---

## 1) Mapa/pin u Standort sekciji (uradjeno, live)

Na zahtev korisnika ("stavi pin i mapu na location") dodata je nova `.mapcard`
komponenta u `#standort` sekciju na `index.html` — Google Maps embed (bez API
ključa, `output=embed`) sa crvenim pin-om na koordinatama centra Baar-a
(47.1974, 8.5237), stilizovano da prati brend dizajn sistem (`--radius`,
`--shadow`, karta koja prati postojeći `.infocard` obrazac).

Pošto tačna adresa ateljea još nije potvrđena (ugovor sa vlasnikom nije
potpisan), korisnik je eksplicitno potvrdio da mapa za sada pokazuje centar
Baar-a uz vidljivu napomenu "Pin trenutno pokazuje centar Baar-a — tačna
adresa stiže uskoro" (DE/EN) — isti pošten obrazac kao postojeće "Folgt in
Kürze" polje. Kad tačna adresa bude potvrđena, zamena je jedna linija
(koordinate ili adresa u `src` atributu iframe-a).

Provereno pre push-a: i18n parovi (190/190), `tidy` bez pravih grešaka, render
u light/dark modu i na mobilnom, pin se stvarno prikazuje na mapi (ne samo
oblast bez markera — testirano sa koordinatama umesto imena mesta, jer imenovan
upit prikazuje samo oznaku oblasti bez pravog pin-a). Live, commit `3c9b135`.

## 2) Faza 7 — korisnikova originalna vizija upisana u plan (NIJE implementirano, samo planirano)

Korisnik je eksplicitno tražio da se sledeće upiše **direktno u plan za
automatizaciju** (ne da se uradi odmah u ovoj sesiji):

1. Prava galerija slika
2. Svaki od 11 paketa dobija SVOJU stranicu (ne samo karticu na početnoj) sa
   slikama i detaljnim objašnjenjem

Ovo je najveći pojedinačni zadatak dodat u `docs/ROADMAP.md` do sad — sajt
prelazi iz jednostranične arhitekture u pravi više-stranični sajt. Dodato kao
**Faza 7**, sa punim planom: preduslov (Faza 4 — `pricing.json` + lokalna build
skripta, sad blokirajuća, ne više "kad ima vremena"), specifikacija za galeriju
(uključujući ključni otvoren problem — nema pravih fotografija ateljea još, bot
ne sme koristiti stock-foto kao zamenu, isti princip kao kod lažnih recenzija),
tabela od 11 predloženih URL slug-ova za paket-stranice, sadržaj koji svaka
stranica treba da ima (hero slika, prošireni opis, tier tabela iz JSON-a,
mini-galerija, FAQ, CTA sa predizabranim paketom, breadcrumb, SEO meta),
povezivanje sa postojećim sajtom (dugmad na početnoj, nav link, sitemap), i
jasna podela šta bot može odmah vs. šta čeka na čoveka (prave fotografije,
odobrenje teksta).

Takođe ažurirano:
- `docs/ARHITEKTURA.md` — nova sekcija o planiranom više-stranicnom sajtu i
  eksplicitno objašnjenje zašto lokalna Python build skripta ne krši postojeći
  princip "potpuno samostalni fajlovi, nema build koraka" (GitHub Pages i dalje
  servira čist statički HTML — skripta se pokreće lokalno pre commit-a, isti
  obrazac koji već postoji za `businessplan/index.html`). Popravljene i zastarele
  stavke u "Poznata ograničenja" (kontakt formular, favicon/OG više nisu "nema
  jos", nego "gotovo, čeka X").
- `docs/BOT-INSTRUKCIJE.md` — zastareli numerisani spisak zadataka (1-6, ostao
  još od handoff-a, više nije odgovarao stvarnom stanju — npr. i dalje je
  govorio "čeka se odluka o paleti" iako je paleta odabrana u sesiji 05) zamenjen
  kratkim statusom po fazi + uputstvom da je `ROADMAP.md` jedini izvor istine za
  zadatke. Dodata nova STROGA GRANICA (stock-foto ne sme da se predstavlja kao
  pravi atelje) i pojašnjenje o build-skripti izuzetku.

## Šta i dalje čeka na čoveka

1. Formspree nalog + zamena placeholder ID-ja.
2. Nova businessplan lozinka pre slanja linka Aligu.
3. Calendly pilot odluka.
4. .ch domena.
5. Tačna adresa ateljea (za mapu i businessplan).
6. **Novo (Faza 7):** bar 15-20 pravih fotografija ateljea/radionica/gotovih
   radova — najveći blokator za pravu galeriju i hero slike po paketu. Ne mora
   profesionalni foto-shoot.
7. **Novo (Faza 7):** kad bot napravi pilot stranicu za jedan paket (predlog:
   Kindergeburtstage), potreban je pregled/odobrenje izgleda pre nego što se
   replicira na preostalih 10 paketa.
