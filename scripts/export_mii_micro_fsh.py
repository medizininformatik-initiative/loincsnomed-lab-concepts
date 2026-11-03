#!/usr/bin/env python3
"""Render the microbiology request ValueSets (config/micro) as MII-convention FSH.

Target: a checkout of medizininformatik-initiative/kerndatensatzmodul-mikrobiologie
(the KDS Mikrobiologie module, IG-publisher layout, 2027 shape). The output is a
proposal accompanying ballot comments, so everything is written under clearly
separated "loinc-ontology" directories and nothing of the module's own content is
touched.

Writes into <out> (the module root):

  input/fsh/valuesets/loinc-ontology/aliases-loinc-ontology.fsh
  input/fsh/valuesets/loinc-ontology/MII_VS_Mikrobio_LOINC_Ontology_<Query>.fsh      one per query
  input/fsh/valuesets/loinc-ontology/MII_VS_Mikrobio_LOINC_Ontology_<Profile>.fsh    union sets for profiles bound to several queries
  input/fsh/profiles/loinc-ontology/MII_PR_Mikrobio_LOINC_Ontology_<Profile>.fsh     one per module profile with a request
  input/pagecontent/loinc-ontology-{valuesets,method,requests,release-delta}.md       (English, from templates/mii-micro/pages)
  input/pagecontent/loinc-ontology-request-<family>.md                                (English, generated)
  input/translations/de/pagecontent/loinc-ontology-*.md                               (German)

Not written (one-time hand edits in the module): sushi-config.yaml pages:,
input/includes/menu.xml (+ de), the IG-level .po page titles, the link line in
value-sets.md (en + de).

Inputs: config/micro/*_custom_ecl.json (the rules), config/micro/l10n_de.json
(German names and descriptions), config/targets.json (which release),
output/micro/version_comparison.json (release delta; run compare_versions.py with
--config-glob "config/micro/*_custom_ecl.json" first), the module checkout itself
(its enumerated LOINC ValueSets, for the coverage tables).

Usage:
  python3 scripts/export_mii_micro_fsh.py --out ~/code/fhir-profiling/kerndatensatzmodul-mikrobiologie
"""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import targets as _targets  # noqa: E402
from terminology_server_adapters import LOINCSNOMEDSnowstormAdapter  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config" / "micro"
L10N_DE_PATH = CONFIG_DIR / "l10n_de.json"
COMPARISON = ROOT / "output" / "micro" / "version_comparison.json"
TEMPLATES = ROOT / "templates" / "mii-micro" / "pages"

MAX_ROWS = 400          # rows listed per query on a request page
MAX_DELTA_ROWS = 600    # rows listed per direction and query on the delta page
SCT_ALIAS = "$sct-loinc-ontology"
LOINC_ALIAS = "$loinc-ontology-loinc"
LOINC_VERSION = "2.83"  # the LOINC release the LOINC Ontology 2026-10-21 is built on
LOINC_SCHEME = "30051010000102"
HEADERS = {"Content-Type": "application/json",
           "Accept-Language": "en-X-900000000000509007,en-X-900000000000508004,en"}
GENERATOR_URL = "https://github.com/medizininformatik-initiative/loincsnomed-lab-concepts"

# (config stem, page slug, English title, German title)
FAMILIES = [
    ("micro_allgemeine_kultur", "allgemeine-kultur", "General culture", "Allgemeine Kultur"),
    ("micro_allgemeine_bestimmung", "allgemeine-bestimmung", "General determination", "Allgemeine Bestimmung"),
    ("micro_spezifische_bestimmung", "spezifische-bestimmung", "Specific determination", "Spezifische Bestimmung"),
    ("micro_mikroskopie", "mikroskopie", "Microscopy", "Mikroskopie"),
    ("micro_keimzahl", "keimzahl", "Colony count", "Keimzahl"),
    ("micro_empfindlichkeit", "empfindlichkeit", "Susceptibility", "Empfindlichkeit"),
    ("micro_ct_wert", "ct-wert", "Ct value", "Ct-Wert"),
    ("micro_molekulare_pathogenlast", "molekulare-pathogenlast", "Molecular pathogen load", "Molekulare Pathogenlast"),
    ("micro_antigen_antikoerper_quantitativ", "antigen-antikoerper-quantitativ",
     "Quantitative antigen and antibody tests", "Antigen/Antikörper quantitativ"),
    ("micro_titer", "titer", "Titre", "Titer"),
    ("micro_resistenzmechanismen", "resistenzmechanismen", "Resistant organisms and resistance mechanisms",
     "Resistente Erreger und Resistenzmechanismen"),
]

