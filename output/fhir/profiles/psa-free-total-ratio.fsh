Profile: PsaFreeTotalRatio
Parent: $KDSLab
Id: psa-free-total-ratio
Title: "%Free PSA (free/total ratio)"
Description: "Observation profile for %Free PSA (free/total ratio) (specialized test). code bound to the curated psa-free-total-ratio ValueSet; specimen Serum/Plasma."
* code from https://interpolar.example/fhir/ValueSet/psa-free-total-ratio (required)
* value[x] only Quantity
* valueQuantity.unit = "%"  // expected unit
* specimen only Reference(Specimen)  // Serum/Plasma
