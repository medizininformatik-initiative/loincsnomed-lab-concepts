# ECL Query Methodology for LOINC-SNOMED Mapping

## Overview

This document describes the methodology used for generating and evaluating Expression Constraint Language (ECL) queries to retrieve LOINC codes through SNOMED CT observable entities in the LOINCSNOMED Edition.

## Background

### The Mapping Challenge

LOINC (Logical Observation Identifiers Names and Codes) and SNOMED CT serve different purposes in healthcare:
- **LOINC**: Primarily focused on laboratory and clinical observations
- **SNOMED CT**: Comprehensive clinical terminology covering diagnoses, procedures, and observations

The LOINCSNOMED Edition provides explicit mappings between LOINC codes and SNOMED CT concepts, but finding all relevant LOINC codes for a given clinical concept requires sophisticated querying strategies.

### Post-coordinated vs Pre-coordinated Concepts

SNOMED CT distinguishes between:

**Post-coordinated concepts**: Constructed at query time by combining attributes
- Example: "Hemoglobin [Mass/volume] in Blood"
- Built from: Component (Hemoglobin) + Property (Mass concentration) + Direct site (Blood)
- Most laboratory observations use this pattern

**Pre-coordinated concepts**: Single existing concepts
- Example: "Mean corpuscular volume"
- Already defined in SNOMED as a single concept ID
- Most calculated laboratory indices use this pattern

## ECL Query Approaches

### Approach 1: ECL Descendants Baseline

**Purpose**: Establish baseline by finding all descendants of a component concept.

**Pattern**:
```ecl
<< ComponentID
```

**Example** (Hemoglobin):
```ecl
<< 38082009 |Hemoglobin|
```

