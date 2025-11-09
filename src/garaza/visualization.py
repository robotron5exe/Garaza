"""
Visualization functions for real estate market data.
"""

from typing import Optional, List, Tuple
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Set default style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def plot_price_trends(df: pd.DataFrame,
                     price_cols: Optional[List[str]] = None,
                     show_market_phases: bool = True,
                     title: str = "Maribor Apartment Prices (2005-2025)",
                     save_path: Optional[str] = None):
    """
    Plot historical price trends.

    Args:
        df: DataFrame with price data
        price_cols: List of price columns to plot (default: ['price_low', 'price_mid', 'price_high'])
        show_market_phases: Whether to highlight market phases
        title: Plot title
        save_path: Optional path to save the figure
    """
    if price_cols is None:
        price_cols = ['price_low', 'price_mid', 'price_high']

    fig, ax = plt.subplots(figsize=(14, 7))

    # Plot price trends
    for col in price_cols:
        if col in df.columns:
            label = col.replace('price_', '').replace('_', ' ').title()
            ax.plot(df['year'], df[col], marker='o', label=label, linewidth=2)

    # Highlight market phases
    if show_market_phases:
        # Boom (2005-2008)
        ax.axvspan(pd.Timestamp('2005-01-01'), pd.Timestamp('2008-12-31'),
                  alpha=0.1, color='green', label='Boom')
        # Crash (2008-2014)
        ax.axvspan(pd.Timestamp('2008-12-31'), pd.Timestamp('2014-12-31'),
                  alpha=0.1, color='red', label='Crash')
        # Recovery (2015-2021)
        ax.axvspan(pd.Timestamp('2015-01-01'), pd.Timestamp('2021-12-31'),
                  alpha=0.1, color='blue', label='Recovery')
        # Late Cycle (2022+)
        ax.axvspan(pd.Timestamp('2022-01-01'), pd.Timestamp('2025-12-31'),
                  alpha=0.1, color='orange', label='Late Cycle')

    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Price per m² (EUR)', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)

    # Format y-axis with EUR symbol
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'€{x:,.0f}'))

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig, ax


def plot_market_phases(df: pd.DataFrame,
                      price_col: str = 'price_mid',
                      volume_data: Optional[pd.DataFrame] = None,
                      save_path: Optional[str] = None):
    """
    Plot price and volume trends with phase annotations.

    Args:
        df: DataFrame with price data
        price_col: Column name for price
        volume_data: Optional DataFrame with transaction volumes
        save_path: Optional path to save the figure
    """
    if volume_data is not None:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
    else:
        fig, ax1 = plt.subplots(figsize=(14, 7))

    # Plot prices
    ax1.plot(df['year'], df[price_col], marker='o', linewidth=2.5,
            color='#2E86AB', label='Price per m²')
    ax1.fill_between(df['year'], df['price_low'], df['price_high'],
                     alpha=0.2, color='#2E86AB')

    # Annotations for key events
    annotations = [
        (pd.Timestamp('2008-07-01'), df.loc[df['year'].dt.year == 2008, price_col].values[0],
         'Peak\n2008', 'red'),
        (pd.Timestamp('2014-07-01'), df.loc[df['year'].dt.year == 2014, price_col].values[0],
         'Bottom\n2014', 'green'),
        (pd.Timestamp('2021-07-01'), df.loc[df['year'].dt.year == 2021, price_col].values[0],
         'Boom\n2021', 'orange')
    ]

    for date, price, text, color in annotations:
        ax1.annotate(text, xy=(date, price), xytext=(10, 10),
                    textcoords='offset points', fontsize=10, fontweight='bold',
                    color=color, bbox=dict(boxstyle='round', facecolor='white',
                    edgecolor=color, alpha=0.8))

    ax1.set_ylabel('Price per m² (EUR)', fontsize=12, fontweight='bold')
    ax1.set_title('Maribor Real Estate: Prices and Market Phases',
                 fontsize=14, fontweight='bold', pad=20)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'€{x:,.0f}'))

    # Plot volumes if available
    if volume_data is not None:
        # Extract numeric column (could be estimate or actual)
        vol_col = 'maribor_actual' if 'maribor_actual' in volume_data.columns else 'maribor_estimate'

        ax2.bar(volume_data['year'], volume_data[vol_col], width=300,
               color='#A23B72', alpha=0.7, label='Transaction Volume')

        ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Number of Transactions', fontsize=12, fontweight='bold')
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig


