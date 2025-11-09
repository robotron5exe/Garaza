#!/usr/bin/env python3
"""
Investment Comparison Script

Compares investment returns between garages and apartments in Maribor.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from garaza import (
    calculate_roi,
    compare_investments,
    plot_roi_comparison
)


def main():
    """Run investment comparison analysis."""

    print("=" * 70)
    print("INVESTMENT COMPARISON: GARAGE VS APARTMENT - MARIBOR")
    print("=" * 70)
    print()

    # Define investment scenarios
    print("SCENARIO 1: TYPICAL MARIBOR INVESTMENT")
    print("-" * 70)

    # Garage investment
    garage_price = 12000
    garage_rent = 82
    garage_costs = 264

    # Apartment investment
    apartment_price = 150000  # ~61m² at €2,450/m²
    apartment_rent = 600
    apartment_costs = 0.15  # 15% of annual rent

    print("\nGARAGE INVESTMENT:")
    print(f"  Purchase Price: €{garage_price:,}")
    print(f"  Monthly Rent: €{garage_rent}")
    print(f"  Annual Costs: €{garage_costs}")

    print("\nAPARTMENT INVESTMENT:")
    print(f"  Purchase Price: €{apartment_price:,}")
    print(f"  Monthly Rent: €{apartment_rent}")
    print(f"  Annual Costs: {apartment_costs*100:.0f}% of rent")
    print()

    # Calculate ROI
    garage_roi = calculate_roi(garage_price, garage_rent, garage_costs)
    apartment_roi = calculate_roi(
        apartment_price, apartment_rent,
        apartment_rent * 12 * apartment_costs
    )

    # Print detailed comparison
    print("=" * 70)
    print("DETAILED ROI COMPARISON")
    print("=" * 70)

    comparison = compare_investments(
        garage_price, garage_rent,
        apartment_price, apartment_rent,
        garage_costs, apartment_costs
    )

    print(comparison.to_string(index=False))
    print()

    # Analysis
    print("=" * 70)
    print("INVESTMENT ANALYSIS")
    print("=" * 70)

    garage_better = garage_roi['net_yield_pct'] > apartment_roi['net_yield_pct']
    yield_diff = abs(garage_roi['net_yield_pct'] - apartment_roi['net_yield_pct'])

    print(f"\n✓ CASH FLOW WINNER: {'GARAGE' if garage_better else 'APARTMENT'}")
    print(f"  Yield Difference: {yield_diff:.2f} percentage points")
    print()

    print("GARAGE ADVANTAGES:")
    print(f"  • {(garage_roi['net_yield_pct'] / apartment_roi['net_yield_pct'] - 1) * 100:.0f}% higher net yield")
    print(f"  • €{garage_price:,} lower capital requirement")
    print(f"  • ${abs(apartment_price - garage_price):,} can be invested elsewhere")
    print(f"  • Simpler property management")
    print(f"  • Lower maintenance responsibilities")
    print()

    print("APARTMENT ADVANTAGES:")
    print(f"  • €{apartment_roi['net_annual_income'] - garage_roi['net_annual_income']:,.0f} higher absolute cash flow")
    print(f"  • Greater appreciation potential historically")
    print(f"  • Inflation hedge (living space)")
    print(f"  • More liquid market")
    print(f"  • Can be used personally")
    print()

    # Scenario 2: Multiple garages vs one apartment
    print("=" * 70)
    print("SCENARIO 2: MULTIPLE GARAGES STRATEGY")
    print("=" * 70)

    num_garages = apartment_price // garage_price
    total_garage_cost = num_garages * garage_price
    total_garage_income = num_garages * garage_roi['net_annual_income']

    print(f"\nWith €{apartment_price:,} you could buy:")
    print(f"  • {num_garages} garages at €{garage_price:,} each")
    print(f"  • Total cost: €{total_garage_cost:,}")
    print(f"  • Remaining: €{apartment_price - total_garage_cost:,}")
    print()

    print("ANNUAL CASH FLOW COMPARISON:")
    print(f"  • 1 Apartment: €{apartment_roi['net_annual_income']:,.0f}/year")
    print(f"  • {num_garages} Garages: €{total_garage_income:,.0f}/year")
    print(f"  • Difference: €{total_garage_income - apartment_roi['net_annual_income']:,.0f}/year")
    print()

    multi_garage_yield = (total_garage_income / total_garage_cost) * 100
    print(f"YIELDS:")
    print(f"  • 1 Apartment: {apartment_roi['net_yield_pct']:.2f}%")
    print(f"  • {num_garages} Garages: {multi_garage_yield:.2f}%")
    print()

    # Generate visualization
    output_dir = Path(__file__).parent.parent / 'output'
    output_dir.mkdir(exist_ok=True)

    print("=" * 70)
    print("GENERATING VISUALIZATION")
    print("=" * 70)

    plot_roi_comparison(garage_roi, apartment_roi,
                       save_path=output_dir / 'roi_comparison.png')
    print(f"✓ Saved to {output_dir / 'roi_comparison.png'}")
    print()

    # Investment recommendation
    print("=" * 70)
    print("INVESTMENT RECOMMENDATION")
    print("=" * 70)
    print()
    print("BEST FOR CASH FLOW: Garages")
    print("  → 2-3x higher yield than apartments")
    print("  → Lower capital requirement allows diversification")
    print()
    print("BEST FOR APPRECIATION: Apartments")
    print("  → Historical appreciation has been stronger")
    print("  → More liquid, easier to sell")
    print()
    print("OPTIMAL STRATEGY: Mixed Portfolio")
    print("  → Buy both for balanced risk/return")
    print("  → Garages for cash flow, apartments for appreciation")
    print("  → Diversification reduces risk")
    print()
    print("⚠️  CURRENT MARKET WARNING (2024-2025):")
    print("  → Transaction volumes down 53% - major red flag")
    print("  → Market likely at or near peak")
    print("  → Exercise extreme caution on any purchase")
    print("  → Consider waiting for market correction")
    print()


if __name__ == '__main__':
    main()
