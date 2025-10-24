#!/usr/bin/env python3
"""
LOINC Display Name Fetcher
===========================
Reusable utility for fetching official LOINC display names from local CSV file
or falling back to terminology server when needed.

This module provides both synchronous and asynchronous interfaces for scripts that
generate FHIR ValueSets with LOINC codes to fetch the correct display labels instead
of using placeholders.

Strategy:
1. Check local LOINC CSV file first (configured via loinc_csv_path in .env)
2. Fall back to OntoServer API only when local lookup fails

Synchronous Usage:
    from scripts.loinc_display_fetcher import LOINCDisplayFetcher

    fetcher = LOINCDisplayFetcher()
    displays = fetcher.fetch_displays(['1920-8', '30239-8', '88112-8'])
    # Returns: {'1920-8': 'Aspartate aminotransferase [Enzymatic activity/volume] in Serum or Plasma', ...}

Asynchronous Usage (much faster for many codes):
    from scripts.loinc_display_fetcher import fetch_displays_async
    import asyncio

    displays = asyncio.run(fetch_displays_async(['1920-8', '30239-8', '88112-8']))
"""

import os
import sys
import asyncio
import csv
from pathlib import Path

# Load .env file
from dotenv import load_dotenv
load_dotenv()

# Add scripts directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from terminology_server_adapters import create_adapter

# Get LOINC CSV path from environment
LOINC_CSV_PATH = os.getenv('loinc_csv_path')

# Global cache for LOINC CSV data (loaded once per process)
_LOINC_LOCAL_CACHE = None


