# Predlog: Calendly za „Termin anfragen“ (Faza 3 — samo istraživanje)

> **Status:** predlog za odluku Petra/Suzane. **Nije implementirano** na sajtu u ovoj sesiji.
> Poslednje ažurirano: 18.09.2026.

## Kontekst

Trenutni tok na `index.html`:

1. Korisnik bira paket/stufu („Format wählen“).
2. Šalje upit putem kontakt formulara (Formspree) ili `mailto:` (`suzana.androvic@gmail.com`).
3. Color and Play ručno potvrđuje datum („innert 24 Stunden“).

Calendly bi zamenio ili dopunio korak 2–3 za **slobodne termine** gde klijent sam bira slot iz Suzaninog kalendara — korisno za Wine & Draw, Offenes Atelier i jednostavne 1:1 konsultacije. Za rođendane i firme i dalje je verovatno potreban ručni dogovor (cena po osobi, dekoracija, broj dece).

## Opcije embeda (kad/ako se odluči)

| Opcija | Kako izgleda | Prednost | Mana |
|--------|--------------|----------|------|
| **Inline embed** | Kalendar direktno u `#kontakt` ili posebnoj sekciji | Najmanje koraka za korisnika | Zauzima puno prostora na mobilnom; treba prilagoditi visinu iframe-a |
| **Pop-up tekst** | Link „Termin wählen“ otvara Calendly u overlay-u | Diskretno, lako uz postojeći CTA | Korisnik mora da klikne dodatni link |
| **Pop-up widget** | Plutajuće dugme u uglu | Uvek vidljivo | Može delovati „salesy“ za premium brend |

Za Color and Play ton preporuka je **pop-up tekst** ili sekundarni CTA pored formulara („Direkt Termin wählen“), ne floating widget.

Tehnički: Calendly daje `<script>` + embed kod — u static HTML repo-u to je jedan `<script src="https://assets.calendly.com/...">` plus link ili iframe. Nema backend-a, ali **uvodi treću stranu** (cookie/tracking — proveriti Impressum/Datenschutz pre go-live).

## Cene i provizije (provereno 09/2026, vidi [calendly.com/pricing](https://calendly.com/pricing))

| Plan | Cena (orientaciono) | Šta pokriva za Color and Play |
|------|---------------------|-------------------------------|
| **Free** | USD 0 | 1 tip događaja, 1 kalendar, neograničeni 1:1 sastanci, osnovni embed na sajt |
| **Standard** | ~USD 10/korisnik/mesec (godišnje) | Više tipova događaja, prilagođen branding, integracije (Zapier, HubSpot…) |
| **Teams** | ~USD 16/korisnik/mesec (godišnje) | Timski raspored, više korisnika |
| **Enterprise** | po dogovoru | Veće firme |

**Provizija Calendly-a:** Calendly **ne uzima proviziju po rezervaciji** — embed i zakazivanje su uključeni u plan. Ako se kasnije uključi **naplata pri zakazivanju** (Stripe/PayPal integracija), Calendly i dalje ne naplaćuje % od transakcije, ali **Stripe/PayPal uzimaju svoje processing fee** (npr. Stripe ~2.9% + fiksno po transakciji u CH). Naplata pri booking-u zahteva **Standard ili viši** plan — na Free planu nema plaćanja kroz Calendly.

Za Color and Play (depozit ili puna cena pri rezervaciji) to je **poslovna odluka**: da li uopšte naplaćivati online pre događaja, ili samo „soft booking“ bez plaćanja.

## Kako bi se uklopilo u „Termin anfragen“

Predloženi hibridni model (bez menjanja trenutnog formulara):

| Tip događaja | Preporučeni kanal |
|--------------|-------------------|
| Kindergeburtstag, Firmen, Private Feiern (tier paketi) | Formspree / mailto — ručna ponuda i potvrda |
| Wine & Draw, Offenes Atelier, Art Club info call | Calendly slot (fiksno trajanje, fiksna cena u opisu) |
| Geschenkgutschein / opšti upit | Formspree |

Na DE/EN sajtu: dva jasna CTA u kontakt sekciji — **„Anfrage senden“** (formular) i **„Verfügbaren Termin wählen“** (Calendly, kad postoji nalog).

## Alternative (kratko)

- **Cal.com** — open-source friendly, self-host ili cloud; više kontrole, više setupa.
- **Microsoft Bookings / Google Appointment Slots** — besplatno ako već koristite Microsoft 365 / Google Workspace; manje „premium“ UX od Calendly.
- **Acuity Scheduling** — sličan model, plaćeni planovi od ~USD 16/mesec.

Za mali atelje sa jednim kalendarom **Calendly Free** je dovoljan za pilot; ograničenje je **samo jedan aktivni tip događaja** na Free planu (promena tipa lomi stare linkove).

## Preporučeni sledeći korak za Petara/Suzanu

1. **Odluka:** Da li želite da gosti **sami biraju termin** za neke formate, ili sve ide preko ručne potvrde?
2. **Ako da — pilot:** Otvoriti besplatan Calendly nalog, povezati Google/Outlook kalendar, napraviti **jedan** event tip (npr. „Wine & Draw — Platz reservieren“, 90 min).
3. **Test bez sajta:** Podeliti Calendly link ručno 2–3 poznanika; proveriti notifikacije i vremensku zonu (Europe/Zurich).
4. **Tek onda embed:** Javiti botu da doda pop-up CTA u `index.html` + ažurira `DEPLOY.md` / Datenschutz napomenu.
5. **Ne uključivati plaćanje** u prvoj fazi — cene na sajtu ostaju informativne; naplata na licu mesta ili faktura kao sada.

**Ne raditi bez ovog koraka:** embed na javni sajt pre nego što Suzana potvrdi radno vreme, trajanje slotova i da li Free plan (1 event tip) pokriva sve ili treba Standard.
