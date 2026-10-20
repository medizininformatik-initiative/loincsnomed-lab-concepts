This page explains how every ValueSet in the [LOINC Ontology proposal](loinc-ontology-valuesets.html) is constructed, so that a reader can check a rule, expand a ValueSet on a terminology server, and regenerate the artifacts for a new release.

### The LOINC Ontology in one paragraph

The [LOINC Ontology](https://loincsnomed.org) is published jointly by the Regenstrief Institute and SNOMED International. It represents LOINC laboratory terms as SNOMED CT concepts in an extension module (module id `11010000107`), placed under *Observable entity*. Each concept carries its LOINC code as an alternate identifier and is modelled with the same attributes that make up a LOINC term. Because the concepts live in SNOMED CT, the SNOMED Expression Constraint Language (ECL) can select them by attribute value, including subtype hierarchies of the value.

| Attribute | SNOMED CT attribute | LOINC part | Example for `718-7` Hemoglobin [Mass/volume] in Blood |
|---|---|---|---|
| Component | `246093002` | Component | Hemoglobin (substance) |
| Property | `370130000` | Property | Mass concentration |
| Scale type | `370132008` | Scale | Quantitative value |
| Direct site | `704327008` | System | Blood specimen |
| Technique | `246501002` | Method | (none) |
| Time aspect | `370134009` | Time | Single point in time |

### Anatomy of a rule

The rule for the clinical test *Hemoglobin concentration in blood* reads:

```
<< 363787002 |Observable entity| :
    246093002 |Component|   = 38082009 |Hemoglobin (substance)|,
 << 704327008 |Direct site| = << 119297000 |Blood specimen|,
 << 370130000 |Property|    = << 118539007 |Mass concentration|,
 << 370132008 |Scale type|  = << 30766002 |Quantitative value|
```

Read it as: any observable entity whose Component is exactly Hemoglobin, whose specimen is Blood or a subtype of Blood (venous, arterial, capillary), whose Property is Mass concentration or a subtype, and whose Scale is Quantitative. `<<` means "this concept and all its descendants", `<` "the descendants only"; without either the value must match exactly. The choice between the two is a clinical decision made visible: `<< 38082009` would additionally pull in HbA1c and the hemoglobin variants, which is wanted for a hemoglobin *pool* but not for the routine hemoglobin test.

{{EXAMPLE_ECL_ROWS}}

### The three parts of every ValueSet

Each ValueSet of this proposal has the same `compose`:

1. **LOINC enumeration.** The LOINC codes of all concepts the rule selects, as `include` on `http://loinc.org` with the module's LOINC version. This is the part any FHIR validator and any terminology server can use today.
2. **Observables without a LOINC code.** The LOINC Ontology also contains observables for which no LOINC code exists yet. They are listed as SNOMED CT codes, so that the ValueSet is complete and a site can see where a LOINC request is pending.
3. **The rule.** The ECL as an intensional `include` on `http://snomed.info/sct` with `filter.property = constraint`, pinned to the release `{{VERSION_URI}}`. It documents why the codes in part 1 are there, and it is the part that regenerates.

Parts 1 and 2 are the enumeration of part 3 at the stated release. They are not independent sources.

### Expanding and validating

* On a terminology server that holds the LOINC Ontology release (for example Snowstorm with the LOINC extension loaded, or the LOINC Ontology browser), all three parts expand and the expansion equals the enumeration.
* On a server without the LOINC Ontology, such as the HL7 server used by the IG build, the SNOMED CT includes cannot be resolved and the build's QA report flags them. The LOINC enumeration still expands, and validation of an `Observation.code` carrying a LOINC code works as usual.
* A validator checking `Observation.code` against a derived profile only needs the LOINC enumeration.

### Versions and regeneration

The artifacts are pinned to **LOINC Ontology {{RELEASE}}**. The LOINC Ontology is released periodically; the module pins LOINC 2.82 for its own ValueSets. A code that LOINC introduced or deprecated between the two is a review item, not a failure of the method. For a new release the generator re-runs every rule, lists the concepts that entered or left each ValueSet, and rewrites these pages. The release-to-release difference report is published with the generator in [{{REPO_NAME}}]({{REPO_URL}}).

### Reading the review tables

For every ValueSet the generator also publishes a table with one row per concept: LOINC code, SCTID, fully specified name, the use-case bucket it was classified into, and the attribute values that caused the classification. These tables are the place to challenge a single code; the rule is the place to challenge a whole set.
