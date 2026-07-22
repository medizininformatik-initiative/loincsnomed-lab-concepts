Profile: PsaTotalStandard
Parent: $KDSLab
Id: psa-total-standard
Title: "Total PSA in serum/plasma"
Description: "Observation profile for Total PSA in serum/plasma (standard test). code bound to the curated psa-total-standard ValueSet; specimen Serum/Plasma."
* code from https://interpolar.example/fhir/ValueSet/psa-total-standard (required)
* value[x] only Quantity
* valueQuantity.unit = "ng/mL"  // expected unit
* specimen only Reference(Specimen)  // Serum/Plasma
