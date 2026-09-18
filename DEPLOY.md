# Color and Play — deploy uputstvo (GitHub Pages)

## Sta je u ovom folderu

- `index.html` — javna marketing stranica (Angebot, Pakete/Tiers, Ablauf, Standort, Kontakt). DE/EN toggle, animacije.
- `businessplan/index.html` — kompletan biznis plan za Alig-a, zakljucan pristupnim kodom. Nije indeksiran od Google-a (`robots.txt` + noindex meta).
- `robots.txt` — govori pretrazivacima da ne indeksiraju `/businessplan/`.
- `docs/ROADMAP.md`, `docs/ARHITEKTURA.md`, `docs/BOT-INSTRUKCIJE.md` — plan rada, tehnicka dokumentacija i instrukcije za automatizovanog agenta koji nastavlja posao. Procitaj ove fajlove pre nego sto menjas sajt dalje.

Trenutni pristupni kod za businessplan stranicu je **ColorPlay2026** — promeni ga pre nego sto posaljes link Aligu (uputstvo ispod).

## 1. Kreiraj GitHub repo

1. Na github.com klikni **New repository**.
2. Ime repoa moze biti npr. `colorandplay-website` (public ili private — za GitHub Pages sa custom domenom, public je jednostavnije na free planu).
3. Ne dodaj README/gitignore, ostavi prazan repo.

## 2. Uploaduj fajlove

Najlaksi nacin bez terminala:
1. Otvori novi repo na GitHub-u, klikni **Add file → Upload files**.
2. Prevuci `index.html`, `robots.txt`, i ceo `businessplan` folder (sa `index.html` unutra).
3. Commit direktno na `main` granu.

Ili preko git-a u terminalu (ako ti odgovara):
```bash
git init
git add .
git commit -m "Color and Play website"
git branch -M main
git remote add origin https://github.com/<tvoj-username>/colorandplay-website.git
git push -u origin main
```

## 3. Ukljuci GitHub Pages

1. U repou idi na **Settings → Pages**.
2. Pod "Build and deployment" izaberi **Deploy from a branch**, grana `main`, folder `/ (root)`.
3. Sacuvaj — GitHub ce ti dati privremeni link tipa `https://<username>.github.io/colorandplay-website/`.

## 4. Kad kupis domen (.ch)

Preporuka: **Hostpoint** ili **Infomaniak** (svajcarski registrari, .ch domen ~CHF 5-15 za prvu godinu, bez potrebe za svajcarskom adresom).

1. Kupi domen (npr. `colorandplay.ch`).
2. Kod registrara postavi DNS:
   - jedan **CNAME** rekord: `www` → `<username>.github.io`
   - ili **A** rekordi za goli domen (`colorandplay.ch`) na GitHub Pages IP adrese (trenutno: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153 — proveri na github.com/pages ako se promene).
3. U repou, u root folderu, napravi fajl **`CNAME`** (bez ekstenzije) sa sadrzajem: `colorandplay.ch` (ili `www.colorandplay.ch`, zavisno sta si podesio).
4. U **Settings → Pages** ukuca custom domain i sacekaj da GitHub verifikuje (par minuta do par sati) i ukljuci "Enforce HTTPS".

## 5. Promeni pristupni kod za businessplan stranicu

U originalnom projektu (ne u ovom deploy folderu) postoji `build_site.py` koji generise `businessplan/index.html` iz `pitch.html`. Da promenis kod:
1. Otvori `build_site.py`, promeni liniju `PASSWORD = "ColorPlay2026"` na novi kod.
2. Pokreni `python3 build_site.py` — ovo regenerise `businessplan/index.html` (u build skripte lokalnom `site/` output folderu, odakle ga onda kopiras/pushujes u ovaj repo) sa novim kodom (hesiran, ne stoji plaintext u fajlu).
3. Uploaduj novi `businessplan/index.html` u repo (zameni stari).

Ako nemas pristup toj Python skripti, javi mi — mogu ti odmah generisati novi fajl sa drugim kodom.

## 6. Napomena o sigurnosti businessplan stranice

Ovo je "lagana" zastita (client-side provera lozinke) — dovoljna da neko ko slucajno naidje na link ili ga prosledi dalje ne moze lako da otvori stranicu, i dovoljna za privremeno deljenje sa Aligom. To NIJE prava server-side autentikacija — neko tehnicki potkovan i uporan bi teoretski mogao da zaobidje. Kako se stranica brise nakon sto Alig pregleda plan, ovo je sasvim ok za tu svrhu.

Ako zelis jace resenje bez napustanja GitHub Pages-a: postavi domen kroz **Cloudflare** (besplatno) i koristi **Cloudflare Access** da zakljucas putanju `/businessplan/*` pravim login-om (npr. samo Aligov email dobija jednokratni kod na mail). Javi ako zelis da ti pripremim i to.

## 7. Kontakt formular (Formspree)

Javna stranica (`index.html`) ima kontakt formular koji šalje upite na Formspree.
Dok se ne podesi nalog, u `action` URL-u stoji placeholder `YOUR_FORMSPREE_ID` —
formular prikazuje poruku da nije aktivan; `mailto:` link ostaje kao rezerva.

### Koraci za Petara/Suzanu (besplatan tier, ~5 min)

1. Idi na [formspree.io](https://formspree.io) i napravi besplatan nalog (email na koji želite da stižu upiti — npr. `suzana.androvic@gmail.com`).
2. Klikni **+ New Form**, daj mu ime npr. „Color and Play Anfragen“.
3. Formspree će pokazati **Form endpoint** u obliku  
   `https://formspree.io/f/xxxxxxxx` — kopiraj samo deo posle `/f/` (to je tvoj Form ID).
4. U repou otvori `index.html`, nađi:
   ```html
   action="https://formspree.io/f/YOUR_FORMSPREE_ID"
   ```
   Zameni `YOUR_FORMSPREE_ID` pravim ID-jem (npr. `action="https://formspree.io/f/abcdwxyz"`).
5. Commit + push na `main` — GitHub Pages redeployuje za par minuta.
6. Test: popuni formular na live sajtu; u Formspree inbox-u treba da se pojavi poruka. Proveri i spam folder.

**Besplatan plan (orientaciono):** ~50 submissiona mesečno, email notifikacije — dovoljno za start. Više submissiona ili timski inbox zahteva plaćeni plan (vidi formspree.io/pricing).

**Polja u formularu:** name, email, message (obavezno), phone (opciono). Formspree automatski prepoznaje `email` za Reply-To.

## 8. Kad Alig pregleda plan — uklanjanje stranice

1. U repou obrisi `businessplan/index.html` (ili ceo `businessplan` folder).
2. Commit — GitHub Pages automatski redeployuje za par minuta i stranica vise ne postoji (404).
3. Javna pocetna stranica (`index.html`) ostaje netaknuta i i dalje radi normalno.
