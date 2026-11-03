# Release delta per request — concepts with FSN and LOINC

- A = `local-2026-03-21` (`MAIN/SNOMEDCT-LOINC/2026-03-21`)
- B = `local-2026-10-21` (`MAIN/SNOMEDCT-LOINC/2026-10-21`)
- LOINC codes from `loincsnomed_identifiers_20261021.txt`

| Request | Query | A | B | only A | only B | both |
|---|---|---:|---:|---:|---:|---:|
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

## micro_allgemeine_bestimmung — General determination — organism identity, any technique

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 118584009 |Presence or identity (property) (qualifier value)|, 704319004 |Inheres in (attribute)| = << 410607006 |Organism (organism)|
```

**Only in B (added)** (24)

| LOINC | SCTID | FSN |
|---|---|---|
| 10686-4 | 883831010000102 | Presence or identity of Leishmania in tissue at point in time by Giemsa stain (observable entity) |
| 10687-2 | 883841010000105 | Presence or identity of Leishmania in tissue at point in time by organism specific culture (observable entity) |
| 111515-3 | 883941010000102 | Presence or identity of Fungi in prostatic fluid at point in time by microbial culture (observable entity) |
| 112851-1 | 884661010000105 | Presence or identity of Bacteria in surgical wound.shallow at point in time by microbial culture (observable entity) |
| 112852-9 | 884671010000100 | Presence or identity of Bacteria in surgical wound.deep at point in time by microbial culture (observable entity) |
| 112889-1 | 884831010000104 | Presence or identity of Fungi in penis at point in time by microbial culture (observable entity) |
| 112891-7 | 884841010000107 | Presence or identity of Bacteria in ear at point in time by microbial culture (observable entity) |
| 112896-6 | 884891010000100 | Presence or identity of Actinomyces in bronchoalveolar lavage fluid at point in time by organism specific culture (observable entity) |
| 112897-4 | 884901010000101 | Presence or identity of Nocardia in bronchoalveolar lavage fluid at point in time by organism specific culture (observable entity) |
| 112898-2 | 884911010000103 | Presence or identity of Legionella in bronchoalveolar lavage fluid at point in time by organism specific culture (observable entity) |
| 113006-1 | 885001010000101 | Presence or identity of Fungi in drain device at point in time by microbial culture (observable entity) |
| 113007-9 | 885011010000103 | Presence or identity of Bacteria in drain device at point in time by microbial culture (observable entity) |
| 113009-5 | 885031010000107 | Presence or identity of Bacteria in drain device at point in time by anaerobic culture (observable entity) |
| 113037-6 | 885091010000106 | Presence or identity of Gram-positive bacteria in synovial fluid at point in time by Gram stain (observable entity) |
| 113049-1 | 885141010000100 | Presence or identity of Gram-positive bacteria in pleural fluid at point in time by Gram stain (observable entity) |
| 113056-6 | 885181010000109 | Presence or identity of Gram-positive bacteria in peritoneal fluid at point in time by Gram stain (observable entity) |
| 23160-5 | 902161010000103 | Presence or identity of Leishmania in tissue at point in time by immunofluorescence (observable entity) |
| 23161-3 | 902171010000108 | Presence or identity of Leishmania in tissue at point in time by electrophoresis (observable entity) |
| 23162-1 | 902181010000106 | Presence or identity of Leishmania in tissue at point in time by PAGE (observable entity) |
| 51709-4 | 902951010000103 | Presence or identity of Leishmania in specimen at point in time by Giemsa stain (observable entity) |
| 51710-2 | 902961010000101 | Presence or identity of Leishmania in specimen at point in time by organism specific culture (observable entity) |
| 53625-0 | 902971010000106 | Presence or identity of Leishmania in tissue at point in time (observable entity) |
| 87986-6 | 903351010000109 | Presence or identity of Leishmania in bone marrow at point in time by organism specific culture (observable entity) |
| 87987-4 | 903361010000106 | Presence or identity of Leishmania in blood at point in time by organism specific culture (observable entity) |

## micro_allgemeine_bestimmung — General determination — method-neutral identity codes

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 118584009 |Presence or identity (property) (qualifier value)|, 704319004 |Inheres in (attribute)| = << 410607006 |Organism (organism)|, [0..0] 246501002 |Technique (attribute)| = *
```

**Only in B (added)** (2)

| LOINC | SCTID | FSN |
|---|---|---|
| 23162-1 | 902181010000106 | Presence or identity of Leishmania in tissue at point in time by PAGE (observable entity) |
| 53625-0 | 902971010000106 | Presence or identity of Leishmania in tissue at point in time (observable entity) |

## micro_allgemeine_bestimmung — Typing — type of an organism (serotype, genotype, biotype)

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 410656007 |Type (property) (qualifier value)|, 704319004 |Inheres in (attribute)| = << 410607006 |Organism (organism)|
```

## micro_allgemeine_kultur — General culture — organism identity by culture technique

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 118584009 |Presence or identity (property) (qualifier value)|, 246501002 |Technique (attribute)| = << 703725008 |Culture technique (qualifier value)|, (704319004 |Inheres in (attribute)| = << 410607006 |Organism (organism)| OR 246093002 |Component (attribute)| = << 410607006 |Organism (organism)|)
```

**Only in B (added)** (15)

| LOINC | SCTID | FSN |
|---|---|---|
| 10687-2 | 883841010000105 | Presence or identity of Leishmania in tissue at point in time by organism specific culture (observable entity) |
| 111515-3 | 883941010000102 | Presence or identity of Fungi in prostatic fluid at point in time by microbial culture (observable entity) |
| 112851-1 | 884661010000105 | Presence or identity of Bacteria in surgical wound.shallow at point in time by microbial culture (observable entity) |
| 112852-9 | 884671010000100 | Presence or identity of Bacteria in surgical wound.deep at point in time by microbial culture (observable entity) |
| 112889-1 | 884831010000104 | Presence or identity of Fungi in penis at point in time by microbial culture (observable entity) |
| 112891-7 | 884841010000107 | Presence or identity of Bacteria in ear at point in time by microbial culture (observable entity) |
| 112896-6 | 884891010000100 | Presence or identity of Actinomyces in bronchoalveolar lavage fluid at point in time by organism specific culture (observable entity) |
| 112897-4 | 884901010000101 | Presence or identity of Nocardia in bronchoalveolar lavage fluid at point in time by organism specific culture (observable entity) |
| 112898-2 | 884911010000103 | Presence or identity of Legionella in bronchoalveolar lavage fluid at point in time by organism specific culture (observable entity) |
| 113006-1 | 885001010000101 | Presence or identity of Fungi in drain device at point in time by microbial culture (observable entity) |
| 113007-9 | 885011010000103 | Presence or identity of Bacteria in drain device at point in time by microbial culture (observable entity) |
| 113009-5 | 885031010000107 | Presence or identity of Bacteria in drain device at point in time by anaerobic culture (observable entity) |
| 51710-2 | 902961010000101 | Presence or identity of Leishmania in specimen at point in time by organism specific culture (observable entity) |
| 87986-6 | 903351010000109 | Presence or identity of Leishmania in bone marrow at point in time by organism specific culture (observable entity) |
| 87987-4 | 903361010000106 | Presence or identity of Leishmania in blood at point in time by organism specific culture (observable entity) |

## micro_allgemeine_kultur — Targeted culture — threshold presence of a named organism by culture technique

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118589004 |Threshold (property) (qualifier value)| OR 705057003 |Presence (property) (qualifier value)|), 246501002 |Technique (attribute)| = << 703725008 |Culture technique (qualifier value)|, (704319004 |Inheres in (attribute)| = << 410607006 |Organism (organism)| OR 246093002 |Component (attribute)| = << 410607006 |Organism (organism)|)
```

**Only in B (added)** (1)

| LOINC | SCTID | FSN |
|---|---|---|
| 112888-3 | 884821010000102 | Threshold presence of Neisseria gonorrhoeae in penis at point in time by organism specific culture (observable entity) |

## micro_allgemeine_kultur — Everything by culture technique (upper bound)

```
<< 363787002 |Observable entity (observable entity)| : 246501002 |Technique (attribute)| = << 703725008 |Culture technique (qualifier value)|
```

**Only in B (added)** (16)

| LOINC | SCTID | FSN |
|---|---|---|
| 10687-2 | 883841010000105 | Presence or identity of Leishmania in tissue at point in time by organism specific culture (observable entity) |
| 111515-3 | 883941010000102 | Presence or identity of Fungi in prostatic fluid at point in time by microbial culture (observable entity) |
| 112851-1 | 884661010000105 | Presence or identity of Bacteria in surgical wound.shallow at point in time by microbial culture (observable entity) |
| 112852-9 | 884671010000100 | Presence or identity of Bacteria in surgical wound.deep at point in time by microbial culture (observable entity) |
| 112888-3 | 884821010000102 | Threshold presence of Neisseria gonorrhoeae in penis at point in time by organism specific culture (observable entity) |
| 112889-1 | 884831010000104 | Presence or identity of Fungi in penis at point in time by microbial culture (observable entity) |
| 112891-7 | 884841010000107 | Presence or identity of Bacteria in ear at point in time by microbial culture (observable entity) |
| 112896-6 | 884891010000100 | Presence or identity of Actinomyces in bronchoalveolar lavage fluid at point in time by organism specific culture (observable entity) |
| 112897-4 | 884901010000101 | Presence or identity of Nocardia in bronchoalveolar lavage fluid at point in time by organism specific culture (observable entity) |
| 112898-2 | 884911010000103 | Presence or identity of Legionella in bronchoalveolar lavage fluid at point in time by organism specific culture (observable entity) |
| 113006-1 | 885001010000101 | Presence or identity of Fungi in drain device at point in time by microbial culture (observable entity) |
| 113007-9 | 885011010000103 | Presence or identity of Bacteria in drain device at point in time by microbial culture (observable entity) |
| 113009-5 | 885031010000107 | Presence or identity of Bacteria in drain device at point in time by anaerobic culture (observable entity) |
| 51710-2 | 902961010000101 | Presence or identity of Leishmania in specimen at point in time by organism specific culture (observable entity) |
| 87986-6 | 903351010000109 | Presence or identity of Leishmania in bone marrow at point in time by organism specific culture (observable entity) |
| 87987-4 | 903361010000106 | Presence or identity of Leishmania in blood at point in time by organism specific culture (observable entity) |

## micro_antigen_antikoerper_quantitativ — Serology quantitative — concentration of a pathogen antibody or antigen

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118569000 |Arbitrary concentration (property) (qualifier value)| OR 118539007 |Mass concentration (property) (qualifier value)| OR 118556004 |Substance concentration (property) (qualifier value)| OR 118550005 |Number concentration (property) (qualifier value)|), 246093002 |Component (attribute)| = (<< 312301006 |Infective organism antibody (substance)| OR << 116633006 |Microbial antigen (substance)|)
```

**Only in B (added)** (43)

