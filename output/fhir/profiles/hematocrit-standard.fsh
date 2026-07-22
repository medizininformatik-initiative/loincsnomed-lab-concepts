Profile: HematocritStandard
Parent: $KDSLab
Id: hematocrit-standard
Title: "Hematocrit (volume fraction) in blood"
Description: "Observation profile for Hematocrit (volume fraction) in blood (standard test). code bound to the curated hematocrit-standard ValueSet; specimen Blood."
* code from https://interpolar.example/fhir/ValueSet/hematocrit-standard (required)
* value[x] only Quantity
* valueQuantity.unit = "L/L"  // expected unit
* specimen only Reference(Specimen)  // Blood
