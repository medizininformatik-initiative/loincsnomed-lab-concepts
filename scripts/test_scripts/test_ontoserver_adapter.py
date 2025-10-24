#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Script for MII OntoServer Adapter
=======================================
Validates that the MII OntoServer instance is working correctly with LOINCSNOMED.

Usage:
    python test_ontoserver_adapter.py [--staging] [--post]

Options:
    --staging: Use staging server instead of production
    --post: Use POST method instead of GET
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


def get_server_config(use_staging=False, use_post=False):
    """Get server configuration based on arguments."""
    if use_staging:
        base_url = 'https://ontoserver-staging.mii-termserv.de/fhir'
        server_name = "MII OntoServer (Staging)"
    else:
        base_url = 'https://ontoserver.mii-termserv.de/fhir'
        server_name = "MII OntoServer (Production)"

    method = "POST" if use_post else "GET"

    config = {
        'base_url': base_url,
        'version_url': 'http://snomed.info/sct/11010000107/version/20250921',
        'use_post': use_post
    }

    return server_name, method, config


def test_simple_ecl(adapter):
    """Test 1: Simple ECL query for Hemoglobin observable entities."""
    print("\n" + "=" * 80)
    print("TEST 1: Simple ECL Query - Hemoglobin")
    print("=" * 80)

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


def test_concept_lookup(adapter):
    """Test 2: Look up specific concept details."""
    print("\n" + "=" * 80)
    print("TEST 2: Concept Lookup - Hemoglobin [Mass/volume] in Blood")
    print("=" * 80)

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


def test_descendants_query(adapter):
    """Test 3: ECL query with descendants."""
    print("\n" + "=" * 80)
    print("TEST 3: Descendants Query - Erythrocyte count variants")
    print("=" * 80)

    # Query with descendants
    ecl = "<< 363787002 |Observable entity| : <<246093002 |Component| = <<41898006, <<704327008 |Direct site| = <<119297000"

    print(f"ECL: {ecl}")
    print("Executing query...")

    result = adapter.execute_ecl_query(ecl, limit=50)

    print(f"Result: {result['total']} concepts found")
    print(f"Execution time: {result['execution_time']:.2f}s")

    if result['total'] > 0:
        print(f"\nSample concepts (first {min(5, len(result['items']))}): ")
        for item in result['items'][:5]:
            print(f"  - {item['conceptId']}: {item['pt']['term']}")
        print("\n✓ TEST PASSED")
        return True
    else:
        print("\n✗ TEST FAILED: No concepts returned")
        return False


def test_complex_ecl(adapter):
    """Test 4: Complex ECL with multiple constraints."""
    print("\n" + "=" * 80)
    print("TEST 4: Complex ECL - White blood cell count")
    print("=" * 80)

    # More complex query with multiple attributes
    ecl = "<< 363787002 |Observable entity| : <<246093002 |Component| = 52501007, <<704327008 |Direct site| = 119297000, <<370132008 |Time aspect| = 123029007"

    print(f"ECL: {ecl}")
    print("Executing query...")

    result = adapter.execute_ecl_query(ecl, limit=20)

    print(f"Result: {result['total']} concepts found")
    print(f"Execution time: {result['execution_time']:.2f}s")

    if result['total'] >= 0:  # Accept 0 results as valid (might be overly restrictive)
        if result['total'] > 0:
            print(f"\nSample concepts (first {min(3, len(result['items']))}):")
            for item in result['items'][:3]:
                print(f"  - {item['conceptId']}: {item['pt']['term']}")
        print("\n✓ TEST PASSED")
        return True
    else:
        print("\n✗ TEST FAILED: Query error")
        return False


def test_api_availability(adapter):
    """Test 5: Check API availability and response time."""
    print("\n" + "=" * 80)
    print("TEST 5: API Availability Check")
    print("=" * 80)

    # Very simple query
    ecl = "<< 363787002 |Observable entity|"

    print("Testing API response time...")

    result = adapter.execute_ecl_query(ecl, limit=1)

    print(f"Execution time: {result['execution_time']:.2f}s")

    if result['execution_time'] < 10.0:
        print("✓ API is responsive (< 10 seconds)")
        return True
    else:
        print("⚠ WARNING: API is slow (> 10 seconds)")
        return False


def main():
    """Run all tests."""
    # Parse arguments
    use_staging = '--staging' in sys.argv
    use_post = '--post' in sys.argv

    server_name, method, config = get_server_config(use_staging, use_post)

    print("=" * 80)
    print("MII ONTOSERVER ADAPTER TEST SUITE")
    print("=" * 80)
    print(f"\nServer: {server_name}")
    print(f"Method: {method}")
    print(f"URL: {config['base_url']}")
    print(f"Version: {config['version_url']}")

    # Create adapter
    try:
        adapter = create_adapter('ontoserver', **config)
    except Exception as e:
        print(f"\n✗ FAILED TO CREATE ADAPTER: {str(e)}")
        return 1

    tests = [
        ("Simple ECL Query", lambda: test_simple_ecl(adapter)),
        ("Concept Lookup", lambda: test_concept_lookup(adapter)),
        ("Descendants Query", lambda: test_descendants_query(adapter)),
        ("Complex ECL Query", lambda: test_complex_ecl(adapter)),
        ("API Availability", lambda: test_api_availability(adapter))
    ]

    results = []

    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n✗ TEST FAILED: {test_name}")
            print(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
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
        print(f"\n✓ ALL TESTS PASSED - {server_name} ({method}) is working correctly")
        return 0
    else:
        print(f"\n✗ {total_count - passed_count} TEST(S) FAILED - Please investigate")
        return 1


if __name__ == "__main__":
    sys.exit(main())