def plot_roi_comparison(garage_roi: dict,
                       apartment_roi: dict,
                       title: str = "Investment ROI Comparison: Garage vs Apartment",
                       save_path: Optional[str] = None):
    """
    Plot ROI comparison between garage and apartment investments.

    Args:
        garage_roi: Dictionary with garage ROI metrics
        apartment_roi: Dictionary with apartment ROI metrics
        title: Plot title
        save_path: Optional path to save figure
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Yield comparison
    categories = ['Gross Yield', 'Net Yield']
    garage_yields = [garage_roi['gross_yield_pct'], garage_roi['net_yield_pct']]
    apartment_yields = [apartment_roi['gross_yield_pct'], apartment_roi['net_yield_pct']]

    x = np.arange(len(categories))
    width = 0.35

    bars1 = ax1.bar(x - width/2, garage_yields, width, label='Garage',
                   color='#00A896', alpha=0.8)
    bars2 = ax1.bar(x + width/2, apartment_yields, width, label='Apartment',
                   color='#F18F01', alpha=0.8)

    ax1.set_ylabel('Yield (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Rental Yields', fontsize=12, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories)
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')

    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontsize=10)

    # Cash flow comparison
    categories = ['Annual Income', 'Annual Costs', 'Net Cash Flow']
    garage_cash = [garage_roi['annual_rent'], garage_roi['annual_costs'],
                   garage_roi['net_annual_income']]
    apartment_cash = [apartment_roi['annual_rent'], apartment_roi['annual_costs'],
                     apartment_roi['net_annual_income']]

    x = np.arange(len(categories))

    bars1 = ax2.bar(x - width/2, garage_cash, width, label='Garage',
                   color='#00A896', alpha=0.8)
    bars2 = ax2.bar(x + width/2, apartment_cash, width, label='Apartment',
                   color='#F18F01', alpha=0.8)

    ax2.set_ylabel('Amount (EUR)', fontsize=12, fontweight='bold')
    ax2.set_title('Cash Flow Analysis', fontsize=12, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(categories, rotation=15, ha='right')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'€{x:,.0f}'))

    fig.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig


def plot_location_comparison(maribor_df: pd.DataFrame,
                            ljubljana_df: pd.DataFrame,
                            save_path: Optional[str] = None):
    """
    Compare garage prices between Maribor and Ljubljana.

    Args:
        maribor_df: DataFrame with Maribor garage data
        ljubljana_df: DataFrame with Ljubljana garage data
        save_path: Optional path to save figure
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Price comparison
    locations = ['Maribor', 'Ljubljana']
    avg_prices = [maribor_df['price'].mean(), ljubljana_df['price'].mean()]
    colors = ['#00A896', '#F18F01']

    bars = ax1.bar(locations, avg_prices, color=colors, alpha=0.7)
    ax1.set_ylabel('Average Price (EUR)', fontsize=12, fontweight='bold')
    ax1.set_title('Average Garage Prices', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'€{x:,.0f}'))

    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'€{height:,.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Price per sqm comparison
    avg_per_sqm = [maribor_df['price_per_sqm'].mean(),
                   ljubljana_df['price_per_sqm'].mean()]

    bars = ax2.bar(locations, avg_per_sqm, color=colors, alpha=0.7)
    ax2.set_ylabel('Price per m² (EUR)', fontsize=12, fontweight='bold')
    ax2.set_title('Price per Square Meter', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'€{x:,.0f}'))

    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'€{height:,.0f}/m²', ha='center', va='bottom',
                fontsize=11, fontweight='bold')

    # Calculate and show discount
    discount = ((avg_prices[1] - avg_prices[0]) / avg_prices[1]) * 100
    fig.text(0.5, 0.02, f'Maribor Discount: {discount:.1f}%',
            ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))

    fig.suptitle('Garage Price Comparison: Maribor vs Ljubljana',
                fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig


def plot_yoy_changes(df: pd.DataFrame,
                    save_path: Optional[str] = None):
    """
    Plot year-over-year price changes.

    Args:
        df: DataFrame with price data and yoy_change column
        save_path: Optional path to save figure
    """
    fig, ax = plt.subplots(figsize=(14, 7))

    # Filter out None/NaN values
    plot_df = df[df['yoy_change'].notna()].copy()

    # Create bar colors based on positive/negative
    colors = ['green' if x > 0 else 'red' for x in plot_df['yoy_change']]

    bars = ax.bar(plot_df['year'], plot_df['yoy_change'],
                 color=colors, alpha=0.6, edgecolor='black', linewidth=0.5)

    # Add horizontal line at 0
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1)

    # Highlight key periods
    ax.axhspan(-15, -5, alpha=0.1, color='red', label='Crisis Period')
    ax.axhspan(5, 20, alpha=0.1, color='green', label='Strong Growth')

    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Year-over-Year Change (%)', fontsize=12, fontweight='bold')
    ax.set_title('Annual Price Growth Rate - Maribor Apartments',
                fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')
    ax.legend(fontsize=10)

    # Add value labels on significant bars
    for i, (year, change) in enumerate(zip(plot_df['year'], plot_df['yoy_change'])):
        if abs(change) > 10:  # Only label significant changes
            ax.text(year, change, f'{change:.1f}%',
                   ha='center', va='bottom' if change > 0 else 'top',
                   fontsize=9, fontweight='bold')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig, ax
