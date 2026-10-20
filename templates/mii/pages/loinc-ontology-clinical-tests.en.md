This page lists the {{N_TESTS}} ValueSets of the [LOINC Ontology proposal](loinc-ontology-valuesets.html) that each describe **one clinical test**, and the Observation profile derived for each of them. The rule behind every ValueSet is shown decomposed into its attributes; the construction is explained under [How the ValueSets are built](loinc-ontology-method.html).

### What counts as one clinical test

A clinical test here is what a clinician means when ordering or reading a value: *the* hemoglobin, *the* potassium, *the* total PSA. It is defined by the Component plus a **tier**:

* **standard**: the routine value. One ValueSet per analyte, narrowed to the usual specimen, property and scale (for example hemoglobin as mass concentration in blood, quantitative).
* **specialized**: a clinically distinct variant that must not be pooled with the standard value and therefore gets its own ValueSet: free PSA, the free/total PSA ratio, the LDH isoenzymes, the white cell differential.

Each test is one ValueSet and one Observation profile derived from [Laboratory Test](StructureDefinition-mii-pr-labor-laboruntersuchung.html). The profile binds `Observation.code` to the ValueSet with strength *required*, restricts `value[x]` to the data type the test produces, and names the expected UCUM unit in a comment. Everything else is inherited from the module's profile; the derived profiles add no new elements.

### How to use them

* **Implementers mapping a local catalogue** pick the ValueSet of the test and choose, within it, the LOINC code whose specimen, property and method match the local procedure. The attribute columns below say what every code in the set has in common; the remaining differences (venous versus arterial blood, calculation versus measurement) are the ones to decide locally.
* **Validation**: an Observation that claims a derived profile in `meta.profile` is checked against the LOINC enumeration of the ValueSet. The example [Laboratory result: hemoglobin](Observation-mii-exa-labor-loinc-ontology-hemoglobin.html) conforms to the hemoglobin profile.
* **Data users** wanting the routine value of an analyte take the *standard* ValueSet; for broader pooling see the [use-case ValueSets](loinc-ontology-use-cases.html).

### The tests

Attribute columns show the rule; `<<` marks "this concept and its subtypes", a bare name means an exact match. *LOINC* is the number of LOINC codes in the ValueSet; *SNOMED only* the number of LOINC Ontology observables without a LOINC code.

{{TESTS_TABLE}}

### Review notes

* **Tier and specimen choices** are clinical decisions. They are visible in the rule and changed by editing it; the table is regenerated.
* **MCH, MCHC and MCV** have no specimen in their rule: the first is Hemoglobin with the property *entitic mass* (mass per cell), the other two are their own observable concepts in the LOINC Ontology and are selected as focus concepts rather than by Component.
* **The white cell differential** is an order-level concept in the LOINC Ontology (a Component without a Property) and currently has no LOINC code there; its ValueSet holds two SNOMED CT codes. The single differential results (neutrophils, lymphocytes and so on) are separate observables and would each be their own clinical test.
* **Nitrite in urine** is the one qualitative test in the set; its profile restricts the value to `CodeableConcept`, to be coded with the module's [coded laboratory results](ValueSet-mii-vs-labor-laborergebnis-codiert.html).
