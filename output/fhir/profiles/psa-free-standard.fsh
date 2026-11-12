Profile: PsaFreeStandard
Parent: $KDSLab
Id: psa-free-standard
Title: "Free PSA in serum, plasma or blood"
Description: "Observation profile for Free PSA in serum, plasma or blood (specialized test). code bound to the curated psa-free-standard ValueSet; specimen Serum/Plasma/Blood."
* code from https://interpolar.example/fhir/ValueSet/psa-free-standard (required)
* value[x] only Quantity
* valueQuantity.unit = "ng/mL"  // expected unit
* specimen only Reference(Specimen)  // Serum/Plasma/Blood
