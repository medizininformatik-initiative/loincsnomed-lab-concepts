#!/usr/bin/env python3
"""
targets.py — read/rotate config/targets.json, the single place where the
LOINC-SNOMED edition under analysis ("current") and the diff baseline
("previous") are pinned.

    import targets
    targets.current()            -> {"name", "api_base", "branch", "effective"}
    targets.previous()
    targets.pair()               -> [previous, current]   (A → B diff order)
    targets.cli_targets()        -> {"local": current, "public": previous, <name>: ...}
    targets.snomed_version_uri() -> "http://snomed.info/sct/11010000107/version/20260321"
    targets.loinc_map_path()     -> Path to the RF2 Identifier extract

    python3 scripts/targets.py   # print the pins
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS_PATH = ROOT / "config" / "targets.json"
LOINC_MODULE = "11010000107"


def load():
    return json.loads(TARGETS_PATH.read_text())


def _entry(cfg, name):
    t = dict(cfg["targets"][name])
    t["name"] = name
    return t


def get(name, cfg=None):
    cfg = cfg or load()
    return _entry(cfg, name)


def current(cfg=None):
    cfg = cfg or load()
    return _entry(cfg, cfg["current"])


def previous(cfg=None):
    cfg = cfg or load()
    return _entry(cfg, cfg["previous"])


def pair(cfg=None):
    cfg = cfg or load()
    return [previous(cfg), current(cfg)]


def cli_targets(cfg=None):
    """Mapping for argparse --target: aliases first, then every named target."""
    cfg = cfg or load()
    m = {"local": current(cfg), "public": previous(cfg)}
    for name in cfg["targets"]:
        m.setdefault(name, _entry(cfg, name))
    return m


def snomed_version_uri(cfg=None):
    cfg = cfg or load()
    return cfg["snomed_version_uri"]


def loinc_map_path(cfg=None):
    cfg = cfg or load()
    return ROOT / cfg["loinc_identifier_file"]


def version_uri_for(effective):
    return "http://snomed.info/sct/{}/version/{}".format(LOINC_MODULE, effective)


def rotate(effective, api_base="http://localhost:8090", code_system="SNOMEDCT-LOINC",
           loinc_file=None, write=True):
    """Make the edition with effectiveTime `effective` (yyyymmdd) the current
    target; the old current becomes previous. Returns the new config."""
    cfg = load()
    iso = "{}-{}-{}".format(effective[:4], effective[4:6], effective[6:8])
    name = "local-{}".format(iso)
    cfg["targets"][name] = {
        "api_base": api_base,
        "branch": "MAIN/{}/{}".format(code_system, iso),
        "effective": effective,
    }
    if cfg["current"] != name:
        cfg["previous"] = cfg["current"]
        cfg["current"] = name
    cfg["snomed_version_uri"] = version_uri_for(effective)
    cfg["loinc_identifier_file"] = loinc_file or "data/loincsnomed_identifiers_{}.txt".format(effective)
    if write:
        TARGETS_PATH.write_text(json.dumps(cfg, indent=2) + "\n")
    return cfg


def main():
    cfg = load()
    print("current : {name}  {branch} @ {api_base}".format(**current(cfg)))
    print("previous: {name}  {branch} @ {api_base}".format(**previous(cfg)))
    print("snomed  : {}".format(snomed_version_uri(cfg)))
    p = loinc_map_path(cfg)
    print("loinc   : {} ({})".format(p.relative_to(ROOT), "present" if p.exists() else "MISSING"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
