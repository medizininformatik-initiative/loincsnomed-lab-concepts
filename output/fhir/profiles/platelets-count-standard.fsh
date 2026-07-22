Profile: PlateletsCountStandard
Parent: $KDSLab
Id: platelets-count-standard
Title: "Platelet count in blood"
Description: "Observation profile for Platelet count in blood (standard test). code bound to the curated platelets-count-standard ValueSet; specimen Blood."
* code from https://interpolar.example/fhir/ValueSet/platelets-count-standard (required)
* value[x] only Quantity
* valueQuantity.unit = "10*9/L"  // expected unit
* specimen only Reference(Specimen)  // Blood
