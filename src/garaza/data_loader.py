"""
Data loading utilities for Garaza real estate analysis.
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional, Union
import pandas as pd


class DataLoader:
    """Load and process real estate market data."""

    def __init__(self, data_dir: Optional[Union[str, Path]] = None):
        """
        Initialize DataLoader.

        Args:
            data_dir: Path to data directory. If None, uses default location.
        """
        if data_dir is None:
            # Default to project root/data/raw
            project_root = Path(__file__).parent.parent.parent
            data_dir = project_root / "data" / "raw"
        self.data_dir = Path(data_dir)

    def load_json(self, filename: str) -> Dict:
        """Load JSON file from data directory."""
        filepath = self.data_dir / filename
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_apartments(self) -> pd.DataFrame:
        """
        Load historical apartment price data for Maribor.

        Returns:
            DataFrame with columns: year, price_low, price_mid, price_high,
            yoy_change, data_quality, notes
        """
        data = self.load_json('maribor_apartments_historical.json')
        df = pd.DataFrame(data['annual_prices'])
        df['year'] = pd.to_datetime(df['year'], format='%Y')
        return df

    def load_garages(self, location: str = 'maribor') -> pd.DataFrame:
        """
        Load garage price data.

        Args:
            location: 'maribor' or 'ljubljana'

        Returns:
            DataFrame with garage listing data
        """
        filename = f'garage_prices_{location}.json'
        data = self.load_json(filename)

        if 'current_listings_2024' in data:
            df = pd.DataFrame(data['current_listings_2024'])
            return df
        return pd.DataFrame()

    def load_national_market(self) -> Dict:
        """
        Load Slovenia national market data.

        Returns:
            Dictionary with national market statistics
        """
        return self.load_json('slovenia_national_market.json')

    def get_current_metrics(self) -> Dict:
        """
        Get current market metrics for Maribor (2024-2025).

        Returns:
            Dictionary with current prices, yields, and investment metrics
        """
        data = self.load_json('maribor_apartments_historical.json')
        return data.get('current_market_data_2025', {})

    def get_transaction_volumes(self) -> pd.DataFrame:
        """
        Get historical transaction volumes.

        Returns:
            DataFrame with transaction volume data
        """
        data = self.load_json('maribor_apartments_historical.json')
        volumes = data.get('transaction_volumes', {})

        records = []
        for year, vol_data in volumes.items():
            record = {'year': int(year)}
            record.update(vol_data)
            records.append(record)

        df = pd.DataFrame(records)
        df['year'] = pd.to_datetime(df['year'], format='%Y')
        return df


# Convenience functions
def load_apartment_data(data_dir: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """Load apartment price data."""
    loader = DataLoader(data_dir)
    return loader.load_apartments()


def load_garage_data(location: str = 'maribor',
                     data_dir: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """Load garage price data."""
    loader = DataLoader(data_dir)
    return loader.load_garages(location)


def load_national_data(data_dir: Optional[Union[str, Path]] = None) -> Dict:
    """Load national market data."""
    loader = DataLoader(data_dir)
    return loader.load_national_market()


def load_all_data(data_dir: Optional[Union[str, Path]] = None) -> Dict[str, Union[pd.DataFrame, Dict]]:
    """
    Load all available data.

    Returns:
        Dictionary with keys: 'apartments', 'garages_maribor', 'garages_ljubljana',
        'national', 'metrics', 'volumes'
    """
    loader = DataLoader(data_dir)
    return {
        'apartments': loader.load_apartments(),
        'garages_maribor': loader.load_garages('maribor'),
        'garages_ljubljana': loader.load_garages('ljubljana'),
        'national': loader.load_national_market(),
        'metrics': loader.get_current_metrics(),
        'volumes': loader.get_transaction_volumes()
    }
