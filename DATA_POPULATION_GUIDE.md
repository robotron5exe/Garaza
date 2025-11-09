# Data Population Guide for Garaza Project

## Overview

This guide provides comprehensive methods to populate real data into your Maribor real estate price tracking website. Currently, the project contains placeholder data in `data.js` that needs to be replaced with actual market data.

## Data Structure

Your project expects data in this format:

```javascript
{
    year: 2024,
    garages: {
        avg: 19500,      // Average garage price in EUR
        min: 14500,      // Minimum price
        max: 26000,      // Maximum price
        median: 19200    // Median price
    },
    apartments: {
        avg: 2450,       // Average apartment price in EUR/m²
        min: 1950,
        max: 3200,
        median: 2420
    },
    houses: {
        avg: 2150,       // Average house price in EUR/m²
        min: 1650,
        max: 2800,
        median: 2120
    }
}
```

---

## Method 1: Official Government Data Sources (RECOMMENDED)

### 1.1 GURS (Geodetska uprava Republike Slovenije)

**What they provide:** Real estate transaction data from actual sales

**Access Method:**
- **Website:** https://egp.gu.gov.si/ and https://www.e-prostor.gov.si/
- **Data License:** Creative Commons 4.0 (CC-BY) - free for commercial and non-commercial use
- **Contact:** gurs@assist.si for API access questions

**Key Information:**
- GURS maintains the Real Estate Market Record (Evidenca trga nepremičnin)
- Data includes concluded sales and rental transactions
- System migration completed in 2024 - now uses JGP (Public Geodetic Data) application
- Data sources from Financial Administration of Slovenia

**Steps to Access:**
1. Visit https://www.e-prostor.gov.si/en/access-to-geodetic-data/
2. Contact gurs@assist.si to request:
   - Historical transaction data for Maribor region
   - API documentation if available
   - Bulk data export options
3. Filter data by:
   - Location: Maribor and surrounding areas
   - Property type: Garages, apartments, houses
   - Time period: 1990-2024

**Data Processing:**
- Download transaction data
- Calculate avg, min, max, median for each year
- Group by property type
- Convert to EUR if needed (data before 2007 may be in SIT)

### 1.2 SURS (Statistični urad Republike Slovenije)

**What they provide:** Quarterly residential housing price indices

**Access Method:**
- **Website:** https://www.stat.si/
- **Reports:** Published quarterly under "Residential housing price indices"

**Key Information:**
- Data available since Q1 2007
- Municipality-level data for Maribor
- Existing flats and detached houses data
- Free public access

**Recent Data Points:**
- Q1 2024: Available at https://www.stat.si/StatWeb/en/News/Index/12937
- Q1 2021: Maribor flats increased by 4.6%
- 2024: Maribor had 440 apartment transactions (down 52.95%)
- Detached houses in Maribor: +11.43% median price growth

**Steps to Access:**
1. Visit https://www.stat.si/StatWeb/en/
2. Navigate to: Data → Residential housing price indices
3. Download quarterly reports for Maribor
4. Extract price data by property type
5. Calculate historical averages

---

## Method 2: Commercial Real Estate Portals

### 2.1 Nepremicnine.net

**What they provide:** Current market listings and historical data

**Important:** Nepremicnine.net does NOT have an official public API

**Option A: Web Scraping (Technical Approach)**

**GitHub Open-Source Scrapers:**
- Repository: https://github.com/mowlc/real-estate-scraper
- Repository: https://github.com/tresko/real-estate-scraper

**Features:**
- Configure search parameters on nepremicnine.net
- Copy URLs into configuration
- Receive email updates with new listings
- Extract: title, location, description, price, link

**Setup Steps:**
```bash
# Clone the repository
git clone https://github.com/mowlc/real-estate-scraper.git
cd real-estate-scraper

# Follow repository README for setup
# Configure for Maribor region and garage/apartment/house searches
# Run scraper to collect current listings
```

**Apify Actor (Paid Service):**
- Service: https://apify.com/potocnik-jure/nepremicnine---actor
- Stealth mode scraping
- Filtered browse page scraping
- Requires monthly subscription

**Option B: Manual Data Collection**

1. Visit https://www.nepremicnine.net/
2. Search for properties in Maribor:
   - Filter by type: Garages, Apartments, Houses
   - Note current asking prices
3. Record data in spreadsheet:
   ```
   Property Type | Location | Size | Price | Price/m² | Date
   Garage        | Maribor  | 18m² | €20000 | -       | 2024-11
   Apartment     | Maribor  | 65m² | €160000 | €2462  | 2024-11
   ```
4. Calculate statistics (avg, min, max, median)
5. Update data.js

**Legal Considerations:**
- Check terms of service before scraping
- Review robots.txt file
- Consider rate limiting
- Attribute data source

### 2.2 Other Real Estate Portals

**Bolha.com:**
- Similar to nepremicnine.net
- Can use same scraping tools
- Good for current market prices

