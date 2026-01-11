# Hierarchical ValueSet Clustering for Laboratory Concepts

## Core Concept

Laboratory LOINC codes form natural **hierarchical clusters** based on clinical specificity:

```
Focused (5-10 codes)
    ↓ subset of
Moderate (30-60 codes)
    ↓ subset of
Comprehensive (200+ codes)
```

**Key principle:** Focused ⊂ Moderate ⊂ Comprehensive

Each level serves a different clinical use case with different precision/recall requirements.

---

## The Three Levels

### Level 1: Focused (Clinical Decision Support)

**Purpose:** Automated alerts, quality measures, clinical rules

**Characteristics:**
- **High precision** (few false positives)
- **Standard tests only** (common assays, routine specimen types)
- **Well-defined clinical semantics** (one specific measurement)

**Size:** Typically 5-10 LOINC codes per lab parameter

**ECL Strategy:** Most restrictive (Component + Property + System fixed)

**Example - Hemoglobin for Anemia Screening:**
```
5 codes:
- 718-7   Hemoglobin [Mass/volume] in Blood
- 59260-0 Hemoglobin [Mass/volume] in Blood by Oximetry
- 20509-6 Hemoglobin [Mass/volume] in Blood by calculation
- 30350-3 Hemoglobin [Mass/volume] in Venous blood
- 30351-1 Hemoglobin [Mass/volume] in Arterial blood

Rationale: These are the standard CBC hemoglobin tests.
Does NOT include: HbA1c, carboxyhemoglobin, methemoglobin (different analytes)
```

**Clinical Rule Example:**
```
IF hemoglobin < 7 g/dL
   AND patient not on transfusion protocol
THEN alert: "Consider transfusion - hemoglobin critically low"
```

**Why focused?** Alert should only fire on CBC hemoglobin, not HbA1c or variant hemoglobins.

---

### Level 2: Moderate (EHR Data Extraction)

**Purpose:** Data warehouse queries, quality reporting, cohort identification

**Characteristics:**
- **Balanced precision/recall** (capture common variations)
- **Multiple measurement methods** (HPLC, immunoassay, calculated)
- **Routine specimen types** (blood, serum, plasma, arterial blood)

**Size:** Typically 30-60 LOINC codes per lab parameter

**ECL Strategy:** Moderate restriction (Component fixed, Property/System descendants)

**Example - Hemoglobin for Quality Reporting:**
```
50 codes including:
- All from Focused level (5 codes)
- Plus variant methods:
  - Hemoglobin by HPLC
  - Hemoglobin by electrophoresis
  - Hemoglobin by CO-oximetry
- Plus specimen variations:
  - Capillary blood
  - Cord blood
  - Mixed venous blood

Rationale: Capture all common clinical methods and specimen types.
Does NOT include: Research assays, exotic specimens, hemoglobin variants
```

**Query Example:**
```sql
-- Find all patients with any hemoglobin test in last year
SELECT patient_id, observation_date, value
FROM lab_results
WHERE loinc_code IN (<moderate_valueset>)
  AND observation_date > NOW() - INTERVAL '1 year'
```

**Why moderate?** Balance capturing real-world variation without noise from exotic tests.

---

### Level 3: Comprehensive (Research & Phenotyping)

**Purpose:** Research cohorts, comprehensive phenotyping, hypothesis generation

**Characteristics:**
- **High recall** (capture everything possibly related)
- **All variants and subtypes** (HbA1c, HbF, HbS, carboxyhemoglobin, etc.)
- **All specimen types** (including research and exotic)

**Size:** Typically 200+ LOINC codes per lab parameter

**ECL Strategy:** Minimal restriction (Component descendants)

**Example - Hemoglobin for Research:**
```
267 codes including:
- All from Moderate level (50 codes)
- Plus hemoglobin variants:
  - HbA1c (glycosylated hemoglobin)
  - HbF (fetal hemoglobin)
  - HbS (sickle cell)
  - Carboxyhemoglobin
  - Methemoglobin
- Plus calculated indices:
  - Mean corpuscular hemoglobin (MCH)
  - MCH concentration (MCHC)
- Plus exotic specimens:
  - Tissue
  - Ascites fluid
  - CSF

Rationale: Comprehensive coverage for research queries where false negatives are worse than false positives.
```

**Research Query Example:**
```python
# Phenotype all patients with ANY hemoglobin-related abnormality
cohort = patients.filter(
    lab_observations.loinc_code.isin(comprehensive_hemoglobin_valueset)
    & lab_observations.abnormal_flag.isin(['L', 'H', 'A'])
)
```