# Module profiles that get a derived proposal profile; the bound ValueSet is the
# query ValueSet (one query) or a union ValueSet (several queries).
PROFILES = [
    {"slug": "allgemeine-kultur", "parent": "MII_PR_Mikrobio_Allgemeine_Kultur",
     "parent_id": "mii-pr-mikrobio-allgemeine-kultur", "family": "micro_allgemeine_kultur",
     "name_en": "General culture", "name_de": "Allgemeine Kultur", "queries": ["general_culture_identity"]},
    {"slug": "allgemeine-bestimmung", "parent": "MII_PR_Mikrobio_Allgemeine_Bestimmung",
     "parent_id": "mii-pr-mikrobio-allgemeine-bestimmung", "family": "micro_allgemeine_bestimmung",
     "name_en": "General determination", "name_de": "Allgemeine Bestimmung", "queries": ["organism_identity_any_technique"]},
    {"slug": "spezifische-bestimmung", "parent": "MII_PR_Mikrobio_Spezifische_Bestimmung",
     "parent_id": "mii-pr-mikrobio-spezifische-bestimmung", "family": "micro_spezifische_bestimmung",
     "name_en": "Specific determination", "name_de": "Spezifische Bestimmung",
     "queries": ["naa_detection_any_technique", "organism_specific_culture_detection", "antigen_detection_threshold"]},
    {"slug": "allgemeine-mikroskopie", "parent": "MII_PR_Mikrobio_Allgemeine_Mikroskopie",
     "parent_id": "mii-pr-mikrobio-mikroskopie", "family": "micro_mikroskopie",
     "name_en": "General microscopy", "name_de": "Allgemeine Mikroskopie",
     "queries": ["general_microscopy_by_technique", "general_microscopy_finding_in_specimen"]},
    {"slug": "spezifische-mikroskopie", "parent": "MII_PR_Mikrobio_Spezifische_Mikroskopie",
     "parent_id": "mii-pr-mikrobio-spezifische-mikroskopie", "family": "micro_mikroskopie",
     "name_en": "Specific microscopy", "name_de": "Spezifische Mikroskopie", "queries": ["specific_microscopy_threshold"]},
    {"slug": "keimzahl", "parent": "MII_PR_Mikrobio_Keimzahl", "parent_id": "mii-pr-mikrobio-keimzahl",
     "family": "micro_keimzahl", "name_en": "Colony count", "name_de": "Keimzahl", "queries": ["colony_count_organism"]},
    {"slug": "empfindlichkeit", "parent": "MII_PR_Mikrobio_Empfindlichkeit",
     "parent_id": "mii-pr-mikrobio-empfindlichkeit", "family": "micro_empfindlichkeit",
     "name_en": "Susceptibility", "name_de": "Empfindlichkeit", "queries": ["susceptibility_phenotype"]},
    {"slug": "voraussichtliche-empfindlichkeit", "parent": "MII_PR_Mikrobio_Voraussichtliche_Empfindlichkeit",
     "parent_id": "mii-pr-mikrobio-voraussichtliche-empfindlichkeit", "family": "micro_empfindlichkeit",
     "name_en": "Predicted susceptibility", "name_de": "Voraussichtliche Empfindlichkeit",
     "queries": ["susceptibility_genotype_predicted"]},
    {"slug": "ct-wert", "parent": "MII_PR_Mikrobio_Ct_Wert", "parent_id": "mii-pr-mikrobio-ct-wert",
     "family": "micro_ct_wert", "name_en": "Ct value", "name_de": "Ct-Wert", "queries": ["ct_value_microbial_nucleic_acid"]},
    {"slug": "molekulare-pathogenlast", "parent": "MII_PR_Mikrobio_Molekulare_Pathogenlast",
     "parent_id": "mii-pr-mikrobio-molekulare-pathogenlast", "family": "micro_molekulare_pathogenlast",
     "name_en": "Molecular pathogen load", "name_de": "Molekulare Pathogenlast", "queries": ["pathogen_load_any_technique"]},
    {"slug": "antigen-antikoerper-quantitativ", "parent": "MII_PR_Mikrobio_Antigen_Antikoerper_Quantitativ",
     "parent_id": "mii-pr-mikrobio-antigen-antikoerper-quantitativ", "family": "micro_antigen_antikoerper_quantitativ",
     "name_en": "Quantitative antigen and antibody tests", "name_de": "Antigen/Antikörper quantitativ",
     "queries": ["ab_ag_quantitative"]},
    {"slug": "titer", "parent": "MII_PR_Mikrobio_Titer", "parent_id": "mii-pr-mikrobio-titer",
     "family": "micro_titer", "name_en": "Titre", "name_de": "Titer", "queries": ["titer_infective_antibody"]},
    {"slug": "resistenzmechanismen-determinanten", "parent": "MII_PR_Mikrobio_Resistenzmechanismen_Determinanten",
     "parent_id": "mii-pr-mikrobio-resistenzmechanismen-determinanten", "family": "micro_resistenzmechanismen",
     "name_en": "Resistance mechanisms and determinants", "name_de": "Resistenzmechanismen und Determinanten",
     "queries": ["resistant_organism_detection"]},
]

ATTR_IDS = {"246093002": "Component", "704319004": "Inheres in", "704320005": "Towards",
            "704327008": "Direct site", "370130000": "Property", "370132008": "Scale type",
            "246501002": "Technique", "370134009": "Time aspect", "704321002": "Characterizes",
            "718497002": "Inherent location", "704326004": "Precondition"}
TABLE_ATTRS = ["Component", "Inheres in", "Towards", "Direct site", "Property", "Scale type", "Technique"]
ACRONYMS = {"naa": "NAA", "ct": "Ct", "ab": "Ab", "ag": "Ag"}

