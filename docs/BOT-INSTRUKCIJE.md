# Instrukcije za automatizovanog agenta — Color and Play sajt

Ovaj fajl je napisan da se direktno nalepi u `zadatak.md` tvog lokalnog agenta
(Desktop\sync\agent, NASTAVI.bat/AGENT.bat) ili da posluzi kao referenca kad mu
rucno zadajes posao. Pise ga Claude (Cowork sesija) za Claude Code lokalnog agenta —
zato je precizan i eksplicitan o granicama. Poslednje azurirano: 18.09.2026,
posle deploy-a i punog deep-check-a sajta.

## OBAVEZNO — model

**Koristi ISKLJUCIVO Composer 2.5 za sav rad na ovom projektu.** Ne prebacuj na
drugi model tokom sesije, cak ni za "brze"/"jeftinije" pod-zadatke, bez
eksplicitnog naloga od Petra/Suzane. Ako tvoje okruzenje (agent-nastavi UI) nudi
select za model, proveri da je Composer 2.5 izabran PRE nego sto pokrenes ijedan
zadatak iz ovog fajla.

## Kontekst (procitaj pre nego sto pocnes)

Ovo je sajt za "Color and Play", kreativni atelje u Baru (CH) koji priprema Suzana
Kozic (osnivac) uz pomoc Petra. Postoje DVA odvojena dokumenta koja NE SMES da mesas:

1. **Javna marketing stranica** (`index.html` u repo root-u) — za buduce mustarije,
   prodajni ton, tier paketi (Basic/Advance/All Inclusive), animacije. Ovo je ono
   na cemu najvise radis.
2. **Biznis plan za vlasnika lokala** (`businessplan/index.html`, izvor u
   `pitch.html` van repo-a, u cloud radnom folderu — nije deo ovog git repo-a) —
   poverljiv dokument sa realnim finansijskim modelom, namenjen g. Aligu (vlasnik
   lokala). Zakljucan lozinkom. NE DIRAJ finansijske brojeve u ovom dokumentu bez
   eksplicitnog naloga — oni su racunati iz `model.py` i moraju ostati
   konzistentni sa PDF-ovima koji su vec poslati.

Procitaj `docs/ROADMAP.md` (fazni plan, sada azuriran sa stvarnim stanjem) i
`docs/ARHITEKTURA.md` (tehnicka dokumentacija, dizajn sistem, i18n obrazac, tier
komponenta) PRE nego sto pises ijednu liniju koda. Ako imas "roadmap rezim", ovaj
`ROADMAP.md` je fajl koji pratis.

## Sta vec postoji — SAJT JE VEC LIVE (ne pravi ispocetka, ne re-deploy-uj)

- **Live URL: https://juznipetar.github.io/colorandplay-website/** — GitHub Pages
  je vec ukljucen i radi (HTTP 200 potvrdjeno).
- **Git repo vec postoji lokalno, tacno u ovom folderu** (`Desktop\Color & Play`),
  sa remote-om na `github.com/juznipetar/colorandplay-website` (public). `git` i
  `gh` (GitHub CLI) su vec instalirani i `gh` je vec ulogovan kao `juznipetar` sa
  `repo` scope-om — NEMA potrebe za novim setup-om, autentifikacijom ili pitanjem
  korisnika za GitHub nalog. Samo `git add` / `commit` / `push` kad zavrsis izmene.
  Uvek prvo `git pull` na pocetku sesije (neko drugi je mozda vec pushovao).
- `index.html` — kompletna, funkcionalna marketing stranica sa DE/EN toggle-om,
  5 grupa tier paketa, animacijama (scroll-reveal, floating blobs, count-up
  brojaci, hover efekti), favicon setom, OG/Twitter meta tagovima, `sitemap.xml`.
  Ovo NIJE prazan template — ovo je zavrsena v2 verzija, vec deep-checked.
- `businessplan/index.html` — zavrsen, zakljucan lozinkom `ColorPlay2026`
  (PROMENI OVU LOZINKU — vidi zadatak 1 ispod). Head/body struktura je ispravljena
  (noindex meta je sada pouzdano u `<head>`) — ne vracaj build_site.py na staru
  verziju.
