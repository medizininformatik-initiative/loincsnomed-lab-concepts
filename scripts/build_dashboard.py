#!/usr/bin/env python3
"""
build_dashboard.py — Assemble a self-contained HTML dashboard from the
LOINCSNOMED version-comparison outputs:

  output/full_diff/added.tsv
  output/full_diff/removed.tsv
  output/full_diff/fsn_changed.tsv
  output/full_diff/by_module.tsv
  output/full_diff/raw.json
  output/version_comparison.json          (cross-analyte)
  output/psa_version_comparison.json
  output/ldh_version_comparison.json

Output:
  output/dashboard/index.html             (open with file://, no server needed)
"""
import csv
import json
import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import targets as _targets
_prev, _cur = _targets.pair()

FD = ROOT / "output" / "full_diff"
OUT = ROOT / "output" / "dashboard"
OUT.mkdir(parents=True, exist_ok=True)

MODULE_LABELS = {
    "900000000000207008": "SNOMED CT International",
    "11010000107": "LOINC Extension",
    "900000000000012004": "SNOMED CT model component",
}

SEMTAG_RE = re.compile(r"\(([^)]+)\)\s*$")


def parse_semtag(fsn: str) -> str:
    m = SEMTAG_RE.search(fsn or "")
    return m.group(1) if m else "(unknown)"


def read_tsv(path):
    with open(path) as f:
        return list(csv.DictReader(f, delimiter="\t"))


def semtag_breakdown(rows, fsn_field):
    agg = {}
    for r in rows:
        st = parse_semtag(r.get(fsn_field, ""))
        agg[st] = agg.get(st, 0) + 1
    return sorted(agg.items(), key=lambda x: -x[1])


def annotate(rows, fsn_field):
    out = []
    for r in rows:
        cid = r["conceptId"]
        fsn = r.get(fsn_field, "")
        mod = r.get("moduleId_A") or r.get("moduleId_B") or r.get("moduleId") or ""
        out.append({
            "id": cid,
            "fsn": fsn,
            "tag": parse_semtag(fsn),
            "mod": mod,
        })
    return out


def main():
    raw = json.loads((FD / "raw.json").read_text())
    by_module = read_tsv(FD / "by_module.tsv")

    added_rows = read_tsv(FD / "added.tsv")
    removed_rows = read_tsv(FD / "removed.tsv")
    fsn_rows = read_tsv(FD / "fsn_changed.tsv")

    added = [{"id": r["conceptId"], "fsn": r["fsn_B"], "tag": parse_semtag(r["fsn_B"]), "mod": r["moduleId_B"]}
             for r in added_rows]
    removed = [{"id": r["conceptId"], "fsn": r["fsn_A"], "tag": parse_semtag(r["fsn_A"]), "mod": r["moduleId_A"]}
               for r in removed_rows]
    fsn_changed = [{"id": r["conceptId"], "a": r["fsn_A"], "b": r["fsn_B"],
                    "tag": parse_semtag(r["fsn_B"]), "modA": r["moduleId_A"], "modB": r["moduleId_B"]}
                   for r in fsn_rows]

    added_tags = semtag_breakdown(added_rows, "fsn_B")
    removed_tags = semtag_breakdown(removed_rows, "fsn_A")
    changed_tags = semtag_breakdown(fsn_rows, "fsn_B")

    # Per-analyte
    analyte_files = [
        ("Cross-analyte (panel)", ROOT / "output/version_comparison.json"),
        ("PSA", ROOT / "output/psa_version_comparison.json"),
        ("LDH", ROOT / "output/ldh_version_comparison.json"),
    ]
    analytes = []
    for label, p in analyte_files:
        if not p.exists():
            continue
        d = json.loads(p.read_text())
        rows = []
        for r in d.get("rows", []):
            per = r.get("per_target", {})
            diff = r.get("diff") or {}
            tnames = list(per.keys())
            rows.append({
                "concept": r["concept"],
                "query": r["query_name"],
                "ecl": r["ecl"],
                "a": tnames[0] if len(tnames) > 0 else "",
                "b": tnames[1] if len(tnames) > 1 else "",
                "a_total": per.get(tnames[0], {}).get("total") if tnames else None,
                "b_total": per.get(tnames[1], {}).get("total") if len(tnames) > 1 else None,
                "only_a": diff.get("only_in_a", []),
                "only_b": diff.get("only_in_b", []),
                "in_both": diff.get("in_both", 0),
            })
        analytes.append({"label": label, "rows": rows})

    bundle = {
        "meta": {
            "a_branch": _prev["branch"],
            "a_endpoint": _prev["api_base"],
            "b_branch": _cur["branch"],
            "b_endpoint": _cur["api_base"],
        },
        "counts": raw["counts"],
        "module_labels": MODULE_LABELS,
        "added_by_module": raw["added_by_module"],
        "removed_by_module": raw["removed_by_module"],
        "added_tags": added_tags,
        "removed_tags": removed_tags,
        "changed_tags": changed_tags,
        "added": added,
        "removed": removed,
        "fsn_changed": fsn_changed,
        "analytes": analytes,
    }

    html = render_html(bundle)
    (OUT / "index.html").write_text(html)
    print(f"Wrote {OUT/'index.html'}  ({len(html):,} chars)")
    print(f"Open: file://{(OUT/'index.html').resolve()}")


