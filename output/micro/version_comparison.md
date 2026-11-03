# ECL Version Comparison

**Targets:** local-2026-03-21, local-2026-10-21

| Concept | Query | local-2026-03-21 | local-2026-10-21 | Only A | Only B | Both |
|---|---|---|---|---|---|---|
| micro_allgemeine_bestimmung | General determination — organism identity, any technique | 756 | 780 | 0 | 24 | 756 |
| micro_allgemeine_bestimmung | General determination — method-neutral identity codes | 86 | 88 | 0 | 2 | 86 |
| micro_allgemeine_bestimmung | Typing — type of an organism (serotype, genotype, biotype) | 22 | 22 | 0 | 0 | 22 |
| micro_allgemeine_kultur | General culture — organism identity by culture technique | 563 | 578 | 0 | 15 | 563 |
| micro_allgemeine_kultur | Targeted culture — threshold presence of a named organism by culture technique | 203 | 204 | 0 | 1 | 203 |
| micro_allgemeine_kultur | Everything by culture technique (upper bound) | 772 | 788 | 0 | 16 | 772 |
| micro_antigen_antikoerper_quantitativ | Serology quantitative — concentration of a pathogen antibody or antigen | 1770 | 1813 | 0 | 43 | 1770 |
| micro_antigen_antikoerper_quantitativ | Serology qualitative — threshold presence of a pathogen antibody or antigen | 2769 | 2796 | 0 | 27 | 2769 |
| micro_ct_wert | Ct value — threshold number of a microbial nucleic acid | 40 | 40 | 0 | 0 | 40 |
| micro_ct_wert | Ct value — all threshold-number observables (upper bound) | 44 | 45 | 0 | 1 | 44 |
| micro_empfindlichkeit | Phenotypic susceptibility — isolate, not genotyping | 1227 | 1230 | 0 | 3 | 1227 |
| micro_empfindlichkeit | Predicted susceptibility — by genotype determination technique | 81 | 81 | 0 | 0 | 81 |
| micro_empfindlichkeit | All susceptibility observables (upper bound) | 1345 | 1350 | 0 | 5 | 1345 |
| micro_keimzahl | Colony count — number concentration of an organism | 16 | 16 | 0 | 0 | 16 |
| micro_keimzahl | Colony count — with culture technique asserted | 4 | 4 | 0 | 0 | 4 |
| micro_mikroskopie | General microscopy — nominal finding by microscopy or staining technique | 376 | 383 | 0 | 7 | 376 |
| micro_mikroskopie | General microscopy — method-neutral 'finding in specimen' pattern | 355 | 357 | 0 | 2 | 355 |
| micro_mikroskopie | Specific microscopy — ordinal threshold presence by microscopy or staining technique | 316 | 331 | 1 | 16 | 315 |
| micro_molekulare_pathogenlast | Pathogen load — quantitative microbial nucleic acid, any technique | 397 | 401 | 0 | 4 | 397 |
| micro_molekulare_pathogenlast | Pathogen load — amplification technique asserted | 355 | 359 | 0 | 4 | 355 |
| micro_resistenzmechanismen | Resistant-organism detection — presence/identity of an antimicrobial resistant organism | 16 | 16 | 0 | 0 | 16 |
| micro_resistenzmechanismen | Resistant organism — any observable about a resistant organism (upper bound) | 16 | 16 | 0 | 0 | 16 |
| micro_spezifische_bestimmung | Nucleic-acid detection — any or no technique | 1922 | 2507 | 1 | 586 | 1921 |
| micro_spezifische_bestimmung | Nucleic-acid detection — amplification technique asserted | 1486 | 1524 | 0 | 38 | 1486 |
| micro_spezifische_bestimmung | Nucleic-acid detection — no technique modelled | 288 | 288 | 19 | 19 | 269 |
| micro_spezifische_bestimmung | Targeted culture detection — organism specific culture technique | 191 | 192 | 0 | 1 | 191 |
| micro_spezifische_bestimmung | Antigen detection — threshold presence of a microbial antigen | 898 | 899 | 0 | 1 | 898 |
| micro_titer | Titre — pathogen antibody titre | 1712 | 1716 | 0 | 4 | 1712 |
| micro_titer | Titre — all titre observables (upper bound) | 2186 | 2188 | 0 | 2 | 2186 |

