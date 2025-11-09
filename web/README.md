# Maribor Real Estate Website

Interactive web visualization of Maribor real estate market data with focus on garage prices.

## Features

- 📊 **Interactive Charts** - Price trends over time using Chart.js
- 🚗 **Garage Focus** - Detailed garage price analysis
- 📈 **Comparison Tools** - Compare garages, apartments, and houses
- 🔍 **Filters** - Filter by property type and time period
- 📱 **Responsive** - Works on desktop and mobile

## Quick Start

### Option 1: Python Server (Recommended)

```bash
# From the web/ directory
python server.py

# Or specify a port
python server.py 8080
```

Then open http://localhost:8000 in your browser.

### Option 2: Direct File Open

Simply open `index.html` in your web browser. Note: Some browsers may restrict local file access to JavaScript files.

### Option 3: Any HTTP Server

```bash
# Using Python 3
python -m http.server 8000

# Using Node.js (if you have http-server installed)
npx http-server

# Using PHP
php -S localhost:8000
```

## Data Updates

The website uses `data.js` which is generated from the comprehensive JSON research data.

To regenerate `data.js` with latest data:

```bash
cd ..
python scripts/generate_web_data.py
```

This will:
1. Load data from `data/raw/*.json`
2. Convert to website format
3. Generate `web/data.js`

## File Structure

```
web/
├── index.html      # Main HTML page
├── styles.css      # Styling
├── app.js          # Application logic and charts
├── data.js         # Real estate data (generated)
├── server.py       # Simple Python HTTP server
└── README.md       # This file
```

## Customization

### Change Data Points

Edit `scripts/generate_web_data.py` and modify the `target_years` array:

```python
target_years = [2005, 2008, 2010, 2012, 2015, 2018, 2020, 2022, 2024, 2025]
```

### Modify Charts

Edit `app.js` to customize chart appearance, colors, or behavior.

### Update Styles

Edit `styles.css` to change the visual design. CSS variables are defined in `:root`:

```css
:root {
    --primary-color: #2563eb;
    --secondary-color: #16a34a;
    --accent-color: #ea580c;
    /* ... */
}
```

## Language

The website is in **Slovenian** (sl). To translate:

1. Edit `index.html` - Update all text content
2. Change `lang="sl"` to your language code (e.g., `lang="en"`)
3. Update meta tags and titles

## Data Sources

All data comes from comprehensive 20-year research:
- GURS (Geodetska uprava Republike Slovenije)
- SORS (Statistical Office of the Republic of Slovenia)
- Eurostat
- Real estate portals (NEPREMICNINE.net, Siol.net)

See the main project README for full data source documentation.

## Browser Compatibility

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

Requires JavaScript enabled.

## License

Part of the Garaza project. See main LICENSE file.
