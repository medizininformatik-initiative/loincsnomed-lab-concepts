// Worked example for the LOINC Ontology proposal. Same case as the module's own
// examples (Patient/111, Encounter/555, Specimen/4999 = venous blood, order and
// report of the renal diagnostics case) so that it slots into the existing bundle.
Instance: mii-exa-labor-loinc-ontology-hemoglobin
InstanceOf: MII_PR_Labor_LOINC_Ontology_Hemoglobin_Standard
Title: "Laboratory result: hemoglobin (LOINC Ontology profile)"
Description: "A quantitative hemoglobin result conforming to the derived profile MII_PR_Labor_LOINC_Ontology_Hemoglobin_Standard: Observation.code carries LOINC 718-7, a member of the computed ValueSet; everything else is as in the module's creatinine example."
Usage: #example
* insert TestDataLabel
* insert MetaProfile(https://www.medizininformatik-initiative.de/fhir/core/modul-labor/StructureDefinition/mii-pr-labor-loinc-ontology-hemoglobin-standard)
* identifier[analyseBefundCode].type = $v2-0203#OBI
* identifier[analyseBefundCode].system = "https://example.org/fhir/sid/test-lab-results"
* identifier[analyseBefundCode].value = "718-7_1234567890"
* identifier[analyseBefundCode].assigner.identifier.system = "https://www.medizininformatik-initiative.de/fhir/core/CodeSystem/core-location-identifier"
* identifier[analyseBefundCode].assigner.identifier.value = "DIZ-ID"
* basedOn.reference = "ServiceRequest/mii-exa-labor-laboranforderung"
* status = #final
* category[observation-category].coding[0] = $observation-category#laboratory "Laboratory"
* category[observation-category].coding[1] = $loinc#26436-6 "Laboratory studies (set)"
* code = $loinc#718-7 "Hemoglobin [Mass/volume] in Blood"
* code.text = "Hämoglobin"
* subject.reference = "Patient/111"
* encounter.reference = "Encounter/555"
* effectiveDateTime = "2018-11-20T08:00:00+01:00"
* effectiveDateTime.extension[QuelleKlinischesBezugsdatum].url = "https://www.medizininformatik-initiative.de/fhir/core/modul-labor/StructureDefinition/QuelleKlinischesBezugsdatum"
* effectiveDateTime.extension[QuelleKlinischesBezugsdatum].valueCoding = $sct#399445004 "Specimen collection date"
* issued = "2018-11-20T14:30:00+01:00"
* performer.reference = "Organization/7772"
* performer.identifier.system = "https://example.org/fhir/sid/test-organizations"
* performer.identifier.value = "7772"
* performer.display = "Zentrallabor Beispielklinikum"
* specimen.reference = "Specimen/4999"
* valueQuantity = 14.2 'g/dL' "g/dL"
* valueQuantity.value.extension[quantityPrecision].valueInteger = 1
* interpretation = $v3-ObservationInterpretation#N
* referenceRange.low = 12.0 'g/dL' "g/dL"
* referenceRange.high = 16.0 'g/dL' "g/dL"
* referenceRange.type = $referencerange-meaning#normal "Normal Range"