| LOINC | SCTID | FSN |
|---|---|---|
| 112632-5 | 884151010000104 | Arbitrary concentration of Adenovirus IgA in serum at point in time by immunoassay (observable entity) |
| 18409-3 | 734971010000101 | Arbitrary concentration of Curvularia lunata IgG in serum at point in time (observable entity) |
| 18410-1 | 734981010000103 | Arbitrary concentration of Epicoccum purpurascens IgG in serum at point in time (observable entity) |
| 18411-9 | 734991010000100 | Arbitrary concentration of Rhizopus stolonifer IgG in serum at point in time (observable entity) |
| 18412-7 | 735001010000105 | Arbitrary concentration of Stemphylium botryosum IgG in serum at point in time (observable entity) |
| 18416-8 | 735011010000108 | Arbitrary concentration of Aspergillus nidulans IgG in serum at point in time (observable entity) |
| 18420-0 | 735021010000102 | Arbitrary concentration of Chaetomium globosum IgG in serum at point in time (observable entity) |
| 18421-8 | 735031010000104 | Arbitrary concentration of Fusarium oxysporum IgG in serum at point in time (observable entity) |
| 24517-5 | 736331010000109 | Arbitrary concentration of Phoma IgG in serum at point in time (observable entity) |
| 25779-0 | 736521010000103 | Arbitrary concentration of Stachybotrys chartarum IgG in serum at point in time (observable entity) |
| 30022-8 | 737311010000103 | Arbitrary concentration of Botrytis cinerea IgG in serum at point in time (observable entity) |
| 30032-7 | 737331010000107 | Arbitrary concentration of Phoma betae IgG in serum at point in time (observable entity) |
| 35548-7 | 739861010000104 | Mass concentration of Fusarium verticillioides IgG in serum at point in time (observable entity) |
| 35549-5 | 739871010000109 | Mass concentration of Mucor racemosus IgG in serum at point in time (observable entity) |
| 35551-1 | 739881010000107 | Mass concentration of Phoma betae IgG in serum at point in time (observable entity) |
| 35552-9 | 739891010000105 | Mass concentration of Rhizopus stolonifer IgG in serum at point in time (observable entity) |
| 35553-7 | 739901010000109 | Mass concentration of Stemphylium botryosum IgG in serum at point in time (observable entity) |
| 35555-2 | 739921010000101 | Mass concentration of Exserohilum rostratum IgG in serum at point in time (observable entity) |
| 42591-8 | 741441010000104 | Mass concentration of Botrytis cinerea IgG in serum at point in time (observable entity) |
| 42816-9 | 741551010000101 | Mass concentration of Stachybotrys chartarum IgG in serum at point in time (observable entity) |
| 42904-3 | 741591010000105 | Mass concentration of Epicoccum purpurascens IgG in serum at point in time (observable entity) |
| 42907-6 | 741601010000104 | Mass concentration of Helminthosporium IgG in serum at point in time (observable entity) |
| 49195-1 | 743311010000105 | Arbitrary concentration of California encephalitis virus IgG in serum at point in time (observable entity) |
| 58958-0 | 749811010000101 | Mass concentration of Fusarium oxysporum IgG in serum at point in time (observable entity) |
| 59382-2 | 749991010000103 | Mass concentration of Aspergillus versicolor IgG in serum at point in time (observable entity) |
| 63162-2 | 751841010000103 | Mass concentration of Curvularia lunata IgG in serum at point in time (observable entity) |
| 63163-0 | 751851010000101 | Mass concentration of Paecilomyces IgG in serum at point in time (observable entity) |
| 63164-8 | 751861010000104 | Mass concentration of Penicillium brevicompactum IgG in serum at point in time (observable entity) |
| 63165-5 | 751871010000109 | Mass concentration of Serpula lacrimans IgG in serum at point in time (observable entity) |
| 63166-3 | 751881010000107 | Mass concentration of Aspergillus terreus IgG in serum at point in time (observable entity) |
| 63168-9 | 751891010000105 | Mass concentration of Aspergillus amstelodami IgG in serum at point in time (observable entity) |
| 63169-7 | 751901010000109 | Mass concentration of Aspergillus nidulans IgG in serum at point in time (observable entity) |
| 63170-5 | 751921010000101 | Mass concentration of Dendryphiella vinosa IgG in serum at point in time (observable entity) |
| 63171-3 | 751931010000103 | Mass concentration of Neurospora sitophila IgG in serum at point in time (observable entity) |
| 63172-1 | 751941010000106 | Mass concentration of Mucor plumbeus IgG in serum at point in time (observable entity) |
| 63173-9 | 751951010000108 | Mass concentration of Hypomyces perniciosus IgG in serum at point in time (observable entity) |
| 63174-7 | 751961010000105 | Mass concentration of Spondylocladium IgG in serum at point in time (observable entity) |
| 63175-4 | 751971010000100 | Mass concentration of Epidermophyton floccosum IgG in serum at point in time (observable entity) |
| 63178-8 | 751991010000104 | Mass concentration of Chaetomium globosum IgG in serum at point in time (observable entity) |
| 7325-4 | 754331010000101 | Arbitrary concentration of Fusarium verticillioides IgG in serum at point in time (observable entity) |
| 7396-5 | 754911010000109 | Arbitrary concentration of Helminthosporium IgG in serum at point in time (observable entity) |
| 7507-7 | 755751010000108 | Arbitrary concentration of Mucor racemosus IgG in serum at point in time (observable entity) |
| 7638-0 | 756331010000105 | Arbitrary concentration of Pullularia IgG in serum at point in time (observable entity) |

## micro_antigen_antikoerper_quantitativ — Serology qualitative — threshold presence of a pathogen antibody or antigen

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118589004 |Threshold (property) (qualifier value)| OR 705057003 |Presence (property) (qualifier value)|), 246093002 |Component (attribute)| = (<< 312301006 |Infective organism antibody (substance)| OR << 116633006 |Microbial antigen (substance)|)
```

**Only in B (added)** (27)

| LOINC | SCTID | FSN |
|---|---|---|
| 102905-7 | 706781010000100 | Threshold presence of Stachybotrys chartarum IgG in serum at point in time by radioallergosorbent testing (observable entity) |
| 102956-0 | 706941010000107 | Threshold presence of Curvularia spicifera IgG in serum at point in time by radioallergosorbent testing (observable entity) |
| 102958-6 | 706961010000106 | Threshold presence of Fusarium verticillioides IgG in serum at point in time by radioallergosorbent testing (observable entity) |
| 102959-4 | 706971010000101 | Threshold presence of Helminthosporium IgG in serum at point in time by radioallergosorbent testing (observable entity) |
| 102961-0 | 706991010000100 | Threshold presence of Mucor racemosus IgG in serum at point in time by radioallergosorbent testing (observable entity) |
| 102963-6 | 707001010000106 | Threshold presence of Phoma betae IgG in serum at point in time by radioallergosorbent testing (observable entity) |
| 102966-9 | 707021010000103 | Threshold presence of Rhizopus stolonifer IgG in serum at point in time by radioallergosorbent testing (observable entity) |
| 102967-7 | 707031010000100 | Threshold presence of Stemphylium botryosum IgG in serum at point in time by radioallergosorbent testing (observable entity) |
| 112334-8 | 883971010000108 | Threshold presence of Western equine encephalitis virus IgM in serum at point in time by immunofluorescence (observable entity) |
| 112335-5 | 883981010000106 | Threshold presence of Saint Louis encephalitis virus IgM in serum at point in time by immunofluorescence (observable entity) |
| 112336-3 | 883991010000109 | Threshold presence of Eastern equine encephalitis virus IgM in serum at point in time by immunofluorescence (observable entity) |
| 112340-5 | 884001010000102 | Threshold presence of Western equine encephalitis virus IgG in serum at point in time by immunofluorescence (observable entity) |
| 112341-3 | 884011010000104 | Threshold presence of Saint Louis encephalitis virus IgG in serum at point in time by immunofluorescence (observable entity) |
| 112598-8 | 884081010000109 | Threshold presence of Borrelia burgdorferi IgM in serum or plasma at point in time by IA.STTT (observable entity) |
| 112599-6 | 884091010000107 | Threshold presence of Borrelia burgdorferi IgG in serum or plasma at point in time by IA.STTT (observable entity) |
| 112694-5 | 884161010000102 | Threshold presence of Human immunodeficiency virus 2 antibody in serum at point in time by line blot (observable entity) |
| 112695-2 | 884171010000107 | Threshold presence of Hepatitis C virus IgG in serum at point in time by line blot (observable entity) |
| 115347-7 | 900621010000103 | Threshold presence of Orthobornavirus bornaense antigen in specimen at point in time by molecular genetics (observable entity) |
| 115744-5 | 901291010000105 | Threshold presence of Saint Louis encephalitis virus IgG in cerebrospinal fluid at point in time by immunofluorescence (observable entity) |
| 115745-2 | 901301010000106 | Threshold presence of Western equine encephalitis virus IgG in cerebrospinal fluid at point in time by immunofluorescence (observable entity) |
| 115749-4 | 901311010000109 | Threshold presence of Eastern equine encephalitis virus IgM in cerebrospinal fluid at point in time by immunofluorescence (observable entity) |
| 115750-2 | 901321010000103 | Threshold presence of Saint Louis encephalitis virus IgM in cerebrospinal fluid at point in time by immunofluorescence (observable entity) |
| 115751-0 | 901331010000100 | Threshold presence of Western equine encephalitis virus IgM in cerebrospinal fluid at point in time by immunofluorescence (observable entity) |
| 51541-1 | 746071010000108 | Threshold presence of Stachybotrys chartarum IgG in serum at point in time (observable entity) |
| 51542-9 | 746081010000106 | Threshold presence of Aspergillus versicolor IgG in serum at point in time (observable entity) |
| 95543-5 | 762721010000104 | Threshold presence of Aspergillus terreus IgG in serum at point in time (observable entity) |
| 96507-9 | 763061010000103 | Threshold presence of California encephalitis virus IgG in specimen at point in time by immunoassay (observable entity) |

## micro_ct_wert — Ct value — threshold number of a microbial nucleic acid

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 1268648001 |Threshold number (property) (qualifier value)|, 246093002 |Component (attribute)| = << 117174000 |Nucleic acid sequence with relative specificity for microorganism (substance)|
```

## micro_ct_wert — Ct value — all threshold-number observables (upper bound)

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 1268648001 |Threshold number (property) (qualifier value)|
```

**Only in B (added)** (1)

| LOINC | SCTID | FSN |
|---|---|---|
| 92002-5 | 903401010000103 | Threshold number of SMN1 gene in dried blood spot at point in time by probe with target amplification (observable entity) |

## micro_empfindlichkeit — Phenotypic susceptibility — isolate, not genotyping

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 118588007 |Susceptibility (property) (qualifier value)|, 704327008 |Direct site (attribute)| = << 119303007 |Microbial isolate specimen (specimen)|, [0..0] 246501002 |Technique (attribute)| = << 708060009 |Genotype determination technique (qualifier value)|
```

**Only in B (added)** (3)

| LOINC | SCTID | FSN |
|---|---|---|
| 55136-6 | 903001010000108 | Susceptibility to penicillin in microbial isolate at point in time by MIC.Parenteral (observable entity) |
| 58085-2 | 903161010000108 | Susceptibility to penicillin in microbial isolate at point in time by parenteral (observable entity) |
| 77960-3 | 903311010000108 | Susceptibility to penicillin in microbial isolate at point in time by agar diffusion.Parenteral (observable entity) |

## micro_empfindlichkeit — Predicted susceptibility — by genotype determination technique

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 118588007 |Susceptibility (property) (qualifier value)|, 246501002 |Technique (attribute)| = << 708060009 |Genotype determination technique (qualifier value)|
```

## micro_empfindlichkeit — All susceptibility observables (upper bound)

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 118588007 |Susceptibility (property) (qualifier value)|
```

**Only in B (added)** (5)

| LOINC | SCTID | FSN |
|---|---|---|
| 55136-6 | 903001010000108 | Susceptibility to penicillin in microbial isolate at point in time by MIC.Parenteral (observable entity) |
| 55137-4 | 903011010000106 | Susceptibility to penicillin in isolate.meningitis at point in time by MIC.Parenteral (observable entity) |
| 58080-3 | 903151010000106 | Susceptibility to penicillin in isolate.meningitis at point in time by parenteral (observable entity) |
| 58085-2 | 903161010000108 | Susceptibility to penicillin in microbial isolate at point in time by parenteral (observable entity) |
| 77960-3 | 903311010000108 | Susceptibility to penicillin in microbial isolate at point in time by agar diffusion.Parenteral (observable entity) |

## micro_keimzahl — Colony count — number concentration of an organism

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118550005 |Number concentration (property) (qualifier value)| OR 705056007 |Logarithmic number concentration (property) (qualifier value)|), (246093002 |Component (attribute)| = << 410607006 |Organism (organism)| OR 704319004 |Inheres in (attribute)| = << 410607006 |Organism (organism)|)
```

## micro_keimzahl — Colony count — with culture technique asserted

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118550005 |Number concentration (property) (qualifier value)| OR 705056007 |Logarithmic number concentration (property) (qualifier value)|), (246093002 |Component (attribute)| = << 410607006 |Organism (organism)| OR 704319004 |Inheres in (attribute)| = << 410607006 |Organism (organism)|), 246501002 |Technique (attribute)| = << 703725008 |Culture technique (qualifier value)|
```

## micro_mikroskopie — General microscopy — nominal finding by microscopy or staining technique

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 118584009 |Presence or identity (property) (qualifier value)|, 370132008 |Scale type (attribute)| = 117362005 |Nominal value (qualifier value)|, 246501002 |Technique (attribute)| = (<< 278289002 |Microscopy technique (qualifier value)| OR << 703857004 |Staining technique (qualifier value)|)
```

**Only in B (added)** (7)

| LOINC | SCTID | FSN |
|---|---|---|
| 10686-4 | 883831010000102 | Presence or identity of Leishmania in tissue at point in time by Giemsa stain (observable entity) |
| 111514-6 | 883931010000105 | Microscopic observation of finding in fistula at point in time by Gram stain (observable entity) |
| 112887-5 | 884811010000108 | Microscopic observation of finding in specimen from penis at point in time by Gram stain (observable entity) |
| 113008-7 | 885021010000109 | Microscopic observation of finding in drain device submitted as specimen at point in time by Gram stain (observable entity) |
| 113049-1 | 885141010000100 | Presence or identity of Gram-positive bacteria in pleural fluid at point in time by Gram stain (observable entity) |
| 113056-6 | 885181010000109 | Presence or identity of Gram-positive bacteria in peritoneal fluid at point in time by Gram stain (observable entity) |
| 51709-4 | 902951010000103 | Presence or identity of Leishmania in specimen at point in time by Giemsa stain (observable entity) |

## micro_mikroskopie — General microscopy — method-neutral 'finding in specimen' pattern

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 118584009 |Presence or identity (property) (qualifier value)|, 370132008 |Scale type (attribute)| = 117362005 |Nominal value (qualifier value)|, 704319004 |Inheres in (attribute)| = << 123038009 |Specimen (specimen)|
```

