"""
Garaza - Maribor Real Estate Market Analysis

A comprehensive package for analyzing real estate and garage prices in Maribor, Slovenia.
"""

__version__ = "1.0.0"
__author__ = "Garaza Project"

from .data_loader import (
    load_apartment_data,
    load_garage_data,
    load_national_data,
    load_all_data
)

from .analysis import (
    calculate_roi,
    calculate_appreciation,
    detect_market_phase,
    compare_investments,
    analyze_price_trends
)

from .visualization import (
    plot_price_trends,
    plot_market_phases,
    plot_roi_comparison,
    plot_location_comparison
)

__all__ = [
    # Data loading
    'load_apartment_data',
    'load_garage_data',
    'load_national_data',
    'load_all_data',

    # Analysis
    'calculate_roi',
    'calculate_appreciation',
    'detect_market_phase',
    'compare_investments',
    'analyze_price_trends',

    # Visualization
    'plot_price_trends',
    'plot_market_phases',
    'plot_roi_comparison',
    'plot_location_comparison',
]
