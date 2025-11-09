# Garaza - Maribor Real Estate Market Analysis

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Website](https://img.shields.io/badge/website-live-blue.svg)
![Data Updated](https://img.shields.io/badge/data-2025--11--09-brightgreen.svg)

A comprehensive analysis and data repository for real estate prices in Maribor, Slovenia, with special focus on garage and parking space markets.

**Features:**
- 📊 **Interactive Website** - Slovenian web interface with charts
- 🐍 **Python API** - Data loading, analysis, and visualization tools
- 📈 **20 Years of Data** - Historical prices from 2005-2025
- 🚗 **Garage Focus** - Detailed garage market analysis
- 📉 **Market Insights** - ROI calculators, trend analysis, phase detection

## 📊 Project Overview

This project provides 20 years of historical real estate market data (2005-2025) for Maribor, Slovenia's second-largest city. It includes:

- **Residential apartment price trends** with annual data points
- **Garage and parking space pricing** across different locations
- **Market cycle analysis** covering boom, crash, and recovery periods
- **Comparative analysis** with Ljubljana and national trends
- **Investment metrics** and ROI calculations

## 🗂️ Project Structure

```
Garaza/
├── web/                                 # Interactive website
│   ├── index.html                       # Main page (Slovenian)
│   ├── app.js                           # Charts and interactivity
│   ├── data.js                          # Generated data
│   ├── styles.css                       # Styling
│   ├── server.py                        # Simple HTTP server
│   └── README.md                        # Website documentation
├── data/
│   ├── raw/                             # Original data files
│   │   ├── maribor_apartments_historical.json
│   │   ├── garage_prices_maribor.json
│   │   ├── garage_prices_ljubljana.json
│   │   └── slovenia_national_market.json
│   └── processed/                       # Processed/cleaned data
├── src/
│   └── garaza/                          # Python package
│       ├── __init__.py
│       ├── data_loader.py               # Data loading utilities
│       ├── analysis.py                  # Analysis functions
│       └── visualization.py             # Plotting and charts
├── scripts/                             # Analysis scripts
│   ├── quick_analysis.py                # Fast market overview
│   ├── price_trends_analysis.py         # Comprehensive analysis
│   ├── investment_comparison.py         # ROI comparison
│   └── generate_web_data.py             # Generate website data
├── docs/                                # Additional documentation
│   └── GETTING_STARTED.md               # Tutorial guide
├── maribor-real-estate-analysis-2005-2025.md  # Comprehensive report
├── README.md                            # This file
└── requirements.txt                     # Python dependencies
```

## 📈 Key Findings

### Apartment Prices (Maribor)

| Period | Price Range (€/m²) | Key Events |
|--------|-------------------|------------|
| 2005 | €1,100-1,500 | Pre-boom period |
| 2008 | €1,700-2,100 | Market peak |
| 2014 | €1,400-1,550 | Crisis bottom (-20% from peak) |
| 2021 | €1,900-2,200 | Boom year (+19% YoY) |
| 2024 | €2,300-2,600 | Current market (transaction volumes -53%) |
| 2025 | €2,400-2,700 | Forecast (cooling expected) |

**Total 20-year appreciation: 80-100% nominal, 40-50% real (inflation-adjusted)**

### Garage Prices (Current Market 2024)

#### Maribor
- **Price Range**: €9,900 - €22,000
- **Average**: €12,500
- **Price/m²**: €688-1,692 (avg €1,100)
- **Net Rental Yield**: 6-7%

#### Ljubljana (Comparison)
- **Price Range**: €11,000 - €37,500
- **Average**: €22,500
- **Price/m²**: €750-2,800 (avg €1,900)
- **Maribor Discount**: 40-60%

### Investment Insights

🟢 **Garage Investment Advantages:**
- Superior cash flow: 6-7% net yield vs apartments (2.5-3.5%)
- Lower capital requirement
- Easier property management
- Growing urban parking demand

🔴 **Current Market Risks:**
- Transaction volumes collapsed 53% in Maribor (2024)
- Market likely at or near peak
- Price-to-income ratio: 7.06 (stretched affordability)
- Limited upside potential in near term

## 🚀 Quick Start

### Option 1: Interactive Website

```bash
# Launch the website
cd web
python server.py

# Open http://localhost:8000 in your browser
```

**No installation required!** The website works with just Python's built-in HTTP server.

### Option 2: Python Analysis

```bash
# Clone the repository
git clone https://github.com/robotron5exe/Garaza.git
cd Garaza

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run quick analysis
python scripts/quick_analysis.py
```

### Basic Usage

```python
from garaza import load_apartment_data, load_garage_data, calculate_roi

# Load historical apartment prices
apartments = load_apartment_data()
print(apartments.head())

# Load garage market data
garages = load_garage_data('maribor')

# Calculate investment ROI
roi = calculate_roi(
    purchase_price=12000,
    monthly_rent=82,
    annual_costs=264
)
print(f"Net Yield: {roi['net_yield_pct']:.2f}%")
```

## 📊 Data Sources

All data is sourced from reliable, official sources:

- **GURS** (Geodetska uprava Republike Slovenije) - Real Estate Market Register
- **SORS** (Statistical Office of the Republic of Slovenia) - Housing Price Indices
- **Eurostat** - European Union official statistics
- **Real Estate Portals** - NEPREMICNINE.net, Siol.net, 24nep.si
- **Market Analysis** - Global Property Guide, Trading Economics, industry reports

### Data Quality Notes

- **2005-2006**: Estimates based on national trends (Low confidence)
- **2007-2024**: Official GURS/SORS data (High confidence)
- **Garage Historical**: Limited data, estimates from market trends (Medium confidence)
- **2025**: Forecasts based on current trends and expert predictions

## 📖 Documentation

### Comprehensive Report

See [maribor-real-estate-analysis-2005-2025.md](maribor-real-estate-analysis-2005-2025.md) for the complete 50+ page analysis including:

- Detailed historical timeline
- Market cycle analysis
- Investment considerations
- Statistical tables and appendices
- Risk factors and future outlook

### Data Files

#### `data/raw/maribor_apartments_historical.json`
Complete historical price series (2005-2025) with:
- Annual low/mid/high price estimates
- Year-over-year change percentages
- Data quality indicators
- Transaction volumes
- Current market metrics

#### `data/raw/garage_prices_maribor.json`
Garage market data including:
- Current listings with locations and prices
- Historical price estimates
- Monthly parking rates
- Investment analysis with ROI calculations

#### `data/raw/slovenia_national_market.json`
National context data:
- House price index (2015=100)
- Transaction volumes
- Market phases
- Economic indicators

## 🔬 Analysis Examples

### Price Trend Analysis

```python
import matplotlib.pyplot as plt
from garaza import load_apartment_data, plot_price_trends

# Load data
df = load_apartment_data()

# Plot 20-year price trends
plot_price_trends(df, show_market_phases=True)
plt.savefig('price_trends.png')
```

### ROI Comparison: Garage vs Apartment

```python
from garaza import compare_investments

results = compare_investments(
    garage_price=12000,
    garage_rent=82,
    apartment_price=150000,
    apartment_rent=600
)

print(results.summary())
```

### Market Cycle Detector

```python
from garaza import detect_market_phase

current_phase = detect_market_phase(
    transaction_volume_change=-53,
    price_change=6.1,
    yoy_price_change=8.38
)

print(f"Current Market Phase: {current_phase}")
# Output: "Late Cycle / Cooling"
```

## 📊 Key Statistics

### Market Phases (2005-2025)

| Phase | Period | Characteristics |
|-------|--------|-----------------|
| 🟢 Boom | 2004-2008 | +16.7% avg annual growth |
| 🔴 Crash | 2008-2014 | -20% total decline |
| 🟡 Recovery | 2015-2021 | Return to peak, +67% growth (2019-2024) |
| 🟠 Late Cycle | 2022-2024 | High prices, low volumes |
| ⚪ Cooling | 2025+ | Expected gradual cooling |

### Current Market Metrics (2024-2025)

| Metric | Value | Status |
|--------|-------|--------|
| Median Price (Maribor) | €2,450/m² | 🟠 Near Peak |
| YoY Price Change | +8.38% | 🟢 Positive |
| Transaction Volume Change | -52.95% | 🔴 Critical Decline |
| Price-to-Income Ratio | 7.06 | 🟠 Stretched |
| Rental Yield (Apartments) | 3.5% | 🟡 Modest |
| Rental Yield (Garages) | 6-7% | 🟢 Good |

## 🛠️ Development

### Running Tests

```bash
pytest tests/
```

### Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Adding New Data

To add new market data:

1. Place raw data files in `data/raw/`
2. Update the data loader in `src/garaza/data_loader.py`
3. Document data sources and quality in metadata
4. Run validation scripts

## 📝 Citation

If you use this data in your research or analysis, please cite:

```
Garaza Project (2025). Maribor Real Estate Market Analysis (2005-2025).
GitHub repository: https://github.com/robotron5exe/Garaza
Data sources: GURS, SORS, Eurostat, real estate portals
```

## ⚖️ License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This analysis is for informational and educational purposes only. It does not constitute investment advice, financial advice, or real estate recommendations. Real estate investments carry significant risks including loss of capital. Past performance does not guarantee future results.

**Always:**
- Conduct your own due diligence
- Consult qualified financial and legal professionals
- Verify all data independently
- Consider your personal financial situation and risk tolerance

## 📞 Contact

- **Project**: [Garaza on GitHub](https://github.com/robotron5exe/Garaza)
- **Issues**: [Report bugs or request features](https://github.com/robotron5exe/Garaza/issues)

## 🙏 Acknowledgments

- GURS and SORS for providing comprehensive real estate market data
- Real estate portals for current market listings
- Market analysts and researchers whose work informed this analysis
- The Slovenian real estate community for insights and context

---

**Last Updated**: November 9, 2025
**Data Coverage**: 2005-2025 (20 years)
**Geographic Focus**: Maribor, Slovenia
