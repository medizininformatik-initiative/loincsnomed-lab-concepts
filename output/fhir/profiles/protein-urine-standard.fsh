Profile: ProteinUrineStandard
Parent: $KDSLab
Id: protein-urine-standard
Title: "Protein in urine (mass concentration)"
Description: "Observation profile for Protein in urine (mass concentration) (standard test). code bound to the curated protein-urine-standard ValueSet; specimen Urine."
* code from https://interpolar.example/fhir/ValueSet/protein-urine-standard (required)
* value[x] only Quantity
* valueQuantity.unit = "mg/dL or g/L"  // expected unit
* specimen only Reference(Specimen)  // Urine
