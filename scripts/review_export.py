#!/usr/bin/env python3
"""
review_export.py — Reviewer-friendly XLSX/CSV export of an analyte's ECL logic,
organised by USE-CASE aggregation profiles (INTERPOLAR pattern).

Rationale (from clinical reviewers):
  A lab physician reviews best in XLSX/CSV. In a *filtered* result list, false
  POSITIVES are visible (a wrong concept sits in the list and gets noticed), but
  false NEGATIVES are invisible — a wrongly excluded concept is simply absent.
  So we ship the COMPLETE candidate pool and mark, per concept, which USE-CASE
  bucket captures it.

Use case defines the aggregation:
  The "right" ValueSet is not one fixed list — it depends on the use case.
  Buckets and the signal concepts live in config/aggregation_profiles.json.
  Classification uses BOTH Scale type AND Property, because Scale type is not
  always asserted (generic 'Measurement of X' groupers and Presence observables
  carry only a Property). Rule (first match wins):
    1. qualitative       — Ordinal/Nominal scale OR Presence property
    2. semiquantitative  — Semi-quantitative scale
    3. quantitative      — Quantitative scale OR any Measurement property
                           (this pulls in the generic groupers = full lists);
                           convertible = concentration property, excl ratio/fraction
    4. UNCLASSIFIED      — none of the above (reviewer decides)

Layout (one file per analyte):
  Rows    = candidate pool (the 'complete' bucket)
  Columns = SCTID | FSN | PT | <one column per bucket: Y/·> | Use case | Reason
  Highlight (XLSX) = UNCLASSIFIED pool concepts.

Component resolution per analyte config:
  1. explicit  "component_ecl"  field, else
  2. Component clause (attr 246093002) lifted from the first query, else
  3. the focus expression of the first query (part before ':').

Usage:
  python3 scripts/review_export.py                        # all analytes, local
  python3 scripts/review_export.py --config config/psa_custom_ecl.json
  python3 scripts/review_export.py --target public
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from terminology_server_adapters import LOINCSNOMEDSnowstormAdapter

import targets as _targets

# Edition pins live in config/targets.json ("local" = current, "public" = previous)
TARGETS = _targets.cli_targets()

OBSERVABLE_ROOT = "<< 363787002 |Observable entity (observable entity)|"
COMPONENT_ATTR = "246093002"
PROFILES_PATH = ROOT / "config" / "aggregation_profiles.json"

# LOINC code ↔ SNOMED concept mapping lives in the LOINCSNOMED edition itself
# (RF2 sct2_Identifier file, alternate-identifier scheme below). Snowstorm does
# not expose it via API, so we read the extracted file directly.
LOINC_SCHEME = "30051010000102"
LOINC_MAP_PATH = _targets.loinc_map_path()


def load_loinc_map(path):
    """Return dict SNOMED conceptId -> LOINC code from the RF2 Identifier file."""
    m = {}
    if not Path(path).exists():
        print("  (LOINC map not found at {} — LOINC column will be empty)".format(path))
        return m
    with open(path) as f:
        next(f, None)  # header
        for line in f:
            p = line.rstrip("\n").split("\t")
            # alternateIdentifier, effectiveTime, active, moduleId, schemeId, refComp
            if len(p) >= 6 and p[2] == "1" and p[4] == LOINC_SCHEME:
                m[p[5]] = p[0]
    return m


def load_profiles():
    with open(PROFILES_PATH) as f:
        return json.load(f)


def load_config(path):
    with open(path) as f:
        data = json.load(f)
    concept = Path(path).stem.replace("_custom_ecl", "")
    return concept, data


def derive_component(data):
    """Return (base_refinement, focus_expr, how)."""
    if data.get("component_ecl"):
        return data["component_ecl"], None, "explicit component_ecl"

    queries = data.get("queries", [])
    if not queries:
        raise ValueError("config has neither component_ecl nor queries")
    first = queries[0]["ecl"]

    m = re.search(
        COMPONENT_ATTR + r"\s*\|[^|]*\|\s*=\s*((?:<<\s*)?\d+\s*\|[^|]*\|)",
        first,
    )
    if m:
        clause = "<< {} |Component (attribute)| = {}".format(
            COMPONENT_ATTR, m.group(1).strip())
        return clause, None, "Component-only pool"

    focus = first.split(":", 1)[0].strip()
    return None, focus, "focus subtree (no Component attribute)"


def or_list(attr, ids):
    """Build an ECL attribute clause: attr = (<<a OR <<b ...)."""
    inner = " OR ".join("<< {}".format(i) for i in ids)
    return "<< {} = ({})".format(attr, inner)


class Probe:
    """Runs signal ECLs for one analyte's candidate pool."""

    def __init__(self, adapter, base_refinement, focus_expr, prof):
        self.adapter = adapter
        self.base_refinement = base_refinement
        self.focus_expr = focus_expr
        self.attr = prof["attributes"]
        self.scale = prof["scale_types"]
        self.prop = prof["properties"]

    def _ecl(self, clause):
        if self.base_refinement:
            parts = [self.base_refinement] + ([clause] if clause else [])
            return "{} : {}".format(OBSERVABLE_ROOT, ", ".join(parts))
        if clause:
            return "{} : {}".format(self.focus_expr, clause)
        return self.focus_expr

    def run(self, clause):
        return run_ecl(self.adapter, self._ecl(clause))

    def signal_sets(self):
        st = self.attr["scale_type"]
        pr = self.attr["property"]
        sets = {}
        sets["pool"] = self.run("")
        sets["scale_quant"] = set(self.run(
            "<< {} = << {}".format(st, self.scale["quantitative"])))
        sets["scale_semiquant"] = set(self.run(
            "<< {} = << {}".format(st, self.scale["semiquantitative"])))
        sets["scale_ordnom"] = set(self.run(
            or_list(st, [self.scale["ordinal"], self.scale["nominal"]])))
        sets["prop_any"] = set(self.run("<< {} = *".format(pr)))
        sets["prop_presence"] = set(self.run(or_list(pr, self.prop["presence"])))
        sets["prop_measurement"] = set(self.run(
            "<< {} = << {}".format(pr, self.prop["measurement"])))
        sets["prop_concentration"] = set(self.run(
            or_list(pr, self.prop["concentration"])))
        sets["prop_ratiofraction"] = set(self.run(
            or_list(pr, self.prop["ratio_fraction"])))
        return sets