L10N = {
    "en": {
        "intro": ("This page is the review material for the request family **{family}** of the "
                  "[LOINC Ontology proposal](loinc-ontology-valuesets.html): every rule of the family as the "
                  "LOINC Ontology {release} resolves it, decomposed into its attributes, with the codes it "
                  "selects and what the release {prev} → {release} changed. The method is explained under "
                  "[How the ValueSets are built](loinc-ontology-method.html); all families are listed under "
                  "[ValueSets per request](loinc-ontology-requests.html)."),
        "attribute": "Attribute", "value": "Value", "rule": "Rule", "name": "Name",
        "vs_line": "ValueSet [{vs}](ValueSet-{vs}.html).",
        "profile_line": " Bound by the derived profile [{pr}](StructureDefinition-{pr}.html).",
        "profile_union_line": " Part of the union ValueSet [{uvs}](ValueSet-{uvs}.html), bound by the derived profile [{pr}](StructureDefinition-{pr}.html).",
        "result": "The rule selects **{n}** concepts ({n_loinc} with a LOINC code, {n_sct} without).",
        "delta": " Release {prev} → {release}: **+{added} / −{removed}** (lists on the [release delta](loinc-ontology-release-delta.html) page).",
        "delta_none": " Unchanged between {prev} and {release}.",
        "codes": "Codes", "more": "… {n} more; the complete enumeration is in the ValueSet.",
        "none_of": "none, `[0..0]`: {v}", "no_attr": "–", "any": "any (`*`)",
        "none_sel": "The rule selects no concept in this release.",
        "sct_only": "SCT {sctid}",
    },
    "de": {
        "intro": ("Diese Seite ist das Review-Material für die Anforderungsfamilie **{family}** des "
                  "[LOINC-Ontology-Vorschlags](loinc-ontology-valuesets.html): jede Regel der Familie, wie die "
                  "LOINC Ontology {release} sie auflöst, zerlegt in ihre Attribute, mit den Codes, die sie "
                  "auswählt, und dem, was das Release {prev} → {release} geändert hat. Die Methode ist unter "
                  "[Wie die ValueSets gebaut werden](loinc-ontology-method.html) erklärt; alle Familien stehen "
                  "unter [ValueSets je Anforderung](loinc-ontology-requests.html)."),
        "attribute": "Attribut", "value": "Wert", "rule": "Regel", "name": "Name",
        "vs_line": "ValueSet [{vs}](ValueSet-{vs}.html).",
        "profile_line": " Gebunden durch das abgeleitete Profil [{pr}](StructureDefinition-{pr}.html).",
        "profile_union_line": " Teil des Vereinigungs-ValueSets [{uvs}](ValueSet-{uvs}.html), gebunden durch das abgeleitete Profil [{pr}](StructureDefinition-{pr}.html).",
        "result": "Die Regel wählt **{n}** Konzepte aus ({n_loinc} mit LOINC-Code, {n_sct} ohne).",
        "delta": " Release {prev} → {release}: **+{added} / −{removed}** (Listen auf der Seite [Release-Delta](loinc-ontology-release-delta.html)).",
        "delta_none": " Unverändert zwischen {prev} und {release}.",
        "codes": "Codes", "more": "… {n} weitere; die vollständige Aufzählung steht im ValueSet.",
        "none_of": "keines, `[0..0]`: {v}", "no_attr": "–", "any": "beliebig (`*`)",
        "none_sel": "Die Regel wählt in diesem Release kein Konzept aus.",
        "sct_only": "SCT {sctid}",
    },
}
ATTR_DE = {"Component": "Component", "Inheres in": "Inheres in", "Towards": "Towards", "Direct site": "Direct site",
           "Property": "Property", "Scale type": "Scale type", "Technique": "Technique", "Time aspect": "Time aspect"}


# ── small helpers ────────────────────────────────────────────────────────────

def fsh_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'


def words(slug):
    return [w for w in re.split(r"[-_]+", slug) if w]


def cap(w):
    return ACRONYMS.get(w.lower(), w.capitalize())


def vs_name(qid):
    return "MII_VS_Mikrobio_LOINC_Ontology_" + "_".join(cap(w) for w in words(qid))


# FHIR ids are limited to 64 characters; the prefix takes 31. Long query ids get a
# shorter id (the FSH name and the file name keep the full query id).
ID_SHORT = {"general_microscopy_finding_in_specimen": "general-microscopy-in-specimen",
            "organism_specific_culture_detection": "specific-culture-detection",
            "resistenzmechanismen-determinanten": "resistenzmechanismen"}


def _check_id(i):
    if len(i) > 64:
        sys.exit("FHIR id longer than 64 characters: {} (add it to ID_SHORT)".format(i))
    return i


def vs_id(qid):
    return _check_id("mii-vs-mikrobio-loinc-ontology-" + "-".join(w.lower() for w in words(ID_SHORT.get(qid, qid))))


def vs_title(qid):
    return "MII VS Microbiology LOINC Ontology " + " ".join(cap(w) for w in words(qid))


def pr_name(slug):
    return "MII_PR_Mikrobio_LOINC_Ontology_" + "_".join(cap(w) for w in words(slug))


def pr_id(slug):
    return _check_id("mii-pr-mikrobio-loinc-ontology-" + "-".join(w.lower() for w in words(ID_SHORT.get(slug, slug))))


