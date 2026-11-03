This page shows what the LOINC Ontology release **{{RELEASE}}** changed for every rule of the [LOINC Ontology proposal](loinc-ontology-valuesets.html) compared with the previous release **{{PREV_RELEASE}}**: how many concepts each rule selected before and after, and which concepts entered or left. It is the output of the generator's release comparison, rendered with fully specified names and LOINC codes so that a reviewer can read it without a terminology server.

### How to read it

* A concept is *added* when the new release selects it and the old one did not. Most additions are new LOINC Ontology concepts for codes of a newer LOINC release; some are existing concepts whose attributes were remodelled so that the rule now sees them.
* A concept is *removed* when the old release selected it and the new one does not: it was inactivated, or an attribute the rule depends on was dropped or changed. A removal is a review item for the rule, not for the module's data.
* Unchanged rules are listed in the table but have no concept lists.

### Summary

{{DELTA_TABLE}}

### Concepts per rule

{{DELTA_LISTS}}
