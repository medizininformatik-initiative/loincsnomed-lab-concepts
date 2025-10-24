# Input Files Documentation

This document describes the contents of  files in the `input/` folder for later reference. The files are available at request

---

## 1. LOINC_Mapping_Interpolar_v3.6 an Debersthäuser 25.09.2025.xlsx

**File Path:** `input/LOINC_Mapping_Interpolar_v3.6 an Debersthäuser 25.09.2025.xlsx`

### Overview

A comprehensive LOINC mapping table for the INTERPOLAR project that establishes relationships between laboratory parameters and LOINC codes.

### Metadata

- **Version:** 3.6
- **Date:** September 15, 2025
- **Responsible:** Martin Federbusch
- **LOINC Version Used:** v2.75

### File Structure

- **Total Records:** 625 laboratory parameter mappings
- **Total Columns:** 35
- **Sheet Name:** "LOINC Mapping Interpolar"
- **Header Row:** Row 18 (rows 0-7 contain metadata, rows 9-16 contain column descriptions)

### Column Groups

#### INTERPOLAR-Specific Columns (1-8)

1. **SORT_NUM** - Sorting/ordering number for records
   - Data completeness: 100%

2. **LOINC** - LOINC codes from LOINC v2.75 that match INTERPOLAR lab parameters
   - Data completeness: 100%
   - Purpose: Identifies FHIR lab observations eligible for INTERPOLAR algorithms

3. **LOINC_PRIMARY** - Primary LOINC code used as linking ID
   - Data completeness: 100%
   - Purpose: Groups comparable lab values; used to link with drug-kidney and drug-disease lists
   - Note: Lab values sharing the same LOINC_PRIMARY are considered comparable

4. **COMPARABILITY_TO_LOINC_PRIMARY** - Comparability rating system
   - Data completeness: 100%
   - Values:
     - `1 - quantitativ` (356 records, 57%): Nearly unrestricted use, unit conversion possible
     - `2 - cutoff_Fragestellung` (36 records, 6%): Usable with ULN/LLN comparison only, no unit conversion
     - `3 - qualitativ` (30 records, 5%): Qualitative, context-dependent interpretation
     - `4 - berechnet` (9 records, 1%): Requires calculation with additional parameters
     - `5 - nein` (163 records, 26%): Not comparable to primary LOINC
     - `unklar` (31 records, 5%): Unclear comparability

5. **COMMENT_COMPARABILITY** - Additional notes on comparability
   - Data completeness: 16.5%

6. **MII_TOP_300** - Boolean flag indicating inclusion in MII Top 300 list
   - Data completeness: 76%
   - Distribution: 206 True, 269 False

7. **GERMAN_NAME_LOINC_PRIMARY** - German translation of LONG_COMMON_NAME
   - Data completeness: 100%
   - Source: LOINC v2.75

8. **SEARCH_NAME** - Search term used to find matching LOINC codes
   - Data completeness: 100%

#### Standard LOINC Database Fields (9-35)

These columns contain standard LOINC metadata:

- **LONG_COMMON_NAME** (100% complete) - Full descriptive name
- **EXAMPLE_UNITS** (63.5% complete) - Example measurement units
- **EXAMPLE_UCUM_UNITS** (64.6% complete) - UCUM-standardized units
- **COMMON_TEST_RANK** (76% complete) - Frequency ranking
- **COMPONENT** (76% complete) - What is measured (e.g., Hemoglobin, Glucose)
- **PROPERTY** (76% complete) - Type of measurement (e.g., MCnc, SCnc, Num)
- **TIME_ASPCT** (76% complete) - Time aspect (e.g., Pt = point in time)
- **SYSTEM** (76% complete) - Sample type (e.g., Blood, Urine, Serum)
- **SCALE_TYP** (76% complete) - Scale type (e.g., Qn = Quantitative)
- **METHOD_TYP** (20.3% complete) - Measurement method
- **CLASS** (76% complete) - LOINC class (e.g., CHEM, HEM, DRUG/TOX)
- **STATUS** (76% complete) - Status (e.g., ACTIVE, DEPRECATED)
- And 23 additional standard LOINC fields

### Primary Use Cases

1. **FHIR Lab Observation Processing** - Identifies which LOINC codes in FHIR observations can be used in INTERPOLAR algorithms
2. **Comparability Assessment** - Determines if lab values from different sources/methods can be compared
3. **Drug Interaction Checking** - Links lab parameters to drug-kidney and drug-disease interaction rules
4. **Localization** - Provides German translations for clinical user interfaces
5. **Quality Control** - Validates quantitative comparability before applying clinical algorithms

### Key Insights