**Why comprehensive?** Research needs maximum recall - better to include extra codes and manually review than miss relevant cases.

---

## Hierarchical Relationships

### Subset Property

```
Focused ⊂ Moderate ⊂ Comprehensive

Example - Hemoglobin:
Focused:      5 codes (100%)
Moderate:    50 codes (includes all 5 from Focused + 45 more)
Comprehensive: 267 codes (includes all 50 from Moderate + 217 more)
```

### Visual Hierarchy

```
┌─────────────────────────────────────────────────┐
│ Comprehensive (Research)                        │
│ All hemoglobin-related tests (267 codes)       │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │ Moderate (EHR Data Extraction)            │ │
│  │ Common methods & specimens (50 codes)     │ │
│  │                                           │ │
│  │  ┌─────────────────────────────────────┐ │ │
│  │  │ Focused (CDS Alerts)                │ │ │
│  │  │ Standard CBC hemoglobin (5 codes)   │ │ │
│  │  └─────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

---

## Selection Criteria by Level

### Focused Level Inclusion Criteria

✅ **Include:**
- Primary measurement for the analyte
- Most common specimen type (typically blood, serum, or plasma)
- Standard measurement property (mass concentration, molar concentration)
- WHO-approved reference methods when available

❌ **Exclude:**
- Calculated values (unless that's the only form)
- Variant analytes (e.g., HbA1c when defining hemoglobin)
- Exotic specimen types (CSF, ascites, tissue)
- Research-only assays
- Deprecated codes

### Moderate Level Inclusion Criteria

✅ **Include:**
- All from Focused level
- Alternative measurement methods (HPLC, immunoassay, electrophoresis)
- Common specimen variations (arterial, venous, capillary blood)
- Point-of-care testing methods
- Calculated values when clinically relevant

❌ **Exclude:**
- Variant analytes (still excluded - e.g., no HbA1c in hemoglobin)
- Very exotic specimen types
- Purely research assays

### Comprehensive Level Inclusion Criteria

✅ **Include:**
- All from Moderate level
- All variant analytes and subtypes
- All specimen types (including exotic)
- All measurement methods (including research)
- Calculated indices using the analyte
- Historical/deprecated codes (for retrospective research)

❌ **Exclude:**
- Only completely unrelated concepts

---

## Clinical Examples with Rationale

### Example 1: Creatinine (Kidney Function)

**Clinical Context:** Monitoring renal function, drug dosing adjustments

| Level | Size | Included | Rationale |
|-------|------|----------|-----------|
| **Focused** | 8 codes | Serum/plasma creatinine mass concentration only | CDS rules for GFR calculation, drug monitoring need standardized serum creatinine |
| **Moderate** | 45 codes | + Urine creatinine, creatinine clearance, different methods | Quality reporting on renal function includes clearance tests |
| **Comprehensive** | 180 codes | + Exotic specimens, ratios, research assays | Research on kidney disease needs all creatinine-related measurements |

**Use Case Examples:**
- **CDS Alert:** "Patient on metformin, last serum creatinine >30 days ago" → Use Focused (serum only)
- **Quality Measure:** "% of CKD patients with annual renal function testing" → Use Moderate (includes clearance)
- **Research Cohort:** "All patients with any creatinine abnormality" → Use Comprehensive (all types)

### Example 2: Glucose (Diabetes Management)

**Clinical Context:** Diabetes screening, diagnosis, monitoring

| Level | Size | Included | Rationale |
|-------|------|----------|-----------|
| **Focused** | 12 codes | Fasting glucose, random glucose in blood/serum/plasma | Diabetes screening rules need standard glucose only |
| **Moderate** | 65 codes | + Post-prandial, 2-hour OGTT, different methods | Quality metrics include glucose tolerance testing |
| **Comprehensive** | 340 codes | + Urine glucose, CSF glucose, continuous monitoring | Research includes all glucose measurements across all body fluids |

**Use Case Examples:**
- **CDS Alert:** "Fasting glucose >126 mg/dL on two occasions → Diabetes diagnosis" → Use Focused
- **Quality Measure:** "% of diabetics with HbA1c AND glucose testing" → Use Moderate (includes OGTT)
- **Research:** "Hypoglycemia phenotyping across all sources" → Use Comprehensive (includes CGM, urine)

### Example 3: PSA (Prostate Cancer Screening)

**Clinical Context:** Prostate cancer screening and monitoring

| Level | Size | Included | Rationale |
|-------|------|----------|-----------|
| **Focused** | 3 codes | Total PSA in serum/plasma | Screening guidelines use total PSA only |
| **Moderate** | 8 codes | + Free PSA, PSA ratios, different methods | Workup includes free/total PSA ratio |
| **Comprehensive** | 25 codes | + PSA velocity, PSA density, exotic calculations | Research on PSA kinetics and derived measures |

**Use Case Examples:**
- **CDS Alert:** "Male >50yo, no PSA in 2 years → Screening reminder" → Use Focused (total PSA)
- **Diagnostic Workup:** "Elevated PSA → Check free/total ratio" → Use Moderate (includes ratios)
- **Research:** "PSA velocity as predictor of cancer progression" → Use Comprehensive (includes kinetics)

---

## Precision vs Recall Tradeoffs

### Clinical Decision Support (Focused)

**Goal:** High Precision (minimize false positives)

**Rationale:** Alert fatigue is a patient safety risk

```
Scenario: Alert for abnormal hemoglobin

