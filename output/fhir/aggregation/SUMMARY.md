# Comprehensive per-analyte ValueSets (use-case aggregation)

Target: `local-2026-10-21` (MAIN/SNOMEDCT-LOINC/2026-10-21)

One ValueSet per analyte × bucket. Cells = concepts (with LOINC).

| Analyte | Pool ECL | complete | quantitative | quantitative_convertible | qualitative | semiquantitative | panel_order | unclassified |
|---|---|---|---|---|---|---|---|---|
| erythrocytes | `<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = 41898006 |Erythrocyte (cell)|` | 107 (106) | 88 (88) | 52 (52) | 17 (16) | 2 (2) | 0 (0) | 0 |
| hba1c | `<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = 733830002 |Glycated hemoglobin-A1c (substance)|` | 10 (8) | 10 (8) | 3 (1) | 0 (0) | 0 (0) | 0 (0) | 0 |
| hematocrit | `<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = 41898006 |Erythrocyte (cell)|` | 107 (106) | 88 (88) | 52 (52) | 17 (16) | 2 (2) | 0 (0) | 0 |
| hemoglobin | `<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = 38082009 |Hemoglobin (substance)|` | 89 (89) | 57 (57) | 40 (40) | 30 (30) | 2 (2) | 0 (0) | 0 |
| ldh | `<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = << 259319003 |Lactate dehydrogenase (substance)|` | 79 (79) | 77 (77) | 41 (41) | 2 (2) | 0 (0) | 0 (0) | 0 |
| leukocytes | `<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = 52501007 |Leukocyte (cell)|` | 161 (158) | 123 (123) | 86 (86) | 34 (33) | 2 (2) | 2 (0) | 0 |
| mch | `<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = << 38082009 |Hemoglobin (substance)|` | 296 (293) | 180 (177) | 59 (57) | 114 (114) | 2 (2) | 0 (0) | 0 |
| mchc | `<< 521371010000101 |Mean cell hemoglobin concentration (observable entity)|` | 2 (2) | 2 (2) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 |
| mcv | `<< 525321010000100 |Mean cell volume (observable entity)|` | 2 (2) | 2 (2) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 |
| methemoglobin | `<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = << 27840003 |Methemoglobin (substance)|` | 17 (17) | 15 (15) | 3 (3) | 2 (2) | 0 (0) | 0 (0) | 0 |
| nitrite_urine | `<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = 31528005 |Nitrite salt (substance)|` | 9 (9) | 5 (5) | 5 (5) | 3 (3) | 1 (1) | 0 (0) | 0 |
| platelets | `<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = 16378004 |Platelet (cell)|` | 19 (19) | 17 (17) | 15 (15) | 2 (2) | 0 (0) | 0 (0) | 0 |
| potassium | `<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = 304048005 |Potassium electrolyte (substance)|` | 57 (57) | 57 (57) | 42 (42) | 0 (0) | 0 (0) | 0 (0) | 0 |
| psa | `<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = << 102687007 |Prostate specific antigen (substance)|` | 37 (37) | 36 (36) | 26 (26) | 1 (1) | 0 (0) | 0 (0) | 0 |

`complete` carries the pool ECL as an intensional SNOMED include; the other buckets are Scale-type/Property classifications (see config/aggregation_profiles.json) and list the rule in their description.
