Profile: CreatinineStandard
Parent: $KDSLab
Id: creatinine-standard
Title: "Creatinine in serum, plasma or blood"
Description: "Observation profile for Creatinine in serum, plasma or blood (standard test). code bound to the curated creatinine-standard ValueSet; specimen Serum/Plasma/Blood."
* code from https://interpolar.example/fhir/ValueSet/creatinine-standard (required)
* value[x] only Quantity
* valueQuantity.unit = "mg/dL or umol/L"  // expected unit
* specimen only Reference(Specimen)  // Serum/Plasma/Blood
