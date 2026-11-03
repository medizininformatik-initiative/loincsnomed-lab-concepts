This page lists the {{N_QUERIES}} rules of the [LOINC Ontology proposal](loinc-ontology-valuesets.html), grouped by the request family of the 2027 module, with the ValueSet each rule produces and the derived Observation profile where one exists. The construction is explained under [How the ValueSets are built](loinc-ontology-method.html); every family has its own review page with the rule decomposed into attributes and the codes it selects.

### What counts as one request

The 2027 module defines one Observation profile per *question asked of the laboratory*: is something growing (general culture), what is it (general determination), is a named pathogen there (specific determination), how much of it (colony count, pathogen load, Ct value, titre, quantitative serology), is it susceptible (phenotypic and predicted susceptibility), what was seen under the microscope (general and specific microscopy), does it carry a resistance mechanism. Each such question is a request family here. Inside a family several rules exist on purpose: the rule the profile would bind, an upper bound for review, and rules that show what a technique clause gains or loses.

### How to use them

* **Implementers mapping a local catalogue** pick the ValueSet of the request and choose, within it, the LOINC code whose organism, specimen and method match the local procedure. The attribute table on the family page says what every code in the set has in common.
* **Validation**: an Observation that claims a derived profile in `meta.profile` is checked against the LOINC enumeration of the bound ValueSet.
* **Module editors** compare the ValueSet of a rule with the module's own LOINC ValueSet of the same request; the coverage tables below do that for the enumerated codes.

### The rules

*LOINC* is the number of LOINC codes in the ValueSet; *SNOMED only* the number of LOINC Ontology observables without a LOINC code; the delta column counts concepts that entered or left the ValueSet between {{PREV_RELEASE}} and {{RELEASE}}.

{{REQUEST_TABLE}}

### The derived profiles

Each profile below is derived from a module profile and only tightens `Observation.code` to the computed ValueSet (binding strength *required*). Where a request needs several rules, the profile binds a union ValueSet.

{{PROFILE_TABLE}}

### Coverage of the module's enumerated codes

The module enumerates LOINC codes in several of its ValueSets (next to the property filters). Of those {{N_ENUM}} codes, {{N_ENUM_IN_ONTOLOGY}} are in the LOINC Ontology {{RELEASE}}; the rest cannot be reached by any rule, whatever the rule says. Missing are, among others, the preferred method-neutral code 41852-5 (*Microorganism or agent identified in Specimen*), all colony-count codes, all avidity codes and all resistance-determinant codes. The second table lists every enumerated code with its SCTID and the proposal ValueSets that contain it.

{{COVERAGE_SUMMARY}}

{{COVERAGE_DETAIL}}