def run_ecl(adapter, ecl, limit=10000):
    """Return dict conceptId -> {fsn, pt}."""
    result = adapter.execute_ecl_query(ecl, limit=limit)
    total = result.get("total", 0)
    if total > limit:
        print("    !! TRUNCATED: {} concepts, only {} loaded".format(total, limit))
    out = {}
    for item in result.get("items", []):
        cid = item.get("conceptId")
        if not cid:
            continue
        out[cid] = {
            "fsn": (item.get("fsn") or {}).get("term", ""),
            "pt": (item.get("pt") or {}).get("term", ""),
        }
    return out


def classify(cid, s):
    """Return (use_case, reason, bucket_membership dict) via first-match rules."""
    if cid not in s["prop_any"]:
        return "panel_order", "no Property attribute → order/panel code", {"panel_order"}
    if cid in s["scale_ordnom"] or cid in s["prop_presence"]:
        reason = ("Presence property → qualitative"
                  if cid in s["prop_presence"] and cid not in s["scale_ordnom"]
                  else "Ordinal/Nominal scale → qualitative")
        return "qualitative", reason, {"qualitative"}
    if cid in s["scale_semiquant"]:
        return "semiquantitative", "Semi-quantitative scale (test strip)", {"semiquantitative"}
    if cid in s["scale_quant"] or cid in s["prop_measurement"]:
        convertible = cid in s["prop_concentration"] and cid not in s["prop_ratiofraction"]
        if cid in s["scale_quant"]:
            base = "Quantitative scale"
        else:
            base = "Measurement property, no scale asserted (generic)"
        if convertible:
            return "quantitative_convertible", base + " + concentration property", \
                   {"quantitative", "quantitative_convertible"}
        return "quantitative", base, {"quantitative"}
    return "UNCLASSIFIED", "no Scale type and no Measurement/Presence property", set()


def build_analyte(adapter, concept, data, prof, loinc_map):
    base_refinement, focus_expr, how = derive_component(data)
    print("  component ({}): {}".format(how, base_refinement or focus_expr))

    probe = Probe(adapter, base_refinement, focus_expr, prof)
    s = probe.signal_sets()
    pool = s.pop("pool")

    buckets = prof["buckets"]
    bucket_ids = [b["id"] for b in buckets]
    counts = {bid: 0 for bid in bucket_ids}

    rows = []
    for cid, meta in pool.items():
        usecase, reason, membership = classify(cid, s)
        membership = set(membership) | {"complete"}
        for bid in membership:
            if bid in counts:
                counts[bid] += 1
        marks = ["Y" if b["id"] in membership else "·" for b in buckets]
        classified = usecase != "UNCLASSIFIED"
        rows.append({
            "sctid": cid, "loinc": loinc_map.get(cid, ""),
            "fsn": meta["fsn"], "pt": meta["pt"],
            "marks": marks, "classified": classified,
            "usecase": usecase, "reason": reason,
        })
    rows.sort(key=lambda r: (r["classified"], r["usecase"], r["fsn"].lower()))

    order = {"UNCLASSIFIED": 0, "qualitative": 1, "semiquantitative": 2,
             "quantitative": 3, "quantitative_convertible": 4}
    for b in buckets:
        print("    {:<42} {:>4}".format(b["name"][:42], counts[b["id"]]))

    return {
        "concept": concept, "how": how,
        "component": base_refinement or focus_expr,
        "buckets": buckets, "counts": counts,
        "rows": rows, "pool_size": len(pool),
        "unclassified": sum(1 for r in rows if not r["classified"]),
    }


