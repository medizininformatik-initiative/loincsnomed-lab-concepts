#!/usr/bin/env python3
"""
compare_versions.py — Run the same ECL query against multiple Snowstorm
endpoints (different LOINCSNOMED editions, or public vs local) and produce
a diff: which concepts were added, removed, unchanged.

Default targets: [previous, current] from config/targets.json
(rotate them with scripts/update_release.py).

Override via TARGETS_CONFIG env var pointing to a JSON file shaped like:
  [
    {"name": "public-2025-09", "api_base": "...", "branch": "..."},
    {"name": "local-2026-03",  "api_base": "...", "branch": "..."}
  ]

Reads ECL queries from config/*_custom_ecl.json (same format the existing
analyzers consume).
"""

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from terminology_server_adapters import LOINCSNOMEDSnowstormAdapter
import targets as _targets

# Default targets come from config/targets.json: [previous, current]


def load_targets():
    cfg_path = os.getenv("TARGETS_CONFIG")
    if cfg_path:
        with open(cfg_path) as f:
            return json.load(f)
    return _targets.pair()


def load_queries(config_files):
    """Load ECL queries from one or more *_custom_ecl.json files."""
    queries = []
    for path in config_files:
        with open(path) as f:
            data = json.load(f)
        concept = Path(path).stem.replace("_custom_ecl", "")
        for q in data.get("queries", []):
            queries.append({
                "concept": concept,
                "id": q["id"],
                "name": q.get("name", q["id"]),
                "ecl": q["ecl"],
            })
    return queries


def fetch_codes(adapter, ecl, limit=5000):
    """Run ECL and return the set of SNOMED concept IDs."""
    result = adapter.execute_ecl_query(ecl, limit=limit)
    return {item["conceptId"] for item in result.get("items", [])}, result.get("total", 0)


def compare(targets, queries):
    """For each query, fetch results from each target and compute set diffs."""
    adapters = {t["name"]: LOINCSNOMEDSnowstormAdapter(api_base=t["api_base"], branch=t["branch"]) for t in targets}
    rows = []
    for q in queries:
        per_target = {}
        for name, adapter in adapters.items():
            try:
                codes, total = fetch_codes(adapter, q["ecl"])
                per_target[name] = {"codes": codes, "total": total, "error": None}
            except Exception as e:
                per_target[name] = {"codes": set(), "total": 0, "error": str(e)}

        names = list(per_target.keys())
        if len(names) == 2:
            a, b = names
            ca, cb = per_target[a]["codes"], per_target[b]["codes"]
            diff = {
                "only_in_a": sorted(ca - cb),
                "only_in_b": sorted(cb - ca),
                "in_both":   len(ca & cb),
            }
        else:
            diff = None

        rows.append({
            "concept": q["concept"],
            "query_id": q["id"],
            "query_name": q["name"],
            "ecl": q["ecl"],
            "per_target": {name: {"total": d["total"], "error": d["error"]} for name, d in per_target.items()},
            "diff": diff,
        })
    return rows, [t["name"] for t in targets]


def render_markdown(rows, target_names):
    out = ["# ECL Version Comparison\n"]
    out.append(f"**Targets:** {', '.join(target_names)}\n")
    headers = ["Concept", "Query"] + target_names
    if len(target_names) == 2:
        headers += ["Only A", "Only B", "Both"]
    out.append("| " + " | ".join(headers) + " |")
    out.append("|" + "|".join(["---"] * len(headers)) + "|")
    for r in rows:
        cells = [r["concept"], r["query_name"]]
        for name in target_names:
            t = r["per_target"][name]
            cells.append(str(t["total"]) if t["error"] is None else f"ERR: {t['error'][:30]}")
        if r["diff"]:
            cells += [str(len(r["diff"]["only_in_a"])), str(len(r["diff"]["only_in_b"])), str(r["diff"]["in_both"])]
        out.append("| " + " | ".join(cells) + " |")

    out.append("\n## Per-query detail\n")
    for r in rows:
        out.append(f"### {r['concept']} — {r['query_name']}")
        out.append(f"```\n{r['ecl']}\n```")
        if r["diff"] and len(target_names) == 2:
            a, b = target_names
            out.append(f"- **Only in {a}** ({len(r['diff']['only_in_a'])}): {', '.join(r['diff']['only_in_a'][:20])}"
                       + (" …" if len(r['diff']['only_in_a']) > 20 else ""))
            out.append(f"- **Only in {b}** ({len(r['diff']['only_in_b'])}): {', '.join(r['diff']['only_in_b'][:20])}"
                       + (" …" if len(r['diff']['only_in_b']) > 20 else ""))
            out.append(f"- **In both**: {r['diff']['in_both']}")
        out.append("")
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description="Compare ECL query results across SNOMED editions / servers")
    parser.add_argument("--config-glob", default="config/*_custom_ecl.json",
                        help="Glob for ECL config files (default: config/*_custom_ecl.json)")
    parser.add_argument("--out", default="output/version_comparison.md",
                        help="Markdown report output path")
    parser.add_argument("--json-out", default="output/version_comparison.json",
                        help="Raw JSON output path (for downstream tooling)")
    args = parser.parse_args()

    config_files = sorted(ROOT.glob(args.config_glob))
    if not config_files:
        sys.exit(f"No config files matched {args.config_glob}")

    targets = load_targets()
    queries = load_queries(config_files)
    print(f"Comparing {len(queries)} queries across {len(targets)} targets…")

    rows, target_names = compare(targets, queries)

    out_md = ROOT / args.out
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(render_markdown(rows, target_names))
    print(f"Markdown report: {out_md}")

    out_json = ROOT / args.json_out
    out_json.write_text(json.dumps(
        {"targets": targets, "rows": [{**r, "diff": (
            None if r["diff"] is None
            else {**r["diff"], "only_in_a": r["diff"]["only_in_a"], "only_in_b": r["diff"]["only_in_b"]}
        )} for r in rows]},
        indent=2))
    print(f"JSON output:     {out_json}")


if __name__ == "__main__":
    main()
