# Microbiology requests (MII KDS Mikrobiologie 2027)

ECL definitions for the investigation requests of the MII KDS module
*Mikrobiologie* in its 2027 shape (one standalone Observation profile per
request, organism / specimen / method post-coordinated instead of
pre-coordinated LOINC codes). One `*_custom_ecl.json` per request family, same
format as the lab analytes in `config/`, but kept in this sub-directory on
purpose: the lab pipeline (`review_export.py`, `build_aggregation_valuesets.py`,
`export_mii_fsh.py`) globs `config/*_custom_ecl.json` non-recursively and is
component-centric, which these request-centric queries are not.

Run (the release updater does the same):

```bash
python3 scripts/compare_versions.py --config-glob "config/micro/*_custom_ecl.json" \
        --out output/micro/version_comparison.md --json-out output/micro/version_comparison.json
python3 scripts/diff_fsn_report.py --json output/micro/version_comparison.json \
        --out output/micro/added_removed.md
```

## Request → ontology pattern

The LOINC Ontology models microbiology observables with six attributes:
Property, Scale type, Direct site, Technique, Time aspect and *either*
Component (nucleic acid, antibody, antigen, organism in counts) *or* Inheres in
(organism in identity / susceptibility observables), plus Towards for the
antimicrobial substance in susceptibility. The ECL for an "organism" request
therefore tests both Component and Inheres in.

| Module profile (2027) | ValueSet rule in the module | Ontology anchor | Config |
|---|---|---|---|
| Allgemeine Kultur | 11475-1 (+ 41852-5) | Property = Presence or identity, Technique = << Culture technique, organism in Inheres in | `micro_allgemeine_kultur` |
| Allgemeine Bestimmung | 6 enumerated codes, 41852-5 preferred | Property = Presence or identity, Inheres in = << Organism, any/no technique; Property = Type for typing | `micro_allgemeine_bestimmung` |
| Spezifische Bestimmung | LOINC CLASS MICRO, PROPERTY Prid/PrThr, molecular METHOD_TYP | Component = << 117174000 (nucleic acid of microorganism), Threshold/Presence; organism specific culture; microbial antigen | `micro_spezifische_bestimmung` |
| Mikroskopie (allgemein) | Prid + Nom, 105059-0 preferred | Presence or identity + Nominal; 105059-0 has **no technique** and Inheres in = Specimen | `micro_mikroskopie` |
| Spezifische Mikroskopie | PrThr + Ord + stain METHOD_TYP | Threshold + Ordinal + Technique = << Microscopy or << Staining technique | `micro_mikroskopie` |
| Keimzahl | 49223-1, 564-5, 38436-2, 699-9 | Number concentration of an organism (Component) | `micro_keimzahl` |
| Empfindlichkeit | CLASS ABXBACT + PROPERTY Susc | Property = Susceptibility, Direct site = Microbial isolate, Towards = drug, `[0..0] Technique = << Genotype determination` | `micro_empfindlichkeit` |
| Voraussichtliche Empfindlichkeit | + METHOD_TYP Genotyping | Technique = 708060009 Genotype determination technique | `micro_empfindlichkeit` |
| Ct-Wert | PROPERTY ThrNum | Property = 1268648001 Threshold number | `micro_ct_wert` |
| Molekulare Pathogenlast | SCALE Qn + molecular METHOD_TYP | number / log number / arbitrary / log arbitrary concentration of a microbial nucleic acid | `micro_molekulare_pathogenlast` |
| Antigen/Antikörper quantitativ | SCALE Qn + immunoassay METHOD_TYP | concentration of << 312301006 Infective organism antibody or << 116633006 Microbial antigen | `micro_antigen_antikoerper_quantitativ` |
| Titer | PROPERTY Titr | Property = 118590008 Dilution factor expressed as titer, Component = infective organism antibody | `micro_titer` |
| Resistenzmechanismen / MRGN | PrThr in CLASS ABXBACT + 6 enumerated | only the organism side is expressible: Component/Inheres in = << 409793007 Antimicrobial resistant bacteria | `micro_resistenzmechanismen` |
| Avidität | 5 enumerated codes | **not in the ontology** (no avidity property, none of the codes mapped) | — |
| Befundtyp, Bartlett/Nugent, Virulenz | enumerated | document codes / scores are out of the ontology's scope; 39 of 61 virulence codes unmapped | — |

## Findings for the 2026-03-21 → 2026-10-21 update

Numbers from `output/micro/version_comparison.md`; concept lists with LOINC
codes in `output/micro/added_removed.md`.

- **Coverage of the module's enumerated codes is unchanged and low.** Of the
  96 LOINC codes enumerated in the Mikrobiologie ValueSets, 33 are in the
  LOINC Ontology, in both releases. Missing anchors include 41852-5
  (Microorganism or agent identified), all four colony-count codes, all six
  resistance-determinant codes, all five avidity codes and the five report-type
  codes. The ontology covers the targeted, fully specified observables, not
  the generic request codes the 2027 module prefers.
- **+585 nucleic-acid detection observables** (`naa_detection_any_technique`
  1,922 → 2,507). All are brand-new concepts for LOINC 2.83 codes
  (104341-3, 1126xx-x …), almost all *Threshold presence of <organism>
  DNA/RNA in specimen by molecular genetics*, i.e. generic technique
  708068002 rather than a specific amplification technique. A technique clause
  on << 1156878000 (amplification) sees only 38 of them.
- **Technique is not reliably asserted.** 288 nucleic-acid detection
  observables carry no Technique at all (LOINC METHOD_TYP `non-probe.amp.tar`
  and method-less codes); 19 of them gained a technique in 2026-10-21 while 19
  others lost it. 105059-0 (general microscopy) and 42 of the 43 new
  quantitative serology observables have no technique either. Any request ECL
  with a mandatory Technique clause silently drops these; use `[0..0]` queries
  to see what is missing.
- **Presence → Threshold** applies here too: qualitative microbiology
  observables carry Property = 118589004 Threshold with Ordinal scale since
  2026-10-21; the configs test Presence OR Threshold for comparability.
- **Smaller deltas:** +15 culture identity codes (wound depth, BAL
  Actinomyces/Nocardia, Leishmania), +16 specific microscopy codes (Gram stain
  of urethra/pleural/peritoneal fluid, light-microscopy bacteria in urine),
  +43 quantitative IgG to moulds (18409-3 …), +3 penicillin susceptibility
  codes by route (55136-6, 58085-2, 77960-3), +4 pathogen loads (West Nile
  virus RNA, CMV in amniotic fluid, log HIV-1 RNA). Susceptibility genotype
  (81), Ct values (40), colony counts (16) and typing (22) are unchanged.
- **Removed:** 107527-4 (clue cells by Gram stain) left the specific-microscopy
  set because 2026-10-21 dropped its Technique (now *Threshold presence of clue
  cell in vagina*, no Gram stain) — the technique-loss pattern above, not a
  content change. 105085-5 (N. gonorrhoeae rRNA) was inactivated. Lists in
  `added_removed.md`.