- 57% of mapped LOINCs are quantitatively comparable with unit conversion support
- 26% are explicitly marked as not comparable to their primary LOINC
- 206 entries (33%) are part of the MII Top 300 most commonly used lab tests
- Primary use is for the INTERPOLAR clinical decision support system

---

## 2. Top300 Stand 2018-08-08.xlsx

**File Path:** `input/Top300 Stand 2018-08-08.xlsx`

### Overview

A ranked list of the top 300 most frequently used laboratory parameters across German healthcare institutions, with detailed LOINC metadata.

### Metadata

- **Date:** August 8, 2018
- **Total Records:** 935 LOINC codes
- **Total Columns:** 50
- **Sheet Name:** "Sheet 1"

### File Structure

- **Total Records:** 935 LOINC code entries
- **Unique Primary LOINCs:** 300
- **Unique Secondary LOINCs:** 924
- **Rank Range:** 1-300

### Key Columns

#### Custom MII Columns

1. **rank** - Frequency ranking (1-300)
   - Lower number = more frequently used
   - Example: Rank 1 = Kreatinin (Creatinine)

2. **primär** - Primary LOINC code
   - 300 unique primary codes representing the top 300 lab parameters

3. **usedInLabs** - Number of labs using this specific LOINC variant
   - Range: 1-5
   - Indicates how common this particular code variant is across institutions

4. **sekundär** - Secondary/alternative LOINC code
   - 924 unique secondary codes
   - Represents variations in measurement method, sample type, or units

5. **GERMAN** - German name for the laboratory parameter

#### Standard LOINC Columns (50 total)

Contains all standard LOINC database fields including:
- COMPONENT, PROPERTY, TIME_ASPCT, SYSTEM, SCALE_TYP, METHOD_TYP
- LONG_COMMON_NAME, SHORTNAME, EXAMPLE_UNITS, EXAMPLE_UCUM_UNITS
- COMMON_TEST_RANK, COMMON_ORDER_RANK, COMMON_SI_TEST_RANK
- STATUS, CLASS, CLASSTYPE, DefinitionDescription
- And 36 additional LOINC metadata fields

### Top 10 Most Commonly Used Lab Parameters in 2018 (example)