## Per-query detail

### micro_allgemeine_bestimmung — General determination — organism identity, any technique
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 118584009 |Presence or identity (property) (qualifier value)|, 704319004 |Inheres in (attribute)| = << 410607006 |Organism (organism)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (24): 883831010000102, 883841010000105, 883941010000102, 884661010000105, 884671010000100, 884831010000104, 884841010000107, 884891010000100, 884901010000101, 884911010000103, 885001010000101, 885011010000103, 885031010000107, 885091010000106, 885141010000100, 885181010000109, 902161010000103, 902171010000108, 902181010000106, 902951010000103 …
- **In both**: 756

### micro_allgemeine_bestimmung — General determination — method-neutral identity codes
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 118584009 |Presence or identity (property) (qualifier value)|, 704319004 |Inheres in (attribute)| = << 410607006 |Organism (organism)|, [0..0] 246501002 |Technique (attribute)| = *
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (2): 902181010000106, 902971010000106
- **In both**: 86

### micro_allgemeine_bestimmung — Typing — type of an organism (serotype, genotype, biotype)
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 410656007 |Type (property) (qualifier value)|, 704319004 |Inheres in (attribute)| = << 410607006 |Organism (organism)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (0): 
- **In both**: 22

### micro_allgemeine_kultur — General culture — organism identity by culture technique
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 118584009 |Presence or identity (property) (qualifier value)|, 246501002 |Technique (attribute)| = << 703725008 |Culture technique (qualifier value)|, (704319004 |Inheres in (attribute)| = << 410607006 |Organism (organism)| OR 246093002 |Component (attribute)| = << 410607006 |Organism (organism)|)
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (15): 883841010000105, 883941010000102, 884661010000105, 884671010000100, 884831010000104, 884841010000107, 884891010000100, 884901010000101, 884911010000103, 885001010000101, 885011010000103, 885031010000107, 902961010000101, 903351010000109, 903361010000106
- **In both**: 563

### micro_allgemeine_kultur — Targeted culture — threshold presence of a named organism by culture technique
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118589004 |Threshold (property) (qualifier value)| OR 705057003 |Presence (property) (qualifier value)|), 246501002 |Technique (attribute)| = << 703725008 |Culture technique (qualifier value)|, (704319004 |Inheres in (attribute)| = << 410607006 |Organism (organism)| OR 246093002 |Component (attribute)| = << 410607006 |Organism (organism)|)
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (1): 884821010000102
- **In both**: 203

