This page lists the {{N_TESTS}} ValueSets of the [LOINC Ontology proposal](loinc-ontology-valuesets.html) that each describe **one clinical test** (German: *Laborparameter*), and the Observation profile derived for each of them. The rule behind every ValueSet is shown decomposed into its attributes; the construction and the shared building blocks are explained under [How the ValueSets are built](loinc-ontology-method.html).

### What counts as one clinical test

A clinical test here is what a clinician means when ordering or reading a value: *the* hemoglobin, *the* potassium, *the* total PSA. One test is one line in a laboratory report, and its codes are the ones whose values can be read as the same quantity. It is defined by the Component plus a **tier**:

* **standard**: the routine value. One ValueSet per analyte, narrowed to the usual specimen, property and scale. Since the clinical review the standard tests share two building blocks: the specimen is *blood and its subtypes, serum and plasma included, cord blood, fetal blood and dried blood spot excluded*, and the property is *any concentration* (mass, substance or arbitrary), so that g/dL and mmol/L codes of the same measurement sit in one set and the unit is left to UCUM conversion.
* **specialized**: a clinically distinct variant that must not be pooled with the standard value and therefore gets its own ValueSet: free PSA, the free/total PSA ratio, the LDH isoenzymes, the white cell differential, the protein/creatinine ratio, hemoglobin in cord blood.

Each test is one ValueSet and one Observation profile derived from [Laboratory Test](StructureDefinition-mii-pr-labor-laboruntersuchung.html). The profile binds `Observation.code` to the ValueSet with strength *required*, restricts `value[x]` to the data type the test produces, and names the expected UCUM unit in a comment. Everything else is inherited from the module's profile; the derived profiles add no new elements.

### How to use them

* **Implementers mapping a local catalogue** pick the ValueSet of the test and choose, within it, the LOINC code whose specimen, property and method match the local procedure. The attribute columns below say what every code in the set has in common; the remaining differences (venous versus arterial blood, calculation versus measurement, g/dL versus mmol/L) are the ones to decide locally.
* **Validation**: an Observation that claims a derived profile in `meta.profile` is checked against the LOINC enumeration of the ValueSet. The example [Laboratory result: hemoglobin](Observation-mii-exa-labor-loinc-ontology-hemoglobin.html) conforms to the hemoglobin profile.
* **Data users** wanting the routine value of an analyte take the *standard* ValueSet; for broader pooling see the [use-case ValueSets](loinc-ontology-use-cases.html).

### The tests

Attribute columns show the rule; `<<` marks "this concept and its subtypes", a bare name means an exact match, `minus` an exclusion inside the value. *LOINC* is the number of LOINC codes in the ValueSet (hand-added ontology-gap codes included); *SNOMED only* the number of LOINC Ontology observables without a LOINC code. The test name links to the analyte's review page with every included and excluded code and the reason.

{{TESTS_TABLE}}

### Review notes

* **Tier and specimen choices** are clinical decisions. They are visible in the rule and changed by editing it; the table is regenerated.
* **Open for clinical review**: whether the platelet count should exclude plasma and platelet-rich plasma (three transfusion-medicine codes), and whether the LDH isoenzymes should be restricted to serum and plasma (21 codes in urine, CSF and effusions dropped). Both are stated as rules and discussed on the analyte pages.
* **What the ontology cannot express.** The LOINC *challenge* and *timing* part is not an attribute of the LOINC Ontology: the creatinine test therefore contains 71 time-point and challenge codes next to the eight routine codes. LOINC's *status* (active, discouraged) is not an attribute either: a discouraged potassium code and two discouraged GFR codes pass their rules. Both would be handled by a filter on the LOINC table in the generator, which is a decision for the module, not for a rule.
* **Ontology gaps.** A LOINC code the release does not model cannot be reached by any rule. The molar MCHC (59467-1) is such a code; it is added to its ValueSet by hand, marked as an ontology gap on the ValueSet and on the analyte page, and reported to the LOINC Ontology maintainers.
* **MCHC and MCV** have no Component in their rule: both are their own observable concepts in the LOINC Ontology (MCHC through *Inheres in* = Hemoglobin) and are selected as focus concepts. **MCH** is Hemoglobin with the entitic properties on the erythrocyte specimen. **The eGFR** has no Component at all; it is selected through *Process output* = Glomerular filtration rate (calculation).
* **The white cell differential** is an order-level concept in the LOINC Ontology (a Component without a Property) and currently has no LOINC code there; its ValueSet holds two SNOMED CT codes. The single differential results (neutrophils, lymphocytes and so on) are separate observables and would each be their own clinical test.
* **Nitrite in urine** is the one qualitative test in the set; its profile restricts the value to `CodeableConcept`, to be coded with the module's [coded laboratory results](ValueSet-mii-vs-labor-laborergebnis-codiert.html).