def md(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def release_label(version_uri):
    m = re.search(r"/version/(\d{4})(\d{2})(\d{2})$", version_uri)
    return "{}-{}-{}".format(*m.groups()) if m else version_uri


def effective_label(eff):
    return "{}-{}-{}".format(eff[:4], eff[4:6], eff[6:8])


def name_of(c):
    return c["pt"] or re.sub(r"\s*\(observable entity\)$", "", c["fsn"])


# ── inputs ───────────────────────────────────────────────────────────────────

def load_families():
    out = []
    for stem, slug, title_en, title_de in FAMILIES:
        data = json.loads((CONFIG_DIR / (stem + "_custom_ecl.json")).read_text(encoding="utf-8"))
        out.append({"stem": stem, "slug": slug, "title_en": title_en, "title_de": title_de,
                    "description": data.get("description", ""),
                    "queries": [{"id": q["id"], "name": q.get("name", q["id"]),
                                 "description": q.get("description", ""), "ecl": q["ecl"]}
                                for q in data["queries"]]})
    return out


def load_l10n_de():
    return json.loads(L10N_DE_PATH.read_text(encoding="utf-8")) if L10N_DE_PATH.exists() else {"families": {}, "queries": {}}


def run_ecl(adapter, ecl, limit=10000):
    res = adapter.execute_ecl_query(ecl, limit=limit)
    total = res.get("total", 0)
    ids = [it["conceptId"] for it in res.get("items", [])]
    if total > len(ids):
        sys.exit("ECL result truncated ({} > {}): {}".format(total, len(ids), ecl))
    return ids


def bulk_load(api_base, branch, ids):
    """conceptId -> {fsn, pt, loinc, active, attrs: {label: [{id, term}]}}"""
    out = {}
    ids = sorted(set(ids))
    for i in range(0, len(ids), 200):
        r = requests.post("{}/browser/{}/concepts/bulk-load".format(api_base, branch),
                          data=json.dumps({"conceptIds": ids[i:i + 200]}), headers=HEADERS, timeout=600)
        r.raise_for_status()
        for c in r.json():
            loinc = ""
            for a in c.get("alternateIdentifiers", []) or []:
                if a.get("identifierSchemeId") == LOINC_SCHEME and a.get("active", True):
                    loinc = a["alternateIdentifier"]
            attrs = {}
            for rel in c.get("relationships", []):
                if not rel.get("active") or rel.get("characteristicType") != "INFERRED_RELATIONSHIP":
                    continue
                tid = rel["type"]["conceptId"]
                if tid == "116680003":
                    continue
                label = ATTR_IDS.get(tid, rel["type"]["pt"]["term"])
                attrs.setdefault(label, []).append({"id": rel["target"]["conceptId"],
                                                    "term": rel["target"]["pt"]["term"]})
            out[c["conceptId"]] = {"sctid": c["conceptId"], "fsn": c["fsn"]["term"], "pt": (c.get("pt") or {}).get("term", ""),
                                   "loinc": loinc, "active": c.get("active", True), "attrs": attrs}
    return out


def load_comparison():
    """ecl -> {added: [...], removed: [...], a_total, b_total} from compare_versions.py --json-out."""
    if not COMPARISON.exists():
        print("!! {} missing: no release delta on the pages".format(COMPARISON))
        return {}, None, None
    data = json.loads(COMPARISON.read_text(encoding="utf-8"))
    a, b = data["targets"]
    out = {}
    for r in data["rows"]:
        d = r["diff"] or {"only_in_a": [], "only_in_b": []}
        out[r["ecl"]] = {"added": sorted(d["only_in_b"]), "removed": sorted(d["only_in_a"]),
                         "a_total": r["per_target"][a["name"]]["total"], "b_total": r["per_target"][b["name"]]["total"]}
    return out, a, b


def module_enumerations(out):
    """[(vs_name, title, [(loinc, display)])] from the module's own LOINC ValueSets."""
    res = []
    for p in sorted((out / "input" / "fsh" / "valuesets").glob("MII_VS_Mikrobio_*LOINC*.fsh")):
        name, title, codes = p.stem, "", []
        for line in p.read_text(encoding="utf-8").splitlines():
            m = re.match(r'^Title:\s*"(.*)"', line)
            if m:
                title = m.group(1)
            m = re.match(r'^\*\s+\$loinc(?:-no-ver)?#(\S+)(?:\s+"([^"]*)")?', line)
            if m:
                codes.append((m.group(1), m.group(2) or ""))
        if codes:
            res.append((name, title or name, codes))
    return res


def load_loinc_to_sct(path):
    m = {}
    with open(path, encoding="utf-8") as f:
        next(f)
        for line in f:
            p = line.rstrip("\r\n").split("\t")
            if len(p) >= 6 and p[2] == "1":
                m[p[0]] = p[5]
    return m


# ── ECL decomposition ────────────────────────────────────────────────────────

def _split_top(s, sep):
    parts, depth, cur, i, inlabel = [], 0, [], 0, False
    while i < len(s):
        ch = s[i]
        if ch == "|":
            inlabel = not inlabel
        if not inlabel:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            elif depth == 0 and s.startswith(sep, i):
                parts.append("".join(cur))
                cur = []
                i += len(sep)
                continue
        cur.append(ch)
        i += 1
    parts.append("".join(cur))
    return [p.strip() for p in parts if p.strip()]


def _term(v, t):
    v = v.strip()
    if v == "*":
        return t["any"]
    if v.startswith("(") and v.endswith(")"):
        return " OR ".join(_term(x, t) for x in _split_top(v[1:-1], " OR "))
    m = re.match(r"^(<<?|>>?)?\s*(\d+)\s*\|([^|]*)\|$", v)
    if not m:
        return "`{}`".format(v)
    op, _cid, label = m.groups()
    label = label.strip()
    while re.search(r"\s*\([^()]*\)\s*$", label):   # "(property) (qualifier value)": every trailing semtag
        label = re.sub(r"\s*\([^()]*\)\s*$", "", label)
    return "`{} {}`".format(op.strip(), label) if op else label


CLAUSE = re.compile(r"^(?:\[(\d+)\.\.(\d+)\]\s*)?(<<?\s*)?(\d+)\s*\|([^|]*)\|\s*=\s*(.+)$", re.S)


def _clause_row(clause, t):
    clause = clause.strip()
    if clause.startswith("(") and clause.endswith(")") and " OR " in clause:
        alts = [_clause_row(a, t) for a in _split_top(clause[1:-1], " OR ")]
        if len({a[1] for a in alts}) == 1:
            return (" OR ".join(a[0] for a in alts), alts[0][1])
        return (" OR ".join(a[0] for a in alts), " / ".join("{} = {}".format(a[0], a[1]) for a in alts))
    m = CLAUSE.match(clause)
    if not m:
        return ("`{}`".format(clause), "")
    lo, hi, _op, _aid, alabel, value = m.groups()
    attr = re.sub(r"\s*\(attribute\)\s*$", "", alabel.strip())
    val = _term(value, t)
    if lo is not None and lo == "0" and hi == "0":
        val = t["none_of"].format(v=val)
    elif lo is not None:
        val = "`[{}..{}]` {}".format(lo, hi, val)
    return (attr, val)


def decompose(ecl, t):
    _focus, _, refinement = ecl.partition(":")
    return [_clause_row(c, t) for c in _split_top(refinement, ",")]


def attr_table(ecl, t):
    L = ["| {} | {} |".format(t["attribute"], t["value"]), "|---|---|"]
    for attr, val in decompose(ecl, t):
        L.append("| {} | {} |".format(attr, val))
    return "\n".join(L)


# ── FSH renderers ────────────────────────────────────────────────────────────

ALIASES = """// LOINC Ontology (SNOMED CT extension module 11010000107), release {release}.
// Only the proposal ValueSets under valuesets/loinc-ontology/ use these aliases; they are
// deliberately NOT in aliases.fsh, whose $sct/$loinc pins are tied to the expansion
// manifest by scripts/terminology-pins.test.mjs.
Alias: {sct} = http://snomed.info/sct|{version_uri}
// LOINC {loinc_version}: the LOINC release the LOINC Ontology {release} is built on. The module pins
// LOINC 2.82 for its own ValueSets; several hundred of the enumerated codes below were
// introduced in 2.83 and would be unknown codes under the 2.82 pin.
Alias: {loinc} = http://loinc.org|{loinc_version}
"""

VS_HEAD = """* insert PR_CS_VS_Version
* insert Publisher
* insert SnomedLicense
* ^status = #draft
* ^experimental = true
* ^date = "{date}"
"""


def render_valueset(q, family, concepts, ids, date, release, delta):
    name, vid, title = vs_name(q["id"]), vs_id(q["id"]), vs_title(q["id"])
    loinc = sorted((concepts[i] for i in ids if concepts[i]["loinc"]), key=lambda c: c["loinc"])
    sct = sorted((concepts[i] for i in ids if not concepts[i]["loinc"]), key=lambda c: c["fsn"])
    desc = ("Proposal: LOINC codes of the microbiology request '{fam}: {qn}', computed by ECL over the LOINC "
            "Ontology {rel}. {qd} Parts: LOINC enumeration ({nl}, LOINC {lv}), LOINC Ontology observables without "
            "LOINC code ({ns}), and the ECL as an intensional include. ECL: `{ecl}`"
            .format(fam=family["title_en"], qn=q["name"], rel=release, qd=q["description"], nl=len(loinc),
                    lv=LOINC_VERSION, ns=len(sct), ecl=q["ecl"]))
    purpose = ("Guidance for binding Observation.code of the MII microbiology request profiles to a computably "
               "defined LOINC set; accompanies ballot comments on 2027.0.0-ballot2. Generated, not hand-curated.")
    out = ["ValueSet: {}".format(name), "Id: {}".format(vid), "Title: {}".format(fsh_str(title)),
           "Description: {}".format(fsh_str(desc)), VS_HEAD.format(date=date).rstrip("\n"),
           "* ^purpose = {}".format(fsh_str(purpose))]
    if delta:
        out.append("// Release delta {}: +{} / -{} concepts (see the release-delta page)".format(
            delta["label"], len(delta["added"]), len(delta["removed"])))
    if loinc:
        out.append("// Request '{}': LOINC enumeration ({} codes) resolved from the ECL below".format(q["id"], len(loinc)))
        for c in loinc:
            out.append("* {}#{}".format(LOINC_ALIAS, c["loinc"]))
    if sct:
        out.append("// Observables of the LOINC Ontology module without a LOINC code ({})".format(len(sct)))
        for c in sct:
            out.append("* {}#{} {}".format(SCT_ALIAS, c["sctid"], fsh_str(c["fsn"])))
    out.append("// The rule itself: intensional include, expandable only on a terminology server that")
    out.append("// holds the LOINC Ontology release named by the alias")
    out.append("* include codes from system {} where constraint = {}".format(SCT_ALIAS, fsh_str(q["ecl"])))
    return name, vid, "\n".join(out) + "\n"


def render_union_valueset(prof, qnames, date, release):
    name, vid = vs_name(prof["slug"]), vs_id(prof["slug"])
    title = "MII VS Microbiology LOINC Ontology " + prof["name_en"]
    desc = ("Proposal: union of the request ValueSets that together cover the module profile {} ({}), each "
            "computed by ECL over the LOINC Ontology {}: {}."
            .format(prof["parent"], prof["name_en"], release, ", ".join(qnames)))
    out = ["ValueSet: {}".format(name), "Id: {}".format(vid), "Title: {}".format(fsh_str(title)),
           "Description: {}".format(fsh_str(desc)), VS_HEAD.format(date=date).rstrip("\n"),
           "* ^purpose = {}".format(fsh_str(
               "Binding ValueSet for the derived profile {}; accompanies ballot comments on 2027.0.0-ballot2. "
               "Generated, not hand-curated.".format(pr_name(prof["slug"]))))]
    for n in qnames:
        out.append("* include codes from valueset {}".format(n))
    return name, vid, "\n".join(out) + "\n"


def render_profile(prof, bound_vs, member_queries, date, release):
    name, pid = pr_name(prof["slug"]), pr_id(prof["slug"])
    title = "MII PR Microbiology LOINC Ontology " + prof["name_en"]
    desc = ("Proposal: Observation profile for the request '{}', derived from {}. Observation.code is bound "
            "(required) to the ValueSet {}, which is defined by ECL over the LOINC Ontology {}. Everything else "
            "is inherited from the module profile.".format(prof["name_en"], prof["parent"], bound_vs, release))
    rules = "; ".join("{}: `{}`".format(q["name"], q["ecl"]) for q in member_queries)
    out = ["Profile: {}".format(name), "Parent: {}".format(prof["parent"]), "Id: {}".format(pid),
           "Title: {}".format(fsh_str(title)), "Description: {}".format(fsh_str(desc)),
           "// License, CRMI profiles and CRMI extensions are INHERITED from the parent profile; re-inserting",
           "// their ^extension[+] rulesets would duplicate the inherited entries. The version is not inherited.",
           "* insert PR_CS_VS_Version", "* insert Publisher", "* insert SnomedLicense",
           "* ^status = #draft", "* ^experimental = true", '* ^date = "{}"'.format(date),
           "* code from {} (required)".format(bound_vs),
           "* code ^binding.description = {}".format(fsh_str(
               "LOINC codes of the request, computed by ECL over the LOINC Ontology {}. {}".format(release, rules)))]
    return name, pid, "\n".join(out) + "\n"


# ── page renderers ───────────────────────────────────────────────────────────

def concept_row_cols(rows):
    """Attribute columns that are non-empty for at least one row."""
    cols = []
    for a in TABLE_ATTRS:
        if any(c["attrs"].get(a) for c in rows):
            cols.append(a)
    return cols


def concept_table(rows, cols, t, limit):
    L = ["| LOINC | {} | {} |".format(t["name"], " | ".join(cols)), "|---|---|" + "---|" * len(cols)]
    rows = sorted(rows, key=lambda c: (c["loinc"] == "", c["loinc"], name_of(c)))
    for c in rows[:limit]:
        code = c["loinc"] or t["sct_only"].format(sctid=c["sctid"])
        cells = [", ".join(v["term"] for v in c["attrs"].get(a, [])) or t["no_attr"] for a in cols]
        L.append("| {} | {} | {} |".format(code, md(name_of(c)), " | ".join(md(x) for x in cells)))
    if len(rows) > limit:
        L.append("")
        L.append(t["more"].format(n=len(rows) - limit))
    return "\n".join(L)


def render_family_page(lang, fam, results, concepts, deltas, profile_of_query, union_of_query, ctx, l10n_de):
    t = L10N[lang]
    fam_title = fam["title_de"] if lang == "de" else fam["title_en"]
    fam_desc = (l10n_de["families"].get(fam["stem"], {}).get("description") or fam["description"]) if lang == "de" else fam["description"]
    L = [t["intro"].format(family=fam_title, release=ctx["release"], prev=ctx["prev_release"]), "", fam_desc, ""]
    for q in fam["queries"]:
        qn = (l10n_de["queries"].get(q["id"], {}).get("name") or q["name"]) if lang == "de" else q["name"]
        qd = (l10n_de["queries"].get(q["id"], {}).get("description") or q["description"]) if lang == "de" else q["description"]
        ids = results[q["id"]]
        rows = [concepts[i] for i in ids]
        n_loinc = sum(1 for c in rows if c["loinc"])
        L.append("### {}".format(qn))
        L.append("")
        L.append(qd)
        L.append("")
        line = t["vs_line"].format(vs=vs_id(q["id"]))
        if q["id"] in profile_of_query:
            prof = profile_of_query[q["id"]]
            if q["id"] in union_of_query:
                line += t["profile_union_line"].format(uvs=vs_id(prof["slug"]), pr=pr_id(prof["slug"]))
            else:
                line += t["profile_line"].format(pr=pr_id(prof["slug"]))
        L.append(line)
        L.append("")
        L.append("```")
        L.append(q["ecl"])
        L.append("```")
        L.append("")
        L.append(attr_table(q["ecl"], t))
        L.append("")
        res = t["result"].format(n=len(rows), n_loinc=n_loinc, n_sct=len(rows) - n_loinc)
        d = deltas.get(q["ecl"])
        if d:
            if d["added"] or d["removed"]:
                res += t["delta"].format(prev=ctx["prev_release"], release=ctx["release"],
                                         added=len(d["added"]), removed=len(d["removed"]))
            else:
                res += t["delta_none"].format(prev=ctx["prev_release"], release=ctx["release"])
        L.append(res)
        L.append("")
        if rows:
            L.append("#### {} ({})".format(t["codes"], len(rows)))
            L.append("")
            L.append(concept_table(rows, concept_row_cols(rows), t, MAX_ROWS))
        else:
            L.append(t["none_sel"])
        L.append("")
    return "\n".join(L).rstrip("\n") + "\n"


def request_table(lang, families, results, concepts, deltas, profile_of_query, l10n_de):
    hdr = {"en": "| Family | Request | LOINC | SNOMED only | +/− vs {prev} | ValueSet | Profile |",
           "de": "| Familie | Anforderung | LOINC | nur SNOMED | +/− ggü. {prev} | ValueSet | Profil |"}[lang]
    L = [hdr, "|---|---|--:|--:|--:|---|---|"]
    for fam in families:
        fam_title = fam["title_de"] if lang == "de" else fam["title_en"]
        for q in fam["queries"]:
            qn = (l10n_de["queries"].get(q["id"], {}).get("name") or q["name"]) if lang == "de" else q["name"]
            rows = [concepts[i] for i in results[q["id"]]]
            n_loinc = sum(1 for c in rows if c["loinc"])
            d = deltas.get(q["ecl"])
            dcell = "+{} / −{}".format(len(d["added"]), len(d["removed"])) if d else "–"
            pcell = "–"
            if q["id"] in profile_of_query:
                p = profile_of_query[q["id"]]
                pcell = "[{}](StructureDefinition-{}.html)".format(p["name_de"] if lang == "de" else p["name_en"], pr_id(p["slug"]))
            L.append("| [{}](loinc-ontology-request-{}.html) | {} | {} | {} | {} | [{}](ValueSet-{}.html) | {} |".format(
                fam_title, fam["slug"], md(qn), n_loinc, len(rows) - n_loinc, dcell, vs_id(q["id"]), vs_id(q["id"]), pcell))
    return "\n".join(L)


def profile_table(lang, profiles, families_by_stem, l10n_de):
    hdr = {"en": "| Module profile | Derived proposal profile | Bound ValueSet | Rules |",
           "de": "| Modulprofil | Abgeleitetes Vorschlagsprofil | Gebundenes ValueSet | Regeln |"}[lang]
    L = [hdr, "|---|---|---|---|"]
    for p in profiles:
        qnames = []
        for qid in p["queries"]:
            q = next(q for q in families_by_stem[p["family"]]["queries"] if q["id"] == qid)
            qnames.append((l10n_de["queries"].get(qid, {}).get("name") or q["name"]) if lang == "de" else q["name"])
        bound = vs_id(p["slug"]) if len(p["queries"]) > 1 else vs_id(p["queries"][0])
        L.append("| [{}](StructureDefinition-{}.html) | [{}](StructureDefinition-{}.html) | [{}](ValueSet-{}.html) | {} |".format(
            p["parent"], p["parent_id"], pr_name(p["slug"]), pr_id(p["slug"]), bound, bound, md("; ".join(qnames))))
    return "\n".join(L)


def coverage_tables(lang, enums, loinc_to_sct, membership, concepts_all):
    t_sum = {"en": "| Module ValueSet | Enumerated codes | In the LOINC Ontology | In a proposal ValueSet |",
             "de": "| Modul-ValueSet | Aufgezählte Codes | In der LOINC Ontology | In einem Vorschlags-ValueSet |"}[lang]
    t_det = {"en": "| Module ValueSet | LOINC | Display | SCTID | Proposal ValueSets |",
             "de": "| Modul-ValueSet | LOINC | Display | SCTID | Vorschlags-ValueSets |"}[lang]
    S = [t_sum, "|---|--:|--:|--:|"]
    D = [t_det, "|---|---|---|---|---|"]
    uniq = {c for _n, _t, codes in enums for c, _ in codes}      # a code listed in two ValueSets counts once
    n_all, n_in = len(uniq), sum(1 for c in uniq if c in loinc_to_sct)
    for name, title, codes in enums:
        in_ont = sum(1 for c, _ in codes if c in loinc_to_sct)
        in_prop = sum(1 for c, _ in codes if membership.get(loinc_to_sct.get(c, ""), set()))
        S.append("| [{}](ValueSet-{}.html) | {} | {} | {} |".format(
            md(title), name.lower().replace("_", "-"), len(codes), in_ont, in_prop))
        for c, disp in codes:
            sct = loinc_to_sct.get(c, "")
            mem = sorted(membership.get(sct, set())) if sct else []
            D.append("| {} | {} | {} | {} | {} |".format(
                md(title), c, md(disp), sct or "–",
                ", ".join("[{}](ValueSet-{}.html)".format(q, vs_id(q)) for q in mem) or "–"))
    return "\n".join(S), "\n".join(D), n_all, n_in


def delta_tables(lang, families, deltas, concepts, prev_concepts, l10n_de, prev_label, cur_label):
    hdr = {"en": "| Family | Request | {a} | {b} | added | removed |",
           "de": "| Familie | Anforderung | {a} | {b} | neu | entfallen |"}[lang].format(a=prev_label, b=cur_label)
    S = [hdr, "|---|---|--:|--:|--:|--:|"]
    heads = {"en": ("Added in {}", "Removed in {}"), "de": ("Neu in {}", "Entfallen in {}")}[lang]
    L = []
    for fam in families:
        fam_title = fam["title_de"] if lang == "de" else fam["title_en"]
        for q in fam["queries"]:
            d = deltas.get(q["ecl"])
            if not d:
                continue
            qn = (l10n_de["queries"].get(q["id"], {}).get("name") or q["name"]) if lang == "de" else q["name"]
            S.append("| [{}](loinc-ontology-request-{}.html) | {} | {} | {} | {} | {} |".format(
                fam_title, fam["slug"], md(qn), d["a_total"], d["b_total"], len(d["added"]), len(d["removed"])))
            if not d["added"] and not d["removed"]:
                continue
            L.append("### {}".format(qn))
            L.append("")
            L.append("[{}](loinc-ontology-request-{}.html) · [ValueSet](ValueSet-{}.html)".format(fam_title, fam["slug"], vs_id(q["id"])))
            L.append("")
            for head, ids, src in ((heads[0].format(cur_label), d["added"], concepts), (heads[1].format(prev_label), d["removed"], prev_concepts)):
                if not ids:
                    continue
                L.append("**{}** ({})".format(head, len(ids)))
                L.append("")
                L.append("| LOINC | SCTID | FSN |")
                L.append("|---|---|---|")
                rows = sorted(ids, key=lambda i: ((src.get(i) or {}).get("loinc", "") == "", (src.get(i) or {}).get("loinc", ""), (src.get(i) or {}).get("fsn", "")))
                for i in rows[:MAX_DELTA_ROWS]:
                    c = src.get(i) or {"loinc": "", "fsn": "?"}
                    L.append("| {} | {} | {} |".format(c["loinc"] or "–", i, md(c["fsn"])))
                if len(rows) > MAX_DELTA_ROWS:
                    L.append("| … | … | {} more |".format(len(rows) - MAX_DELTA_ROWS))
                L.append("")
    return "\n".join(S), "\n".join(L)


def fill_template(page, lang, ctx):
    text = (TEMPLATES / "{}.{}.md".format(page, lang)).read_text(encoding="utf-8")
    for k, v in ctx.items():
        text = text.replace("{{" + k + "}}", str(v))
    left = re.findall(r"\{\{[A-Z_]+\}\}", text)
    if left:
        sys.exit("unfilled placeholders in {}.{}.md: {}".format(page, lang, sorted(set(left))))
    return text


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, help="module checkout (kerndatensatzmodul-mikrobiologie root)")
    ap.add_argument("--date", default=dt.date.today().isoformat())
    args = ap.parse_args()
    out = Path(args.out).expanduser().resolve()
    if not (out / "sushi-config.yaml").exists():
        sys.exit("{} is not an IG checkout (no sushi-config.yaml)".format(out))

    cfg = _targets.load()
    cur, prev = _targets.current(cfg), _targets.previous(cfg)
    version_uri = _targets.snomed_version_uri(cfg)
    release = release_label(version_uri)
    prev_release = effective_label(prev["effective"])
    adapter = LOINCSNOMEDSnowstormAdapter(api_base=cur["api_base"], branch=cur["branch"])

    families = load_families()
    families_by_stem = {f["stem"]: f for f in families}
    l10n_de = load_l10n_de()
    deltas, _a, _b = load_comparison()

    # 1. run every rule on the current release
    results = {}
    for fam in families:
        for q in fam["queries"]:
            results[q["id"]] = run_ecl(adapter, q["ecl"])
            print("  {:45s} {:5d}".format(q["id"], len(results[q["id"]])))
    all_ids = set()
    for ids in results.values():
        all_ids |= set(ids)
    print("resolving {} concepts on {} ...".format(len(all_ids), cur["branch"]))
    concepts = bulk_load(cur["api_base"], cur["branch"], all_ids)
    removed_ids = set()
    for d in deltas.values():
        removed_ids |= set(d["removed"])
    prev_concepts = bulk_load(prev["api_base"], prev["branch"], removed_ids) if removed_ids else {}
    for d in deltas.values():
        d["label"] = "{} -> {}".format(prev_release, release)

    membership = {}
    for qid, ids in results.items():
        for i in ids:
            membership.setdefault(i, set()).add(qid)

    profile_of_query, union_of_query = {}, {}
    for p in PROFILES:
        for qid in p["queries"]:
            profile_of_query[qid] = p
            if len(p["queries"]) > 1:
                union_of_query[qid] = p

    # 2. FSH
    vs_dir = out / "input" / "fsh" / "valuesets" / "loinc-ontology"
    pr_dir = out / "input" / "fsh" / "profiles" / "loinc-ontology"
    vs_dir.mkdir(parents=True, exist_ok=True)
    pr_dir.mkdir(parents=True, exist_ok=True)
    (vs_dir / "aliases-loinc-ontology.fsh").write_text(ALIASES.format(
        release=release, sct=SCT_ALIAS, version_uri=version_uri, loinc=LOINC_ALIAS, loinc_version=LOINC_VERSION), encoding="utf-8")
    n_vs = n_pr = 0
    for fam in families:
        for q in fam["queries"]:
            name, _vid, text = render_valueset(q, fam, concepts, results[q["id"]], args.date, release, deltas.get(q["ecl"]))
            (vs_dir / (name + ".fsh")).write_text(text, encoding="utf-8")
            n_vs += 1
    for p in PROFILES:
        member = [next(q for q in families_by_stem[p["family"]]["queries"] if q["id"] == qid) for qid in p["queries"]]
        if len(p["queries"]) > 1:
            uname, _uid, utext = render_union_valueset(p, [vs_name(qid) for qid in p["queries"]], args.date, release)
            (vs_dir / (uname + ".fsh")).write_text(utext, encoding="utf-8")
            n_vs += 1
            bound = uname
        else:
            bound = vs_name(p["queries"][0])
        name, _pid, text = render_profile(p, bound, member, args.date, release)
        (pr_dir / (name + ".fsh")).write_text(text, encoding="utf-8")
        n_pr += 1
    print("wrote {} ValueSets and {} profiles under {}".format(n_vs, n_pr, out / "input" / "fsh"))

    # 3. pages
    enums = module_enumerations(out)
    loinc_to_sct = load_loinc_to_sct(_targets.loinc_map_path(cfg))
    n_queries = sum(len(f["queries"]) for f in families)
    for lang, pdir in (("en", out / "input" / "pagecontent"),
                       ("de", out / "input" / "translations" / "de" / "pagecontent")):
        pdir.mkdir(parents=True, exist_ok=True)
        fam_list = []
        for fam in families:
            title = fam["title_de"] if lang == "de" else fam["title_en"]
            n = sum(len(results[q["id"]]) for q in fam["queries"])
            fam_list.append("* [{}](loinc-ontology-request-{}.html) — {} {}".format(
                title, fam["slug"], len(fam["queries"]), {"en": "rules", "de": "Regeln"}[lang] if len(fam["queries"]) != 1 else {"en": "rule", "de": "Regel"}[lang]))
        cov_sum, cov_det, n_enum, n_enum_in = coverage_tables(lang, enums, loinc_to_sct, membership, concepts)
        d_sum, d_lists = delta_tables(lang, families, deltas, concepts, prev_concepts, l10n_de, prev_release, release)
        ctx = {"RELEASE": release, "PREV_RELEASE": prev_release, "VERSION_URI": version_uri,
               "LOINC_VERSION": LOINC_VERSION, "N_VS": n_vs, "N_PROFILES": n_pr, "N_QUERIES": n_queries,
               "N_FAMILIES": len(families), "FAMILY_LIST": "\n".join(fam_list), "GENERATOR_URL": GENERATOR_URL,
               "REQUEST_TABLE": request_table(lang, families, results, concepts, deltas, profile_of_query, l10n_de),
               "PROFILE_TABLE": profile_table(lang, PROFILES, families_by_stem, l10n_de),
               "COVERAGE_SUMMARY": cov_sum, "COVERAGE_DETAIL": cov_det, "N_ENUM": n_enum, "N_ENUM_IN_ONTOLOGY": n_enum_in,
               "DELTA_TABLE": d_sum, "DELTA_LISTS": d_lists}
        for page in ("loinc-ontology-valuesets", "loinc-ontology-method", "loinc-ontology-requests", "loinc-ontology-release-delta"):
            (pdir / (page + ".md")).write_text(fill_template(page, lang, ctx), encoding="utf-8")
        for fam in families:
            (pdir / "loinc-ontology-request-{}.md".format(fam["slug"])).write_text(
                render_family_page(lang, fam, results, concepts, deltas, profile_of_query, union_of_query,
                                   {"release": release, "prev_release": prev_release}, l10n_de), encoding="utf-8")
        print("wrote {} pages ({})".format(4 + len(families), lang))

    # 4. what the module owner still has to do by hand
    print("\nHand edits in the module (see the docstring): sushi-config.yaml pages:, menu.xml (en+de), "
          "IG .po page titles, value-sets.md (en+de).")
    print("Module enumerated codes: {} of {} in the LOINC Ontology {}".format(n_enum_in, n_enum, release))


if __name__ == "__main__":
    main()
