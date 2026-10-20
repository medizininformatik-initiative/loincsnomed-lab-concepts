This section is a **proposal**, not normative content of the module. It accompanies ballot comments on 2027.0.0-ballot and shows, with working artifacts, how LOINC ValueSets for `Observation.code` can be *computed* from the LOINC Ontology instead of being maintained as hand-curated lists. Everything in this section is generated from a published rule set; nothing was edited by hand after generation.

### The problem it addresses

The module binds `Observation.code` to LOINC, but leaves open *which* LOINC codes a site should use for a given test, and which codes a data user may pool when answering a question such as "all hemoglobin values of this patient". Today both answers are lists: the MII-300 subset, local mapping tables, project-specific code lists. Lists go stale with each LOINC release, they carry no statement of *why* a code is in or out, and two lists for the same test rarely agree.

The LOINC Ontology makes the rule itself the artifact. Each LOINC laboratory term is represented there as a SNOMED CT observable with explicit attributes (what is measured, in which specimen, which property, on which scale). A ValueSet is then an expression over those attributes, and its LOINC enumeration is a derived product that can be regenerated for every release.

### What this section offers

| Page | Content | For whom |
|---|---|---|
| [How the ValueSets are built](loinc-ontology-method.html) | The LOINC Ontology attribute model, the ECL rule anatomy, the three parts of every ValueSet, expansion and versioning | implementers, terminologists |
| [ValueSets per clinical test](loinc-ontology-clinical-tests.html) | {{N_TESTS}} ValueSets, one per distinct clinical test, each with a derived Observation profile and the rule decomposed into attribute columns | implementers mapping a local catalogue, validators |
| [Use-case ValueSets per analyte](loinc-ontology-use-cases.html) | {{N_USECASE}} ValueSets over {{N_ANALYTES}} analytes, graded by what a data user may pool: everything, numeric, unit-convertible, qualitative, semiquantitative | researchers, data integration centres |

A worked example instance, [Laboratory result: hemoglobin (LOINC Ontology profile)](Observation-mii-exa-labor-loinc-ontology-hemoglobin.html), shows a result conforming to one of the derived profiles.

### At a glance

* Release used: **LOINC Ontology {{RELEASE}}** (`{{VERSION_URI}}`); the module's LOINC pin is 2.82.
* Every ValueSet carries the LOINC enumeration, the LOINC Ontology observables that have no LOINC code yet, and the rule itself as an intensional SNOMED CT include.
* All artifacts are `draft` and `experimental`. Their canonical URLs follow the module pattern and would be stable if the module adopted them.
* Generator, rule set and per-concept review tables: [{{REPO_NAME}}]({{REPO_URL}}).

### What a reviewer is asked to judge

1. Is a computed, rule-based definition the right way for the module to state which LOINC codes belong to a test?
2. Are the two layers, clinical test and use case, the right granularity for implementers and for data users?
3. Which of the pool definitions and tier choices on the following pages should the module decide differently? Each choice is visible as a rule and can be changed by editing that rule.
