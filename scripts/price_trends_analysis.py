#!/usr/bin/env python3
"""
Price Trends Analysis Script

Analyzes historical price trends for Maribor real estate market
and generates comprehensive visualizations.
"""

import sys
from pathlib import Path

# Add parent directory to path to import garaza package
sys.path.insert(0, str(Path(__file__).parent.parent))

from garaza import (
    load_apartment_data,
    load_garage_data,
    load_all_data,
    analyze_price_trends,
    calculate_market_statistics,
    plot_price_trends,
    plot_market_phases,
    plot_yoy_changes,
    plot_location_comparison
)


def main():
    """Run complete price trends analysis."""

    print("=" * 60)
    print("MARIBOR REAL ESTATE MARKET - PRICE TRENDS ANALYSIS")
    print("=" * 60)
    print()

    # Load data
    print("Loading data...")
    data = load_all_data()

    apartments = data['apartments']
    garages_mb = data['garages_maribor']
    garages_lj = data['garages_ljubljana']
    volumes = data['volumes']

    print(f"✓ Loaded {len(apartments)} years of apartment data")
    print(f"✓ Loaded {len(garages_mb)} Maribor garage listings")
    print(f"✓ Loaded {len(garages_lj)} Ljubljana garage listings")
    print()

    # Analyze trends
    print("Analyzing price trends...")
    trends = analyze_price_trends(apartments)

    # Calculate statistics
    stats = calculate_market_statistics(apartments)

    print("\n" + "=" * 60)
    print("MARKET STATISTICS (2005-2025)")
    print("=" * 60)
    print(f"Mean Price: €{stats['mean']:,.0f}/m²")
    print(f"Median Price: €{stats['median']:,.0f}/m²")
    print(f"Price Range: €{stats['min']:,.0f} - €{stats['max']:,.0f}")
    print(f"Total Return: {stats['total_return_pct']:.1f}%")
    print(f"CAGR: {stats['cagr_pct']:.1f}%")
    print(f"Volatility: {stats['volatility']:.1f}%")
    print()

    # Current market phase
    print("=" * 60)
    print("CURRENT MARKET ANALYSIS (2024)")
    print("=" * 60)

    latest = apartments.iloc[-2]  # 2024 (last is forecast)
    prev = apartments.iloc[-3]     # 2023

    vol_2024 = volumes[volumes['year'].dt.year == 2024].iloc[0]
    vol_2023 = volumes[volumes['year'].dt.year == 2023].iloc[0]

    volume_change = ((vol_2024['maribor_actual'] - vol_2023['maribor_estimate']) /
                    vol_2023['maribor_estimate'] * 100)

    print(f"2024 Price: €{latest['price_mid']:,.0f}/m²")
    print(f"YoY Price Change: +{latest['yoy_change']:.1f}%")
    print(f"Transaction Volume: {vol_2024['maribor_actual']}")
    print(f"YoY Volume Change: {volume_change:.1f}%")
    print()

    from garaza.analysis import detect_market_phase
    phase = detect_market_phase(
        transaction_volume_change=volume_change,
        price_change=latest['yoy_change']
    )

    print(f"Market Phase: {phase['phase']}")
    print(f"Risk Level: {phase['risk_level']}")
    print(f"Description: {phase['description']}")
    print()

    # Generate visualizations
    print("=" * 60)
    print("GENERATING VISUALIZATIONS")
    print("=" * 60)

    output_dir = Path(__file__).parent.parent / 'output'
    output_dir.mkdir(exist_ok=True)

    # 1. Price trends
    print("1. Plotting price trends with market phases...")
    plot_price_trends(apartments, save_path=output_dir / 'price_trends.png')
    print(f"   ✓ Saved to {output_dir / 'price_trends.png'}")

    # 2. Market phases with volumes
    print("2. Plotting market phases...")
    plot_market_phases(apartments, volume_data=volumes,
                      save_path=output_dir / 'market_phases.png')
    print(f"   ✓ Saved to {output_dir / 'market_phases.png'}")

    # 3. Year-over-year changes
    print("3. Plotting YoY price changes...")
    plot_yoy_changes(apartments, save_path=output_dir / 'yoy_changes.png')
    print(f"   ✓ Saved to {output_dir / 'yoy_changes.png'}")

    # 4. Location comparison
    print("4. Plotting location comparison...")
    plot_location_comparison(garages_mb, garages_lj,
                            save_path=output_dir / 'location_comparison.png')
    print(f"   ✓ Saved to {output_dir / 'location_comparison.png'}")

    print()
    print("=" * 60)
    print("ANALYSIS COMPLETE!")
    print("=" * 60)
    print(f"All visualizations saved to: {output_dir}")
    print()


if __name__ == '__main__':
    main()
