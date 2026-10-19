# Full Branch Diff — Active Concepts

- A = `MAIN/LOINC/2025-09-21` @ `http://browser.loincsnomed.org/snowstorm/snomed-ct`
- B = `MAIN/SNOMEDCT-LOINC/2026-03-21` @ `http://localhost:8090`

| Metric | Count |
|---|---:|
| Active in A | 416,815 |
| Active in B | 423,857 |
| Only in A (removed in B) | 1,539 |
| Only in B (added in B)   | 8,581 |
| Active in both           | 415,276 |
| FSN changed on shared    | 2,655 |

## Removed concepts, grouped by module (A side)

| moduleId | count |
|---|---:|
| `900000000000207008` | 1,528 |
| `11010000107` | 10 |
| `900000000000012004` | 1 |

## Added concepts, grouped by module (B side)

| moduleId | count |
|---|---:|
| `900000000000207008` | 4,712 |
| `11010000107` | 3,862 |
| `900000000000012004` | 7 |

## Sample: added in International module (`900000000000207008`)

_4,712 total_

- `1000061000202103` — Liothyronine hydrochloride (substance)
- `1000071000202107` — Metoclopramide hydrochloride monohydrate (substance)
- `1000201000202107` — Flucloxacillin sodium monohydrate (substance)
- `1000311000202102` — Prothipendyl hydrochloride (substance)
- `1000341000202101` — Arctostaphylos uva-ursi extract (substance)
- `1000421000202100` — Ketobemidone hydrochloride (substance)
- `1000631000202101` — Lithium orotate (substance)
- `1000701000112100` — Breast examination abnormal (finding)
- `1000741000202102` — Levomethadone hydrochloride (substance)
- `1000771000202105` — Heavy magnesium oxide (substance)
- `1000791000202109` — Flupirtine (substance)
- `1000821000202102` — Clenbuterol hydrochloride (substance)
- `1000841000202106` — Fusidic acid hemihydrate (substance)
- `1000931000202106` — Diquafosol tetrasodium (substance)
- `1000981000202105` — Dixyrazine (substance)

## Sample: added in LOINC Extension module (`11010000107`)

_3,862 total_

- `1381232009` — Antigen of amyloid beta peptide (substance)
- `1381234005` — Antigen of amyloid-beta precursor protein (substance)
- `1381235006` — Antigen of alpha-crystallin B chain (substance)
- `1381236007` — Antigen of muscle specific actin (substance)
- `1381237003` — Antigen of smooth muscle actin (substance)
- `1381238008` — Antigen of ATP-binding cassette sub-family D member 1 (substance)
- `1381239000` — Antigen of phosphoRAC-alpha serine/threonine-protein kinase (substance)
- `1381240003` — Antigen of laminin subunit alpha-2 (substance)
- `1381241004` — Antigen of alpha-synuclein (substance)
- `1381243001` — Antigen of ALK tyrosine kinase receptor (substance)
- `1381244007` — Antigen of androgen receptor (substance)
- `1381245008` — Antigen of annexin A1 (substance)
- `1381246009` — Antigen of arginase-1 (substance)
- `1381247000` — Antigen of G1/S-specific cyclin-D1 (substance)
- `1381248005` — Antigen of B-cell lymphoma/leukemia 10 (substance)

## Sample: removed in International module (`900000000000207008`)

_1,528 total_

- `1004085005` — Injection of filling material into eyelid (procedure)
- `1010454006` — Retrograde pyelography of left renal pelvis with contrast (procedure)
- `1010455007` — Retrograde pyelography of right renal pelvis with contrast (procedure)
- `102784005` — Beta-N-acetylhexosaminidase A (substance)
- `102785006` — Beta-N-acetylhexosaminidase B (substance)
- `102863008` — Urinary crystal, magnesium ammonium phosphate (finding)
- `102931001` — Fear of heart attack (finding)
- `103062007` — Ectopic chorionic gonadotropin secretion (substance)
- `103534005` — Coccidian parasite (navigational concept)
- `10354000` — Somantin (substance)
- `104077008` — Blood product reservation, release, transfusion or disposition (navigational concept)
- `104497009` — Allo-tetrahydrocortisol measurement (procedure)
- `104683007` — Gastrin challenge tests (procedure)
- `105448009` — Sickness in family (finding)
- `105506000` — Dependence on seeing eye dog (finding)

## Sample: removed in LOINC Extension module (`11010000107`)

_10 total_

- `125521010000104` — Presence of beta-lactoglobulin specific immunoglobulin E in serum at point in time by radioallergosorbent testing (observable entity)
- `211361010000109` — Arbitrary concentration of beta-lactoglobulin specific immunoglobulin E in serum at point in time (observable entity)
- `486731010000109` — Presence or identity of Clostridium botulinum toxin in specimen at point in time by Endopep-MS (observable entity)
- `538181010000106` — Mass ratio of 11-ketoandrosterone to creatinine in urine in 24 hours (observable entity)
- `538191010000109` — Mass ratio of 11-ketoetiocholanolone to creatinine in urine in 24 hours (observable entity)
- `605191010000102` — Mass rate of excretion of 11-ketoandrosterone in 24 hours in urine (observable entity)
- `605201010000104` — Mass rate of excretion of 11-ketoetiocholanolone in 24 hours in urine (observable entity)
- `760951010000108` — Susceptibility to delafloxacin in microbial isolate at point in time (observable entity)
- `761411010000106` — Susceptibility to delafloxacin in microbial isolate at point in time by MIC (observable entity)
- `762241010000103` — Susceptibility to delafloxacin in microbial isolate at point in time by gradient strip susceptibility test (observable entity)

