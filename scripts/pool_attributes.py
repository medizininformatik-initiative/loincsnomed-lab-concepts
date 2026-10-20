#!/usr/bin/env python3
"""
pool_attributes.py — per-concept attributes and per-test inclusion/exclusion reasons.

For every analyte pool (output/fhir/aggregation/review/<analyte>-complete.csv) this
fetches each concept's defining attributes from Snowstorm (Component, Direct site,
Property, Scale type, Technique, Time aspect, ...) and, for every clinical test of
that analyte (config/clinical_tests.json), evaluates each refinement clause of the
test's ECL separately against the pool. The result says, per concept, which
clauses it satisfies, so that an excluded concept can be explained by the clause
it fails ("Direct site is Urine specimen, rule wants << Blood specimen").

Output: output/fhir/aggregation/pool_attributes.json
  { "<analyte>": { "pool_ecl": ..., "concepts": { "<sctid>": { "loinc", "fsn", "pt",
      "use_case", "reason", "attrs": { "<attribute>": [ {"id","term"} ] } } },
      "tests": { "<test-id>": { "ecl", "included": [...sctids],
                 "clauses": [ {"attr","text","negated","satisfied":[...]} ] } } } }

Usage: python3 scripts/pool_attributes.py [--target local|public]
"""
import argparse
import csv
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from terminology_server_adapters import LOINCSNOMEDSnowstormAdapter  # noqa: E402
from review_export import TARGETS, run_ecl  # noqa: E402

TESTS_PATH = ROOT / "config" / "clinical_tests.json"
AGG = ROOT / "output" / "fhir" / "aggregation"
OUT = AGG / "pool_attributes.json"

ATTR_NAMES = {"246093002": "Component", "704327008": "Direct site", "370130000": "Property",
              "370132008": "Scale type", "246501002": "Technique", "370134009": "Time aspect",
              "704319004": "Inheres in", "704321002": "Characterizes", "704320005": "Towards",
              "718497002": "Inherent location", "704326004": "Precondition",
              "719722006": "Has realization", "704322009": "Process agent",
              "704323004": "Process duration", "704324005": "Process output",
              "704325006": "Relative to", "704327008 ": "Direct site"}


def strip_tag(term):
    while True:
        t = re.sub(r"\s*\([^()]*\)\s*$", "", term)
        if t == term:
            return term
        term = t


def split_top(text, sep=","):
    parts, buf, inside, depth = [], "", False, 0
    for ch in text:
        if ch == "|":
            inside = not inside
        elif not inside:
            depth += {"(": 1, ")": -1}.get(ch, 0)
        if ch == sep and not inside and depth == 0:
            parts.append(buf)
            buf = ""
        else:
            buf += ch
    parts.append(buf)
    return [p.strip() for p in parts if p.strip()]


def parse_clauses(ecl):
    """-> (base expression, [ {attr, text, negated} ]) for the shapes used in clinical_tests.json."""
    ecl = ecl.strip()
    clauses = []
    minus = None
    if " MINUS " in ecl:
        ecl, minus = ecl.split(" MINUS ", 1)
        ecl = ecl.strip()
        if ecl.startswith("(") and ecl.endswith(")"):
            ecl = ecl[1:-1].strip()
    base = ecl
    if ":" in ecl:
        base, refinement = ecl.split(":", 1)
        for part in split_top(refinement):
            aid = re.search(r"\d{6,}", part.split("=", 1)[0])
            clauses.append({"attr": ATTR_NAMES.get(aid.group(0), aid.group(0)) if aid else "?",
                            "text": part, "negated": False})
    if minus:
        m = re.search(r"(\d{6,}) \|[^|]*\| = \*", minus)
        if m:
            aid = m.group(1)
            clauses.append({"attr": ATTR_NAMES.get(aid, aid), "text": "<< {} = *".format(aid), "negated": True})
    return base.strip(), clauses


def bulk_attributes(api_base, branch, ids, chunk=100):
    """conceptId -> {attr name: [{id, term}]} from inferred relationships."""
    url = "{}/browser/{}/concepts/bulk-load".format(api_base.rstrip("/"), branch)
    out = {}
    ids = list(ids)
    for i in range(0, len(ids), chunk):
        body = json.dumps({"conceptIds": ids[i:i + chunk]}).encode()
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json",
                                                              "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            data = json.load(r)
        for c in data:
            attrs = {}
            for rel in c.get("relationships", []):
                if not rel.get("active") or rel.get("characteristicType") != "INFERRED_RELATIONSHIP":
                    continue
                tid = rel["type"]["conceptId"]
                if tid == "116680003":  # Is a
                    continue
                name = ATTR_NAMES.get(tid, strip_tag(rel["type"]["fsn"]["term"]))
                attrs.setdefault(name, []).append({"id": rel["target"]["conceptId"],
                                                   "term": strip_tag(rel["target"]["fsn"]["term"])})
            out[c["conceptId"]] = attrs
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", choices=list(TARGETS), default="local")
    args = ap.parse_args()
    tgt = TARGETS[args.target]
    print("Target: {} ({})".format(tgt["name"], tgt["branch"]))
    adapter = LOINCSNOMEDSnowstormAdapter(api_base=tgt["api_base"], branch=tgt["branch"])
    tests = json.loads(TESTS_PATH.read_text())["tests"]

    result = {}
    for csv_path in sorted((AGG / "review").glob("*-complete.csv")):
        analyte = csv_path.name[: -len("-complete.csv")].replace("-", "_")
        vs = json.loads((AGG / "valuesets" / "{}-complete.json".format(analyte.replace("_", "-"))).read_text())
        pool_ecl = vs["_ecl"]
        concepts = {}
        with open(csv_path, newline="") as f:
            for row in csv.DictReader(f):
                concepts[row["SCTID"]] = {"loinc": row["LOINC"], "fsn": row["FSN"], "pt": "",
                                          "use_case": row["use_case"], "reason": row["reason"], "attrs": {}}
        print("\n{}: pool {} concepts".format(analyte, len(concepts)))
        attrs = bulk_attributes(tgt["api_base"], tgt["branch"], concepts.keys())
        for cid, a in attrs.items():
            if cid in concepts:
                concepts[cid]["attrs"] = a
        # preferred terms for the table (LOINC long common name in the LOINC Ontology)
        pts = run_ecl(adapter, "({})".format(pool_ecl))
        for cid, meta in pts.items():
            if cid in concepts:
                concepts[cid]["pt"] = meta["pt"]

        tests_out = {}
        for t in [x for x in tests if x["analyte"] == analyte]:
            included = sorted(run_ecl(adapter, t["ecl"]).keys())
            base, clauses = parse_clauses(t["ecl"])
            for cl in clauses:
                sat = run_ecl(adapter, "({}) : {}".format(pool_ecl, cl["text"]))
                cl["satisfied"] = sorted(set(sat.keys()) & set(concepts.keys()))
            outside = [c for c in included if c not in concepts]
            if outside:
                print("   !! {}: {} included concepts are outside the pool (component differs)".format(t["id"], len(outside)))
            tests_out[t["id"]] = {"ecl": t["ecl"], "included": included, "clauses": clauses}
            print("   {:<32} included {:>3}  pool {:>3}  clauses {}".format(
                t["id"], len(included), len(concepts), [len(c["satisfied"]) for c in clauses]))
        result[analyte] = {"pool_ecl": pool_ecl, "concepts": concepts, "tests": tests_out}

    OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("\nwrote", OUT)


if __name__ == "__main__":
    main()
