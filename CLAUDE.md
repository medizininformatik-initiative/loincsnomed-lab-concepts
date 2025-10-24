# MII Lab SNOMED-LOINC Mapping Project

## Project Overview
This project analyzes and generates LOINC-SNOMED value sets for laboratory concepts using the LOINCSNOMED edition. The goal is to create accurate, computable value sets that can be used for semantic interoperability in healthcare systems.

## Repository Structure

```
mii_lab_snomedloinc/
├── analysis/                       # Analysis scripts
│   ├── experiments/                # ECL query experiments
│   │   ├── ecl/                   # ECL-based approaches
│   │   │   ├── ecl_descendants_baseline_run_all.py
│   │   │   ├── ecl_fixed_component_run_all.py
│   │   │   ├── ecl_component_descendants_run_all.py
│   │   │   ├── ecl_fixed_component_property_run_all.py
│   │   │   └── ecl_fixed_component_system_run_all.py
│   │   └── interpolar/            # Interpolar-based approaches
│   │       ├── create_valuesets_from_interpolar.py
│   │       └── create_valuesets_from_interpolar_filtered.py
│   ├── create_decision_dashboard.py      # Decision dashboard generator
│   ├── create_singular_concept_table.py  # Single concept analysis
│   ├── cbc_component_analyzer.py         # CBC component analyzer
│   ├── tests/                            # Test files for specific concepts
│   │   ├── test_hemoglobin_ecl_refined.py
│   │   ├── test_methemoglobin_precoord_vs_postcoord.py
│   │   ├── test_erythrocytes_ecl_refined.py
│   │   ├── test_leukocytes_ecl_refined.py
│   │   ├── test_platelets_ecl_refined.py
│   │   ├── test_hematocrit_ecl_refined.py
│   │   ├── test_mcv_ecl_refined.py
│   │   ├── test_mch_ecl_refined.py
│   │   └── test_mchc_ecl_refined.py
│   └── create_hemoglobin_html.py         # HTML report generator
├── docs/                           # Documentation
│   └── ecl_query_template_with_rationale.md  # ECL query patterns
├── input/                          # Reference data
│   ├── LOINC_Mapping_Interpolar_v3.6 an Debersthäuser 25.09.2025.xlsx
│   └── Top300 Stand 2018-08-08.xlsx
├── output/                         # Generated outputs
│   ├── decision_dashboards/        # Interactive HTML dashboards
│   │   ├── hemoglobin_decision_dashboard.html
│   │   ├── erythrocytes_decision_dashboard.html
│   │   ├── leukocytes_decision_dashboard.html
│   │   ├── platelets_decision_dashboard.html
│   │   ├── hematocrit_decision_dashboard.html
│   │   ├── mcv_decision_dashboard.html      # Erythrocyte indices
│   │   ├── mch_decision_dashboard.html
│   │   ├── mchc_decision_dashboard.html
│   │   ├── methemoglobin_decision_dashboard.html
│   │   ├── methemoglobin_ratio_decision_dashboard.html
│   │   ├── potassium_decision_dashboard.html
│   │   ├── nitrite_urine_decision_dashboard.html
│   │   └── decision_dashboards.zip         # Archived dashboards
│   ├── singular_concepts/          # Individual concept analyses
│   │   ├── blood_count_hemoglobin/ # Hemoglobin family analyses
│   │   ├── blood_count_erythrocytes/
│   │   ├── blood_count_leukocytes/
│   │   ├── blood_count_platelets/
│   │   ├── blood_count_hematocrit/
│   │   └── blood_count_erythrocyte_indices/ # MCV, MCH, MCHC
│   ├── valuesets/                  # FHIR ValueSet resources
│   │   ├── valueset-interpolar-loinc-*.json
│   │   └── valueset-mii-top-300-loinc.json
│   ├── ecl_descendants_baseline/   # Baseline ECL results
│   ├── ecl_fixed_component/        # Fixed component results
│   ├── ecl_component_descendants/  # Component descendants results
│   ├── ecl_fixed_component_property/ # Fixed component+property results
│   └── ecl_fixed_component_system/ # Fixed component+system results
├── scripts/                        # Utility scripts
│   ├── loinc_display_fetcher.py   # LOINC display name fetcher
│   └── test_or_property_ecl.py    # Property ECL testing
└── CLAUDE.md                       # This file
```

### Key Directories

#### `analysis/`
Contains all analysis scripts and test files for evaluating ECL queries against different laboratory concepts.

**Important**: `create_decision_dashboard.py` generates interactive HTML dashboards comparing different ECL strategies (Exp 0-5) for a given LOINC code.

