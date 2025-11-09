# Getting Started with Garaza

Quick start guide for using the Maribor Real Estate Analysis project.

## Installation

### 1. Clone and Setup

```bash
git clone https://github.com/robotron5exe/Garaza.git
cd Garaza

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Verify Installation

```python
# Test import
python -c "from garaza import load_apartment_data; print('✓ Installation successful!')"
```

## Quick Analysis

### Run the Quick Analysis Script

```bash
python scripts/quick_analysis.py
```

This will show you:
- Current market prices (2024)
- Transaction volumes
- Market phase analysis
- Investment metrics
- Historical performance
- 2025 outlook and recommendations

**Output example:**
```
📊 CURRENT MARKET SNAPSHOT (2024)
💰 APARTMENT PRICES:
   City Center:    €2,666/m²
   Outside Center: €2,100/m²
   Market Average: €2,450/m²
   YoY Change:     +6.1%
...
```

## Detailed Analysis

### 1. Price Trends Analysis

```bash
python scripts/price_trends_analysis.py
```

Generates:
- `output/price_trends.png` - 20-year price history with market phases
- `output/market_phases.png` - Prices and volumes with annotations
- `output/yoy_changes.png` - Year-over-year growth rates
- `output/location_comparison.png` - Maribor vs Ljubljana comparison

### 2. Investment Comparison

```bash
python scripts/investment_comparison.py
```

Compares:
- Garage vs apartment ROI
- Cash flow analysis
- Multiple garages strategy
- Investment recommendations

Generates:
- `output/roi_comparison.png` - Visual ROI comparison

## Using the Python API

### Load Data

```python
from garaza import load_apartment_data, load_garage_data

# Load apartment prices
apartments = load_apartment_data()
print(apartments.head())

# Load garage data
garages = load_garage_data('maribor')
print(garages[['location', 'price', 'price_per_sqm']])
```

### Calculate ROI

```python
from garaza import calculate_roi

# Calculate garage investment ROI
roi = calculate_roi(
    purchase_price=12000,
    monthly_rent=82,
    annual_costs=264
)

print(f"Net Yield: {roi['net_yield_pct']:.2f}%")
print(f"Monthly Cash Flow: €{roi['monthly_cash_flow']:.0f}")
```

### Analyze Market Phase

```python
from garaza import detect_market_phase

phase = detect_market_phase(
    transaction_volume_change=-52.95,  # 2024 data
    price_change=6.1
)

print(f"Market Phase: {phase['phase']}")
print(f"Risk Level: {phase['risk_level']}")
```

### Compare Investments

```python
from garaza import compare_investments

comparison = compare_investments(
    garage_price=12000,
    garage_rent=82,
    apartment_price=150000,
    apartment_rent=600
)

print(comparison)
```

### Visualize Data

```python
from garaza import load_apartment_data, plot_price_trends
import matplotlib.pyplot as plt

apartments = load_apartment_data()
plot_price_trends(apartments, show_market_phases=True)
plt.show()
```

## Data Files

All data is stored in JSON format in `data/raw/`:

- **`maribor_apartments_historical.json`** - 20 years of apartment prices
- **`garage_prices_maribor.json`** - Current garage listings and historical estimates
- **`garage_prices_ljubljana.json`** - Ljubljana comparison data
- **`slovenia_national_market.json`** - National market context

### Example: Reading Raw Data

```python
import json

with open('data/raw/maribor_apartments_historical.json', 'r') as f:
    data = json.load(f)

# Get current market metrics
metrics = data['current_market_data_2025']
print(f"City Center: €{metrics['city_center']['price_per_sqm']}/m²")
```

## Common Tasks

### 1. Find Cheapest Garages

```python
from garaza import load_garage_data

garages = load_garage_data('maribor')
cheapest = garages.nsmallest(5, 'price')
print(cheapest[['location', 'size_sqm', 'price', 'price_per_sqm']])
```

### 2. Calculate Historical Returns

```python
from garaza import load_apartment_data, calculate_appreciation