| Rank | Primary LOINC | Used in Labs | German Name | English Name |
|------|---------------|--------------|-------------|--------------|
| 1 | 59826-8 | 5 | Kreatinin | Creatinine [Moles/volume] in Serum or Plasma |
| 2 | 26464-8 | 5 | Leukozyten | Leukocytes [#/volume] in Blood |
| 3 | 20570-8 | 5 | Hämatokrit | Hematocrit [Volume Fraction] of Blood |
| 4 | 6690-2 | 5 | Leukozyten | Leukocytes [#/volume] in Blood |
| 5 | 789-8 | 5 | Erythrozyten | Erythrocytes [#/volume] in Blood |
| 6 | 718-7 | 5 | Hämoglobin | Hemoglobin [Mass/volume] in Blood |
| 7 | 777-3 | 5 | Thrombozyten | Platelets [#/volume] in Blood |
| 8 | 33914-3 | 5 | GFR | Glomerular filtration rate |
| 9 | 2345-7 | 5 | Glucose | Glucose [Mass/volume] in Serum or Plasma |
| 10 | 3094-0 | 5 | BUN | Urea nitrogen [Mass/volume] in Serum or Plasma |

### Data Characteristics

- **Multiple variants per rank:** Each primary LOINC (rank) typically has 2-4 secondary variants
  - Different measurement methods (e.g., automated vs. manual count)
  - Different sample types (e.g., serum, plasma, arterial blood)
  - Different units (e.g., mass concentration vs. molar concentration)

- **Standardization level:** `usedInLabs` value of 5 indicates maximum standardization across institutions

### Primary Use Cases

1. **Prioritization** - Identifies which lab parameters to prioritize for standardization efforts
2. **Interoperability** - Shows which LOINC codes are most critical for data exchange
3. **Variant Analysis** - Reveals common variations in how labs code the same parameter
4. **Implementation Planning** - Helps determine which mappings provide the most value
5. **Quality Metrics** - Baseline for measuring adoption of standardized lab coding

### Key Insights

- Top 3 parameters (Creatinine, Leukocytes, Hematocrit) are used by all 5 reference labs
- Multiple LOINC codes exist for the same clinical concept due to:
  - Different units (mg/dL vs umol/L)
  - Different methods (automated vs. manual)
  - Different sample sources (serum vs. plasma vs. arterial blood)
- Dataset from 2018 represents historical usage patterns that may inform current standardization

---

## 3. top300loinc (2).json

**File Path:** `input/top300loinc (2).json`

### Overview

A JSON file containing hierarchical relationships between LOINC codes, showing parent-child relationships within the LOINC taxonomy.

### File Structure

```json
[
  {
    "loinc": "10329-1",
    "parents": ["10330-9", "26487-9", "26486-1"]
  },
  ...
]
```

### Data Statistics

- **Total Entries:** 829 LOINC codes
- **Entries with Parents:** 545 (66%)
- **Entries without Parents:** 284 (34%)
- **Maximum Parents per Entry:** 9
- **Data Format:** JSON array of objects

### Structure

Each entry contains:

1. **loinc** (string) - The LOINC code identifier
   - Format: Standard LOINC code (e.g., "10329-1")
   - Data completeness: 100%

2. **parents** (array of strings) - List of parent LOINC codes
   - Can be empty array `[]` for root concepts
   - Can contain multiple parents (multi-parent hierarchy)
   - Average: ~2-3 parents per entry with parents
   - Maximum: 9 parents

### Hierarchy Characteristics

- **Multi-parent taxonomy:** Single LOINC can have multiple parent codes
- **Orphan concepts:** 284 entries (34%) have no parents (either root concepts or isolated codes)
- **Well-connected concepts:** Some entries have up to 9 parent relationships

### Example Entries

```json
{
  "loinc": "10329-1",
  "parents": ["10330-9", "26487-9", "26486-1"]
}

{
  "loinc": "10501-5",
  "parents": []
}

{
  "loinc": "10835-7",
  "parents": ["2576-7", "2885-2", "107377-4", "32337-8"]
}
```

### Primary Use Cases

1. **Hierarchy Navigation** - Understanding LOINC taxonomic relationships
2. **Code Expansion** - Finding all related/parent concepts for a given LOINC
3. **Subsumption Queries** - Determining if one LOINC is more general/specific than another
4. **Mapping Validation** - Verifying semantic relationships between lab parameters
5. **Search Enhancement** - Expanding searches to include parent/related concepts

### Key Insights

- 66% of codes have hierarchical relationships (not isolated)
- Complex multi-parent structure reflects overlapping clinical concepts
- 284 orphan codes may represent:
  - Root concepts in the hierarchy
  - Isolated/deprecated codes not linked to taxonomy
  - Codes pending hierarchy integration
- Some concepts are highly connected (9 parents) indicating rich semantic relationships

### Relationship to Other Files

- **Direct relationship with Top300 Stand 2018-08-08.xlsx:** Contains 95.4% of the same LOINC codes (791 out of 829 match)
  - JSON codes correspond to the "sekundär" column in the Excel file
  - The Excel file provides rich metadata (names, units, German translations, rankings)
  - The JSON file adds hierarchical parent-child relationships to those same codes
  - 38 codes in JSON not in Excel (possibly deprecated or added later)
  - 133 codes in Excel not in JSON (possibly lack hierarchy information or were filtered out)
  - **These files represent the same dataset in different formats for different purposes**
- May be used with `LOINC_Mapping_Interpolar_v3.6` to expand LOINC_PRIMARY groups via hierarchy
- Enables semantic queries beyond exact code matching

---

## Summary

These three files work together to support laboratory data standardization and clinical decision support:

1. **LOINC_Mapping_Interpolar_v3.6** - The core mapping table for INTERPOLAR algorithms
2. **Top300 Stand 2018-08-08** - Prioritization data showing which lab codes matter most (with full metadata)
3. **top300loinc (2).json** - Hierarchical relationships for the same Top300 codes

### File Relationships

- **Top300 Excel + JSON are complementary:** They contain essentially the same 829 LOINC codes (95.4% overlap)
  - Excel = rich metadata (names, units, rankings, German translations)
  - JSON = hierarchical taxonomy (parent-child relationships)
  - Together they provide both "what" (metadata) and "how codes relate" (hierarchy)

- **LOINC_Mapping_Interpolar builds on Top300:**
  - 38.6% of Interpolar LOINC codes (241/625) appear in Top300
  - **95.7% of Interpolar LOINC_PRIMARY codes (45/47) appear in Top300** - showing Interpolar's primary reference codes are drawn from the most commonly used lab parameters
  - 31.4% of Interpolar LOINC codes (196/625) appear in the JSON hierarchy
  - The MII_TOP_300 flag in Interpolar identifies which codes are in the Top300 list

### Common Themes

- All files focus on laboratory parameter standardization using LOINC
- German healthcare context (MII = Medizininformatik-Initiative)
- Support for multiple LOINC variants representing the same clinical concept
- Emphasis on comparability and interoperability across institutions
- Foundation for clinical decision support systems (especially INTERPOLAR)

### Data Completeness Notes

- LOINC_Mapping_Interpolar has the most curated dataset for clinical algorithms (625 entries)
- Top300 Excel has the largest raw dataset (935 entries across 300 ranked parameters)
- JSON hierarchy file (829 entries) is a filtered subset of Top300 with added taxonomy
