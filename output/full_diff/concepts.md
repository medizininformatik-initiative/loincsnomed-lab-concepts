# Full Branch Diff — Active Concepts

- A = `MAIN/SNOMEDCT-LOINC/2026-03-21` @ `http://localhost:8093`
- B = `MAIN/SNOMEDCT-LOINC/2026-10-21` @ `http://localhost:8093`

| Metric | Count |
|---|---:|
| Active in A | 423,857 |
| Active in B | 430,542 |
| Only in A (removed in B) | 737 |
| Only in B (added in B)   | 7,422 |
| Active in both           | 423,120 |
| FSN changed on shared    | 12,663 |

## Removed concepts, grouped by module (A side)

| moduleId | count |
|---|---:|
| `900000000000207008` | 734 |
| `11010000107` | 3 |

## Added concepts, grouped by module (B side)

| moduleId | count |
|---|---:|
| `900000000000207008` | 5,435 |
| `11010000107` | 1,972 |
| `900000000000012004` | 15 |

## Sample: added in International module (`900000000000207008`)

_5,435 total_

- `1000481000202104` — Fish oil rich in omega-3 acids (substance)
- `1002011000202101` — Product containing only dixyrazine (medicinal product)
- `1002811000202106` — Product containing only dixyrazine in oral dose form (medicinal product form)
- `1003041000202105` — Product containing only metamizole in parenteral dose form (medicinal product form)
- `1008101000112104` — Abnormal digital rectal examination (finding)
- `101000112107` — Escherichia coli serotype O103:H19 (organism)
- `102061000146107` — Excision of condylomata acuminata of anus (procedure)
- `102371000146104` — Craniotomy and evacuation of chronic intracranial subdural hematoma (procedure)
- `102911000146109` — Injection of joint of upper limb (procedure)
- `103091561000119106` — Aspirated food in lung (disorder)
- `1031000181101` — Deinococcus aerolatus (organism)
- `1036301000112107` — Vancomycin-resistant Enterococcus gallinarum (organism)
- `103741000146102` — Drainage of hematoma (procedure)
- `104221000146104` — Excision of neoplasm of middle base of skull (procedure)
- `1047481000000108` — Able to sequence events (finding)

## Sample: added in LOINC Extension module (`11010000107`)

_1,972 total_

- `120993002` — Human herpes simplex virus antigen (substance)
- `258473003` — Semen sample (specimen)
- `873791010000100` — Volatile substance (substance)
- `873801010000104` — Gene sequence variant (morphologic abnormality)
- `873811010000101` — Targeted gene mutation analysis technique (qualifier value)
- `883801010000108` — Presence or identity of gene sequence variant in GNA11 gene in tissue or whole blood at point in time by targeted gene mutation analysis (observable entity)
- `883811010000106` — Number fraction of LRBA+ cell to CD3+CD14-CD45+ cell in blood at point in time by flow cytometry (observable entity)
- `883821010000100` — Number fraction of LRBA+ cell to CD3-CD14-CD19+CD45+ cell in blood at point in time by flow cytometry (observable entity)
- `883831010000102` — Presence or identity of Leishmania in tissue at point in time by Giemsa stain (observable entity)
- `883841010000105` — Presence or identity of Leishmania in tissue at point in time by organism specific culture (observable entity)
- `883851010000107` — Number fraction of CD3+CD26+ cell to cell in bone marrow at point in time by flow cytometry (observable entity)
- `883861010000109` — Number fraction of CD3-CD19+ cell to cell in bone marrow at point in time by flow cytometry (observable entity)
- `883871010000104` — Number fraction of CD19+CD25+ cell to cell in specimen at point in time by flow cytometry (observable entity)
- `883881010000101` — Presence or identity of MPL gene mutations tested for in tissue or whole blood at point in time by nucleic acid sequencing (observable entity)
- `883891010000103` — Arbitrary concentration of white bean IgG in serum or plasma at point in time by immunoassay (observable entity)

## Sample: removed in International module (`900000000000207008`)

_734 total_

- `106090003` — Body fluid property (observable entity)
- `106330007` — Philologist, translator/interpreter (occupation)
- `107615000` — Family Asclepiadaceae - milkweed (organism)
- `1079004` — Macular retinal cyst (disorder)
- `108313002` — Family psychotherapy procedure (regime/therapy)
- `1089021000119108` — Malignant otitis externa of left external auditory canal (disorder)
- `1091631000119100` — Malignant otitis externa of right external auditory canal (disorder)
- `109431006` — Ebstein-like malformation of mitral valve (disorder)
- `109480001` — Generalized enamel hypoplasia associated with systemic disease (disorder)
- `109481002` — Generalized enamel hypoplasia associated with fluorosis (disorder)
- `109482009` — Generalized enamel hypoplasia associated with radiation therapy (disorder)
- `109483004` — Generalized enamel hypoplasia associated with ingestion of drugs (disorder)
- `109485006` — Localized enamel hypoplasia associated with localized trauma (disorder)
- `109489000` — Localized enamel hypomineralization associated with localized trauma (disorder)
- `109540007` — Failure of exfoliation associated with lack of succedaneous tooth (disorder)

## Sample: removed in LOINC Extension module (`11010000107`)

_3 total_

- `484201010000101` — Presence of Neisseria gonorrhoeae rRNA in specimen at point in time (observable entity)
- `531681010000106` — Velocity of spermatozoa at point in time in seminal fluid (observable entity)
- `710211010000102` — Number areic of burst-forming unit erythroid in plasma at point in time (observable entity)