Comprehensive ValueSet (267 codes):
- True Positives:  100 alerts (correct)
- False Positives: 60 alerts (HbA1c, carboxyhemoglobin trigger incorrectly)
- Precision: 100/(100+60) = 62.5%
- Result: Clinicians ignore alerts → Safety risk

Focused ValueSet (5 codes):
- True Positives:  95 alerts (correct)
- False Positives: 2 alerts (edge cases)
- Precision: 95/(95+2) = 97.9%
- Result: Clinicians trust alerts → Better outcomes
```

**Accept some false negatives** (missed 5 alerts) to avoid alert fatigue.

### Research Phenotyping (Comprehensive)

**Goal:** High Recall (minimize false negatives)

**Rationale:** Missing cases biases research results

```
Scenario: Identify all patients with hemoglobin abnormalities

Focused ValueSet (5 codes):
- True Positives: 1,000 patients identified
- False Negatives: 300 patients missed (had HbA1c, methemoglobin issues)
- Recall: 1,000/(1,000+300) = 76.9%
- Result: Biased cohort, incomplete phenotyping

Comprehensive ValueSet (267 codes):
- True Positives: 1,280 patients identified
- False Negatives: 20 patients missed (exotic edge cases)
- Recall: 1,280/(1,280+20) = 98.5%
- Result: Complete cohort, manual review filters noise
```

**Accept some false positives** (extra codes to manually review) to avoid missing cases.

### EHR Data Extraction (Moderate)

**Goal:** Balanced Precision/Recall

**Rationale:** Capture real-world variation without excessive noise

```
Moderate ValueSet (50 codes):
- Captures 95% of routine clinical tests
- Excludes exotic/research assays
- Balanced for quality reporting and cohort studies
```

---

## Implementation Decision Framework

### Decision Tree for Use Case Selection

```
START: What is the primary use case?

├─ Automated clinical alerts/rules (CDS)?
│  └─ Use FOCUSED
│     Why: High precision needed, alert fatigue is safety risk
│
├─ Quality reporting, data warehouse queries?
│  └─ Use MODERATE
│     Why: Capture clinical variation, balance precision/recall
│
└─ Research cohorts, hypothesis generation?
   └─ Use COMPREHENSIVE
      Why: High recall needed, manual review filters noise
