# Next Steps & Future Improvements

## Overview
This document outlines potential improvements to make the codebase more generalizable and maintainable. The current implementation is tightly coupled to specific reference datasets (Interpolar, MII Top 300), but the methodology can be applied to any reference value sets.

---

## 1. Generalize Reference ValueSet Handling

### Current State
- Scripts hardcode references to "Interpolar" and "MII300"
- File paths and column names are specific to these datasets
- Comparison logic assumes these specific formats

### Goal
Allow users to evaluate ECL queries against **any** reference value set, making the tool useful beyond the MII Lab use case.

### Proposed Architecture

#### Option A: Configuration-Driven Approach
Create a configuration file to define reference value sets:

**`config/reference_valuesets.json`**
```json
{
  "reference_sets": [
    {
      "id": "interpolar",
      "name": "Interpolar Expert Mappings",
      "type": "fhir_valueset_directory",
      "path": "output/valuesets/",
      "pattern": "valueset-interpolar-loinc-*.json",
      "description": "Expert-curated LOINC mappings from Interpolar project"
    },
    {
      "id": "mii300",
      "name": "MII Top 300",
      "type": "fhir_valueset_file",
      "path": "output/valuesets/valueset-mii-top-300-loinc.json",
      "description": "Most important 300 LOINC codes for German medical informatics"
    },
    {
      "id": "custom_excel",
      "name": "Custom Excel Mapping",
      "type": "excel",
      "path": "input/custom_mapping.xlsx",
      "sheet_name": "LOINC Mapping",
      "header_row": 0,
      "primary_code_column": "LOINC_PRIMARY",
      "secondary_code_column": "LOINC",
      "filter_column": "QUALITY",
      "filter_values": ["high", "medium"]
    },
    {
      "id": "simple_csv",
      "name": "Simple CSV List",
      "type": "csv",
      "path": "input/loinc_codes.csv",
      "loinc_column": "code"
    }
  ]
}
```

**Usage:**
```bash
# Generate dashboard with specific reference set
python analysis/create_decision_dashboard.py 59260-0 hemoglobin --reference-set interpolar

# Run ECL experiment comparing against custom reference
python analysis/experiments/ecl/ecl_fixed_component_run_all.py --reference-set custom_excel

# Compare multiple reference sets
python analysis/create_decision_dashboard.py 59260-0 hemoglobin --reference-sets interpolar,mii300,custom_csv
```

#### Option B: Plugin Architecture
Create a loader plugin system:

**`scripts/reference_valueset_loaders/`**
```
base_loader.py          # Abstract base class
fhir_valueset_loader.py # Loads FHIR ValueSet JSON
excel_loader.py         # Loads Excel with configurable columns
csv_loader.py           # Loads simple CSV files
api_loader.py           # Fetches from terminology server
```

**Usage:**
```python
from scripts.reference_valueset_loaders import load_reference_set

# Auto-detect format and load
ref_set = load_reference_set('path/to/file.xlsx',
                              primary_column='LOINC_PRIMARY',
                              secondary_column='LOINC')

# Use in comparison
comparison = compare_ecl_results(ecl_results, ref_set)
```

#### Option C: Simple Convention-Based Approach
Establish file naming conventions:

```
reference_sets/
├── interpolar/
│   ├── metadata.json          # Name, description, version
│   └── codes_by_primary.json  # { "primary_code": ["code1", "code2", ...] }
├── mii300/
│   ├── metadata.json
│   └── codes_by_primary.json
└── my_custom_set/
    ├── metadata.json
    └── codes_by_primary.json
```

All scripts automatically discover reference sets by scanning this directory.

---

## 2. Refactor Comparison Logic

### Current State
Comparison code scattered across multiple scripts with duplicated logic.

### Proposed Solution
Create a unified comparison module:

**`scripts/ecl_comparison.py`**
```python
class ECLComparison:
    def __init__(self, ecl_results, reference_set):
        self.ecl_results = ecl_results
        self.reference_set = reference_set

    def calculate_metrics(self):
        """Calculate precision, recall, F1"""
        return {
            'precision': ...,
            'recall': ...,
            'f1': ...,
            'overlap_codes': ...,
            'ecl_only_codes': ...,
            'reference_only_codes': ...
        }

    def generate_comparison_table(self):
        """Generate pandas DataFrame for analysis"""
        ...

    def export_dashboard_data(self):
        """Export data in format for HTML dashboards"""
        ...
```

**Benefits:**
- Single source of truth for metrics calculation
- Easy to add new comparison metrics
- Testable in isolation
- Reusable across all experiments

---

## 3. Improve Dashboard Generation

### Current State
Decision dashboards are generated per-concept with hardcoded assumptions.

### Proposed Improvements

#### 3.1 Template-Based Dashboard Generation
Separate data from presentation:

```
templates/
├── dashboard_template.html     # Jinja2 template
├── styles.css                  # Shared styles
└── components/
    ├── metrics_card.html
    ├── code_comparison_table.html
    └── ecl_query_display.html
```

