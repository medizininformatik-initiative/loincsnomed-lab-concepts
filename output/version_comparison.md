# ECL Version Comparison

**Targets:** local-2026-03-21, local-2026-10-21

| Concept | Query | local-2026-03-21 | local-2026-10-21 | Only A | Only B | Both |
|---|---|---|---|---|---|---|
| erythrocytes | Refined Query V2 (Property-Specific: Number Concentration) | 4 | 4 | 0 | 0 | 4 |
| hba1c | Refined Query V2 (Mass Fraction Property) | 6 | 6 | 0 | 0 | 6 |
| hematocrit | Refined Query V2 (Property-Specific: Volume Fraction) | 0 | 0 | 0 | 0 | 0 |
| hemoglobin | Refined Query V2 (Excl. Ratio & Plasma) | 32 | 33 | 0 | 1 | 32 |
| ldh | Refined Query V2 (Universal Measurement Property, incl. isoenzymes) | 21 | 22 | 0 | 1 | 21 |
| ldh | Refined Query V2 (Total LDH only, exact component) | 4 | 4 | 0 | 0 | 4 |
| ldh | Refined Query V2 (Excl. Ratio) | 20 | 21 | 0 | 1 | 20 |
| ldh | Refined Query V2 (Ratio Properties) | 1 | 1 | 0 | 0 | 1 |
| leukocytes | Refined Query V2 (Property-Specific: Number Concentration) | 11 | 11 | 0 | 0 | 11 |
| mch | Refined Query V2 (Entitic Mass Property) | 2 | 2 | 0 | 0 | 2 |
| mchc | Refined Query V2 (Pre-coordinated Parent Descendants) | 2 | 2 | 0 | 0 | 2 |
| mcv | Refined Query V2 (Pre-coordinated Parent Descendants) | 2 | 2 | 0 | 0 | 2 |
| methemoglobin | Refined Query V2 Quantitative (Measurement Properties) | 12 | 13 | 0 | 1 | 12 |
| methemoglobin | Refined Query V2 Ratio (Ratio Properties) | 0 | 0 | 0 | 0 | 0 |
| nitrite_urine | Refined Query V2 Quantitative (Measurement Properties) | 2 | 5 | 0 | 3 | 2 |
| nitrite_urine | Refined Query V2 Qualitative (Presence Properties) | 3 | 0 | 3 | 0 | 0 |
| platelets | Refined Query V2 (Property-Specific: Number Concentration, Excl. Cord & Plasma) | 7 | 7 | 0 | 0 | 7 |
| potassium | Refined Query V2 (Universal Measurement Property) | 17 | 17 | 0 | 0 | 17 |
| psa | Refined Query V2 (Universal Measurement Property) | 14 | 14 | 0 | 0 | 14 |
| psa | Refined Query V2 (Excl. Ratio) | 14 | 14 | 0 | 0 | 14 |
| psa | Refined Query V2 (Ratio Properties) | 0 | 0 | 0 | 0 | 0 |

## Per-query detail

### erythrocytes — Refined Query V2 (Property-Specific: Number Concentration)
```
<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = 41898006 |Erythrocyte (cell)|, << 704327008 |Direct site (attribute)| = << 119297000 |Blood specimen (specimen)|, << 370130000 |Property (attribute)| = << 118550005 |Number concentration (property) (qualifier value)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (0): 
- **In both**: 4

### hba1c — Refined Query V2 (Mass Fraction Property)
```
<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = 733830002 |Glycated hemoglobin-A1c (substance)|, << 370130000 |Property (attribute)| = << 118542001 |Mass fraction (property) (qualifier value)|, << 704327008 |Direct site (attribute)| = << 119297000 |Blood specimen (specimen)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (0): 
- **In both**: 6

### hematocrit — Refined Query V2 (Property-Specific: Volume Fraction)
```
<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = 41898006 |Erythrocyte (cell)|, << 704327008 |Direct site (attribute)| = << 119297000 |Blood specimen (specimen)|, << 370130000 |Property (attribute)| = << 118586006 |Volume fraction (property) (qualifier value)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (0): 
- **In both**: 0

### hemoglobin — Refined Query V2 (Excl. Ratio & Plasma)
```
<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = 38082009 |Hemoglobin (substance)|, << 704327008 |Direct site (attribute)| = << 119297000 |Blood specimen (specimen)|, << 370130000 |Property (attribute)| = << 685451010000100 |Measurement property (qualifier value)|, << 370130000 |Property (attribute)| != << 118586006 |Ratio (property) (qualifier value)|, << 704327008 |Direct site (attribute)| != << 119361006 |Plasma specimen (specimen)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (1): 186111010000103
- **In both**: 32

### ldh — Refined Query V2 (Universal Measurement Property, incl. isoenzymes)
```
<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = << 259319003 |Lactate dehydrogenase (substance)|, << 704327008 |Direct site (attribute)| = << 119297000 |Blood specimen (specimen)|, << 370130000 |Property (attribute)| = << 685451010000100 |Measurement property (qualifier value)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (1): 188471010000100
- **In both**: 21

### ldh — Refined Query V2 (Total LDH only, exact component)
```
<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = 259319003 |Lactate dehydrogenase (substance)|, << 704327008 |Direct site (attribute)| = << 119297000 |Blood specimen (specimen)|, << 370130000 |Property (attribute)| = << 685451010000100 |Measurement property (qualifier value)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (0): 
- **In both**: 4