apartments = load_apartment_data()
price_2005 = apartments[apartments['year'].dt.year == 2005].iloc[0]['price_mid']
price_2024 = apartments[apartments['year'].dt.year == 2024].iloc[0]['price_mid']

appreciation = calculate_appreciation(
    initial_price=price_2005,
    final_price=price_2024,
    years=19,
    inflation_rate=0.025  # 2.5% average inflation
)

print(f"Total Return: {appreciation['total_appreciation_pct']:.1f}%")
print(f"CAGR: {appreciation['cagr_pct']:.1f}%")
print(f"Real Return: {appreciation['real_appreciation_pct']:.1f}%")
```

### 3. Analyze Specific Year

```python
from garaza import load_apartment_data

apartments = load_apartment_data()
year_2021 = apartments[apartments['year'].dt.year == 2021].iloc[0]

print(f"2021 Price: €{year_2021['price_mid']}/m²")
print(f"YoY Change: +{year_2021['yoy_change']:.1f}%")
print(f"Notes: {year_2021['notes']}")
```

## Advanced Analysis

### Custom Market Statistics

```python
from garaza import load_apartment_data
from garaza.analysis import calculate_market_statistics

apartments = load_apartment_data()
stats = calculate_market_statistics(apartments, price_col='price_mid')

print(f"Mean: €{stats['mean']:,.0f}/m²")
print(f"Volatility: {stats['volatility']:.1f}%")
print(f"Max Gain: {stats['max_gain']:.1f}%")
print(f"Max Loss: {stats['max_loss']:.1f}%")
```

### Trend Analysis

```python
from garaza import load_apartment_data, analyze_price_trends

apartments = load_apartment_data()
trends = analyze_price_trends(apartments, window=3)

# Show trends for last 5 years
recent = trends[trends['year'].dt.year >= 2020]
print(recent[['year', 'price_mid', 'yoy_change', 'trend']])
```

## Troubleshooting

### Import Errors

If you get `ModuleNotFoundError: No module named 'garaza'`:

```bash
# Make sure you're in the project directory
cd /path/to/Garaza

# Install in development mode
pip install -e .
```

Or add to Python path:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
```

### Data File Not Found

```python
# Specify custom data directory
from garaza import DataLoader

loader = DataLoader(data_dir='/custom/path/to/data')
apartments = loader.load_apartments()
```

### Visualization Issues

```bash
# Install matplotlib backend for your system
pip install matplotlib pyqt5  # For Qt backend

# Or use non-interactive backend
import matplotlib
matplotlib.use('Agg')
```

## Next Steps

1. **Read the full analysis**: [maribor-real-estate-analysis-2005-2025.md](../maribor-real-estate-analysis-2005-2025.md)

2. **Explore the code**: Check `src/garaza/` for implementation details

3. **Run all analyses**: Execute all scripts in `scripts/` directory

4. **Customize**: Modify scripts for your specific analysis needs

5. **Contribute**: Submit issues or PRs on GitHub

## Key Insights Summary

🟢 **Positive Indicators:**
- 20-year appreciation: 80-100% nominal
- Garages offer 6-7% net yields (excellent cash flow)
- Maribor 45-50% cheaper than Ljubljana
- Prices continuing to rise (+8.38% in 2024)

🔴 **Warning Signals:**
- Transaction volumes crashed 53% in 2024
- Market likely at or near peak
- Price-to-income ratio: 7.06 (stretched)
- Limited upside potential

💡 **Investment Strategy:**
- **For Cash Flow**: Garages are superior (6-7% vs 2.5-3.5%)
- **For Appreciation**: Wait for market correction
- **Current Market**: Exercise extreme caution
- **Best Play**: Patience - wait for better entry point

---

**For more help:**
- Full documentation: [README.md](../README.md)
- Detailed report: [maribor-real-estate-analysis-2005-2025.md](../maribor-real-estate-analysis-2005-2025.md)
- Issues: https://github.com/robotron5exe/Garaza/issues