def _load_loinc_csv():
    """
    Load LOINC CSV file into memory for fast lookup.
    Returns dictionary mapping LOINC_NUM -> LONG_COMMON_NAME.
    """
    global _LOINC_LOCAL_CACHE

    if _LOINC_LOCAL_CACHE is not None:
        return _LOINC_LOCAL_CACHE

    if not LOINC_CSV_PATH or not os.path.exists(LOINC_CSV_PATH):
        print(f"  Warning: LOINC CSV not found at {LOINC_CSV_PATH}, will use API fallback")
        _LOINC_LOCAL_CACHE = {}
        return _LOINC_LOCAL_CACHE

    print(f"  Loading local LOINC CSV from {LOINC_CSV_PATH}...")

    loinc_dict = {}
    try:
        with open(LOINC_CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                loinc_num = row.get('LOINC_NUM', '').strip()
                long_common_name = row.get('LONG_COMMON_NAME', '').strip()

                if loinc_num and long_common_name:
                    loinc_dict[loinc_num] = long_common_name

        print(f"  [OK] Loaded {len(loinc_dict)} LOINC codes from local CSV")
        _LOINC_LOCAL_CACHE = loinc_dict
        return loinc_dict

    except Exception as e:
        print(f"  Warning: Error loading LOINC CSV: {e}, will use API fallback")
        _LOINC_LOCAL_CACHE = {}
        return _LOINC_LOCAL_CACHE


class LOINCDisplayFetcher:
    """
    Fetches LOINC display names from local CSV or MII OntoServer.
    Prioritizes local lookup, falls back to API when needed.
    """

    def __init__(self, base_url=None, verbose=True):
        """
        Initialize the LOINC display fetcher.

        Args:
            base_url: OntoServer base URL (default: MII production server)
            verbose: If True, print progress messages
        """
        self.base_url = base_url or 'https://ontoserver.mii-termserv.de/fhir'
        self.verbose = verbose
        self.cache = {}

        if self.verbose:
            print(f"Initializing LOINC display fetcher")
            print(f"  - Local CSV: {LOINC_CSV_PATH if LOINC_CSV_PATH else 'Not configured'}")
            print(f"  - API fallback: {self.base_url}")

        # Load local LOINC CSV
        self.local_loinc = _load_loinc_csv()

        # Create adapter for API fallback
        self.adapter = create_adapter('ontoserver', base_url=self.base_url)

    def get_display(self, loinc_code):
        """
        Get display name for a single LOINC code.
        Tries local CSV first, falls back to API.

        Args:
            loinc_code: LOINC code (e.g., '1920-8')

        Returns:
            Display name string
        """
        # Check cache first
        if loinc_code in self.cache:
            return self.cache[loinc_code]

        # Try local CSV lookup
        if loinc_code in self.local_loinc:
            display = self.local_loinc[loinc_code]
            self.cache[loinc_code] = display
            if self.verbose:
                print(f"  Local: {loinc_code} -> {display}")
            return display

        # Fall back to API
        try:
            url = f"{self.adapter.base_url}/CodeSystem/$lookup"
            params = {
                "system": "http://loinc.org",
                "code": loinc_code
            }

            session = self.adapter._get_session()
            response = session.get(url, params=params)

            if response.status_code == 200:
                fhir_response = response.json()

                # Extract display from parameter
                for param in fhir_response.get('parameter', []):
                    if param.get('name') == 'display':
                        display = param.get('valueString', f"LOINC {loinc_code}")
                        self.cache[loinc_code] = display

                        if self.verbose:
                            print(f"  API: {loinc_code} -> {display}")

                        return display

                # Fallback if no display parameter found
                fallback = f"LOINC {loinc_code}"
                self.cache[loinc_code] = fallback

                if self.verbose:
                    print(f"  Warning: No display found for {loinc_code}, using fallback")

                return fallback
            else:
                if self.verbose:
                    print(f"  Warning: HTTP {response.status_code} for {loinc_code}, using fallback")

                fallback = f"LOINC {loinc_code}"
                self.cache[loinc_code] = fallback
                return fallback

        except Exception as e:
            if self.verbose:
                print(f"  Error fetching {loinc_code}: {str(e)}, using fallback")

            fallback = f"LOINC {loinc_code}"
            self.cache[loinc_code] = fallback
            return fallback

    def fetch_displays(self, loinc_codes):
        """
        Fetch display names for multiple LOINC codes.

        Args:
            loinc_codes: List or iterable of LOINC codes

        Returns:
            Dictionary mapping LOINC code -> display name
        """
        if self.verbose:
            unique_codes = [c for c in loinc_codes if c not in self.cache]
            if unique_codes:
                print(f"\nFetching displays for {len(unique_codes)} LOINC codes (cached: {len(self.cache)})...")

        results = {}
        for code in loinc_codes:
            results[code] = self.get_display(code)

        if self.verbose:
            print(f"Total cached LOINC displays: {len(self.cache)}\n")

        return results

    def get_cache_stats(self):
        """
        Get statistics about the cache.

        Returns:
            Dictionary with cache statistics
        """
        return {
            'total_cached': len(self.cache),
            'cached_codes': sorted(self.cache.keys())
        }


# Convenience function for simple usage
def fetch_loinc_displays(loinc_codes, base_url=None, verbose=True):
    """
    Convenience function to fetch LOINC displays without creating a fetcher object.

    Args:
        loinc_codes: List of LOINC codes
        base_url: OntoServer base URL (optional)
        verbose: Print progress messages

    Returns:
        Dictionary mapping LOINC code -> display name
    """
    fetcher = LOINCDisplayFetcher(base_url=base_url, verbose=verbose)
    return fetcher.fetch_displays(loinc_codes)


# ==============================================================================
# ASYNC INTERFACE - Much faster for large batches
# ==============================================================================
# Uses asyncio with ThreadPoolExecutor for parallelism while keeping cert auth

import concurrent.futures

def _fetch_single_sync(adapter, loinc_code, local_loinc, verbose=False):
    """
    Helper function to fetch a single LOINC display synchronously.
    Tries local CSV first, falls back to API.
    Used by async interface in thread pool.
    """
    # Try local lookup first
    if loinc_code in local_loinc:
        display = local_loinc[loinc_code]
        if verbose:
            print(f"  Local: {loinc_code} -> {display}")
        return (loinc_code, display)

    # Fall back to API
    try:
        url = f"{adapter.base_url}/CodeSystem/$lookup"
        params = {
            "system": "http://loinc.org",
            "code": loinc_code
        }

        session = adapter._get_session()
        response = session.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            # Extract display from parameter
            for param in data.get('parameter', []):
                if param.get('name') == 'display':
                    display = param.get('valueString', f"LOINC {loinc_code}")
                    if verbose:
                        print(f"  API: {loinc_code} -> {display}")
                    return (loinc_code, display)

            # Fallback if no display parameter found
            if verbose:
                print(f"  Warning: No display found for {loinc_code}, using fallback")
            return (loinc_code, f"LOINC {loinc_code}")
        else:
            if verbose:
                print(f"  Warning: HTTP {response.status_code} for {loinc_code}, using fallback")
            return (loinc_code, f"LOINC {loinc_code}")

    except Exception as e:
        if verbose:
            print(f"  Error fetching {loinc_code}: {str(e)}, using fallback")
        return (loinc_code, f"LOINC {loinc_code}")


async def fetch_displays_async(loinc_codes, base_url=None, verbose=True, max_concurrent=10):
    """
    Fetch LOINC displays for multiple codes in parallel.
    Uses local CSV for fast lookup, only calls API for missing codes.

    This is MUCH faster than API-only fetching when dealing with many codes.
    Uses ThreadPoolExecutor to run requests in parallel while maintaining
    certificate authentication support.

    Args:
        loinc_codes: List of LOINC codes
        base_url: OntoServer base URL (default: MII production server)
        verbose: Print progress messages
        max_concurrent: Maximum number of concurrent requests (default: 10)

    Returns:
        Dictionary mapping LOINC code -> display name

    Example:
        import asyncio
        displays = asyncio.run(fetch_displays_async(['1920-8', '2345-7']))
    """
    base_url = base_url or 'https://ontoserver.mii-termserv.de/fhir'

    if verbose:
        print(f"Fetching displays for {len(loinc_codes)} LOINC codes...")
        print(f"  - Local CSV: {LOINC_CSV_PATH if LOINC_CSV_PATH else 'Not configured'}")
        print(f"  - API fallback: {base_url}")
        print(f"  - Max concurrent API requests: {max_concurrent}")

    # Load local LOINC CSV
    local_loinc = _load_loinc_csv()

    # Create adapter with certificate authentication
    adapter = create_adapter('ontoserver', base_url=base_url)

    # Use ThreadPoolExecutor to run lookups in parallel
    loop = asyncio.get_event_loop()

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent) as executor:
        # Create futures for all LOINC codes
        futures = [
            loop.run_in_executor(executor, _fetch_single_sync, adapter, code, local_loinc, verbose)
            for code in loinc_codes
        ]

        # Wait for all futures to complete
        results = await asyncio.gather(*futures)

    # Convert results to dictionary
    displays = dict(results)

    # Count local vs API fetches
    if verbose:
        local_count = sum(1 for code in loinc_codes if code in local_loinc)
        api_count = len(loinc_codes) - local_count
        print(f"\nCompleted: {len(displays)} displays ({local_count} from local CSV, {api_count} from API)")

    return displays