```

### Mixed Use Cases

**If you need multiple:**

Example: "Find all diabetics for quality reporting AND research"

**Approach:**
1. Use MODERATE for quality measure calculation (official metric)
2. Use COMPREHENSIVE for research cohort (exploratory analysis)
3. Document which ValueSet used for which purpose
4. Compare results between levels to understand sensitivity

---

## Validation Approach

### How We Validate Each Level

**Reference Sets:**
- **Interpolar:** Expert-curated LOINC mappings (empirical usage)
- **LOINC300:** 300 most common lab tests in German healthcare
- **MII Top 100:** Priority lab parameters for MII

**Validation Questions:**

**For Focused:**
1. Does it include ALL codes from Interpolar for this concept? (Should be ~100% overlap)
2. Does it exclude variant analytes? (e.g., no HbA1c in hemoglobin)
3. Is it useful for a specific CDS rule? (Test with real rule)

**For Moderate:**
1. Does it include ALL codes from LOINC300 for this concept? (High overlap expected)
2. Does it capture common method variations? (HPLC, immunoassay, etc.)
3. Is it useful for quality measure calculation? (Test with real measure)

**For Comprehensive:**
1. Does it include ALL related concepts via ECL descendants?
2. Are there any codes that should be EXCLUDED? (Completely unrelated only)
3. Is manual review feasible? (Not so large that review is impossible)

---

## For Medical Staff Reviewers

### What We Need You to Validate

**You do NOT need to review all codes in each ValueSet.**

**Instead, review the SELECTION RULES:**

1. **Focused Selection Rule:** "Include only standard measurement of primary analyte in blood/serum/plasma"
   - Does this make sense for CDS alerts?
   - Spot-check 3-5 examples: Does focused set look right?

2. **Moderate Selection Rule:** "Include common methods and specimen types, exclude variant analytes"
   - Does this make sense for quality reporting?
   - Spot-check 3-5 examples: Does moderate set look reasonable?

3. **Comprehensive Selection Rule:** "Include all related concepts via ECL descendants"
   - Does this make sense for research?
   - Spot-check 3-5 examples: Does comprehensive set capture everything?

**Your approval:** "The selection rules are clinically sound" (not "every code is correct")

---

## For MIO Working Group

### Alignment with MIO Profiles

**Recommendation:** MIO profiles should specify which level to use based on profile purpose.

**Example - MII Laboratory Observation Profile:**

```fhir
{
  "resourceType": "StructureDefinition",
  "url": "https://www.medizininformatik-initiative.de/fhir/core/modul-labor/StructureDefinition/ObservationLab",
  "binding": {
    "strength": "preferred",
    "valueSet": "https://loinclab.org/ValueSet/hemoglobin-moderate",
    "extension": {
      "url": "http://hl7.org/fhir/StructureDefinition/alternate-valueset",
      "valueCanonical": [
        "https://loinclab.org/ValueSet/hemoglobin-focused",    // For CDS use
        "https://loinclab.org/ValueSet/hemoglobin-comprehensive" // For research use
      ]
    }
  }
}
```

**Recommendation:**
- **Default:** Moderate (balanced for most MII use cases)
- **Alternative - Focused:** For CDS systems and quality measures
- **Alternative - Comprehensive:** For research data queries

---

## Population Aggregation vs Individual Precision

### The Two Dimensions

**Use cases differ on TWO axes:**

| Axis | Description | Impact on ValueSet Selection |
|------|-------------|------------------------------|
| **Individual vs Population** | Single patient decision vs aggregate analysis | Individual needs precision, population tolerates variation |
| **Precision vs Recall** | Minimize false positives vs minimize false negatives | Precision for alerts, recall for research |

### Use Case Matrix

```
                     INDIVIDUAL PATIENT              POPULATION AGGREGATE
                     ─────────────────               ──────────────────

PRECISION      │  CDS Alerts                   │  Quality Measures
(avoid false+) │  → FOCUSED ValueSet           │  → MODERATE ValueSet
               │  Example: Drug-lab alert      │  Example: % diabetics tested
               │  Need: Exact code match       │  Tolerates: Method variation
               │                              │
─────────────────────────────────────────────────────────────────────────
               │                              │
RECALL         │  Individual Phenotyping      │  Research Cohorts
(avoid false-) │  → MODERATE ValueSet          │  → COMPREHENSIVE ValueSet
               │  Example: Patient summary     │  Example: Hypothesis testing
               │  Need: Complete history       │  Tolerates: Manual review
```

### Why This Matters

**Individual Patient Decisions (CDS):**
- **Stakes:** One wrong alert → Patient harm or clinician distrust
- **Volume:** Thousands of alerts per day
- **Review:** No manual review possible (automated)
- **Requirement:** HIGH PRECISION (minimize false positives)

**Example:**
```
Alert: "Patient on warfarin, INR >5.0 → Bleeding risk"

Focused ValueSet (3 codes):
- INR in platelet poor plasma by coagulation assay
→ Fires only on actual INR measurements

If we used Moderate/Comprehensive:
- Would trigger on PT (related but not INR)
- Would trigger on exotic coagulation tests
- Result: Alert fatigue → Clinicians disable alert → Patient harm
```

**Population Aggregate Analysis (Quality Measures):**
- **Stakes:** One patient miscategorized → Minimal impact on aggregate metric
- **Volume:** Thousands of patients in denominator
- **Review:** Manual audit of sample possible
- **Requirement:** BALANCED (capture real-world variation)

**Example:**
```
Quality Measure: "% of diabetics with annual HbA1c testing"

Moderate ValueSet (15 codes):
- HbA1c by HPLC
- HbA1c by immunoassay
- HbA1c by electrophoresis
→ Captures all common methods used across sites

