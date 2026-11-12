Profile: EgfrStandard
Parent: $KDSLab
Id: egfr-standard
Title: "Estimated glomerular filtration rate (eGFR)"
Description: "Observation profile for Estimated glomerular filtration rate (eGFR) (standard test). code bound to the curated egfr-standard ValueSet; specimen Serum/Plasma/Blood."
* code from https://interpolar.example/fhir/ValueSet/egfr-standard (required)
* value[x] only Quantity
* valueQuantity.unit = "mL/min/{1.73_m2}"  // expected unit
* specimen only Reference(Specimen)  // Serum/Plasma/Blood