**Real Estate Agencies:**
- RE/MAX Slovenia
- Sotheby's International Realty Slovenia
- Local Maribor agencies
- Request historical transaction data

---

## Method 3: Manual Data Entry Process

### Step-by-Step Guide

**1. Open data.js file**
```bash
nano data.js
# or use your preferred editor
```

**2. Locate the years array**
```javascript
years: [
    {
        year: 2024,
        garages: { ... },
        // etc.
    }
]
```

**3. Update data for each year**
- Replace placeholder values with real data
- Ensure all required fields are present: avg, min, max, median
- Maintain proper JavaScript syntax

**4. Update metadata**
```javascript
metadata: {
    lastUpdated: '2024-11-09',  // Update to current date
    currency: 'EUR',
    source: 'GURS, SURS, nepremicnine.net',  // List actual sources
    notes: [
        // Update notes to reflect real data
    ]
}
```

**5. Validate data**
```bash
# Open in browser and check for errors
python3 -m http.server 8000
# Visit http://localhost:8000
```

---

## Method 4: Creating a Data Collection Script

### Option A: Python Script for SURS Data

Create a script to fetch and process SURS quarterly reports:

```python
# data_collector.py
import requests
import json
from datetime import datetime

def fetch_surs_data(year, quarter):
    """
    Fetch SURS residential housing price data
    """
    # SURS API endpoint (if available)
    # Or parse HTML from quarterly reports
    pass

def calculate_statistics(prices):
    """
    Calculate avg, min, max, median from price list
    """
    return {
        'avg': sum(prices) / len(prices),
        'min': min(prices),
        'max': max(prices),
        'median': sorted(prices)[len(prices) // 2]
    }

def update_data_js(new_data):
    """
    Update the data.js file with new data
    """
    pass

if __name__ == '__main__':
    # Collect data for all years
    for year in range(2007, 2025):
        print(f"Processing {year}...")
        # Fetch and process data
```

### Option B: Node.js Scraper

```javascript
// scraper.js
const axios = require('axios');
const cheerio = require('cheerio');

async function scrapeNepremicnine(searchUrl) {
    try {
        const response = await axios.get(searchUrl);
        const $ = cheerio.load(response.data);

        // Parse listings
        const listings = [];
        $('.property-item').each((i, elem) => {
            // Extract price, location, etc.
        });

        return listings;
    } catch (error) {
        console.error('Scraping error:', error);
    }
}

function calculateStats(listings) {
    // Calculate avg, min, max, median
}

// Run scraper
scrapeNepremicnine('https://www.nepremicnine.net/...');
```

---

## Recommended Workflow

### Phase 1: Get Official Data (Weeks 1-2)

1. **Contact GURS:**
   - Email: gurs@assist.si
   - Request: Historical transaction data for Maribor (1990-2024)
   - Ask about: API access, bulk data export, data format

2. **Download SURS Reports:**
   - Visit https://www.stat.si/
   - Download all quarterly reports since 2007
   - Extract Maribor-specific data
   - Create spreadsheet with extracted data

3. **Process and Convert:**
   - Convert SIT to EUR for pre-2007 data (1 EUR = 239.640 SIT)
   - Calculate annual averages from quarterly data
   - Generate avg, min, max, median statistics

### Phase 2: Fill Data Gaps (Week 3)

1. **For recent data (2020-2024):**
   - Use nepremicnine.net current listings
   - Manual sampling of 20-30 garages, apartments, houses
   - Calculate current market statistics

2. **For historical gaps (1990-2007):**
   - Research local Maribor real estate agencies
   - Check municipal archives
   - Use inflation adjustment from later known data
   - Consult Uradni list RS archives

### Phase 3: Validate and Update (Week 4)

1. **Data validation:**
   - Check for outliers
   - Verify trends make sense
   - Cross-reference with national trends
   - Ensure inflation adjustment is correct

2. **Update data.js:**
   - Replace placeholder data with real data
   - Update metadata section
   - Add proper source attribution
   - Update lastUpdated date

3. **Test website:**
   - Run local server
   - Check all graphs render correctly
   - Verify filters work
   - Test responsiveness

### Phase 4: Maintain and Update (Ongoing)

1. **Quarterly updates:**
   - Check SURS for new quarterly data
   - Update latest year's data
   - Add new year when available

2. **Annual review:**
   - Verify data accuracy
   - Update methodology if needed
   - Add new data sources if discovered

---

## Historical Context: Currency Conversion

**Slovenia adopted EUR on January 1, 2007**

For data before 2007:
- Original currency: Slovenian Tolar (SIT)
- Conversion rate: 1 EUR = 239.640 SIT
- Example: 1,000,000 SIT = 4,173.52 EUR

**Inflation Adjustment:**

If you have nominal prices from earlier years, consider adjusting for inflation:
- Use Eurostat HICP (Harmonised Index of Consumer Prices)
- Slovenia inflation calculator: https://www.stat.si/