**Only in B (added)** (2)

| LOINC | SCTID | FSN |
|---|---|---|
| 112887-5 | 884811010000108 | Microscopic observation of finding in specimen from penis at point in time by Gram stain (observable entity) |
| 113008-7 | 885021010000109 | Microscopic observation of finding in drain device submitted as specimen at point in time by Gram stain (observable entity) |

## micro_mikroskopie — Specific microscopy — ordinal threshold presence by microscopy or staining technique

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118589004 |Threshold (property) (qualifier value)| OR 705057003 |Presence (property) (qualifier value)|), 370132008 |Scale type (attribute)| = 117363000 |Ordinal value (qualifier value)|, 246501002 |Technique (attribute)| = (<< 278289002 |Microscopy technique (qualifier value)| OR << 703857004 |Staining technique (qualifier value)|)
```

**Only in B (added)** (16)

| LOINC | SCTID | FSN |
|---|---|---|
| 112407-2 | 884021010000105 | Threshold presence of bacteria in urine at point in time by light microscopy (observable entity) |
| 113024-4 | 885051010000102 | Threshold presence of yeast in urethra at point in time by Gram stain (observable entity) |
| 113028-5 | 885061010000100 | Threshold presence of Gram-positive bacteria in urethra at point in time by Gram stain (observable entity) |
| 113032-7 | 885071010000105 | Threshold presence of Gram-positive bacteria in bronchoalveolar lavage fluid at point in time by Gram stain (observable entity) |
| 113042-6 | 885101010000102 | Threshold presence of Gram-positive bacteria in vagina at point in time by Gram stain (observable entity) |
| 113045-9 | 885131010000108 | Threshold presence of yeast in pleural fluid at point in time by Gram stain (observable entity) |
| 113053-3 | 885171010000106 | Threshold presence of yeast in peritoneal fluid at point in time by Gram stain (observable entity) |
| 113058-2 | 885201010000105 | Threshold presence of leukocyte in peritoneal fluid at point in time by Gram stain (observable entity) |
| 113059-0 | 885211010000108 | Threshold presence of Gram-positive bacteria in sputum at point in time by Gram stain (observable entity) |
| 113060-8 | 885221010000102 | Threshold presence of yeast in bronchoalveolar aspirate at point in time by Gram stain (observable entity) |
| 113064-0 | 885231010000104 | Threshold presence of Gram-positive bacteria in bronchoalveolar aspirate at point in time by Gram stain (observable entity) |
| 113071-5 | 885241010000107 | Threshold presence of yeast in tissue at point in time by Gram stain (observable entity) |
| 113075-6 | 885251010000109 | Threshold presence of Gram-positive bacteria in tissue at point in time by Gram stain (observable entity) |
| 113081-4 | 885281010000103 | Threshold presence of Gram-positive bacteria in specimen obtained by aspiration at point in time by Gram stain (observable entity) |
| 113082-2 | 885291010000100 | Threshold presence of yeast in sputum at point in time by Gram stain (observable entity) |
| 113089-7 | 885301010000104 | Threshold presence of Gram-positive bacteria in pus at point in time by Gram stain (observable entity) |

**Only in A (removed)** (1)

| LOINC | SCTID | FSN |
|---|---|---|
| 107527-4 | 710541010000101 | Presence of clue cell in vagina at point in time by Gram stain (observable entity) |

## micro_molekulare_pathogenlast — Pathogen load — quantitative microbial nucleic acid, any technique

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118550005 |Number concentration (property) (qualifier value)| OR 705056007 |Logarithmic number concentration (property) (qualifier value)| OR 118569000 |Arbitrary concentration (property) (qualifier value)| OR 762918005 |Logarithmic arbitrary concentration (property) (qualifier value)|), 246093002 |Component (attribute)| = << 117174000 |Nucleic acid sequence with relative specificity for microorganism (substance)|
```

**Only in B (added)** (4)

| LOINC | SCTID | FSN |
|---|---|---|
| 112751-3 | 884481010000100 | Number concentration of West Nile virus RNA in plasma at point in time by probe with target amplification (observable entity) |
| 112752-1 | 884491010000102 | Number concentration of West Nile virus RNA in specimen at point in time by probe with target amplification (observable entity) |
| 112753-9 | 884501010000108 | Arbitrary concentration of Cytomegalovirus DNA in amniotic fluid at point in time by probe with target amplification (observable entity) |
| 115802-1 | 901651010000103 | Logarithmic arbitrary concentration of Human immunodeficiency virus 1 RNA in serum or plasma at point in time by probe with target amplification (observable entity) |

## micro_molekulare_pathogenlast — Pathogen load — amplification technique asserted

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118550005 |Number concentration (property) (qualifier value)| OR 705056007 |Logarithmic number concentration (property) (qualifier value)| OR 118569000 |Arbitrary concentration (property) (qualifier value)| OR 762918005 |Logarithmic arbitrary concentration (property) (qualifier value)|), 246093002 |Component (attribute)| = << 117174000 |Nucleic acid sequence with relative specificity for microorganism (substance)|, 246501002 |Technique (attribute)| = << 1156878000 |Molecular nucleic acid amplification technique (qualifier value)|
```

**Only in B (added)** (4)

| LOINC | SCTID | FSN |
|---|---|---|
| 112751-3 | 884481010000100 | Number concentration of West Nile virus RNA in plasma at point in time by probe with target amplification (observable entity) |
| 112752-1 | 884491010000102 | Number concentration of West Nile virus RNA in specimen at point in time by probe with target amplification (observable entity) |
| 112753-9 | 884501010000108 | Arbitrary concentration of Cytomegalovirus DNA in amniotic fluid at point in time by probe with target amplification (observable entity) |
| 115802-1 | 901651010000103 | Logarithmic arbitrary concentration of Human immunodeficiency virus 1 RNA in serum or plasma at point in time by probe with target amplification (observable entity) |

## micro_resistenzmechanismen — Resistant-organism detection — presence/identity of an antimicrobial resistant organism

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118589004 |Threshold (property) (qualifier value)| OR 705057003 |Presence (property) (qualifier value)| OR 118584009 |Presence or identity (property) (qualifier value)|), (246093002 |Component (attribute)| = << 409793007 |Antimicrobial resistant bacteria (organism)| OR 704319004 |Inheres in (attribute)| = << 409793007 |Antimicrobial resistant bacteria (organism)|)
```

## micro_resistenzmechanismen — Resistant organism — any observable about a resistant organism (upper bound)

```
<< 363787002 |Observable entity (observable entity)| : (246093002 |Component (attribute)| = << 409793007 |Antimicrobial resistant bacteria (organism)| OR 704319004 |Inheres in (attribute)| = << 409793007 |Antimicrobial resistant bacteria (organism)|)
```

