"""
Test ECL query with OR clause for properties to verify if OntoServer supports it.
This will test whether we can capture both measurement properties AND mass fraction properties.
"""

import sys
import io
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add scripts directory to path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

from terminology_server_adapters import create_adapter

def test_or_property_query():
    """Test if OR clause works in ECL property refinements"""

    print("=" * 80)
    print("Testing ECL Query with OR Property Clause")
    print("=" * 80)

    adapter = create_adapter('loincsnomed')

    # Test case: Methemoglobin component with OR property clause
    # Should capture both:
    # - Substance concentration (measurement property descendants)
    # - Mass fraction (118586006)

    component_concept = "27840003"  # Methemoglobin
    measurement_property = "685451010000100"  # Measurement property
    mass_fraction_property = "118586006"  # Mass fraction

    print("\nTest 1: Simple OR with two specific properties")
    print("-" * 80)
    ecl_query_1 = f"""<< 363787002 |Observable entity| :
    246093002 |Component| = << {component_concept},
    370130000 |Property| = ({measurement_property} OR {mass_fraction_property})"""

    print(f"ECL Query:\n{ecl_query_1}\n")

    try:
        result_1 = adapter.execute_ecl_query(ecl_query_1, limit=100)
        print(f"✓ Query succeeded!")
        print(f"  Found {result_1['total']} SNOMED concepts")
        print(f"  Execution time: {result_1['execution_time']:.2f}s")

        # Show first 5 results
        if result_1['items']:
            print("\n  Sample results:")
            for i, concept in enumerate(result_1['items'][:5], 1):
                fsn = concept.get('fsn', {}).get('term', 'Unknown')
                print(f"    {i}. {concept['conceptId']} - {fsn}")
    except Exception as e:
        print(f"✗ Query failed: {e}")

    print("\n" + "=" * 80)
    print("\nTest 2: OR with descendants")
    print("-" * 80)
    ecl_query_2 = f"""<< 363787002 |Observable entity| :
    246093002 |Component| = << {component_concept},
    370130000 |Property| = (<< {measurement_property} OR {mass_fraction_property})"""

    print(f"ECL Query:\n{ecl_query_2}\n")

    try:
        result_2 = adapter.execute_ecl_query(ecl_query_2, limit=100)
        print(f"✓ Query succeeded!")
        print(f"  Found {result_2['total']} SNOMED concepts")
        print(f"  Execution time: {result_2['execution_time']:.2f}s")

        # Show first 5 results
        if result_2['items']:
            print("\n  Sample results:")
            for i, concept in enumerate(result_2['items'][:5], 1):
                fsn = concept.get('fsn', {}).get('term', 'Unknown')
                print(f"    {i}. {concept['conceptId']} - {fsn}")
    except Exception as e:
        print(f"✗ Query failed: {e}")

    print("\n" + "=" * 80)
    print("\nConclusion:")
    print("-" * 80)
    if 'result_1' in locals() or 'result_2' in locals():
        print("✓ OR clause syntax IS supported by the terminology server!")
        print("  You can use this pattern in refined ECL queries to capture both")
        print("  measurement properties and mass fraction properties.")
        print()
        print("  The expected methemoglobin mass fraction LOINC codes are:")
        print("    - 71879-1: Methemoglobin/Hemoglobin.total [Pure mass fraction] in Venous blood")
        print("    - 71880-9: Methemoglobin/Hemoglobin.total [Pure mass fraction] in Mixed venous blood")
        print("    - 71881-7: Methemoglobin/Hemoglobin.total [Pure mass fraction] in Capillary blood")
        print("    - 71882-5: Methemoglobin/Hemoglobin.total [Pure mass fraction] in Arterial blood")
        print("    - 71883-3: Methemoglobin/Hemoglobin.total [Pure mass fraction] in Blood")
        print()
        print("  These should be captured by the OR query if SNOMED models them")
        print("  with the mass fraction property (118586006).")
    else:
        print("✗ OR clause syntax is NOT supported by the terminology server.")
        print("  You may need to run separate queries and merge results.")
    print("=" * 80)

if __name__ == "__main__":
    test_or_property_query()