Why not Focused (5 codes)?
- Might miss some hospitals using different methods
- False negative in quality metric
- Underestimates true testing rate

Why not Comprehensive (100+ codes)?
- Would include HbA variants, research assays
- False positives dilute metric
- Overestimates testing rate
```

**Population Research Cohorts:**
- **Stakes:** Missing patients → Biased research findings
- **Volume:** Building cohort for analysis
- **Review:** Manual chart review typical
- **Requirement:** HIGH RECALL (minimize false negatives)

**Example:**
```
Research: "Identify all patients with anemia for outcomes study"

Comprehensive ValueSet (267 hemoglobin codes):
- All hemoglobin measurements (CBC, variants, calculated)
- All specimen types (blood, arterial, capillary)
→ Maximum sensitivity for cohort identification

Why Comprehensive?
- Research budget allows manual chart review (100-200 patients)
- False positives filtered during chart review
- False negatives (missed patients) can't be recovered
- Better to overinclude and manually filter
```

### Clinical Examples

**Example 1: Creatinine Monitoring**

| Scenario | Level | Rationale |
|----------|-------|-----------|
| **Drug dosing alert (individual)** | Focused | "Patient on lithium, creatinine >1.5 → Check level" - Need exact serum creatinine, can't tolerate false triggers |
| **CKD quality measure (population)** | Moderate | "% of CKD patients tested annually" - Capture method variation across sites, aggregate metric tolerates some variation |
| **AKI research cohort (population)** | Comprehensive | "Identify all AKI cases" - Include urine creatinine, clearance, all methods - manual review filters cohort |

**Example 2: Glucose**

| Scenario | Level | Rationale |
|----------|-------|-----------|
| **Diabetes diagnosis alert (individual)** | Focused | "Fasting glucose >126 on 2 occasions → Diabetes" - Must be fasting glucose specifically, not random/post-prandial |
| **Diabetes registry (population)** | Moderate | "% of diabetics meeting control targets" - Capture OGTT, post-prandial testing used in practice |
| **Hypoglycemia research (population)** | Comprehensive | "Hypoglycemia events across all contexts" - Include CGM, urine glucose, all sources for complete phenotype |

### The Precision-Population Trade-off

```
                 TIGHT (Focused)          MODERATE           BROAD (Comprehensive)
                       ↓                      ↓                      ↓
Individual        ████████              ██████░░              ████░░░░
Patient CDS       (Optimal)             (Too noisy)           (Unusable)

Population        ████░░░░              ████████              ██████░░
Quality           (Too narrow)          (Optimal)             (Too broad)

Population        ██░░░░░░              ██████░░              ████████
Research          (Miss cases)          (Some missing)        (Optimal)
```

**Key Insight:**
- **Individual decisions:** Errors compound (one alert × thousands of patients)
- **Population aggregates:** Errors average out (statistically robust)

### Validation by Context

**For Individual Patient Use (CDS):**

Test: "Can a clinician trust this alert without looking up the lab result?"

```
Alert: "Hemoglobin <7.0 g/dL"

Using Focused (5 codes):
✓ Clinician sees alert
✓ Looks at patient chart
✓ Confirms: CBC hemoglobin = 6.8 g/dL
✓ Takes action: Order transfusion
✓ Trust maintained

Using Comprehensive (267 codes):
✗ Clinician sees alert
✗ Looks at patient chart
✗ Finds: HbA1c = 6.9% (NOT the same as 6.9 g/dL!)
✗ Alert is false positive
✗ Trust destroyed → Clinician disables alert
```

**For Population Aggregate (Quality Measure):**

Test: "Does the metric accurately reflect testing rates?"

```
Measure: "% of diabetics with annual HbA1c"

Using Focused (5 codes):
- Denominator: 1,000 diabetics
- Numerator: 720 patients (missed 80 who had different method)
- Rate: 72% (UNDERESTIMATE - actually 80%)
- Conclusion: False low performance

Using Moderate (15 codes):
- Denominator: 1,000 diabetics
- Numerator: 795 patients (captures all common methods)
- Rate: 79.5% (ACCURATE)
- Conclusion: True performance

