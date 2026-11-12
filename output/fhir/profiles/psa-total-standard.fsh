Profile: PsaTotalStandard
Parent: $KDSLab
Id: psa-total-standard
Title: "Total PSA in serum, plasma or blood"
Description: "Observation profile for Total PSA in serum, plasma or blood (standard test). code bound to the curated psa-total-standard ValueSet; specimen Serum/Plasma/Blood."
* code from https://interpolar.example/fhir/ValueSet/psa-total-standard (required)
* value[x] only Quantity
* valueQuantity.unit = "ng/mL"  // expected unit
* specimen only Reference(Specimen)  // Serum/Plasma/Blood