### micro_allgemeine_kultur — Everything by culture technique (upper bound)
```
<< 363787002 |Observable entity (observable entity)| : 246501002 |Technique (attribute)| = << 703725008 |Culture technique (qualifier value)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (16): 883841010000105, 883941010000102, 884661010000105, 884671010000100, 884821010000102, 884831010000104, 884841010000107, 884891010000100, 884901010000101, 884911010000103, 885001010000101, 885011010000103, 885031010000107, 902961010000101, 903351010000109, 903361010000106
- **In both**: 772

### micro_antigen_antikoerper_quantitativ — Serology quantitative — concentration of a pathogen antibody or antigen
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118569000 |Arbitrary concentration (property) (qualifier value)| OR 118539007 |Mass concentration (property) (qualifier value)| OR 118556004 |Substance concentration (property) (qualifier value)| OR 118550005 |Number concentration (property) (qualifier value)|), 246093002 |Component (attribute)| = (<< 312301006 |Infective organism antibody (substance)| OR << 116633006 |Microbial antigen (substance)|)
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (43): 734971010000101, 734981010000103, 734991010000100, 735001010000105, 735011010000108, 735021010000102, 735031010000104, 736331010000109, 736521010000103, 737311010000103, 737331010000107, 739861010000104, 739871010000109, 739881010000107, 739891010000105, 739901010000109, 739921010000101, 741441010000104, 741551010000101, 741591010000105 …
- **In both**: 1770

### micro_antigen_antikoerper_quantitativ — Serology qualitative — threshold presence of a pathogen antibody or antigen
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118589004 |Threshold (property) (qualifier value)| OR 705057003 |Presence (property) (qualifier value)|), 246093002 |Component (attribute)| = (<< 312301006 |Infective organism antibody (substance)| OR << 116633006 |Microbial antigen (substance)|)
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (27): 706781010000100, 706941010000107, 706961010000106, 706971010000101, 706991010000100, 707001010000106, 707021010000103, 707031010000100, 746071010000108, 746081010000106, 762721010000104, 763061010000103, 883971010000108, 883981010000106, 883991010000109, 884001010000102, 884011010000104, 884081010000109, 884091010000107, 884161010000102 …
- **In both**: 2769

### micro_ct_wert — Ct value — threshold number of a microbial nucleic acid
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 1268648001 |Threshold number (property) (qualifier value)|, 246093002 |Component (attribute)| = << 117174000 |Nucleic acid sequence with relative specificity for microorganism (substance)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (0): 
- **In both**: 40

### micro_ct_wert — Ct value — all threshold-number observables (upper bound)
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 1268648001 |Threshold number (property) (qualifier value)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (1): 903401010000103
- **In both**: 44

### micro_empfindlichkeit — Phenotypic susceptibility — isolate, not genotyping
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 118588007 |Susceptibility (property) (qualifier value)|, 704327008 |Direct site (attribute)| = << 119303007 |Microbial isolate specimen (specimen)|, [0..0] 246501002 |Technique (attribute)| = << 708060009 |Genotype determination technique (qualifier value)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (3): 903001010000108, 903161010000108, 903311010000108
- **In both**: 1227

### micro_empfindlichkeit — Predicted susceptibility — by genotype determination technique
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 118588007 |Susceptibility (property) (qualifier value)|, 246501002 |Technique (attribute)| = << 708060009 |Genotype determination technique (qualifier value)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (0): 
- **In both**: 81

### micro_empfindlichkeit — All susceptibility observables (upper bound)
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 118588007 |Susceptibility (property) (qualifier value)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (5): 903001010000108, 903011010000106, 903151010000106, 903161010000108, 903311010000108
- **In both**: 1345

### micro_keimzahl — Colony count — number concentration of an organism
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118550005 |Number concentration (property) (qualifier value)| OR 705056007 |Logarithmic number concentration (property) (qualifier value)|), (246093002 |Component (attribute)| = << 410607006 |Organism (organism)| OR 704319004 |Inheres in (attribute)| = << 410607006 |Organism (organism)|)
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (0): 
- **In both**: 16

### micro_keimzahl — Colony count — with culture technique asserted
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118550005 |Number concentration (property) (qualifier value)| OR 705056007 |Logarithmic number concentration (property) (qualifier value)|), (246093002 |Component (attribute)| = << 410607006 |Organism (organism)| OR 704319004 |Inheres in (attribute)| = << 410607006 |Organism (organism)|), 246501002 |Technique (attribute)| = << 703725008 |Culture technique (qualifier value)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (0): 
- **In both**: 4

### micro_mikroskopie — General microscopy — nominal finding by microscopy or staining technique
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 118584009 |Presence or identity (property) (qualifier value)|, 370132008 |Scale type (attribute)| = 117362005 |Nominal value (qualifier value)|, 246501002 |Technique (attribute)| = (<< 278289002 |Microscopy technique (qualifier value)| OR << 703857004 |Staining technique (qualifier value)|)
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (7): 883831010000102, 883931010000105, 884811010000108, 885021010000109, 885141010000100, 885181010000109, 902951010000103
- **In both**: 376

### micro_mikroskopie — General microscopy — method-neutral 'finding in specimen' pattern
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 118584009 |Presence or identity (property) (qualifier value)|, 370132008 |Scale type (attribute)| = 117362005 |Nominal value (qualifier value)|, 704319004 |Inheres in (attribute)| = << 123038009 |Specimen (specimen)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (2): 884811010000108, 885021010000109
- **In both**: 355

### micro_mikroskopie — Specific microscopy — ordinal threshold presence by microscopy or staining technique
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118589004 |Threshold (property) (qualifier value)| OR 705057003 |Presence (property) (qualifier value)|), 370132008 |Scale type (attribute)| = 117363000 |Ordinal value (qualifier value)|, 246501002 |Technique (attribute)| = (<< 278289002 |Microscopy technique (qualifier value)| OR << 703857004 |Staining technique (qualifier value)|)
```
- **Only in local-2026-03-21** (1): 710541010000101
- **Only in local-2026-10-21** (16): 884021010000105, 885051010000102, 885061010000100, 885071010000105, 885101010000102, 885131010000108, 885171010000106, 885201010000105, 885211010000108, 885221010000102, 885231010000104, 885241010000107, 885251010000109, 885281010000103, 885291010000100, 885301010000104
- **In both**: 315

