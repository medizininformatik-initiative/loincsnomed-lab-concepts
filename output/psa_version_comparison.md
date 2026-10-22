# ECL Version Comparison

**Targets:** local-2026-03-21, local-2026-10-21

| Concept | Query | local-2026-03-21 | local-2026-10-21 | Only A | Only B | Both |
|---|---|---|---|---|---|---|
| psa | Refined Query V2 (Universal Measurement Property) | 14 | 14 | 0 | 0 | 14 |
| psa | Refined Query V2 (Excl. Ratio) | 14 | 14 | 0 | 0 | 14 |
| psa | Refined Query V2 (Ratio Properties) | 0 | 0 | 0 | 0 | 0 |

## Per-query detail

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