#### 3.2 Multi-Reference Dashboard
Allow comparing ECL results against multiple reference sets simultaneously:

```python
python create_decision_dashboard.py 59260-0 hemoglobin \
    --reference-sets interpolar,mii300,custom_set \
    --output hemoglobin_multi_ref_dashboard.html
```

Dashboard shows:
- ECL Experiment 0 vs Interpolar: Precision 78%, Recall 85%
- ECL Experiment 0 vs MII300: Precision 92%, Recall 100%
- ECL Experiment 0 vs Custom: Precision 65%, Recall 70%

#### 3.3 Batch Dashboard Generation
Generate dashboards for multiple concepts at once:

```python
python create_batch_dashboards.py \
    --concepts 59260-0,789-8,2614-6 \
    --reference-set interpolar \
    --output-dir output/dashboards/
```

---

## 4. Standardize Output Formats

### Current State
Different scripts produce different output formats (JSON, CSV, HTML).

### Proposed Standards

#### 4.1 Standard Result Format
All ECL experiments output the same JSON structure:

```json
{
  "metadata": {
    "experiment_id": "ecl_fixed_component",
    "timestamp": "2025-01-15T10:30:00Z",
    "ecl_query": "...",
    "loinc_code": "59260-0"
  },
  "results": {
    "snomed_concepts": [...],
    "loinc_codes": [...],
    "concept_count": 26
  },
  "comparison": {
    "reference_set": "interpolar",
    "metrics": {
      "precision": 0.789,
      "recall": 0.850,
      "f1": 0.818
    }
  }
}
```

#### 4.2 Standard CSV Export
Common columns across all exports:
- `LOINC_Code`
- `LOINC_Display`
- `SNOMED_ID`
- `SNOMED_FSN`
- `In_Reference_Set` (boolean)
- `In_ECL_Result` (boolean)
- `Match_Type` (exact_match, ecl_only, reference_only)

---

## 5. Create Utility Modules

### Proposed Structure

```
scripts/
├── reference_valueset_loader.py    # Load any reference format
├── ecl_comparison.py               # Calculate comparison metrics
├── dashboard_generator.py          # Generate HTML dashboards
├── fhir_valueset_builder.py       # Build FHIR ValueSets
└── loinc_display_fetcher.py       # (already exists)
```

### Example: `reference_valueset_loader.py`

```python
from pathlib import Path
from typing import Dict, List, Union

class ReferenceValueSetLoader:
    """Generic loader for reference value sets in various formats"""

    @staticmethod
    def load(source: Union[str, Path], **kwargs) -> Dict[str, List[str]]:
        """
        Load a reference value set from any supported format.

        Returns:
            Dict mapping primary LOINC code to list of related codes
            { "59260-0": ["59260-0", "55782-7", ...], ... }
        """
        source_path = Path(source)

        if source_path.is_dir():
            return ReferenceValueSetLoader._load_fhir_directory(source_path)
        elif source_path.suffix == '.json':
            return ReferenceValueSetLoader._load_fhir_valueset(source_path)
        elif source_path.suffix == '.xlsx':
            return ReferenceValueSetLoader._load_excel(source_path, **kwargs)
        elif source_path.suffix == '.csv':
            return ReferenceValueSetLoader._load_csv(source_path, **kwargs)
        else:
            raise ValueError(f"Unsupported format: {source_path.suffix}")

    @staticmethod
    def _load_fhir_directory(directory: Path) -> Dict[str, List[str]]:
        """Load all FHIR ValueSets from directory"""
        ...

    @staticmethod
    def _load_fhir_valueset(file_path: Path) -> Dict[str, List[str]]:
        """Load single FHIR ValueSet JSON"""
        ...

    @staticmethod
    def _load_excel(file_path: Path, **kwargs) -> Dict[str, List[str]]:
        """Load from Excel with configurable columns"""
        ...

    @staticmethod
    def _load_csv(file_path: Path, **kwargs) -> Dict[str, List[str]]:
        """Load from simple CSV"""
        ...
```

---

## 6. Add Validation & Testing

### 6.1 Reference ValueSet Validation
Ensure reference sets are valid before use:

```python
# scripts/validate_reference_set.py
python scripts/validate_reference_set.py input/my_reference.xlsx
```

Checks:
- All LOINC codes are valid format (dashes, numbers)
- No duplicates within a primary group
- Display names exist (if provided)
- Required columns present

### 6.2 Unit Tests
Add tests for core functionality:

```
tests/
├── test_reference_loader.py       # Test all loader formats
├── test_ecl_comparison.py        # Test metrics calculation
├── test_dashboard_generation.py  # Test HTML generation
└── fixtures/                     # Sample test data
    ├── sample_interpolar.xlsx
    ├── sample_fhir_valueset.json
    └── sample_ecl_results.json
```

---

## 7. Documentation Improvements

### 7.1 User Guide
Create `docs/USER_GUIDE.md`:
- How to prepare your own reference value sets
- Supported file formats and column mappings
- Running ECL experiments with custom references
- Interpreting dashboard results

### 7.2 API Documentation
Document all utility modules:
- Function signatures
- Parameter descriptions
- Return value formats
- Usage examples

