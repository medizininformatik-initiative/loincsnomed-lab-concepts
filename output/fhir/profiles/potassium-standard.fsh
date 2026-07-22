Profile: PotassiumStandard
Parent: $KDSLab
Id: potassium-standard
Title: "Potassium in serum/plasma"
Description: "Observation profile for Potassium in serum/plasma (standard test). code bound to the curated potassium-standard ValueSet; specimen Serum/Plasma."
* code from https://interpolar.example/fhir/ValueSet/potassium-standard (required)
* value[x] only Quantity
* valueQuantity.unit = "mmol/L"  // expected unit
* specimen only Reference(Specimen)  // Serum/Plasma
