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
 << 704327008 |Direct site| = (<< 119297000 |Blood specimen|
                               MINUS (<< 122556008 |Cord blood specimen|
                                      OR << 737357006 |Fetal blood specimen|
                                      OR << 440500007 |Dried blood spot specimen|)),
 << 370130000 |Property|    = (<< 118539007 |Mass concentration|
                               OR << 118556004 |Substance concentration|
                               OR << 118569000 |Arbitrary concentration|),
 << 370132008 |Scale type|  = << 30766002 |Quantitative value|
```

Read it as: any observable entity whose Component is exactly Hemoglobin, whose specimen is Blood or a subtype of Blood (venous, arterial, capillary, serum, plasma) but not cord blood, fetal blood or a dried blood spot, whose Property is one of the three concentration properties or a subtype, and whose Scale is Quantitative. `<<` means "this concept and all its descendants", `<` "the descendants only"; without either the value must match exactly. The choice between the two is a clinical decision made visible: `<< 38082009` would additionally pull in HbA1c and the hemoglobin variants, which is wanted for a hemoglobin *pool* but not for the routine hemoglobin test.

{{EXAMPLE_ECL_ROWS}}

### The shared building blocks

The clinical review of the first version led to two building blocks that every routine blood test now shares, so that a decision is made once and applied everywhere:

| Block | ECL | Decision it encodes |
|---|---|---|
| **Blood** (specimen) | `<< Blood specimen MINUS (<< Cord blood specimen OR << Fetal blood specimen OR << Dried blood spot specimen)` | Venous, arterial, capillary and mixed venous blood, serum and plasma are the same routine specimen for a clinical test; the differences are left to `Observation.specimen`. Cord blood is a neonatal value with its own reference range and gets its own test. Fetal blood and dried blood spots belong to prenatal and screening programmes, not to routine care. |
| **Concentration** (property) | `<< Mass concentration OR << Substance concentration OR << Arbitrary concentration` | g/dL, mmol/L and U/mL codes of the same measurement are one clinical test; the unit is a UCUM conversion, not a code boundary. Ratios, fractions and rates are not concentrations and stay out. |

Two limits of the ontology show up in these blocks. Observables "in Fetus" carry no Direct site in the LOINC Ontology, so no specimen rule can select or exclude them; they are simply invisible. And SNOMED CT models plasma as an *acellular blood specimen* under Blood specimen, which is right for chemistry but admits the plasma platelet counts of transfusion medicine; the platelet rule therefore subtracts `<< Plasma specimen` from the block, a point marked for clinical review.

### The three parts of every ValueSet

Each ValueSet of this proposal has the same `compose`:

1. **LOINC enumeration.** The LOINC codes of all concepts the rule selects, as `include` on `http://loinc.org` with the module's LOINC version. This is the part any FHIR validator and any terminology server can use today.
2. **Observables without a LOINC code.** The LOINC Ontology also contains observables for which no LOINC code exists yet. They are listed as SNOMED CT codes, so that the ValueSet is complete and a site can see where a LOINC request is pending.
3. **The rule.** The ECL as an intensional `include` on `http://snomed.info/sct` with `filter.property = constraint`, pinned to the release `{{VERSION_URI}}`. It documents why the codes in part 1 are there, and it is the part that regenerates.

Parts 1 and 2 are the enumeration of part 3 at the stated release. They are not independent sources.

### Expanding and validating

* On a terminology server that holds the LOINC Ontology release (for example Snowstorm with the LOINC extension loaded, or the LOINC Ontology browser), all three parts expand and the expansion equals the enumeration.
* On a server without the LOINC Ontology, such as the public HL7 server, the SNOMED CT includes cannot be resolved. The build's QA report shows this as a warning for every ECL include and as an error for every enumerated SNOMED CT code without a LOINC code. The LOINC enumeration still expands, and validation of an `Observation.code` carrying a LOINC code works as usual.
* A validator checking `Observation.code` against a derived profile only needs the LOINC enumeration.
* **The module's own CI** validates against the MII terminology server (Ontoserver) through a proxy. Since November 2026 that server holds the LOINC Ontology {{RELEASE}}, and the ECL includes of this proposal expand there. Three classes of QA errors remain, none of them a content error: (1) the server rejects the publisher's batch validation request, so every enumerated LOINC and SNOMED CT code is reported once, on `master` as well; (2) the LOINC Ontology observables without a LOINC code are reported against the international edition; (3) the publisher checks each ECL include by asking the server to *validate* a one-rule ValueSet, and the server evaluates that ECL in its default edition instead of the edition the include names, so every rule that uses a concept of the LOINC Ontology module itself (*Measurement property*, the MCHC and MCV focus concepts) is reported as "unknown concept", although the same ValueSet *expands* correctly. The third class is reproducible on the vendor's public server and has been reported. The counts in the QA report therefore measure the terminology setup; the build with the public HL7 server reports only the first two classes.

### Versions and regeneration

The artifacts are pinned to **LOINC Ontology {{RELEASE}}**, and their LOINC enumerations to **LOINC {{LOINC_VERSION}}**, the LOINC release that LOINC Ontology release is built on. That LOINC alias lives next to the ValueSets (`aliases-loinc-ontology.fsh`), not in the module's `aliases.fsh`: the module pins LOINC {{MODULE_LOINC_PIN}} for its own ValueSets and forces that version in its expansion manifest (`force-system-version`), so an IG build validates every LOINC code against the module's pin, whatever a ValueSet declares. The two pins are kept separate so that a new LOINC Ontology release can be regenerated without touching the module. A code that LOINC introduced or deprecated between the two is a review item, not a failure of the method.{{NEW_LOINC_SENTENCE_EN}} For a new release the generator re-runs every rule, lists the concepts that entered or left each ValueSet, and rewrites these pages. A release can also remodel the attributes themselves: between 2026-03-21 and 2026-10-21 the LOINC Ontology moved more than 10,000 presence observables from Property `Presence` (705057003) to `Threshold (property)` (118589004, a subtype of Measurement property) and renamed them from "Presence of …" to "Threshold presence of …". The nitrite rule on this branch therefore selects `<< 118589004 |Threshold (property)|` instead of `<< 705057003 |Presence|`; its LOINC enumeration did not change. The old rule would have returned an empty ValueSet, which is the kind of failure a regeneration makes visible. The release-to-release difference report is published with the generator in [{{REPO_NAME}}]({{REPO_URL}}).

### Reading the review tables

For every ValueSet the generator also publishes a table with one row per concept: LOINC code, SCTID, fully specified name, the use-case bucket it was classified into, and the attribute values that caused the classification. These tables are the place to challenge a single code; the rule is the place to challenge a whole set.