def render_html(bundle: dict) -> str:
    payload = json.dumps(bundle, separators=(",", ":"))
    # Escape only </script> for safe inline embedding
    payload = payload.replace("</", "<\\/")
    return TEMPLATE.replace("__BUNDLE__", payload)


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>LOINCSNOMED Version Diff Dashboard</title>
<style>
  :root {
    --bg: #0f1216; --panel: #1a1f27; --panel2: #232a34; --line: #2c3340;
    --text: #e6e9ef; --muted: #97a0ad; --accent: #61dafb; --accent2: #f8c155;
    --good: #5fd07e; --bad: #ee6c6c; --warn: #f59f4d;
    --mod-intl: #5fb1ee; --mod-loinc: #f8c155; --mod-other: #b48ff5;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; background: var(--bg); color: var(--text);
    font: 13px/1.45 -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; }
  a { color: var(--accent); text-decoration: none; }
  header { padding: 18px 24px 8px; border-bottom: 1px solid var(--line); }
  header h1 { margin: 0 0 4px 0; font-size: 16px; font-weight: 600; letter-spacing: .3px; }
  header .branches { color: var(--muted); font-size: 12px; }
  header .branches code { background: var(--panel2); padding: 1px 5px; border-radius: 3px; }
  nav { display: flex; gap: 2px; padding: 0 24px; background: var(--panel);
    border-bottom: 1px solid var(--line); }
  nav button { background: transparent; border: 0; color: var(--muted);
    padding: 11px 16px; cursor: pointer; font: inherit; border-bottom: 2px solid transparent; }
  nav button.active { color: var(--text); border-bottom-color: var(--accent); }
  nav button:hover { color: var(--text); }
  main { padding: 20px 24px 40px; }
  section { display: none; }
  section.active { display: block; }
  .kpi-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 14px; margin-bottom: 22px; }
  .kpi { background: var(--panel); border: 1px solid var(--line); border-radius: 6px;
    padding: 14px 16px; }
  .kpi .label { color: var(--muted); font-size: 11px; text-transform: uppercase; letter-spacing: .5px; }
  .kpi .value { font-size: 22px; font-weight: 600; margin-top: 4px; }
  .kpi .delta { font-size: 11px; color: var(--muted); margin-top: 2px; }
  .kpi.added .value { color: var(--good); }
  .kpi.removed .value { color: var(--bad); }
  .kpi.changed .value { color: var(--warn); }
  .panel { background: var(--panel); border: 1px solid var(--line); border-radius: 6px;
    padding: 14px 16px; margin-bottom: 18px; }
  .panel h3 { margin: 0 0 10px 0; font-size: 13px; font-weight: 600; color: var(--text); }
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
  @media (max-width: 900px) { .grid-2 { grid-template-columns: 1fr; } }
  .bar-row { display: grid; grid-template-columns: 200px 1fr 60px; gap: 10px;
    align-items: center; padding: 3px 0; }
  .bar-row .name { color: var(--muted); font-size: 12px; overflow: hidden;
    text-overflow: ellipsis; white-space: nowrap; }
  .bar-row .bar { background: var(--panel2); height: 18px; border-radius: 3px;
    position: relative; overflow: hidden; }
  .bar-row .bar > span { display: block; height: 100%; background: var(--accent); }
  .bar-row .bar.added > span { background: var(--good); }
  .bar-row .bar.removed > span { background: var(--bad); }
  .bar-row .bar.changed > span { background: var(--warn); }
  .bar-row .count { text-align: right; font-variant-numeric: tabular-nums; font-size: 12px; color: var(--text); }
  .module-mix { display: flex; height: 24px; border-radius: 4px; overflow: hidden; margin: 6px 0 12px; }
  .module-mix > div { display: flex; align-items: center; justify-content: center;
    color: #0f1216; font-size: 11px; font-weight: 600; }
  .legend { display: flex; gap: 14px; flex-wrap: wrap; font-size: 11px; color: var(--muted); }
  .legend-dot { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 5px;
    vertical-align: middle; }
  .controls { display: flex; gap: 10px; margin-bottom: 12px; flex-wrap: wrap; align-items: center; }
  .controls input[type=search], .controls select { background: var(--panel); border: 1px solid var(--line);
    color: var(--text); padding: 7px 10px; border-radius: 4px; font: inherit; }
  .controls input[type=search] { min-width: 260px; }
  .controls .meta { color: var(--muted); font-size: 12px; margin-left: auto; }
  table { width: 100%; border-collapse: collapse; font-size: 12px; }
  table th { text-align: left; color: var(--muted); font-weight: 500;
    padding: 8px 10px; border-bottom: 1px solid var(--line); background: var(--panel);
    position: sticky; top: 0; z-index: 1; }
  table td { padding: 7px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
  table tr:hover td { background: rgba(255,255,255,0.02); }
  .cid { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: 11.5px; color: var(--accent); }
  .tag { display: inline-block; background: var(--panel2); color: var(--muted);
    padding: 1px 6px; border-radius: 9px; font-size: 10.5px; }
  .mod-pill { display: inline-block; padding: 1px 6px; border-radius: 3px; font-size: 10.5px;
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
  .mod-intl { background: rgba(95,177,238,.15); color: var(--mod-intl); }
  .mod-loinc { background: rgba(248,193,85,.15); color: var(--mod-loinc); }
  .mod-other { background: rgba(180,143,245,.15); color: var(--mod-other); }
  .diff-old { color: var(--bad); text-decoration: line-through; opacity: .85; }
  .diff-new { color: var(--good); }
  .ecl { background: #0b0e12; border: 1px solid var(--line); padding: 8px 10px; border-radius: 4px;
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 11.5px;
    white-space: pre-wrap; overflow-x: auto; color: var(--muted); }
  .pager { display: flex; gap: 6px; justify-content: center; padding: 14px 0; }
  .pager button { background: var(--panel); border: 1px solid var(--line); color: var(--text);
    padding: 4px 10px; border-radius: 3px; cursor: pointer; font: inherit; }
  .pager button:disabled { opacity: .35; cursor: default; }
  .empty { color: var(--muted); text-align: center; padding: 30px; font-style: italic; }
  .analyte-row td { vertical-align: middle; }
  .analyte-delta { font-weight: 600; }
  .analyte-delta.zero { color: var(--muted); }
  .analyte-delta.pos { color: var(--good); }
  .analyte-delta.neg { color: var(--bad); }
  details.q { background: var(--panel); border: 1px solid var(--line); border-radius: 5px;
    padding: 8px 12px; margin-bottom: 8px; }
  details.q summary { cursor: pointer; font-weight: 500; }
  details.q .body { margin-top: 10px; color: var(--muted); }
  details.q .body ul { margin: 4px 0 8px 18px; padding: 0; }
  details.q .body li { font-family: ui-monospace, monospace; font-size: 11.5px; }
</style>
</head>
<body>

<header>
  <h1>LOINCSNOMED Version-Diff Dashboard</h1>
  <div class="branches">
    A = <code id="a-branch"></code> @ <code id="a-endpoint"></code>
    &nbsp;→&nbsp;
    B = <code id="b-branch"></code> @ <code id="b-endpoint"></code>
  </div>
</header>

<nav>
  <button data-tab="overview" class="active">Overview</button>
  <button data-tab="added">Added (B only)</button>
  <button data-tab="removed">Removed (A only)</button>
  <button data-tab="changed">FSN Changed</button>
  <button data-tab="analytes">Per-Analyte</button>
  <button data-tab="story">Coordination</button>
</nav>

<main>
  <section id="overview" class="active">
    <div class="kpi-row" id="kpi-row"></div>
    <div class="grid-2">
      <div class="panel">
        <h3>Module attribution — additions (B only)</h3>
        <div class="module-mix" id="mix-added"></div>
        <div class="legend" id="legend-added"></div>
      </div>
      <div class="panel">
        <h3>Module attribution — removals (A only)</h3>
        <div class="module-mix" id="mix-removed"></div>
        <div class="legend" id="legend-removed"></div>
      </div>
    </div>
    <div class="grid-2">
      <div class="panel">
        <h3>Top semantic tags — added</h3>
        <div id="tags-added"></div>
      </div>
      <div class="panel">
        <h3>Top semantic tags — removed</h3>
        <div id="tags-removed"></div>
      </div>
    </div>
    <div class="panel">
      <h3>Top semantic tags — FSN changed (B side tag)</h3>
      <div id="tags-changed"></div>
    </div>
  </section>

  <section id="added">
    <div class="controls">
      <input id="search-added" type="search" placeholder="Search FSN or concept ID…">
      <select id="filter-added-tag"><option value="">All semantic tags</option></select>
      <select id="filter-added-mod"><option value="">All modules</option></select>
      <span class="meta" id="meta-added"></span>
    </div>
    <div class="panel" style="padding: 0;">
      <table>
        <thead><tr><th style="width:160px">Concept ID</th><th>FSN (B)</th><th style="width:170px">Tag</th><th style="width:170px">Module</th></tr></thead>
        <tbody id="tbody-added"></tbody>
      </table>
    </div>
    <div class="pager" id="pager-added"></div>
  </section>

  <section id="removed">
    <div class="controls">
      <input id="search-removed" type="search" placeholder="Search FSN or concept ID…">
      <select id="filter-removed-tag"><option value="">All semantic tags</option></select>
      <select id="filter-removed-mod"><option value="">All modules</option></select>
      <span class="meta" id="meta-removed"></span>
    </div>
    <div class="panel" style="padding: 0;">
      <table>
        <thead><tr><th style="width:160px">Concept ID</th><th>FSN (A — removed)</th><th style="width:170px">Tag</th><th style="width:170px">Module</th></tr></thead>
        <tbody id="tbody-removed"></tbody>
      </table>
    </div>
    <div class="pager" id="pager-removed"></div>
  </section>

  <section id="changed">
    <div class="controls">
      <input id="search-changed" type="search" placeholder="Search either FSN or concept ID…">
      <select id="filter-changed-tag"><option value="">All semantic tags</option></select>
      <span class="meta" id="meta-changed"></span>
    </div>
    <div class="panel" style="padding: 0;">
      <table>
        <thead><tr><th style="width:160px">Concept ID</th><th>Before (A) → After (B)</th><th style="width:170px">Tag</th></tr></thead>
        <tbody id="tbody-changed"></tbody>
      </table>
    </div>
    <div class="pager" id="pager-changed"></div>
  </section>

  <section id="analytes">
    <div id="analytes-body"></div>
  </section>

  <section id="story">
    <div class="panel" style="padding:18px;">
      <h3 style="margin-bottom:12px">Why this content drop happened — tri-organizational coordination</h3>
      <div style="background:#0b0e12; border:1px solid var(--line); border-radius:6px; padding:8px; text-align:center;">
        <object type="image/svg+xml" data="coordination.svg" style="width:100%; max-width:1280px; height:auto;">
          <img src="coordination.svg" alt="Tri-organizational coordination diagram"/>
        </object>
      </div>
      <p style="color:var(--muted); margin-top:14px; font-size:12px;">
        SCTID provenance evidence: 121 new "Antigen of …" substances live in SNOMED International's <em>core namespace</em>
        (contiguous block <code>1381232009 – 1381477009</code>), while 3,627 new observable concepts live in the
        LOINC-Extension namespace (suffix <code>…1010000XXX</code>). Both ship in module <code>11010000107</code>
        with <code>effectiveTime 20260321</code>. SVG source:
        <a href="coordination.svg">coordination.svg</a>
      </p>
    </div>
  </section>
</main>

<script>
const D = __BUNDLE__;
const PAGE = 100;

function fmt(n) { return n == null ? "" : Number(n).toLocaleString(); }
function modClass(mid) {
  if (mid === "900000000000207008") return "mod-intl";
  if (mid === "11010000107") return "mod-loinc";
  return "mod-other";
}
function modLabel(mid) { return D.module_labels[mid] || mid; }
function modPill(mid) { return `<span class="mod-pill ${modClass(mid)}" title="${modLabel(mid)}">${modLabel(mid)}</span>`; }
function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  })[c]);
}

