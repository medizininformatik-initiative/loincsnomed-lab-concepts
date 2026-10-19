#!/usr/bin/env python3
"""
build_aggregation_valuesets.py — comprehensive per-analyte ValueSets.

For every analyte in config/*_custom_ecl.json, take the candidate pool
(component-only ECL = the 'complete' bucket), classify it with the use-case
rules from config/aggregation_profiles.json (same code as review_export.py)
and emit one FHIR ValueSet per analyte × bucket:

  output/fhir/aggregation/valuesets/<analyte>-<bucket>.json
  output/fhir/aggregation/review/<analyte>-<bucket>.csv
  output/fhir/aggregation/SUMMARY.md

Each ValueSet is LOINC-coded (SNOMED fallback for concepts without a LOINC
alternate identifier). The 'complete' bucket additionally carries the pool
ECL as an intensional SNOMED include; the other buckets are classifications
(Scale type + Property rules), so they carry the rule in the description and
the pool ECL in `_ecl`.

Usage:
  python3 scripts/build_aggregation_valuesets.py [--target local|public] [--config <json> ...]
"""

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from terminology_server_adapters import LOINCSNOMEDSnowstormAdapter
from review_export import (TARGETS, LOINC_MAP_PATH, load_loinc_map, load_profiles,
                           load_config, build_analyte, OBSERVABLE_ROOT)
from build_observation_artifacts import ecl_include
import targets as _targets

TESTS_PATH = ROOT / "config" / "clinical_tests.json"
OUT = ROOT / "output" / "fhir" / "aggregation"


def pool_ecl(res):
    comp = res["component"]
    return "{} : {}".format(OBSERVABLE_ROOT, comp) if res["how"] != "focus subtree (no Component attribute)" else comp


def make_valueset(cfg, analyte, bucket, rows, res):
    vs_id = "{}-{}".format(analyte.replace("_", "-"), bucket["id"].replace("_", "-"))
    loinc_c, snomed_c = [], []
    for r in rows:
        if r["loinc"]:
            loinc_c.append({"code": r["loinc"], "display": r["fsn"]})
        else:
            snomed_c.append({"code": r["sctid"], "display": r["fsn"]})
    include = []
    if loinc_c:
        include.append({"system": cfg["loinc_system"], "concept": loinc_c})
    if snomed_c:
        include.append({"system": cfg["snomed_system"], "version": cfg["snomed_version"], "concept": snomed_c})
    ecl = pool_ecl(res)
    if bucket["id"] == "complete":
        include.append(ecl_include(cfg, ecl))
    return {
        "resourceType": "ValueSet",
        "id": vs_id,
        "url": "{}/{}".format(cfg["base_valueset_url"], vs_id),
        "name": "".join(w.capitalize() for w in vs_id.split("-")),
        "title": "{} — {}".format(analyte.replace("_", " "), bucket["name"]),
        "status": "draft",
        "experimental": True,
        "description": "{}: {} Pool = {} against {}. {} concepts ({} with LOINC). Review required."
            .format(bucket["name"], bucket["description"], ecl, cfg["snomed_version"],
                    len(rows), len(loinc_c)),
        "compose": {"include": include or [{"system": cfg["loinc_system"]}]},
        "_ecl": ecl,
        "_bucket": bucket["id"],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", action="append")
    ap.add_argument("--target", choices=list(TARGETS), default="local")
    ap.add_argument("--loinc-map", default=str(LOINC_MAP_PATH))
    args = ap.parse_args()

    config_files = [Path(c) for c in args.config] if args.config else sorted(ROOT.glob("config/*_custom_ecl.json"))
    cfg = json.loads(TESTS_PATH.read_text())
    cfg["snomed_version"] = _targets.snomed_version_uri()
    prof = load_profiles()
    tgt = TARGETS[args.target]
    print("Target: {} ({})".format(tgt["name"], tgt["branch"]))
    loinc_map = load_loinc_map(args.loinc_map)
    adapter = LOINCSNOMEDSnowstormAdapter(api_base=tgt["api_base"], branch=tgt["branch"])

    (OUT / "valuesets").mkdir(parents=True, exist_ok=True)
    (OUT / "review").mkdir(parents=True, exist_ok=True)
    bucket_ids = [b["id"] for b in prof["buckets"]]
    md = ["# Comprehensive per-analyte ValueSets (use-case aggregation)", "",
          "Target: `{}` ({})".format(tgt["name"], tgt["branch"]), "",
          "One ValueSet per analyte × bucket. Cells = concepts (with LOINC).", "",
          "| Analyte | Pool ECL | " + " | ".join(bucket_ids) + " | unclassified |",
          "|---|---|" + "---|" * len(bucket_ids) + "---|"]
    total = 0
    for path in config_files:
        concept, data = load_config(path)
        print("\n{}".format(concept))
        res = build_analyte(adapter, concept, data, prof, loinc_map)
        cells = []
        for i, b in enumerate(prof["buckets"]):
            rows = [r for r in res["rows"] if r["marks"][i] == "Y"]
            n_loinc = sum(1 for r in rows if r["loinc"])
            cells.append("{} ({})".format(len(rows), n_loinc))
            if not rows:
                continue
            vs = make_valueset(cfg, concept, b, rows, res)
            (OUT / "valuesets" / "{}.json".format(vs["id"])).write_text(json.dumps(vs, indent=2, ensure_ascii=False) + "\n")
            with open(OUT / "review" / "{}.csv".format(vs["id"]), "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["LOINC", "SCTID", "FSN", "use_case", "reason"])
                for r in sorted(rows, key=lambda r: (r["loinc"] or "~", r["fsn"])):
                    w.writerow([r["loinc"], r["sctid"], r["fsn"], r["usecase"], r["reason"]])
            total += 1
        md.append("| {} | `{}` | {} | {} |".format(concept, pool_ecl(res), " | ".join(cells), res["unclassified"]))
    md += ["", "`complete` carries the pool ECL as an intensional SNOMED include; the other buckets are "
           "Scale-type/Property classifications (see config/aggregation_profiles.json) and list the rule in their description.", ""]
    (OUT / "SUMMARY.md").write_text("\n".join(md))
    print("\n{} ValueSets written to {}".format(total, OUT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
