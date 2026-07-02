#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHYSICAL_PRECHECK = ROOT / "scripts/precheck_tau_lensing_physical_candidate_upstream_table.py"
DERIVATION_INTAKE = ROOT / "scripts/audit_tau_lensing_physical_derivation_intake.py"
ROUTE_B_PARENT_PRECHECK = ROOT / "scripts/precheck_tau_lensing_route_b_parent_source_table.py"
ROUTE_B_FORMULA_AUDIT = ROOT / "scripts/audit_tau_lensing_route_b_parent_source_formula_spec.py"
PHYSICAL_PACKAGE = ROOT / "scripts/build_tau_lensing_physical_candidate_delta_route_package.py"
SCORING_STATUS = ROOT / "scripts/build_tau_lensing_scoring_status_summary.py"
DEFAULT_STATUS = ROOT / "data/derived/cmb_tau_lensing_grid_production_status_v01.json"
UPSTREAM_METADATA = ROOT / "payload_staging/tau_lensing_upstream_l_response_metadata_v01.json"
ACTIVE_PROVENANCE = ROOT / "payloads/tau_lensing_response_grid_provenance_v01.json"
STAGING_PROVENANCE = ROOT / "payload_staging/delta_PP_tau_against_named_fiducial_PP/tau_lensing_response_grid_provenance_v01.json"


def run_json(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout)


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def classify_text(text: str) -> str:
    lowered = text.lower()
    if "template_not_payload" in lowered or "fill:" in lowered:
        return "template"
    if "control" in lowered or "identically zero" in lowered or "null-control" in lowered:
        return "control"
    if "probe" in lowered or "diagnostic" in lowered or "not a physical tau response" in lowered:
        return "diagnostic_probe"
    if "physical_candidate" in lowered or "tau-derived" in lowered or "tau-side" in lowered:
        return "physical_candidate"
    return "unknown"


def classify_metadata(path: Path) -> dict[str, Any]:
    data = load_json(path)
    if data is None:
        return {"path": str(path.relative_to(ROOT)), "exists": path.exists(), "classification": "missing_or_invalid"}
    text = json.dumps(data, sort_keys=True)
    return {
        "path": str(path.relative_to(ROOT)),
        "exists": True,
        "classification": classify_text(text),
        "selected_route": data.get("selected_route"),
        "formula_role": data.get("formula_role"),
        "claim_boundary": data.get("claim_boundary"),
    }


def failed_checks(precheck: dict[str, Any]) -> list[dict[str, Any]]:
    failures = []
    for check in precheck.get("checks", []):
        if check.get("passes") is not True:
            failures.append(
                {
                    "name": check.get("name"),
                    "detail": check.get("detail"),
                }
            )
    return failures