// Header
document.getElementById("a-branch").textContent = D.meta.a_branch;
document.getElementById("a-endpoint").textContent = D.meta.a_endpoint;
document.getElementById("b-branch").textContent = D.meta.b_branch;
document.getElementById("b-endpoint").textContent = D.meta.b_endpoint;

// Tabs
for (const btn of document.querySelectorAll("nav button")) {
  btn.addEventListener("click", () => {
    for (const b of document.querySelectorAll("nav button")) b.classList.toggle("active", b === btn);
    for (const s of document.querySelectorAll("main > section"))
      s.classList.toggle("active", s.id === btn.dataset.tab);
  });
}

// === Overview ===
function renderKPIs() {
  const c = D.counts;
  const kpis = [
    {label: "Active in A", value: c.active_A, cls: ""},
    {label: "Active in B", value: c.active_B, delta: ((c.active_B - c.active_A) >= 0 ? "+" : "") + fmt(c.active_B - c.active_A), cls: ""},
    {label: "Added in B", value: c.only_B, cls: "added"},
    {label: "Removed in B", value: c.only_A, cls: "removed"},
    {label: "FSN changed", value: c.fsn_changed, cls: "changed"},
    {label: "Shared", value: c.both, cls: ""},
  ];
  document.getElementById("kpi-row").innerHTML = kpis.map(k => `
    <div class="kpi ${k.cls}">
      <div class="label">${k.label}</div>
      <div class="value">${fmt(k.value)}</div>
      ${k.delta ? `<div class="delta">Δ ${k.delta}</div>` : ""}
    </div>`).join("");
}

