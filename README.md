# MII Lab LOINC-SNOMED Mapping Analysis

Comprehensive analysis of LOINC to SNOMED CT mappings using the LOINCSNOMED Edition, with a focus on laboratory test concepts and Complete Blood Count (CBC) components.

## Overview

This repository serves two purposes:

### 1. ValueSet Library
Ready-to-use FHIR ValueSets for laboratory concepts, generated through systematic ECL query evaluation:
- **CBC Components**: Hemoglobin, Erythrocytes, Hematocrit, Leukocytes, Platelets, MCV, MCH, MCHC, Methemoglobin
- Multiple ECL query variants per concept (broad to narrow)
- Validated against Interpolar and LOINC300 reference sets
- Available in JSON format with comprehensive metadata

### 2. Analysis Tools & Scripts
Automated tools for exploring and validating LOINC-SNOMED mappings:
- ECL query generator and executor
- Comparative analysis across multiple query approaches
- Interactive HTML report generator
- Batch processing for multiple concepts

## Features

- **Automated ECL Query Generation**: Automatically builds multiple ECL query variants for any LOINC concept
- **CBC Component Analysis**: Comprehensive analysis of all 9 CBC components (Hemoglobin, Erythrocytes, Hematocrit, Leukocytes, Platelets, MCV, MCH, MCHC, Methemoglobin)
- **Interactive HTML Reports**: Visual comparison tables showing LOINC codes captured by different ECL approaches
- **Reference Set Comparison**: Tracks membership in Interpolar and LOINC300 reference sets
- **Refined Query Identification**: Flags the most specific technical representation (Component + Property + Direct site)

## Project Structure

```
.
├── 📚 output/valuesets/          # VALUE SET LIBRARY (PRIMARY OUTPUT)
│   ├── hemoglobin_refined.json          # Focused: Component + Property + System
│   ├── hemoglobin_fixed_component.json  # Broad: All hemoglobin observations
│   ├── hemoglobin_component_descendants.json  # Broadest: Includes variants
│   ├── erythrocytes_refined.json
│   ├── leukocytes_refined.json
│   └── ...                              # All 9 CBC components × multiple approaches
│
├── 📊 output/singular_concepts/  # ANALYSIS RESULTS & REPORTS
│   ├── hemoglobin/
│   │   ├── hemoglobin_ecl_results.json       # Detailed ECL query results
│   │   └── hemoglobin_ecl_comparison.csv     # Comparison table
│   ├── erythrocytes/
│   ├── leukocytes/
│   └── cbc_components_analysis.html    # Interactive HTML report
│
├── 🔧 analysis/                  # ANALYSIS TOOLS & SCRIPTS
│   ├── cbc_component_analyzer.py       # Core ECL analyzer (run for any concept)
│   ├── run_all_cbc_analyses.py         # Batch processor for all CBC components
│   ├── create_cbc_html_tables_v2.py    # HTML report generator
│   └── experiments/                     # Individual ECL experiment runners
│
├── 🛠️ scripts/                   # HELPER UTILITIES
│   ├── terminology_server_adapters.py  # MII OntoServer API client
│   ├── loinc_display_fetcher.py        # LOINC display name resolver
│   ├── interactive_ecl_builder.py      # Interactive ECL query builder
│   └── ecl_permutation_analyzer_simple.py  # ECL permutation analyzer
│
├── 📥 input/                     # INPUT DATA (user-provided)
│   └── (place terminology files here)
│
├── 📖 docs/                      # DOCUMENTATION
│   └── ECL_METHODOLOGY.md              # Detailed ECL query methodology
│
├── .env.example                 # Configuration template
├── CLAUDE.md                    # AI assistant instructions
└── README.md                    # This file
```

### Key Directories

**📚 `output/valuesets/`** - The main deliverable. Use these JSON files as FHIR ValueSets in your implementations.

**📊 `output/singular_concepts/`** - Analysis artifacts showing how ValueSets were derived and validated.

**🔧 `analysis/` & 🛠️ `scripts/`** - Tools for generating new ValueSets or analyzing different concepts.

## Prerequisites

