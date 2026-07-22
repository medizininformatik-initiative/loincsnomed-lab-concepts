Profile: PsaFreeStandard
Parent: $KDSLab
Id: psa-free-standard
Title: "Free PSA in serum/plasma"
Description: "Observation profile for Free PSA in serum/plasma (specialized test). code bound to the curated psa-free-standard ValueSet; specimen Serum/Plasma."
* code from https://interpolar.example/fhir/ValueSet/psa-free-standard (required)
* value[x] only Quantity
* valueQuantity.unit = "ng/mL"  // expected unit
* specimen only Reference(Specimen)  // Serum/Plasma
