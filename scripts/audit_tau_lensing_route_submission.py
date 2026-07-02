#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / "scripts/intake_tau_lensing_route_evidence.py"
FIREWALL = ROOT / "scripts/check_tau_lensing_route_evidence_firewall.py"
DEFAULT_AUDIT = ROOT / "data/derived/cmb_tau_lensing_route_submission_audit_v01.json"


def run_json(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout)


def selected_route_kind(selected_routes: list[str]) -> str | None:
    if len(selected_routes) != 1:
        return None
    route = selected_routes[0]
    if route in {"direct_tau_PP_grid", "delta_PP_tau_against_named_fiducial_PP"}:
        return "numeric_route"
    if route == "explicit_failure_no_endpoint_blind_grid":
        return "failure_route"
    return "unknown_route"


def build_audit() -> dict[str, Any]:
    intake = run_json([sys.executable, str(INTAKE), "--write-report"])
    firewall = run_json([sys.executable, str(FIREWALL), "--write-report"])

    selected_routes = intake.get("selected_routes", [])
    route_kind = selected_route_kind(selected_routes)
    exactly_one_route = intake.get("selected_route_count") == 1
    firewall_passed = firewall.get("firewall_passed") is True
    numeric_route_ready_for_materializer = exactly_one_route and route_kind == "numeric_route" and firewall_passed
    failure_route_recorded = exactly_one_route and route_kind == "failure_route" and firewall_passed

    if numeric_route_ready_for_materializer:
        audit_decision = "NUMERIC_ROUTE_READY_FOR_MATERIALIZE_REPLAY"
        readiness_decision = "BLOCKED_ON_PROJECTION_REPLAY"
        blocking_layer = "projection_replay"
        next_required_action = "run_make_materialize_replay"
    elif failure_route_recorded:
        audit_decision = "FAILURE_ROUTE_RECORDED_SCORE_REMAINS_BLOCKED"
        readiness_decision = "BLOCKED_ON_TAU_ROUTE_EVIDENCE"
        blocking_layer = "tau_route_evidence"
        next_required_action = "preserve_failure_statement_no_score_run"
    elif not exactly_one_route:
        audit_decision = "BLOCKED_SUBMIT_EXACTLY_ONE_ROUTE"
        readiness_decision = "BLOCKED_ON_TAU_ROUTE_EVIDENCE"
        blocking_layer = "tau_route_evidence"
        next_required_action = intake.get("next_required_action")
    elif not firewall_passed:
        audit_decision = "BLOCKED_REPAIR_ROUTE_EVIDENCE_FIREWALL"
        readiness_decision = "BLOCKED_ON_ROUTE_EVIDENCE_FIREWALL"
        blocking_layer = "route_evidence_firewall"
        next_required_action = firewall.get("next_required_action")
    else:
        audit_decision = "BLOCKED_UNSUPPORTED_ROUTE_STATE"
        readiness_decision = "BLOCKED_ON_PREFLIGHT"
        blocking_layer = "route_submission_audit"
        next_required_action = "inspect_route_submission_audit"

    return {
        "report_id": "tau_lensing_route_submission_audit_v01",
        "claim_boundary": "route_submission_audit_only_no_grid_validation_no_score_no_dark_sector_verdict",
        "audit_decision": audit_decision,
        "selected_route_count": intake.get("selected_route_count"),
        "selected_routes": selected_routes,
        "selected_route_kind": route_kind,
        "firewall_passed": firewall_passed,
        "readiness_decision": readiness_decision,
        "blocking_layer": blocking_layer,
        "numeric_route_ready_for_materializer": numeric_route_ready_for_materializer,
        "failure_route_recorded": failure_route_recorded,
        "intake_next_required_action": intake.get("next_required_action"),
        "firewall_next_required_action": firewall.get("next_required_action"),
        "next_required_action": next_required_action,
        "score_run": False,
        "dark_sector_verdict": False,
        "source_reports": {
            "intake": intake.get("report_id"),
            "firewall": firewall.get("report_id"),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit the current Tau lensing route submission before replay.")
    parser.add_argument(
        "--write-audit",
        default=None,
        nargs="?",
        const=str(DEFAULT_AUDIT),
        help=f"Optional JSON audit path. Defaults to {DEFAULT_AUDIT} when passed without a path.",
    )
    args = parser.parse_args()

    audit = build_audit()
    text = json.dumps(audit, indent=2, sort_keys=True)
    if args.write_audit:
        path = Path(args.write_audit)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
