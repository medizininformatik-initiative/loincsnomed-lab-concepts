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
  input/fsh/instances/loinc-ontology/*.fsh                        (worked examples, from templates/mii/fsh)
  input/pagecontent/loinc-ontology-{valuesets,method,clinical-tests,use-cases}.md        (English)
  input/translations/de/pagecontent/loinc-ontology-*.md           (German translation)

Page prose lives in templates/mii/pages/<page>.<lang>.md with {{PLACEHOLDERS}} for the
generated tables and numbers; edit the prose there, never in the module.

Not written (one-time hand edits in the module, see README "MII lab module branch"):
sushi-config.yaml pages:, input/includes/menu.xml (+ de), the IG-level .po page
titles, the link line in value-sets.md and the example line in examples.md (en + de).

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
LOINC_VERSION = "2.83"  # the LOINC release the LOINC Ontology 2026-10-21 is built on
LOINC_ALIAS = "$loinc-ontology-loinc"  # own pin; the module's $loinc is tied to the expansion manifest
BUCKET_SLUG = {"quantitative_convertible": "convertible"}
SKIP_BUCKETS = {"panel_order"}  # order/panel codes: review tables only, no ValueSet
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
    """-> (loinc concepts the rule selected, snomed-only concepts, ecl or None, snomed version).
    Hand-added ontology-gap codes (`_extra_loinc`) are left out of the first list; render them separately."""
    loinc, sct, ecl, ver = [], [], None, None
    extra = {e["code"] for e in vs.get("_extra_loinc", [])}
    for inc in vs["compose"]["include"]:
        if inc["system"] == LOINC_SYSTEM:
            loinc.extend(c for c in inc.get("concept", []) if c["code"] not in extra)
        elif inc["system"] == SCT_SYSTEM:
            ver = inc.get("version", ver)
            if "filter" in inc:
                for f in inc["filter"]:
                    if f.get("property") == "constraint":
                        ecl = f["value"]
            else:
                sct.extend(inc.get("concept", []))
    return loinc, sct, ecl, ver


def module_loinc_pin(out):
    """The LOINC version the module's own `$loinc` alias pins (input/fsh/aliases.fsh), or None."""
    m = re.search(r"^Alias:\s*\$loinc\s*=\s*http://loinc\.org\|(\S+)", (out / "input" / "fsh" / "aliases.fsh").read_text(), re.M)
    return m.group(1) if m else None


def loinc_codes_first_released(loinc_csv, codes, version):
    """[(code, long common name)] of `codes` whose VersionFirstReleased in Loinc.csv equals `version`."""
    import csv
    csv.field_size_limit(10 ** 8)
    hits = []
    with loinc_csv.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["LOINC_NUM"] in codes and row.get("VersionFirstReleased") == version:
                hits.append((row["LOINC_NUM"], row["LONG_COMMON_NAME"]))
    return sorted(hits)


def load_loinc_lab_terms(loinc_csv):
    """Laboratory terms (CLASSTYPE 1, not DEPRECATED) of Loinc.csv, the columns the survey needs."""
    import csv
    csv.field_size_limit(10 ** 8)
    out = []
    with loinc_csv.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["CLASSTYPE"] == "1" and row["STATUS"] != "DEPRECATED":
                out.append({"code": row["LOINC_NUM"], "component": row["COMPONENT"], "property": row["PROPERTY"],
                            "system": row["SYSTEM"], "name": row["LONG_COMMON_NAME"], "status": row["STATUS"]})
    return out


def loinc_survey(terms, spec, pool_codes, test_codes):
    """Recall of the LOINC Ontology pool against LOINC's own terms of the analyte.
    spec = {component, property, system}: regexes on the LOINC parts (keys optional)."""
    def hit(r):
        return all(re.search(spec[k], r[k]) for k in ("component", "property", "system") if spec.get(k))
    matched = [r for r in terms if hit(r)]
    outside = sorted((r for r in matched if r["code"] not in pool_codes), key=lambda r: r["name"])
    pattern = "; ".join("{} ~ {}".format(k.capitalize(), spec[k]) for k in ("component", "property", "system") if spec.get(k))
    return {"pattern": pattern, "n_total": len(matched), "n_pool": len(matched) - len(outside),
            "outside": outside, "n_tests": sum(1 for r in matched if r["code"] in test_codes)}


def ecl_short(ecl):
    """Strip the FSN labels for compact table cells."""
    return re.sub(r"\s*\|[^|]*\|", "", ecl)


def release_label(version_uri):
    m = re.search(r"/version/(\d{4})(\d{2})(\d{2})$", version_uri)
    return "{}-{}-{}".format(*m.groups()) if m else version_uri


# ── FSH renderers ────────────────────────────────────────────────────────────

def render_valueset(name, vid, title, description, purpose, loinc, sct, ecl, date, comments, extra=()):
    out = ["ValueSet: {}".format(name), "Id: {}".format(vid), "Title: {}".format(fsh_str(title)),
           "Description: {}".format(fsh_str(description))]
    out.append(VS_RULESETS.replace("{date}", date).rstrip("\n"))
    out.append("* ^purpose = {}".format(fsh_str(purpose)))
    if loinc:
        out.append("// {}: LOINC enumeration ({} codes, LOINC {}) resolved from the ECL below".format(
            comments, len(loinc), LOINC_VERSION))
        for c in loinc:
            out.append("* {}#{}".format(LOINC_ALIAS, c["code"]))
    if extra:
        out.append("// Ontology gap: LOINC codes the LOINC Ontology release does not model, so no rule can reach them.")
        out.append("// Added by hand and documented on the analyte review page; to be removed once the release models them.")
        for e in extra:
            out.append("* {}#{} // {}".format(LOINC_ALIAS, e["code"], e["display"]))
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
               "LOINC codes of the clinical test, computed by ECL over the LOINC Ontology {}: `{}`"
               .format(release, test["ecl"])))]
    dtype = test.get("dataType")
    if dtype == "Quantity":
        out.append("* value[x] only Quantity")
        if test.get("unit"):
            out.append("* valueQuantity ^comment = {}".format(fsh_str("Expected UCUM unit: {}".format(test["unit"]))))
    elif dtype == "CodeableConcept":
        out.append("* value[x] only CodeableConcept")
    return name, pid, "\n".join(out) + "\n"


# ── ECL decomposition + page rendering ───────────────────────────────────────

TEMPLATES = ROOT / "templates" / "mii"
PAGES = ["loinc-ontology-valuesets", "loinc-ontology-method", "loinc-ontology-clinical-tests",
         "loinc-ontology-use-cases"]
ATTR_NAMES = {"246093002": "Component", "704327008": "Direct site", "370130000": "Property",
              "370132008": "Scale type", "246501002": "Technique", "370134009": "Time aspect",
              "704319004": "Inheres in", "704321002": "Characterizes", "704320005": "Towards",
              "718497002": "Inherent location", "704326004": "Precondition",
              "704324001": "Process output", "704325000": "Relative to", "704323007": "Process duration"}
ATTR_ORDER = ["Component", "Inheres in", "Process output", "Relative to", "Direct site", "Property", "Scale type",
              "Technique", "Time aspect"]


def _term(label):
    """'<< 38082009 |Hemoglobin (substance)|' -> '<< Hemoglobin'; handles '<', '<<', OR-groups and
    'A MINUS (B OR C)' groups (the blood block)."""
    label = label.strip()
    while label.startswith("(") and label.endswith(")") and _balanced(label[1:-1]):
        label = label[1:-1].strip()
    left, right = split_top_minus(label)
    if right is not None:
        return "{} minus ({})".format(_term(left), _term(right))
    if " OR " in label:
        return " or ".join(_term(x) for x in _split_top(label, " OR ") if x.strip())
    prefix = "<< " if label.startswith("<<") else ("< " if label.startswith("<") else "")
    m = re.search(r"\|([^|]*)\|", label)
    name = m.group(1).strip() if m else label.lstrip("<").strip()
    while True:  # drop semantic tags, also doubled ones like '(property) (qualifier value)'
        n2 = re.sub(r"\s*\([^()]*\)\s*$", "", name)
        if n2 == name:
            break
        name = n2
    return prefix + name


def _split_top(text, sep=","):
    """Split on `sep` (one or more characters) outside |labels| and outside parentheses."""
    parts, buf, inside, depth, i = [], "", False, 0, 0
    while i < len(text):
        ch = text[i]
        if ch == "|":
            inside = not inside
        elif not inside:
            depth += {"(": 1, ")": -1}.get(ch, 0)
        if not inside and depth == 0 and text.startswith(sep, i):
            parts.append(buf); buf = ""
            i += len(sep)
            continue
        buf += ch
        i += 1
    parts.append(buf)
    return parts


def _balanced(text):
    inside, depth = False, 0
    for ch in text:
        if ch == "|":
            inside = not inside
        elif not inside:
            depth += {"(": 1, ")": -1}.get(ch, 0)
            if depth < 0:
                return False
    return depth == 0


def split_top_minus(ecl):
    """-> (left, right) at a top-level ' MINUS ' (outside |labels| and parentheses), else (ecl, None)."""
    inside, depth, i = False, 0, 0
    while i < len(ecl):
        ch = ecl[i]
        if ch == "|":
            inside = not inside
        elif not inside:
            depth += {"(": 1, ")": -1}.get(ch, 0)
            if depth == 0 and ecl.startswith(" MINUS ", i):
                return ecl[:i], ecl[i + len(" MINUS "):]
        i += 1
    return ecl, None


def parse_ecl(ecl):
    """-> (focus, [(attribute name, value text)]) for the ECL shapes used in this project:
    'focus : attr = value, ...', focus-only, and 'A MINUS (A, attr = *)' (attribute absent)."""
    ecl = ecl.strip()
    ecl, minus = split_top_minus(ecl)
    ecl = ecl.strip()
    if minus is not None and ecl.startswith("(") and ecl.endswith(")"):
        ecl = ecl[1:-1].strip()
    if ":" not in ecl:
        focus, rows = _term(ecl), []
    else:
        focus_s, refinement = ecl.split(":", 1)
        focus, rows = _term(focus_s), []
        for part in _split_top(refinement):
            if "=" not in part:
                continue
            negated = "!=" in part
            attr, value = (part.split("!=", 1) if negated else part.split("=", 1))
            aid = re.search(r"\d{6,}", attr)
            aname = ATTR_NAMES.get(aid.group(0), _term(attr)) if aid else attr.strip()
            rows.append((aname, ("not " if negated else "") + _term(value)))
    if minus:  # the subtrahend names the attribute that must be absent
        m = re.search(r"(\d{6,}) \|[^|]*\| = \*", minus)
        if m:
            rows.append((ATTR_NAMES.get(m.group(1), m.group(1)), "(none)"))
    if "Component" not in dict(rows) and not focus.endswith("Observable entity"):
        rows.insert(0, ("Component", focus + " [observable]"))  # rule selects a focus concept, not a Component
    return focus, rows


def attr_columns(rows_by_test):
    cols = [a for a in ATTR_ORDER if any(a in dict(r) for r in rows_by_test)]
    extra = sorted({a for r in rows_by_test for a, _ in r} - set(cols))
    return cols + extra


def md_cell(s):
    """Table cell text. ECL operators go into a code span: the IG Publisher's markdown
    renderer turns a bare '<<' into a guillemet."""
    s = s.replace("|", "\\|")
    return "`{}`".format(s) if "<" in s else s


def tests_table(test_rows, lang):
    cols = attr_columns([r["attrs"] for r in test_rows])
    if lang == "en":
        head = ["Test", "Tier"] + cols + ["LOINC", "SNOMED only", "ValueSet", "Profile"]
        vs, pr = "ValueSet", "Profile"
    else:
        head = ["Test", "Stufe"] + cols + ["LOINC", "nur SNOMED", "ValueSet", "Profil"]
        vs, pr = "ValueSet", "Profil"
    L = ["| " + " | ".join(head) + " |", "|---|---|" + "|".join("---" for _ in cols) + "|--:|--:|---|---|"]
    for r in test_rows:
        d = {}
        for a, v in r["attrs"]:
            d[a] = (d[a] + "; " + v) if a in d else v
        cells = ["[{}]({}.html)".format(r["name"], analyte_page_id(r["analyte"])), r["tier"]] + [md_cell(d.get(c, "")) for c in cols] + [
            str(r["n_loinc"]), str(r["n_sct"]),
            "[{}](ValueSet-{}.html)".format(vs, r["vs_id"]),
            "[{}](StructureDefinition-{}.html)".format(pr, r["pr_id"])]
        L.append("| " + " | ".join(cells) + " |")
    return "\n".join(L)


def pool_label(ecl):
    """Compact pool description: the Component, plus any further refinement the pool carries
    ('Erythrocyte; << Volume fraction'); a pool without Component names its attribute."""
    focus, rows = parse_ecl(ecl)
    real = [(a, v) for a, v in rows if not v.endswith(" [observable]")]
    if not real:
        return focus
    return "; ".join(v if a == "Component" else "{} {}".format(a, v) for a, v in real)


def usecase_table(analytes, buckets, agg_index, lang):
    names = {"en": {"complete": "Complete", "quantitative": "Quantitative", "quantitative_convertible": "Convertible",
                    "qualitative": "Qualitative", "semiquantitative": "Semi-quantitative"},
             "de": {"complete": "Vollständig", "quantitative": "Quantitativ", "quantitative_convertible": "Konvertierbar",
                    "qualitative": "Qualitativ", "semiquantitative": "Semiquantitativ"}}[lang]
    cols = [b for b in buckets if b["id"] in names]
    head = ("| Analyte | Pool (Component) | " if lang == "en" else "| Analyt | Pool (Component) | ") + \
           " | ".join(names[b["id"]] for b in cols) + " |"
    L = [head, "|---|---|" + "|".join("--:" for _ in cols) + "|"]
    for a in analytes:
        pool = pool_label(a["ecl"])
        cells = []
        for b in cols:
            e = agg_index.get((a["analyte"], b["id"]))
            cells.append("[{}](ValueSet-{}.html)".format(e["n"], e["vs_id"]) if e else "–")
        L.append("| [{}]({}.html) | {} | {} |".format(a["analyte"].replace("_", " "), analyte_page_id(a["analyte"]), md_cell(pool), " | ".join(cells)))
    return "\n".join(L)


def example_ecl_rows(tests, lang):
    t = next(x for x in tests if x["id"] == "hemoglobin-standard")
    focus, rows = parse_ecl(t["ecl"])
    if lang == "en":
        L = ["The same rule, decomposed as the tables on the following pages show it:", "",
             "| Attribute | Value | Reading |", "|---|---|---|"]
        reading = {"Component": "exactly this substance", "Direct site": "this specimen or any subtype",
                   "Property": "this property or any subtype", "Scale type": "this scale or any subtype"}
    else:
        L = ["Dieselbe Regel, zerlegt wie in den Tabellen der folgenden Seiten:", "",
             "| Attribut | Wert | Lesart |", "|---|---|---|"]
        reading = {"Component": "genau diese Substanz", "Direct site": "dieses Material oder ein Subtyp",
                   "Property": "diese Property oder ein Subtyp", "Scale type": "diese Skala oder ein Subtyp"}
    for a, v in rows:
        L.append("| {} | {} | {} |".format(a, md_cell(v), reading.get(a, "")))
    return "\n".join(L)


def recall_table(analytes, survey, lang):
    """Per analyte: LOINC terms matching the analyte's LOINC pattern, how many the pool reaches, how many the
    per-test ValueSets enumerate."""
    if not survey:
        return ("*(LOINC recall table: run the generator with `--loinc-csv` to produce it.)*" if lang == "en" else
                "*(LOINC-Recall-Tabelle: den Generator mit `--loinc-csv` ausführen, um sie zu erzeugen.)*")
    head = ("| Analyte | LOINC pattern | LOINC terms | in the pool | not in the pool | in per-test ValueSets |" if lang == "en" else
            "| Analyt | LOINC-Muster | LOINC-Terme | im Pool | nicht im Pool | in ValueSets je Laborparameter |")
    L = [head, "|---|---|--:|--:|--:|--:|"]
    for a in analytes:
        s = survey.get(a["analyte"])
        if not s:
            continue
        L.append("| [{}]({}.html) | `{}` | {} | {} | {} | {} |".format(
            a["analyte"].replace("_", " "), analyte_page_id(a["analyte"]), s["pattern"], s["n_total"],
            s["n_pool"], len(s["outside"]), s["n_tests"]))
    return "\n".join(L)


def render_pages(lang, ctx, tests, test_rows, analytes, buckets, agg_index, survey=None):
    subst = dict(ctx)
    subst["TESTS_TABLE"] = tests_table(test_rows, lang)
    subst["USECASE_TABLE"] = usecase_table(analytes, buckets, agg_index, lang)
    subst["RECALL_TABLE"] = recall_table(analytes, survey or {}, lang)
    subst["EXAMPLE_ECL_ROWS"] = example_ecl_rows(tests, lang)
    out = {}
    for page in PAGES:
        text = (TEMPLATES / "pages" / "{}.{}.md".format(page, lang)).read_text(encoding="utf-8")
        for k, v in subst.items():
            text = text.replace("{{" + k + "}}", str(v))
        left = re.findall(r"{{[A-Z_]+}}", text)
        if left:
            sys.exit("unreplaced placeholders in {}.{}: {}".format(page, lang, left))
        out[page] = text
    return out


# ── analyte subpages (pool, per-test included/excluded with reasons, discussion) ──

POOL_ATTRS = ROOT / "output" / "fhir" / "aggregation" / "pool_attributes.json"
SHOW_ATTRS = ["Direct site", "Property", "Scale type", "Technique"]
L10N = {
    "en": {"name": "LOINC name", "fails": "Fails", "included": "Included", "excluded": "Excluded from the pool",
           "gap": "Ontology gap: added by hand", "gap_note": "Codes the rule cannot reach because the LOINC Ontology {release} does not model them. They are part of the ValueSet's LOINC enumeration and are listed here, not in the pool tables.",
           "survey": "LOINC terms of the analyte outside the pool", "survey_cols": "| LOINC | LOINC name | Property | System |",
           "survey_note": "Recall check against LOINC {lv} itself: {n_total} laboratory terms match the analyte's LOINC pattern ({pattern}); {n_pool} of them are in the pool, {n_out} are not. A term is outside the pool when the LOINC Ontology models it with another Component, or not at all. Each of these is either a modelling difference to accept or a change request to the LOINC Ontology.",
           "survey_none": "Recall check against LOINC {lv} itself: all {n_total} laboratory terms that match the analyte's LOINC pattern ({pattern}) are in the pool.",
           "discussion": "Discussion", "pool": "The pool and its use-case buckets", "bucket": "Bucket",
           "reason": "Reason", "rule": "Rule", "attribute": "Attribute", "value": "Value",
           "specimens": "Specimens among the included codes", "techniques": "Techniques among the included codes",
           "none": "(none)", "no_attr": "–",
           "because": "Excluded because {} does not match ({})", "because_multi": "Excluded because {} do not match ({})",
           "because_neg": "Excluded because the concept has a {} ({})",
           "intro": ("This page is the review material for the analyte **{analyte}** of the "
                     "[LOINC Ontology proposal](loinc-ontology-valuesets.html): the candidate pool as the LOINC Ontology "
                     "{release} defines it, and for every clinical test (Laborparameter) of the analyte which pool concepts "
                     "the rule selects, which it leaves out and on which attribute. The method is explained under "
                     "[How the ValueSets are built](loinc-ontology-method.html)."),
           "pool_intro": "Candidate pool: `{ecl}` ({n} concepts, {n_loinc} with a LOINC code). Use-case ValueSets: {links}.",
           "test_intro": "ValueSet [{vs}](ValueSet-{vs}.html), profile [{pr}](StructureDefinition-{pr}.html). The rule selects {n_inc} of the {n_pool} pool concepts.",
           "auto_note": "Points a reviewer should settle for this test:",
           "pool_note": "One row per pool concept with the attributes the classification uses; the bucket is the use-case ValueSet the concept lands in.",
           "and": " and ", "comma": ", ",
           "unmodelled": "{} of these have no {} attribute in this release at all (the LOINC system part is not modelled yet), so the rule cannot see them: {}."},
    "de": {"name": "LOINC-Name", "fails": "Scheitert an", "included": "Enthalten", "excluded": "Aus dem Pool ausgeschlossen",
           "gap": "Ontologie-Lücke: von Hand ergänzt", "gap_note": "Codes, die die Regel nicht erreichen kann, weil die LOINC Ontology {release} sie nicht modelliert. Sie gehören zur LOINC-Aufzählung des ValueSets und stehen hier, nicht in den Pool-Tabellen.",
           "survey": "LOINC-Terme des Analyten außerhalb des Pools", "survey_cols": "| LOINC | LOINC-Name | Property | System |",
           "survey_note": "Recall-Prüfung gegen LOINC {lv} selbst: {n_total} Laborterme passen auf das LOINC-Muster des Analyten ({pattern}); {n_pool} davon liegen im Pool, {n_out} nicht. Ein Term liegt außerhalb des Pools, wenn die LOINC Ontology ihn mit einer anderen Component modelliert oder gar nicht. Jeder davon ist entweder ein hinzunehmender Modellierungsunterschied oder ein Change Request an die LOINC Ontology.",
           "survey_none": "Recall-Prüfung gegen LOINC {lv} selbst: alle {n_total} Laborterme, die auf das LOINC-Muster des Analyten passen ({pattern}), liegen im Pool.",
           "discussion": "Diskussion", "pool": "Der Pool und seine Use-Case-Gruppen", "bucket": "Gruppe",
           "reason": "Begründung", "rule": "Regel", "attribute": "Attribut", "value": "Wert",
           "specimens": "Materialien unter den enthaltenen Codes", "techniques": "Techniken unter den enthaltenen Codes",
           "none": "(keine)", "no_attr": "–",
           "because": "Ausgeschlossen, weil {} nicht passt ({})", "because_multi": "Ausgeschlossen, weil {} nicht passen ({})",
           "because_neg": "Ausgeschlossen, weil das Konzept eine {} hat ({})",
           "intro": ("Diese Seite ist das Review-Material für den Analyten **{analyte}** des "
                     "[LOINC-Ontology-Vorschlags](loinc-ontology-valuesets.html): der Kandidatenpool, wie ihn die LOINC "
                     "Ontology {release} definiert, und für jeden Laborparameter des Analyten, welche Poolkonzepte die "
                     "Regel auswählt, welche sie auslässt und an welchem Attribut. Die Methode ist unter "
                     "[Wie die ValueSets gebaut werden](loinc-ontology-method.html) erklärt."),
           "pool_intro": "Kandidatenpool: `{ecl}` ({n} Konzepte, {n_loinc} mit LOINC-Code). Use-Case-ValueSets: {links}.",
           "test_intro": "ValueSet [{vs}](ValueSet-{vs}.html), Profil [{pr}](StructureDefinition-{pr}.html). Die Regel wählt {n_inc} der {n_pool} Poolkonzepte aus.",
           "auto_note": "Punkte, die ein Reviewer für diesen Test entscheiden sollte:",
           "pool_note": "Eine Zeile je Poolkonzept mit den Attributen, die die Klassifikation nutzt; die Gruppe ist das Use-Case-ValueSet, in dem das Konzept landet.",
           "and": " und ", "comma": ", ",
           "unmodelled": "{} davon haben in diesem Release gar kein Attribut {} (der LOINC-System-Part ist noch nicht modelliert), die Regel kann sie also nicht sehen: {}."},
}
BUCKET_LABEL = {"en": {"complete": "Complete", "quantitative": "Quantitative", "quantitative_convertible": "Convertible",
                       "qualitative": "Qualitative", "semiquantitative": "Semi-quantitative", "panel_order": "Panel / order",
                       "UNCLASSIFIED": "unclassified"},
                "de": {"complete": "Vollständig", "quantitative": "Quantitativ", "quantitative_convertible": "Konvertierbar",
                       "qualitative": "Qualitativ", "semiquantitative": "Semiquantitativ", "panel_order": "Panel / Auftrag",
                       "UNCLASSIFIED": "unklassifiziert"}}
ATTR_LABEL_DE = {"Direct site": "Direct site", "Property": "Property", "Scale type": "Scale type",
                 "Technique": "Technique", "Component": "Component", "Time aspect": "Time aspect"}
REASON_DE = {"Quantitative scale + concentration property": "Quantitative Skala + Konzentrations-Property",
             "Quantitative scale": "Quantitative Skala",
             "Ordinal/Nominal scale → qualitative": "Ordinale/nominale Skala → qualitativ",
             "Presence property → qualitative": "Nachweis-Property → qualitativ",
             "Semi-quantitative scale (test strip)": "Semiquantitative Skala (Teststreifen)",
             "Measurement property, no scale asserted (generic)": "Mess-Property, keine Skala asserted (generisch)",
             "Measurement property, no scale asserted (generic) + concentration property":
                 "Mess-Property, keine Skala asserted (generisch) + Konzentrations-Property",
             "no Property attribute → order/panel code": "keine Property → Auftrags-/Panelcode"}


def attr_text(concept, attr, t):
    vals = concept["attrs"].get(attr)
    return t["comma"].join(v["term"] for v in vals) if vals else t["no_attr"]


def name_of(c):
    return c["pt"] or re.sub(r"\s*\(observable entity\)$", "", c["fsn"])


def code_cell(c):
    return c["loinc"] if c["loinc"] else "SCT {}".format(c["sctid"])


def analyte_page_id(analyte):
    return "loinc-ontology-analyte-" + analyte.replace("_", "-")


def render_analyte_page(lang, analyte, data, tests, test_rows_by_id, agg_index, buckets, ctx, survey=None):
    t = L10N[lang]
    pool = data["concepts"]
    for cid, c in pool.items():
        c["sctid"] = cid
    L = []
    L.append(t["intro"].format(analyte=analyte.replace("_", " "), release=ctx["RELEASE"]))
    L.append("")
    links = []
    for b in buckets:
        e = agg_index.get((analyte, b["id"]))
        if e:
            links.append("[{}]({})".format(BUCKET_LABEL[lang][b["id"]], "ValueSet-{}.html".format(e["vs_id"])))
    L.append(t["pool_intro"].format(ecl=data["pool_ecl"], n=len(pool),
                                    n_loinc=sum(1 for c in pool.values() if c["loinc"]), links=t["comma"].join(links)))
    L.append("")
    for test in [x for x in tests if x["analyte"] == analyte]:
        td = data["tests"][test["id"]]
        row = test_rows_by_id[test["id"]]
        inc = [pool[c] for c in td["included"] if c in pool]
        inc.sort(key=lambda c: name_of(c))
        L.append("### {}".format(test["name"]))
        L.append("")
        L.append(t["test_intro"].format(vs=row["vs_id"], pr=row["pr_id"], n_inc=len(inc), n_pool=len(pool)))
        L.append("")
        # rule
        focus, rows = parse_ecl(test["ecl"])
        L.append("| {} | {} |".format(t["attribute"], t["value"]))
        L.append("|---|---|")
        for a, v in rows:
            L.append("| {} | {} |".format(a, md_cell(v)))
        L.append("")
        # included
        L.append("#### {} ({})".format(t["included"], len(inc)))
        L.append("")
        if inc:
            L.append("| LOINC | {} | {} |".format(t["name"], " | ".join(SHOW_ATTRS)))
            L.append("|---|---|" + "---|" * len(SHOW_ATTRS))
            for c in inc:
                L.append("| {} | {} | {} |".format(code_cell(c), name_of(c), " | ".join(attr_text(c, a, t) for a in SHOW_ATTRS)))
            L.append("")
            # auto facts: specimens and techniques among included
            spec = {}
            tech = {}
            for c in inc:
                for v in c["attrs"].get("Direct site", []):
                    spec[v["term"]] = spec.get(v["term"], 0) + 1
                for v in c["attrs"].get("Technique", []):
                    tech[v["term"]] = tech.get(v["term"], 0) + 1
            L.append("* **{}**: {}".format(t["specimens"], t["comma"].join("{} ({})".format(k, n) for k, n in sorted(spec.items(), key=lambda x: -x[1])) or t["none"]))
            L.append("* **{}**: {}".format(t["techniques"], t["comma"].join("{} ({})".format(k, n) for k, n in sorted(tech.items(), key=lambda x: -x[1])) or t["none"]))
            L.append("")
        # ontology gaps: hand-added LOINC codes
        extra = test.get("extra_loinc", [])
        if extra:
            L.append("#### {} ({})".format(t["gap"], len(extra)))
            L.append("")
            L.append(t["gap_note"].format(release=ctx["RELEASE"]))
            L.append("")
            L.append("| LOINC | {} | {} |".format(t["name"], t["reason"]))
            L.append("|---|---|---|")
            for e in extra:
                L.append("| {} | {} | {} |".format(e["code"], e["display"], e["reason_" + lang]))
            L.append("")
        # excluded, grouped by failing clause set
        groups = {}
        for cid, c in pool.items():
            if cid in td["included"]:
                continue
            fails = []
            for cl in td["clauses"]:
                satisfied = cid in cl["satisfied"]
                if satisfied == cl["negated"]:
                    fails.append(cl)
            key = tuple((cl["attr"], cl["negated"]) for cl in fails)
            groups.setdefault(key, []).append(c)
        n_exc = sum(len(v) for v in groups.values())
        L.append("#### {} ({})".format(t["excluded"], n_exc))
        L.append("")
        for key, members in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            members.sort(key=lambda c: name_of(c))
            attrs = [a for a, neg in key]
            if any(neg for a, neg in key):
                head = t["because_neg"].format(attrs[0], len(members))
            elif len(attrs) == 1:
                head = t["because"].format(attrs[0], len(members))
            elif attrs:
                head = t["because_multi"].format(t["comma"].join(attrs[:-1]) + t["and"] + attrs[-1], len(members))
            else:
                head = "{} ({})".format(t["excluded"], len(members))
            L.append("**{}**".format(head))
            L.append("")
            cols = [a for a in SHOW_ATTRS if a in attrs] or SHOW_ATTRS[:3]
            L.append("| LOINC | {} | {} |".format(t["name"], " | ".join(cols)))
            L.append("|---|---|" + "---|" * len(cols))
            for c in members:
                L.append("| {} | {} | {} |".format(code_cell(c), name_of(c), " | ".join(attr_text(c, a, t) for a in cols)))
            L.append("")
            for a in attrs:
                missing = [c for c in members if not c["attrs"].get(a)]
                if missing and not any(neg for _, neg in key):
                    L.append(t["unmodelled"].format(len(missing), a, t["comma"].join(code_cell(c) for c in missing)))
                    L.append("")
        # discussion
        disc = TEMPLATES / "tests" / "{}.{}.md".format(test["id"], lang)
        L.append("#### {}".format(t["discussion"]))
        L.append("")
        if disc.exists():
            L.append(disc.read_text(encoding="utf-8").strip())
        else:
            L.append(t["auto_note"])
            L.append("")
            L.append("* " + ("Whether every specimen subtype and technique listed above belongs to the routine test."
                             if lang == "en" else
                             "Ob jeder oben genannte Materialsubtyp und jede Technik zum Routinetest gehört."))
            L.append("* " + ("Whether any excluded group is a result the sites actually report under this test."
                             if lang == "en" else
                             "Ob eine ausgeschlossene Gruppe ein Ergebnis ist, das die Standorte tatsächlich unter diesem Test berichten."))
        L.append("")
    # full pool
    L.append("### {}".format(t["pool"]))
    L.append("")
    L.append(t["pool_note"])
    L.append("")
    L.append("| LOINC | {} | Property | Scale type | Direct site | {} | {} |".format(t["name"], t["bucket"], t["reason"]))
    L.append("|---|---|---|---|---|---|---|")
    order = {"quantitative_convertible": 0, "quantitative": 1, "qualitative": 2, "semiquantitative": 3, "panel_order": 4, "UNCLASSIFIED": 5}
    for c in sorted(pool.values(), key=lambda c: (order.get(c["use_case"], 9), name_of(c))):
        reason = c["reason"] if lang == "en" else REASON_DE.get(c["reason"], c["reason"])
        L.append("| {} | {} | {} | {} | {} | {} | {} |".format(
            code_cell(c), name_of(c), attr_text(c, "Property", t), attr_text(c, "Scale type", t),
            attr_text(c, "Direct site", t), BUCKET_LABEL[lang].get(c["use_case"], c["use_case"]), reason))
    # LOINC-side recall: terms of the analyte the pool does not reach
    if survey:
        L.append("")
        L.append("### {}".format(t["survey"]))
        L.append("")
        key = "survey_none" if not survey["outside"] else "survey_note"
        L.append(t[key].format(lv=ctx["LOINC_VERSION"], n_total=survey["n_total"], n_pool=survey["n_pool"],
                               n_out=len(survey["outside"]), pattern=survey["pattern"]))
        if survey["outside"]:
            L.append("")
            L.append(t["survey_cols"])
            L.append("|---|---|---|---|")
            for r in survey["outside"]:
                L.append("| {} | {} | {} | {} |".format(r["code"], r["name"], r["property"], r["system"]))
    return "\n".join(L) + "\n"


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, help="root of the kerndatensatzmodul-labor checkout")
    ap.add_argument("--date", default=dt.date.today().isoformat())
    ap.add_argument("--repo-url", default="https://github.com/medizininformatik-initiative/loincsnomed-lab-concepts")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--loinc-csv", help="LoincTable/Loinc.csv of LOINC %s; when given, the pages name the enumerated "
                    "codes that this LOINC release introduced (unknown under the module's 2.82 pin)" % LOINC_VERSION)
    args = ap.parse_args()

    out = Path(args.out).expanduser().resolve()
    if not (out / "sushi-config.yaml").exists():
        sys.exit("not a module checkout (no sushi-config.yaml): {}".format(out))

    version_uri = _targets.snomed_version_uri()
    module_pin = module_loinc_pin(out)
    release = release_label(version_uri)
    tests_cfg = json.loads(CLINICAL_TESTS.read_text())
    tests = tests_cfg["tests"]
    buckets = json.loads(AGG_PROFILES.read_text())["buckets"]
    bucket_by_id = {b["id"]: b for b in buckets}

    vs_test_dir = out / "input" / "fsh" / "valuesets" / "loinc-ontology"
    pr_dir = out / "input" / "fsh" / "profiles" / "loinc-ontology"
    inst_dir = out / "input" / "fsh" / "instances" / "loinc-ontology"

    files = {}  # path -> text
    all_loinc_codes = set()
    test_codes_by_analyte = {}  # analyte -> LOINC codes enumerated by its per-test ValueSets

    files[vs_test_dir / "aliases-loinc-ontology.fsh"] = (
        "// LOINC Ontology (SNOMED CT extension module 11010000107), release {rel}.\n"
        "// Only the proposal ValueSets under valuesets/loinc-ontology/ use these aliases; they are\n"
        "// deliberately NOT in aliases.fsh, whose $sct/$loinc pins are tied to the expansion\n"
        "// manifest by scripts/terminology-pins.test.mjs.\n"
        "Alias: {alias} = http://snomed.info/sct|{uri}\n"
        "// LOINC {lv}: the LOINC release the LOINC Ontology {rel} is built on. Kept separate from the\n"
        "// module's own $loinc pin ({mp}, forced by the expansion manifest) so that the two can drift\n"
        "// without touching the module; codes a newer LOINC release introduced are unknown under an older pin.\n"
        "Alias: {lalias} = http://loinc.org|{lv}\n".format(rel=release, alias=SCT_ALIAS, uri=version_uri,
                                                            lalias=LOINC_ALIAS, lv=LOINC_VERSION, mp=module_pin or "none"))

    # Layer 1: tests
    test_rows = []
    for t in tests:
        vs = json.loads((TEST_VS_DIR / "{}.json".format(t["id"])).read_text())
        loinc, sct, ecl, _ = split_includes(vs)
        extra = vs.get("_extra_loinc", [])
        all_loinc_codes.update(c["code"] for c in loinc)
        all_loinc_codes.update(e["code"] for e in extra)
        test_codes_by_analyte.setdefault(t["analyte"], set()).update(c["code"] for c in loinc)
        vs_name = fsh_name("MII_VS_Labor", t["id"])
        vs_id = fsh_id("mii-vs-labor", t["id"])
        desc = ("Proposal: LOINC codes of the clinical test '{}' ({} tier, specimen {}), computed by ECL over the "
                "LOINC Ontology {}. Parts: LOINC enumeration ({}, LOINC {}), LOINC Ontology observables without LOINC code ({}), "
                "and the ECL as an intensional include.{} ECL: `{}`"
                .format(t["name"], t["tier"], t["specimen"], release, len(loinc), LOINC_VERSION, len(sct),
                        " Plus {} hand-added LOINC code(s) the LOINC Ontology release does not model (ontology gap, see the "
                        "analyte review page): {}.".format(len(extra), ", ".join(e["code"] for e in extra)) if extra else "",
                        t["ecl"]))
        purpose = ("Guidance for binding Observation.code of the MII laboratory test profile to a computably defined "
                   "LOINC set; accompanies ballot comments on 2027.0.0-ballot. Generated, not hand-curated.")
        files[vs_test_dir / "tests" / (vs_name + ".fsh")] = render_valueset(
            vs_name, vs_id, fsh_title("MII VS Labor", t["id"]), desc, purpose, loinc, sct, ecl, args.date,
            "Clinical test '{}'".format(t["name"]), extra=extra)
        pr_name, pr_id, pr_text = render_profile(t, vs_name, args.date, release)
        files[pr_dir / (pr_name + ".fsh")] = pr_text
        test_rows.append({"test_id": t["id"], "analyte": t["analyte"], "name": t["name"], "tier": t["tier"], "specimen": t["specimen"],
                          "n_loinc": len(loinc) + len(extra), "n_sct": len(sct), "vs_id": vs_id, "pr_id": pr_id,
                          "attrs": parse_ecl(t["ecl"])[1]})

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
        all_loinc_codes.update(c["code"] for c in loinc)
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
                "Ontology {}. {} concepts ({} with LOINC, enumerated at LOINC {}). {}"
                .format(b["name"], analyte.replace("_", " "), b["description"], "`" + pool_ecl + "`", release, n, len(loinc), LOINC_VERSION,
                        "The pool ECL is carried as an intensional include." if ecl else
                        "Classification of the pool by Scale type and Property; the rule is stated above."))
        purpose = ("Guidance for use-case-driven aggregation of laboratory results in secondary use; accompanies "
                   "ballot comments on 2027.0.0-ballot. Generated, not hand-curated.")
        files[vs_test_dir / "aggregation" / (vs_name + ".fsh")] = render_valueset(
            vs_name, vs_id, fsh_title("MII VS Labor", slug), desc, purpose, loinc, sct, ecl, args.date,
            "Analyte {}, bucket {}".format(analyte, bucket_id))
    analytes.sort(key=lambda a: a["analyte"])

    ctx = {"RELEASE": release, "VERSION_URI": version_uri, "REPO_URL": args.repo_url, "LOINC_VERSION": LOINC_VERSION,
           "MODULE_LOINC_PIN": module_pin or "none", "NEW_LOINC_SENTENCE_EN": "", "NEW_LOINC_SENTENCE_DE": "",
           "REPO_NAME": args.repo_url.rstrip("/").split("/")[-1], "N_TESTS": len(test_rows),
           "N_USECASE": len(agg_index), "N_ANALYTES": len(analytes)}
    # LOINC-side recall survey per analyte (needs Loinc.csv and the pool tables)
    survey = {}
    if args.loinc_csv and POOL_ATTRS.exists():
        terms = load_loinc_lab_terms(Path(args.loinc_csv))
        pool_data_for_survey = json.loads(POOL_ATTRS.read_text(encoding="utf-8"))
        for cf in sorted((ROOT / "config").glob("*_custom_ecl.json")):
            analyte = cf.name[: -len("_custom_ecl.json")]
            spec = json.loads(cf.read_text(encoding="utf-8")).get("loinc_survey")
            if not spec or analyte not in pool_data_for_survey:
                continue
            pool_codes = {c["loinc"] for c in pool_data_for_survey[analyte]["concepts"].values() if c["loinc"]}
            survey[analyte] = loinc_survey(terms, spec, pool_codes, test_codes_by_analyte.get(analyte, set()))
    if args.loinc_csv:
        new_codes = loinc_codes_first_released(Path(args.loinc_csv), all_loinc_codes, LOINC_VERSION)
        if new_codes:
            listing = ", ".join("`{}` {}".format(c, n) for c, n in new_codes)
            ctx["NEW_LOINC_SENTENCE_EN"] = (" {} of the enumerated codes were introduced in LOINC {} and are unknown "
                                           "codes under any older LOINC pin: {}.".format(len(new_codes), LOINC_VERSION, listing))
            ctx["NEW_LOINC_SENTENCE_DE"] = (" {} der aufgezählten Codes wurden mit LOINC {} eingeführt und sind unter jedem "
                                           "älteren LOINC-Pin unbekannte Codes: {}.".format(len(new_codes), LOINC_VERSION, listing))
    for lang, base in (("en", out / "input" / "pagecontent"),
                       ("de", out / "input" / "translations" / "de" / "pagecontent")):
        for page, text in render_pages(lang, ctx, tests, test_rows, analytes, buckets, agg_index, survey).items():
            files[base / (page + ".md")] = text
    for src in sorted((TEMPLATES / "fsh").glob("*.fsh")):
        files[inst_dir / src.name] = src.read_text(encoding="utf-8")
    analyte_pages = []
    if POOL_ATTRS.exists():
        pool_data = json.loads(POOL_ATTRS.read_text(encoding="utf-8"))
        test_rows_by_id = {r["test_id"]: r for r in test_rows}
        for analyte in sorted(pool_data):
            analyte_pages.append(analyte_page_id(analyte))
            for lang, base in (("en", out / "input" / "pagecontent"),
                               ("de", out / "input" / "translations" / "de" / "pagecontent")):
                files[base / (analyte_page_id(analyte) + ".md")] = render_analyte_page(
                    lang, analyte, pool_data[analyte], tests, test_rows_by_id, agg_index, buckets, ctx,
                    survey.get(analyte))
    else:
        print("  (no pool_attributes.json: analyte subpages skipped; run scripts/pool_attributes.py)")

    print("LOINC Ontology {} -> {}".format(release, out))
    print("  {} test ValueSets, {} profiles, {} aggregation ValueSets, {} pages x 2 languages, {} example(s)".format(
        len(test_rows), len(test_rows), len(agg_index), len(PAGES), len(list((TEMPLATES / "fsh").glob("*.fsh")))))
    if args.dry_run:
        for p in sorted(files):
            print("  would write", p.relative_to(out))
        return
    for d in (vs_test_dir, pr_dir, inst_dir):
        if d.exists():
            shutil.rmtree(d)
    for p, text in files.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    print("  analyte pages: {}".format(len(analyte_pages)))
    print("  written")


if __name__ == "__main__":
    main()
