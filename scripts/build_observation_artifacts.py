#!/usr/bin/env python3
"""
build_observation_artifacts.py — For every clinical test in
config/clinical_tests.json, emit:
  - a FHIR ValueSet (LOINC-coded, SNOMED fallback) with the ECL-selected concepts
  - a FHIR Observation profile as FSH (derived from MII KDS Laborbefund),
    binding the ValueSet to Observation.code and fixing specimen/unit/dataType
  - a per-test concept CSV for clinical review (LOINC, SCTID, FSN, tier)

Output:
  output/fhir/valuesets/<id>.json
  output/fhir/profiles/<id>.fsh
  output/fhir/review/<id>.csv
  output/fhir/SUMMARY.md

Usage:
  python3 scripts/build_observation_artifacts.py [--target local|public]
"""

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from terminology_server_adapters import LOINCSNOMEDSnowstormAdapter
from review_export import TARGETS, load_loinc_map, LOINC_MAP_PATH

TESTS_PATH = ROOT / "config" / "clinical_tests.json"


def run_ecl(adapter, ecl, limit=10000):
    result = adapter.execute_ecl_query(ecl, limit=limit)
    total = result.get("total", 0)
    if total > limit:
        print("    !! TRUNCATED {} > {}".format(total, limit))
    out = []
    for item in result.get("items", []):
        out.append({
            "sctid": item.get("conceptId"),
            "fsn": (item.get("fsn") or {}).get("term", ""),
        })
    return out


def make_valueset(cfg, test, concepts, loinc_map):
    """LOINC-coded ValueSet; SNOMED include for concepts lacking a LOINC code."""
    vs_url = "{}/{}".format(cfg["base_valueset_url"], test["id"])
    loinc_concepts, snomed_concepts = [], []
    for c in concepts:
        code = loinc_map.get(c["sctid"])
        if code:
            loinc_concepts.append({"code": code, "display": c["fsn"]})
        else:
            snomed_concepts.append({"code": c["sctid"], "display": c["fsn"]})
    include = []
    if loinc_concepts:
        include.append({"system": cfg["loinc_system"], "concept": loinc_concepts})
    if snomed_concepts:
        include.append({"system": cfg["snomed_system"],
                        "version": cfg["snomed_version"], "concept": snomed_concepts})
    return {
        "resourceType": "ValueSet",
        "id": test["id"],
        "url": vs_url,
        "name": "".join(w.capitalize() for w in test["id"].split("-")),
        "title": test["name"],
        "status": "draft",
        "experimental": True,
        "description": "{} ({}). Generated from ECL against {}. Review required."
            .format(test["name"], test["tier"], cfg["snomed_version"]),
        "compose": {"include": include or [{"system": cfg["loinc_system"]}]},
        "_ecl": test["ecl"],
    }


def make_profile_fsh(cfg, test):
    """Observation profile as FSH, derived from MII KDS Laborbefund."""
    pid = "".join(w.capitalize() for w in test["id"].split("-"))
    vs_url = "{}/{}".format(cfg["base_valueset_url"], test["id"])
    lines = [
        "Profile: {}".format(pid),
        "Parent: $KDSLab",
        "Id: {}".format(test["id"]),
        'Title: "{}"'.format(test["name"]),
        'Description: "Observation profile for {} ({} test). code bound to the '
        'curated {} ValueSet; specimen {}."'.format(
            test["name"], test["tier"], test["id"], test["specimen"]),
        "* code from {} (required)".format(vs_url),
    ]
    dt = test.get("dataType", "unset")
    if dt == "Quantity":
        lines.append("* value[x] only Quantity")
        if test.get("unit"):
            lines.append('* valueQuantity.unit = "{}"  // expected unit'.format(test["unit"]))
    elif dt == "CodeableConcept":
        lines.append("* value[x] only CodeableConcept")
        lines.append("// qualitative result — bind valueCodeableConcept to a "
                     "presence/absence ValueSet")
    else:
        lines.append("// panel/order — no single value[x]; use hasMember to the "
                     "component result Observations")
    lines.append('* specimen only Reference(Specimen)  // {}'.format(test["specimen"]))
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", choices=list(TARGETS), default="local")
    ap.add_argument("--loinc-map", default=str(LOINC_MAP_PATH))
    args = ap.parse_args()

    cfg = json.loads(TESTS_PATH.read_text())
    tgt = TARGETS[args.target]
    print("Target: {} ({})".format(tgt["name"], tgt["branch"]))
    loinc_map = load_loinc_map(args.loinc_map)
    print("LOINC map: {} entries\n".format(len(loinc_map)))
    adapter = LOINCSNOMEDSnowstormAdapter(api_base=tgt["api_base"], branch=tgt["branch"])

    out = ROOT / "output" / "fhir"
    (out / "valuesets").mkdir(parents=True, exist_ok=True)
    (out / "profiles").mkdir(parents=True, exist_ok=True)
    (out / "review").mkdir(parents=True, exist_ok=True)

    summary = []
    for test in cfg["tests"]:
        concepts = run_ecl(adapter, test["ecl"])
        n_loinc = sum(1 for c in concepts if loinc_map.get(c["sctid"]))

        vs = make_valueset(cfg, test, concepts, loinc_map)
        (out / "valuesets" / "{}.json".format(test["id"])).write_text(
            json.dumps(vs, indent=2, ensure_ascii=False))

        (out / "profiles" / "{}.fsh".format(test["id"])).write_text(
            make_profile_fsh(cfg, test))

        with open(out / "review" / "{}.csv".format(test["id"]), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["LOINC", "SCTID", "FSN", "tier", "test"])
            for c in concepts:
                w.writerow([loinc_map.get(c["sctid"], ""), c["sctid"], c["fsn"],
                            test["tier"], test["id"]])

        summary.append((test["id"], test["analyte"], test["tier"],
                        len(concepts), n_loinc))
        print("  {:<32} {:<11} {:>4} concepts ({} LOINC)".format(
            test["id"], test["tier"], len(concepts), n_loinc))

    md = ["# Clinical test artifacts\n",
          "Target: `{}` ({})\n".format(tgt["name"], tgt["branch"]),
          "{} tests → {} ValueSets + {} Observation profiles.\n".format(
              len(summary), len(summary), len(summary)),
          "| Test | Analyte | Tier | Concepts | with LOINC |",
          "|---|---|---|--:|--:|"]
    for tid, analyte, tier, n, nl in summary:
        md.append("| `{}` | {} | {} | {} | {} |".format(tid, analyte, tier, n, nl))
    (out / "SUMMARY.md").write_text("\n".join(md) + "\n")

    print("\n{} tests → {} ValueSets + {} profiles".format(
        len(summary), len(summary), len(summary)))
    print("Written to: {}".format(out))


if __name__ == "__main__":
    main()
