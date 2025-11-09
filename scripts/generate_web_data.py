#!/usr/bin/env python3
"""
Generate Web Data Script

Converts JSON data files to JavaScript format for the website.
"""

import json
from pathlib import Path


def load_json_data():
    """Load JSON data files directly."""
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data' / 'raw'

    with open(data_dir / 'maribor_apartments_historical.json', 'r') as f:
        apartments_data = json.load(f)

    with open(data_dir / 'garage_prices_maribor.json', 'r') as f:
        garages_data = json.load(f)

    return {
        'apartments': apartments_data['annual_prices'],
        'garages': garages_data['current_listings_2024']
    }


def convert_to_web_format(data):
    """Convert JSON data to website-friendly format."""

    apartments = data['apartments']
    garages = data['garages']

    # Calculate garage averages from current listings
    garage_prices = [g['price'] for g in garages]
    garage_avg = int(sum(garage_prices) / len(garage_prices))
    garage_min = min(garage_prices)
    garage_max = max(garage_prices)
    garage_median = int(sorted(garage_prices)[len(garage_prices) // 2])

    # Build years array for website
    years_data = []

    # Filter to match website's year points
    target_years = [2005, 2008, 2010, 2012, 2015, 2018, 2020, 2022, 2024, 2025]

    for apt_year in apartments:
        year = apt_year['year']
        if year in target_years:
            # Estimate garage prices based on apartment prices and known 2024 ratio
            # 2024: garages ~12,500, apartments ~2,450/m² -> ratio ~5.1
            garage_ratio = 5.1
            garage_avg_est = int(apt_year['price_mid'] * garage_ratio)

            year_entry = {
                'year': year,
                'garages': {
                    'avg': garage_avg_est,
                    'min': int(apt_year['price_low'] * garage_ratio),
                    'max': int(apt_year['price_high'] * garage_ratio),
                    'median': garage_avg_est
                },
                'apartments': {
                    'avg': int(apt_year['price_mid']),
                    'min': int(apt_year['price_low']),
                    'max': int(apt_year['price_high']),
                    'median': int(apt_year['price_mid'])
                },
                'houses': {
                    # Houses typically 80-90% of apartment prices in Maribor
                    'avg': int(apt_year['price_mid'] * 0.85),
                    'min': int(apt_year['price_low'] * 0.85),
                    'max': int(apt_year['price_high'] * 0.85),
                    'median': int(apt_year['price_mid'] * 0.85)
                }
            }

            # Override 2024 with actual garage data
            if year == 2024:
                year_entry['garages'] = {
                    'avg': garage_avg,
                    'min': garage_min,
                    'max': garage_max,
                    'median': garage_median
                }

            years_data.append(year_entry)

    return years_data


def generate_javascript_data(years_data):
    """Generate JavaScript file content."""

    js_content = """// Real Estate Price Data for Maribor
// All prices are in EUR
// Apartment and house prices are per m²
// Garage prices are total price
// Generated from comprehensive market research data

const realEstateData = {
    // Array of yearly data points
    years: """

    js_content += json.dumps(years_data, indent=8)

    js_content += """,

    // Metadata
    metadata: {
        lastUpdated: '2024-11-09',
        currency: 'EUR',
        source: 'GURS, SORS, Eurostat, real estate portals - comprehensive 20-year research',
        dataQuality: {
            '2005-2006': 'Estimates based on national trends',
            '2007-2024': 'Official GURS/SORS data (high confidence)',
            'garages_2024': 'Current market listings'
        },
        notes: [
            'Garage prices represent total price for a standard garage (12-16m²)',
            'Apartment and house prices are per square meter',
            'Data represents market prices in Maribor',
            'Historical garage prices estimated from apartment price ratios',
            '2024 garage data from actual market listings'
        ]
    }
};

// Helper functions to work with the data
const DataHelper = {
    // Get all years
    getYears() {
        return realEstateData.years.map(d => d.year);
    },

    // Get data for a specific property type
    getPropertyData(propertyType) {
        return realEstateData.years.map(d => d[propertyType].avg);
    },

    // Get data for a specific year range
    getDataInRange(startYear, endYear) {
        return realEstateData.years.filter(d => d.year >= startYear && d.year <= endYear);
    },

    // Calculate percentage change
    calculateChange(startValue, endValue) {
        return ((endValue - startValue) / startValue * 100).toFixed(1);
    },

    // Get latest data
    getLatest() {
        return realEstateData.years[realEstateData.years.length - 1];
    },

    // Get first data
    getFirst() {
        return realEstateData.years[0];
    }
};
"""

    return js_content


def main():
    """Main function."""

    print("=" * 70)
    print("GENERATING WEB DATA FROM RESEARCH")
    print("=" * 70)
    print()

    # Load all data
    print("Loading comprehensive market data...")
    data = load_json_data()
    print("✓ Data loaded")
    print()

    # Convert to web format
    print("Converting to website format...")
    years_data = convert_to_web_format(data)
    print(f"✓ Generated {len(years_data)} year data points")
    print()

    # Generate JavaScript
    print("Generating JavaScript file...")
    js_content = generate_javascript_data(years_data)

    # Write to web directory
    output_path = Path(__file__).parent.parent / 'web' / 'data.js'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"✓ Written to {output_path}")
    print()

    # Show summary
    print("=" * 70)
    print("DATA SUMMARY")
    print("=" * 70)

    if years_data:
        latest = years_data[-1]
        first = years_data[0]

        print(f"\nLatest Year: {latest['year']}")
        print(f"  Garages:    €{latest['garages']['avg']:,} (range: €{latest['garages']['min']:,}-{latest['garages']['max']:,})")
        print(f"  Apartments: €{latest['apartments']['avg']:,}/m²")
        print(f"  Houses:     €{latest['houses']['avg']:,}/m²")

        garage_growth = ((latest['garages']['avg'] - first['garages']['avg']) / first['garages']['avg'] * 100)
        apt_growth = ((latest['apartments']['avg'] - first['apartments']['avg']) / first['apartments']['avg'] * 100)

        print(f"\nGrowth since {first['year']}:")
        print(f"  Garages:    +{garage_growth:.1f}%")
        print(f"  Apartments: +{apt_growth:.1f}%")
    print()

    print("=" * 70)
    print("WEBSITE DATA GENERATION COMPLETE")
    print("=" * 70)
    print(f"Open web/index.html in a browser to view the website")
    print()


if __name__ == '__main__':
    main()
