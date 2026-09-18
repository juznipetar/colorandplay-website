# Instrukcije za automatizovanog agenta — Color and Play sajt

Ovaj fajl je napisan da se direktno nalepi u `zadatak.md` tvog lokalnog agenta
(Desktop\sync\agent, NASTAVI.bat/AGENT.bat) ili da posluzi kao referenca kad mu
rucno zadajes posao. Pise ga Claude (Cowork sesija) za Claude Code lokalnog agenta —
zato je precizan i eksplicitan o granicama.

## Kontekst (procitaj pre nego sto pocnes)

Ovo je sajt za "Color and Play", kreativni atelje u Baru (CH) koji priprema Suzana
Kozic (osnivac) uz pomoc Petra. Postoje DVA odvojena dokumenta koja NE SMES da mesas:

1. **Javna marketing stranica** (`site/index.html`) — za buduce mustarije, prodajni
   ton, tier paketi (Basic/Advance/All Inclusive), animacije. Ovo je ono na cemu
   najvise radis.
2. **Biznis plan za vlasnika lokala** (`site/businessplan/index.html`, izvor u
   `pitch.html` van site foldera) — poverljiv dokument sa realnim finansijskim
   modelom, namenjen g. Aligu (vlasnik lokala). Zakljucan lozinkom. NE DIRAJ
   finansijske brojeve u ovom dokumentu bez eksplicitnog naloga — oni su racunati
   iz `model.py` i moraju ostati konzistentni sa PDF-ovima koji su vec poslati.

Procitaj `docs/ROADMAP.md` (fazni plan) i `docs/ARHITEKTURA.md` (tehnicka
dokumentacija, dizajn sistem, i18n obrazac, tier komponenta) PRE nego sto pises
ijednu liniju koda. Ako imas "roadmap rezim", ovaj `ROADMAP.md` je fajl koji pratis.

## Sta vec postoji (ne pravi ispocetka)

- `site/index.html` — kompletna, funkcionalna marketing stranica sa DE/EN toggle-om,
  5 grupa tier paketa, animacijama (scroll-reveal, floating blobs, count-up
  brojaci, hover efekti). Ovo NIJE prazan template — ovo je zavrsena v2 verzija.
- `site/businessplan/index.html` — zavrsen, zakljucan lozinkom `ColorPlay2026`
  (PROMENI OVU LOZINKU — vidi zadatak 1 ispod).
- `site/robots.txt`, `site/DEPLOY.md` — gotovi.

## Zadaci (redosled po prioritetu)

### 1. Bezbednost — promeni placeholder lozinku (URADI PRVO)
Fajl `build_site.py` (van site foldera) ima liniju `PASSWORD = "ColorPlay2026"`.
Ovo je placeholder i NE SME da ostane kad se link posalje g. Aligu. Ako korisnik
(Petar/Suzana) nije vec dao novu lozinku, PITAJ ih za nju pre nego sto nastavis —
ne izmisljaj lozinku sam. Kad dobijes lozinku, izmeni `PASSWORD` u skripti, pokreni
`python3 build_site.py`, proveri da `site/businessplan/index.html` sadrzi novi hash
(ne stari), i commituj.

### 2. Deploy priprema (vidi DEPLOY.md)
Ako GitHub repo vec postoji (korisnik ce reci), inicijalizuj git u `site/` folderu
(ili kopiraj njegov sadrzaj u postojeci repo), push na `main`, ukljuci GitHub Pages
u Settings (ovo poslednje moras rucno kroz browser ili uputiti korisnika — GitHub
Pages se ne moze ukljuciti preko git push-a).

Ako korisnik jos nema domenu, NE CEKAJ na nju da nastavis ostatak posla (Faza 2/3 u
ROADMAP.md ne zavise od domene).

### 3. Tehnicka higijena (Faza 2 u ROADMAP.md)
Ovo mozes raditi potpuno samostalno bez daljih pitanja:
- Favicon (koristi brend boje: teal `#0B6E6B` i gold `#C9962E`, jednostavan
  geometrijski oblik — npr. tackica kao u `.brandmark .dot`)
- OG/Twitter meta tagovi
- `sitemap.xml`
- Skripta koja proverava i18n parove (svaki `data-lang="de"` ima svoj
  `data-lang="en"` par) i obrnuto — javi ako nadjes nesparene
