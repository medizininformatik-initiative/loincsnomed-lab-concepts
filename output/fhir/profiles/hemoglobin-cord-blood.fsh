Profile: HemoglobinCordBlood
Parent: $KDSLab
Id: hemoglobin-cord-blood
Title: "Hemoglobin concentration in cord blood"
Description: "Observation profile for Hemoglobin concentration in cord blood (specialized test). code bound to the curated hemoglobin-cord-blood ValueSet; specimen Cord blood."
* code from https://interpolar.example/fhir/ValueSet/hemoglobin-cord-blood (required)
* value[x] only Quantity
* valueQuantity.unit = "g/dL or mmol/L"  // expected unit
* specimen only Reference(Specimen)  // Cord blood
