#!/usr/bin/env python3
"""
full_branch_diff.py — Complete concept-level diff between two SNOMED CT branches
served by (possibly different) Snowstorm endpoints.

Outputs:
  output/full_diff/concepts.md         — summary table + added/removed concept samples
  output/full_diff/added.tsv           — every concept active in B but not A
  output/full_diff/removed.tsv         — every concept active in A but not B
  output/full_diff/fsn_changed.tsv     — concepts active in both whose FSN differs
  output/full_diff/by_module.tsv       — added/removed counts grouped by module
  output/full_diff/raw.json            — set sizes + first effectiveTime per added concept

Strategy:
  1. Page through all active concepts on each branch via searchAfter
     (limit=10000, returns conceptId + fsn + moduleId).
  2. Set-diff conceptIds.
  3. For the intersection, compare FSNs (already in the paged payload — no extra calls).
  4. Group added/removed by moduleId to separate International vs LOINC-Extension drift.
"""

import json
import os
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "output" / "full_diff"
OUT_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(ROOT / "scripts"))
import targets as _targets

# A = previous, B = current (config/targets.json)
TARGETS = _targets.pair()

PAGE = 10000
CACHE_DIR = ROOT / "output" / "full_diff" / ".cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def fetch_page(url, params, attempts=6):
    delay = 5
    last_err = None
    for i in range(attempts):
        try:
            r = requests.get(url, params=params, timeout=300,
                             headers={"Accept-Language": "en-X-900000000000509007,en;q=0.9"})
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last_err = e
            print(f"    ! attempt {i+1} failed: {e!r}; sleep {delay}s", flush=True)
            time.sleep(delay)
            delay = min(delay * 2, 60)
    raise RuntimeError(f"Page failed after {attempts} attempts: {last_err}")


def fetch_all_active(api_base, branch, cache_name):
    """Returns dict[conceptId] = {'fsn': str, 'moduleId': str}. Cached to disk."""
    cache_file = CACHE_DIR / f"{cache_name}.json"
    if cache_file.exists():
        print(f"  ↳ using cache {cache_file.name}", flush=True)
        return json.loads(cache_file.read_text())

    url = f"{api_base.rstrip('/')}/{branch}/concepts"
    out = {}
    search_after = None
    page = 0
    started = time.time()
    while True:
        params = {"activeFilter": "true", "limit": PAGE}
        if search_after is not None:
            params["searchAfter"] = search_after
        data = fetch_page(url, params)
        items = data.get("items", [])
        if not items:
            break
        for it in items:
            cid = it.get("conceptId")
            if not cid:
                continue
            fsn = (it.get("fsn") or {}).get("term") or ""
            mod = it.get("moduleId") or ""
            out[cid] = {"fsn": fsn, "moduleId": mod}
        page += 1
        elapsed = time.time() - started
        print(f"  page {page}: {len(items)} items, total so far {len(out)}, elapsed {elapsed:.1f}s",
              flush=True)
        if len(items) < PAGE:
            break
        search_after = data.get("searchAfter")
        if not search_after:
            break
    cache_file.write_text(json.dumps(out))
    print(f"  ↳ cached to {cache_file.name}", flush=True)
    return out


def write_tsv(path, rows, header):
    with open(path, "w") as f:
        f.write("\t".join(header) + "\n")
        for r in rows:
            f.write("\t".join(str(c) for c in r) + "\n")


