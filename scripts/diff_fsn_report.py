#!/usr/bin/env python3
"""
diff_fsn_report.py — human-readable companion to compare_versions.py.

compare_versions.py writes only SCTIDs for the per-query deltas. This script
reads its JSON output, resolves every 'only in A' / 'only in B' concept to FSN
and LOINC code (identifier file of the current pin) and writes one Markdown
file with the full lists, so a reviewer can read what a release added or
removed per request without opening Snowstorm.

Usage:
  python3 scripts/diff_fsn_report.py                                   # output/version_comparison.json
  python3 scripts/diff_fsn_report.py --json output/micro/version_comparison.json \
                                     --out  output/micro/added_removed.md
"""

import argparse
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import targets as _targets

HEADERS = {"Content-Type": "application/json",
           "Accept-Language": "en-X-900000000000509007,en-X-900000000000508004,en"}


def load_loinc_map(path):
    m = {}
    with open(path, encoding="utf-8") as f:
        next(f)
        for line in f:
            p = line.rstrip("\r\n").split("\t")
            if len(p) >= 6 and p[2] == "1":
                m[p[5]] = p[0]
    return m


def bulk_fsn(api_base, branch, ids):
    out = {}
    ids = list(ids)
    for i in range(0, len(ids), 200):
        req = urllib.request.Request(
            "{}/browser/{}/concepts/bulk-load".format(api_base, branch),
            data=json.dumps({"conceptIds": ids[i:i + 200]}).encode(), headers=HEADERS)
        for c in json.load(urllib.request.urlopen(req, timeout=300)):
            out[c["conceptId"]] = c["fsn"]["term"]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="output/version_comparison.json")
    ap.add_argument("--out", default="output/version_comparison_fsn.md")
    ap.add_argument("--max", type=int, default=400, help="max rows listed per direction and query")
    args = ap.parse_args()

    data = json.loads((ROOT / args.json).read_text())
    tgts = data["targets"]
    if len(tgts) != 2:
        sys.exit("expected exactly two targets in {}".format(args.json))
    a, b = tgts
    loinc = load_loinc_map(_targets.loinc_map_path())

    need_a, need_b = set(), set()
    for r in data["rows"]:
        if r["diff"]:
            need_a |= set(r["diff"]["only_in_a"])
            need_b |= set(r["diff"]["only_in_b"])
    fsn_a = bulk_fsn(a["api_base"], a["branch"], need_a)
    fsn_b = bulk_fsn(b["api_base"], b["branch"], need_b)

    md = ["# Release delta per request — concepts with FSN and LOINC", "",
          "- A = `{}` (`{}`)".format(a["name"], a["branch"]),
          "- B = `{}` (`{}`)".format(b["name"], b["branch"]),
          "- LOINC codes from `{}`".format(_targets.loinc_map_path().name), "",
          "| Request | Query | A | B | only A | only B | both |", "|---|---|---:|---:|---:|---:|---:|"]
    for r in data["rows"]:
        d = r["diff"] or {"only_in_a": [], "only_in_b": [], "in_both": 0}
        md.append("| {} | {} | {} | {} | {} | {} | {} |".format(
            r["concept"], r["query_name"], r["per_target"][a["name"]]["total"], r["per_target"][b["name"]]["total"],
            len(d["only_in_a"]), len(d["only_in_b"]), d["in_both"]))
    md.append("")

    def section(title, ids, fsn):
        if not ids:
            return
        md.append("**{}** ({})".format(title, len(ids)))
        md.append("")
        md.append("| LOINC | SCTID | FSN |")
        md.append("|---|---|---|")
        rows = sorted(ids, key=lambda c: (loinc.get(c, "~"), fsn.get(c, "")))
        for c in rows[:args.max]:
            md.append("| {} | {} | {} |".format(loinc.get(c, ""), c, fsn.get(c, "?")))
        if len(rows) > args.max:
            md.append("| … | … | {} more |".format(len(rows) - args.max))
        md.append("")

    for r in data["rows"]:
        if not r["diff"]:
            continue
        md.append("## {} — {}".format(r["concept"], r["query_name"]))
        md.append("")
        md.append("```\n{}\n```".format(r["ecl"]))
        md.append("")
        section("Only in B (added)", r["diff"]["only_in_b"], fsn_b)
        section("Only in A (removed)", r["diff"]["only_in_a"], fsn_a)

    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("wrote", out, "(", len(need_b), "added /", len(need_a), "removed concepts resolved )")


if __name__ == "__main__":
    main()
