# ECL Query Template with Design Rationale

## Template for Laboratory Observable Entities with OR Property Clause

```
// Design Rationale: This ECL query uses an OR clause for the Property attribute to capture
// both quantitative measurements (descendants of "Measurement property") AND mass fraction
// measurements (property 118586006). Mass fraction is NOT a descendant of measurement property
// in SNOMED CT, causing laboratory tests with mass fraction units (e.g., methemoglobin/
// hemoglobin ratio LOINC codes 71879-1, 71880-9, 71881-7, 71882-5, 71883-3) to be missed
// if only measurement property descendants are queried. The OR clause ensures comprehensive
// coverage of all relevant laboratory measurement types while maintaining specificity through
// component and specimen constraints.

<< 363787002 |Observable entity| :
    246093002 |Component| = << [COMPONENT_CONCEPT_ID] |Component name|,
    370130000 |Property| = (<< 685451010000100 |Measurement property (qualifier value)| OR 118586006 |Mass fraction (property) (qualifier value)|),
    704327008 |Direct site| = << [SPECIMEN_CONCEPT_ID] |Specimen type|
```

## Example: Methemoglobin in Blood

```
// Design Rationale: This ECL query uses an OR clause for the Property attribute to capture
// both quantitative measurements (descendants of "Measurement property") AND mass fraction
// measurements (property 118586006). Mass fraction is NOT a descendant of measurement property
// in SNOMED CT, causing laboratory tests with mass fraction units (e.g., methemoglobin/
// hemoglobin ratio LOINC codes 71879-1, 71880-9, 71881-7, 71882-5, 71883-3) to be missed
// if only measurement property descendants are queried. The OR clause ensures comprehensive
// coverage of all relevant laboratory measurement types while maintaining specificity through
// component and specimen constraints.

<< 363787002 |Observable entity| :
    246093002 |Component| = << 27840003 |Methemoglobin (substance)|,
    370130000 |Property| = (<< 685451010000100 |Measurement property (qualifier value)| OR 118586006 |Mass fraction (property) (qualifier value)|),
    704327008 |Direct site| = << 119297000 |Blood specimen (specimen)|
```

## Key Design Decisions

1. **Component Descendants (`= <<`)**: Uses descendant operator to capture substance derivatives (e.g., cyanmethemoglobin as descendant of methemoglobin)

2. **Property OR Clause**: Includes both measurement property descendants AND mass fraction to ensure complete coverage

3. **Measurement Property Descendants (`<< 685451010000100`)**: Captures all quantitative measurement types (substance concentration, mass concentration, etc.)

4. **Mass Fraction Explicit (`118586006`)**: NOT a descendant of measurement property - must be explicitly included via OR

5. **Specimen Descendants (`= <<`)**: Allows for specific specimen types while capturing relevant subtypes

## Properties Covered

The OR clause captures:

**Via Measurement Property Descendants:**
- 118555000 |Substance concentration (property) (qualifier value)|
- 119349003 |Mass concentration (property) (qualifier value)|
- 119350003 |Molar concentration (property) (qualifier value)|
- 119351004 |Catalytic concentration (property) (qualifier value)|
- And many other measurement property subtypes...

**Via Explicit Mass Fraction:**
- 118586006 |Mass fraction (property) (qualifier value)| - NOT in measurement property hierarchy

## Validation

Test query confirmed OR clause support:
- Server: LOINCSNOMED Snowstorm (browser.loincsnomed.org)
- Test date: 2025-01-14
- Results: Successfully returned 15 concepts including mass fraction measurements
- Script: `scripts/test_or_property_ecl.py`
