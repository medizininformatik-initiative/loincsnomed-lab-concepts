#!/usr/bin/env python3
"""
Test async LOINC display fetcher performance.
Compares synchronous vs async fetching speed.
"""

import asyncio
import time
import sys
import os

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))
from loinc_display_fetcher import LOINCDisplayFetcher, fetch_displays_async

# Test with a reasonable number of codes
test_codes = [
    '1920-8',   # AST
    '2345-7',   # Glucose
    '2951-2',   # Sodium
    '30239-8',  # AST with P-5'-P
    '88112-8',  # AST without P-5'-P
    '2160-0',   # Creatinine
    '1742-6',   # ALT
    '2823-3',   # Potassium
    '17861-6',  # Calcium
    '2885-2',   # Protein
]

print("="*70)
print("Testing LOINC Display Fetcher - Synchronous vs Async")
print("="*70)
print(f"\nTest codes: {len(test_codes)}")

# Test 1: Synchronous fetching
print("\n[TEST 1] Synchronous Fetching")
print("-"*70)
start_time = time.time()
fetcher = LOINCDisplayFetcher(verbose=False)
sync_displays = fetcher.fetch_displays(test_codes)
sync_time = time.time() - start_time

print(f"Time taken: {sync_time:.2f} seconds")
print(f"Codes fetched: {len(sync_displays)}")

# Test 2: Async fetching
print("\n[TEST 2] Async/Parallel Fetching")
print("-"*70)
start_time = time.time()
async_displays = asyncio.run(fetch_displays_async(test_codes, verbose=False, max_concurrent=10))
async_time = time.time() - start_time

print(f"Time taken: {async_time:.2f} seconds")
print(f"Codes fetched: {len(async_displays)}")

# Compare results
print("\n[RESULTS]")
print("="*70)
print(f"Synchronous: {sync_time:.2f}s")
print(f"Async/Parallel: {async_time:.2f}s")
print(f"Speedup: {sync_time/async_time:.2f}x faster")

# Verify results match
if sync_displays == async_displays:
    print("\nResults match: PASS")
else:
    print("\nERROR: Results don't match!")
    print("Differences:")
    for code in test_codes:
        if sync_displays.get(code) != async_displays.get(code):
            print(f"  {code}: '{sync_displays.get(code)}' vs '{async_displays.get(code)}'")

# Show sample displays
print("\n[SAMPLE DISPLAYS]")
print("-"*70)
for i, (code, display) in enumerate(list(async_displays.items())[:3]):
    print(f"{code}: {display}")

print("\n" + "="*70)
print("Test complete!")
