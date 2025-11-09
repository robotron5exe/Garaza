#!/usr/bin/env python3
"""
Quick Analysis Script

Fast overview of current market conditions and key metrics.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from garaza import load_all_data
from garaza.analysis import detect_market_phase, calculate_roi


def print_section(title):
    """Print formatted section header."""
    print("\n" + "=" * 70)
    print(title.center(70))
    print("=" * 70)


def main():
    """Run quick market analysis."""

    print("\n" + "🏠" * 35)
    print("MARIBOR REAL ESTATE - QUICK MARKET ANALYSIS".center(70))
    print("🏠" * 35)

    # Load data
    data = load_all_data()
    apartments = data['apartments']
    garages_mb = data['garages_maribor']
    metrics = data['metrics']
    volumes = data['volumes']

    # Current prices (2024)
    current_2024 = apartments[apartments['year'].dt.year == 2024].iloc[0]
    forecast_2025 = apartments[apartments['year'].dt.year == 2025].iloc[0]

    print_section("📊 CURRENT MARKET SNAPSHOT (2024)")

    print("\n💰 APARTMENT PRICES:")
    print(f"   City Center:    €{metrics['city_center']['price_per_sqm']:,.0f}/m²")
    print(f"   Outside Center: €{metrics['outside_center']['price_per_sqm']:,.0f}/m²")
    print(f"   Market Average: €{current_2024['price_mid']:,.0f}/m²")
    print(f"   YoY Change:     +{current_2024['yoy_change']:.1f}%")

    print("\n🚗 GARAGE PRICES (Maribor):")
    print(f"   Average:        €{garages_mb['price'].mean():,.0f}")
    print(f"   Range:          €{garages_mb['price'].min():,.0f} - €{garages_mb['price'].max():,.0f}")
    print(f"   Price/m²:       €{garages_mb['price_per_sqm'].mean():,.0f}/m²")

    print("\n📈 TRANSACTION VOLUMES:")
    vol_2024 = volumes[volumes['year'].dt.year == 2024].iloc[0]
    vol_2023 = volumes[volumes['year'].dt.year == 2023].iloc[0]
    print(f"   2024:           {vol_2024['maribor_actual']} apartments")
    print(f"   2023:           {vol_2023['maribor_estimate']} apartments (est.)")
    print(f"   YoY Change:     {vol_2024['yoy_change']:.1f}% 🔴")

    # Market phase detection
    print_section("🔍 MARKET PHASE ANALYSIS")

    phase = detect_market_phase(
        transaction_volume_change=vol_2024['yoy_change'],
        price_change=current_2024['yoy_change']
    )

    print(f"\n   Phase:          {phase['phase']}")
    print(f"   Risk Level:     {phase['risk_level']}")
    print(f"   Description:    {phase['description']}")

    print("\n   ⚠️  SIGNALS:")
    for signal in phase['signals']:
        print(f"      • {signal.replace('_', ' ')}")

    # Investment metrics
    print_section("💵 INVESTMENT METRICS")

    print("\n🏢 APARTMENTS:")
    print(f"   Price-to-Income:     {metrics['investment_metrics']['price_to_income_ratio']:.2f}x")
    print(f"   Mortgage % Income:   {metrics['investment_metrics']['mortgage_pct_income']:.1f}%")
    print(f"   Rental Yield (City): {metrics['investment_metrics']['gross_rental_yield_city']:.2f}%")
    print(f"   Net Yield:           ~2.5-3.5%")

    # Garage ROI example
    garage_roi = calculate_roi(12000, 82, 264)
    print("\n🚗 GARAGES (Example: €12,000):")
    print(f"   Gross Yield:         {garage_roi['gross_yield_pct']:.2f}%")
    print(f"   Net Yield:           {garage_roi['net_yield_pct']:.2f}%")
    print(f"   Monthly Cash Flow:   €{garage_roi['monthly_cash_flow']:.0f}")

    # Historical performance
    print_section("📈 HISTORICAL PERFORMANCE (20 YEARS)")

    price_2005 = apartments[apartments['year'].dt.year == 2005].iloc[0]['price_mid']
    price_2024 = current_2024['price_mid']

    total_return = ((price_2024 - price_2005) / price_2005) * 100
    cagr = (((price_2024 / price_2005) ** (1/19)) - 1) * 100

    print(f"\n   2005 Price:          €{price_2005:,.0f}/m²")
    print(f"   2024 Price:          €{price_2024:,.0f}/m²")
    print(f"   Total Return:        +{total_return:.1f}%")
    print(f"   CAGR:                +{cagr:.1f}%")
    print(f"   Real Return (est.):  ~40-50% (inflation-adjusted)")

    # Key milestones
    print("\n   🏆 KEY MILESTONES:")
    price_2008 = apartments[apartments['year'].dt.year == 2008].iloc[0]['price_mid']
    price_2014 = apartments[apartments['year'].dt.year == 2014].iloc[0]['price_mid']
    price_2021 = apartments[apartments['year'].dt.year == 2021].iloc[0]['price_mid']

    print(f"      2008 Peak:        €{price_2008:,.0f}/m²")
    print(f"      2014 Bottom:      €{price_2014:,.0f}/m² (-{((price_2008-price_2014)/price_2008)*100:.1f}%)")
    print(f"      2021 Boom:        €{price_2021:,.0f}/m² (+{apartments[apartments['year'].dt.year == 2021].iloc[0]['yoy_change']:.1f}%)")

    # Outlook
    print_section("🔮 2025 OUTLOOK")

    print(f"\n   Forecast Price:      €{forecast_2025['price_mid']:,.0f}/m²")
    print(f"   Expected Change:     +{forecast_2025['yoy_change']:.1f}%")
    print(f"   Market Direction:    Cooling/Stabilization")

    print("\n   ⚠️  INVESTMENT WARNINGS:")
    print("      • Transaction volumes collapsed (-53%)")
    print("      • Market likely at or near peak")
    print("      • Price-to-income ratio stretched (7.06x)")
    print("      • Limited upside potential")
    print("      • Significant downside risk")

    print("\n   ✅ POTENTIAL OPPORTUNITIES:")
    print("      • Garages offer superior cash flow (6-7% net)")
    print("      • Maribor 45-50% cheaper than Ljubljana")
    print("      • Wait for market correction (better entry)")
    print("      • Focus on cash-flowing assets if buying")

    # Quick recommendation
    print_section("🎯 QUICK RECOMMENDATION")

    avg_salary = metrics['economic_context']['avg_monthly_net_salary']
    annual_salary = avg_salary * 12

    print(f"\n   Average Salary:      €{avg_salary:,.0f}/month (€{annual_salary:,.0f}/year)")
    print(f"   60m² Apartment:      €{60 * price_2024:,.0f}")
    print(f"   Years of Salary:     {(60 * price_2024) / annual_salary:.1f} years")

    print("\n   FOR INVESTORS:")
    print("      🟡 HOLD: If you own property, consider holding")
    print("      🔴 CAUTION: If buying, extreme caution advised")
    print("      🟢 GARAGE: Best cash flow option currently")
    print("      ⏸️  WAIT: Consider waiting for correction")

    print("\n   FOR HOMEBUYERS:")
    print("      ⏸️  PATIENCE: Transaction volume collapse suggests")
    print("         sellers may become more flexible")
    print("      💰 NEGOTIATE: Strong bargaining position")
    print("      📊 RESEARCH: Focus on fundamental value")
    print("      🏠 NEED: Only buy if you genuinely need housing")

    print("\n" + "=" * 70)
    print("Analysis complete! For detailed analysis, run:")
    print("  python scripts/price_trends_analysis.py")
    print("  python scripts/investment_comparison.py")
    print("=" * 70)
    print()


if __name__ == '__main__':
    main()
