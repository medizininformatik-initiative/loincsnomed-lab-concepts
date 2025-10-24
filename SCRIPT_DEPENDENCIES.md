
# Script Dependencies for ecl_fixed_component Experiment

## Timestamp
Created: 2025-10-08

## Source Repository
**Note:** This project originally used external helper scripts from a separate repository. Those scripts have been integrated into the `scripts/` directory of this project.

## Key Scripts Used

### 1. terminology_server_adapters.py
- **Status:** Available in source repo
- **Purpose:** Provides adapters for LOINCSNOMED Snowstorm and OntoServer
- **Usage:** Import directly from helper repo or copy to project

### 2. ecl_permutation_analyzer_simple.py
- **Status:** Available and tested in source repo
- **Purpose:**
  - Load LOINC-SNOMED mappings from identifier file
  - Execute ECL queries against terminology servers
  - Build ECL expressions with permutations
- **Key Functions:**
  - `load_loinc_mappings(identifier_file)` - Loads LOINC→SNOMED mappings
  - `execute_ecl_query(ecl, mappings, limit, adapter)` - Executes ECL and enriches with LOINC codes
  - `build_ecl_query(component_id, site_id, ...)` - Builds ECL expressions

### 3. interactive_ecl_builder.py
- **Status:** Available in source repo
- **Purpose:** Interactive tool to extract SNOMED relationships and build ECL queries
- **Key Functions:**
  - `extract_all_relationships(concept_id, relationship_file, description_file)` - Gets all relationships
  - `build_ecl_from_attributes(attributes)` - Builds ECL from selected attributes
  - `generate_permutations(selected_attrs)` - Generates fixed vs descendant permutations

## Integration Strategy

### Import from project scripts directory
All helper scripts are now integrated into this project:
```python
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent  # Adjust based on your script location
sys.path.insert(0, str(PROJECT_ROOT / 'scripts'))
from ecl_permutation_analyzer_simple import load_loinc_mappings, execute_ecl_query
from terminology_server_adapters import create_adapter
```

## Environment Variables Required

From `.env`:
- `loinc_snomed_mapping_path` - Path to `sct2_Identifier_Full_LO1010000_20250921.txt`

## Testing

Scripts available in `scripts/` directory and can be tested directly from the project root.

Python version: 3.13+
