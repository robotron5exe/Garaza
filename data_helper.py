#!/usr/bin/env python3
"""
Data Helper Script for Garaza Project
This script helps you collect, process, and update real estate data.
"""

import json
import statistics
from datetime import datetime
from typing import List, Dict


class RealEstateDataHelper:
    """Helper class for processing real estate data"""

    SIT_TO_EUR = 239.640  # Official conversion rate

    @staticmethod
    def calculate_statistics(prices: List[float]) -> Dict[str, float]:
        """
        Calculate avg, min, max, and median from a list of prices.

        Args:
            prices: List of property prices

        Returns:
            Dictionary with avg, min, max, median
        """
        if not prices:
            raise ValueError("Price list cannot be empty")

        return {
            'avg': round(statistics.mean(prices), 2),
            'min': round(min(prices), 2),
            'max': round(max(prices), 2),
            'median': round(statistics.median(prices), 2)
        }

    @staticmethod
    def convert_sit_to_eur(sit_amount: float) -> float:
        """
        Convert Slovenian Tolar (SIT) to Euro (EUR).
        Use for data before January 1, 2007.

        Args:
            sit_amount: Amount in SIT

        Returns:
            Amount in EUR
        """
        return round(sit_amount / RealEstateDataHelper.SIT_TO_EUR, 2)

    @staticmethod
    def validate_data_entry(data: Dict) -> bool:
        """
        Validate that a data entry has correct structure and logical values.

        Args:
            data: Dictionary with year and property data

        Returns:
            True if valid, raises ValueError if invalid
        """
        required_keys = ['year', 'garages', 'apartments', 'houses']
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing required key: {key}")

        for property_type in ['garages', 'apartments', 'houses']:
            prop_data = data[property_type]

            # Check all required fields exist
            for field in ['avg', 'min', 'max', 'median']:
                if field not in prop_data:
                    raise ValueError(f"Missing {field} in {property_type}")

            # Validate logical relationships
            if not (prop_data['min'] <= prop_data['avg'] <= prop_data['max']):
                raise ValueError(
                    f"{property_type}: min ({prop_data['min']}) should be <= "
                    f"avg ({prop_data['avg']}) <= max ({prop_data['max']})"
                )

            if not (prop_data['min'] <= prop_data['median'] <= prop_data['max']):
                raise ValueError(
                    f"{property_type}: median ({prop_data['median']}) should be "
                    f"between min and max"
                )

        return True

    @staticmethod
    def create_data_template(year: int) -> Dict:
        """
        Create a template data entry for a specific year.

        Args:
            year: Year for the data entry

        Returns:
            Template dictionary
        """
        return {
            'year': year,
            'garages': {
                'avg': 0,
                'min': 0,
                'max': 0,
                'median': 0
            },
            'apartments': {
                'avg': 0,
                'min': 0,
                'max': 0,
                'median': 0
            },
            'houses': {
                'avg': 0,
                'min': 0,
                'max': 0,
                'median': 0
            }
        }

    @staticmethod
    def generate_data_js_format(years_data: List[Dict],
                                source: str = "Please specify data source") -> str:
        """
        Generate JavaScript format for data.js file.

        Args:
            years_data: List of year data dictionaries
            source: Data source description

        Returns:
            Formatted JavaScript code as string
        """
        js_code = "// Real Estate Price Data for Maribor\n"
        js_code += "// All prices are in EUR\n"
        js_code += "// Apartment and house prices are per m²\n"
        js_code += "// Garage prices are total price\n\n"
        js_code += "const realEstateData = {\n"
        js_code += "    // Array of yearly data points\n"
        js_code += "    years: [\n"

        for i, data in enumerate(years_data):
            js_code += "        {\n"
            js_code += f"            year: {data['year']},\n"

            for prop_type in ['garages', 'apartments', 'houses']:
                js_code += f"            {prop_type}: {{\n"
                js_code += f"                avg: {data[prop_type]['avg']},\n"
                js_code += f"                min: {data[prop_type]['min']},\n"
                js_code += f"                max: {data[prop_type]['max']},\n"
                js_code += f"                median: {data[prop_type]['median']}\n"
                js_code += "            }" + ("," if prop_type != 'houses' else "") + "\n"

            js_code += "        }" + ("," if i < len(years_data) - 1 else "") + "\n"

        js_code += "    ],\n\n"
        js_code += "    // Metadata\n"
        js_code += "    metadata: {\n"
        js_code += f"        lastUpdated: '{datetime.now().strftime('%Y-%m-%d')}',\n"
        js_code += "        currency: 'EUR',\n"
        js_code += f"        source: '{source}',\n"
        js_code += "        notes: [\n"
        js_code += "            'Garage prices represent total price for a standard garage (15-20m²)',\n"
        js_code += "            'Apartment and house prices are per square meter',\n"
        js_code += "            'Prices are adjusted for inflation and shown in current EUR value',\n"
        js_code += "            'Data represents average market prices in Maribor city center and surrounding areas'\n"
        js_code += "        ]\n"
        js_code += "    }\n"
        js_code += "};\n"

        return js_code