## micro_spezifische_bestimmung — Nucleic-acid detection — any or no technique

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118589004 |Threshold (property) (qualifier value)| OR 705057003 |Presence (property) (qualifier value)| OR 118584009 |Presence or identity (property) (qualifier value)|), 246093002 |Component (attribute)| = << 117174000 |Nucleic acid sequence with relative specificity for microorganism (substance)|
```

**Only in B (added)** (586)

| LOINC | SCTID | FSN |
|---|---|---|
| 104341-3 | 708031010000104 | Threshold presence of Orthobornavirus bornaense RNA in specimen at point in time by molecular genetics (observable entity) |
| 112628-3 | 884111010000100 | Threshold presence of Human coronavirus RNA in bronchoalveolar lavage fluid at point in time by non-probe.amp.tar (observable entity) |
| 112629-1 | 884121010000106 | Threshold presence of Human coronavirus RNA in sputum at point in time by non-probe.amp.tar (observable entity) |
| 112630-9 | 884131010000109 | Threshold presence of Mycoplasma pneumoniae DNA in sputum at point in time by non-probe.amp.tar (observable entity) |
| 112631-7 | 884141010000101 | Threshold presence of Mycoplasma pneumoniae DNA in bronchoalveolar lavage fluid at point in time by non-probe.amp.tar (observable entity) |
| 112707-5 | 884181010000105 | Threshold presence of Streptococcus pneumoniae DNA in wound at point in time by probe with target amplification (observable entity) |
| 112708-3 | 884191010000108 | Threshold presence of Neisseria meningitidis DNA in wound at point in time by probe with target amplification (observable entity) |
| 112709-1 | 884201010000106 | Threshold presence of Escherichia coli DNA in wound at point in time by probe with target amplification (observable entity) |
| 112710-9 | 884211010000109 | Threshold presence of Enterococcus faecium DNA in wound at point in time by probe with target amplification (observable entity) |
| 112711-7 | 884221010000103 | Threshold presence of Streptococcus DNA in wound at point in time by probe with target amplification (observable entity) |
| 112712-5 | 884231010000100 | Threshold presence of Enterobacteriaceae DNA in wound at point in time by probe with target amplification (observable entity) |
| 112713-3 | 884241010000108 | Threshold presence of Stenotrophomonas maltophilia DNA in wound at point in time by probe with target amplification (observable entity) |
| 112714-1 | 884251010000105 | Threshold presence of Candida tropicalis DNA in wound at point in time by probe with target amplification (observable entity) |
| 112716-6 | 884261010000107 | Threshold presence of Enterococcus faecalis DNA in wound at point in time by probe with target amplification (observable entity) |
| 112717-4 | 884271010000102 | Threshold presence of Listeria monocytogenes DNA in wound at point in time by probe with target amplification (observable entity) |
| 112723-2 | 884281010000104 | Threshold presence of Candida parapsilosis DNA in wound at point in time by probe with target amplification (observable entity) |
| 112724-0 | 884291010000101 | Threshold presence of Klebsiella oxytoca DNA in wound at point in time by probe with target amplification (observable entity) |
| 112725-7 | 884301010000100 | Threshold presence of Haemophilus influenzae DNA in wound at point in time by probe with target amplification (observable entity) |
| 112726-5 | 884311010000102 | Threshold presence of Acinetobacter baumannii DNA in wound at point in time by probe with target amplification (observable entity) |
| 112727-3 | 884321010000108 | Threshold presence of Klebsiella pneumoniae DNA in wound at point in time by probe with target amplification (observable entity) |
| 112728-1 | 884331010000106 | Threshold presence of Candida albicans DNA in wound at point in time by probe with target amplification (observable entity) |
| 112729-9 | 884341010000103 | Threshold presence of Pseudomonas aeruginosa DNA in wound at point in time by probe with target amplification (observable entity) |
| 112732-3 | 884351010000101 | Threshold presence of Nakaseomyces glabratus DNA in wound at point in time by probe with target amplification (observable entity) |
| 112733-1 | 884361010000104 | Threshold presence of Candida krusei DNA in wound at point in time by probe with target amplification (observable entity) |
| 112735-6 | 884371010000109 | Threshold presence of Pseudomonas DNA in wound at point in time by probe with target amplification (observable entity) |
| 112736-4 | 884381010000107 | Threshold presence of Staphylococcus aureus DNA in wound at point in time by probe with target amplification (observable entity) |
| 112749-7 | 884461010000108 | Threshold presence of Human coronavirus 229E RNA in bronchoalveolar aspirate at point in time by probe with target amplification (observable entity) |
| 112750-5 | 884471010000103 | Threshold presence of severe acute respiratory syndrome coronavirus 2 RNA in sputum at point in time by probe with target amplification (observable entity) |
| 112755-4 | 884511010000106 | Threshold presence of Human coronavirus RNA in sputum at point in time by probe with target amplification (observable entity) |
| 112757-0 | 884521010000100 | Threshold presence of Legionella pneumophila DNA in throat at point in time by probe with target amplification (observable entity) |
| 112776-0 | 884531010000102 | Threshold presence of Human herpesvirus 8 DNA in cerebrospinal fluid at point in time by probe with target amplification (observable entity) |
| 112777-8 | 884541010000105 | Threshold presence of Human herpesvirus 8 DNA in specimen at point in time by probe with target amplification (observable entity) |
| 112778-6 | 884551010000107 | Threshold presence of human herpes simplex virus DNA in skin at point in time by probe with target amplification (observable entity) |
| 112779-4 | 884561010000109 | Threshold presence of human herpes simplex virus DNA in bronchoalveolar lavage fluid at point in time by probe with target amplification (observable entity) |
| 112780-2 | 884571010000104 | Threshold presence of Human alphaherpesvirus 2 DNA in bronchoalveolar lavage fluid at point in time by probe with target amplification (observable entity) |
| 112781-0 | 884581010000101 | Threshold presence of Human alphaherpesvirus 1 DNA in bronchoalveolar lavage fluid at point in time by probe with target amplification (observable entity) |
| 112782-8 | 884591010000103 | Threshold presence of Epstein-Barr virus DNA in bronchoalveolar lavage fluid at point in time by probe with target amplification (observable entity) |
| 112783-6 | 884601010000109 | Threshold presence of Epstein-Barr virus DNA in throat at point in time by probe with target amplification (observable entity) |
| 112873-5 | 884681010000102 | Threshold presence of Legionella pneumophila DNA in sputum at point in time by non-probe.amp.tar (observable entity) |
| 112874-3 | 884691010000104 | Threshold presence of Parainfluenza virus 4 RNA in throat at point in time by non-probe.amp.tar (observable entity) |
| 112875-0 | 884701010000104 | Threshold presence of Parainfluenza virus 3 RNA in throat at point in time by non-probe.amp.tar (observable entity) |
| 112876-8 | 884711010000101 | Threshold presence of Parainfluenza virus 2 RNA in throat at point in time by non-probe.amp.tar (observable entity) |
| 112877-6 | 884721010000107 | Threshold presence of Parainfluenza virus 1 RNA in throat at point in time by non-probe.amp.tar (observable entity) |
| 112878-4 | 884731010000105 | Threshold presence of Betacoronavirus cameli RNA in throat at point in time by non-probe.amp.tar (observable entity) |
| 112879-2 | 884741010000102 | Threshold presence of Influenza A virus H1 RNA in throat at point in time by non-probe.amp.tar (observable entity) |
| 112880-0 | 884751010000100 | Threshold presence of Human coronavirus OC43 RNA in throat at point in time by non-probe.amp.tar (observable entity) |
| 112881-8 | 884761010000103 | Threshold presence of Klebsiella pneumoniae DNA in synovial fluid at point in time by non-probe.amp.tar (observable entity) |
| 112882-6 | 884771010000108 | Threshold presence of Human coronavirus 229E RNA in throat at point in time by non-probe.amp.tar (observable entity) |
| 112883-4 | 884781010000106 | Threshold presence of Human coronavirus NL63 RNA in throat at point in time by non-probe.amp.tar (observable entity) |
| 112884-2 | 884791010000109 | Threshold presence of Parainfluenza virus RNA in sputum at point in time by non-probe.amp.tar (observable entity) |
| 112885-9 | 884801010000105 | Threshold presence of Betacoronavirus cameli RNA in sputum at point in time by non-probe.amp.tar (observable entity) |
| 112892-5 | 884851010000109 | Threshold presence of Human Respiratory syncytial virus RNA in sputum at point in time by non-probe.amp.tar (observable entity) |
| 112893-3 | 884861010000106 | Threshold presence of Human coronavirus HKU1 RNA in throat at point in time by non-probe.amp.tar (observable entity) |
| 112894-1 | 884871010000101 | Threshold presence of Haemophilus influenzae DNA in throat at point in time by probe with target amplification (observable entity) |
| 112895-8 | 884881010000103 | Threshold presence of Streptococcus pneumoniae DNA in throat at point in time by probe with target amplification (observable entity) |
| 114505-1 | 895931010000105 | Threshold presence of Orthoflavivirus zikaense RNA in specimen at point in time by molecular genetics (observable entity) |
| 114507-7 | 895941010000102 | Threshold presence of Yersinia pseudotuberculosis DNA in specimen at point in time by molecular genetics (observable entity) |
| 114508-5 | 895951010000100 | Threshold presence of Yersinia pestis DNA in specimen at point in time by molecular genetics (observable entity) |
| 114510-1 | 895961010000103 | Threshold presence of Yellow fever virus RNA in specimen at point in time by molecular genetics (observable entity) |
| 114512-7 | 895971010000108 | Threshold presence of microorganism DNA in specimen at point in time by molecular genetics (observable entity) |
| 114513-5 | 895981010000106 | Threshold presence of Western equine encephalitis virus RNA in specimen at point in time by molecular genetics (observable entity) |
| 114514-3 | 895991010000109 | Threshold presence of West Nile virus RNA in specimen at point in time by molecular genetics (observable entity) |
| 114516-8 | 896001010000105 | Threshold presence of Vibrio vulnificus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114517-6 | 896011010000108 | Threshold presence of Vibrio parahaemolyticus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114523-4 | 896021010000102 | Threshold presence of Alphavirus venezuelan RNA in specimen at point in time by molecular genetics (observable entity) |
| 114524-2 | 896031010000104 | Threshold presence of Variola virus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114525-9 | 896041010000107 | Threshold presence of Varicella virus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114526-7 | 896051010000109 | Threshold presence of Vaccinia virus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114529-1 | 896061010000106 | Threshold presence of Ureaplasma urealyticum DNA in specimen at point in time by molecular genetics (observable entity) |
| 114530-9 | 896071010000101 | Threshold presence of Ureaplasma DNA in specimen at point in time by molecular genetics (observable entity) |
| 114531-7 | 896081010000103 | Threshold presence of Ureaplasma parvum DNA in specimen at point in time by molecular genetics (observable entity) |
| 114534-1 | 896091010000100 | Threshold presence of Trypanosoma cruzi DNA in specimen at point in time by molecular genetics (observable entity) |
| 114536-6 | 896101010000109 | Threshold presence of Trypanosoma brucei DNA in specimen at point in time by molecular genetics (observable entity) |
| 114537-4 | 896111010000107 | Threshold presence of Tropheryma whipplei DNA in specimen at point in time by molecular genetics (observable entity) |
| 114539-0 | 896121010000101 | Threshold presence of Trichophyton violaceum DNA in specimen at point in time by molecular genetics (observable entity) |
| 114540-8 | 896131010000103 | Threshold presence of Trichophyton verrucosum DNA in specimen at point in time by molecular genetics (observable entity) |
| 114541-6 | 896141010000106 | Threshold presence of Trichophyton tonsurans DNA in specimen at point in time by molecular genetics (observable entity) |
| 114542-4 | 896151010000108 | Threshold presence of Trichophyton simii DNA in specimen at point in time by molecular genetics (observable entity) |
| 114543-2 | 896161010000105 | Threshold presence of Trichophyton schoenleinii DNA in specimen at point in time by molecular genetics (observable entity) |
| 114544-0 | 896171010000100 | Threshold presence of Trichophyton rubrum DNA in specimen at point in time by molecular genetics (observable entity) |
| 114545-7 | 896181010000102 | Threshold presence of Trichophyton quinckeanum DNA in specimen at point in time by molecular genetics (observable entity) |
| 114546-5 | 896191010000104 | Threshold presence of Trichophyton mentagrophytes DNA in specimen at point in time by molecular genetics (observable entity) |
| 114547-3 | 896201010000101 | Threshold presence of Trichophyton interdigitale DNA in specimen at point in time by molecular genetics (observable entity) |
| 114548-1 | 896211010000103 | Threshold presence of Trichophyton eriotrephon DNA in specimen at point in time by molecular genetics (observable entity) |
| 114549-9 | 896221010000109 | Threshold presence of Trichophyton erinacei DNA in specimen at point in time by molecular genetics (observable entity) |
| 114550-7 | 896231010000107 | Threshold presence of Trichophyton equinum DNA in specimen at point in time by molecular genetics (observable entity) |
| 114551-5 | 896241010000104 | Threshold presence of Trichophyton concentricum DNA in specimen at point in time by molecular genetics (observable entity) |
| 114552-3 | 896251010000102 | Threshold presence of Trichophyton bullosum DNA in specimen at point in time by molecular genetics (observable entity) |
| 114555-6 | 896261010000100 | Threshold presence of Trichinella spiralis DNA in specimen at point in time by molecular genetics (observable entity) |
| 114557-2 | 896271010000105 | Threshold presence of Treponema pallidum DNA in specimen at point in time by molecular genetics (observable entity) |
| 114559-8 | 896281010000108 | Threshold presence of Toxoplasma gondii DNA in specimen at point in time by molecular genetics (observable entity) |
| 114561-4 | 896291010000106 | Threshold presence of Torque teno virus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114562-2 | 896301010000107 | Threshold presence of Orthoflavivirus encephalitidis RNA in specimen at point in time by molecular genetics (observable entity) |
| 114572-1 | 896311010000105 | Threshold presence of Taenia solium DNA in specimen at point in time by molecular genetics (observable entity) |
| 114574-7 | 896321010000104 | Threshold presence of Orthoebolavirus sudanense RNA in specimen at point in time by molecular genetics (observable entity) |
| 114575-4 | 896331010000101 | Threshold presence of Strongyloides stercoralis DNA in specimen at point in time by molecular genetics (observable entity) |
| 114577-0 | 896341010000109 | Threshold presence of Streptococcus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114578-8 | 896351010000106 | Threshold presence of Streptococcus salivarius DNA in specimen at point in time by molecular genetics (observable entity) |
| 114579-6 | 896361010000108 | Threshold presence of Streptococcus pyogenes rRNA in specimen at point in time by molecular genetics (observable entity) |
| 114581-2 | 896371010000103 | Threshold presence of Streptococcus pneumoniae rRNA in specimen at point in time by molecular genetics (observable entity) |
| 114583-8 | 896381010000100 | Threshold presence of Streptococcus pneumoniae DNA in specimen at point in time by molecular genetics (observable entity) |
| 114584-6 | 896391010000102 | Threshold presence of Streptococcus mitis DNA in specimen at point in time by molecular genetics (observable entity) |
| 114585-3 | 896401010000100 | Threshold presence of Streptococcus intermedius DNA in specimen at point in time by molecular genetics (observable entity) |
| 114586-1 | 896411010000102 | Threshold presence of Streptococcus gordonii DNA in specimen at point in time by molecular genetics (observable entity) |
| 114587-9 | 896421010000108 | Threshold presence of Streptococcus equinus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114588-7 | 896431010000106 | Threshold presence of Streptococcus dysgalactiae equisimilis DNA in specimen at point in time by molecular genetics (observable entity) |
| 114589-5 | 896441010000103 | Threshold presence of Streptococcus dysgalactiae DNA in specimen at point in time by molecular genetics (observable entity) |
| 114590-3 | 896451010000101 | Threshold presence of Streptococcus constellatus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114593-7 | 896461010000104 | Threshold presence of Streptococcus anginosus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114594-5 | 896471010000109 | Threshold presence of Streptococcus agalactiae rRNA in specimen at point in time by molecular genetics (observable entity) |
| 114596-0 | 896481010000107 | Threshold presence of Streptobacillus moniliformis DNA in specimen at point in time by molecular genetics (observable entity) |
| 114597-8 | 896491010000105 | Threshold presence of Stenotrophomonas maltophilia DNA in specimen at point in time by molecular genetics (observable entity) |
| 114598-6 | 896501010000104 | Threshold presence of coagulase-negative Staphylococcus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114601-8 | 896511010000101 | Threshold presence of Staphylococcus saprophyticus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114603-4 | 896521010000107 | Threshold presence of Staphylococcus lugdunensis DNA in specimen at point in time by molecular genetics (observable entity) |
| 114604-2 | 896531010000105 | Threshold presence of Staphylococcus haemolyticus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114606-7 | 896541010000102 | Threshold presence of Staphylococcus epidermidis DNA in specimen at point in time by molecular genetics (observable entity) |
| 114607-5 | 896551010000100 | Threshold presence of methicillin resistant Staphylococcus aureus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114609-1 | 896561010000103 | Threshold presence of Staphylococcus aureus rRNA in specimen at point in time by molecular genetics (observable entity) |
| 114622-4 | 896571010000108 | Threshold presence of Alphavirus sindbis RNA in specimen at point in time by molecular genetics (observable entity) |
| 114624-0 | 896581010000106 | Threshold presence of Shigella DNA in specimen at point in time by molecular genetics (observable entity) |
| 114626-5 | 896591010000109 | Threshold presence of Serratia marcescens DNA in specimen at point in time by molecular genetics (observable entity) |
| 114628-1 | 896601010000103 | Threshold presence of Alphavirus semliki RNA in specimen at point in time by molecular genetics (observable entity) |
| 114629-9 | 896611010000100 | Threshold presence of Scopulariopsis brevicaulis DNA in specimen at point in time by molecular genetics (observable entity) |
| 114631-5 | 896621010000106 | Threshold presence of Scedosporium DNA in specimen at point in time by molecular genetics (observable entity) |
| 114632-3 | 896631010000109 | Threshold presence of Lomentospora prolificans DNA in specimen at point in time by molecular genetics (observable entity) |
| 114633-1 | 896641010000101 | Threshold presence of Scedosporium apiospermum DNA in specimen at point in time by molecular genetics (observable entity) |
| 114639-8 | 896651010000104 | Threshold presence of Severe acute respiratory syndrome coronavirus Urbani RNA in specimen at point in time by molecular genetics (observable entity) |
| 114640-6 | 896661010000102 | Threshold presence of Severe acute respiratory syndrome coronavirus RNA in specimen at point in time by molecular genetics (observable entity) |
| 114651-3 | 896671010000107 | Threshold presence of Sarcoptes scabiei DNA in specimen at point in time by molecular genetics (observable entity) |
| 114652-1 | 896681010000105 | Threshold presence of Sapovirus RNA in specimen at point in time by molecular genetics (observable entity) |
| 114654-7 | 896691010000108 | Threshold presence of Sapovirus genogroup V RNA in specimen at point in time by molecular genetics (observable entity) |
| 114655-4 | 896701010000108 | Threshold presence of Phlebovirus napoliense RNA in specimen at point in time by molecular genetics (observable entity) |
| 114656-2 | 896711010000106 | Threshold presence of Salmonella enterica enterica serovar Typhi DNA in specimen at point in time by molecular genetics (observable entity) |
| 114660-4 | 896721010000100 | Threshold presence of Salmonella DNA in specimen at point in time by molecular genetics (observable entity) |
| 114666-1 | 896731010000102 | Threshold presence of Salmonella enterica DNA in specimen at point in time by molecular genetics (observable entity) |
| 114667-9 | 896741010000105 | Threshold presence of Saint Louis encephalitis virus RNA in specimen at point in time by molecular genetics (observable entity) |
| 114668-7 | 896751010000107 | Threshold presence of Saccharomyces DNA in specimen at point in time by molecular genetics (observable entity) |
| 114669-5 | 896761010000109 | Threshold presence of Saccharomyces cerevisiae DNA in specimen at point in time by molecular genetics (observable entity) |
| 114670-3 | 896771010000104 | Threshold presence of Rubella virus RNA in specimen at point in time by molecular genetics (observable entity) |
| 114671-1 | 896781010000101 | Threshold presence of Rotavirus RNA in specimen at point in time by molecular genetics (observable entity) |
| 114672-9 | 896791010000103 | Threshold presence of Rotavirus dsRNA in specimen at point in time by molecular genetics (observable entity) |
| 114673-7 | 896801010000102 | Threshold presence of Rotavirus tritogastroenteritidis RNA in specimen at point in time by molecular genetics (observable entity) |
| 114674-5 | 896811010000104 | Threshold presence of Rotavirus betagastroenteritidis RNA in specimen at point in time by molecular genetics (observable entity) |
| 114677-8 | 896821010000105 | Threshold presence of Alphavirus rossriver RNA in specimen at point in time by molecular genetics (observable entity) |
| 114679-4 | 896831010000108 | Threshold presence of Phlebovirus riftense RNA in specimen at point in time by molecular genetics (observable entity) |
| 114680-2 | 896841010000100 | Threshold presence of Rickettsia typhus group DNA in specimen at point in time by molecular genetics (observable entity) |
| 114681-0 | 896851010000103 | Threshold presence of Rickettsia spotted fever group RNA in specimen at point in time by molecular genetics (observable entity) |
| 114682-8 | 896861010000101 | Threshold presence of Rickettsia spotted fever group DNA in specimen at point in time by molecular genetics (observable entity) |
| 114683-6 | 896871010000106 | Threshold presence of Rickettsia DNA in specimen at point in time by molecular genetics (observable entity) |
| 114684-4 | 896881010000109 | Threshold presence of Rickettsia rickettsii RNA in specimen at point in time by molecular genetics (observable entity) |
| 114685-1 | 896891010000107 | Threshold presence of Rickettsia rickettsii DNA in specimen at point in time by molecular genetics (observable entity) |
| 114686-9 | 896901010000106 | Threshold presence of Rickettsia prowazekii RNA in specimen at point in time by molecular genetics (observable entity) |
| 114687-7 | 896911010000109 | Threshold presence of Rhodotorula DNA in specimen at point in time by molecular genetics (observable entity) |
| 114689-3 | 896921010000103 | Threshold presence of Rhinovirus RNA in specimen at point in time by molecular genetics (observable entity) |
| 114692-7 | 896931010000100 | Threshold presence of Human respiratory syncytial virus B RNA in specimen at point in time by molecular genetics (observable entity) |
| 114695-0 | 896941010000108 | Threshold presence of Human respiratory syncytial virus A RNA in specimen at point in time by molecular genetics (observable entity) |
| 114696-8 | 896951010000105 | Threshold presence of Orthopneumovirus hominis A 5' untranslated region RNA in specimen at point in time by molecular genetics (observable entity) |
| 114698-4 | 896961010000107 | Threshold presence of Lyssavirus rabies RNA in specimen at point in time by molecular genetics (observable entity) |
| 114705-7 | 896971010000102 | Threshold presence of Pseudomonas aeruginosa DNA in specimen at point in time by molecular genetics (observable entity) |
| 114707-3 | 896981010000104 | Threshold presence of Pseudocowpox virus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114708-1 | 896991010000101 | Threshold presence of Providencia stuartii DNA in specimen at point in time by molecular genetics (observable entity) |
| 114709-9 | 897001010000107 | Threshold presence of Providencia rettgeri DNA in specimen at point in time by molecular genetics (observable entity) |
| 114710-7 | 897011010000105 | Threshold presence of Proteus vulgaris DNA in specimen at point in time by molecular genetics (observable entity) |
| 114711-5 | 897021010000104 | Threshold presence of Proteus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114713-1 | 897031010000101 | Threshold presence of Proteus mirabilis DNA in specimen at point in time by molecular genetics (observable entity) |
| 114714-9 | 897041010000109 | Threshold presence of Propionibacteriaceae DNA in specimen at point in time by molecular genetics (observable entity) |
| 114715-6 | 897051010000106 | Threshold presence of Prevotella intermedia DNA in specimen at point in time by molecular genetics (observable entity) |
| 114716-4 | 897061010000108 | Threshold presence of Prevotella buccae DNA in specimen at point in time by molecular genetics (observable entity) |
| 114717-2 | 897071010000103 | Threshold presence of Powassan virus RNA in specimen at point in time by molecular genetics (observable entity) |
| 114732-1 | 897081010000100 | Threshold presence of Pneumocystis murina DNA in specimen at point in time by molecular genetics (observable entity) |
| 114733-9 | 897091010000102 | Threshold presence of Pneumocystis jirovecii DNA in specimen at point in time by molecular genetics (observable entity) |
| 114735-4 | 897101010000106 | Threshold presence of Plasmodium vivax DNA in specimen at point in time by molecular genetics (observable entity) |
| 114736-2 | 897111010000109 | Threshold presence of Plasmodium DNA in specimen at point in time by molecular genetics (observable entity) |
| 114737-0 | 897121010000103 | Threshold presence of Plasmodium ovale DNA in specimen at point in time by molecular genetics (observable entity) |
| 114738-8 | 897131010000100 | Threshold presence of Plasmodium malariae DNA in specimen at point in time by molecular genetics (observable entity) |
| 114739-6 | 897141010000108 | Threshold presence of Plasmodium knowlesi DNA in specimen at point in time by molecular genetics (observable entity) |
| 114740-4 | 897151010000105 | Threshold presence of Plasmodium falciparum DNA in specimen at point in time by molecular genetics (observable entity) |
| 114741-2 | 897161010000107 | Threshold presence of Pichia DNA in specimen at point in time by molecular genetics (observable entity) |
| 114742-0 | 897171010000102 | Threshold presence of Pichia kudriavzevii DNA in specimen at point in time by molecular genetics (observable entity) |
| 114743-8 | 897181010000104 | Threshold presence of Phlebovirus RNA in specimen at point in time by molecular genetics (observable entity) |
| 114745-3 | 897191010000101 | Threshold presence of Peptostreptococcus anaerobius DNA in specimen at point in time by molecular genetics (observable entity) |
| 114746-1 | 897201010000103 | Threshold presence of Peptoniphilus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114748-7 | 897211010000100 | Threshold presence of Pasteurella multocida rRNA in specimen at point in time by molecular genetics (observable entity) |
| 114749-5 | 897221010000106 | Threshold presence of Pasteurella multocida DNA in specimen at point in time by molecular genetics (observable entity) |
| 114750-3 | 897231010000109 | Threshold presence of Human parvovirus B19 RNA in specimen at point in time by molecular genetics (observable entity) |
| 114751-1 | 897241010000101 | Threshold presence of Human parvovirus B19 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114752-9 | 897251010000104 | Threshold presence of Parvimonas micra DNA in specimen at point in time by molecular genetics (observable entity) |
| 114753-7 | 897261010000102 | Threshold presence of Parechovirus RNA in specimen at point in time by molecular genetics (observable entity) |
| 114754-5 | 897271010000107 | Threshold presence of Human parechovirus RNA in specimen at point in time by molecular genetics (observable entity) |
| 114755-2 | 897281010000105 | Threshold presence of Parapoxvirus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114756-0 | 897291010000108 | Threshold presence of Parainfluenza virus RNA in specimen at point in time by molecular genetics (observable entity) |
| 114757-8 | 897301010000109 | Threshold presence of Parainfluenza virus 4b RNA in specimen at point in time by molecular genetics (observable entity) |
| 114758-6 | 897311010000107 | Threshold presence of Parainfluenza virus 4a RNA in specimen at point in time by molecular genetics (observable entity) |
| 114765-1 | 897321010000101 | Threshold presence of Pantoea DNA in specimen at point in time by molecular genetics (observable entity) |
| 114770-1 | 897331010000103 | Threshold presence of Orthopoxvirus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114771-9 | 897341010000106 | Threshold presence of Orthobunyavirus oropoucheense RNA in specimen at point in time by molecular genetics (observable entity) |
| 114772-7 | 897351010000108 | Threshold presence of Orientia tsutsugamushi DNA in specimen at point in time by molecular genetics (observable entity) |
| 114773-5 | 897361010000105 | Threshold presence of Parapoxvirus orf DNA in specimen at point in time by molecular genetics (observable entity) |
| 114774-3 | 897371010000100 | Threshold presence of Alphavirus onyong RNA in specimen at point in time by molecular genetics (observable entity) |
| 114775-0 | 897381010000102 | Threshold presence of Norovirus RNA in specimen at point in time by molecular genetics (observable entity) |
| 114776-8 | 897391010000104 | Threshold presence of Norovirus genogroup II RNA in specimen at point in time by molecular genetics (observable entity) |
| 114778-4 | 897401010000102 | Threshold presence of Norovirus genogroup I RNA in specimen at point in time by molecular genetics (observable entity) |
| 114779-2 | 897411010000104 | Threshold presence of Nocardia DNA in specimen at point in time by molecular genetics (observable entity) |
| 114781-8 | 897421010000105 | Threshold presence of Neisseria meningitidis serogroup Y DNA in specimen at point in time by molecular genetics (observable entity) |
| 114782-6 | 897431010000108 | Threshold presence of Neisseria meningitidis serogroup X DNA in specimen at point in time by molecular genetics (observable entity) |
| 114783-4 | 897441010000100 | Threshold presence of Neisseria meningitidis serogroup W135 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114784-2 | 897451010000103 | Threshold presence of Neisseria meningitidis serogroup C DNA in specimen at point in time by molecular genetics (observable entity) |
| 114785-9 | 897461010000101 | Threshold presence of Neisseria meningitidis serogroup B DNA in specimen at point in time by molecular genetics (observable entity) |
| 114786-7 | 897471010000106 | Threshold presence of Neisseria meningitidis serogroup A DNA in specimen at point in time by molecular genetics (observable entity) |
| 114787-5 | 897481010000109 | Threshold presence of Neisseria meningitidis rRNA in specimen at point in time by molecular genetics (observable entity) |
| 114788-3 | 897491010000107 | Threshold presence of Neisseria meningitidis DNA in specimen at point in time by molecular genetics (observable entity) |
| 114789-1 | 897501010000101 | Threshold presence of Nannizzia persicolor DNA in specimen at point in time by molecular genetics (observable entity) |
| 114790-9 | 897511010000103 | Threshold presence of Nannizzia incurvata DNA in specimen at point in time by molecular genetics (observable entity) |
| 114791-7 | 897521010000109 | Threshold presence of Nannizzia gypsea DNA in specimen at point in time by molecular genetics (observable entity) |
| 114792-5 | 897531010000107 | Threshold presence of Nannizzia fulva DNA in specimen at point in time by molecular genetics (observable entity) |
| 114793-3 | 897541010000104 | Threshold presence of Nakaseomyces nivariensis DNA in specimen at point in time by molecular genetics (observable entity) |
| 114794-1 | 897551010000102 | Threshold presence of Nakaseomyces bracarensis DNA in specimen at point in time by molecular genetics (observable entity) |
| 114795-8 | 897561010000100 | Threshold presence of Naegleria fowleri DNA in specimen at point in time by molecular genetics (observable entity) |
| 114798-2 | 897571010000105 | Threshold presence of Mycoplasma rRNA in specimen at point in time by molecular genetics (observable entity) |
| 114799-0 | 897581010000108 | Threshold presence of Mycoplasma DNA in specimen at point in time by molecular genetics (observable entity) |
| 114800-6 | 897591010000106 | Threshold presence of Mycoplasma pneumoniae rRNA in specimen at point in time by molecular genetics (observable entity) |
| 114801-4 | 897601010000100 | Threshold presence of Mycoplasma penetrans DNA in specimen at point in time by molecular genetics (observable entity) |
| 114804-8 | 897611010000102 | Threshold presence of Mycoplasma hominis DNA in specimen at point in time by molecular genetics (observable entity) |
| 114805-5 | 897621010000108 | Threshold presence of Mycoplasma genitalium rRNA in specimen at point in time by molecular genetics (observable entity) |
| 114806-3 | 897631010000106 | Threshold presence of Mycoplasma genitalium DNA in specimen at point in time by molecular genetics (observable entity) |
| 114811-3 | 897641010000103 | Threshold presence of Mycoplasma fermentans DNA in specimen at point in time by molecular genetics (observable entity) |
| 114815-4 | 897651010000101 | Threshold presence of Mycobacterium ulcerans DNA in specimen at point in time by molecular genetics (observable entity) |
| 114816-2 | 897661010000104 | Threshold presence of Mycobacterium tuberculosis rRNA in specimen at point in time by molecular genetics (observable entity) |
| 114817-0 | 897671010000109 | Threshold presence of Mycobacterium tuberculosis DNA in specimen at point in time by molecular genetics (observable entity) |
| 114818-8 | 897681010000107 | Threshold presence of Mycobacterium tuberculosis complex rRNA in specimen at point in time by molecular genetics (observable entity) |
| 114819-6 | 897691010000105 | Threshold presence of Mycobacterium tuberculosis complex DNA in specimen at point in time by molecular genetics (observable entity) |
| 114820-4 | 897701010000105 | Threshold presence of Mycobacterium rRNA in specimen at point in time by molecular genetics (observable entity) |
| 114821-2 | 897711010000108 | Threshold presence of Mycobacterium DNA in specimen at point in time by molecular genetics (observable entity) |
| 114822-0 | 897721010000102 | Threshold presence of Mycobacterium marinum DNA in specimen at point in time by molecular genetics (observable entity) |
| 114823-8 | 897731010000104 | Threshold presence of Mycobacterium leprae DNA in specimen at point in time by molecular genetics (observable entity) |
| 114824-6 | 897741010000107 | Threshold presence of Mycobacterium kansasii rRNA in specimen at point in time by molecular genetics (observable entity) |
| 114825-3 | 897751010000109 | Threshold presence of Mycobacterium kansasii DNA in specimen at point in time by molecular genetics (observable entity) |
| 114826-1 | 897761010000106 | Threshold presence of Mycobacterium intracellulare rRNA in specimen at point in time by molecular genetics (observable entity) |
| 114827-9 | 897771010000101 | Threshold presence of Mycobacterium gordonae rRNA in specimen at point in time by molecular genetics (observable entity) |
| 114830-3 | 897781010000103 | Threshold presence of Mycobacterium avium subspecies avium rRNA in specimen at point in time by molecular genetics (observable entity) |
| 114831-1 | 897791010000100 | Threshold presence of Mycobacterium avium complex rRNA in specimen at point in time by molecular genetics (observable entity) |
| 114832-9 | 897801010000104 | Threshold presence of Mycobacterium avium complex DNA in specimen at point in time by molecular genetics (observable entity) |
| 114833-7 | 897811010000101 | Threshold presence of Mycobacterium abscessus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114834-5 | 897821010000107 | Threshold presence of Orthoflavivirus murrayense RNA in specimen at point in time by molecular genetics (observable entity) |
| 114835-2 | 897831010000105 | Threshold presence of Orthorubulavirus parotitidis RNA in specimen at point in time by molecular genetics (observable entity) |
| 114836-0 | 897841010000102 | Threshold presence of Morganella morganii DNA in specimen at point in time by molecular genetics (observable entity) |
| 114837-8 | 897851010000100 | Threshold presence of Moraxella catarrhalis DNA in specimen at point in time by molecular genetics (observable entity) |
| 114838-6 | 897861010000103 | Threshold presence of Orthopoxvirus monkeypox DNA in specimen at point in time by molecular genetics (observable entity) |
| 114843-6 | 897871010000108 | Threshold presence of Mobiluncus rRNA in specimen at point in time by molecular genetics (observable entity) |
| 114844-4 | 897881010000106 | Threshold presence of Betacoronavirus cameli upstream of E gene RNA in specimen at point in time by molecular genetics (observable entity) |
| 114845-1 | 897891010000109 | Threshold presence of Betacoronavirus cameli RNA in specimen at point in time by molecular genetics (observable entity) |
| 114846-9 | 897901010000108 | Threshold presence of Betacoronavirus cameli N3 gene RNA in specimen at point in time by molecular genetics (observable entity) |
| 114847-7 | 897911010000106 | Threshold presence of Betacoronavirus cameli N2 gene RNA in specimen at point in time by molecular genetics (observable entity) |
| 114848-5 | 897921010000100 | Threshold presence of Microsporum ferrugineum DNA in specimen at point in time by molecular genetics (observable entity) |
| 114849-3 | 897931010000102 | Threshold presence of Microsporum canis DNA in specimen at point in time by molecular genetics (observable entity) |
| 114850-1 | 897941010000105 | Threshold presence of Microsporum audouinii DNA in specimen at point in time by molecular genetics (observable entity) |
| 114851-9 | 897951010000107 | Threshold presence of Microsporidia DNA in specimen at point in time by molecular genetics (observable entity) |
| 114852-7 | 897961010000109 | Threshold presence of Micrococcus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114853-5 | 897971010000104 | Threshold presence of Micrococcus luteus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114854-3 | 897981010000101 | Threshold presence of Measles virus RNA in specimen at point in time by molecular genetics (observable entity) |
| 114856-8 | 897991010000103 | Threshold presence of Alphavirus mayaro RNA in specimen at point in time by molecular genetics (observable entity) |
| 114858-4 | 898001010000106 | Threshold presence of Marburg virus RNA in specimen at point in time by molecular genetics (observable entity) |
| 114859-2 | 898011010000109 | Threshold presence of Lymphocytic choriomeningitis virus RNA in specimen at point in time by molecular genetics (observable entity) |
| 114861-8 | 898021010000103 | Threshold presence of Loa loa DNA in specimen at point in time by molecular genetics (observable entity) |
| 114864-2 | 898031010000100 | Threshold presence of Listeria monocytogenes rRNA in specimen at point in time by molecular genetics (observable entity) |
| 114865-9 | 898041010000108 | Threshold presence of Listeria monocytogenes DNA in specimen at point in time by molecular genetics (observable entity) |
| 114866-7 | 898051010000105 | Threshold presence of Leptospira DNA in specimen at point in time by molecular genetics (observable entity) |
| 114867-5 | 898061010000107 | Threshold presence of Leishmania DNA in specimen at point in time by molecular genetics (observable entity) |
| 114869-1 | 898071010000102 | Threshold presence of Legionella rRNA in specimen at point in time by molecular genetics (observable entity) |
| 114870-9 | 898081010000104 | Threshold presence of Legionella DNA in specimen at point in time by molecular genetics (observable entity) |
| 114871-7 | 898091010000101 | Threshold presence of Legionella pneumophila DNA in specimen at point in time by molecular genetics (observable entity) |
| 114872-5 | 898101010000105 | Threshold presence of Legionella micdadei DNA in specimen at point in time by molecular genetics (observable entity) |
| 114873-3 | 898111010000108 | Threshold presence of Mammarenavirus lassaense RNA in specimen at point in time by molecular genetics (observable entity) |
| 114874-1 | 898121010000102 | Threshold presence of Lactobacillus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114877-4 | 898131010000104 | Threshold presence of La Crosse virus RNA in specimen at point in time by molecular genetics (observable entity) |
| 114878-2 | 898141010000107 | Threshold presence of Klebsiella variicola subspecies tropica DNA in specimen at point in time by molecular genetics (observable entity) |
| 114881-6 | 898151010000109 | Threshold presence of Klebsiella pneumoniae DNA in specimen at point in time by molecular genetics (observable entity) |
| 114883-2 | 898161010000106 | Threshold presence of Klebsiella oxytoca DNA in specimen at point in time by molecular genetics (observable entity) |
| 114885-7 | 898171010000101 | Threshold presence of Klebsiella aerogenes DNA in specimen at point in time by molecular genetics (observable entity) |
| 114887-3 | 898181010000103 | Threshold presence of Kingella kingae DNA in specimen at point in time by molecular genetics (observable entity) |
| 114888-1 | 898191010000100 | Threshold presence of John Cunningham virus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114889-9 | 898201010000102 | Threshold presence of Japanese encephalitis virus RNA in specimen at point in time by molecular genetics (observable entity) |
| 114890-7 | 898211010000104 | Threshold presence of Jamestown Canyon virus RNA in specimen at point in time by molecular genetics (observable entity) |
| 114891-5 | 898221010000105 | Threshold presence of Influenza C virus RNA in specimen at point in time by molecular genetics (observable entity) |
| 114892-3 | 898231010000108 | Threshold presence of Betainfluenzavirus influenzae Yamagata lineage RNA in specimen at point in time by molecular genetics (observable entity) |
| 114893-1 | 898241010000100 | Threshold presence of Betainfluenzavirus influenzae Victoria lineage RNA in specimen at point in time by molecular genetics (observable entity) |
| 114897-2 | 898251010000103 | Threshold presence of Influenza A virus N1 RNA in specimen at point in time by molecular genetics (observable entity) |
| 114899-8 | 898261010000101 | Threshold presence of Influenza A virus H9 RNA in specimen at point in time by molecular genetics (observable entity) |
| 114900-4 | 898271010000106 | Threshold presence of Influenza A virus H7 RNA in specimen at point in time by molecular genetics (observable entity) |
| 114902-0 | 898281010000109 | Threshold presence of Influenza A virus H6 RNA in specimen at point in time by molecular genetics (observable entity) |
| 114905-3 | 898291010000107 | Threshold presence of Influenza A virus H5 RNA in specimen at point in time by molecular genetics (observable entity) |
| 114906-1 | 898301010000108 | Threshold presence of Influenza A virus H5 Asian lineage RNA in specimen at point in time by molecular genetics (observable entity) |
| 114908-7 | 898311010000106 | Threshold presence of Influenza A virus H2 RNA in specimen at point in time by molecular genetics (observable entity) |
| 114912-9 | 898321010000100 | Threshold presence of Alphainfluenzavirus influenzae H3N2 variant RNA in specimen at point in time by molecular genetics (observable entity) |
| 114914-5 | 898331010000102 | Threshold presence of Orthoflavivirus ilheusense RNA in specimen at point in time by molecular genetics (observable entity) |
| 114916-0 | 898351010000107 | Threshold presence of Enterovirus alpharhino RNA in specimen at point in time by molecular genetics (observable entity) |
| 114918-6 | 898361010000109 | Threshold presence of Papillomavirus rRNA in specimen at point in time by molecular genetics (observable entity) |
| 114919-4 | 898371010000104 | Threshold presence of Human papillomavirus 82 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114920-2 | 898381010000101 | Threshold presence of Human papillomavirus 73 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114921-0 | 898391010000103 | Threshold presence of Human papillomavirus 70 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114922-8 | 898401010000101 | Threshold presence of Human papillomavirus 69 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114923-6 | 898411010000103 | Threshold presence of Human papillomavirus 68 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114924-4 | 898421010000109 | Threshold presence of Human papillomavirus 67 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114925-1 | 898431010000107 | Threshold presence of Human papillomavirus 66 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114930-1 | 898441010000104 | Threshold presence of Human papillomavirus 6 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114931-9 | 898451010000102 | Threshold presence of Human papillomavirus 59 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114932-7 | 898461010000100 | Threshold presence of Human papillomavirus 58 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114934-3 | 898471010000105 | Threshold presence of Human papillomavirus 56 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114935-0 | 898481010000108 | Threshold presence of Human papillomavirus 53 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114936-8 | 898491010000106 | Threshold presence of Human papillomavirus 52 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114937-6 | 898501010000100 | Threshold presence of Human papillomavirus 51 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114938-4 | 898511010000102 | Threshold presence of Human papillomavirus 45 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114939-2 | 898521010000108 | Threshold presence of Human papillomavirus 44 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114940-0 | 898531010000106 | Threshold presence of Human papillomavirus 42 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114941-8 | 898541010000103 | Threshold presence of Human papillomavirus 39 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114944-2 | 898551010000101 | Threshold presence of Human papillomavirus 35 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114946-7 | 898561010000104 | Threshold presence of Human papillomavirus 33 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114951-7 | 898571010000109 | Threshold presence of Human papillomavirus 31 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114953-3 | 898581010000107 | Threshold presence of Human papillomavirus 26 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114956-6 | 898591010000105 | Threshold presence of Human papillomavirus 18 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114966-5 | 898601010000104 | Threshold presence of Alphapapillomavirus 9 mRNA in specimen at point in time by molecular genetics (observable entity) |
| 114968-1 | 898611010000101 | Threshold presence of Human papillomavirus 16 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114971-5 | 898621010000107 | Threshold presence of Human papillomavirus 11 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114972-3 | 898631010000105 | Threshold presence of Human metapneumovirus B RNA in specimen at point in time by molecular genetics (observable entity) |
| 114974-9 | 898641010000102 | Threshold presence of Human metapneumovirus A RNA in specimen at point in time by molecular genetics (observable entity) |
| 114975-6 | 898651010000100 | Threshold presence of Human coronavirus RNA in specimen at point in time by molecular genetics (observable entity) |
| 114981-4 | 898661010000103 | Threshold presence of Human bocavirus DNA in specimen at point in time by molecular genetics (observable entity) |
| 114984-8 | 898671010000108 | Threshold presence of Human T-lymphotropic virus type 2 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114987-1 | 898681010000106 | Threshold presence of Human T-lymphotropic virus type 1 DNA in specimen at point in time by molecular genetics (observable entity) |
| 114989-7 | 898691010000109 | Threshold presence of Human immunodeficiency virus 2 RNA in specimen at point in time by molecular genetics (observable entity) |
| 114990-5 | 898701010000109 | Threshold presence of HIV 2 proviral DNA in specimen at point in time by molecular genetics (observable entity) |
| 114997-0 | 898711010000107 | Threshold presence of Human immunodeficiency virus 1 RNA in specimen at point in time by molecular genetics (observable entity) |
| 114998-8 | 898721010000101 | Threshold presence of Human immunodeficiency virus 1 proviral DNA in specimen at point in time by molecular genetics (observable entity) |
| 115002-8 | 898731010000103 | Threshold presence of Histoplasma capsulatum rRNA in specimen at point in time by molecular genetics (observable entity) |
| 115003-6 | 898741010000106 | Threshold presence of Histoplasma capsulatum DNA in specimen at point in time by molecular genetics (observable entity) |
| 115004-4 | 898751010000108 | Threshold presence of Alphavirus highlandsj RNA in specimen at point in time by molecular genetics (observable entity) |
| 115005-1 | 898761010000105 | Threshold presence of Human herpesvirus 8 DNA in specimen at point in time by molecular genetics (observable entity) |
| 115006-9 | 898771010000100 | Threshold presence of Human herpesvirus 7 DNA in specimen at point in time by molecular genetics (observable entity) |
| 115007-7 | 898781010000102 | Threshold presence of Human herpesvirus 6B DNA in specimen at point in time by molecular genetics (observable entity) |
| 115008-5 | 898791010000104 | Threshold presence of Human herpesvirus 6A DNA in specimen at point in time by molecular genetics (observable entity) |
| 115009-3 | 898801010000103 | Threshold presence of Human herpesvirus 6 DNA in specimen at point in time by molecular genetics (observable entity) |
| 115011-9 | 898811010000100 | Threshold presence of human herpes simplex virus DNA in specimen at point in time by molecular genetics (observable entity) |
| 115013-5 | 898821010000106 | Threshold presence of Human alphaherpesvirus 2 DNA in specimen at point in time by molecular genetics (observable entity) |
| 115016-8 | 898831010000109 | Threshold presence of Human alphaherpesvirus 1 DNA in specimen at point in time by molecular genetics (observable entity) |
| 115017-6 | 898841010000101 | Threshold presence of Hepatitis G virus RNA in specimen at point in time by molecular genetics (observable entity) |
| 115018-4 | 898851010000104 | Threshold presence of Hepatitis E virus RNA in specimen at point in time by molecular genetics (observable entity) |
| 115020-0 | 898861010000102 | Threshold presence of Hepatitis D virus RNA in specimen at point in time by molecular genetics (observable entity) |
| 115021-8 | 898871010000107 | Threshold presence of Hepatitis C virus RNA in specimen at point in time by molecular genetics (observable entity) |
| 115023-4 | 898881010000105 | Threshold presence of Hepatitis B virus rRNA in specimen at point in time by molecular genetics (observable entity) |
| 115025-9 | 898891010000108 | Threshold presence of Hepatitis B virus polymerase DNA in specimen at point in time by molecular genetics (observable entity) |
| 115026-7 | 898901010000107 | Threshold presence of Hepatitis B virus DNA in specimen at point in time by molecular genetics (observable entity) |
| 115027-5 | 898911010000105 | Threshold presence of Hepatitis A virus RNA in specimen at point in time by molecular genetics (observable entity) |
| 115028-3 | 898921010000104 | Threshold presence of Henipavirus hendraense RNA in specimen at point in time by molecular genetics (observable entity) |
| 115029-1 | 898931010000101 | Threshold presence of Helicobacter pylori DNA in specimen at point in time by molecular genetics (observable entity) |
| 115030-9 | 898941010000109 | Threshold presence of Bandavirus heartlandense RNA in specimen at point in time by molecular genetics (observable entity) |
| 115031-7 | 898951010000106 | Threshold presence of Hantavirus RNA in specimen at point in time by molecular genetics (observable entity) |
| 115032-5 | 898961010000108 | Threshold presence of Orthohantavirus puumalaense RNA in specimen at point in time by molecular genetics (observable entity) |
| 115033-3 | 898971010000103 | Threshold presence of Haemophilus parainfluenzae DNA in specimen at point in time by molecular genetics (observable entity) |
| 115034-1 | 898981010000100 | Threshold presence of Haemophilus influenzae rRNA in specimen at point in time by molecular genetics (observable entity) |
| 115037-4 | 898991010000102 | Threshold presence of Haemophilus influenzae DNA in specimen at point in time by molecular genetics (observable entity) |
| 115040-8 | 899001010000102 | Threshold presence of Haemophilus influenzae type b DNA in specimen at point in time by molecular genetics (observable entity) |
| 115041-6 | 899011010000104 | Threshold presence of Haemophilus influenzae type a DNA in specimen at point in time by molecular genetics (observable entity) |
| 115042-4 | 899021010000105 | Threshold presence of Haemophilus haemolyticus DNA in specimen at point in time by molecular genetics (observable entity) |
| 115043-2 | 899031010000108 | Threshold presence of Haemophilus ducreyi DNA in specimen at point in time by molecular genetics (observable entity) |
| 115044-0 | 899041010000100 | Threshold presence of Granulicatella adiacens DNA in specimen at point in time by molecular genetics (observable entity) |
| 115049-9 | 899051010000103 | Threshold presence of Giardia lamblia DNA in specimen at point in time by molecular genetics (observable entity) |
| 115050-7 | 899061010000101 | Threshold presence of Giardia lamblia 18S rRNA in specimen at point in time by molecular genetics (observable entity) |
| 115052-3 | 899071010000106 | Threshold presence of Gardnerella vaginalis rRNA in specimen at point in time by molecular genetics (observable entity) |
| 115053-1 | 899081010000109 | Threshold presence of Gardnerella vaginalis DNA in specimen at point in time by molecular genetics (observable entity) |
| 115054-9 | 899091010000107 | Threshold presence of Fusobacterium DNA in specimen at point in time by molecular genetics (observable entity) |
| 115055-6 | 899101010000103 | Threshold presence of Fusobacterium nucleatum DNA in specimen at point in time by molecular genetics (observable entity) |
| 115056-4 | 899111010000100 | Threshold presence of Fusobacterium necrophorum DNA in specimen at point in time by molecular genetics (observable entity) |
| 115057-2 | 899121010000106 | Threshold presence of Fusarium DNA in specimen at point in time by molecular genetics (observable entity) |
| 115059-8 | 899131010000109 | Threshold presence of Fusarium oxysporum DNA in specimen at point in time by molecular genetics (observable entity) |
| 115064-8 | 899141010000101 | Threshold presence of Francisella tularensis rRNA in specimen at point in time by molecular genetics (observable entity) |
| 115065-5 | 899151010000104 | Threshold presence of Francisella tularensis DNA in specimen at point in time by molecular genetics (observable entity) |
| 115066-3 | 899161010000102 | Threshold presence of Francisella tularensis holarctica rRNA in specimen at point in time by molecular genetics (observable entity) |
| 115067-1 | 899171010000107 | Threshold presence of Francisella tularensis holarctica DNA in specimen at point in time by molecular genetics (observable entity) |
| 115068-9 | 899181010000105 | Threshold presence of Francisella tularensis tularensis rRNA in specimen at point in time by molecular genetics (observable entity) |
| 115069-7 | 899191010000108 | Threshold presence of Francisella tularensis tularensis DNA in specimen at point in time by molecular genetics (observable entity) |
| 115072-1 | 899201010000106 | Threshold presence of Flavivirus RNA in specimen at point in time by molecular genetics (observable entity) |
| 115073-9 | 899211010000109 | Threshold presence of Finegoldia magna DNA in specimen at point in time by molecular genetics (observable entity) |
| 115074-7 | 899221010000103 | Threshold presence of Filaria DNA in specimen at point in time by molecular genetics (observable entity) |
| 115076-2 | 899231010000100 | Threshold presence of Exserohilum rostratum DNA in specimen at point in time by molecular genetics (observable entity) |
| 115085-3 | 899241010000108 | Threshold presence of Escherichia coli O157:H7 DNA in specimen at point in time by molecular genetics (observable entity) |
| 115087-9 | 899251010000105 | Threshold presence of Escherichia coli O157 DNA in specimen at point in time by molecular genetics (observable entity) |
| 115088-7 | 899261010000107 | Threshold presence of Escherichia coli K99 DNA in specimen at point in time by molecular genetics (observable entity) |
| 115089-5 | 899271010000102 | Threshold presence of Escherichia coli K88 DNA in specimen at point in time by molecular genetics (observable entity) |
| 115090-3 | 899281010000104 | Threshold presence of Escherichia coli K1 DNA in specimen at point in time by molecular genetics (observable entity) |
| 115099-4 | 899291010000101 | Threshold presence of enterotoxigenic Escherichia coli DNA in specimen at point in time by molecular genetics (observable entity) |
| 115101-8 | 899301010000100 | Threshold presence of enteropathogenic Escherichia coli DNA in specimen at point in time by molecular genetics (observable entity) |
| 115102-6 | 899311010000102 | Threshold presence of enteroinvasive Escherichia coli DNA in specimen at point in time by molecular genetics (observable entity) |
| 115104-2 | 899321010000108 | Threshold presence of enteroaggregative Escherichia coli DNA in specimen at point in time by molecular genetics (observable entity) |
| 115107-5 | 899331010000106 | Threshold presence of Escherichia coli DNA in specimen at point in time by molecular genetics (observable entity) |
| 115115-8 | 899341010000103 | Threshold presence of Epstein-Barr virus-encoded RNA 1 in specimen at point in time by molecular genetics (observable entity) |
| 115116-6 | 899351010000101 | Threshold presence of Epstein-Barr virus DNA in specimen at point in time by molecular genetics (observable entity) |
| 115118-2 | 899361010000104 | Threshold presence of Epidermophyton floccosum DNA in specimen at point in time by molecular genetics (observable entity) |
| 115119-0 | 899371010000109 | Threshold presence of Enterovirus RNA in specimen at point in time by molecular genetics (observable entity) |
| 115121-6 | 899381010000107 | Threshold presence of Enterovirus D68 RNA in specimen at point in time by molecular genetics (observable entity) |
| … | … | 186 more |

**Only in A (removed)** (1)

| LOINC | SCTID | FSN |
|---|---|---|
| 105085-5 | 484201010000101 | Presence of Neisseria gonorrhoeae rRNA in specimen at point in time (observable entity) |

## micro_spezifische_bestimmung — Nucleic-acid detection — amplification technique asserted

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118589004 |Threshold (property) (qualifier value)| OR 705057003 |Presence (property) (qualifier value)| OR 118584009 |Presence or identity (property) (qualifier value)|), 246093002 |Component (attribute)| = << 117174000 |Nucleic acid sequence with relative specificity for microorganism (substance)|, 246501002 |Technique (attribute)| = << 1156878000 |Molecular nucleic acid amplification technique (qualifier value)|
```