- `robots.txt`, `sitemap.xml`, `DEPLOY.md`, `.gitignore` — gotovi.
- `check_i18n.py` (repo root) — pokreni ga posle svake izmene teksta:
  `python3 check_i18n.py index.html businessplan/index.html` — mora da vrati OK
  za oba fajla pre commit-a.

## Zadaci (redosled po prioritetu)

### 1. Bezbednost — promeni placeholder lozinku (URADI PRVO, sajt je vec public)
`build_site.py` (u cloud radnom folderu, van ovog repo-a — proveri da li ti je
dostupan; ako nije, pitaj korisnika da ti prebaci `pitch.html` + `build_site.py`)
ima liniju `PASSWORD = "ColorPlay2026"`. Ovo je placeholder i NE SME da ostane
sad kad je repo vec public na GitHub-u i sajt live. Ako korisnik (Petar/Suzana)
nije vec dao novu lozinku, PITAJ ih za nju pre nego sto nastavis — ne izmisljaj
lozinku sam. Kad dobijes lozinku, izmeni `PASSWORD` u skripti, pokreni
`python3 build_site.py`, proveri da `businessplan/index.html` sadrzi novi hash
(ne stari), pokreni `check_i18n.py`, i commituj + push-uj.

### 2. Odluka o boji palete — CEKA NA POTVRDU, ne biraj sam
U posebnoj Cowork sesiji su pripremljene 3 konkretne, veselije palete boja
(Sunny Citrus, Playful Pastel, Bold Primary Play — svaka sa hex kodovima i
mapom upotrebe) kao vizuelno poredjenje, ali korisnik JOS NIJE izabrao koju
(ili da li uopste menja trenutnu tamniju/ekskluzivnu teal/gold/coral/sage
paletu). **Ne primenjuj nijednu paletu sam.** Ako Petar/Suzana kazu koju zele
(ili traze mesavinu), tek onda promeni `:root` promenljive u `index.html` i
`businessplan/index.html` (isto mesto na oba fajla, vidi ARHITEKTURA.md "Dizajn
sistem"), i proveri kontrast/citljivost posle promene.

### 3. Deploy odrzavanje (domena, kad je kupljena)
Ako korisnik kupi .ch domenu, napravi `CNAME` fajl u root-u sa domenom, uputi
korisnika koje DNS zapise da doda kod registrara (vidi DEPLOY.md korak 4), i
ukljuci "Enforce HTTPS" u repo Settings → Pages (rucno kroz browser, ili
`gh api` ako znas tacan endpoint — testiraj pre nego sto potvrdis korisniku
da je gotovo).

### 4. Tehnicka higijena — VECINA VEC GOTOVA, ostalo:
Favicon, OG/Twitter tagovi, sitemap.xml i i18n-check skripta su vec uradjeni
(vidi gore). Ostaje:
- Provera pristupacnosti (accessibility): kontrast boja (posebno ako menjas
  paletu u zadatku 2 — ponovo proveri), `alt` tekstovi, tab-navigacija kroz
  formu i dugmad
- Performance provera (Lighthouse ili slicno) — cilj: 90+ na Performance i SEO
- Rucno citanje DE/EN teksta na tipfelere (i18n-check proverava samo da li su
  parovi kompletni, ne i da li je tekst tacan)

### 5. Prosirenje tier paketa (Faza 3)
Dodaj Basic/Advance/All Inclusive strukturu (isti CSS obrazac, vidi
ARHITEKTURA.md sekciju "Tier pricing komponenta") za: Grundangebot, Solo-Abend,
Familie/Paare/Senioren, Plus-Angebot, Geschenkgutscheine, Ferien-Workshops.

**Cene su proizvoljne/ilustrativne — izmisli razumne cene u istom stilu kao
postojecih 5 grupa (Basic jeftinije/osnovnije, Advance srednje sa "Beliebt"
bedzom, All Inclusive najskuplje sa najvise pogodnosti).** Ovo je izricito
trazeno od korisnika ("cene stavi proizvoljne, mozemo kasnije da azuriramo") —
ne treba da pitas za svaku cenu, samo budi razuman i konzistentan sa postojecim
rasponima. Pokreni `check_i18n.py` posle.

### 6. Jedan izvor istine za cene (Faza 4 — vremenski zahtevno, radi kad ima vremena)
Napravi `data/pricing.json` i prepravi build skripte da iz njega generisu HTML.
Ovo je veci refaktor — testiraj dobro da oba fajla (marketing + businessplan) i
dalje rade identicno posle promene.

## STROGE GRANICE — nikad ne radi ovo bez eksplicitnog naloga od Petra/Suzane

- **Ne menjaj finansijske brojeve** u `pitch.html`/`businessplan/index.html`
  (Investitionsplan, Fixkosten, Umsatz, Startkapital itd.) — oni su racunati u
  `model.py` iz stvarnih pretpostavki i moraju odgovarati vec poslatim PDF-ovima.
  Ako mislis da treba da se promene, PITAJ prvo.
- **Ne biraj/primenjuj boju paletu sam** (zadatak 2 gore) — cekaj potvrdu.
- **Ne kupuj nista** (domenu, hosting, placene alate) — to trazi platne podatke,
  covek to mora sam da uradi (vidi DEPLOY.md).
- **Ne dodaj lazne recenzije/testimonijale.** Sajt namerno nema "Sta gosti kazu"
  sekciju jer bi izmisljeni citati predstavljeni kao pravi bili neposteni prema
  buducim mustarijama. Ako se doda takva sekcija, MORA biti jasno obelezena kao
  primer/placeholder, nikad predstavljena kao stvarna recenzija.
- **Ne izmisljaj tacnu adresu lokala.** Ugovor sa vlasnikom jos nije potpisan —
  adresa ostaje "Folgt in Kürze" dok Petar/Suzana ne potvrde da je potpisan.
- **Ne uklanjaj `noindex` meta tag ni `robots.txt` pravilo** za `/businessplan/`
  putanju — ta stranica ne sme da zavrsi u Google pretrazi. `noindex` je sad
  ispravno u `<head>` — ne premesti ga slucajno nazad u `<body>` ako menjas
  `build_site.py`.
- **Ne uvodi build alate/framework-e** (Webpack, React, itd.) bez dogovora — vidi
  princip "potpuno samostalni fajlovi" u ARHITEKTURA.md.
- **Ne menjaj model** sa Composer 2.5 na nesto drugo bez eksplicitnog naloga
  (vidi "OBAVEZNO — model" na vrhu).
- Ako naletis na odluku koja je poslovne/finansijske ili vizuelne/brend prirode
  (npr. "da li da dodamo online placanje", "koja provizija za booking sistem",
  koja boja paleta) — to STANI i prijavi, ne odlucuj sam. Vidi Faza 5 u
  ROADMAP.md ("van trenutnog obima").

## Kako da prijavis napredak

Prati konvenciju iz Smart MRO projekta: izvestaj sesije u `docs/izvestaji/` (npr.
`01-izvestaj-sesije-2026-09.md`) sa sazetkom sta je uradjeno, sta je ostalo, i sta
treba covek da odluci. Na pocetku svake nove sesije, procitaj poslednji izvestaj
PRE nego sto nastavis, i masinski proveri stanje (npr. `git log`, `git status`,
da li sajt stvarno radi — `curl` na live URL, ne veruj da je "sigurno jos live")
umesto da slepo veruje izvestaju — isti princip koji vec koristis na Smart MRO.

## Napomena o poreklu ovog fajla

Ovaj roadmap/instrukcije je napravila Cowork (cloud) sesija Claude-a. Ta ista
sesija je, uz eksplicitnu dozvolu korisnika, direktno sa ovog racunara (preko
Desktop Commander MCP-a) napravila GitHub repo, pushovala sajt i ukljucila
GitHub Pages — repo i live sajt VEC POSTOJE, to nije hipotetski sledeci korak.
Cloud sesija NIJE imala pristup Smart MRO projektu (samo procitala beleske o
njemu iz memorije, ne i sam kod). Format je pokusaj da se uklopi u tvoje
postojece konvencije (docs/ROADMAP.md, izvestaji sesija) — ako se razlikuje od
onoga sto tvoj lokalni agent ocekuje, prilagodi slobodno.