## Sample: FSN changed (first 25)

| conceptId | A FSN | B FSN |
|---|---|---|
| `1055246005` | Entire bone of distal phalanx of all digits of hand (body structure) | All entire distal phalanges of hand (body structure) |
| `178591005` | Revisional anterior decompression operation on cervical spinal cord and fusion (procedure) | Revision of anterior decompression of cervical spinal cord and fusion of cervical spine joint (procedure) |
| `96181010000103` | Mass concentration of zolpidem in saliva at point in time by confirmatory (observable entity) | Mass concentration of zolpidem in saliva at point in time by confirmatory technique (observable entity) |
| `738772006` | Kazachstania pintolopesii (organism) | Arxiozyma pintolopesii (organism) |
| `525091010000101` | Number fraction of eosinophil to leukocyte in nose at point in time (observable entity) | Number fraction of eosinophilic granulocytic cell to leukocyte in nose at point in time (observable entity) |
| `536751010000102` | Duration of intrinsic pathway coagulation process at point in time in platelet poor plasma by coagulation baseline (observable entity) | Duration of coagulation at point in time in platelet poor plasma by surface induced coagulation using blood coagulation analyzer baseline (observable entity) |
| `283355005` | Laceration of oral cavity (disorder) | Laceration of internal part of mouth (disorder) |
| `10676351000119103` | Moderate persistent asthma controlled (finding) | Moderate persistent asthma controlled (disorder) |
| `159411010000107` | Number concentration of basophil in body fluid at point in time (observable entity) | Number concentration of basophilic granulocytic cell in body fluid at point in time (observable entity) |
| `179800000` | Revision open intra-articular prosthetic augmentation intra-articular ligament (procedure) | Revision open augmentation of intra-articular ligament using intra-articular prosthetic ligament (procedure) |
| `203278004` | Tuberculosis of bones of shoulder region (disorder) | Tuberculosis of bone of shoulder girdle and/or proximal humerus (disorder) |
| `194821010000105` | Presence of tetrahydrocannabinol in urine at point in time by confirmatory (observable entity) | Presence of tetrahydrocannabinol in urine at point in time by confirmatory technique (observable entity) |
| `617981010000105` | Mass ratio of tizanidine to creatinine in urine at point in time by confirmatory (observable entity) | Mass ratio of tizanidine to creatinine in urine at point in time by confirmatory technique (observable entity) |
| `504491010000104` | Susceptibility to clofazimine in microbial isolate at point in time by method for Slow-growing mycobacteria (observable entity) | Susceptibility to clofazimine in microbial isolate at point in time by method for slow growing mycobacteria (observable entity) |
| `539211010000100` | Susceptibility to emtricitabine in microbial isolate at point in time by genotype determination (observable entity) | Susceptibility to emtricitabine in microbial isolate at point in time by genotyping (observable entity) |
| `745901010000105` | Number fraction of cell positive for CD103 antigen to cell in cerebrospinal fluid at point in time (observable entity) | Number fraction of CD103+ cell to cell in cerebrospinal fluid at point in time (observable entity) |
| `711311010000104` | Arbitrary concentration of gliadin antibody, IgG in serum or plasma at point in time by immunoassay (observable entity) | Arbitrary concentration of gliadin IgG in serum or plasma at point in time by immunoassay (observable entity) |
| `720341010000100` | Measurement of Influenza B virus antigen in nasopharyngeal (observable entity) | Measurement of Influenza B virus antigen in nasopharynx (observable entity) |
| `760211010000101` | Mass concentration of cannabinol in plasma or serum or whole blood at point in time by confirmatory (observable entity) | Mass concentration of cannabinol in plasma or serum or whole blood at point in time by confirmatory technique (observable entity) |
| `236021010000102` | Presence of benzoylecgonine in urine at point in time by confirmatory (observable entity) | Presence of benzoylecgonine in urine at point in time by confirmatory technique (observable entity) |
| `760701010000106` | Presence or identity of human parainfluenza viruses in Cornea/Conjunctiva at point in time by organism specific culture (observable entity) | Presence or identity of human parainfluenza virus in Cornea/Conjunctiva at point in time by organism specific culture (observable entity) |
| `239097004` | Gangrene of newborn (disorder) | Neonatal gangrene (disorder) |
| `188191010000105` | Number concentration of cell positive for CD34 antigen in body fluid at point in time (observable entity) | Number concentration of CD34+ cell in body fluid at point in time (observable entity) |
| `232761010000108` | Presence of triazolam in umbilical cord tissue at point in time by confirmatory (observable entity) | Presence of triazolam in umbilical cord tissue at point in time by confirmatory technique (observable entity) |
| `169867004` | Baby birth weight equal to or greater than 96 percent (over 4499g) (finding) | Baby birth weight equal to or greater than 96 percent, over 4499 grams (finding) |