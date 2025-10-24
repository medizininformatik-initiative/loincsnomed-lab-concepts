# Exploratory Analysis: Interpolar LOINC Mappings vs SNOMED ECL-Based Value Sets

## Overview
This document outlines experiments comparing Interpolar LOINC primary/secondary code groupings with SNOMED CT-based value sets generated via ECL (Expression Constraint Language) queries.

## Experiments

### 1. **ecl_descendants_baseline** (BASELINE - Intentionally Poor)
Simple descendant queries: `<< [SNOMED Concept]`
- **Purpose:** Establish baseline performance
- **Results:** Precision=0.606, Recall=0.390, F1=0.398
- **Why poor:** Just gets descendants of the entire observable concept, not filtered by component

### 2. **ecl_fixed_component** (PROPER EXPERIMENT)
Component-based queries: `<< 363787002 |Observable entity| : 246093002 |Component| = <<[Component_ID]`
- **Purpose:** Group by SNOMED Component attribute (e.g., all observables measuring Hemoglobin)
- **Expected:** Much better precision and recall

---

## Analysis Pipeline

### Step 1: Convert LOINC Codes to SNOMED Concepts

**Input:**
- Interpolar mapping file: `input/LOINC_Mapping_Interpolar_v3.6 an Debersthäuser 25.09.2025.xlsx`
- All primary LOINC codes (47 codes identified)
- All secondary LOINC codes (356 total code mappings)

**Process:**
1. Read LOINC-SNOMED mapping file from `loinc_snomed_mapping_path` (.env variable)
   - File: `sct2_Identifier_Full_LO1010000_20250921.txt`
2. For each LOINC code in Interpolar:
   - Look up corresponding SNOMED CT concept ID
   - Extract SNOMED concept attributes (Component, Property, Time Aspect, System, Scale Type, Method)
3. Store mapping: `LOINC → SNOMED Concept ID → Attributes`

**Output:**
- `output/ecl_fixed_component/interpolar_loinc_to_snomed_mapping.json`
- Contains: LOINC code, SNOMED concept ID, FSN, component attribute

**Script to create:**
```python
# ecl_fixed_component_step1_convert_loinc_to_snomed.py
```

---

### Step 2: Generate ECL Expressions Based on Component

**Input:**
- SNOMED concepts from Step 1
- Focus: **Component attribute** (704327008 |Direct site|)

**Process:**
For each primary LOINC / SNOMED concept:
1. Extract the "Component" attribute value
2. Generate ECL query:
   ```
   << [Component_Concept_ID] : 704327008 |Direct site| = [System_Concept]
   ```
   - Use descendant-or-self operator `<<` to include the component and all descendants
3. Alternative ECL patterns (for future permutation analysis):
   - Component only: `<< [Component_ID]`
   - Component + Property: `<< [Component_ID] : 370130000 |Property| = [Property_ID]`
   - Component + System: `<< [Component_ID] : 704327008 |Direct site| = [System_ID]`

**Output:**
- `output/ecl_fixed_component/ecl_expressions_by_component.json`
- Contains: Primary LOINC, SNOMED concept, component ID, ECL expression

**Script to create:**
```python
# ecl_fixed_component_step2_generate_ecl_expressions.py
```

**Notes:**
- This exploratory analysis focuses on Component-based ECL
- Future analyses may permute across Method, System, Property attributes
- ECL complexity increases with additional constraints

---

### Step 3: Execute ECL Queries and Create SNOMED Value Sets

**Input:**
- ECL expressions from Step 2

**Process:**
1. Execute each ECL query against LOINCSNOMED Snowstorm API
   - Use existing adapter: `terminology_server_adapters.LOINCSNOMEDSnowstormAdapter`
   - API endpoint: `http://browser.loincsnomed.org/snowstorm/snomed-ct`
   - Branch: `MAIN/LOINC/2025-09-21`
2. For each ECL query result:
   - Collect all SNOMED concept IDs that match
   - Map SNOMED concepts back to LOINC codes (reverse lookup via identifier file)
3. Create FHIR ValueSet:
   - Include all LOINC codes found in ECL expansion
   - Store as FHIR ValueSet JSON

**Output:**
- `output/ecl_fixed_component/valuesets/` directory
  - `valueset-ecl-component-[primary_loinc].json` (one per primary code)
- `output/ecl_fixed_component/ecl_query_results_summary.json`
  - Contains: Primary LOINC, ECL query, SNOMED concept count, LOINC code count

**Script to create:**
```python
# ecl_fixed_component_step3_execute_ecl_create_valuesets.py
```

**Technical Details:**
- Reuse `terminology_server_adapters.py` from helper/loinc_blood_grouper
- Handle API rate limits (add delays if needed)
- Filter for active concepts only

---

### Step 4: Compare ECL-Generated Value Sets with Interpolar

**Input:**
- Interpolar value sets: `output/valuesets/valueset-interpolar-loinc-*.json` (47 files)
- ECL-generated value sets: `output/valuesets_snomed_ecl/valueset-ecl-component-*.json`

**Process:**
For each primary LOINC code:
1. Load Interpolar value set (manual curation)
2. Load ECL-generated value set (automated SNOMED query)
3. Compare LOINC codes:
   - **Overlap:** Codes in both sets
   - **Interpolar-only:** Codes in Interpolar but NOT in ECL
   - **ECL-only:** Codes in ECL but NOT in Interpolar
4. Calculate metrics:
   - Precision: `|Overlap| / |ECL set|`
   - Recall: `|Overlap| / |Interpolar set|`
   - F1-score: `2 * (Precision * Recall) / (Precision + Recall)`
