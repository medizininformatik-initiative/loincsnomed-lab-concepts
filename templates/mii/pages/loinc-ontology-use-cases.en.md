This page lists the {{N_USECASE}} ValueSets of the [LOINC Ontology proposal](loinc-ontology-valuesets.html) that serve **data users**: for each of {{N_ANALYTES}} analytes, graded sets of everything the LOINC Ontology maps to that analyte. The construction is explained under [How the ValueSets are built](loinc-ontology-method.html); the narrow per-test sets are on [ValueSets per clinical test (Laborparameter)](loinc-ontology-clinical-tests.html).

### The use case defines the aggregation

A data integration centre is asked for "all hemoglobin values". What that means depends on the question: a cohort screen wants every observation that is about hemoglobin at all; a longitudinal analysis wants numeric values; a cross-site comparison wants only values that can be converted to one unit. No single list serves all three, and a list that serves one will be wrong for the others.

The proposal therefore starts from the **candidate pool** of an analyte, everything in the LOINC Ontology whose Component is the analyte (any property, any scale, any specimen), and classifies that pool by two attributes, **Scale type** and **Property**, into buckets that correspond to what a data user may do with the values. One ValueSet per analyte and bucket.

### The buckets

| Bucket | Rule | What a data user gets |
|---|---|---|
| **Complete** | the whole pool | Upper bound: every observable about the analyte, including panel-like groupers and the "Measurement of X" concepts that have no scale. For recall, cohort screening, and as the base the other buckets are cut from. |
| **Quantitative (all numeric)** | Scale type Quantitative, or any measurement Property when no scale is asserted | All numeric results, including ratios, fractions and rates. Values can be plotted per code, but not pooled across codes without looking at the unit. |
| **Quantitative and convertible** | Quantitative with a concentration Property (mass, substance, number, arbitrary or quantity concentration), ratios and fractions excluded | The set whose values can be pooled after UCUM conversion. The bucket for cross-site comparison and for reference-range work. |
| **Qualitative** | Scale type Ordinal or Nominal, or a Presence or Threshold Property | Presence or absence, positive or negative, graded findings. Values are coded, not numeric. |
| **Semi-quantitative** | Scale type Semi-quantitative | Test-strip and dipstick reads (0 to ++++). Neither strictly numeric nor purely qualitative; usually kept apart from both. |

The classification is applied in this order, first match wins: qualitative, then semi-quantitative, then quantitative (with convertible as a refinement). Scale type is not always asserted in the LOINC Ontology; using Property as a second criterion is what makes the classification complete. Across all analytes no concept remained unclassified.

Observables with a Component but **no Property** are order or panel codes (for example "Differential count of white blood cells"). They resolve into several results and are not a single measurable value; they appear in the review tables but get no ValueSet.

### The analytes

The pool column shows the Component; `<<` marks "this concept and its subtypes". Cells link to the ValueSet and show the number of concepts.

{{USECASE_TABLE}}

### Recall against LOINC itself

A rule can only select what the LOINC Ontology models, so the pools are checked the other way round as well: for every analyte, the LOINC table of release {{LOINC_VERSION}} is searched for the laboratory terms a laboratory physician would count as that analyte (by Component, where needed Property and System), and the table says how many of them the pool reaches. A term outside the pool is modelled with another Component, or not modelled at all; the analyte pages list them one by one. The last column counts how many of the LOINC terms the per-test ValueSets enumerate; the gap to the pool is the set of codes a clinician would not call the routine value.

{{RECALL_TABLE}}

### Review notes

* **Hematocrit** has its own pool now: Erythrocyte with the property volume fraction. The erythrocyte pool still contains the hematocrit concepts, which is correct, a hematocrit is an erythrocyte observable; only the hematocrit use-case ValueSets are no longer a copy of the erythrocyte ones.
* **MCH** is pooled on the exact Component Hemoglobin with the two entitic properties (mass and substance amount per cell), no longer on `<< Hemoglobin`, which had brought HbA1c and the hemoglobin variants in. The hemoglobin pool uses the exact Component and therefore also contains the MCH concepts.
* **GFR** has no Component in the LOINC Ontology; its pool is every observable whose *Process output* is the GFR calculation. **Protein in urine** is pooled with the specimen in the pool definition, because total protein in serum is a different clinical parameter.
* **Leukocytes** has two order-level concepts (the differential) that are listed in the review tables and excluded from every bucket.
* **Specimen is not a criterion** in this layer: urine hemoglobin and blood hemoglobin are in the same quantitative bucket. A data user who needs one specimen narrows by the per-test ValueSet or by `Observation.specimen`.