function renderMix(elId, legendId, dataByMod) {
  const total = Object.values(dataByMod).reduce((a,b) => a+b, 0);
  const entries = Object.entries(dataByMod).sort((a,b) => b[1]-a[1]);
  const colors = { "900000000000207008": "var(--mod-intl)", "11010000107": "var(--mod-loinc)" };
  document.getElementById(elId).innerHTML = entries.map(([mid, n]) => {
    const pct = (n/total*100);
    const color = colors[mid] || "var(--mod-other)";
    return `<div style="width:${pct}%; background:${color};" title="${modLabel(mid)}: ${fmt(n)} (${pct.toFixed(1)}%)">${pct > 8 ? `${pct.toFixed(0)}%` : ""}</div>`;
  }).join("");
  document.getElementById(legendId).innerHTML = entries.map(([mid, n]) => {
    const color = colors[mid] || "var(--mod-other)";
    return `<span><span class="legend-dot" style="background:${color}"></span>${modLabel(mid)} — ${fmt(n)}</span>`;
  }).join("");
}

function renderBars(elId, items, cls, topN = 12) {
  const top = items.slice(0, topN);
  const max = top.length ? top[0][1] : 1;
  document.getElementById(elId).innerHTML = top.map(([name, n]) => `
    <div class="bar-row">
      <div class="name" title="${esc(name)}">${esc(name)}</div>
      <div class="bar ${cls}"><span style="width:${(n/max*100).toFixed(1)}%"></span></div>
      <div class="count">${fmt(n)}</div>
    </div>`).join("");
}

