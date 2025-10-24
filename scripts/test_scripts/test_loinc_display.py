#!/usr/bin/env python3
"""
Quick test to verify LOINC display labels are working correctly.
Creates one test value set with proper LOINC displays.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))
from loinc_display_fetcher import LOINCDisplayFetcher

print("Testing LOINC display fetcher integration...")
print("="*60)

# Test LOINC codes (AST codes from example)
test_codes = ['1920-8', '30239-8', '88112-8']

# Initialize fetcher
print("\n1. Initializing LOINC display fetcher...")
fetcher = LOINCDisplayFetcher(verbose=True)

# Fetch displays
print("\n2. Fetching displays...")
displays = fetcher.fetch_displays(test_codes)

# Create test value set
print("\n3. Creating test FHIR ValueSet...")
valueset = {
    "resourceType": "ValueSet",
    "id": "test-loinc-displays",
    "url": "https://test.example.org/ValueSet/test-loinc-displays",
    "version": "1.0",
    "name": "TestLOINCDisplays",
    "title": "Test Value Set with Correct LOINC Displays",
    "status": "draft",
    "experimental": True,
    "date": datetime.now().strftime("%Y-%m-%d"),
    "publisher": "Test",
    "description": "Test value set to verify LOINC display labels are fetched correctly",
    "compose": {
        "include": [
            {
                "system": "http://loinc.org",
                "concept": [
                    {
                        "code": code,
                        "display": displays.get(code, f"LOINC {code}")
                    }
                    for code in sorted(test_codes)
                ]
            }
        ]
    }
}

# Save to file
output_file = Path('output') / 'test_valueset_with_displays.json'
output_file.parent.mkdir(exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(valueset, f, indent=2, ensure_ascii=False)

print(f"\n4. Test ValueSet saved to: {output_file}")

# Display the concepts
print("\n5. Verify - LOINC codes with displays:")
print("="*60)
for concept in valueset['compose']['include'][0]['concept']:
    print(f"  Code:    {concept['code']}")
    print(f"  Display: {concept['display']}")
    print()

print("="*60)
print("Test complete! Check the JSON file to verify display labels.")