- Provera linkova i tipfelera

### 4. Prosirenje tier paketa (Faza 3)
Dodaj Basic/Advance/All Inclusive strukturu (isti CSS obrazac, vidi
ARHITEKTURA.md sekciju "Tier pricing komponenta") za: Grundangebot, Solo-Abend,
Familie/Paare/Senioren, Plus-Angebot, Geschenkgutscheine, Ferien-Workshops.

**Cene su proizvoljne/ilustrativne — izmisli razumne cene u istom stilu kao
postojecih 5 grupa (Basic jeftinije/osnovnije, Advance srednje sa "Beliebt" bedzom,
All Inclusive najskuplje sa najvise pogodnosti).** Ovo je izricito trazeno od
korisnika ("cene stavi proizvoljne, mozemo kasnije da azuriramo") — ne treba da
pitas za svaku cenu, samo budi razuman i konzistentan sa postojecim rasponima.

### 5. Jedan izvor istine za cene (Faza 4 — vremenski zahtevno, radi kad ima vremena)
Napravi `data/pricing.json` i prepravi build skripte da iz njega generisu HTML.
Ovo je veci refaktor — testiraj dobro da oba fajla (marketing + businessplan) i
dalje rade identicno posle promene.

## STROGE GRANICE — nikad ne radi ovo bez eksplicitnog naloga od Petra/Suzane

- **Ne menjaj finansijske brojeve** u `pitch.html`/`businessplan/index.html`
  (Investitionsplan, Fixkosten, Umsatz, Startkapital itd.) — oni su racunati u
  `model.py` iz stvarnih pretpostavki i moraju odgovarati vec poslatim PDF-ovima.
  Ako mislis da treba da se promene, PITAJ prvo.
- **Ne kupuj nista** (domenu, hosting, placene alate) — to trazi platne podatke,
  covek to mora sam da uradi (vidi DEPLOY.md).
- **Ne dodaj lazne recenzije/testimonijale.** Sajt namerno nema "Sta gosti kazu"
  sekciju jer bi izmisljeni citati predstavljeni kao pravi bili neposteni prema
  buducim mustarijama. Ako se doda takva sekcija, MORA biti jasno obelezena kao
  primer/placeholder, nikad predstavljena kao stvarna recenzija.
- **Ne izmisljaj tacnu adresu lokala.** Ugovor sa vlasnikom jos nije potpisan —
  adresa ostaje "Folgt in Kürze" dok Petar/Suzana ne potvrde da je potpisan.
- **Ne uklanjaj `noindex` meta tag ni `robots.txt` pravilo** za `/businessplan/`
  putanju — ta stranica ne sme da zavrsi u Google pretrazi.
- **Ne uvodi build alate/framework-e** (Webpack, React, itd.) bez dogovora — vidi
  princip "potpuno samostalni fajlovi" u ARHITEKTURA.md.
- Ako naletis na odluku koja je poslovne/finansijske prirode (npr. "da li da
  dodamo online placanje", "koja provizija za booking sistem") — to STANI i
  prijavi, ne odlucuj sam. Vidi Faza 5 u ROADMAP.md ("van trenutnog obima").

## Kako da prijavis napredak

Prati konvenciju iz Smart MRO projekta: izvestaj sesije u `docs/izvestaji/` (npr.
`01-izvestaj-sesije-2026-09.md`) sa sazetkom sta je uradjeno, sta je ostalo, i sta
treba covek da odluci. Na pocetku svake nove sesije, procitaj poslednji izvestaj
PRE nego sto nastavis, i masinski proveri stanje (npr. `git log`, da li sajt
stvarno radi) umesto da slepo veruje izvestaju — isti princip koji vec koristis
na Smart MRO.

## Napomena o poreklu ovog fajla

Ovaj roadmap/instrukcije je napravila Cowork (cloud) sesija Claude-a, koja NIJE
imala pristup tvom racunaru niti Smart MRO projektu (samo procitala beleske o
njemu iz memorije, ne i sam kod). Format je pokusaj da se uklopi u tvoje postojece
konvencije (docs/ROADMAP.md, izvestaji sesija) — ako se razlikuje od onoga sto tvoj
lokalni agent ocekuje, prilagodi slobodno.