Using Comprehensive (100+ codes):
- Denominator: 1,000 diabetics
- Numerator: 845 patients (includes HbA2, HbF, research assays)
- Rate: 84.5% (OVERESTIMATE)
- Conclusion: False high performance
```

## Summary

**Key Principles:**

1. ✅ **Hierarchical clustering:** Focused ⊂ Moderate ⊂ Comprehensive
2. ✅ **Use-case driven:** CDS needs focused, research needs comprehensive
3. ✅ **Two dimensions:** Individual vs population AND precision vs recall
4. ✅ **Precision/recall tradeoff:** Explicit and documented
5. ✅ **Selection rules:** Reviewable, not individual codes
6. ✅ **Validation:** Against reference sets and clinical use cases

---

## The Units and Reference Range Problem

### Challenge: Same Test, Different Units

**Problem:** A single LOINC code can have results reported in multiple units, and different sites use different reference ranges.

**Example - Hemoglobin:**

```
LOINC 718-7: "Hemoglobin [Mass/volume] in Blood"

Hospital A reports:
- Value: 14.5
- Unit: g/dL
- Reference range: 13.5-17.5 (male), 12.0-15.5 (female)

Hospital B reports:
- Value: 145
- Unit: g/L
- Reference range: 135-175 (male), 120-155 (female)

Hospital C reports:
- Value: 9.0
- Unit: mmol/L
- Reference range: 8.4-10.9 (male), 7.4-9.6 (female)
```

**All three are THE SAME TEST reporting THE SAME RESULT (14.5 g/dL = 145 g/L = 9.0 mmol/L)**

### Impact on ValueSet Usage

**This creates THREE problems:**

#### Problem 1: CDS Alert Thresholds

**CDS Rule:** "Alert if hemoglobin < 7.0 g/dL (severe anemia)"

**Implementation Challenge:**
```
IF hemoglobin.loinc IN hemoglobin_focused_valueset
   AND hemoglobin.value < 7.0
THEN alert

❌ BROKEN: This fails if result reported in g/L (70) or mmol/L (4.3)
```

**Solution Needed:** Unit conversion or unit-specific thresholds

**Approaches:**

**Option A: Normalize to single unit**
```python
def normalize_hemoglobin(value, unit):
    if unit == "g/dL":
        return value
    elif unit == "g/L":
        return value / 10  # Convert to g/dL
    elif unit == "mmol/L":
        return value * 1.61  # Convert to g/dL using MW of hemoglobin
    else:
        raise UnitNotSupportedError(f"Unknown unit: {unit}")

normalized_value = normalize_hemoglobin(hemoglobin.value, hemoglobin.unit)
if normalized_value < 7.0:
    alert()
```

**Option B: Unit-specific thresholds**
```yaml
hemoglobin_severe_anemia_thresholds:
  "g/dL": 7.0
  "g/L": 70
  "mmol/L": 4.3

if hemoglobin.value < thresholds[hemoglobin.unit]:
    alert()
```

#### Problem 2: Reference Range Variation

**Challenge:** Reference ranges vary by demographics and local lab calibration

**Example - Creatinine:**

| Population | Reference Range (mg/dL) | Reference Range (µmol/L) |
|------------|-------------------------|--------------------------|
| **Adult Male** | 0.7-1.3 | 62-115 |
| **Adult Female** | 0.6-1.1 | 53-97 |
| **Child (1-12y)** | 0.3-0.7 | 27-62 |
| **Elderly (>65)** | 0.8-1.5 | 71-133 |

**CDS Rule:** "Alert if creatinine elevated"

**Which reference range to use?**
- Patient demographics (age, sex)?
- Lab-specific ranges (calibration differences)?
- Population-specific (ethnicity, pregnancy)?

#### Problem 3: LOINC Doesn't Always Specify Units

**Some LOINC codes are unit-agnostic:**

```
LOINC 2160-0: "Creatinine [Mass/volume] in Serum or Plasma"

Observation 1:
- Value: 1.2
- Unit: mg/dL
- Interpretation: Normal (assuming adult male)

Observation 2:
- Value: 106
- Unit: µmol/L
- Interpretation: Normal (same patient, same result, different unit)

Observation 3:
- Value: 1.2
- Unit: (missing!)
- Interpretation: UNKNOWN - cannot determine if normal
```

### Implications for Each Level

#### Focused ValueSets (CDS)

**Additional complexity:** Unit handling is CRITICAL

**Requirements:**
1. ✅ Document expected units for each LOINC code
2. ✅ Provide unit conversion functions
3. ✅ Provide demographic-adjusted reference ranges
4. ✅ Validation: Test CDS rules with multi-unit data

**Example - Hemoglobin Focused ValueSet Metadata:**
```yaml
hemoglobin_focused:
  loinc_codes:
    - code: 718-7
      display: "Hemoglobin [Mass/volume] in Blood"
      common_units:
        - "g/dL"    # USA, most common
        - "g/L"     # Europe, SI units
        - "mmol/L"  # Some European labs
      unit_conversions:
        g/dL_to_g/L: multiply_by_10
        g/dL_to_mmol/L: multiply_by_0.6206
      reference_ranges:
        adult_male_g/dL: {low: 13.5, high: 17.5}
        adult_female_g/dL: {low: 12.0, high: 15.5}
        adult_male_g/L: {low: 135, high: 175}
        adult_female_g/L: {low: 120, high: 155}

  cds_thresholds:
    severe_anemia:
      g/dL: 7.0
      g/L: 70
      mmol/L: 4.3
    mild_anemia_male:
      g/dL: 13.5
      g/L: 135
      mmol/L: 8.4