renderKPIs();
renderMix("mix-added", "legend-added", D.added_by_module);
renderMix("mix-removed", "legend-removed", D.removed_by_module);
renderBars("tags-added", D.added_tags, "added");
renderBars("tags-removed", D.removed_tags, "removed");
renderBars("tags-changed", D.changed_tags, "changed");

// === Tables (added / removed / changed) ===
function uniqSorted(items, key) {
  const s = new Set(items.map(i => i[key]).filter(Boolean));
  return [...s].sort();
}

function populateFilter(selectId, options, labeler = (x => x)) {
  const sel = document.getElementById(selectId);
  for (const o of options) {
    const opt = document.createElement("option");
    opt.value = o; opt.textContent = labeler(o);
    sel.appendChild(opt);
  }
}

populateFilter("filter-added-tag", uniqSorted(D.added, "tag"));
populateFilter("filter-added-mod", uniqSorted(D.added, "mod"), modLabel);
populateFilter("filter-removed-tag", uniqSorted(D.removed, "tag"));
populateFilter("filter-removed-mod", uniqSorted(D.removed, "mod"), modLabel);
populateFilter("filter-changed-tag", uniqSorted(D.fsn_changed, "tag"));

function makeListPanel({data, tbodyId, metaId, pagerId, searchId, filters, rowFn, searchFields}) {
  const state = { page: 0, filtered: data };
  function applyFilters() {
    const q = (document.getElementById(searchId).value || "").toLowerCase().trim();
    const fvals = filters.map(f => ({ key: f.key, val: document.getElementById(f.id).value }));
    state.filtered = data.filter(item => {
      for (const {key, val} of fvals) if (val && item[key] !== val) return false;
      if (!q) return true;
      return searchFields.some(k => String(item[k] || "").toLowerCase().includes(q));
    });
    state.page = 0; render();
  }
  function render() {
    const total = state.filtered.length;
    const pages = Math.max(1, Math.ceil(total / PAGE));
    if (state.page >= pages) state.page = pages - 1;
    const start = state.page * PAGE;
    const slice = state.filtered.slice(start, start + PAGE);
    const tbody = document.getElementById(tbodyId);
    if (!slice.length) {
      tbody.innerHTML = `<tr><td colspan="4" class="empty">No matches.</td></tr>`;
    } else {
      tbody.innerHTML = slice.map(rowFn).join("");
    }
    document.getElementById(metaId).textContent =
      `${fmt(total)} matches · page ${state.page+1}/${pages} · showing ${fmt(slice.length)}`;
    const pager = document.getElementById(pagerId);
    pager.innerHTML = "";
    function btn(label, page, disabled) {
      const b = document.createElement("button"); b.textContent = label;
      b.disabled = disabled; b.onclick = () => { state.page = page; render(); };
      pager.appendChild(b);
    }
    btn("« First", 0, state.page === 0);
    btn("‹ Prev", state.page - 1, state.page === 0);
    btn(`${state.page+1} / ${pages}`, state.page, true);
    btn("Next ›", state.page + 1, state.page >= pages - 1);
    btn("Last »", pages - 1, state.page >= pages - 1);
  }
  document.getElementById(searchId).addEventListener("input", applyFilters);
  for (const f of filters) document.getElementById(f.id).addEventListener("change", applyFilters);
  applyFilters();
}