- Python 3.8+
- Access to MII OntoServer with LOINCSNOMED Edition
- PKCS12 certificate (.p12) for authentication
- LOINC-SNOMED mapping file (`sct2_Identifier_Full`)
- Local LOINC distribution (Loinc.csv)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd mii_lab_snomedloinc
```

2. Install dependencies:
```bash
pip install pandas requests python-dotenv
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your paths and credentials
```

4. Place required files:
   - PKCS12 certificate in your secure directory
   - LOINC-SNOMED mapping file (sct2_Identifier_Full)
   - LOINC distribution (Loinc.csv)

## Configuration

Edit `.env` with your local paths:

```env
# Path to directory containing certificate (no trailing slash)
auth_path=C:/Users/username/.secrets

# Certificate filename (PKCS12 format)
auth_file=your_certificate.p12

# Certificate password (leave empty if none)
auth_pw=

# Path to LOINC-SNOMED mapping file
loinc_snomed_mapping_path=C:/path/to/sct2_Identifier_Full_LO1010000_20250921.txt

# Path to local LOINC CSV file
loinc_csv_path=C:/path/to/Loinc.csv
```

**Important**: Never commit your `.env` file or certificates to version control!

## 📚 Using the ValueSet Library

### Quick Start: Using Pre-generated ValueSets

The `output/valuesets/` directory contains ready-to-use FHIR ValueSets for CBC components. Each concept has multiple ValueSet variants optimized for different use cases:

#### ValueSet Naming Convention
```
<component>_<approach>.json
```

#### Available Approaches (Narrow to Broad)

| Approach | File Suffix | Use Case | Typical Size |
|----------|-------------|----------|--------------|
| **Refined** | `_refined.json` | Clinical decision support (focused) | 5-10 codes |
| **Fixed Component + Property** | `_fixed_component_property.json` | Specific measurement types | 5-20 codes |
| **Fixed Component + System** | `_fixed_component_system.json` | Specific specimen types | 30-40 codes |
| **Fixed Component** | `_fixed_component.json` | General observations | 50-60 codes |
| **Component Descendants** | `_component_descendants.json` | Comprehensive coverage | 200+ codes |
| **Pre-coordinated** | `_precoord.json` | Calculated indices (MCV, MCH, MCHC) | 2-264 codes |

#### Example: Choosing a Hemoglobin ValueSet

```javascript
// For anemia screening (focused, primary use case)
import hemoglobin_refined from './output/valuesets/hemoglobin_refined.json'
// Contains: 5 LOINC codes - blood hemoglobin mass concentration

// For research on all hemoglobin tests
import hemoglobin_component_descendants from './output/valuesets/hemoglobin_component_descendants.json'
// Contains: 267 LOINC codes - includes HbA1c, HbF, HbS, variants

// For quality measures (consistent measurement type)
import hemoglobin_fixed_component_property from './output/valuesets/hemoglobin_fixed_component_property.json'
// Contains: 5 LOINC codes - mass concentration only
```

### ValueSet Metadata

Each ValueSet JSON includes:
- **ECL expression**: The SNOMED query used to generate it
- **LOINC codes**: Complete list of codes in the value set
- **SNOMED concept count**: Number of SNOMED concepts matched
- **Timestamp**: When the value set was generated
- **Attributes**: Component, Property, Direct site (when applicable)

### Available CBC Components

| Component | Primary LOINC | Category | Refined Set Size | Full Set Size |
|-----------|---------------|----------|------------------|---------------|
| **Hemoglobin** | 59260-0 | Direct Observation | 5 codes | 264 codes |
| **Erythrocytes** | 26453-1 | Direct Observation | TBD | 213 codes |
| **Hematocrit** | 20570-8 | Direct Observation | TBD | 213 codes |
| **Leukocytes** | 26464-8 | Direct Observation | TBD | 741 codes |
| **Platelets** | 26515-7 | Direct Observation | TBD | 26 codes |
| **Methemoglobin** | 2614-6 | Direct Observation | TBD | 17 codes |
| **MCV** | 30428-7 | Calculated Index | 2 codes | 2 codes |
| **MCH** | 28539-5 | Calculated Index | TBD | 264 codes |
| **MCHC** | 28540-3 | Calculated Index | 2 codes | 2 codes |

### Validation & Quality

All ValueSets are:
- ✅ Generated from validated LOINCSNOMED Edition mappings
- ✅ Compared against Interpolar reference set (empirical usage data)
- ✅ Compared against LOINC300 reference set (common tests)
- ✅ Documented with complete ECL expressions
- ✅ Version-tracked with generation timestamps

**Note**: While systematically generated and validated, clinical review is recommended before production use.

## 🔧 ECL Query Approaches

This project evaluates 7+ different ECL query strategies:

### 1. ECL Descendants Baseline
```ecl
<< ComponentID
```
Simple descendant search of the SNOMED component concept.

### 2. ECL Fixed Component
```ecl
<< 363787002 |Observable entity| :
   246093002 |Component| = ComponentID
