Profile: LeukocytesCountStandard
Parent: $KDSLab
Id: leukocytes-count-standard
Title: "Leukocyte count in blood"
Description: "Observation profile for Leukocyte count in blood (standard test). code bound to the curated leukocytes-count-standard ValueSet; specimen Blood."
* code from https://interpolar.example/fhir/ValueSet/leukocytes-count-standard (required)
* value[x] only Quantity
* valueQuantity.unit = "10*9/L"  // expected unit
* specimen only Reference(Specimen)  // Blood
