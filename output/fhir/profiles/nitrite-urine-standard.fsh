Profile: NitriteUrineStandard
Parent: $KDSLab
Id: nitrite-urine-standard
Title: "Nitrite in urine (qualitative)"
Description: "Observation profile for Nitrite in urine (qualitative) (standard test). code bound to the curated nitrite-urine-standard ValueSet; specimen Urine."
* code from https://interpolar.example/fhir/ValueSet/nitrite-urine-standard (required)
* value[x] only CodeableConcept
// qualitative result — bind valueCodeableConcept to a presence/absence ValueSet
* specimen only Reference(Specimen)  // Urine
