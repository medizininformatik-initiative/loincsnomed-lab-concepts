Profile: HemoglobinStandard
Parent: $KDSLab
Id: hemoglobin-standard
Title: "Hemoglobin concentration in blood"
Description: "Observation profile for Hemoglobin concentration in blood (standard test). code bound to the curated hemoglobin-standard ValueSet; specimen Blood."
* code from https://interpolar.example/fhir/ValueSet/hemoglobin-standard (required)
* value[x] only Quantity
* valueQuantity.unit = "g/dL"  // expected unit
* specimen only Reference(Specimen)  // Blood