def example_usage():
    """Example usage of the RealEstateDataHelper class"""

    print("=== Real Estate Data Helper - Example Usage ===\n")

    # Example 1: Calculate statistics from sample prices
    print("Example 1: Calculate statistics from garage prices")
    garage_prices = [15000, 18000, 19500, 22000, 26000, 17500, 20000, 19000]
    stats = RealEstateDataHelper.calculate_statistics(garage_prices)
    print(f"Prices: {garage_prices}")
    print(f"Statistics: {stats}\n")

    # Example 2: Convert SIT to EUR
    print("Example 2: Convert old Slovenian Tolar to EUR")
    sit_price = 1000000
    eur_price = RealEstateDataHelper.convert_sit_to_eur(sit_price)
    print(f"{sit_price:,} SIT = {eur_price:,} EUR\n")

    # Example 3: Create and validate a data entry
    print("Example 3: Create data entry for 2024")
    data_2024 = RealEstateDataHelper.create_data_template(2024)

    # Fill with sample data
    data_2024['garages'] = stats
    data_2024['apartments'] = {
        'avg': 2450,
        'min': 1950,
        'max': 3200,
        'median': 2420
    }
    data_2024['houses'] = {
        'avg': 2150,
        'min': 1650,
        'max': 2800,
        'median': 2120
    }

    print(f"Created data entry:")
    print(json.dumps(data_2024, indent=2))

    # Validate
    try:
        RealEstateDataHelper.validate_data_entry(data_2024)
        print("\n✓ Data entry is valid!\n")
    except ValueError as e:
        print(f"\n✗ Validation error: {e}\n")

    # Example 4: Generate data.js format
    print("Example 4: Generate JavaScript code")
    years_data = [data_2024]  # In real use, you'd have multiple years
    js_code = RealEstateDataHelper.generate_data_js_format(
        years_data,
        "Sample data from manual collection"
    )
    print("First 500 characters of generated code:")
    print(js_code[:500] + "...\n")


def interactive_mode():
    """Interactive mode for entering data"""

    print("\n=== Interactive Data Entry Mode ===\n")

    try:
        year = int(input("Enter year: "))
    except ValueError:
        print("Invalid year!")
        return

    data_entry = RealEstateDataHelper.create_data_template(year)

    for property_type in ['garages', 'apartments', 'houses']:
        print(f"\n--- {property_type.upper()} ---")
        print("Enter prices (comma-separated, e.g., 15000,18000,20000,22000):")

        try:
            prices_input = input(f"{property_type} prices: ")
            prices = [float(p.strip()) for p in prices_input.split(',')]

            if not prices:
                print("No prices entered, skipping...")
                continue

            stats = RealEstateDataHelper.calculate_statistics(prices)
            data_entry[property_type] = stats

            print(f"Calculated: {stats}")

        except Exception as e:
            print(f"Error processing prices: {e}")
            continue

    # Validate
    try:
        RealEstateDataHelper.validate_data_entry(data_entry)
        print("\n✓ Data entry is valid!")

        # Show result
        print("\n=== Generated Data Entry ===")
        print(json.dumps(data_entry, indent=2))

        # Option to save
        save = input("\nSave to JSON file? (y/n): ")
        if save.lower() == 'y':
            filename = f"data_{year}.json"
            with open(filename, 'w') as f:
                json.dump(data_entry, f, indent=2)
            print(f"Saved to {filename}")

    except ValueError as e:
        print(f"\n✗ Validation error: {e}")


def main():
    """Main function"""
    print("Garaza Project - Real Estate Data Helper")
    print("=" * 50)
    print("\nOptions:")
    print("1. Run examples")
    print("2. Interactive data entry")
    print("3. Exit")

    choice = input("\nEnter choice (1-3): ")

    if choice == '1':
        example_usage()
    elif choice == '2':
        interactive_mode()
    elif choice == '3':
        print("Goodbye!")
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()
