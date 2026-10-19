# ECL Version Comparison

**Targets:** public-2025-09-21, local-2026-03-21

| Concept | Query | public-2025-09-21 | local-2026-03-21 | Only A | Only B | Both |
|---|---|---|---|---|---|---|
| ldh | Refined Query V2 (Universal Measurement Property, incl. isoenzymes) | 21 | 21 | 0 | 0 | 21 |
| ldh | Refined Query V2 (Total LDH only, exact component) | 4 | 4 | 0 | 0 | 4 |
| ldh | Refined Query V2 (Excl. Ratio) | 15 | 20 | 0 | 5 | 15 |
| ldh | Refined Query V2 (Ratio Properties) | 6 | 1 | 5 | 0 | 1 |

## Per-query detail

### ldh — Refined Query V2 (Universal Measurement Property, incl. isoenzymes)
```
<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = << 259319003 |Lactate dehydrogenase (substance)|, << 704327008 |Direct site (attribute)| = << 119297000 |Blood specimen (specimen)|, << 370130000 |Property (attribute)| = << 685451010000100 |Measurement property (qualifier value)|
```
- **Only in public-2025-09-21** (0): 
- **Only in local-2026-03-21** (0): 
- **In both**: 21

### ldh — Refined Query V2 (Total LDH only, exact component)
```
<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = 259319003 |Lactate dehydrogenase (substance)|, << 704327008 |Direct site (attribute)| = << 119297000 |Blood specimen (specimen)|, << 370130000 |Property (attribute)| = << 685451010000100 |Measurement property (qualifier value)|
```
- **Only in public-2025-09-21** (0): 
- **Only in local-2026-03-21** (0): 
- **In both**: 4

### ldh — Refined Query V2 (Excl. Ratio)
```
<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = << 259319003 |Lactate dehydrogenase (substance)|, << 704327008 |Direct site (attribute)| = << 119297000 |Blood specimen (specimen)|, << 370130000 |Property (attribute)| = << 685451010000100 |Measurement property (qualifier value)|, << 370130000 |Property (attribute)| != << 118586006 |Ratio (property) (qualifier value)|
```
- **Only in public-2025-09-21** (0): 
- **Only in local-2026-03-21** (5): 515391010000108, 515511010000109, 515651010000106, 515781010000109, 515861010000109
- **In both**: 15

### ldh — Refined Query V2 (Ratio Properties)
```
<< 363787002 |Observable entity (observable entity)| : << 246093002 |Component (attribute)| = << 259319003 |Lactate dehydrogenase (substance)|, << 704327008 |Direct site (attribute)| = << 119297000 |Blood specimen (specimen)|, << 370130000 |Property (attribute)| = << 118586006 |Ratio (property) (qualifier value)|
```
- **Only in public-2025-09-21** (5): 515391010000108, 515511010000109, 515651010000106, 515781010000109, 515861010000109
- **Only in local-2026-03-21** (0): 
- **In both**: 1