---

## Data Quality Best Practices

### 1. Source Attribution
Always document your data sources:
```javascript
metadata: {
    sources: [
        {
            name: 'GURS',
            url: 'https://www.e-prostor.gov.si/',
            dataRange: '1995-2024',
            type: 'Transaction data'
        },
        {
            name: 'SURS',
            url: 'https://www.stat.si/',
            dataRange: '2007-2024',
            type: 'Price indices'
        }
    ]
}
```

### 2. Data Validation Rules
- Minimum < Average < Maximum
- Median should be close to Average (normally)
- Year-over-year changes should be reasonable (typically -20% to +30%)
- Garage prices should be lower than apartment prices (total vs per m²)

### 3. Documentation
Keep a log of:
- When data was collected
- Which sources were used
- Any adjustments or calculations made
- Known gaps or limitations

---

## Sample Data Collection Template

Create a spreadsheet for data collection:

| Year | Property | Source | Data Type | Avg | Min | Max | Median | Sample Size | Notes |
|------|----------|--------|-----------|-----|-----|-----|--------|-------------|-------|
| 2024 | Garage | GURS | Transaction | 19500 | 14500 | 26000 | 19200 | 45 | Full year |
| 2024 | Apartment | SURS | Index | 2450 | 1950 | 3200 | 2420 | Q1-Q3 | Preliminary |
| 2023 | Garage | Nepremicnine | Listing | 18000 | 13000 | 24000 | 17800 | 28 | Sampled |

---

## Quick Start: Immediate Data Update

If you need to update data quickly with current market prices:

1. **Visit nepremicnine.net:**
   - Search "garaža Maribor" → note 10 prices → calculate stats
   - Search "stanovanje Maribor" → note 10 prices per m² → calculate stats
   - Search "hiša Maribor" → note 10 prices per m² → calculate stats

2. **Open data.js and update 2024 entry:**
   ```javascript
   {
       year: 2024,
       garages: {
           avg: [calculated average],
           min: [lowest price seen],
           max: [highest price seen],
           median: [middle value]
       },
       // ... same for apartments and houses
   }
   ```

3. **Update metadata:**
   ```javascript
   metadata: {
       lastUpdated: '2024-11-09',
       source: 'Market data from nepremicnine.net, sampled November 2024'
   }
   ```

4. **Test:**
   ```bash
   python3 -m http.server 8000
   ```

---

## Automation Ideas for Future

### 1. Scheduled Data Collection
- Set up monthly/quarterly scraping job
- Use GitHub Actions or cron job
- Automatically update data.js

### 2. Data API Integration
- If GURS provides API, integrate directly
- Cache results to avoid excessive requests
- Update website data automatically

### 3. User Submissions
- Add form for real estate professionals to submit data
- Verify submissions before adding to dataset
- Community-driven data collection

---

## Legal and Ethical Considerations

### Web Scraping Ethics
- Respect robots.txt
- Implement rate limiting (1-2 requests per second max)
- Don't overload servers
- Cache results to minimize requests
- Consider commercial data licenses if scraping extensively

### Data Usage Rights
- GURS data: CC-BY 4.0 (free to use with attribution)
- SURS data: Public statistical data (free to use)
- Nepremicnine.net: Check terms of service
- Always attribute sources clearly on website

### Privacy
- Don't publish individual transaction addresses
- Use aggregated/anonymized data only
- Respect GDPR requirements for EU data

---

## Contact Information for Data Access

**GURS (Surveying and Mapping Authority):**
- Email: gurs@assist.si
- Website: https://www.e-prostor.gov.si/
- Purpose: Request API access, bulk data export

**SURS (Statistical Office):**
- Website: https://www.stat.si/
- Public data portal: https://pxweb.stat.si/

**Nepremicnine.net:**
- Technical support: podpora@nepremicnine.net
- General: info@nepremicnine.net
- Ask about: Data licensing for research/website use

---

## Troubleshooting

**Problem: Historical data not available**
- Solution: Use interpolation from known data points
- Cross-reference with national Slovenia trends
- Adjust recent data for inflation backwards

**Problem: Inconsistent data between sources**
- Solution: Use multiple sources and average
- Document discrepancies
- Prefer official government data (GURS/SURS)

**Problem: Garage-specific data scarce**
- Solution: Sample current nepremicnine.net listings
- Contact local real estate agencies in Maribor
- Use proportional adjustment from apartment prices

**Problem: API access denied**
- Solution: Use manual data collection
- Request academic/research access
- Use publicly available reports and extract manually

---

## Next Steps

1. **Immediate:** Manually update 2024 data from current nepremicnine.net listings (1-2 hours)
2. **Short-term:** Contact GURS and download SURS reports (1-2 weeks)
3. **Medium-term:** Process official data and update all years (2-4 weeks)
4. **Long-term:** Set up automated data collection (optional)

Good luck with your data population! Start with the official sources (GURS/SURS) for the most reliable historical data.