```
Observable entities with fixed component value.

### 3. ECL Component Descendants
```ecl
<< 363787002 |Observable entity| :
   246093002 |Component| = << ComponentID
```
Observable entities with component or descendants.

### 4. ECL Fixed Component + Property
```ecl
<< 363787002 |Observable entity| :
   246093002 |Component| = ComponentID,
   370130000 |Property| = PropertyID
```
Adds property constraint (e.g., Mass concentration).

### 5. ECL Fixed Component + System
```ecl
<< 363787002 |Observable entity| :
   246093002 |Component| = ComponentID,
   704327008 |Direct site| = << SystemID
```
Adds specimen/system constraint (e.g., Blood specimen).

### 6. Refined Query (Most Specific)
```ecl
<< 363787002 |Observable entity| :
   246093002 |Component| = ComponentID,
   370130000 |Property| = << PropertyID,
   704327008 |Direct site| = << SystemID
```
Complete specification with all three attributes. This is flagged as "Refined Query" in the output.

### 7. Pre-coordinated Descendants
```ecl
<< PrecoordinatedConceptID
```
Used for calculated indices (MCV, MCH, MCHC) that have pre-coordinated SNOMED concepts.

## Usage

### For ValueSet Consumers: Using the Library

**If you just want to use the pre-generated ValueSets**, no installation is needed! Simply:

1. Browse `output/valuesets/` directory
2. Select the appropriate ValueSet variant for your use case (see [ValueSet Library](#-using-the-valueset-library) section)
3. Import the JSON file into your system

```bash
# Example: Copy ValueSets to your project
cp output/valuesets/hemoglobin_refined.json /your/project/valuesets/
cp output/valuesets/leukocytes_refined.json /your/project/valuesets/
```

### For Analysts: Running the Analysis Tools

**If you want to generate new ValueSets or analyze different concepts:**

#### 1. Analyze a Single Component

```bash
python analysis/cbc_component_analyzer.py <primary_loinc> <component_name>
```

Example:
```bash
python analysis/cbc_component_analyzer.py 59260-0 hemoglobin
```

Generates:
- `output/singular_concepts/hemoglobin/hemoglobin_ecl_results.json` - Detailed results
- `output/singular_concepts/hemoglobin/hemoglobin_ecl_comparison.csv` - Comparison table

#### 2. Batch Process All CBC Components

```bash
python analysis/run_all_cbc_analyses.py
```

Runs comprehensive ECL analysis for all 9 CBC components. Takes ~5-10 minutes.

#### 3. Generate Interactive HTML Reports

```bash
python analysis/create_cbc_html_tables_v2.py
```

Creates: `output/singular_concepts/cbc_components_analysis.html`

Interactive tables showing:
- LOINC codes and display names
- Refined Query designation (most specific technical representation)
- Interpolar and LOINC300 membership
- Results from all ECL approaches (✓ = captured)
- Number of approaches that captured each code

#### 4. Exploring Individual Experiments

```bash
# Run specific ECL approach across multiple concepts
python analysis/experiments/ecl/ecl_fixed_component_run_all.py
python analysis/experiments/ecl/ecl_component_descendants_run_all.py
```

#### 5. Interactive ECL Query Building

For exploratory analysis of a LOINC code:

```bash
python scripts/interactive_ecl_builder.py <LOINC_CODE>
```

This interactive tool:
1. Extracts all SNOMED relationships for the LOINC code
2. Lets you select which attributes to use in ECL
3. Generates all permutations (fixed vs descendants for each attribute)
4. Executes queries and compares results

Example:
```bash
python scripts/interactive_ecl_builder.py 787-2
# Interactive prompts guide you through attribute selection
# Results saved to ecl_results/ directory
```

#### 6. ECL Permutation Analysis

Analyze all possible ECL variations systematically:

```bash
python scripts/ecl_permutation_analyzer_simple.py
```

Useful for understanding which attribute combinations yield the best results.

## Understanding the Output

### Comparison CSV Files

Each component gets a CSV file (e.g., `hemoglobin_ecl_comparison.csv`) with columns:
- `LOINC_Code`: The LOINC code
- `LOINC_Display`: Human-readable name
- `SNOMED_CT_ID`: Mapped SNOMED concept ID
- `FSN`: Fully Specified Name from SNOMED
- `Is_Primary`: Whether this is the primary/reference code
- `Refined_Query`: Technical designation for most specific query results
- `In_Interpolar`: Membership in Interpolar reference set
- `In_LOINC300`: Membership in LOINC300 reference set
- `ecl_*_Present`: Whether captured by each ECL approach
- `Approach_Count`: Total number of approaches that captured this code

### ECL Results JSON Files

Detailed results for each ECL experiment (e.g., `hemoglobin_ecl_results.json`):
```json
{
  "timestamp": "2025-10-13T12:36:06",
  "primary_loinc": "59260-0",
  "component_name": "hemoglobin",
  "snomed_concept_id": "214131010000101",
  "attributes": {
    "property": "118556004",
    "direct_site": "119297000",
    "component": "38082009"
  },
  "experiments": {
    "refined_base": {
      "ecl_expression": "...",
      "loinc_codes": ["59260-0", "103750-6", ...],
      "snomed_concept_count": 5,
      "execution_time": 1.257
    }
  }
}
```

### HTML Reports

Interactive tables with:
- Color-coded sections for Direct Observations vs Calculated Indices
- Primary codes highlighted in yellow
- Visual badges for Refined Query, Interpolar, and LOINC300 membership
- Checkmarks for ECL approach results
- Sortable columns
- Print-friendly styling

## Key Findings

### CBC Analysis Results (All 9 Components)

| Component | Category | LOINC Codes | Primary Code |
|-----------|----------|-------------|--------------|
| Hemoglobin | Direct Observation | 264 | 59260-0 |
| Methemoglobin | Direct Observation | 17 | 2614-6 |
| Erythrocytes | Direct Observation | 213 | 26453-1 |
| Hematocrit | Direct Observation | 213 | 20570-8 |
| Leukocytes | Direct Observation | 741 | 26464-8 |
| Platelets | Direct Observation | 26 | 26515-7 |
| MCV | Calculated Index | 2 | 30428-7 |
| MCH | Calculated Index | 264 | 28539-5 |
| MCHC | Calculated Index | 2 | 28540-3 |

**Total**: 1,742 LOINC codes across all CBC components

### Query Effectiveness

- **Refined Query (Component + Property + System)**: Most specific, typically 5-10 codes per component for direct observations
- **Fixed Component**: Broader coverage, captures ~50-60 codes for major components
- **Component Descendants**: Broadest coverage, captures 200+ codes including variants
- **Pre-coordinated**: Only 2 codes for calculated indices (MCV, MCHC), more for MCH

### Important Notes

- **Interpolar is NOT a gold standard**: It represents empirical real-world usage data, not a validated mapping reference
- **LOINC300**: Common test reference set, useful for identifying frequently used codes
- **Refined Query designation**: Technical flag for most specific query, NOT a clinical quality judgment

## MII OntoServer API Quirks

When working with the MII OntoServer:

1. **Parameter Embedding**: The `fhir_vs` parameter must be embedded INSIDE the `url` parameter:
   ```
   ?url=http://snomed.info/sct/...?fhir_vs=ecl/...
   ```
   NOT as separate parameters: `?url=...&fhir_vs=...`

2. **$lookup vs $expand**: Use separate `system` and `version` parameters for `$lookup` operations

3. **Certificate Authentication**: Windows certificate store may auto-handle passwords, hiding password requirements

## Contributing

Contributions are welcome! Please ensure:
- No secrets or credentials in commits
- Clear documentation for new ECL approaches
- Test with multiple LOINC concepts before submitting

## License

[Add your license here]

## References

- [SNOMED CT](https://www.snomed.org/)
- [LOINC](https://loinc.org/)
- [LOINCSNOMED Edition](https://confluence.ihtsdotools.org/display/DOCLOINC/)
- [ECL Specification](https://confluence.ihtsdotools.org/display/DOCECL/)
- [MII CORD-MI Project](https://www.medizininformatik-initiative.de/)

## Contact

[Add contact information or links]

## Acknowledgments

This work is part of the Medical Informatics Initiative (MII) laboratory data harmonization efforts.
