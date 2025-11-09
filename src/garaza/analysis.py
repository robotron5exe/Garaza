"""
Analysis functions for real estate market data.
"""

from typing import Dict, Optional, Tuple
import pandas as pd
import numpy as np


def calculate_roi(purchase_price: float,
                  monthly_rent: float,
                  annual_costs: float = 0,
                  vacancy_rate: float = 0.05) -> Dict[str, float]:
    """
    Calculate return on investment for a property.

    Args:
        purchase_price: Property purchase price
        monthly_rent: Monthly rental income
        annual_costs: Annual operating costs (management, maintenance, etc.)
        vacancy_rate: Expected vacancy rate (default 5%)

    Returns:
        Dictionary with ROI metrics: gross_yield, net_yield, annual_cash_flow
    """
    annual_rent = monthly_rent * 12
    effective_rent = annual_rent * (1 - vacancy_rate)
    net_income = effective_rent - annual_costs

    gross_yield = (annual_rent / purchase_price) * 100
    net_yield = (net_income / purchase_price) * 100

    return {
        'annual_rent': annual_rent,
        'effective_rent': effective_rent,
        'annual_costs': annual_costs,
        'net_annual_income': net_income,
        'gross_yield_pct': gross_yield,
        'net_yield_pct': net_yield,
        'monthly_cash_flow': net_income / 12
    }


def calculate_appreciation(initial_price: float,
                          final_price: float,
                          years: int,
                          inflation_rate: Optional[float] = None) -> Dict[str, float]:
    """
    Calculate price appreciation over time.

    Args:
        initial_price: Starting price
        final_price: Ending price
        years: Number of years
        inflation_rate: Optional annual inflation rate for real appreciation

    Returns:
        Dictionary with appreciation metrics
    """
    total_appreciation = ((final_price - initial_price) / initial_price) * 100
    cagr = (((final_price / initial_price) ** (1 / years)) - 1) * 100

    result = {
        'initial_price': initial_price,
        'final_price': final_price,
        'years': years,
        'total_appreciation_pct': total_appreciation,
        'cagr_pct': cagr,
        'total_gain': final_price - initial_price
    }

    if inflation_rate is not None:
        real_final_price = final_price / ((1 + inflation_rate) ** years)
        real_appreciation = ((real_final_price - initial_price) / initial_price) * 100
        result['real_appreciation_pct'] = real_appreciation
        result['inflation_adjusted_price'] = real_final_price

    return result


def detect_market_phase(transaction_volume_change: float,
                       price_change: float,
                       yoy_price_change: Optional[float] = None) -> Dict[str, str]:
    """
    Detect current market phase based on indicators.

    Args:
        transaction_volume_change: YoY change in transaction volumes (%)
        price_change: Recent price change (%)
        yoy_price_change: Year-over-year price change (%)

    Returns:
        Dictionary with phase classification and signals
    """
    signals = []

    # Volume indicators
    if transaction_volume_change < -30:
        signals.append('CRITICAL_VOLUME_DECLINE')
        volume_signal = 'bearish'
    elif transaction_volume_change < -15:
        signals.append('SIGNIFICANT_VOLUME_DECLINE')
        volume_signal = 'bearish'
    elif transaction_volume_change > 15:
        signals.append('STRONG_VOLUME_GROWTH')
        volume_signal = 'bullish'
    else:
        volume_signal = 'neutral'

    # Price indicators
    if price_change > 10:
        signals.append('STRONG_PRICE_GROWTH')
        price_signal = 'bullish'
    elif price_change > 5:
        signals.append('MODERATE_PRICE_GROWTH')
        price_signal = 'bullish'
    elif price_change < -5:
        signals.append('PRICE_DECLINE')
        price_signal = 'bearish'
    else:
        price_signal = 'neutral'

    # Determine phase
    if volume_signal == 'bearish' and price_signal == 'bullish':
        phase = 'LATE_CYCLE_COOLING'
        risk = 'HIGH'
        description = 'Prices rising but volumes falling - classic late cycle warning'
    elif volume_signal == 'bearish' and price_signal == 'bearish':
        phase = 'DOWNTURN'
        risk = 'VERY_HIGH'
        description = 'Both prices and volumes declining - market correction'
    elif volume_signal == 'bullish' and price_signal == 'bearish':
        phase = 'RECOVERY_EARLY'
        risk = 'MEDIUM'
        description = 'Volumes increasing but prices still weak - potential bottom'
    elif volume_signal == 'bullish' and price_signal == 'bullish':
        phase = 'EXPANSION'
        risk = 'LOW'
        description = 'Both volumes and prices rising - healthy market growth'
    else:
        phase = 'STABLE'
        risk = 'MEDIUM'
        description = 'Market showing stability with neutral indicators'

    return {
        'phase': phase,
        'risk_level': risk,
        'description': description,
        'signals': signals,
        'volume_signal': volume_signal,
        'price_signal': price_signal
    }


