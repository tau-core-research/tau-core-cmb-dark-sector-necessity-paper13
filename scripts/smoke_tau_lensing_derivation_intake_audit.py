#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "scripts/audit_tau_lensing_physical_derivation_intake.py"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_derivation_intake_audit_smoke_v01.json"


def run_audit(metadata: Path) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(AUDIT), "--metadata", str(metadata)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def route_b_metadata() -> dict[str, Any]:
    return {
        "selected_route": "delta_PP_tau_against_named_fiducial_PP",
        "formula_role": "endpoint_blind_tau_derived_lensing_l_response_physical_candidate",
        "endpoint_blind_statement": (
            "Endpoint-blind parent_tau_source response values are fixed before any score readout."
        ),
        "parameter_policy": (
            "No endpoint or score tuning is allowed; parameters are fixed from Tau-side parent evidence."
        ),
        "source_chain": [
            "docs/example_tau_parent_source_contract_v01.md",
            "scripts/example_tau_parent_source_to_f_tau_l.py",
        ],
        "normalization_statement": "dimensionless delta_PP_tau normalization fixed by parent_tau_source convention",
        "known_limit_statement": "delta_PP_tau tends to zero when parent_tau_source is absent",
        "derivation_script_or_formula": (
            "delta_PP_tau(L) = F_tau_L(parent_tau_source, readout_profile, scale_profile; L)"
        ),
        "claim_boundary": "test_fixture_only_no_grid_no_score_no_dark_sector_verdict",
    }


def ambiguous_metadata() -> dict[str, Any]:
    payload = route_b_metadata()
    payload["derivation_script_or_formula"] = (
        "rho_tau_eff -> Phi_tau_eff -> T_tau_CMB -> Projection_PP and "
        "delta_PP_tau(L) = F_tau_L(parent_tau_source, readout_profile, scale_profile; L)"
    )
    payload["normalization_statement"] = (
        "projection_PP normalization and dimensionless delta_PP_tau normalization are both declared"
    )
    return payload


def probe_metadata() -> dict[str, Any]:
    payload = route_b_metadata()
    payload["formula_role"] = "endpoint_blind_nonzero_tau_lensing_response_probe"
    payload["endpoint_blind_statement"] = "Diagnostic probe fixed before score readout."
    payload["derivation_script_or_formula"] = "diagnostic probe delta_PP_tau(L), not a physical Tau response"
    payload["claim_boundary"] = "nonzero_probe_response_only_no_tau_score_no_dark_sector_verdict"
    return payload


def build_report() -> dict[str, Any]:
    cases = []
    with tempfile.TemporaryDirectory(prefix="tau_derivation_intake_smoke_") as tmp:
        tmpdir = Path(tmp)
        specs = [
            ("probe_must_fail", probe_metadata(), False, "route_B_direct_L_space"),
            ("route_b_fixture_must_pass", route_b_metadata(), True, "route_B_direct_L_space"),
            ("ambiguous_route_must_fail", ambiguous_metadata(), False, "ambiguous_or_incomplete"),
        ]
        for name, metadata, expected_pass, expected_route in specs:
            path = tmpdir / f"{name}.json"
            write_json(path, metadata)
            audit = run_audit(path)
            passed = audit.get("audit_passed") is expected_pass and audit.get("selected_route_family") == expected_route
            cases.append(
                {
                    "case": name,
                    "expected_pass": expected_pass,
                    "actual_pass": audit.get("audit_passed"),
                    "expected_route_family": expected_route,
                    "actual_route_family": audit.get("selected_route_family"),
                    "case_passed": passed,
                }
            )
    smoke_passed = all(case["case_passed"] for case in cases)
    return {
        "report_id": "cmb_tau_lensing_derivation_intake_audit_smoke_v01",
        "claim_boundary": "derivation_intake_audit_smoke_only_no_grid_no_score_no_dark_sector_verdict",
        "smoke_passed": smoke_passed,
        "cases": cases,
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": (
            "keep_derivation_intake_audit_in_regression_suite"
            if smoke_passed
            else "fix_derivation_intake_audit_route_classification"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Smoke-test the Tau lensing physical derivation intake audit.")
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    args = parser.parse_args()

    report = build_report()
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)
    if not report["smoke_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