Usage: `python analysis/create_decision_dashboard.py <LOINC_CODE> <output_name>`

#### `output/decision_dashboards/`
Interactive HTML reports showing:
- ECL experiment statistics (recall, precision, F1 scores)
- SNOMED concept attributes (Component, Property, Direct site)
- ECL query details for each experiment
- LOINC code comparison matrix
- Specimen types found
- Decision guidance for choosing the best ECL approach

**Special cases**: MCV, MCH, MCHC dashboards include warning boxes about erythrocyte indices modeling (no Component attribute, uses "Inheres in" relationship).

#### `output/valuesets/`
FHIR-compliant ValueSet resources generated from:
- Interpolar reference mappings
- MII Top 300 LOINC codes
- ECL query results

#### `docs/`
Project documentation including ECL query patterns and rationale.

## Key Strategies & Findings

### 1. ECL Query Approaches

#### Pre-coordinated vs Post-coordinated
**Finding**: Pre-coordinated hierarchies and post-coordinated ECL are NOT always semantically equivalent.

**Example - Methemoglobin**:
- Pre-coordinated: `<< 719541010000106 |Measurement of methemoglobin in blood|`
- Post-coordinated (exact): `Component = 27840003 |Methemoglobin|` → Missing cyanmethemoglobin
- Post-coordinated (descendants): `Component = << 27840003` → Captures cyanmethemoglobin ✓

**Rule**: Use **component descendants** (`= <<`) to achieve semantic equivalence with pre-coordinated hierarchies.

#### Refined ECL Pattern (Recommended)
```
<< 363787002 |Observable entity| :
    << 246093002 |Component| = << [COMPONENT_CONCEPT] |Component|,
    << 370130000 |Property| = << 685451010000100 |Measurement property|,
    << 704327008 |Direct site| = << 119297000 |Blood specimen|,
    << 704327008 |Direct site| != << 122556008 |Cord blood specimen|
```

**Key elements**:
- Component descendants to capture substance derivatives
- Measurement property constraint
- Blood specimen constraint
- Cord blood exclusion (optional, use case dependent)

#### ECL Experiment Variants
1. **ecl_descendants_baseline**: Simple `<< [concept]` queries (baseline)
2. **ecl_fixed_component**: Fixed component, descendant system/property
3. **ecl_component_descendants**: Component descendants exploration
4. **ecl_fixed_component_property**: Fixed component + fixed property
5. **ecl_fixed_component_system**: Fixed component + fixed system (blood specimen)

### 2. Data Sources

#### Interpolar Mapping
- Manual expert curation by Interpolar
- LOINC_PRIMARY field: Primary code for each concept family
- COMPARABILITY_TO_LOINC_PRIMARY: Quality levels (1-5)
  - `1 - quantitativ`: Quantitative, fully comparable
  - `2 - qualitativ`: Qualitative/ordinal
  - `3-5`: Lower comparability
- Used as ground truth for validation

#### LOINC300
- MII Top 300 most important LOINC codes
- File: `Top300 Stand 2018-08-08.xlsx`
- Used to flag high-priority codes

#### Local LOINC CSV
- Path: `C:/Users/
/code/helper/terminologies/LOINC/LoincTable/Loinc.csv`
- 108,248 LOINC codes with display names
- Used for fast local lookup (100% hit rate for project codes)

### 3. Singular Concept Analysis Workflow

For analyzing individual CBC concepts (e.g., hemoglobin, methemoglobin):

1. **Identify Interpolar primary codes**
   ```python
   interpolar_primaries = ['2614-6', '56040-9']  # Methemoglobin example
   ```

2. **Test refined ECL query**
   ```bash
   python analysis/test_hemoglobin_ecl_refined.py
   ```

3. **Generate comparison table**
   ```bash
   python analysis/create_singular_concept_table.py 59260-0  # Hemoglobin
   ```

4. **Generate HTML report**
   ```bash
   python analysis/create_hemoglobin_html.py
   ```

5. **Test semantic equivalence (optional)**
   ```bash
   python analysis/test_methemoglobin_precoord_vs_postcoord.py
   ```

### 4. Results Format

#### JSON Output
```json
{
  "hemoglobin_excl_cord": {
    "ecl": "...",
    "snomed_concept_count": 26,
    "loinc_code_count": 26,
    "loinc_codes": ["59260-0", ...],
    "snomed_to_loinc_mapping": {
      "59260-0": [{
        "snomed_id": "259695003",
        "snomed_fsn": "..."
      }]
    },
    "interpolar_comparison": {
      "interpolar_count": 19,
      "overlap_count": 15,
      "overlap_codes": [...],
      "interpolar_only": [...],
      "ecl_only": [...]
    }
  }
}
```

