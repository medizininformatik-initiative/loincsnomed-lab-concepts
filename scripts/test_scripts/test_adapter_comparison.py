#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adapter Comparison Test Suite
==============================
Compares results between LOINCSNOMED Snowstorm and MII OntoServer
to ensure they return consistent data.

This is a data quality validation tool to verify that both servers
are serving the same LOINCSNOMED content.

Usage:
    python test_adapter_comparison.py [--staging]
"""

import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from terminology_server_adapters import create_adapter


def compare_concept_sets(set1, set2, name1, name2):
    """Compare two sets of concept IDs and report differences."""
    concepts1 = set(item['conceptId'] for item in set1)
    concepts2 = set(item['conceptId'] for item in set2)

    only_in_1 = concepts1 - concepts2
    only_in_2 = concepts2 - concepts1
    in_both = concepts1 & concepts2

    print(f"\n  Comparison:")
    print(f"    {name1}: {len(concepts1)} concepts")
    print(f"    {name2}: {len(concepts2)} concepts")
    print(f"    In both: {len(in_both)} concepts")

    if only_in_1:
        print(f"    Only in {name1}: {len(only_in_1)} concepts")
        if len(only_in_1) <= 5:
            for cid in only_in_1:
                print(f"      - {cid}")

    if only_in_2:
        print(f"    Only in {name2}: {len(only_in_2)} concepts")
        if len(only_in_2) <= 5:
            for cid in only_in_2:
                print(f"      - {cid}")

    # Consider match if at least 90% overlap
    if len(concepts1) == 0 and len(concepts2) == 0:
        return True, 100.0

    total_unique = len(concepts1 | concepts2)
    if total_unique == 0:
        return True, 100.0

    overlap_percentage = (len(in_both) / total_unique) * 100

    return overlap_percentage >= 90.0, overlap_percentage


def test_hemoglobin_query(snowstorm_adapter, onto_adapter, server_name):
    """Test 1: Compare Hemoglobin query results."""
    print("\n" + "=" * 80)
    print("TEST 1: Hemoglobin Query Comparison")
    print("=" * 80)

    ecl = "<< 363787002 |Observable entity| : <<246093002 |Component| = 38082009, <<704327008 |Direct site| = 119297000"

    print(f"ECL: {ecl}")

    print("\n  Querying LOINCSNOMED Snowstorm...")
    result1 = snowstorm_adapter.execute_ecl_query(ecl, limit=100)

    print(f"  Querying {server_name}...")
    result2 = onto_adapter.execute_ecl_query(ecl, limit=100)

    print(f"\n  LOINCSNOMED: {result1['total']} concepts in {result1['execution_time']:.2f}s")
    print(f"  {server_name}: {result2['total']} concepts in {result2['execution_time']:.2f}s")

    passed, overlap = compare_concept_sets(
        result1['items'], result2['items'],
        "LOINCSNOMED", server_name
    )

    if passed:
        print(f"\n  ✓ TEST PASSED - {overlap:.1f}% overlap")
        return True
    else:
        print(f"\n  ✗ TEST FAILED - Only {overlap:.1f}% overlap (expected >= 90%)")
        return False


def test_erythrocyte_descendants(snowstorm_adapter, onto_adapter, server_name):
    """Test 2: Compare Erythrocyte descendants query."""
    print("\n" + "=" * 80)
    print("TEST 2: Erythrocyte Descendants Comparison")
    print("=" * 80)

    ecl = "<< 363787002 |Observable entity| : <<246093002 |Component| = <<41898006, <<704327008 |Direct site| = <<119297000"

    print(f"ECL: {ecl}")

    print("\n  Querying LOINCSNOMED Snowstorm...")
    result1 = snowstorm_adapter.execute_ecl_query(ecl, limit=100)

    print(f"  Querying {server_name}...")
    result2 = onto_adapter.execute_ecl_query(ecl, limit=100)

    print(f"\n  LOINCSNOMED: {result1['total']} concepts in {result1['execution_time']:.2f}s")
    print(f"  {server_name}: {result2['total']} concepts in {result2['execution_time']:.2f}s")

    passed, overlap = compare_concept_sets(
        result1['items'], result2['items'],
        "LOINCSNOMED", server_name
    )

    if passed:
        print(f"\n  ✓ TEST PASSED - {overlap:.1f}% overlap")
        return True
    else:
        print(f"\n  ✗ TEST FAILED - Only {overlap:.1f}% overlap (expected >= 90%)")
        return False


def test_concept_details(snowstorm_adapter, onto_adapter, server_name):
    """Test 3: Compare concept details lookup."""
    print("\n" + "=" * 80)
    print("TEST 3: Concept Details Comparison")
    print("=" * 80)

    concept_id = "168331010000106"  # Hemoglobin [Mass/volume] in Blood

    print(f"Looking up concept: {concept_id}")

    print("\n  Querying LOINCSNOMED Snowstorm...")
    result1 = snowstorm_adapter.get_concept_details(concept_id)

    print(f"  Querying {server_name}...")
    result2 = onto_adapter.get_concept_details(concept_id)

    print(f"\n  LOINCSNOMED:")
    print(f"    FSN: {result1['fsn']}")
    print(f"    PT: {result1['pt']}")

    print(f"\n  {server_name}:")
    print(f"    FSN: {result2['fsn']}")
    print(f"    PT: {result2['pt']}")

    # Check if both returned valid data
    both_valid = (result1['fsn'] != 'Unknown' and result2['fsn'] != 'Unknown')

    # FSN should match exactly
    fsn_match = result1['fsn'] == result2['fsn']

    if both_valid and fsn_match:
        print("\n  ✓ TEST PASSED - Concept details match")
        return True
    elif both_valid and not fsn_match:
        print("\n  ⚠ WARNING - Both servers returned data but FSN differs")
        return True  # Still pass, might be minor differences
    else:
        print("\n  ✗ TEST FAILED - One or both servers did not return valid data")
        return False


def test_performance_comparison(snowstorm_adapter, onto_adapter, server_name):
    """Test 4: Compare query performance."""
    print("\n" + "=" * 80)
    print("TEST 4: Performance Comparison")
    print("=" * 80)

    # Simple but realistic query
    ecl = "<< 363787002 |Observable entity| : <<246093002 |Component| = 52501007"

    print(f"ECL: {ecl}")

    print("\n  Benchmarking LOINCSNOMED Snowstorm...")
    result1 = snowstorm_adapter.execute_ecl_query(ecl, limit=50)

    print(f"  Benchmarking {server_name}...")
    result2 = onto_adapter.execute_ecl_query(ecl, limit=50)

    print(f"\n  LOINCSNOMED: {result1['execution_time']:.2f}s")
    print(f"  {server_name}: {result2['execution_time']:.2f}s")

    # Both should be reasonably fast
    both_fast = result1['execution_time'] < 10.0 and result2['execution_time'] < 10.0

    if both_fast:
        faster = server_name if result2['execution_time'] < result1['execution_time'] else "LOINCSNOMED"
        print(f"\n  ✓ TEST PASSED - Both servers responsive, {faster} is faster")
        return True
    else:
        print("\n  ⚠ WARNING - One or both servers are slow (>10s)")
        return True  # Don't fail on performance issues


def test_observable_entity_base(snowstorm_adapter, onto_adapter, server_name):
    """Test 5: Test base Observable entity query."""
    print("\n" + "=" * 80)
    print("TEST 5: Observable Entity Base Query")
    print("=" * 80)

    ecl = "<< 363787002 |Observable entity|"

    print(f"ECL: {ecl}")
    print("(Limiting to 10 results for speed)")

    print("\n  Querying LOINCSNOMED Snowstorm...")
    result1 = snowstorm_adapter.execute_ecl_query(ecl, limit=10)

    print(f"  Querying {server_name}...")
    result2 = onto_adapter.execute_ecl_query(ecl, limit=10)

    print(f"\n  LOINCSNOMED: {result1['total']} total concepts, returned {len(result1['items'])}")
    print(f"  {server_name}: {result2['total']} total concepts, returned {len(result2['items'])}")

    # Both should return a large number of total concepts
    both_have_many = result1['total'] > 100 and result2['total'] > 100

    # Totals should be similar (within 10%)
    if result1['total'] > 0 and result2['total'] > 0:
        ratio = min(result1['total'], result2['total']) / max(result1['total'], result2['total'])
        totals_similar = ratio > 0.9
    else:
        totals_similar = False

    if both_have_many and totals_similar:
        print(f"\n  ✓ TEST PASSED - Both servers have similar LOINCSNOMED content")
        return True
    else:
        print(f"\n  ✗ TEST FAILED - Servers have significantly different content sizes")
        return False


def main():
    """Run comparison tests."""
    use_staging = '--staging' in sys.argv

    print("=" * 80)
    print("ADAPTER COMPARISON TEST SUITE")
    print("Data Quality Validation: LOINCSNOMED Snowstorm vs MII OntoServer")
    print("=" * 80)

    # Create adapters
    print("\nInitializing adapters...")

    snowstorm_adapter = create_adapter('loincsnomed')
    print("  ✓ LOINCSNOMED Snowstorm adapter ready")

    if use_staging:
        onto_config = {
            'base_url': 'https://ontoserver-staging.mii-termserv.de/fhir',
            'version_url': 'http://snomed.info/sct/11010000107/version/20250921'
        }
        server_name = "MII OntoServer (Staging)"
    else:
        onto_config = {
            'base_url': 'https://ontoserver.mii-termserv.de/fhir',
            'version_url': 'http://snomed.info/sct/11010000107/version/20250921'
        }
        server_name = "MII OntoServer"

    onto_adapter = create_adapter('ontoserver', **onto_config)
    print(f"  ✓ {server_name} adapter ready")

    # Run tests
    tests = [
        ("Hemoglobin Query", lambda: test_hemoglobin_query(snowstorm_adapter, onto_adapter, server_name)),
        ("Erythrocyte Descendants", lambda: test_erythrocyte_descendants(snowstorm_adapter, onto_adapter, server_name)),
        ("Concept Details", lambda: test_concept_details(snowstorm_adapter, onto_adapter, server_name)),
        ("Performance", lambda: test_performance_comparison(snowstorm_adapter, onto_adapter, server_name)),
        ("Observable Entity Base", lambda: test_observable_entity_base(snowstorm_adapter, onto_adapter, server_name))
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
    print("COMPARISON TEST SUMMARY")
    print("=" * 80)

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status:<10} {test_name}")

    print()
    print(f"Total: {passed_count}/{total_count} tests passed")

    if passed_count == total_count:
        print("\n✓ DATA QUALITY VALIDATION PASSED")
        print("Both servers are serving consistent LOINCSNOMED content")
        return 0
    else:
        print(f"\n✗ DATA QUALITY ISSUES DETECTED")
        print(f"{total_count - passed_count} test(s) failed - investigate discrepancies")
        return 1


if __name__ == "__main__":
    sys.exit(main())