**Characteristics**:
- Simplest approach
- Often retrieves many non-observable concepts
- Usually returns 0 LOINC codes (because raw substance concepts aren't mapped)
- Useful for understanding the concept hierarchy

**When to use**: Understanding the SNOMED hierarchy, not for production value sets.

---

### Approach 2: ECL Fixed Component

**Purpose**: Find observable entities with a specific component.

**Pattern**:
```ecl
<< 363787002 |Observable entity| :
   246093002 |Component| = ComponentID
```

**Example** (Hemoglobin):
```ecl
<< 363787002 |Observable entity| :
   246093002 |Component| = 38082009 |Hemoglobin|
```

**Characteristics**:
- Returns observable entities only
- Component must be exactly the specified concept (no descendants)
- Typically retrieves 50-60 LOINC codes for major CBC components
- Includes various properties and specimens

**When to use**: When you want all observations of a specific substance, regardless of measurement type or specimen.

**Results for Hemoglobin**: 60 LOINC codes

---

### Approach 3: ECL Component Descendants

**Purpose**: Find observable entities where component is the concept OR any descendant.

**Pattern**:
```ecl
<< 363787002 |Observable entity| :
   246093002 |Component| = << ComponentID
```

**Example** (Hemoglobin):
```ecl
<< 363787002 |Observable entity| :
   246093002 |Component| = << 38082009 |Hemoglobin|
```

**Characteristics**:
- Broadest coverage of related concepts
- Includes specialized hemoglobin variants (HbA1c, HbF, HbS, etc.)
- Typically retrieves 200+ LOINC codes for major components
- May include clinically unrelated concepts

**When to use**: Exploratory analysis, understanding the full landscape of related tests.

**Results for Hemoglobin**: 267 LOINC codes (includes HbA1c, fetal hemoglobin, etc.)

---

### Approach 4: ECL Fixed Component + Property

**Purpose**: Narrow results to a specific type of measurement (e.g., concentration vs ratio).

**Pattern**:
```ecl
<< 363787002 |Observable entity| :
   246093002 |Component| = ComponentID,
   370130000 |Property| = PropertyID
```

**Example** (Hemoglobin with Mass concentration):
```ecl
<< 363787002 |Observable entity| :
   246093002 |Component| = 38082009 |Hemoglobin|,
   370130000 |Property| = 118556004 |Mass concentration|
```

**Characteristics**:
- More specific than fixed component alone
- Filters by measurement type
- Typically retrieves 5-20 LOINC codes
- Still includes various specimens

**Common Properties**:
- `118556004` - Mass concentration (per volume)
- `119362007` - Number concentration (per volume)
- `118555003` - Substance concentration
- `119366009` - Time concentration
- `118586006` - Arbitrary concentration

**When to use**: When clinical context requires specific measurement types.

**Results for Hemoglobin**: 5 LOINC codes

---

### Approach 5: ECL Fixed Component + System

**Purpose**: Narrow results to specific specimen types (e.g., blood vs urine).

**Pattern**:
```ecl
<< 363787002 |Observable entity| :
   246093002 |Component| = ComponentID,
   704327008 |Direct site| = << SystemID
```

**Example** (Hemoglobin in Blood):
```ecl
<< 363787002 |Observable entity| :
   246093002 |Component| = 38082009 |Hemoglobin|,
   704327008 |Direct site| = << 119297000 |Blood specimen|
```

**Characteristics**:
- Filters by specimen/system
- Uses descendants (`<<`) for system to include variants (venous blood, capillary blood, etc.)
- Typically retrieves 30-40 LOINC codes
- Still includes various measurement properties

**Common Specimen Types**:
- `119297000` - Blood specimen (and descendants)
- `122575003` - Urine specimen
- `119361006` - Plasma specimen
- `119364003` - Serum specimen
- `258580003` - Whole blood specimen

**When to use**: When specimen type is clinically critical (e.g., excluding plasma platelets).

**Results for Hemoglobin**: 33 LOINC codes

---

### Approach 6: Refined Query (Component + Property + System)

**Purpose**: Most specific technical definition combining all three attributes.

**Pattern**:
```ecl
<< 363787002 |Observable entity| :
   246093002 |Component| = ComponentID,
   370130000 |Property| = << PropertyID,
   704327008 |Direct site| = << SystemID
```

**Example** (Hemoglobin - Mass concentration in Blood):
```ecl
<< 363787002 |Observable entity| :
   246093002 |Component| = 38082009 |Hemoglobin|,
   370130000 |Property| = << 118556004 |Mass concentration|,
   704327008 |Direct site| = << 119297000 |Blood specimen|
```

**Characteristics**:
- Most restrictive and specific
- Typically retrieves 5-10 LOINC codes
- Represents the "core" clinical concept
- Uses descendants (`<<`) for Property and System to allow related concepts
- Marked as "Refined Query" in analysis output

**When to use**:
- Creating focused value sets for specific clinical use cases
- When precision is more important than recall
- As a starting point for manual refinement

**Results for Hemoglobin**: 5 LOINC codes

**Note**: This is a **technical designation**, not a clinical quality judgment. It flags the most specific query, but clinical review is still required.

---

### Approach 7: Pre-coordinated Descendants

**Purpose**: For concepts that exist as single SNOMED concepts (primarily calculated indices).

**Pattern**:
```ecl
<< PrecoordinatedConceptID
```

**Example** (Mean Corpuscular Volume):
```ecl
<< 250170007 |Mean corpuscular volume|
```

**Characteristics**:
- Used for calculated laboratory indices
- Single concept search, not post-coordinated
- Typically retrieves 1-3 LOINC codes
- Very precise for established calculations

**Common Pre-coordinated Concepts**:
- `250170007` - Mean corpuscular volume (MCV)
- `28539005` - Mean corpuscular hemoglobin (MCH)
- `28540003` - Mean corpuscular hemoglobin concentration (MCHC)

**When to use**: When the concept is a well-defined calculation or ratio that exists as a SNOMED concept.

**Results**:
- MCV: 2 LOINC codes
- MCH: 264 LOINC codes (has more variants)
- MCHC: 2 LOINC codes

---

## Analytical Value of Multiple Experiments

### Why Run All These Approaches?

The primary value of running multiple ECL experiments is **comparative analysis** - understanding how different constraint choices affect result sets reveals important information about the SNOMED CT concept structure and helps identify refinement opportunities.

### Key Insight: Fixed vs Descendants Comparison

**Comparing Approach 2 (Fixed Component) with Approach 3 (Component Descendants) reveals the existence and nature of subcomponents:**

#### What the Difference Tells Us

When Approach 3 returns **more codes** than Approach 2, it indicates that **subcomponents exist** in the SNOMED CT hierarchy beneath the target component.

**Example - Hemoglobin:**
- **Fixed Component** (Approach 2): 60 LOINC codes
  - Generic hemoglobin measurements
  - Component = exactly `38082009 |Hemoglobin|`

- **Component Descendants** (Approach 3): 267 LOINC codes
  - **Additional 207 codes** from subcomponents:
    - Hemoglobin A1c (HbA1c) - diabetes monitoring
    - Hemoglobin F (Fetal hemoglobin) - neonatal care
    - Hemoglobin S (Sickle cell) - genetic disorders
    - Methemoglobin - toxicology
    - Carboxyhemoglobin - carbon monoxide poisoning

#### Clinical Decision Point

This comparison forces an important **clinical and use-case decision**:

**Option A: Include Subcomponents (Broad Approach)**
- **When**: Creating a comprehensive hemoglobin dashboard
- **Rationale**: Clinicians may want to see all hemoglobin-related values
- **Trade-off**: May include highly specialized tests irrelevant to most contexts
- **Implementation**: Use Approach 3 (Component Descendants)

**Option B: Exclude Subcomponents (Focused Approach)**
- **When**: Creating a value set for "total hemoglobin" in anemia screening
- **Rationale**: HbA1c and fetal hemoglobin are different clinical concepts
- **Trade-off**: May miss clinically relevant variants
- **Implementation**: Use Approach 2 (Fixed Component) or add explicit exclusions

**Option C: Selectively Include Subcomponents (Hybrid Approach)**
- **When**: Complex clinical workflow with multiple decision branches
- **Rationale**: Some subcomponents are relevant, others are not
- **Trade-off**: Requires manual review and explicit inclusion/exclusion rules
- **Implementation**: Start with Approach 2, manually add specific subcomponents

### Comparing Other Experiments

**Approaches 4-5 (Adding Property and System constraints):**
- Show how additional attributes **narrow** the result set
- Reveal **attribute interdependencies** (some combinations yield empty sets)
- Help identify **clinically meaningful groupings** (e.g., "mass concentration in blood")

**Approaches 6-7 (Refined queries with universal Measurement property):**
- Use `685451010000100 |Measurement property (qualifier value)|` instead of specific property
- Captures **all quantitative measurement types** (mass concentration, molar concentration, etc.)
- **Critical for real-world use**: Handles the fact that laboratories may report the same analyte in different units
- Represents the **production-ready query** that accounts for measurement variation

### Practical Workflow

1. **Run all experiments** to understand the concept landscape
2. **Compare Approach 2 vs 3** to identify subcomponents
3. **Review subcomponents** with clinical experts
4. **Decide inclusion/exclusion strategy** based on use case
5. **Examine refined query results** (Approaches 6-7) for final validation
6. **Document decisions** for reproducibility and maintenance

### Documentation Value

By **saving all experiment results**, we create an audit trail showing:
- What options were considered
- Why certain choices were made
- What trade-offs exist
- How to adjust for different clinical contexts

This is especially valuable when:
- Requirements change over time
- New LOINC codes are added
- Different sites have different needs
- Explaining value set composition to stakeholders

---

## Attribute Extraction Process

The analyzer automatically extracts SNOMED attributes for a given LOINC code:

### Step 1: Get SNOMED Concept ID
- Look up LOINC code in `sct2_Identifier_Full` file
- Extract SNOMED CT concept ID from LOINCSNOMED Edition

### Step 2: Fetch Concept Relationships
- Use OntoServer `$lookup` operation
- Extract properties from relationship groups:
  - `246093002` (Component)
  - `370130000` (Property)
  - `704327008` (Direct site)
  - `370132008` (Scale type)
  - `370134009` (Time aspect)
  - `424361007` (Using substance)
  - `424244007` (Using device)

### Step 3: Build ECL Expressions
- Automatically construct all relevant query variants
- Include FSN (Fully Specified Name) labels for readability
- Handle both post-coordinated and pre-coordinated patterns

### Step 4: Execute and Compare
- Run all queries against OntoServer
- Compare results against Interpolar and LOINC300 reference sets
- Generate comparison tables and visualizations

---

## Evaluation Metrics

### Coverage Metrics

**Per Query Approach**:
- Total LOINC codes retrieved
- Total SNOMED concepts matched
- Overlap with Interpolar reference set
- Overlap with LOINC300 reference set

**Per LOINC Code**:
- How many approaches captured this code?
- Is it captured by the refined query?
- Is it in Interpolar or LOINC300?

### Not Used: Precision/Recall

**Important**: This analysis does NOT use precision/recall metrics with Interpolar as ground truth because:
- Interpolar represents empirical usage data, not a validated mapping gold standard
- Different ECL approaches serve different clinical purposes (broad vs narrow)
- No single "correct" answer exists for how many LOINC codes should be in a value set

Instead, we provide:
- **Descriptive statistics**: How many codes each approach retrieves
- **Reference set membership**: Whether codes appear in known reference sets
- **Technical designation**: Refined query flag for most specific representation

---

## Decision Guide: Which Approach to Use?

| Use Case | Recommended Approach | Rationale |
|----------|---------------------|-----------|
| Clinical decision support (broad) | Component Descendants | Maximum sensitivity, captures variants |
| Clinical decision support (focused) | Refined Query | Balanced specificity and sensitivity |
| Quality measures | Fixed Component + Property | Ensures consistent measurement type |
| Reference data analysis | Fixed Component | Explores full landscape of related tests |
| Calculated indices | Pre-coordinated Descendants | Matches how SNOMED models these concepts |
| Research/exploratory | All approaches | Compare coverage and overlap |

### Considerations:

**Clinical Context Matters**:
- Hemoglobin for anemia screening: May want all blood hemoglobin measurements
- Hemoglobin for diabetes: May want only HbA1c (not covered by base hemoglobin query)

**Local Implementation**:
- What LOINC codes are actually used in your system?
- What level of granularity do clinicians expect?
- Are there specific exclusions needed (e.g., exclude cord blood)?

**Validation Required**:
- Always review generated value sets with domain experts
- Check for unexpected inclusions/exclusions
- Iterate based on clinical feedback

---

## Known Limitations

### 1. Interpolar is Not Ground Truth
- Represents empirical usage, not validation
- May include rarely used codes
- May miss emerging codes
- Geographical and temporal bias

### 2. LOINCSNOMED Edition Mapping Completeness
- Not all LOINC codes have SNOMED mappings
- Some mappings may be imprecise
- Mapping quality varies by concept area

### 3. Query Complexity
- More attributes = more specific but may miss valid variants
- Fewer attributes = broader but may include unrelated concepts
- No perfect query exists for all use cases

### 4. Calculated Indices Behavior
- Pre-coordinated concepts behave differently
- May not follow same attribute patterns
- Requires separate handling logic

### 5. Exclusions Needed
- Some concepts require explicit exclusions (e.g., plasma platelets)
- Cannot always be captured by positive ECL constraints alone
- May require post-processing or manual curation

---

## Best Practices

### 1. Start with Refined Query
- Most clinically focused representation
- Good balance of specificity and coverage
- Review and adjust based on results

### 2. Compare Multiple Approaches
- Run all approaches to understand landscape
- Identify gaps and overlaps
- Make informed decisions about inclusions

### 3. Validate Against Reference Sets
- Check overlap with Interpolar (empirical usage)
- Check overlap with LOINC300 (common tests)
- Investigate significant differences

### 4. Review Unexpected Results
- Why did a code appear in one approach but not another?
- Are there missing attributes or unexpected descendants?
- Document decisions for future reference

### 5. Iterate with Clinical Input
- Share generated value sets with domain experts
- Incorporate clinical context and local needs
- Update queries based on feedback

### 6. Document Methodology
- Record which approach(es) used
- Explain rationale for inclusions/exclusions
- Version control your value sets

---

## Technical Implementation Details

### MII OntoServer API Usage

**$expand Operation** (for ECL queries):
```http
GET /fhir/ValueSet/$expand?url=http://snomed.info/sct/11000274103/version/20250921?fhir_vs=ecl/EXPRESSION
```

**$lookup Operation** (for concept details):
```http
GET /fhir/CodeSystem/$lookup?system=http://snomed.info/sct/11000274103&version=http://snomed.info/sct/11000274103/version/20250921&code=CONCEPTID
```

**Important**: The `fhir_vs` parameter must be embedded inside the `url` parameter, not passed separately.

### Authentication
- PKCS12 certificate (.p12 format)
- Handled by Python `requests` library with cert parameter
- Password may be empty string, None, or actual password

### Rate Limiting
- Respect server capacity
- Implement delays between requests if needed
- Cache results when appropriate

---

## Future Directions

### Potential Enhancements

1. **Machine Learning Validation**
   - Train models to predict appropriate value set membership
   - Learn from clinical validation feedback
   - Identify patterns in expert decisions

2. **Temporal Analysis**
   - Track changes in query results over LOINCSNOMED editions
   - Identify emerging LOINC codes
   - Monitor mapping completeness improvements

3. **Cross-terminology Validation**
   - Compare with other mapping sources
   - Integrate with local implementation usage data
   - Validate against published value sets

4. **Automated Exclusion Detection**
   - Identify concepts that should be explicitly excluded
   - Learn exclusion patterns from manual curation
   - Suggest refinement constraints

5. **Interactive Value Set Builder**
   - Web interface for exploring query results
   - Visual representation of attribute combinations
   - Real-time preview of LOINC code membership

---

## References

1. SNOMED International. (2024). *Expression Constraint Language - Specification and Guide*. https://confluence.ihtsdotools.org/display/DOCECL/

2. SNOMED International. (2024). *LOINC to SNOMED CT Mapping Guide*. https://confluence.ihtsdotools.org/display/DOCLOINC/

3. Regenstrief Institute. *LOINC Users' Guide*. https://loinc.org/

4. Medical Informatics Initiative (MII). *Interpolar Project*. https://www.medizininformatik-initiative.de/

---

## Version History

- v1.0 (2025-01-13): Initial methodology documentation
- v1.1 (2025-01-13): Added refined query technical designation, clarified Interpolar status
- v1.2 (2025-01-13): Added section on analytical value of multiple experiments, documented universal Measurement property usage in refined queries

---

## Contact

For questions about this methodology or to report issues, please contact the MII laboratory data harmonization team.
thomas.debertshaeuser@charite.de
martin.federbusch@medizin.uni-leipzig.de