**Only in B (added)** (38)

| LOINC | SCTID | FSN |
|---|---|---|
| 112707-5 | 884181010000105 | Threshold presence of Streptococcus pneumoniae DNA in wound at point in time by probe with target amplification (observable entity) |
| 112708-3 | 884191010000108 | Threshold presence of Neisseria meningitidis DNA in wound at point in time by probe with target amplification (observable entity) |
| 112709-1 | 884201010000106 | Threshold presence of Escherichia coli DNA in wound at point in time by probe with target amplification (observable entity) |
| 112710-9 | 884211010000109 | Threshold presence of Enterococcus faecium DNA in wound at point in time by probe with target amplification (observable entity) |
| 112711-7 | 884221010000103 | Threshold presence of Streptococcus DNA in wound at point in time by probe with target amplification (observable entity) |
| 112712-5 | 884231010000100 | Threshold presence of Enterobacteriaceae DNA in wound at point in time by probe with target amplification (observable entity) |
| 112713-3 | 884241010000108 | Threshold presence of Stenotrophomonas maltophilia DNA in wound at point in time by probe with target amplification (observable entity) |
| 112714-1 | 884251010000105 | Threshold presence of Candida tropicalis DNA in wound at point in time by probe with target amplification (observable entity) |
| 112716-6 | 884261010000107 | Threshold presence of Enterococcus faecalis DNA in wound at point in time by probe with target amplification (observable entity) |
| 112717-4 | 884271010000102 | Threshold presence of Listeria monocytogenes DNA in wound at point in time by probe with target amplification (observable entity) |
| 112723-2 | 884281010000104 | Threshold presence of Candida parapsilosis DNA in wound at point in time by probe with target amplification (observable entity) |
| 112724-0 | 884291010000101 | Threshold presence of Klebsiella oxytoca DNA in wound at point in time by probe with target amplification (observable entity) |
| 112725-7 | 884301010000100 | Threshold presence of Haemophilus influenzae DNA in wound at point in time by probe with target amplification (observable entity) |
| 112726-5 | 884311010000102 | Threshold presence of Acinetobacter baumannii DNA in wound at point in time by probe with target amplification (observable entity) |
| 112727-3 | 884321010000108 | Threshold presence of Klebsiella pneumoniae DNA in wound at point in time by probe with target amplification (observable entity) |
| 112728-1 | 884331010000106 | Threshold presence of Candida albicans DNA in wound at point in time by probe with target amplification (observable entity) |
| 112729-9 | 884341010000103 | Threshold presence of Pseudomonas aeruginosa DNA in wound at point in time by probe with target amplification (observable entity) |
| 112732-3 | 884351010000101 | Threshold presence of Nakaseomyces glabratus DNA in wound at point in time by probe with target amplification (observable entity) |
| 112733-1 | 884361010000104 | Threshold presence of Candida krusei DNA in wound at point in time by probe with target amplification (observable entity) |
| 112735-6 | 884371010000109 | Threshold presence of Pseudomonas DNA in wound at point in time by probe with target amplification (observable entity) |
| 112736-4 | 884381010000107 | Threshold presence of Staphylococcus aureus DNA in wound at point in time by probe with target amplification (observable entity) |
| 112749-7 | 884461010000108 | Threshold presence of Human coronavirus 229E RNA in bronchoalveolar aspirate at point in time by probe with target amplification (observable entity) |
| 112750-5 | 884471010000103 | Threshold presence of severe acute respiratory syndrome coronavirus 2 RNA in sputum at point in time by probe with target amplification (observable entity) |
| 112755-4 | 884511010000106 | Threshold presence of Human coronavirus RNA in sputum at point in time by probe with target amplification (observable entity) |
| 112757-0 | 884521010000100 | Threshold presence of Legionella pneumophila DNA in throat at point in time by probe with target amplification (observable entity) |
| 112776-0 | 884531010000102 | Threshold presence of Human herpesvirus 8 DNA in cerebrospinal fluid at point in time by probe with target amplification (observable entity) |
| 112777-8 | 884541010000105 | Threshold presence of Human herpesvirus 8 DNA in specimen at point in time by probe with target amplification (observable entity) |
| 112778-6 | 884551010000107 | Threshold presence of human herpes simplex virus DNA in skin at point in time by probe with target amplification (observable entity) |
| 112779-4 | 884561010000109 | Threshold presence of human herpes simplex virus DNA in bronchoalveolar lavage fluid at point in time by probe with target amplification (observable entity) |
| 112780-2 | 884571010000104 | Threshold presence of Human alphaherpesvirus 2 DNA in bronchoalveolar lavage fluid at point in time by probe with target amplification (observable entity) |
| 112781-0 | 884581010000101 | Threshold presence of Human alphaherpesvirus 1 DNA in bronchoalveolar lavage fluid at point in time by probe with target amplification (observable entity) |
| 112782-8 | 884591010000103 | Threshold presence of Epstein-Barr virus DNA in bronchoalveolar lavage fluid at point in time by probe with target amplification (observable entity) |
| 112783-6 | 884601010000109 | Threshold presence of Epstein-Barr virus DNA in throat at point in time by probe with target amplification (observable entity) |
| 112894-1 | 884871010000101 | Threshold presence of Haemophilus influenzae DNA in throat at point in time by probe with target amplification (observable entity) |
| 112895-8 | 884881010000103 | Threshold presence of Streptococcus pneumoniae DNA in throat at point in time by probe with target amplification (observable entity) |
| 115795-7 | 901611010000104 | Threshold presence of Human papillomavirus 45 DNA in vagina at point in time by probe with target amplification (observable entity) |
| 115796-5 | 901621010000105 | Threshold presence of Human papillomavirus 18 DNA in vagina at point in time by probe with target amplification (observable entity) |
| 115798-1 | 901641010000100 | Threshold presence of Human papillomavirus 16 DNA in vagina at point in time by probe with target amplification (observable entity) |

