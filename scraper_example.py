#!/usr/bin/env python3
"""
Example Web Scraper for Nepremicnine.net
WARNING: This is a template only. Check nepremicnine.net's terms of service
and robots.txt before using. Implement rate limiting and respect the website.
"""

import time
import re
from typing import List, Dict, Optional

# You'll need to install these packages:
# pip install requests beautifulsoup4

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Required packages not installed!")
    print("Install with: pip install requests beautifulsoup4")
    exit(1)


class NepremicnineScraperExample:
    """
    Example scraper for nepremicnine.net
    This is a TEMPLATE - adjust selectors based on actual website structure
    """

    BASE_URL = "https://www.nepremicnine.net"
    RATE_LIMIT = 2  # seconds between requests

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Research Bot for Academic Purposes)'
        })

    def search_properties(self,
                         property_type: str,
                         location: str = "maribor",
                         transaction_type: str = "prodaja") -> Optional[str]:
        """
        Construct search URL for nepremicnine.net

        Args:
            property_type: 'stanovanje', 'hisa', 'garaza'
            location: Location name
            transaction_type: 'prodaja' or 'najem'

        Returns:
            Search URL
        """
        # Example URL structure - VERIFY THIS ON ACTUAL WEBSITE
        url = f"{self.BASE_URL}/{transaction_type}/{property_type}/{location}/"
        return url

    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch a page with rate limiting and error handling

        Args:
            url: URL to fetch

        Returns:
            Page HTML or None if error
        """
        try:
            print(f"Fetching: {url}")
            time.sleep(self.RATE_LIMIT)  # Rate limiting

            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            return response.text

        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse_listings(self, html: str) -> List[Dict]:
        """
        Parse property listings from HTML
        WARNING: Selectors are examples - inspect actual website HTML!

        Args:
            html: Page HTML

        Returns:
            List of property dictionaries
        """
        soup = BeautifulSoup(html, 'html.parser')
        listings = []

        # Example selectors - THESE WILL NEED TO BE UPDATED
        # based on actual website structure
        listing_elements = soup.find_all('div', class_='property-card')

        for element in listing_elements:
            try:
                listing = self._parse_single_listing(element)
                if listing:
                    listings.append(listing)
            except Exception as e:
                print(f"Error parsing listing: {e}")
                continue

        return listings

    def _parse_single_listing(self, element) -> Optional[Dict]:
        """
        Parse a single listing element
        WARNING: This is a template - adjust based on actual HTML structure

        Args:
            element: BeautifulSoup element

        Returns:
            Dictionary with listing data
        """
        # Example parsing - UPDATE THESE SELECTORS
        title_elem = element.find('h3', class_='title')
        price_elem = element.find('span', class_='price')
        size_elem = element.find('span', class_='size')
        location_elem = element.find('span', class_='location')

        if not price_elem:
            return None

        # Extract price
        price_text = price_elem.get_text(strip=True)
        price = self._extract_price(price_text)

        if not price:
            return None

        # Extract size (for calculating price per m²)
        size = None
        if size_elem:
            size_text = size_elem.get_text(strip=True)
            size = self._extract_number(size_text)

        listing = {
            'title': title_elem.get_text(strip=True) if title_elem else 'N/A',
            'price': price,
            'size': size,
            'price_per_m2': price / size if size and size > 0 else None,
            'location': location_elem.get_text(strip=True) if location_elem else 'N/A'
        }

        return listing

    @staticmethod
    def _extract_price(price_text: str) -> Optional[float]:
        """Extract numeric price from text"""
        # Remove non-numeric characters except digits and dots
        price_text = re.sub(r'[^\d.]', '', price_text)

        try:
            return float(price_text)
        except ValueError:
            return None

    @staticmethod
    def _extract_number(text: str) -> Optional[float]:
        """Extract first number from text"""
        match = re.search(r'(\d+(?:\.\d+)?)', text)
        if match:
            return float(match.group(1))
        return None

    def collect_garage_data_maribor(self) -> List[Dict]:
        """
        Example function to collect garage data for Maribor

        Returns:
            List of garage listings
        """
        print("Collecting garage data for Maribor...")

        url = self.search_properties('garaza', 'maribor', 'prodaja')
        html = self.fetch_page(url)

        if not html:
            print("Failed to fetch page")
            return []

        listings = self.parse_listings(html)
        print(f"Found {len(listings)} garage listings")

        return listings


def check_robots_txt():
    """
    Check robots.txt before scraping
    ALWAYS do this before running scraper!
    """
    print("Checking robots.txt...")
    try:
        response = requests.get("https://www.nepremicnine.net/robots.txt", timeout=5)
        print("\n" + "=" * 50)
        print("robots.txt content:")
        print("=" * 50)
        print(response.text)
        print("=" * 50)
        print("\nIMPORTANT: Review the robots.txt file above!")
        print("Respect the crawl-delay and disallowed paths.")
        print("=" * 50 + "\n")
    except Exception as e:
        print(f"Error fetching robots.txt: {e}")


def example_usage():
    """Example of how to use the scraper"""

    print("=" * 70)
    print("WARNING: Web Scraping Legal and Ethical Considerations")
    print("=" * 70)
    print("1. Check robots.txt and terms of service")
    print("2. Implement rate limiting (don't overload servers)")
    print("3. Use data responsibly")
    print("4. Consider contacting website owner for permission")
    print("5. This is for EDUCATIONAL/RESEARCH purposes only")
    print("=" * 70 + "\n")

    proceed = input("Have you checked robots.txt and ToS? (yes/no): ")
    if proceed.lower() != 'yes':
        print("Please review website policies before scraping.")
        return

    # Check robots.txt
    check_robots_txt()

    proceed = input("\nProceed with example scraping? (yes/no): ")
    if proceed.lower() != 'yes':
        print("Exiting.")
        return

    # Create scraper instance
    scraper = NepremicnineScraperExample()

    # Collect garage data
    garage_listings = scraper.collect_garage_data_maribor()

    if garage_listings:
        print("\n=== Sample Listings ===")
        for i, listing in enumerate(garage_listings[:5], 1):
            print(f"\n{i}. {listing['title']}")
            print(f"   Price: €{listing['price']:,.0f}")
            if listing['size']:
                print(f"   Size: {listing['size']} m²")
            if listing['price_per_m2']:
                print(f"   Price/m²: €{listing['price_per_m2']:,.0f}")
            print(f"   Location: {listing['location']}")

        # Calculate statistics
        prices = [l['price'] for l in garage_listings if l['price']]
        if prices:
            print("\n=== Statistics ===")
            print(f"Average: €{sum(prices) / len(prices):,.0f}")
            print(f"Min: €{min(prices):,.0f}")
            print(f"Max: €{max(prices):,.0f}")
            print(f"Median: €{sorted(prices)[len(prices) // 2]:,.0f}")
            print(f"Sample size: {len(prices)} listings")

        # Save to file
        save = input("\nSave to JSON? (yes/no): ")
        if save.lower() == 'yes':
            import json
            from datetime import datetime

            filename = f"garage_data_{datetime.now().strftime('%Y%m%d')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'date': datetime.now().isoformat(),
                    'location': 'Maribor',
                    'property_type': 'garage',
                    'listings': garage_listings,
                    'statistics': {
                        'avg': sum(prices) / len(prices),
                        'min': min(prices),
                        'max': max(prices),
                        'median': sorted(prices)[len(prices) // 2],
                        'sample_size': len(prices)
                    }
                }, f, indent=2, ensure_ascii=False)

            print(f"Saved to {filename}")

    else:
        print("No listings found. Check selectors and website structure.")


def main():
    """Main function"""
    print("\n" + "=" * 70)
    print("Nepremicnine.net Scraper Example - TEMPLATE ONLY")
    print("=" * 70)
    print("\nIMPORTANT NOTES:")
    print("• This is a TEMPLATE that needs to be customized")
    print("• HTML selectors must be updated based on actual website")
    print("• Check robots.txt before running")
    print("• Review website terms of service")
    print("• Implement proper rate limiting")
    print("• Use data responsibly and legally")
    print("=" * 70 + "\n")

    print("Options:")
    print("1. Check robots.txt only")
    print("2. Run example scraping (requires customization)")
    print("3. Exit")

    choice = input("\nChoice (1-3): ")

    if choice == '1':
        check_robots_txt()
    elif choice == '2':
        print("\n⚠️  WARNING: This template requires customization!")
        print("The CSS selectors are examples and need to be updated")
        print("based on actual website HTML structure.\n")

        proceed = input("Continue anyway? (yes/no): ")
        if proceed.lower() == 'yes':
            example_usage()
    elif choice == '3':
        print("Goodbye!")
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()