def compare_investments(garage_price: float,
                       garage_rent: float,
                       apartment_price: float,
                       apartment_rent: float,
                       garage_costs: float = 264,
                       apartment_costs_pct: float = 0.15) -> pd.DataFrame:
    """
    Compare garage vs apartment investment.

    Args:
        garage_price: Garage purchase price
        garage_rent: Monthly garage rent
        apartment_price: Apartment purchase price
        apartment_rent: Monthly apartment rent
        garage_costs: Annual garage costs
        apartment_costs_pct: Apartment costs as % of rent (default 15%)

    Returns:
        DataFrame comparing the two investments
    """
    garage_roi = calculate_roi(garage_price, garage_rent, garage_costs)
    apartment_costs = apartment_rent * 12 * apartment_costs_pct
    apartment_roi = calculate_roi(apartment_price, apartment_rent, apartment_costs)

    comparison = pd.DataFrame({
        'Metric': [
            'Purchase Price',
            'Monthly Rent',
            'Annual Rent',
            'Annual Costs',
            'Net Annual Income',
            'Gross Yield (%)',
            'Net Yield (%)',
            'Monthly Cash Flow'
        ],
        'Garage': [
            f'€{garage_price:,.0f}',
            f'€{garage_rent:.0f}',
            f'€{garage_roi["annual_rent"]:,.0f}',
            f'€{garage_costs:.0f}',
            f'€{garage_roi["net_annual_income"]:,.0f}',
            f'{garage_roi["gross_yield_pct"]:.2f}%',
            f'{garage_roi["net_yield_pct"]:.2f}%',
            f'€{garage_roi["monthly_cash_flow"]:.0f}'
        ],
        'Apartment': [
            f'€{apartment_price:,.0f}',
            f'€{apartment_rent:.0f}',
            f'€{apartment_roi["annual_rent"]:,.0f}',
            f'€{apartment_costs:.0f}',
            f'€{apartment_roi["net_annual_income"]:,.0f}',
            f'{apartment_roi["gross_yield_pct"]:.2f}%',
            f'{apartment_roi["net_yield_pct"]:.2f}%',
            f'€{apartment_roi["monthly_cash_flow"]:.0f}'
        ]
    })

    return comparison


def analyze_price_trends(df: pd.DataFrame,
                        price_col: str = 'price_mid',
                        window: int = 3) -> pd.DataFrame:
    """
    Analyze price trends with moving averages and momentum.

    Args:
        df: DataFrame with price data
        price_col: Column name for price data
        window: Window size for moving average

    Returns:
        DataFrame with trend analysis
    """
    result = df.copy()

    # Calculate moving average
    result['ma'] = result[price_col].rolling(window=window).mean()

    # Calculate year-over-year change
    result['yoy_change'] = result[price_col].pct_change() * 100

    # Calculate momentum (acceleration)
    result['momentum'] = result['yoy_change'].diff()

    # Trend classification
    result['trend'] = 'neutral'
    result.loc[result['yoy_change'] > 5, 'trend'] = 'strong_growth'
    result.loc[(result['yoy_change'] > 0) & (result['yoy_change'] <= 5), 'trend'] = 'moderate_growth'
    result.loc[(result['yoy_change'] < 0) & (result['yoy_change'] >= -5), 'trend'] = 'moderate_decline'
    result.loc[result['yoy_change'] < -5, 'trend'] = 'strong_decline'

    return result


def calculate_market_statistics(df: pd.DataFrame,
                               price_col: str = 'price_mid') -> Dict:
    """
    Calculate comprehensive market statistics.

    Args:
        df: DataFrame with price data
        price_col: Column name for price data

    Returns:
        Dictionary with market statistics
    """
    prices = df[price_col].dropna()

    # Basic statistics
    stats = {
        'mean': prices.mean(),
        'median': prices.median(),
        'std': prices.std(),
        'min': prices.min(),
        'max': prices.max(),
        'range': prices.max() - prices.min(),
        'cv': (prices.std() / prices.mean()) * 100,  # Coefficient of variation
    }

    # Growth statistics
    if len(prices) > 1:
        total_return = ((prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0]) * 100
        years = len(prices)
        cagr = (((prices.iloc[-1] / prices.iloc[0]) ** (1 / years)) - 1) * 100

        stats.update({
            'total_return_pct': total_return,
            'cagr_pct': cagr,
            'years': years
        })

    # Volatility
    if len(prices) > 1:
        returns = prices.pct_change().dropna()
        stats['volatility'] = returns.std() * 100
        stats['max_gain'] = returns.max() * 100
        stats['max_loss'] = returns.min() * 100

    return stats