## micro_spezifische_bestimmung — Nucleic-acid detection — no technique modelled

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118589004 |Threshold (property) (qualifier value)| OR 705057003 |Presence (property) (qualifier value)| OR 118584009 |Presence or identity (property) (qualifier value)|), 246093002 |Component (attribute)| = << 117174000 |Nucleic acid sequence with relative specificity for microorganism (substance)|, [0..0] 246501002 |Technique (attribute)| = *
```

**Only in B (added)** (19)

| LOINC | SCTID | FSN |
|---|---|---|
| 112628-3 | 884111010000100 | Threshold presence of Human coronavirus RNA in bronchoalveolar lavage fluid at point in time by non-probe.amp.tar (observable entity) |
| 112629-1 | 884121010000106 | Threshold presence of Human coronavirus RNA in sputum at point in time by non-probe.amp.tar (observable entity) |
| 112630-9 | 884131010000109 | Threshold presence of Mycoplasma pneumoniae DNA in sputum at point in time by non-probe.amp.tar (observable entity) |
| 112631-7 | 884141010000101 | Threshold presence of Mycoplasma pneumoniae DNA in bronchoalveolar lavage fluid at point in time by non-probe.amp.tar (observable entity) |
| 112873-5 | 884681010000102 | Threshold presence of Legionella pneumophila DNA in sputum at point in time by non-probe.amp.tar (observable entity) |
| 112874-3 | 884691010000104 | Threshold presence of Parainfluenza virus 4 RNA in throat at point in time by non-probe.amp.tar (observable entity) |
| 112875-0 | 884701010000104 | Threshold presence of Parainfluenza virus 3 RNA in throat at point in time by non-probe.amp.tar (observable entity) |
| 112876-8 | 884711010000101 | Threshold presence of Parainfluenza virus 2 RNA in throat at point in time by non-probe.amp.tar (observable entity) |
| 112877-6 | 884721010000107 | Threshold presence of Parainfluenza virus 1 RNA in throat at point in time by non-probe.amp.tar (observable entity) |
| 112878-4 | 884731010000105 | Threshold presence of Betacoronavirus cameli RNA in throat at point in time by non-probe.amp.tar (observable entity) |
| 112879-2 | 884741010000102 | Threshold presence of Influenza A virus H1 RNA in throat at point in time by non-probe.amp.tar (observable entity) |
| 112880-0 | 884751010000100 | Threshold presence of Human coronavirus OC43 RNA in throat at point in time by non-probe.amp.tar (observable entity) |
| 112881-8 | 884761010000103 | Threshold presence of Klebsiella pneumoniae DNA in synovial fluid at point in time by non-probe.amp.tar (observable entity) |
| 112882-6 | 884771010000108 | Threshold presence of Human coronavirus 229E RNA in throat at point in time by non-probe.amp.tar (observable entity) |
| 112883-4 | 884781010000106 | Threshold presence of Human coronavirus NL63 RNA in throat at point in time by non-probe.amp.tar (observable entity) |
| 112884-2 | 884791010000109 | Threshold presence of Parainfluenza virus RNA in sputum at point in time by non-probe.amp.tar (observable entity) |
| 112885-9 | 884801010000105 | Threshold presence of Betacoronavirus cameli RNA in sputum at point in time by non-probe.amp.tar (observable entity) |
| 112892-5 | 884851010000109 | Threshold presence of Human Respiratory syncytial virus RNA in sputum at point in time by non-probe.amp.tar (observable entity) |
| 112893-3 | 884861010000106 | Threshold presence of Human coronavirus HKU1 RNA in throat at point in time by non-probe.amp.tar (observable entity) |

**Only in A (removed)** (19)

| LOINC | SCTID | FSN |
|---|---|---|
| 105056-6 | 708471010000109 | Presence of Rotavirus alphagastroenteritidis RNA in specimen at point in time (observable entity) |
| 105057-4 | 484031010000104 | Presence of Plesiomonas shigelloides DNA in specimen at point in time (observable entity) |
| 105062-4 | 484061010000106 | Presence of Streptococcus pyogenes DNA in specimen at point in time (observable entity) |
| 105073-1 | 484101010000109 | Presence of Megasphaera type 1 DNA in specimen at point in time (observable entity) |
| 105075-6 | 484121010000101 | Presence of Influenza A virus RNA in specimen at point in time (observable entity) |
| 105076-4 | 484131010000103 | Presence of Influenza A virus H1 RNA in specimen at point in time (observable entity) |
| 105077-2 | 484141010000106 | Presence of human papillomavirus DNA in specimen at point in time (observable entity) |
| 105078-0 | 484151010000108 | Presence of Human coronavirus OC43 RNA in specimen at point in time (observable entity) |
| 105079-8 | 484161010000105 | Presence of Human coronavirus 229E RNA in specimen at point in time (observable entity) |
| 105084-8 | 484191010000104 | Presence of Trichomonas vaginalis rRNA in specimen at point in time (observable entity) |
| 105085-5 | 484201010000101 | Presence of Neisseria gonorrhoeae rRNA in specimen at point in time (observable entity) |
| 105875-9 | 485601010000104 | Presence of Bordetella pertussis DNA in specimen at point in time (observable entity) |
| 105876-7 | 485611010000101 | Presence of Bordetella parapertussis DNA in specimen at point in time (observable entity) |
| 105884-1 | 485681010000106 | Presence of Chlamydophila pneumoniae DNA in specimen at point in time (observable entity) |
| 105887-4 | 485711010000107 | Presence of Adenovirus DNA in specimen at point in time (observable entity) |
| 105890-8 | 709341010000102 | Presence of Yersinia enterocolitica DNA in specimen at point in time (observable entity) |
| 105892-4 | 485741010000106 | Presence of Vibrio cholerae DNA in specimen at point in time (observable entity) |
| 105898-1 | 485801010000103 | Presence of Human polyomavirus 1 DNA in specimen at point in time (observable entity) |
| 105909-6 | 485881010000105 | Presence of severe acute respiratory syndrome coronavirus 2 RNA in specimen at point in time (observable entity) |

## micro_spezifische_bestimmung — Targeted culture detection — organism specific culture technique

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118589004 |Threshold (property) (qualifier value)| OR 705057003 |Presence (property) (qualifier value)|), 246501002 |Technique (attribute)| = << 703752003 |Organism specific culture technique (qualifier value)|
```