## Sample: FSN changed (first 25)

| conceptId | A FSN | B FSN |
|---|---|---|
| `100021010000109` | Presence of John Cunningham virus DNA in tissue at point in time by probe with target amplification (observable entity) | Threshold presence of John Cunningham virus DNA in tissue at point in time by probe with target amplification (observable entity) |
| `100041010000104` | Presence of 6-O-monoacetylmorphine in urine at point in time by confirmatory technique (observable entity) | Threshold presence of 6-O-monoacetylmorphine in urine at point in time by confirmatory technique (observable entity) |
| `100061010000100` | Presence of anti-platelet antibody in serum at point in time by flow cytometry (observable entity) | Threshold presence of anti-platelet antibody in serum at point in time by flow cytometry (observable entity) |
| `100081010000108` | Presence of Chlamydia trachomatis antibody in serum at point in time (observable entity) | Threshold presence of Chlamydia trachomatis antibody in serum at point in time (observable entity) |
| `100151010000103` | Presence of Cryptococcus antibody in serum at point in time by immunofluorescence (observable entity) | Threshold presence of Cryptococcus antibody in serum at point in time by immunofluorescence (observable entity) |
| `100171010000106` | Presence of hop specific immunoglobulin E in serum at point in time by radioallergosorbent testing (observable entity) | Threshold presence of hop specific immunoglobulin E in serum at point in time by radioallergosorbent testing (observable entity) |
| `100241010000107` | Presence of Human T-lymphotropic virus type 2 DNA in blood at point in time by probe with target amplification (observable entity) | Threshold presence of Human T-lymphotropic virus type 2 DNA in blood at point in time by probe with target amplification (observable entity) |
| `100261010000106` | Presence of glutamate in urine in 24 hours (observable entity) | Threshold presence of glutamate in urine in 24 hours (observable entity) |
| `100281010000103` | Presence of Eastern equine encephalitis virus IgM in specimen at point in time (observable entity) | Threshold presence of Eastern equine encephalitis virus IgM in specimen at point in time (observable entity) |
| `100311010000101` | Number concentration of leukocyte in seminal fluid at point in time by manual count (observable entity) | Number concentration of leukocyte in semen sample at point in time by manual count (observable entity) |
| `100321010000107` | Presence of cast in urine at point in time by automated technique (observable entity) | Threshold presence of cast in urine at point in time by automated technique (observable entity) |
| `100331010000105` | Presence of methamphetamine in umbilical cord tissue at point in time by confirmatory technique (observable entity) | Threshold presence of methamphetamine in umbilical cord tissue at point in time by confirmatory technique (observable entity) |
| `100371010000108` | Presence of chicken droppings specific immunoglobulin E in serum at point in time by radioallergosorbent testing (observable entity) | Threshold presence of chicken droppings specific immunoglobulin E in serum at point in time by radioallergosorbent testing (observable entity) |
| `100401010000106` | Presence of Varicella virus DNA in blood at point in time by probe with target amplification (observable entity) | Threshold presence of Varicella virus DNA in blood at point in time by probe with target amplification (observable entity) |
| `100411010000109` | Presence of tetrahydrocannabinol in blood at point in time by confirmatory technique (observable entity) | Threshold presence of tetrahydrocannabinol in blood at point in time by confirmatory technique (observable entity) |
| `100421010000103` | Presence of Hepatitis B core antigen antibody in body fluid at point in time (observable entity) | Threshold presence of Hepatitis B core antigen antibody in body fluid at point in time (observable entity) |
| `100511010000105` | Presence of Chlamydophila pneumoniae DNA in upper respiratory at point in time by probe with target amplification (observable entity) | Threshold presence of Chlamydophila pneumoniae DNA in upper respiratory at point in time by probe with target amplification (observable entity) |
| `100521010000104` | Presence of Toxoplasma gondii IgG in serum at point in time by dye test (observable entity) | Threshold presence of Toxoplasma gondii IgG in serum at point in time by dye test (observable entity) |
| `100541010000109` | Presence of human coronavirus 229E IgG in serum at point in time by immunoassay (observable entity) | Threshold presence of human coronavirus 229E IgG in serum at point in time by immunoassay (observable entity) |
| `100641010000105` | Presence of Bartonella quintana IgM in serum at point in time (observable entity) | Threshold presence of Bartonella quintana IgM in serum at point in time (observable entity) |
| `100681010000101` | Presence of Rubella virus antigen in uterine cervix at point in time (observable entity) | Threshold presence of Rubella virus antigen in uterine cervix at point in time (observable entity) |
| `100701010000103` | Presence of Acinetobacter baumannii DNA in bld.pos growth at point in time by probe with target amplification (observable entity) | Threshold presence of Acinetobacter baumannii DNA in bld.pos growth at point in time by probe with target amplification (observable entity) |
| `100711010000100` | Presence of dextromethorphan in urine at point in time by confirmatory technique (observable entity) | Threshold presence of dextromethorphan in urine at point in time by confirmatory technique (observable entity) |
| `100731010000109` | Presence of glucose in urine at point in time by test strip 6H post dose glucose (observable entity) | Threshold presence of glucose in urine at point in time by test strip 6H post dose glucose (observable entity) |
| `100761010000102` | Presence of Neisseria meningitidis DNA in bld.pos growth at point in time by non-probe.amp.tar (observable entity) | Threshold presence of Neisseria meningitidis DNA in bld.pos growth at point in time by non-probe.amp.tar (observable entity) |