def main():
    print("Fetching all active concepts from both branches…", flush=True)
    sides = {}
    for t in TARGETS:
        print(f"  → {t['name']}", flush=True)
        sides[t["name"]] = fetch_all_active(t["api_base"], t["branch"], t["name"])

    a_name, b_name = TARGETS[0]["name"], TARGETS[1]["name"]
    A, B = sides[a_name], sides[b_name]
    a_ids, b_ids = set(A), set(B)

    only_a = a_ids - b_ids   # active in A only — "removed" going A→B
    only_b = b_ids - a_ids   # active in B only — "added"   going A→B
    both = a_ids & b_ids

    print(f"\nActive in A only (removed): {len(only_a):,}")
    print(f"Active in B only (added):   {len(only_b):,}")
    print(f"Active in both:             {len(both):,}")

    fsn_changed = []
    for cid in both:
        if A[cid]["fsn"] != B[cid]["fsn"]:
            fsn_changed.append((cid, A[cid]["fsn"], B[cid]["fsn"], A[cid]["moduleId"], B[cid]["moduleId"]))
    print(f"FSN changed on shared:      {len(fsn_changed):,}")

    # By-module breakdown
    def by_module(ids, src):
        agg = {}
        for cid in ids:
            mod = src[cid]["moduleId"] or "<none>"
            agg[mod] = agg.get(mod, 0) + 1
        return sorted(agg.items(), key=lambda x: -x[1])

    rm_by_mod = by_module(only_a, A)
    add_by_mod = by_module(only_b, B)

    # Write TSVs
    write_tsv(OUT_DIR / "removed.tsv",
              [(cid, A[cid]["fsn"], A[cid]["moduleId"]) for cid in sorted(only_a)],
              ["conceptId", "fsn_A", "moduleId_A"])
    write_tsv(OUT_DIR / "added.tsv",
              [(cid, B[cid]["fsn"], B[cid]["moduleId"]) for cid in sorted(only_b)],
              ["conceptId", "fsn_B", "moduleId_B"])
    write_tsv(OUT_DIR / "fsn_changed.tsv",
              fsn_changed,
              ["conceptId", "fsn_A", "fsn_B", "moduleId_A", "moduleId_B"])

    with open(OUT_DIR / "by_module.tsv", "w") as f:
        f.write("direction\tmoduleId\tcount\n")
        for mod, n in rm_by_mod:
            f.write(f"removed\t{mod}\t{n}\n")
        for mod, n in add_by_mod:
            f.write(f"added\t{mod}\t{n}\n")

    # Markdown summary
    md = []
    md.append("# Full Branch Diff — Active Concepts\n")
    md.append(f"- A = `{TARGETS[0]['branch']}` @ `{TARGETS[0]['api_base']}`")
    md.append(f"- B = `{TARGETS[1]['branch']}` @ `{TARGETS[1]['api_base']}`\n")
    md.append(f"| Metric | Count |")
    md.append(f"|---|---:|")
    md.append(f"| Active in A | {len(a_ids):,} |")
    md.append(f"| Active in B | {len(b_ids):,} |")
    md.append(f"| Only in A (removed in B) | {len(only_a):,} |")
    md.append(f"| Only in B (added in B)   | {len(only_b):,} |")
    md.append(f"| Active in both           | {len(both):,} |")
    md.append(f"| FSN changed on shared    | {len(fsn_changed):,} |\n")

    md.append("## Removed concepts, grouped by module (A side)\n")
    md.append("| moduleId | count |")
    md.append("|---|---:|")
    for mod, n in rm_by_mod:
        md.append(f"| `{mod}` | {n:,} |")
    md.append("")

    md.append("## Added concepts, grouped by module (B side)\n")
    md.append("| moduleId | count |")
    md.append("|---|---:|")
    for mod, n in add_by_mod:
        md.append(f"| `{mod}` | {n:,} |")
    md.append("")

    # Modules of interest
    INTL_MOD = "900000000000207008"
    LOINC_EXT = "11010000107"

    def sample_by_mod(ids, src, mod, k=15):
        rows = [(cid, src[cid]["fsn"]) for cid in sorted(ids) if src[cid]["moduleId"] == mod]
        return rows[:k], len(rows)

    md.append("## Sample: added in International module (`900000000000207008`)\n")
    sample, total = sample_by_mod(only_b, B, INTL_MOD)
    md.append(f"_{total:,} total_\n")
    for cid, fsn in sample:
        md.append(f"- `{cid}` — {fsn}")
    md.append("")

    md.append("## Sample: added in LOINC Extension module (`11010000107`)\n")
    sample, total = sample_by_mod(only_b, B, LOINC_EXT)
    md.append(f"_{total:,} total_\n")
    for cid, fsn in sample:
        md.append(f"- `{cid}` — {fsn}")
    md.append("")

    md.append("## Sample: removed in International module (`900000000000207008`)\n")
    sample, total = sample_by_mod(only_a, A, INTL_MOD)
    md.append(f"_{total:,} total_\n")
    for cid, fsn in sample:
        md.append(f"- `{cid}` — {fsn}")
    md.append("")

    md.append("## Sample: removed in LOINC Extension module (`11010000107`)\n")
    sample, total = sample_by_mod(only_a, A, LOINC_EXT)
    md.append(f"_{total:,} total_\n")
    for cid, fsn in sample:
        md.append(f"- `{cid}` — {fsn}")
    md.append("")

    md.append("## Sample: FSN changed (first 25)\n")
    md.append("| conceptId | A FSN | B FSN |")
    md.append("|---|---|---|")
    for cid, fa, fb, _, _ in fsn_changed[:25]:
        md.append(f"| `{cid}` | {fa} | {fb} |")

    (OUT_DIR / "concepts.md").write_text("\n".join(md))

    with open(OUT_DIR / "raw.json", "w") as f:
        json.dump({
            "targets": TARGETS,
            "counts": {
                "active_A": len(a_ids), "active_B": len(b_ids),
                "only_A": len(only_a), "only_B": len(only_b),
                "both": len(both), "fsn_changed": len(fsn_changed),
            },
            "removed_by_module": dict(rm_by_mod),
            "added_by_module": dict(add_by_mod),
        }, f, indent=2)

    print(f"\nWrote: {OUT_DIR}")


if __name__ == "__main__":
    main()
