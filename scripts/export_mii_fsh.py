#!/usr/bin/env python3
"""Render the generated ValueSets and profiles as MII-convention FSH.

Target: a checkout of medizininformatik-initiative/kerndatensatzmodul-labor
(the KDS Laborbefund module, IG-publisher layout). The output is a proposal
accompanying ballot comments, so everything is written under clearly separated
"loinc-ontology" directories and nothing of the module's own content is touched.

Writes into <out> (the module root):

  input/fsh/valuesets/loinc-ontology/aliases-loinc-ontology.fsh
  input/fsh/valuesets/loinc-ontology/tests/MII_VS_Labor_LOINC_Ontology_<Test>.fsh      (18)
  input/fsh/valuesets/loinc-ontology/aggregation/MII_VS_Labor_LOINC_Ontology_<Analyte>_<Bucket>.fsh
  input/fsh/profiles/loinc-ontology/MII_PR_Labor_LOINC_Ontology_<Test>.fsh              (18)
  input/pagecontent/loinc-ontology-valuesets.md                   (English, default language)
  input/translations/de/pagecontent/loinc-ontology-valuesets.md   (German translation)

Not written (one-time hand edits in the module, see README "MII lab module branch"):
sushi-config.yaml pages:, input/includes/menu.xml (+ de), the IG-level .po page
title, and the link line in value-sets.md.

Inputs: output/fhir/valuesets/*.json, output/fhir/aggregation/valuesets/*.json,
config/clinical_tests.json, config/aggregation_profiles.json, config/targets.json.
Run build_observation_artifacts.py and build_aggregation_valuesets.py first.
"""
import argparse
import datetime as dt
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import targets as _targets  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TEST_VS_DIR = ROOT / "output" / "fhir" / "valuesets"
AGG_VS_DIR = ROOT / "output" / "fhir" / "aggregation" / "valuesets"
CLINICAL_TESTS = ROOT / "config" / "clinical_tests.json"
AGG_PROFILES = ROOT / "config" / "aggregation_profiles.json"

LOINC_SYSTEM = "http://loinc.org"
SCT_SYSTEM = "http://snomed.info/sct"
SCT_ALIAS = "$sct-loinc-ontology"
BUCKET_SLUG = {"quantitative_convertible": "convertible"}
SKIP_BUCKETS = {"panel_order"}  # order/panel codes: review tables only, no ValueSet
PAGE = "loinc-ontology-valuesets"
TOPIC = "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl"

VS_RULESETS = """* ^meta.profile = "http://hl7.org/fhir/StructureDefinition/shareablevalueset"
* insert PR_CS_VS_Version
* insert Publisher
* insert LicenseCodeableCCBY40
* insert SnomedLicense
* insert CRMIShareableValueSet
* insert CRMIPublishableValueSet
* insert CRMIComputableValueSet
* insert CRMIKnowledgeCapabilitiesValueSet
* insert CRMIVersionPolicyStrict
* insert CRMIPackageSourceDefinitionalResource
* insert CRMIArtifactTopic({topic}, C36292)
* insert CRMIArtifactTopic({topic}, C25294)
* insert CRMIArtifactContributors
* ^status = #draft
* ^experimental = true
* ^date = "{date}"
""".replace("{topic}", TOPIC)

PR_RULESETS = """// License, CRMI profiles and CRMI extensions are INHERITED from the parent profile; re-inserting
// their ^extension[+] rulesets would duplicate the inherited entries. The version is not inherited.
* insert PR_CS_VS_Version
* insert Publisher
* insert SnomedLicense
* ^status = #draft
* ^experimental = true
* ^date = "{date}"
"""


# ── helpers ──────────────────────────────────────────────────────────────────