### 7.3 Tutorial Notebooks
Create Jupyter notebooks showing:
- Basic ECL experiment workflow
- Custom reference set creation
- Result analysis and visualization
- Comparing multiple reference sets

---

## 8. Command-Line Interface Improvements

### Current State
Each script has different argument patterns.

### Proposed: Unified CLI

```bash
# Main CLI entry point
python -m mii_lab_snomedloinc <command> [options]

# Commands
mii_lab_snomedloinc ecl-experiment <loinc_code> --experiment fixed_component --reference interpolar
mii_lab_snomedloinc dashboard <loinc_code> --name hemoglobin --reference interpolar
mii_lab_snomedloinc validate-reference <file_path>
mii_lab_snomedloinc compare-results <experiment_dir> --references interpolar,mii300
mii_lab_snomedloinc create-valueset --from-ecl "<<..." --name my_valueset
```

Benefits:
- Consistent interface
- Easier to remember
- Better help documentation
- Can add bash completion

---

## 9. Performance Optimizations

### 9.1 Caching
Cache terminology server responses:
```python
# Cache ECL query results for 24 hours
@cache(ttl=86400)
def execute_ecl_query(ecl, adapter):
    ...
```

### 9.2 Parallel Processing
Run multiple ECL experiments in parallel:
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(run_ecl_experiment, experiment_configs)
```

### 9.3 Incremental Results
For large batch runs, save results incrementally:
```python
# Don't load all results in memory
for primary_code in primary_codes:
    result = run_experiment(primary_code)
    save_to_disk(result)  # Save immediately
```

---

## 10. Packaging & Distribution

### 10.1 Make it pip-installable
```bash
pip install mii-lab-snomedloinc
```

**Setup structure:**
```
setup.py or pyproject.toml
mii_lab_snomedloinc/
├── __init__.py
├── cli.py              # Command-line entry point
├── loaders/            # Reference set loaders
├── experiments/        # ECL experiment runners
└── utils/              # Utility functions
```

### 10.2 Docker Container
Provide pre-configured environment:
```dockerfile
FROM python:3.11
RUN pip install mii-lab-snomedloinc
ENTRYPOINT ["mii_lab_snomedloinc"]
```

Usage:
```bash
docker run -v ./data:/data mii-lab-snomedloinc \
    dashboard 59260-0 --reference /data/my_reference.xlsx
```

---

## Implementation Priority

### Phase 1: Core Generalization (High Priority)
1. Create `reference_valueset_loader.py` utility
2. Update 2-3 key scripts to use generic loader as examples
3. Document reference set format requirements

### Phase 2: Refactor Comparison Logic (Medium Priority)
4. Extract comparison logic into `ecl_comparison.py`
5. Update all experiment scripts to use unified comparison
6. Add basic unit tests

### Phase 3: Enhanced Dashboards (Medium Priority)
7. Create template-based dashboard generator
8. Support multiple reference sets in one dashboard
9. Add batch dashboard generation

### Phase 4: Developer Experience (Lower Priority)
10. Add comprehensive documentation
11. Create tutorial notebooks
12. Implement unified CLI
13. Add validation tools

### Phase 5: Distribution (Optional)
14. Package for pip installation
15. Create Docker container
16. Publish documentation site

---

## Quick Wins

If time is limited, these changes provide maximum value with minimum effort:

1. **Create `reference_valueset_loader.py`** (~2 hours)
   - Single module that handles all formats
   - Immediate benefit to anyone wanting to use custom references

2. **Add `--reference-set` parameter** to top 3 scripts (~1 hour)
   - `create_decision_dashboard.py`
   - `ecl_fixed_component_run_all.py`
   - `create_valuesets_from_interpolar.py` → rename to `create_valuesets_from_reference.py`

3. **Document reference formats** in README (~30 min)
   - Show 2-3 examples of acceptable input formats
   - Explain column name requirements

**Total: ~4 hours of work makes the tool 80% more generalizable.**

---

## Questions to Decide

Before implementing, consider:

1. **Which reference set formats are most important?**
   - FHIR ValueSet JSON (standard but complex)
   - Excel (user-friendly but requires pandas)
   - CSV (simple but limited metadata)
   - API endpoint (flexible but requires network)

2. **How important is backward compatibility?**
   - Keep existing Interpolar-specific scripts?
   - Migrate everything to generic versions?
   - Support both during transition?

3. **What level of validation is needed?**
   - Trust user input?
   - Strict validation with helpful error messages?
   - Auto-correction of common issues?

4. **Target audience?**
   - Medical informaticians (comfortable with code)
   - Clinical users (need GUI?)
   - Other FHIR implementers (need packaging)

---

## Contributing

Once generalized, this tool could benefit the broader FHIR/terminology community. Consider:
- Open-sourcing under permissive license (MIT/Apache)
- Publishing methodology paper describing the approach
- Creating example reference sets for common use cases
- Engaging with HL7 FHIR community for feedback

---

*This document is a living roadmap. Update as priorities and requirements evolve.*
