#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "data/derived/cmb_tau_lensing_physical_projection_operator_packet_v01.csv"
DEFAULT_AUDIT = ROOT / "data/derived/cmb_tau_lensing_physical_projection_operator_packet_audit_v01.json"
REQUIRED_COMPONENTS = {
    "projection_domain",
    "projection_codomain",
    "projection_operator_rule",
    "projection_normalization",
    "projection_replay",
    "endpoint_firewall",
}


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def build_audit(path: Path) -> dict[str, Any]:
    checks: list[dict[str, Any]] = [{"name": "packet_exists", "passes": path.exists(), "detail": rel(path)}]
    if not path.exists():
        return finalize(checks, explicit_failure=False)
    rows = read_rows(path)
    components = {row.get("component_id", "") for row in rows}
    missing = sorted(REQUIRED_COMPONENTS - components)
    checks.append({"name": "required_components_present", "passes": not missing, "detail": missing})
    empty_values = [row.get("component_id") for row in rows if not str(row.get("accepted_value", "")).strip()]
    checks.append(
        {
            "name": "accepted_values_populated",
            "passes": not empty_values,
            "detail": empty_values,
        }
    )
    blocked_rows = [
        row.get("component_id")
        for row in rows
        if "BLOCKED" in str(row.get("current_status", "")).upper()
    ]
    checks.append({"name": "no_blocked_rows", "passes": not blocked_rows, "detail": blocked_rows})
    firewall_row = next((row for row in rows if row.get("component_id") == "endpoint_firewall"), {})
    firewall_passed = "PASS" in str(firewall_row.get("current_status", "")).upper()
    checks.append({"name": "endpoint_firewall_passed", "passes": firewall_passed, "detail": firewall_row})
    operator_row = next((row for row in rows if row.get("component_id") == "projection_operator_rule"), {})
    explicit_failure = "FAILURE" in str(operator_row.get("current_status", "")).upper()
    checks.append(
        {
            "name": "explicit_operator_failure_declared",
            "passes": explicit_failure,
            "detail": operator_row,
        }
    )
    return finalize(checks, explicit_failure=explicit_failure)


def finalize(checks: list[dict[str, Any]], explicit_failure: bool) -> dict[str, Any]:
    acceptance_checks = [check for check in checks if check.get("name") != "explicit_operator_failure_declared"]
    accepted = all(check.get("passes") is True for check in acceptance_checks) and not explicit_failure
    if accepted:
        decision = "ACCEPT_PHYSICAL_PROJECTION_OPERATOR"
        next_required_action = "update_parent_projection_packet_with_accepted_N_projection"
    elif explicit_failure:
        decision = "DO_NOT_SCORE_EXPLICIT_OPERATOR_FAILURE"
        next_required_action = "resume_only_with_endpoint_blind_projection_operator_normalization_replay_and_firewall"
    else:
        decision = "BLOCK_PHYSICAL_N_PROJECTION_PENDING_OPERATOR_NORMALIZATION_REPLAY_AND_FIREWALL"
        next_required_action = "supply_endpoint_blind_projection_operator_packet_values"
    return {
        "report_id": "cmb_tau_lensing_physical_projection_operator_packet_audit_v01",
        "claim_boundary": "physical_projection_operator_packet_audit_only_no_score_no_dark_sector_verdict",
        "projection_operator_packet_accepted": accepted,
        "N_projection_physical_accepted": accepted,
        "checks": checks,
        "explicit_operator_failure_declared": explicit_failure,
        "decision": decision,
        "next_required_action": next_required_action,
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit physical Tau lensing projection operator packet.")
    parser.add_argument("--packet", default=str(DEFAULT_PACKET))
    parser.add_argument("--write-audit", nargs="?", const=str(DEFAULT_AUDIT))
    args = parser.parse_args()
    audit = build_audit(Path(args.packet).resolve())
    text = json.dumps(audit, indent=2, sort_keys=True)
    if args.write_audit:
        path = Path(args.write_audit)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