def fsh_str(s):
    """One-line FSH string literal."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'


def words(slug):
    return [w for w in re.split(r"[-_]+", slug) if w]


def fsh_name(prefix, slug):
    # MII_VS_Labor_LOINC_Ontology_Hemoglobin_Standard
    return prefix + "_LOINC_Ontology_" + "_".join(w.capitalize() for w in words(slug))


def fsh_id(prefix, slug):
    # mii-vs-labor-loinc-ontology-hemoglobin-standard
    return prefix + "-loinc-ontology-" + "-".join(w.lower() for w in words(slug))


def fsh_title(prefix, slug):
    return prefix + " LOINC Ontology " + " ".join(w.capitalize() for w in words(slug))


def split_includes(vs):
    """-> (loinc concepts, snomed-only concepts, ecl or None, snomed version)."""
    loinc, sct, ecl, ver = [], [], None, None
    for inc in vs["compose"]["include"]:
        if inc["system"] == LOINC_SYSTEM:
            loinc.extend(inc.get("concept", []))
        elif inc["system"] == SCT_SYSTEM:
            ver = inc.get("version", ver)
            if "filter" in inc:
                for f in inc["filter"]:
                    if f.get("property") == "constraint":
                        ecl = f["value"]
            else:
                sct.extend(inc.get("concept", []))
    return loinc, sct, ecl, ver


def ecl_short(ecl):
    """Strip the FSN labels for compact table cells."""
    return re.sub(r"\s*\|[^|]*\|", "", ecl)


def release_label(version_uri):
    m = re.search(r"/version/(\d{4})(\d{2})(\d{2})$", version_uri)
    return "{}-{}-{}".format(*m.groups()) if m else version_uri


# ── FSH renderers ────────────────────────────────────────────────────────────

def render_valueset(name, vid, title, description, purpose, loinc, sct, ecl, date, comments):
    out = ["ValueSet: {}".format(name), "Id: {}".format(vid), "Title: {}".format(fsh_str(title)),
           "Description: {}".format(fsh_str(description))]
    out.append(VS_RULESETS.replace("{date}", date).rstrip("\n"))
    out.append("* ^purpose = {}".format(fsh_str(purpose)))
    if loinc:
        out.append("// {}: LOINC enumeration ({} codes) resolved from the ECL below".format(comments, len(loinc)))
        for c in loinc:
            out.append("* $loinc#{}".format(c["code"]))
    if sct:
        out.append("// Observables of the LOINC Ontology module without a LOINC code ({})".format(len(sct)))
        for c in sct:
            out.append("* {}#{} {}".format(SCT_ALIAS, c["code"], fsh_str(c["display"])))
    if ecl:
        out.append("// The rule itself: intensional include, expandable only on a terminology server that")
        out.append("// holds the LOINC Ontology release named by the alias")
        out.append("* include codes from system {} where constraint = {}".format(SCT_ALIAS, fsh_str(ecl)))
    return "\n".join(out) + "\n"


def render_profile(test, vs_name, date, release):
    name = fsh_name("MII_PR_Labor", test["id"])
    pid = fsh_id("mii-pr-labor", test["id"])
    title = fsh_title("MII PR Labor", test["id"])
    desc = ("Proposal: Observation profile for the clinical test '{}' ({} tier), derived from "
            "MII_PR_Labor_Laboruntersuchung. Observation.code is bound (required) to the ValueSet "
            "{}, which is defined by ECL over the LOINC Ontology {}. Specimen: {}."
            .format(test["name"], test["tier"], vs_name, release, test["specimen"]))
    out = ["Profile: {}".format(name), "Parent: MII_PR_Labor_Laboruntersuchung", "Id: {}".format(pid),
           "Title: {}".format(fsh_str(title)), "Description: {}".format(fsh_str(desc)),
           PR_RULESETS.replace("{date}", date).rstrip("\n"),
           "* code from {} (required)".format(vs_name),
           "* code ^binding.description = {}".format(fsh_str(
               "LOINC codes of the clinical test, computed by ECL over the LOINC Ontology {}: {}"
               .format(release, test["ecl"])))]
    dtype = test.get("dataType")
    if dtype == "Quantity":
        out.append("* value[x] only Quantity")
        if test.get("unit"):
            out.append("* valueQuantity ^comment = {}".format(fsh_str("Expected UCUM unit: {}".format(test["unit"]))))
    elif dtype == "CodeableConcept":
        out.append("* value[x] only CodeableConcept")
    return name, pid, "\n".join(out) + "\n"


# ── page renderers ───────────────────────────────────────────────────────────

def page_en(release, version_uri, tests, test_rows, analytes, buckets, agg_index, repo_url):
    L = []
    L.append("This page is a **proposal**, not normative content of the module. It accompanies ballot comments on "
             "2027.0.0-ballot and shows, with concrete artifacts, how the LOINC ValueSets bound to `Observation.code` "
             "can be defined computably from the LOINC Ontology instead of being maintained as hand-curated lists. "
             "All artifacts on this page are generated; the generator and the review tables behind them live in "
             "[{}]({}).".format(repo_url.split("/")[-1], repo_url))
    L.append("")
    L.append("### Why the LOINC Ontology")
    L.append("")
    L.append("The [LOINC Ontology](https://loincsnomed.org) (SNOMED International and the Regenstrief Institute) "
             "represents LOINC laboratory terms as SNOMED CT observable entities with the attributes Component, "
             "Property, Scale type, Direct site (specimen), Technique and Time aspect. Every such observable carries "
             "its LOINC code as an alternate identifier. A set of LOINC codes can therefore be stated as an "
             "Expression Constraint Language (ECL) expression over those attributes, and the enumeration can be "
             "regenerated whenever a new LOINC Ontology release appears. The release used here is "
             "**LOINC Ontology {}** (`{}`).".format(release, version_uri))
    L.append("")
    L.append("Every ValueSet on this page has the same three parts:")
    L.append("")
    L.append("1. the **LOINC enumeration** (`http://loinc.org`), resolved from the ECL against that release;")
    L.append("2. observables of the LOINC Ontology module that have **no LOINC code yet**, as SNOMED CT codes;")
    L.append("3. the **ECL itself** as an intensional include, pinned to the release. It is the rule a reviewer reads, "
             "and the part a terminology server that holds the LOINC Ontology can expand directly.")
    L.append("")
    L.append("### Layer 1: ValueSets per clinical test")
    L.append("")
    L.append("One distinct clinical test (component plus tier: *standard* is the routine value a clinician means, "
             "*specialized* a clinically distinct variant such as free PSA or the LDH isoenzymes) is one ValueSet and "
             "one Observation profile derived from [Laboratory Test](StructureDefinition-mii-pr-labor-laboruntersuchung.html). "
             "The profile binds `Observation.code` to the ValueSet (required) and states the expected data type and unit. "
             "The ECL of each test constrains Component, Direct site, Property and Scale type.")
    L.append("")
    L.append("| Test | Tier | Specimen | LOINC codes | SNOMED only | ValueSet | Profile |")
    L.append("|---|---|---|--:|--:|---|---|")
    for r in test_rows:
        L.append("| {name} | {tier} | {specimen} | {n_loinc} | {n_sct} | [ValueSet](ValueSet-{vs_id}.html) | "
                 "[Profile](StructureDefinition-{pr_id}.html) |".format(**r))
    L.append("")
    L.append("### Layer 2: use-case ValueSets per analyte")
    L.append("")
    L.append("For secondary use the **use case defines the aggregation**, not a fixed list. The candidate pool of an "
             "analyte is everything mapped to its Component (any property, scale or specimen). Each pool is then "
             "classified by Scale type and Property into use-case buckets:")
    L.append("")
    for b in buckets:
        if b["id"] == "panel_order":
            L.append("* **{}**: {} These are listed in the review tables but get no ValueSet.".format(b["name"], b["description"]))
        else:
            L.append("* **{}**: {}".format(b["name"], b["description"]))
    L.append("")
    L.append("Scale type is not always asserted in the LOINC Ontology, so the classification uses Scale type *and* "
             "Property (presence properties count as qualitative; any measurement property counts as quantitative). "
             "The *complete* ValueSet carries the pool ECL as its intensional include; the other buckets are "
             "classifications of that pool and state their rule in the description. Cells link to the ValueSet and show "
             "the number of concepts.")
    L.append("")
    cols = [b for b in buckets if b["id"] != "panel_order"]
    L.append("| Analyte | Pool ECL | " + " | ".join(b["name"] for b in cols) + " |")
    L.append("|---|---|" + "|".join("--:" for _ in cols) + "|")
    for a in analytes:
        cells = []
        for b in cols:
            e = agg_index.get((a["analyte"], b["id"]))
            cells.append("[{}](ValueSet-{}.html)".format(e["n"], e["vs_id"]) if e else "–")
        L.append("| {} | `{}` | {} |".format(a["analyte"].replace("_", " "), ecl_short(a["ecl"]), " | ".join(cells)))
    L.append("")
    L.append("### What to review")
    L.append("")
    L.append("* **Expansion.** The HL7 terminology server used by the IG build does not hold the LOINC Ontology, so the "
             "SNOMED CT includes of these ValueSets cannot be expanded there and the QA report flags them. The LOINC "
             "enumerations expand as usual. A terminology server with the LOINC Ontology loaded (for example Snowstorm "
             "with the LOINC extension) expands all three parts.")
    L.append("* **Versions.** The LOINC enumerations were resolved against LOINC Ontology {}; the module pins LOINC 2.82. "
             "A code introduced or deprecated between the two is a review item, not an error of the method.".format(release))
    L.append("* **Pool definitions.** Hematocrit and erythrocyte count share the same Component (Erythrocyte), so their "
             "*complete* ValueSets are identical; the narrow test ValueSets differ. MCH is modelled on descendants of "
             "Hemoglobin and therefore also pulls in HbA1c and the hemoglobin variants. Both are pool-definition choices "
             "to be settled by the module, not properties of the LOINC Ontology.")
    L.append("* **Panel codes.** Observables with a Component but without a Property (for example the WBC differential) "
             "are order or panel codes and are excluded from result aggregation.")
    L.append("* **Tier and specimen choices** per test are a clinical decision; the ECL makes each choice explicit and "
             "reviewable.")
    L.append("")
    L.append("The review tables with one row per concept (LOINC, SCTID, FSN, bucket and reason) are published with the "
             "generator in [{}]({}).".format(repo_url.split("/")[-1], repo_url))
    return "\n".join(L) + "\n"


def page_de(release, version_uri, tests, test_rows, analytes, buckets, agg_index, repo_url):
    names_de = {
        "complete": "Vollständig", "quantitative": "Quantitativ (alle numerischen)",
        "quantitative_convertible": "Quantitativ & konvertierbar",
        "qualitative": "Qualitativ (ordinal / nominal / Nachweis)",
        "semiquantitative": "Semiquantitativ (Teststreifen)", "panel_order": "Panel / Auftragscode (ohne Property)"}
    desc_de = {
        "complete": "Alles, was auf die Komponente abgebildet ist: jede Skala, jede Property, jedes Material. "
                    "Definiert den Kandidatenpool als Obergrenze, einschließlich der generischen Grouper-Konzepte "
                    "„Measurement of X“.",
        "quantitative": "Messungen mit quantitativer Skala plus generische Messkonzepte ohne asserted Skala. Alle "
                        "numerischen Ergebnisse einschließlich Verhältnisse und Anteile.",
        "quantitative_convertible": "Quantitativ mit einer Konzentrations-Property (Masse, Stoffmenge, arbiträr, "
                                    "Anzahl, Menge), ohne Verhältnisse und Anteile. Die Menge, deren Werte sich "
                                    "tatsächlich poolen und umrechnen lassen.",
        "qualitative": "Ordinale oder nominale Skala oder Nachweis-Property. Nachweis/kein Nachweis, +/-, "
                       "Teststreifen-ähnliche Ergebnisse.",
        "semiquantitative": "Semiquantitative Skala: Teststreifen-Ablesungen, die weder streng quantitativ noch rein "
                            "qualitativ sind (z. B. Nitrit, Hämoglobin im Urin per Teststreifen).",
        "panel_order": "Observable mit Komponente, aber ohne Property (oft nur Technique, z. B. „Differential count "
                       "of white blood cells“). Strukturell ein Auftrags- oder Panelcode, der in mehrere "
                       "Einzelergebnisse zerfällt, kein einzelner Messwert."}
    L = []
    L.append("Diese Seite ist ein **Vorschlag**, kein normativer Inhalt des Moduls. Sie begleitet Ballot-Kommentare zu "
             "2027.0.0-ballot und zeigt an konkreten Artefakten, wie die an `Observation.code` gebundenen LOINC-ValueSets "
             "berechenbar aus der LOINC Ontology definiert werden können, statt als handgepflegte Listen. Alle Artefakte "
             "dieser Seite sind generiert; Generator und Review-Tabellen liegen in [{}]({}).".format(repo_url.split("/")[-1], repo_url))
    L.append("")
    L.append("### Warum die LOINC Ontology")
    L.append("")
    L.append("Die [LOINC Ontology](https://loincsnomed.org) (SNOMED International und Regenstrief Institute) bildet "
             "LOINC-Laborterme als SNOMED-CT-Observables mit den Attributen Component, Property, Scale type, Direct site "
             "(Material), Technique und Time aspect ab. Jedes dieser Observables trägt seinen LOINC-Code als alternativen "
             "Identifikator. Eine Menge von LOINC-Codes lässt sich daher als Ausdruck der Expression Constraint Language "
             "(ECL) über diese Attribute formulieren, und die Aufzählung lässt sich bei jedem neuen Release der LOINC "
             "Ontology neu erzeugen. Verwendetes Release: **LOINC Ontology {}** (`{}`).".format(release, version_uri))
    L.append("")
    L.append("Jedes ValueSet dieser Seite besteht aus denselben drei Teilen:")
    L.append("")
    L.append("1. der **LOINC-Aufzählung** (`http://loinc.org`), aus der ECL gegen dieses Release aufgelöst;")
    L.append("2. Observables des LOINC-Ontology-Moduls, die **noch keinen LOINC-Code** haben, als SNOMED-CT-Codes;")
    L.append("3. der **ECL selbst** als intensionales Include, auf das Release gepinnt. Das ist die Regel, die ein "
             "Reviewer liest, und der Teil, den ein Terminologieserver mit geladener LOINC Ontology direkt expandieren kann.")
    L.append("")
    L.append("### Ebene 1: ValueSets je klinischem Test")
    L.append("")
    L.append("Ein klinisch unterscheidbarer Test (Komponente plus Stufe: *standard* ist der Routinewert, den eine "
             "Klinikerin meint, *specialized* eine klinisch eigenständige Variante wie freies PSA oder die LDH-Isoenzyme) "
             "ist ein ValueSet und ein von [Laboruntersuchung](StructureDefinition-mii-pr-labor-laboruntersuchung.html) "
             "abgeleitetes Observation-Profil. Das Profil bindet `Observation.code` required an das ValueSet und nennt "
             "erwarteten Datentyp und Einheit. Die ECL jedes Tests schränkt Component, Direct site, Property und Scale type ein.")
    L.append("")
    L.append("| Test | Stufe | Material | LOINC-Codes | nur SNOMED | ValueSet | Profil |")
    L.append("|---|---|---|--:|--:|---|---|")
    for r in test_rows:
        L.append("| {name} | {tier} | {specimen} | {n_loinc} | {n_sct} | [ValueSet](ValueSet-{vs_id}.html) | "
                 "[Profil](StructureDefinition-{pr_id}.html) |".format(**r))
    L.append("")
    L.append("### Ebene 2: Use-Case-ValueSets je Analyt")
    L.append("")
    L.append("Für die Sekundärnutzung **definiert der Use Case die Aggregation**, nicht eine feste Liste. Der "
             "Kandidatenpool eines Analyten ist alles, was auf seine Komponente abgebildet ist (jede Property, Skala, "
             "jedes Material). Jeder Pool wird dann über Scale type und Property in Use-Case-Gruppen klassifiziert:")
    L.append("")
    for b in buckets:
        if b["id"] == "panel_order":
            L.append("* **{}**: {} Diese erscheinen in den Review-Tabellen, erhalten aber kein ValueSet.".format(names_de[b["id"]], desc_de[b["id"]]))
        else:
            L.append("* **{}**: {}".format(names_de[b["id"]], desc_de[b["id"]]))
    L.append("")
    L.append("Scale type ist in der LOINC Ontology nicht immer asserted, deshalb nutzt die Klassifikation Scale type "
             "*und* Property (Nachweis-Properties zählen als qualitativ, jede Mess-Property als quantitativ). Das "
             "ValueSet *Vollständig* trägt die Pool-ECL als intensionales Include; die übrigen Gruppen sind "
             "Klassifikationen dieses Pools und nennen ihre Regel in der Beschreibung. Die Zellen verlinken das ValueSet "
             "und zeigen die Zahl der Konzepte.")
    L.append("")
    cols = [b for b in buckets if b["id"] != "panel_order"]
    L.append("| Analyt | Pool-ECL | " + " | ".join(names_de[b["id"]] for b in cols) + " |")
    L.append("|---|---|" + "|".join("--:" for _ in cols) + "|")
    for a in analytes:
        cells = []
        for b in cols:
            e = agg_index.get((a["analyte"], b["id"]))
            cells.append("[{}](ValueSet-{}.html)".format(e["n"], e["vs_id"]) if e else "–")
        L.append("| {} | `{}` | {} |".format(a["analyte"].replace("_", " "), ecl_short(a["ecl"]), " | ".join(cells)))
    L.append("")
    L.append("### Was zu prüfen ist")
    L.append("")
    L.append("* **Expansion.** Der HL7-Terminologieserver des IG-Builds hält die LOINC Ontology nicht; die SNOMED-CT-"
             "Includes dieser ValueSets lassen sich dort nicht expandieren, und der QA-Report markiert sie. Die "
             "LOINC-Aufzählungen expandieren wie gewohnt. Ein Terminologieserver mit geladener LOINC Ontology (z. B. "
             "Snowstorm mit der LOINC-Extension) expandiert alle drei Teile.")
    L.append("* **Versionen.** Die LOINC-Aufzählungen wurden gegen LOINC Ontology {} aufgelöst; das Modul pinnt LOINC "
             "2.82. Ein zwischen beiden eingeführter oder abgekündigter Code ist ein Review-Punkt, kein Fehler der "
             "Methode.".format(release))
    L.append("* **Pool-Definitionen.** Hämatokrit und Erythrozytenzahl teilen dieselbe Komponente (Erythrocyte), ihre "
             "*vollständigen* ValueSets sind daher identisch; die engen Test-ValueSets unterscheiden sich. MCH ist über "
             "die Nachfahren von Hemoglobin modelliert und zieht deshalb auch HbA1c und die Hämoglobin-Varianten mit. "
             "Beides sind Entscheidungen zur Pool-Definition, die das Modul treffen muss, keine Eigenschaften der LOINC Ontology.")
    L.append("* **Panelcodes.** Observables mit Komponente, aber ohne Property (z. B. das Differentialblutbild) sind "
             "Auftrags- oder Panelcodes und von der Ergebnisaggregation ausgeschlossen.")
    L.append("* **Stufen- und Materialwahl** je Test sind klinische Entscheidungen; die ECL macht jede Wahl explizit und prüfbar.")
    L.append("")
    L.append("Die Review-Tabellen mit einer Zeile je Konzept (LOINC, SCTID, FSN, Gruppe und Begründung) sind mit dem "
             "Generator in [{}]({}) veröffentlicht.".format(repo_url.split("/")[-1], repo_url))
    return "\n".join(L) + "\n"


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, help="root of the kerndatensatzmodul-labor checkout")
    ap.add_argument("--date", default=dt.date.today().isoformat())
    ap.add_argument("--repo-url", default="https://github.com/medizininformatik-initiative/loincsnomed-lab-concepts")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    out = Path(args.out).expanduser().resolve()
    if not (out / "sushi-config.yaml").exists():
        sys.exit("not a module checkout (no sushi-config.yaml): {}".format(out))

    version_uri = _targets.snomed_version_uri()
    release = release_label(version_uri)
    tests_cfg = json.loads(CLINICAL_TESTS.read_text())
    tests = tests_cfg["tests"]
    buckets = json.loads(AGG_PROFILES.read_text())["buckets"]
    bucket_by_id = {b["id"]: b for b in buckets}

    vs_test_dir = out / "input" / "fsh" / "valuesets" / "loinc-ontology"
    pr_dir = out / "input" / "fsh" / "profiles" / "loinc-ontology"
    page_en_path = out / "input" / "pagecontent" / (PAGE + ".md")
    page_de_path = out / "input" / "translations" / "de" / "pagecontent" / (PAGE + ".md")

    files = {}  # path -> text

    files[vs_test_dir / "aliases-loinc-ontology.fsh"] = (
        "// LOINC Ontology (SNOMED CT extension module 11010000107), release {rel}.\n"
        "// Only the proposal ValueSets under valuesets/loinc-ontology/ use this alias; it is\n"
        "// deliberately NOT in aliases.fsh, whose $sct/$loinc pins are tied to the expansion\n"
        "// manifest by scripts/terminology-pins.test.mjs.\n"
        "Alias: {alias} = http://snomed.info/sct|{uri}\n".format(rel=release, alias=SCT_ALIAS, uri=version_uri))

    # Layer 1: tests
    test_rows = []
    for t in tests:
        vs = json.loads((TEST_VS_DIR / "{}.json".format(t["id"])).read_text())
        loinc, sct, ecl, _ = split_includes(vs)
        vs_name = fsh_name("MII_VS_Labor", t["id"])
        vs_id = fsh_id("mii-vs-labor", t["id"])
        desc = ("Proposal: LOINC codes of the clinical test '{}' ({} tier, specimen {}), computed by ECL over the "
                "LOINC Ontology {}. Parts: LOINC enumeration ({}), LOINC Ontology observables without LOINC code ({}), "
                "and the ECL as an intensional include. ECL: {}"
                .format(t["name"], t["tier"], t["specimen"], release, len(loinc), len(sct), t["ecl"]))
        purpose = ("Guidance for binding Observation.code of the MII laboratory test profile to a computably defined "
                   "LOINC set; accompanies ballot comments on 2027.0.0-ballot. Generated, not hand-curated.")
        files[vs_test_dir / "tests" / (vs_name + ".fsh")] = render_valueset(
            vs_name, vs_id, fsh_title("MII VS Labor", t["id"]), desc, purpose, loinc, sct, ecl, args.date,
            "Clinical test '{}'".format(t["name"]))
        pr_name, pr_id, pr_text = render_profile(t, vs_name, args.date, release)
        files[pr_dir / (pr_name + ".fsh")] = pr_text
        test_rows.append({"name": t["name"], "tier": t["tier"], "specimen": t["specimen"],
                          "n_loinc": len(loinc), "n_sct": len(sct), "vs_id": vs_id, "pr_id": pr_id})

    # Layer 2: aggregation
    analytes, seen = [], set()
    agg_index = {}
    for p in sorted(AGG_VS_DIR.glob("*.json")):
        vs = json.loads(p.read_text())
        bucket_id = vs["_bucket"]
        if bucket_id in SKIP_BUCKETS:
            continue
        analyte = vs["id"][: -(len(bucket_id.replace("_", "-")) + 1)].replace("-", "_")
        loinc, sct, ecl, _ = split_includes(vs)
        pool_ecl = vs["_ecl"]
        if analyte not in seen:
            seen.add(analyte)
            analytes.append({"analyte": analyte, "ecl": pool_ecl})
        b = bucket_by_id[bucket_id]
        slug = "{}-{}".format(analyte, BUCKET_SLUG.get(bucket_id, bucket_id))
        vs_name = fsh_name("MII_VS_Labor", slug)
        vs_id = fsh_id("mii-vs-labor", slug)
        n = len(loinc) + len(sct)
        agg_index[(analyte, bucket_id)] = {"vs_id": vs_id, "n": n}
        desc = ("Proposal: use-case ValueSet '{}' for the analyte {} ({}). Candidate pool = {} against the LOINC "
                "Ontology {}. {} concepts ({} with LOINC). {}"
                .format(b["name"], analyte.replace("_", " "), b["description"], pool_ecl, release, n, len(loinc),
                        "The pool ECL is carried as an intensional include." if ecl else
                        "Classification of the pool by Scale type and Property; the rule is stated above."))
        purpose = ("Guidance for use-case-driven aggregation of laboratory results in secondary use; accompanies "
                   "ballot comments on 2027.0.0-ballot. Generated, not hand-curated.")
        files[vs_test_dir / "aggregation" / (vs_name + ".fsh")] = render_valueset(
            vs_name, vs_id, fsh_title("MII VS Labor", slug), desc, purpose, loinc, sct, ecl, args.date,
            "Analyte {}, bucket {}".format(analyte, bucket_id))
    analytes.sort(key=lambda a: a["analyte"])

    files[page_en_path] = page_en(release, version_uri, tests, test_rows, analytes, buckets, agg_index, args.repo_url)
    files[page_de_path] = page_de(release, version_uri, tests, test_rows, analytes, buckets, agg_index, args.repo_url)

    print("LOINC Ontology {} -> {}".format(release, out))
    print("  {} test ValueSets, {} profiles, {} aggregation ValueSets, 2 pages".format(
        len(test_rows), len(test_rows), len(agg_index)))
    if args.dry_run:
        for p in sorted(files):
            print("  would write", p.relative_to(out))
        return
    for d in (vs_test_dir, pr_dir):
        if d.exists():
            shutil.rmtree(d)
    for p, text in files.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    print("  written")


if __name__ == "__main__":
    main()