#### CSV Output
```csv
LOINC_Code,LOINC_Display,In_Interpolar,In_LOINC300,In_ECL,SNOMED_IDs
59260-0,Hemoglobin [Mass/volume] in Blood,Yes,Yes,Yes,259695003
```

#### HTML Report
- Interactive table with all LOINC codes
- Sortable by approach coverage
- Color-coded recommended approach
- SNOMED IDs and FSN labels
- LOINC300 indicator

## Technical Notes

### Authentication
In .env there are three attributes:
- `auth_path` - Directory containing certificate (no trailing slash)
- `auth_file` - Certificate filename (.p12 format)
- `auth_pw` - Certificate password (can be empty string, None, or actual password)
- `loinc_snomed_mapping_path` - Path to LOINC-SNOMED mapping file (sct2_Identifier_Full)

You are not allowed to read .env yourself (prohibited by your config).
Use them to login to the terminology server.

#### Important: Certificate Password
- Windows certificate store may auto-handle passwords, hiding the fact that a password exists
- Empty string `""` ≠ None ≠ no value in .env
- If authentication fails with "Invalid password or PKCS12 data", the password is likely wrong
- User can verify with: `openssl pkcs12 -info -in "path/to/cert.p12" -noout`

### MII OntoServer API Quirks
- The `fhir_vs` parameter must be embedded INSIDE the `url` parameter value for `$expand`
- Correct structure: `?url=http://snomed.info/sct/.../version/...?fhir_vs=ecl/...`
- NOT: `?url=...&fhir_vs=...` (this won't work)
- For `$lookup`: use separate `system` and `version` parameters

### LOINCSNOMED Edition Limitations
- Not all SNOMED CT concepts are included
- Example: Carboxyhemoglobin concepts (719551010000100, 9052005) don't exist
- Always test concept existence before relying on them

## Key Findings & Lessons

### Semantic Gap: Pre-coordinated vs Post-coordinated
**Problem**: Using exact component matching (`Component = X`) misses substance derivatives.

**Example**: Methemoglobin measurements
- Cyanmethemoglobin (4534-4) is modeled as child of methemoglobin in hierarchy
- But component attribute points to distinct substance concept
- Exact component match misses it

**Solution**: Use component descendants (`Component = << X`)
- Captures all substance derivatives and subtypes
- Achieves semantic equivalence with pre-coordinated hierarchies
- Validated: Methemoglobin pre-coord (12 codes) = post-coord descendants (12 codes)

### Refined ECL Performance
- Hemoglobin (excl cord blood): 26 codes, 15/19 (78.9%) Interpolar overlap
- Methemoglobin: 12 codes, 7/14 (50%) Interpolar overlap
- Using descendants captures edge cases like cyanmethemoglobin

### Interpolar vs ECL Coverage
- Interpolar includes some codes ECL misses (different properties, systems)
- ECL finds some codes Interpolar doesn't include (more exhaustive)
- Neither is perfect ground truth - complementary approaches

### Erythrocyte Indices Special Modeling
**Problem**: MCV, MCH, and MCHC use different SNOMED modeling than standard laboratory parameters.

**SNOMED Structure**:
- **No Component attribute**: These concepts do NOT use Component (246093002)
- **Uses "Inheres in" relationship**: Instead use 704319004 |Inheres in|
  - MCV: Inheres in 41898006 |Erythrocyte|
  - MCH/MCHC: Inheres in 38082009 |Hemoglobin|
- **Parent concepts**: Each has a generic parent with 2 descendants (generic + automated count)
  - MCV: 525321010000100 → 30428-7 (generic), 787-2 (automated)
  - MCH: 521361010000106 → 28539-5 (generic), 785-6 (automated)
  - MCHC: 521371010000101 → 28540-3 (generic), 786-4 (automated)

**Solution**: Use **Pre-coordinated Descendants** (Exp 0) approach only
- Query the parent observable entity: `<< [PARENT_CONCEPT]`
- Post-coordinated queries (Exp 1-5) fail because no Component attribute exists
- Parent hierarchy correctly captures both method variants

**Note**: For dashboard generation, use the generic LOINC code (not automated count variant) to access the parent concept.

## Collaboration Guidelines
- **User is the boss**: User decides direction, priorities, what matters
- **Question user assumptions when stuck**: Help debug their thinking
  - ✅ "Have you verified the password actually works?"
  - ✅ "Are you sure that version exists on the server?"
  - ❌ "Do you understand how certificates work?" (condescending)
- **User's knowledge is heterogeneous**: They know some things deeply, others they're figuring out
- **Present options, not interrogations**: Suggest paths forward rather than testing knowledge