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


# ── ECL decomposition + page rendering ───────────────────────────────────────

TEMPLATES = ROOT / "templates" / "mii"
PAGES = ["loinc-ontology-valuesets", "loinc-ontology-method", "loinc-ontology-clinical-tests",
         "loinc-ontology-use-cases"]
ATTR_NAMES = {"246093002": "Component", "704327008": "Direct site", "370130000": "Property",
              "370132008": "Scale type", "246501002": "Technique", "370134009": "Time aspect",
              "704319004": "Inheres in", "704321002": "Characterizes", "704320005": "Towards",
              "718497002": "Inherent location", "704326004": "Precondition"}
ATTR_ORDER = ["Component", "Inheres in", "Direct site", "Property", "Scale type", "Technique", "Time aspect"]


def _term(label):
    """'<< 38082009 |Hemoglobin (substance)|' -> '<< Hemoglobin'; handles '<', '<<', OR-groups."""
    label = label.strip()
    if label.startswith("(") and label.endswith(")"):
        inner = label[1:-1]
        if " OR " in inner:
            return " or ".join(_term(x) for x in inner.split(" OR "))
        label = inner.strip()
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
    """Split on `sep` outside |labels| and outside parentheses."""
    parts, buf, inside, depth = [], "", False, 0
    for ch in text:
        if ch == "|":
            inside = not inside
        elif not inside:
            depth += {"(": 1, ")": -1}.get(ch, 0)
        if ch == sep and not inside and depth == 0:
            parts.append(buf); buf = ""
        else:
            buf += ch
    parts.append(buf)
    return parts


def parse_ecl(ecl):
    """-> (focus, [(attribute name, value text)]) for the ECL shapes used in this project:
    'focus : attr = value, ...', focus-only, and 'A MINUS (A, attr = *)' (attribute absent)."""
    ecl = ecl.strip()
    minus = None
    if " MINUS " in ecl:
        ecl, minus = ecl.split(" MINUS ", 1)
        ecl = ecl.strip().strip("()").strip()
    if ":" not in ecl:
        focus, rows = _term(ecl), []
    else:
        focus_s, refinement = ecl.split(":", 1)
        focus, rows = _term(focus_s), []
        for part in _split_top(refinement):
            if "=" not in part:
                continue
            attr, value = part.split("=", 1)
            aid = re.search(r"\d{6,}", attr)
            aname = ATTR_NAMES.get(aid.group(0), _term(attr)) if aid else attr.strip()
            rows.append((aname, _term(value)))
    if minus:  # the subtrahend names the attribute that must be absent
        m = re.search(r"(\d{6,}) \|[^|]*\| = \*", minus)
        if m:
            rows.append((ATTR_NAMES.get(m.group(1), m.group(1)), "(none)"))
    if "Component" not in dict(rows):
        rows.insert(0, ("Component", focus + " [observable]"))
    return focus, rows


def attr_columns(rows_by_test):
    cols = [a for a in ATTR_ORDER if any(a in dict(r) for r in rows_by_test)]
    extra = sorted({a for r in rows_by_test for a, _ in r} - set(cols))
    return cols + extra


def md_cell(s):
    return s.replace("|", "\\|")


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
        d = dict(r["attrs"])
        cells = [r["name"], r["tier"]] + [md_cell(d.get(c, "")) for c in cols] + [
            str(r["n_loinc"]), str(r["n_sct"]),
            "[{}](ValueSet-{}.html)".format(vs, r["vs_id"]),
            "[{}](StructureDefinition-{}.html)".format(pr, r["pr_id"])]
        L.append("| " + " | ".join(cells) + " |")
    return "\n".join(L)


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
        focus, rows = parse_ecl(a["ecl"])
        pool = dict(rows).get("Component") or focus
        cells = []
        for b in cols:
            e = agg_index.get((a["analyte"], b["id"]))
            cells.append("[{}](ValueSet-{}.html)".format(e["n"], e["vs_id"]) if e else "–")
        L.append("| {} | {} | {} |".format(a["analyte"].replace("_", " "), md_cell(pool), " | ".join(cells)))
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


def render_pages(lang, ctx, tests, test_rows, analytes, buckets, agg_index):
    subst = dict(ctx)
    subst["TESTS_TABLE"] = tests_table(test_rows, lang)
    subst["USECASE_TABLE"] = usecase_table(analytes, buckets, agg_index, lang)
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
    inst_dir = out / "input" / "fsh" / "instances" / "loinc-ontology"

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
                          "n_loinc": len(loinc), "n_sct": len(sct), "vs_id": vs_id, "pr_id": pr_id,
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

    ctx = {"RELEASE": release, "VERSION_URI": version_uri, "REPO_URL": args.repo_url,
           "REPO_NAME": args.repo_url.rstrip("/").split("/")[-1], "N_TESTS": len(test_rows),
           "N_USECASE": len(agg_index), "N_ANALYTES": len(analytes)}
    for lang, base in (("en", out / "input" / "pagecontent"),
                       ("de", out / "input" / "translations" / "de" / "pagecontent")):
        for page, text in render_pages(lang, ctx, tests, test_rows, analytes, buckets, agg_index).items():
            files[base / (page + ".md")] = text
    for src in sorted((TEMPLATES / "fsh").glob("*.fsh")):
        files[inst_dir / src.name] = src.read_text(encoding="utf-8")

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
    print("  written")


if __name__ == "__main__":
    main()