### micro_molekulare_pathogenlast — Pathogen load — quantitative microbial nucleic acid, any technique
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118550005 |Number concentration (property) (qualifier value)| OR 705056007 |Logarithmic number concentration (property) (qualifier value)| OR 118569000 |Arbitrary concentration (property) (qualifier value)| OR 762918005 |Logarithmic arbitrary concentration (property) (qualifier value)|), 246093002 |Component (attribute)| = << 117174000 |Nucleic acid sequence with relative specificity for microorganism (substance)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (4): 884481010000100, 884491010000102, 884501010000108, 901651010000103
- **In both**: 397

### micro_molekulare_pathogenlast — Pathogen load — amplification technique asserted
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118550005 |Number concentration (property) (qualifier value)| OR 705056007 |Logarithmic number concentration (property) (qualifier value)| OR 118569000 |Arbitrary concentration (property) (qualifier value)| OR 762918005 |Logarithmic arbitrary concentration (property) (qualifier value)|), 246093002 |Component (attribute)| = << 117174000 |Nucleic acid sequence with relative specificity for microorganism (substance)|, 246501002 |Technique (attribute)| = << 1156878000 |Molecular nucleic acid amplification technique (qualifier value)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (4): 884481010000100, 884491010000102, 884501010000108, 901651010000103
- **In both**: 355

### micro_resistenzmechanismen — Resistant-organism detection — presence/identity of an antimicrobial resistant organism
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118589004 |Threshold (property) (qualifier value)| OR 705057003 |Presence (property) (qualifier value)| OR 118584009 |Presence or identity (property) (qualifier value)|), (246093002 |Component (attribute)| = << 409793007 |Antimicrobial resistant bacteria (organism)| OR 704319004 |Inheres in (attribute)| = << 409793007 |Antimicrobial resistant bacteria (organism)|)
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (0): 
- **In both**: 16

### micro_resistenzmechanismen — Resistant organism — any observable about a resistant organism (upper bound)
```
<< 363787002 |Observable entity (observable entity)| : (246093002 |Component (attribute)| = << 409793007 |Antimicrobial resistant bacteria (organism)| OR 704319004 |Inheres in (attribute)| = << 409793007 |Antimicrobial resistant bacteria (organism)|)
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (0): 
- **In both**: 16

### micro_spezifische_bestimmung — Nucleic-acid detection — any or no technique
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118589004 |Threshold (property) (qualifier value)| OR 705057003 |Presence (property) (qualifier value)| OR 118584009 |Presence or identity (property) (qualifier value)|), 246093002 |Component (attribute)| = << 117174000 |Nucleic acid sequence with relative specificity for microorganism (substance)|
```
- **Only in local-2026-03-21** (1): 484201010000101
- **Only in local-2026-10-21** (586): 708031010000104, 884111010000100, 884121010000106, 884131010000109, 884141010000101, 884181010000105, 884191010000108, 884201010000106, 884211010000109, 884221010000103, 884231010000100, 884241010000108, 884251010000105, 884261010000107, 884271010000102, 884281010000104, 884291010000101, 884301010000100, 884311010000102, 884321010000108 …
- **In both**: 1921

