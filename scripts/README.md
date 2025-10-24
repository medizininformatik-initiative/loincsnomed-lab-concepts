# Helper Scripts

Utility scripts for LOINC-SNOMED mapping analysis and ECL query execution.

## Core Utilities

### terminology_server_adapters.py

Adapter pattern for multiple terminology servers. Provides unified interface for:
- **LOINCSNOMED Snowstorm** (public browser.loincsnomed.org)
- **MII OntoServer** (with mTLS authentication)

**Usage:**
```python
from terminology_server_adapters import create_adapter

# Public LOINCSNOMED Snowstorm
adapter = create_adapter('loincsnomed')

# MII OntoServer with authentication
adapter = create_adapter('ontoserver',
                        base_url='https://ontoserver.mii-termserv.de/fhir',
                        version_url='http://snomed.info/sct/11010000107/version/20250921')

# Execute ECL query
result = adapter.execute_ecl_query("<< 38082009 |Hemoglobin|")
```

**Features:**
- Automatic certificate loading from `.env`
- Support for legacy PKCS12 certificates
- GET and POST methods for $expand operations
- FHIR response normalization

### loinc_display_fetcher.py

Fast LOINC display name lookup with local CSV fallback.

**Usage:**
```python
from loinc_display_fetcher import LOINCDisplayFetcher

fetcher = LOINCDisplayFetcher(
    loinc_csv_path='path/to/Loinc.csv',  # Local cache
    api_base='https://fhir.loinc.org'     # Fallback API
)

display = fetcher.get_display('59260-0')
# Returns: "Hemoglobin [Mass/volume] in Blood"
```

**Features:**
- Local CSV cache for fast lookup (100% hit rate for common codes)
- Automatic fallback to LOINC FHIR API
- Batch processing support

## Interactive Tools

### interactive_ecl_builder.py

Interactive CLI tool for building and testing ECL queries.

**Usage:**
```bash
python scripts/interactive_ecl_builder.py <LOINC_CODE>

# Example
python scripts/interactive_ecl_builder.py 787-2
```

**Workflow:**
1. **Load LOINC mapping** → Finds SNOMED concept for LOINC code
2. **Extract relationships** → Shows all SNOMED attributes (Component, Property, Direct site, etc.)
3. **Select attributes** → Choose which attributes to use in ECL
4. **Generate permutations** → Creates all combinations of fixed vs descendants
5. **Execute queries** → Runs all permutations against terminology server
6. **Save results** → Exports JSON + CSV for analysis

**Example Session:**
```
INTERACTIVE ECL BUILDER FOR LOINC 787-2
========================================

Found: Erythrocyte mean corpuscular volume [Entitic volume] in Blood
SNOMED Concept ID: 250170007

Extracting all relationships...
Found 5 relationship types:
1. Component (246093002)
   -> Erythrocyte (14089001)
2. Property (370130000)
   -> Entitic volume (118565006)
3. Direct site (704327008)
   -> Blood specimen (119297000)
4. Scale type (370134009)
   -> Quantitative (26716007)
5. Time aspect (370132008)
   -> Point in time (123029007)

SELECT ATTRIBUTES FOR ECL QUERY
===============================
Enter numbers (comma-separated, e.g., 1,2,3) or Enter for auto-selection

Your selection: 1,2,3

Selected 3 attributes:
  - Component: Erythrocyte
  - Property: Entitic volume
  - Direct site: Blood specimen

Generating 8 permutations...

Executing ECL QUERIES
===================
Permutation 1: Component=Fixed | Property=Fixed | Direct site=Fixed
  ECL: << 363787002 |Observable entity| : 246093002 |Component| = 14089001, ...
  Result: 2 concepts

...

RESULTS SUMMARY
==============
1. Component=Fixed | Property=Fixed | Direct site=Fixed: 2 concepts
2. Component=Fixed | Property=Fixed | Direct site=Desc: 2 concepts
3. Component=Fixed | Property=Desc | Direct site=Fixed: 2 concepts
...

Results saved to: ecl_results/787_2_interactive_results.json
CSV saved to: ecl_results/787_2_interactive_concepts.csv
```

**Output Files:**
- `*_results.json` - Complete results with ECL expressions
- `*_concepts.csv` - Flattened table of all concepts found

### ecl_permutation_analyzer_simple.py

Systematic analysis of ECL query permutations.