5. Identify discrepancies:
   - Why are certain codes in Interpolar but not ECL? (e.g., different Method, different System)
   - Why are certain codes in ECL but not Interpolar? (e.g., broader Component descendants)

**Output:**
- `output/ecl_fixed_component/comparison_interpolar_vs_ecl.json`
  - Per-primary-code comparison metrics
- `output/ecl_fixed_component/comparison_summary.csv`
  - Aggregated statistics: mean precision, recall, F1
- `output/ecl_fixed_component/comparison_detailed_report.md`
  - Human-readable report with examples of discrepancies

**Script to create:**
```python
# ecl_fixed_component_step4_compare_valuesets.py
```

**Comparison Metrics:**
| Primary LOINC | Interpolar Count | ECL Count | Overlap | Precision | Recall | F1 |
|---------------|------------------|-----------|---------|-----------|--------|-----|
| 1742-6        | 5                | 8         | 4       | 0.50      | 0.80   | 0.62|
| ...           | ...              | ...       | ...     | ...       | ...    | ... |

---

## Future Permutation Analysis

This exploratory analysis focuses on **Component-only ECL queries**. Future analyses could systematically permute:

1. **Component + Property:**
   - ECL: `<< [Component] : 370130000 |Property| = [Property_ID]`
   - Example: Alanine aminotransferase + "Catalytic activity"

2. **Component + System:**
   - ECL: `<< [Component] : 704327008 |Direct site| = [System_ID]`
   - Example: Alanine aminotransferase + "Serum"

3. **Component + Method:**
   - ECL: `<< [Component] : 370132008 |Scale type| = [Scale_ID]`
   - Example: Alanine aminotransferase + "Quantitative"

4. **Component + Property + System:**
   - ECL: `<< [Component] : 370130000 |Property| = [Prop], 704327008 |Direct site| = [Sys]`

5. **Full attribute permutation:**
   - Test all combinations of attributes to find optimal ECL patterns

**Goal:** Identify which attribute combinations yield highest precision/recall compared to Interpolar.

---

## Expected Outcomes

### Hypothesis 1: High Recall, Low Precision
- ECL-based queries (Component descendants) will likely retrieve MORE codes than Interpolar
- Why? Interpolar is manually curated for clinical relevance; ECL includes all SNOMED descendants
- Result: ECL-only codes may include edge cases not clinically relevant

### Hypothesis 2: Attribute Constraints Improve Precision
- Adding Property, System, or Method constraints to ECL will reduce ECL-only codes
- Future permutation analysis will test this

### Hypothesis 3: Some Interpolar Codes Cannot Be Captured by Component-Only ECL
- Interpolar may group codes with different Components but same clinical meaning
- These will appear as Interpolar-only codes

---

## Implementation Notes

### File Paths (from .env)
```bash
# Example paths - update with your local terminology file locations
loinc_snomed_mapping_path=/path/to/terminologies/LOINCSSNOMED/.../sct2_Identifier_Full_LO1010000_YYYYMMDD.txt
SNOMED_TERMINOLOGY_PATH=/path/to/SNOMED/Snapshot/Terminology
```

### Dependencies
- Python 3.6+
- `pandas` (Excel reading)
- `requests` (API calls)
- Existing modules:
  - `terminology_server_adapters.py` (from helper/loinc_blood_grouper)
  - `ecl_permutation_analyzer_simple.py` (for reference)

### Directory Structure
```
mii_lab_snomedloinc/
├── input/
│   └── LOINC_Mapping_Interpolar_v3.6 an Debersthäuser 25.09.2025.xlsx
├── output/
│   ├── valuesets/                          # Interpolar value sets
│   ├── ecl_descendants_baseline/           # Baseline experiment (poor results)
│   └── ecl_fixed_component/                # Component-based experiment
│       ├── valuesets/                      # ECL-generated value sets
│       ├── interpolar_loinc_to_snomed_mapping.json
│       ├── ecl_expressions_by_component.json
│       ├── ecl_query_results_summary.json
│       ├── comparison_interpolar_vs_ecl.json
│       ├── comparison_summary.csv
│       └── charts (PNG)
├── ecl_descendants_baseline_run_all.py     # Baseline experiment
├── ecl_fixed_component_run_all.py          # Proper experiment (TBD)
└── EXPLORATORY_ANALYSIS_PLAN.md (this file)
```

---

## Timeline

1. **Step 1:** LOINC → SNOMED conversion (~30 mins to implement + run)
2. **Step 2:** ECL generation (~15 mins to implement)
3. **Step 3:** Execute ECL queries (~1-2 hours, depends on API rate limits)
4. **Step 4:** Comparison analysis (~30 mins to implement + run)

**Total:** ~3-4 hours for complete pipeline

---

## Success Criteria

✅ All 47 primary LOINC codes successfully mapped to SNOMED concepts
✅ ECL queries execute without errors on LOINCSNOMED Snowstorm
✅ Comparison metrics calculated for all primary codes
✅ Detailed report generated with discrepancy analysis
✅ Framework established for future permutation analysis

---

## Questions to Answer

1. What percentage of Interpolar secondary codes can be recovered via Component-only ECL?
2. Which primary codes have the highest/lowest recall?
3. Are there systematic patterns in Interpolar-only codes? (e.g., specific methods, systems)
4. How many "extra" codes does ECL retrieve? Are they clinically relevant?
5. Does the SNOMED hierarchy structure align with Interpolar's clinical grouping logic?

---

## Next Steps After This Analysis

1. Review discrepancies with clinical domain experts
2. Run permutation analysis with additional attribute constraints
3. Evaluate OntoServer (MII) vs LOINCSNOMED Snowstorm results
4. Propose hybrid approach: ECL queries + manual curation filters
5. Implement automated value set generation pipeline for production use
