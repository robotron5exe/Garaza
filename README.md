# Cene Nepremičnin Maribor 📊

Spletna stran za prikaz zgodovinskih cen nepremičnin v Mariboru z osredotočenostjo na garaže.

## 🌐 Demo

Ko bo stran objavljena na GitHub Pages, bo dostopna na: `https://[username].github.io/Garaza/`

## 📋 Značilnosti

- **Interaktivni grafi** prikazujejo trende cen skozi desetletja
- **Osredotočenost na garaže** z detajlno analizo
- **Filtri** za izbiro vrste nepremičnine in časovnega obdobja
- **Odziven dizajn** - deluje na vseh napravah
- **Primerjalne analize** - rast cen različnih vrst nepremičnin
- **Pregledna tabela** s podrobnimi podatki

## 🚀 Namestitev in uporaba

### Lokalno testiranje

1. Klonirajte repozitorij:
```bash
git clone https://github.com/[username]/Garaza.git
cd Garaza
```

2. Odprite `index.html` v brskalniku ali uporabite lokalni strežnik:
```bash
# Z Python 3
python -m http.server 8000

# Z Node.js (npx)
npx serve
```

3. Odprite brskalnik na `http://localhost:8000`

### Objava na GitHub Pages

1. Pojdite v nastavitve repozitorija (Settings)
2. V levem meniju izberite "Pages"
3. Pod "Source" izberite "Deploy from a branch"
4. Izberite branch (npr. `main` ali `claude/realestate-prices-website-...`)
5. Izberite folder `/root`
6. Kliknite "Save"

Stran bo objavljena v nekaj minutah na `https://[username].github.io/Garaza/`

## 📊 Posodabljanje podatkov

Podatki so shranjeni v datoteki `data.js`. Trenutno so prikazani示zani podatki.

### Struktura podatkov

```javascript
{
    year: 2024,
    garages: {
        avg: 19500,      // Povprečna cena garaže v EUR
        min: 14500,      // Najnižja cena
        max: 26000,      // Najvišja cena
        median: 19200    // Mediana
    },
    apartments: {
        avg: 2450,       // Povprečna cena stanovanja v EUR/m²
        min: 1950,
        max: 3200,
        median: 2420
    },
    houses: {
        avg: 2150,       // Povprečna cena hiše v EUR/m²
        min: 1650,
        max: 2800,
        median: 2120
    }
}
```

### Kako posodobiti podatke

1. Odprite `data.js`
2. Najdite polje `years` v objektu `realEstateData`
3. Dodajte nove podatke ali spremenite obstoječe
4. Posodobite `metadata.lastUpdated` na trenutni datum
5. Shranite in znova naložite stran

### Viri podatkov

Priporočeni viri za resnične podatke:
- **GURS** (Geodetska uprava RS) - uradni podatki o transakcijah
- **SURS** (Statistični urad RS) - statistični podatki
- **nepremicnine.net** - tržni podatki
- **Uradni list RS** - javne dražbe in oglasi

### 📚 Vodič za populacijo podatkov

Za podrobna navodila o tem, kako pridobiti in vnesti resnične podatke, glejte:

**[DATA_POPULATION_GUIDE.md](DATA_POPULATION_GUIDE.md)** - Obsežen vodič, ki vključuje:
- Uradne vire podatkov (GURS, SURS)
- Metode spletnega zajemanja podatkov
- Kontaktne informacije za dostop do API-jev
- Korake za ročni vnos podatkov
- Pretvorbo SIT v EUR
- Najboljše prakse za kakovost podatkov

**Pomočna orodja:**
- `data_helper.py` - Python skripta za obdelavo podatkov
  - Izračun statistike (avg, min, max, median)
  - Pretvorba SIT v EUR
  - Validacija podatkov
  - Generiranje JavaScript formata za data.js
  - Interaktivni način vnosa podatkov

- `scraper_example.py` - Primer web scraperja (predloga)
  - Primer zajemanja podatkov iz nepremicnine.net
  - Vključuje preverjanje robots.txt
  - Potrebna prilagoditev CSS selektorjev

**Namestitev orodij:**
```bash
# Namestitev Python odvisnosti
pip install -r requirements.txt

# Zagon pomočnika za podatke
python3 data_helper.py

# Primer uporabe scraperja (zahteva prilagoditev)
python3 scraper_example.py
```

## 🛠️ Tehnologije

- **HTML5** - struktura
- **CSS3** - stilizacija z responsive dizajnom
- **Vanilla JavaScript** - logika aplikacije
- **Chart.js 4.4.0** - interaktivni grafi
- **GitHub Pages** - brezplačno gostovanje

## 📁 Struktura projekta

```
Garaza/
├── index.html                   # Glavna HTML stran
├── styles.css                   # CSS stilizacija
├── app.js                       # Logika aplikacije in grafi
├── data.js                      # Podatki o cenah nepremičnin
├── README.md                    # Ta datoteka
├── DATA_POPULATION_GUIDE.md     # Vodič za populacijo podatkov
├── data_helper.py               # Python skripta za obdelavo podatkov
├── scraper_example.py           # Primer web scraperja
└── requirements.txt             # Python odvisnosti
```

## 🎨 Prilagajanje

### Sprememba barv

Odprite `styles.css` in spremenite CSS spremenljivke v `:root`:

```css
:root {
    --primary-color: #2563eb;
    --secondary-color: #16a34a;
    --accent-color: #ea580c;
    /* ... */
}
```

### Dodajanje novih grafov

1. Dodajte `<canvas>` element v `index.html`
2. Ustvarite funkcijo grafa v `app.js`
3. Uporabite Chart.js dokumentacijo: https://www.chartjs.org/docs/

## 📝 Licenca

Ta projekt je namenjen informativnim namenom. Podatki so示zani in jih je potrebno nadomestiti z resničnimi podatki.

## 🤝 Prispevki

Prispevki so dobrodošli! Prosim ustvarite issue ali pull request.

## 📧 Kontakt

Za vprašanja in predloge odprite issue na GitHub repozitoriju.

---

**Opomba:** Trenutno prikazani podatki so示zani in služijo zgolj kot示示 strukture. Za produkcijsko uporabo jih nadomestite z resničnimi podatki iz zanesljivih virov.