makeListPanel({
  data: D.added,
  tbodyId: "tbody-added", metaId: "meta-added", pagerId: "pager-added", searchId: "search-added",
  filters: [{id: "filter-added-tag", key: "tag"}, {id: "filter-added-mod", key: "mod"}],
  searchFields: ["id", "fsn"],
  rowFn: r => `<tr>
    <td><span class="cid">${esc(r.id)}</span></td>
    <td>${esc(r.fsn)}</td>
    <td><span class="tag">${esc(r.tag)}</span></td>
    <td>${modPill(r.mod)}</td></tr>`,
});

makeListPanel({
  data: D.removed,
  tbodyId: "tbody-removed", metaId: "meta-removed", pagerId: "pager-removed", searchId: "search-removed",
  filters: [{id: "filter-removed-tag", key: "tag"}, {id: "filter-removed-mod", key: "mod"}],
  searchFields: ["id", "fsn"],
  rowFn: r => `<tr>
    <td><span class="cid">${esc(r.id)}</span></td>
    <td>${esc(r.fsn)}</td>
    <td><span class="tag">${esc(r.tag)}</span></td>
    <td>${modPill(r.mod)}</td></tr>`,
});

makeListPanel({
  data: D.fsn_changed,
  tbodyId: "tbody-changed", metaId: "meta-changed", pagerId: "pager-changed", searchId: "search-changed",
  filters: [{id: "filter-changed-tag", key: "tag"}],
  searchFields: ["id", "a", "b"],
  rowFn: r => `<tr>
    <td><span class="cid">${esc(r.id)}</span></td>
    <td><div class="diff-old">${esc(r.a)}</div><div class="diff-new">${esc(r.b)}</div></td>
    <td><span class="tag">${esc(r.tag)}</span></td></tr>`,
});

