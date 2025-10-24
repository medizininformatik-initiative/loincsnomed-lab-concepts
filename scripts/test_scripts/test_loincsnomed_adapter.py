#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Script for LOINCSNOMED Snowstorm Adapter
==============================================
Validates that the public LOINCSNOMED Snowstorm API is working correctly.

Usage:
    python test_loincsnomed_adapter.py
"""

import sys
import io
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from terminology_server_adapters import create_adapter


def test_simple_ecl():
    """Test 1: Simple ECL query for Hemoglobin observable entities."""
    print("\n" + "=" * 80)
    print("TEST 1: Simple ECL Query - Hemoglobin")
    print("=" * 80)

    adapter = create_adapter('loincsnomed')

    # Simple query: Hemoglobin in Blood
    ecl = "<< 363787002 |Observable entity| : <<246093002 |Component| = 38082009, <<704327008 |Direct site| = 119297000"

    print(f"ECL: {ecl}")
    print("Executing query...")

    result = adapter.execute_ecl_query(ecl, limit=10)

    print(f"Result: {result['total']} concepts found")
    print(f"Execution time: {result['execution_time']:.2f}s")

    if result['total'] > 0:
        print(f"\nSample concepts (first {min(5, len(result['items']))}):")
        for item in result['items'][:5]:
            print(f"  - {item['conceptId']}: {item['pt']['term']}")
        print("\n✓ TEST PASSED")
        return True
    else:
        print("\n✗ TEST FAILED: No concepts returned")
        return False


def test_concept_lookup():
    """Test 2: Look up specific concept details."""
    print("\n" + "=" * 80)
    print("TEST 2: Concept Lookup - Hemoglobin [Mass/volume] in Blood")
    print("=" * 80)

    adapter = create_adapter('loincsnomed')

    # Known LOINC-SNOMED concept for Hemoglobin
    concept_id = "168331010000106"  # Hemoglobin [Mass/volume] in Blood (LOINC 718-7)

    print(f"Looking up concept: {concept_id}")

    result = adapter.get_concept_details(concept_id)

    print(f"Concept ID: {result['concept_id']}")
    print(f"FSN: {result['fsn']}")
    print(f"PT: {result['pt']}")

    if result['fsn'] != 'Unknown':
        print("\n✓ TEST PASSED")
        return True
    else:
        print("\n✗ TEST FAILED: Could not retrieve concept details")
        return False


def test_descendants_query():
    """Test 3: ECL query with descendants."""
    print("\n" + "=" * 80)
    print("TEST 3: Descendants Query - Erythrocyte count variants")
    print("=" * 80)

    adapter = create_adapter('loincsnomed')

    # Query with descendants
    ecl = "<< 363787002 |Observable entity| : <<246093002 |Component| = <<41898006, <<704327008 |Direct site| = <<119297000"

    print(f"ECL: {ecl}")
    print("Executing query...")

    result = adapter.execute_ecl_query(ecl, limit=50)

    print(f"Result: {result['total']} concepts found")
    print(f"Execution time: {result['execution_time']:.2f}s")

    if result['total'] > 0:
        print(f"\nSample concepts (first {min(5, len(result['items']))}):")
        for item in result['items'][:5]:
            print(f"  - {item['conceptId']}: {item['pt']['term']}")
        print("\n✓ TEST PASSED")
        return True
    else:
        print("\n✗ TEST FAILED: No concepts returned")
        return False


def test_api_availability():
    """Test 4: Check API availability and response time."""
    print("\n" + "=" * 80)
    print("TEST 4: API Availability Check")
    print("=" * 80)

    adapter = create_adapter('loincsnomed')

    # Very simple query
    ecl = "<< 363787002 |Observable entity|"

    print("Testing API response time...")

    result = adapter.execute_ecl_query(ecl, limit=1)

    print(f"Execution time: {result['execution_time']:.2f}s")

    if result['execution_time'] < 5.0:
        print("✓ API is responsive (< 5 seconds)")
        return True
    else:
        print("⚠ WARNING: API is slow (> 5 seconds)")
        return False


def main():
    """Run all tests."""
    print("=" * 80)
    print("LOINCSNOMED SNOWSTORM ADAPTER TEST SUITE")
    print("=" * 80)
    print("\nTesting connection to: http://browser.loincsnomed.org/snowstorm/snomed-ct")

    tests = [
        ("Simple ECL Query", test_simple_ecl),
        ("Concept Lookup", test_concept_lookup),
        ("Descendants Query", test_descendants_query),
        ("API Availability", test_api_availability)
    ]

    results = []

    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n✗ TEST FAILED: {test_name}")
            print(f"Error: {str(e)}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status:<10} {test_name}")

    print()
    print(f"Total: {passed_count}/{total_count} tests passed")

    if passed_count == total_count:
        print("\n✓ ALL TESTS PASSED - Adapter is working correctly")
        return 0
    else:
        print(f"\n✗ {total_count - passed_count} TEST(S) FAILED - Please investigate")
        return 1


if __name__ == "__main__":
    sys.exit(main())