def write_csv(res, path):
    names = [b["name"] for b in res["buckets"]]
    header = ["LOINC", "SCTID", "FSN", "PT"] + names + ["Use case", "Reason"]
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in res["rows"]:
            w.writerow([r["loinc"], r["sctid"], r["fsn"], r["pt"]] + r["marks"]
                       + [r["usecase"], r["reason"]])


def write_xlsx(res, path):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    wb = Workbook()
    ws = wb.active
    ws.title = res["concept"][:31]

    hdr_fill = PatternFill("solid", fgColor="34495E")
    hdr_font = Font(color="FFFFFF", bold=True)
    warn_fill = PatternFill("solid", fgColor="FFF2CC")
    hit_font = Font(color="1E7B34", bold=True)
    thin = Side(style="thin", color="DDDDDD")
    border = Border(bottom=thin)

    ws.append(["Analyte:", res["concept"]])
    ws.append(["Component pool ({}):".format(res["how"]), res["component"]])
    ws.append(["Pool size:", res["pool_size"],
               "Unclassified (highlighted):", res["unclassified"]])
    ws.append([])
    ws.append(["Use-case buckets (columns) — classified by Scale type + Property:"])
    for b in res["buckets"]:
        ws.append(["  {} = {}".format(b["name"], res["counts"][b["id"]]),
                   b["description"]])
    ws.append([])
    header_row_idx = ws.max_row + 1

    names = [b["name"] for b in res["buckets"]]
    header = ["LOINC", "SCTID", "FSN", "PT"] + names + ["Use case", "Reason"]
    ws.append(header)
    for c in range(1, len(header) + 1):
        cell = ws.cell(row=header_row_idx, column=c)
        cell.fill = hdr_fill
        cell.font = hdr_font
        cell.alignment = Alignment(vertical="center", wrap_text=True)

    n_b = len(res["buckets"])
    mark_col0 = 5  # first bucket column (after LOINC, SCTID, FSN, PT)
    for r in res["rows"]:
        row = [r["loinc"], r["sctid"], r["fsn"], r["pt"]] + r["marks"] + [r["usecase"], r["reason"]]
        ws.append(row)
        ridx = ws.max_row
        for c in range(1, len(row) + 1):
            ws.cell(row=ridx, column=c).border = border
        if not r["classified"]:
            for c in range(1, len(row) + 1):
                ws.cell(row=ridx, column=c).fill = warn_fill
        for j in range(n_b):
            cell = ws.cell(row=ridx, column=mark_col0 + j)
            if cell.value == "Y":
                cell.font = hit_font
            cell.alignment = Alignment(horizontal="center")

    ws.freeze_panes = ws.cell(row=header_row_idx + 1, column=1)
    ws.auto_filter.ref = "A{}:{}{}".format(
        header_row_idx, get_column_letter(len(header)), ws.max_row)

    widths = [12, 18, 55, 40] + [14] * n_b + [22, 50]
    for i, wdt in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = wdt

    wb.save(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", action="append")
    ap.add_argument("--target", choices=list(TARGETS), default="local")
    ap.add_argument("--out-dir", default="output/review")
    ap.add_argument("--loinc-map", default=str(LOINC_MAP_PATH),
                    help="RF2 sct2_Identifier file with LOINC alternate identifiers")
    args = ap.parse_args()

    if args.config:
        config_files = [Path(c) for c in args.config]
    else:
        config_files = sorted(ROOT.glob("config/*_custom_ecl.json"))
    if not config_files:
        sys.exit("No config files found.")

    prof = load_profiles()
    tgt = TARGETS[args.target]
    print("Target: {} ({} @ {})".format(tgt["name"], tgt["branch"], tgt["api_base"]))
    print("Buckets: {}".format(", ".join(b["id"] for b in prof["buckets"])))
    loinc_map = load_loinc_map(args.loinc_map)
    print("LOINC map: {} concept→code entries\n".format(len(loinc_map)))
    adapter = LOINCSNOMEDSnowstormAdapter(api_base=tgt["api_base"], branch=tgt["branch"])

    out_dir = ROOT / args.out_dir / tgt["name"]
    out_dir.mkdir(parents=True, exist_ok=True)

    summary = []
    for cf in config_files:
        concept, data = load_config(cf)
        print("{}:".format(concept))
        res = build_analyte(adapter, concept, data, prof, loinc_map)
        write_csv(res, out_dir / "{}_review.csv".format(concept))
        write_xlsx(res, out_dir / "{}_review.xlsx".format(concept))
        summary.append((concept, res["counts"], res["pool_size"], res["unclassified"]))
        print()

    print("=== Summary (concepts per use-case bucket) ===")
    bids = [b["id"] for b in prof["buckets"]]
    print("{:<16} {}  {:>6}".format("analyte",
          "  ".join("{:>8}".format(b[:8]) for b in bids), "uncls"))
    for concept, counts, pool, uncls in summary:
        print("{:<16} {}  {:>6}".format(concept,
              "  ".join("{:>8}".format(counts[b]) for b in bids), uncls))
    print("\nWritten to: {}".format(out_dir))


if __name__ == "__main__":
    main()