**Only in B (added)** (1)

| LOINC | SCTID | FSN |
|---|---|---|
| 112888-3 | 884821010000102 | Threshold presence of Neisseria gonorrhoeae in penis at point in time by organism specific culture (observable entity) |

## micro_spezifische_bestimmung — Antigen detection — threshold presence of a microbial antigen

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = (118589004 |Threshold (property) (qualifier value)| OR 705057003 |Presence (property) (qualifier value)|), 246093002 |Component (attribute)| = << 116633006 |Microbial antigen (substance)|
```

**Only in B (added)** (1)

| LOINC | SCTID | FSN |
|---|---|---|
| 115347-7 | 900621010000103 | Threshold presence of Orthobornavirus bornaense antigen in specimen at point in time by molecular genetics (observable entity) |

## micro_titer — Titre — pathogen antibody titre

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 118590008 |Dilution factor expressed as titer (property) (qualifier value)|, 246093002 |Component (attribute)| = << 312301006 |Infective organism antibody (substance)|
```

**Only in B (added)** (4)

| LOINC | SCTID | FSN |
|---|---|---|
| 35694-9 | 739971010000100 | Titer of California encephalitis virus IgG in serum at point in time (observable entity) |
| 49138-1 | 743281010000108 | Titer of California encephalitis virus IgG in cerebrospinal fluid at point in time by immunofluorescence (observable entity) |
| 49140-7 | 743291010000106 | Titer of California encephalitis virus IgG in serum at point in time by immunofluorescence (observable entity) |
| 49194-4 | 743301010000107 | Titer of California encephalitis virus IgG in cerebrospinal fluid at point in time (observable entity) |

## micro_titer — Titre — all titre observables (upper bound)

```
<< 363787002 |Observable entity (observable entity)| : 370130000 |Property (attribute)| = 118590008 |Dilution factor expressed as titer (property) (qualifier value)|
```

**Only in B (added)** (2)

| LOINC | SCTID | FSN |
|---|---|---|
| 10866-2 | 883911010000101 | Titer of sulfatide IgG in serum at point in time (observable entity) |
| 21545-9 | 901791010000102 | Titer of sulfatide IgG in cerebrospinal fluid at point in time (observable entity) |