def build_status() -> dict[str, Any]:
    physical_precheck = run_json([sys.executable, str(PHYSICAL_PRECHECK), "--write-report"])
    derivation_intake = run_json([sys.executable, str(DERIVATION_INTAKE), "--write-audit"])
    route_b_formula_audit = run_json([sys.executable, str(ROUTE_B_FORMULA_AUDIT), "--write-report"])
    route_b_parent_precheck = run_json([sys.executable, str(ROUTE_B_PARENT_PRECHECK), "--write-report"])
    physical_package = run_json([sys.executable, str(PHYSICAL_PACKAGE), "--write-report"])
    scoring_status = run_json([sys.executable, str(SCORING_STATUS), "--write-status"])

    upstream = classify_metadata(UPSTREAM_METADATA)
    active = classify_metadata(ACTIVE_PROVENANCE)
    staging = classify_metadata(STAGING_PROVENANCE)

    physical_ready = (
        physical_precheck.get("precheck_passed") is True
        and physical_package.get("package_status") == "PHYSICAL_CANDIDATE_DELTA_ROUTE_STAGING_PACKAGE_WRITTEN"
    )
    if physical_ready:
        production_status = "PHYSICAL_CANDIDATE_STAGING_READY"
        next_required_action = "run_make_staging-promote-delta-dry-run"
    elif route_b_formula_audit.get("audit_passed") is not True:
        production_status = "BLOCKED_NO_AUDITED_ROUTE_B_PARENT_SOURCE_FORMULA_SPEC"
        next_required_action = "produce_audited_endpoint_blind_tau_derived_parent_source_formula_spec"
    elif route_b_parent_precheck.get("precheck_passed") is not True:
        production_status = "BLOCKED_NO_ROUTE_B_PARENT_SOURCE"
        next_required_action = "produce_endpoint_blind_tau_derived_parent_tau_source_l_table"
    else:
        production_status = "BLOCKED_NO_PHYSICAL_TAU_GRID"
        next_required_action = "produce_tau_derived_endpoint_blind_3000_row_l_response_table"

    return {
        "report_id": "cmb_tau_lensing_grid_production_status_v01",
        "claim_boundary": "tau_grid_production_status_only_no_new_grid_no_score_no_dark_sector_verdict",
        "production_status": production_status,
        "plain_language_status": (
            "Active scoring payload is control and staging input is diagnostic/probe-like; "
            "no physical Tau-grid candidate is available yet."
            if not physical_ready
            else "A physical-candidate Tau-grid staging package is ready for dry-run promotion."
        ),
        "active_payload_classification": active,
        "staging_route_classification": staging,
        "upstream_input_classification": upstream,
        "physical_candidate_precheck_passed": physical_precheck.get("precheck_passed") is True,
        "physical_candidate_precheck_failures": failed_checks(physical_precheck),
        "physical_derivation_intake_audit_passed": derivation_intake.get("audit_passed") is True,
        "physical_derivation_intake_route_family": derivation_intake.get("selected_route_family"),
        "physical_derivation_intake_failures": failed_checks(derivation_intake),
        "route_b_parent_source_formula_spec_audit_passed": route_b_formula_audit.get("audit_passed") is True,
        "route_b_parent_source_formula_spec_audit_failures": failed_checks(route_b_formula_audit),
        "route_b_parent_source_precheck_passed": route_b_parent_precheck.get("precheck_passed") is True,
        "route_b_parent_source_precheck_failures": failed_checks(route_b_parent_precheck),
        "physical_candidate_package_status": physical_package.get("package_status"),
        "scoring_status": scoring_status.get("scoring_status"),
        "scoring_route_classification": scoring_status.get("route_classification"),
        "control_score_output_accepted": scoring_status.get("control_score_output_accepted") is True,
        "diagnostic_probe_score_output_accepted": scoring_status.get("diagnostic_probe_score_output_accepted") is True,
        "physical_tau_score_output_accepted": scoring_status.get("physical_tau_score_output_accepted") is True,
        "required_next_files": [
            "payload_staging/tau_lensing_route_b_parent_source_formula_spec_v01.json",
            "payload_staging/tau_lensing_route_b_parent_source_v01.csv",
            "payload_staging/tau_lensing_route_b_parent_source_config_v01.json",
            "payload_staging/tau_lensing_upstream_l_response_v01.csv",
            "payload_staging/tau_lensing_upstream_l_response_metadata_v01.json",
        ],
        "required_acceptance_commands": [
            "make tau-grid-route-b-parent-formula-audit",
            "make tau-grid-route-b-parent-from-formula-dry-run",
            "make tau-grid-route-b-parent-from-formula-write-staging",
            "make tau-grid-route-b-parent-table-precheck",
            "make tau-grid-route-b-parent-dry-run",
            "make tau-grid-route-b-parent-write-staging",
            "make tau-grid-derivation-intake-audit",
            "make tau-grid-physical-candidate-precheck",
            "make tau-grid-handoff-write-staging",
            "make tau-grid-physical-candidate-package",
            "make staging-promote-delta-dry-run",
        ],
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": next_required_action,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau lensing grid production status.")
    parser.add_argument("--write-status", nargs="?", const=str(DEFAULT_STATUS))
    args = parser.parse_args()

    status = build_status()
    text = json.dumps(status, indent=2, sort_keys=True)
    if args.write_status:
        path = Path(args.write_status)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
