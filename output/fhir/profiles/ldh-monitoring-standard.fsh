Profile: LdhMonitoringStandard
Parent: $KDSLab
Id: ldh-monitoring-standard
Title: "LDH (total) monitoring in serum/plasma"
Description: "Observation profile for LDH (total) monitoring in serum/plasma (standard test). code bound to the curated ldh-monitoring-standard ValueSet; specimen Serum/Plasma."
* code from https://interpolar.example/fhir/ValueSet/ldh-monitoring-standard (required)
* value[x] only Quantity
* valueQuantity.unit = "U/L"  // expected unit
* specimen only Reference(Specimen)  // Serum/Plasma
