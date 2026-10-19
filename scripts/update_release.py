#!/usr/bin/env python3
"""
update_release.py — move this repo to a new LOINC-SNOMED release.

    python3 scripts/update_release.py --zip ~/Downloads/SnomedCT_LOINCExtension_PRODUCTION_LO1010000_20261021T120000Z.zip
        [--int-zip <SnomedCT_InternationalRF2_PRODUCTION_*.zip>]   # if the release needs an INT version not loaded
        [--helper ~/code/helper/local-snowstorm] [--api-base http://localhost:8090]
        [--skip-snowstorm]   # Snowstorm already has the new version branch
        [--skip-runs]        # only rotate pins + identifier file, do not regenerate outputs
        [--dry-run]

Steps
  1. inspect the archive (effectiveTime, identifier file)
  2. local-snowstorm helper: update-extension.sh --zip ...  (in place, keeps old version branch)
  3. verify MAIN/SNOMEDCT-LOINC/<yyyy-mm-dd> exists on --api-base
  4. extract sct2_Identifier_Snapshot → data/loincsnomed_identifiers_<eff>.txt (gitignored, licensed)
  5. rotate config/targets.json: previous ← current, current ← new; snomed version URI; identifier file
  6. regenerate: compare_versions (all + psa + ldh), full_branch_diff, review_export,
     build_observation_artifacts, build_dashboard
"""

import argparse
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import targets as _targets  # noqa: E402

DEFAULT_HELPER = Path.home() / "code" / "helper" / "local-snowstorm"
CODE_SYSTEM = "SNOMEDCT-LOINC"

RUNS = [
    ["python3", "scripts/compare_versions.py"],
    ["python3", "scripts/compare_versions.py", "--config-glob", "config/psa_custom_ecl.json",
     "--out", "output/psa_version_comparison.md", "--json-out", "output/psa_version_comparison.json"],
    ["python3", "scripts/compare_versions.py", "--config-glob", "config/ldh_custom_ecl.json",
     "--out", "output/ldh_version_comparison.md", "--json-out", "output/ldh_version_comparison.json"],
    ["python3", "scripts/full_branch_diff.py"],
    ["python3", "scripts/review_export.py"],
    ["python3", "scripts/build_observation_artifacts.py"],
    ["python3", "scripts/build_aggregation_valuesets.py"],
    ["python3", "scripts/build_dashboard.py"],
]


def banner(msg):
    print("\n" + "=" * 70 + "\n  " + msg + "\n" + "=" * 70, flush=True)


def effective_from_name(path):
    m = re.search(r"_(\d{8})T\d{6}Z", Path(path).name)
    if not m:
        sys.exit("Cannot read effectiveTime from archive name: {}".format(path))
    return m.group(1)


def snowstorm_versions(api_base):
    import requests
    r = requests.get("{}/codesystems/{}/versions".format(api_base.rstrip("/"), CODE_SYSTEM), timeout=30)
    r.raise_for_status()
    return sorted(str(v.get("effectiveDate")) for v in r.json().get("items", []))


def run_helper(helper, zip_path, int_zip, dry_run):
    script = Path(helper) / "update-extension.sh"
    if not script.exists():
        sys.exit("Helper script not found: {}".format(script))
    cmd = [str(script), "--zip", str(zip_path)]
    if int_zip:
        cmd += ["--int-zip", str(int_zip)]
    if dry_run:
        cmd.append("--dry-run")
    print("  $ " + " ".join(cmd), flush=True)
    rc = subprocess.call(cmd, cwd=str(helper))
    if rc != 0:
        sys.exit("update-extension.sh failed (exit {})".format(rc))


def extract_identifiers(zip_path, effective):
    out = ROOT / "data" / "loincsnomed_identifiers_{}.txt".format(effective)
    with zipfile.ZipFile(zip_path) as z:
        names = [n for n in z.namelist() if re.search(r"Snapshot/Terminology/sct2_Identifier_Snapshot_", n)]
        if not names:
            sys.exit("No sct2_Identifier_Snapshot file in archive")
        out.parent.mkdir(exist_ok=True)
        out.write_bytes(z.read(names[0]))
    n = sum(1 for _ in open(out)) - 1
    print("  {} ({} rows)".format(out.relative_to(ROOT), n))
    return out


