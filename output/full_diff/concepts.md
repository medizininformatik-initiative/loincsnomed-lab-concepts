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
| `100041010000104` | Presence of 6-O-monoacetylmorphine in urine at point in time by confirmatory (observable entity) | Presence of 6-O-monoacetylmorphine in urine at point in time by confirmatory technique (observable entity) |
| `100251010000109` | Presence of Albumin/Creatinine in urine at point in time by test strip (observable entity) | Mass ratio of albumin to creatinine in urine at point in time by test strip (observable entity) |
| `100331010000105` | Presence of methamphetamine in umbilical cord tissue at point in time by confirmatory (observable entity) | Presence of methamphetamine in umbilical cord tissue at point in time by confirmatory technique (observable entity) |
| `1003442001` | Synostosis of bilateral humerus, radius and ulna (disorder) | Congenital synostosis of bilateral humerus, radius, and ulna (disorder) |
| `100411010000109` | Presence of tetrahydrocannabinol in blood at point in time by confirmatory (observable entity) | Presence of tetrahydrocannabinol in blood at point in time by confirmatory technique (observable entity) |
| `100601010000108` | Number concentration of basophil in blood at point in time (observable entity) | Number concentration of basophilic granulocytic cell in blood at point in time (observable entity) |
| `100611010000106` | Number concentration of cell positive for CD56 antigen in blood at point in time (observable entity) | Number concentration of CD56+ cell in blood at point in time (observable entity) |
| `100711010000100` | Presence of dextromethorphan in urine at point in time by confirmatory (observable entity) | Presence of dextromethorphan in urine at point in time by confirmatory technique (observable entity) |
| `100981010000107` | Presence of Factor VII antibody in platelet poor plasma at point in time by coagulation (observable entity) | Presence of Factor VII antibody in platelet poor plasma at point in time using blood coagulation analyzer (observable entity) |
| `101031010000100` | Presence of hydromorphone in saliva at point in time by confirmatory (observable entity) | Presence of hydromorphone in saliva at point in time by confirmatory technique (observable entity) |
| `101351010000107` | Presence of benzoylecgonine in serum or plasma at point in time by confirmatory (observable entity) | Presence of benzoylecgonine in serum or plasma at point in time by confirmatory technique (observable entity) |
| `101451010000102` | Mass concentration of flurazepam in body fluid at point in time by confirmatory (observable entity) | Mass concentration of flurazepam in body fluid at point in time by confirmatory technique (observable entity) |
| `101711000119105` | Glomerulonephritis co-occurrent and due to antineutrophil cytoplasmic antibody positive vasculitis (disorder) | Glomerulonephritis due to antineutrophil cytoplasmic antibody positive vasculitis (disorder) |
| `101861010000102` | Mass concentration of methylephedrine in serum or plasma at point in time by confirmatory (observable entity) | Mass concentration of methylephedrine in serum or plasma at point in time by confirmatory technique (observable entity) |
| `102381010000105` | Arbitrary concentration of human chorionic gonadotropin, beta subunit in body fluid at point in time (observable entity) | Arbitrary concentration of human chorionic gonadotropin beta subunit in body fluid at point in time (observable entity) |
| `102631010000101` | Number concentration of basophil in cerebrospinal fluid at point in time (observable entity) | Number concentration of basophilic granulocytic cell in cerebrospinal fluid at point in time (observable entity) |
| `102671010000103` | Mass concentration of clonazepam in body fluid at point in time by confirmatory (observable entity) | Mass concentration of clonazepam in body fluid at point in time by confirmatory technique (observable entity) |
| `102711010000104` | Presence of tetrahydrocannabinol in gastric fluid at point in time by confirmatory (observable entity) | Presence of tetrahydrocannabinol in gastric fluid at point in time by confirmatory technique (observable entity) |
| `102841010000105` | Mass concentration of ziprasidone in urine at point in time by confirmatory (observable entity) | Mass concentration of ziprasidone in urine at point in time by confirmatory technique (observable entity) |
| `103093008` | Antigen of Human immunodeficiency virus protein 24 (substance) | Antigen of human immunodeficiency virus protein 24 (substance) |
| `103131010000103` | Mass concentration of estriol, unconjugated in amniotic fluid at point in time (observable entity) | Mass concentration of unconjugated estriol in amniotic fluid at point in time (observable entity) |
| `103514009` | Chlamydophila pneumoniae (organism) | Chlamydia pneumoniae (organism) |
| `103571010000108` | Presence of cell positive for CD14 antigen in blood at point in time (observable entity) | Presence of CD14+ cell in blood at point in time (observable entity) |
| `103751010000107` | Mass concentration of butabarbital in urine at point in time by confirmatory (observable entity) | Mass concentration of butabarbital in urine at point in time by confirmatory technique (observable entity) |
| `104351010000109` | Presence of Borrelia burgdorferi 66-kD antibody in cerebrospinal fluid at point in time by immunoblot assay (observable entity) | Presence of Borrelia burgdorferi 66 kDa antibody in cerebrospinal fluid at point in time by immunoblot assay (observable entity) |