### ldh — Refined Query V2 (Excl. Ratio)
```
<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = << 259319003 |Lactate dehydrogenase (substance)|, << 704327008 |Direct site (attribute)| = << 119297000 |Blood specimen (specimen)|, << 370130000 |Property (attribute)| = << 685451010000100 |Measurement property (qualifier value)|, << 370130000 |Property (attribute)| != << 118586006 |Ratio (property) (qualifier value)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (1): 188471010000100
- **In both**: 20

### ldh — Refined Query V2 (Ratio Properties)
```
<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = << 259319003 |Lactate dehydrogenase (substance)|, << 704327008 |Direct site (attribute)| = << 119297000 |Blood specimen (specimen)|, << 370130000 |Property (attribute)| = << 118586006 |Ratio (property) (qualifier value)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (0): 
- **In both**: 1

### leukocytes — Refined Query V2 (Property-Specific: Number Concentration)
```
<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = 52501007 |Leukocyte (cell)|, << 370130000 |Property (attribute)| = << 118550005 |Number concentration (property) (qualifier value)|, << 704327008 |Direct site (attribute)| = << 119297000 |Blood specimen (specimen)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (0): 
- **In both**: 11

### mch — Refined Query V2 (Entitic Mass Property)
```
<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = << 38082009 |Hemoglobin (substance)|, << 370130000 |Property (attribute)| = << 118535001 |Entitic mass (property) (qualifier value)|, << 704327008 |Direct site (attribute)| = << 119351004 |Erythrocyte specimen (specimen)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (0): 
- **In both**: 2

### mchc — Refined Query V2 (Pre-coordinated Parent Descendants)
```
<< 521371010000101 |Mean cell hemoglobin concentration (observable entity)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (0): 
- **In both**: 2

### mcv — Refined Query V2 (Pre-coordinated Parent Descendants)
```
<< 525321010000100 |Mean cell volume (observable entity)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (0): 
- **In both**: 2

### methemoglobin — Refined Query V2 Quantitative (Measurement Properties)
```
<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = << 27840003 |Methemoglobin (substance)|, << 704327008 |Direct site (attribute)| = << 119297000 |Blood specimen (specimen)|, << 370130000 |Property (attribute)| = << 685451010000100 |Measurement property (qualifier value)|, << 370130000 |Property (attribute)| != << 118586006 |Ratio (property) (qualifier value)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (1): 112391010000106
- **In both**: 12

### methemoglobin — Refined Query V2 Ratio (Ratio Properties)
```
<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = << 27840003 |Methemoglobin (substance)|, << 704327008 |Direct site (attribute)| = << 119297000 |Blood specimen (specimen)|, << 370130000 |Property (attribute)| = << 118586006 |Ratio (property) (qualifier value)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (0): 
- **In both**: 0

### nitrite_urine — Refined Query V2 Quantitative (Measurement Properties)
```
<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = 31528005 |Nitrite salt (substance)|, << 370130000 |Property (attribute)| = << 685451010000100 |Measurement property (qualifier value)|, << 704327008 |Direct site (attribute)| = << 122575003 |Urine specimen (specimen)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (3): 194401010000100, 209111010000106, 45931010000103
- **In both**: 2

### nitrite_urine — Refined Query V2 Qualitative (Presence Properties)
```
<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = 31528005 |Nitrite salt (substance)|, << 370130000 |Property (attribute)| = << 705057003 |Presence (property) (qualifier value)|, << 704327008 |Direct site (attribute)| = << 122575003 |Urine specimen (specimen)|
```
- **Only in local-2026-03-21** (3): 194401010000100, 209111010000106, 45931010000103
- **Only in local-2026-10-21** (0): 
- **In both**: 0

### platelets — Refined Query V2 (Property-Specific: Number Concentration, Excl. Cord & Plasma)
```
<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = 16378004 |Platelet (cell)|, << 370130000 |Property (attribute)| = << 118550005 |Number concentration (property) (qualifier value)|, << 704327008 |Direct site (attribute)| = << 119297000 |Blood specimen (specimen)|, << 704327008 |Direct site (attribute)| != << 122556008 |Cord blood specimen (specimen)|, << 704327008 |Direct site (attribute)| != << 119361006 |Plasma specimen (specimen)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (0): 
- **In both**: 7

### potassium — Refined Query V2 (Universal Measurement Property)
```
<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = 304048005 |Potassium electrolyte (substance)|, << 370130000 |Property (attribute)| = << 685451010000100 |Measurement property (qualifier value)|, << 704327008 |Direct site (attribute)| = << 119297000 |Blood specimen (specimen)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (0): 
- **In both**: 17

### psa — Refined Query V2 (Universal Measurement Property)
```
<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = << 102687007 |Prostate specific antigen (substance)|, << 704327008 |Direct site (attribute)| = << 119297000 |Blood specimen (specimen)|, << 370130000 |Property (attribute)| = << 685451010000100 |Measurement property (qualifier value)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (0): 
- **In both**: 14

### psa — Refined Query V2 (Excl. Ratio)
```
<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = << 102687007 |Prostate specific antigen (substance)|, << 704327008 |Direct site (attribute)| = << 119297000 |Blood specimen (specimen)|, << 370130000 |Property (attribute)| = << 685451010000100 |Measurement property (qualifier value)|, << 370130000 |Property (attribute)| != << 118586006 |Ratio (property) (qualifier value)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (0): 
- **In both**: 14

### psa — Refined Query V2 (Ratio Properties)
```
<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = << 102687007 |Prostate specific antigen (substance)|, << 704327008 |Direct site (attribute)| = << 119297000 |Blood specimen (specimen)|, << 370130000 |Property (attribute)| = << 118586006 |Ratio (property) (qualifier value)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (0): 
- **In both**: 0