def run_steps(skip_runs):
    if skip_runs:
        print("  (skipped)")
        return
    for cmd in RUNS:
        banner(" ".join(cmd[1:]))
        rc = subprocess.call(cmd, cwd=str(ROOT))
        if rc != 0:
            sys.exit("step failed (exit {}): {}".format(rc, " ".join(cmd)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--zip", required=True, help="SnomedCT_LOINCExtension_PRODUCTION_*.zip")
    ap.add_argument("--int-zip", help="International archive if the release needs an INT version not loaded")
    ap.add_argument("--helper", default=str(DEFAULT_HELPER), help="local-snowstorm helper directory")
    ap.add_argument("--api-base", default=None, help="Snowstorm API base (default: current target's)")
    ap.add_argument("--skip-snowstorm", action="store_true")
    ap.add_argument("--skip-runs", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    zip_path = Path(args.zip).expanduser().resolve()
    if not zip_path.exists():
        sys.exit("Archive not found: {}".format(zip_path))
    effective = effective_from_name(zip_path)
    iso = "{}-{}-{}".format(effective[:4], effective[4:6], effective[6:8])
    cur = _targets.current()
    api_base = args.api_base or cur["api_base"]

    banner("1. Release {}  (current pin: {})".format(effective, cur["name"]))
    print("  archive : {}\n  branch  : MAIN/{}/{}\n  api     : {}".format(zip_path.name, CODE_SYSTEM, iso, api_base))
    if cur["effective"] == effective and not args.dry_run:
        print("  NOTE: this release is already the current target; pins stay, outputs will be regenerated.")

    banner("2. Local Snowstorm (helper: {})".format(args.helper))
    if args.skip_snowstorm:
        print("  (skipped)")
    else:
        run_helper(args.helper, zip_path, args.int_zip, args.dry_run)

    banner("3. Verify version branch")
    try:
        versions = snowstorm_versions(api_base)
        print("  {} versions on {}: {}".format(CODE_SYSTEM, api_base, ", ".join(versions)))
        if effective not in versions and not args.dry_run:
            sys.exit("Version {} not found on Snowstorm — import failed?".format(effective))
    except Exception as e:  # noqa: BLE001
        if args.dry_run:
            print("  (Snowstorm not reachable: {})".format(e))
        else:
            sys.exit("Cannot verify Snowstorm: {}".format(e))

    banner("4. LOINC identifier extract")
    if args.dry_run:
        print("  would write data/loincsnomed_identifiers_{}.txt".format(effective))
    else:
        extract_identifiers(zip_path, effective)

    banner("5. Rotate config/targets.json")
    new_cfg = _targets.rotate(effective, api_base=api_base, write=not args.dry_run)
    print("  previous: {}\n  current : {}\n  snomed  : {}".format(
        new_cfg["previous"], new_cfg["current"], new_cfg["snomed_version_uri"]))
    if args.dry_run:
        print("  (dry-run: not written)")

    banner("6. Regenerate outputs")
    if args.dry_run:
        for cmd in RUNS:
            print("  would run: " + " ".join(cmd[1:]))
        return 0
    run_steps(args.skip_runs)

    banner("Done — where to look")
    print("  output/version_comparison.md        per-query added/removed vs {}".format(new_cfg["previous"]))
    print("  output/full_diff/concepts.md        whole-branch concept diff by module")
    print("  output/review/{}/                   per-analyte review XLSX/CSV".format(new_cfg["current"]))
    print("  output/fhir/SUMMARY.md              18 ValueSets + profiles, concept counts")
    print("  output/fhir/aggregation/SUMMARY.md  comprehensive per-analyte ValueSets (one per use-case bucket)")
    print("  output/dashboard/index.html         dashboard")
    return 0


if __name__ == "__main__":
    sys.exit(main())