**Usage:**
```python
from ecl_permutation_analyzer_simple import load_loinc_mappings, execute_ecl_query
from terminology_server_adapters import create_adapter

# Load LOINC-SNOMED mappings
mappings = load_loinc_mappings(identifier_file, description_file)

# Create server adapter
adapter = create_adapter('loincsnomed')

# Execute ECL query
ecl = "<< 363787002 |Observable entity| : 246093002 |Component| = 38082009"
result = execute_ecl_query(ecl, loinc_mappings=mappings, server_adapter=adapter)

print(f"Found {len(result['detailed_concepts'])} concepts")
for concept in result['detailed_concepts']:
    print(f"  {concept['concept_id']}: {concept['fsn']}")
    print(f"    LOINC: {concept.get('loinc_code', 'N/A')}")
```

**Features:**
- Automatic LOINC code enrichment (adds LOINC codes to SNOMED results)
- Support for all server adapters
- Detailed concept information (FSN, PT, LOINC mappings)

## Configuration

All scripts use environment variables from `.env`:

```env
# MII OntoServer Authentication
auth_path=C:/Users/username/.secrets
auth_file=certificate.p12
auth_pw=password

# SNOMED/LOINC Data Files
loinc_snomed_mapping_path=C:/path/to/sct2_Identifier_Full_LO1010000_20250921.txt
loinc_csv_path=C:/path/to/Loinc.csv
```

## Dependencies

```bash
pip install requests python-dotenv
pip install requests-pkcs12  # For mTLS authentication (optional)
```

## Common Use Cases

### 1. Exploring a New LOINC Code

```bash
# Interactive exploration
python scripts/interactive_ecl_builder.py 59260-0
```

### 2. Testing Specific ECL Query

```python
from terminology_server_adapters import create_adapter

adapter = create_adapter('loincsnomed')
result = adapter.execute_ecl_query(
    "<< 363787002 |Observable entity| : "
    "246093002 |Component| = 38082009, "
    "370130000 |Property| = << 118556004"
)

print(f"Total: {result['total']} concepts")
for item in result['items']:
    print(f"  {item['conceptId']}: {item['fsn']['term']}")
```

### 3. Batch LOINC Display Lookup

```python
from loinc_display_fetcher import LOINCDisplayFetcher

fetcher = LOINCDisplayFetcher()

codes = ['59260-0', '26453-1', '20570-8']
for code in codes:
    display = fetcher.get_display(code)
    print(f"{code}: {display}")
```

### 4. Switch Between Servers

```python
from terminology_server_adapters import create_adapter

# Compare results from different servers
public_adapter = create_adapter('loincsnomed')
mii_adapter = create_adapter('ontoserver',
                             base_url='https://ontoserver.mii-termserv.de/fhir')

ecl = "<< 38082009 |Hemoglobin|"

public_result = public_adapter.execute_ecl_query(ecl)
mii_result = mii_adapter.execute_ecl_query(ecl)

print(f"Public: {public_result['total']} concepts")
print(f"MII: {mii_result['total']} concepts")
```

## Troubleshooting

### Certificate Authentication Issues

**Problem**: "Invalid password or PKCS12 data"

**Solutions**:
1. Verify password with OpenSSL:
   ```bash
   openssl pkcs12 -info -in certificate.p12 -noout
   ```

2. Check `.env` configuration:
   - Empty password: `auth_pw=` (no value)
   - Actual password: `auth_pw=YourPassword`

3. Install legacy cryptography support:
   ```bash
   pip install cryptography[ssh]
   ```

### Connection Timeouts

**Problem**: Queries timeout on large result sets

**Solutions**:
1. Reduce limit:
   ```python
   result = adapter.execute_ecl_query(ecl, limit=100)
   ```

2. Use more specific ECL (add more constraints)

3. Switch to POST method (OntoServer):
   ```python
   adapter = create_adapter('ontoserver', use_post=True)
   ```

### LOINC Code Not Found

**Problem**: Interactive builder can't find LOINC code

**Solutions**:
1. Verify LOINC code format (e.g., `787-2` not `787`)
2. Check mapping file path in interactive_ecl_builder.py (line 327)
3. Ensure LOINCSNOMED Edition date matches your files

## Development

### Adding New Server Adapter

1. Create subclass of `TerminologyServerAdapter`
2. Implement `execute_ecl_query()` and `get_concept_details()`
3. Add to `create_adapter()` factory function
4. Update documentation

Example:
```python
class MyServerAdapter(TerminologyServerAdapter):
    def execute_ecl_query(self, ecl_expression, limit=1000):
        # Implementation
        pass

    def get_concept_details(self, concept_id):
        # Implementation
        pass
```

### Testing New Features

Use the test scripts in `scripts/test_scripts/` directory.

## References

- [SNOMED ECL Specification](https://confluence.ihtsdotools.org/display/DOCECL/)
- [FHIR Terminology Service](https://www.hl7.org/fhir/terminology-service.html)
- [LOINCSNOMED Browser](http://browser.loincsnomed.org)
- [MII OntoServer Documentation](https://ontoserver.mii-termserv.de)