### micro_spezifische_bestimmung — Nucleic-acid detection — amplification technique asserted
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118589004 |Threshold (property) (qualifier value)| OR 705057003 |Presence (property) (qualifier value)| OR 118584009 |Presence or identity (property) (qualifier value)|), 246093002 |Component (attribute)| = << 117174000 |Nucleic acid sequence with relative specificity for microorganism (substance)|, 246501002 |Technique (attribute)| = << 1156878000 |Molecular nucleic acid amplification technique (qualifier value)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (38): 884181010000105, 884191010000108, 884201010000106, 884211010000109, 884221010000103, 884231010000100, 884241010000108, 884251010000105, 884261010000107, 884271010000102, 884281010000104, 884291010000101, 884301010000100, 884311010000102, 884321010000108, 884331010000106, 884341010000103, 884351010000101, 884361010000104, 884371010000109 …
- **In both**: 1486

### micro_spezifische_bestimmung — Nucleic-acid detection — no technique modelled
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118589004 |Threshold (property) (qualifier value)| OR 705057003 |Presence (property) (qualifier value)| OR 118584009 |Presence or identity (property) (qualifier value)|), 246093002 |Component (attribute)| = << 117174000 |Nucleic acid sequence with relative specificity for microorganism (substance)|, [0..0] 246501002 |Technique (attribute)| = *
```
- **Only in local-2026-03-21** (19): 484031010000104, 484061010000106, 484101010000109, 484121010000101, 484131010000103, 484141010000106, 484151010000108, 484161010000105, 484191010000104, 484201010000101, 485601010000104, 485611010000101, 485681010000106, 485711010000107, 485741010000106, 485801010000103, 485881010000105, 708471010000109, 709341010000102
- **Only in local-2026-10-21** (19): 884111010000100, 884121010000106, 884131010000109, 884141010000101, 884681010000102, 884691010000104, 884701010000104, 884711010000101, 884721010000107, 884731010000105, 884741010000102, 884751010000100, 884761010000103, 884771010000108, 884781010000106, 884791010000109, 884801010000105, 884851010000109, 884861010000106
- **In both**: 269

### micro_spezifische_bestimmung — Targeted culture detection — organism specific culture technique
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118589004 |Threshold (property) (qualifier value)| OR 705057003 |Presence (property) (qualifier value)|), 246501002 |Technique (attribute)| = << 703752003 |Organism specific culture technique (qualifier value)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (1): 884821010000102
- **In both**: 191

### micro_spezifische_bestimmung — Antigen detection — threshold presence of a microbial antigen
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118589004 |Threshold (property) (qualifier value)| OR 705057003 |Presence (property) (qualifier value)|), 246093002 |Component (attribute)| = << 116633006 |Microbial antigen (substance)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (1): 900621010000103
- **In both**: 898

### micro_titer — Titre — pathogen antibody titre
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 118590008 |Dilution factor expressed as titer (property) (qualifier value)|, 246093002 |Component (attribute)| = << 312301006 |Infective organism antibody (substance)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (4): 739971010000100, 743281010000108, 743291010000106, 743301010000107
- **In both**: 1712

### micro_titer — Titre — all titre observables (upper bound)
```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 118590008 |Dilution factor expressed as titer (property) (qualifier value)|
```
- **Only in local-2026-03-21** (0): 
- **Only in local-2026-10-21** (2): 883911010000101, 901791010000102
- **In both**: 2186