// === Per-analyte ===
function renderAnalytes() {
  const c = document.getElementById("analytes-body");
  if (!D.analytes.length) { c.innerHTML = `<div class="empty">No analyte JSONs found.</div>`; return; }
  c.innerHTML = D.analytes.map(grp => {
    const rows = grp.rows.map(r => {
      const delta = (r.b_total ?? 0) - (r.a_total ?? 0);
      const dCls = delta === 0 ? "zero" : (delta > 0 ? "pos" : "neg");
      const dStr = delta === 0 ? "0" : (delta > 0 ? `+${delta}` : `${delta}`);
      return `<tr class="analyte-row">
        <td>${esc(r.concept)}</td>
        <td>${esc(r.query)}</td>
        <td style="text-align:right">${fmt(r.a_total)}</td>
        <td style="text-align:right">${fmt(r.b_total)}</td>
        <td style="text-align:right" class="analyte-delta ${dCls}">${dStr}</td>
        <td style="text-align:right">${fmt(r.only_a.length)}</td>
        <td style="text-align:right">${fmt(r.only_b.length)}</td>
        <td style="text-align:right">${fmt(r.in_both)}</td>
      </tr>
      <tr><td colspan="8" style="background:#0b0e12">
        <details class="q">
          <summary>ECL & member diff</summary>
          <div class="body">
            <div class="ecl">${esc(r.ecl)}</div>
            ${r.only_a.length ? `<div><b>Only in A (${r.only_a.length})</b><ul>${r.only_a.map(x => `<li>${esc(x)}</li>`).join("")}</ul></div>` : ""}
            ${r.only_b.length ? `<div><b>Only in B (${r.only_b.length})</b><ul>${r.only_b.map(x => `<li>${esc(x)}</li>`).join("")}</ul></div>` : ""}
          </div>
        </details>
      </td></tr>`;
    }).join("");
    return `<div class="panel">
      <h3>${esc(grp.label)}</h3>
      <table>
        <thead><tr>
          <th>Concept</th><th>Query</th>
          <th style="text-align:right">A total</th>
          <th style="text-align:right">B total</th>
          <th style="text-align:right">Δ</th>
          <th style="text-align:right">Only A</th>
          <th style="text-align:right">Only B</th>
          <th style="text-align:right">Both</th>
        </tr></thead>
        <tbody>${rows}</tbody>
      </table>
    </div>`;
  }).join("");
}
renderAnalytes();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
