Profile: ErythrocytesCountStandard
Parent: $KDSLab
Id: erythrocytes-count-standard
Title: "Erythrocyte count in blood"
Description: "Observation profile for Erythrocyte count in blood (standard test). code bound to the curated erythrocytes-count-standard ValueSet; specimen Blood."
* code from https://interpolar.example/fhir/ValueSet/erythrocytes-count-standard (required)
* value[x] only Quantity
* valueQuantity.unit = "10*12/L"  // expected unit
* specimen only Reference(Specimen)  // Blood