```

**Recommendation for CDS:** Include unit metadata WITH ValueSet, not separate

#### Moderate ValueSets (Quality Measures)

**Different challenge:** Aggregating across sites with different units

**Example - Quality Measure:**
```
"% of diabetics with HbA1c <7.0% (53 mmol/mol)"

Site A reports: 6.5% (NGSP units - USA)
Site B reports: 48 mmol/mol (IFCC units - Europe)
Site C reports: 0.065 (fraction - rare)

Need to normalize before calculating aggregate metric
```

**Requirements:**
1. ✅ Document unit prevalence by region
2. ✅ Provide normalization guidance
3. ✅ Flag when multi-unit data detected

#### Comprehensive ValueSets (Research)

**Challenge:** Maximum diversity of units and reference ranges

**Example - Research Cohort:**
```
"Identify all patients with abnormal hemoglobin"

- What defines "abnormal"?
  - < 2 SD from mean?
  - Below reference range (which one)?
  - Lab-flagged as abnormal?

- How to handle unit variation?
  - Normalize all to g/dL?
  - Keep original units (for validation)?
  - Flag missing units?
```

**Requirements:**
1. ✅ Preserve original units (for quality checking)
2. ✅ Provide normalization scripts
3. ✅ Document unit distribution in dataset

### Solutions & Recommendations

#### Recommendation 1: Publish Unit Metadata WITH ValueSets

**Don't just publish LOINC codes - publish USAGE metadata:**

```yaml
hemoglobin_focused_valueset:
  id: "hemoglobin-cds-focused"
  name: "Hemoglobin for Clinical Decision Support (Focused)"
  loinc_codes: [718-7, 59260-0, 20509-6, 30350-3, 30351-1]

  # NEW: Unit metadata
  unit_guidance:
    common_units: ["g/dL", "g/L", "mmol/L"]
    preferred_unit: "g/dL"  # For CDS implementation

    conversions:
      - from: "g/L"
        to: "g/dL"
        formula: "divide_by_10"
      - from: "mmol/L"
        to: "g/dL"
        formula: "multiply_by_1.61"

    reference_ranges:
      - population: "adult_male"
        unit: "g/dL"
        low: 13.5
        high: 17.5
      - population: "adult_female"
        unit: "g/dL"
        low: 12.0
        high: 15.5

    cds_thresholds:
      - name: "severe_anemia"
        values:
          "g/dL": 7.0
          "g/L": 70
          "mmol/L": 4.3
```

#### Recommendation 2: Validation Against Real-World Data

**Test ValueSets with multi-site data:**

```python
# Validation script
def validate_valueset_with_real_data(valueset, ehr_data):
    """
    Check if ValueSet handles real-world unit variation
    """
    # Find observations matching this ValueSet
    obs = ehr_data[ehr_data.loinc_code.isin(valueset.loinc_codes)]

    # Check unit distribution
    unit_counts = obs.groupby('unit').size()
    print(f"Unit distribution: {unit_counts}")

    # Flag if expected units missing from ValueSet metadata
    unexpected_units = set(unit_counts.index) - set(valueset.common_units)
    if unexpected_units:
        warn(f"Unexpected units found: {unexpected_units}")

    # Check if reference ranges cover observed data
    for pop in ['adult_male', 'adult_female']:
        pop_data = obs[obs.population == pop]
        ref_range = valueset.get_reference_range(pop, obs.unit.iloc[0])

        below_range = (pop_data.value < ref_range.low).sum()
        above_range = (pop_data.value > ref_range.high).sum()

        print(f"{pop}: {below_range} below, {above_range} above range")
