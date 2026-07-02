#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MATERIALIZER = ROOT / "scripts/materialize_tau_lensing_route_b_from_parent_source.py"
PARENT_PRECHECK = ROOT / "scripts/precheck_tau_lensing_route_b_parent_source_table.py"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_route_b_parent_source_materializer_smoke_v01.json"


def write_parent_table(path: Path) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["L", "parent_tau_source_value"])
        for ell in range(10, 3010):
            value = (ell / 1000.0) * math.exp(-((ell / 2400.0) ** 2))
            writer.writerow([ell, format(value, ".17e")])


def write_config(path: Path, parent_table: Path) -> None:
    payload = {
        "config_id": "tau_lensing_route_b_parent_source_config_smoke_fixture_v01",
        "selected_route": "delta_PP_tau_against_named_fiducial_PP",
        "response_rule": "linear_parent_source_v01",
        "parent_source_table": str(parent_table.resolve()),
        "parent_l_column": "L",
        "parent_value_column": "parent_tau_source_value",
        "normalization": 1.0e-9,
        "endpoint_blind_statement": "Endpoint-blind parent_tau_source fixture fixed before any score readout.",
        "parameter_policy": "No endpoint or score tuning is allowed; smoke fixture constants are predeclared.",
        "source_chain": [
            "docs/example_tau_parent_source_contract_v01.md",
            "scripts/smoke_tau_lensing_route_b_parent_source_materializer.py",
        ],
        "normalization_statement": "dimensionless delta_PP_tau = normalization * parent_tau_source_value",
        "known_limit_statement": "delta_PP_tau tends to zero when parent_tau_source_value tends to zero",
        "claim_boundary": "route_b_parent_source_materializer_smoke_fixture_no_score_no_dark_sector_verdict",
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def run_materializer(config: Path) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(MATERIALIZER), str(config)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def run_parent_precheck(parent: Path) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(PARENT_PRECHECK),
            "--table",
            str(parent),
            "--l-column",
            "L",
            "--value-column",
            "parent_tau_source_value",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def template_rejected() -> bool:
    completed = subprocess.run(
        [
            sys.executable,
            str(MATERIALIZER),
            "payload_templates/tau_lensing_route_b_parent_source_CONFIG_TEMPLATE_v01.json",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return completed.returncode != 0 and "forbidden/template markers" in completed.stderr


def build_report() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="tau_route_b_parent_source_smoke_") as tmp:
        tmpdir = Path(tmp)
        parent = tmpdir / "parent_source.csv"
        config = tmpdir / "route_b_config.json"
        write_parent_table(parent)
        write_config(config, parent)
        parent_precheck = run_parent_precheck(parent)
        dry_run = run_materializer(config)
        checks = [
            {
                "name": "template_config_rejected",
                "passes": template_rejected(),
            },
            {
                "name": "fixture_parent_precheck_passed",
                "passes": parent_precheck.get("precheck_passed") is True,
            },
            {
                "name": "fixture_dry_run_passed",
                "passes": dry_run.get("materialization_status") == "DRY_RUN_PASSED",
            },
            {
                "name": "fixture_rows_3000",
                "passes": dry_run.get("rows") == 3000,
            },
            {
                "name": "fixture_nonzero",
                "passes": float(dry_run.get("max_abs_value", 0.0)) > 0.0,
            },
        ]
    smoke_passed = all(check["passes"] for check in checks)
    return {
        "report_id": "cmb_tau_lensing_route_b_parent_source_materializer_smoke_v01",
        "claim_boundary": "route_b_parent_source_materializer_smoke_only_no_staging_no_score_no_dark_sector_verdict",
        "smoke_passed": smoke_passed,
        "checks": checks,
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": (
            "keep_route_b_parent_source_materializer_in_regression_suite"
            if smoke_passed
            else "fix_route_b_parent_source_materializer"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Smoke-test Route B parent-source materializer.")
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    args = parser.parse_args()

    report = build_report()
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.write_report:
        report_path = Path(args.write_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(text + "\n")
    print(text)
    if not report["smoke_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
