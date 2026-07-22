Profile: Hba1cStandard
Parent: $KDSLab
Id: hba1c-standard
Title: "HbA1c in blood"
Description: "Observation profile for HbA1c in blood (standard test). code bound to the curated hba1c-standard ValueSet; specimen Blood."
* code from https://interpolar.example/fhir/ValueSet/hba1c-standard (required)
* value[x] only Quantity
* valueQuantity.unit = "% or mmol/mol"  // expected unit
* specimen only Reference(Specimen)  // Blood