```

#### Recommendation 3: UCUM Standardization

**Use UCUM (Unified Code for Units of Measure) codes:**

```yaml
hemoglobin:
  loinc: 718-7
  ucum_units:
    - code: "g/dL"
      ucum: "g/dL"
      common: true
    - code: "g/L"
      ucum: "g/L"
      common: true
    - code: "mmol/L"
      ucum: "mmol/L"
      common: true
    - code: "gm/dL"    # Non-standard variant
      ucum: "g/dL"     # Maps to standard
      common: false
```

**FHIR Observation already supports UCUM:**
```json
{
  "resourceType": "Observation",
  "code": {
    "coding": [{
      "system": "http://loinc.org",
      "code": "718-7"
    }]
  },
  "valueQuantity": {
    "value": 14.5,
    "unit": "g/dL",
    "system": "http://unitsofmeasure.org",
    "code": "g/dL"
  }
}
```

#### Recommendation 4: Decision Support Service API

**For CDS use cases, provide conversion service:**

```python
# API endpoint
POST /api/evaluate-threshold
{
  "loinc_code": "718-7",
  "value": 145,
  "unit": "g/L",
  "patient": {
    "sex": "male",
    "age": 45
  },
  "threshold_type": "severe_anemia"
}

Response:
{
  "normalized_value": 14.5,
  "normalized_unit": "g/dL",
  "threshold": 7.0,
  "threshold_unit": "g/dL",
  "threshold_exceeded": false,
  "reference_range": {
    "low": 13.5,
    "high": 17.5,
    "unit": "g/dL"
  },
  "interpretation": "NORMAL"
}
```

### What Medical Staff Need to Review

**Extended approval questions:**

1. ✅ Are the selection rules (focused/moderate/comprehensive) clinically sound?
2. ✅ **NEW:** Are the documented units the ones used in practice?
3. ✅ **NEW:** Are the reference ranges appropriate for our population?
4. ✅ **NEW:** Are the CDS thresholds clinically safe?

**Spot-check example:**
```
Hemoglobin Severe Anemia Alert

LOINC Codes (Focused): 5 codes
Units Supported: g/dL, g/L, mmol/L
Threshold: <7.0 g/dL (or equivalent)

Reference Ranges (adult male, g/dL): 13.5-17.5
Reference Ranges (adult female, g/dL): 12.0-15.5

Question for reviewer:
1. Is the 7.0 g/dL threshold clinically appropriate for transfusion consideration?
2. Are these reference ranges consistent with local lab standards?
3. Are the supported units the ones we actually see in our EHR?
```

### Implementation Guidance

**For implementers using these ValueSets:**

**Step 1:** Determine your EHR's unit conventions
```sql
SELECT loinc_code, unit, COUNT(*)
FROM lab_observations
WHERE loinc_code IN ('718-7', '59260-0', ...)  -- hemoglobin codes
GROUP BY loinc_code, unit
ORDER BY COUNT(*) DESC
```

**Step 2:** Choose normalization strategy
- Option A: Normalize at query time (flexible but slower)
- Option B: Pre-normalize warehouse (faster but needs maintenance)

**Step 3:** Implement with unit handling
```python
# Example CDS rule with unit normalization
from valueset_utils import normalize_value, get_threshold

def check_severe_anemia(observation, patient):
    # Normalize to g/dL
    normalized = normalize_value(
        value=observation.value,
        from_unit=observation.unit,
        to_unit="g/dL",
        loinc_code=observation.code
    )

    # Get demographic-adjusted threshold
    threshold = get_threshold(
        valueset="hemoglobin_focused",
        condition="severe_anemia",
        unit="g/dL",
        sex=patient.sex,
        age=patient.age
    )

    return normalized < threshold
```

---

## Summary (Updated)

**Key Principles:**

1. ✅ **Hierarchical clustering:** Focused ⊂ Moderate ⊂ Comprehensive
2. ✅ **Use-case driven:** CDS needs focused, research needs comprehensive
3. ✅ **Two dimensions:** Individual vs population AND precision vs recall
4. ✅ **Precision/recall tradeoff:** Explicit and documented
5. ✅ **Selection rules:** Reviewable, not individual codes
6. ✅ **Validation:** Against reference sets and clinical use cases
7. ✅ **NEW: Unit handling:** Document units, provide conversions, validate thresholds

**Next Steps:**

1. Review and approve hierarchical clustering concept
2. Validate selection rules (not individual codes)
3. **NEW:** Review unit metadata and reference ranges
4. **NEW:** Validate CDS thresholds with local clinicians
5. Spot-check 5-10 examples per level
6. Approve framework for all 100 lab parameters

---

**Questions or concerns? Contact:** [Your email]

**Last Updated:** 2026-01-11
