#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GRID = ROOT / "payloads/tau_lensing_response_pp_grid_v01.csv"
DECLARATION = ROOT / "payloads/tau_lensing_response_grid_route_declaration_v01.md"
PROVENANCE = ROOT / "payloads/tau_lensing_response_grid_provenance_v01.json"
TEMP_FILES = [GRID, DECLARATION, PROVENANCE]


def run_json(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout)


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def write_bad_direct_route() -> None:
    preexisting = [str(path.relative_to(ROOT)) for path in TEMP_FILES if path.exists()]
    if preexisting:
        raise RuntimeError(f"refusing to overwrite existing route payloads: {preexisting}")

    GRID.write_text("10,0.0\n11,0.0\n")
    DECLARATION.write_text(
        "\n".join(
            [
                "selected_route: direct_tau_PP_grid",
                "numeric_grid_file: payloads/tau_lensing_response_pp_grid_v01.csv",
                "fiducial_reference_file: not_used",
                "provenance_file: payloads/tau_lensing_response_grid_provenance_v01.json",
                "index_alignment: L = 10 + i",
                "",
            ]
        )
    )
    PROVENANCE.write_text(
        json.dumps(
            {
                "selected_route": "direct_tau_PP_grid",
                "numeric_grid_file": "payloads/tau_lensing_response_pp_grid_v01.csv",
                "numeric_grid_sha256": "wronghash",
                "source_chain": "temporary_firewall_blocker_smoke_only",
                "derivation_script_or_formula": "temporary_firewall_blocker_smoke_only",
                "no_endpoint_fit_statement": "temporary_firewall_blocker_smoke_only",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def cleanup_bad_direct_route() -> None:
    for path in TEMP_FILES:
        if path.exists():
            path.unlink()


def main() -> None:
    try:
        write_bad_direct_route()
        intake = run_json([sys.executable, "scripts/intake_tau_lensing_route_evidence.py"])
        firewall = run_json([sys.executable, "scripts/check_tau_lensing_route_evidence_firewall.py"])
        readiness = run_json([sys.executable, "scripts/decide_tau_lensing_score_readiness.py"])
        submission_audit = run_json([sys.executable, "scripts/audit_tau_lensing_route_submission.py"])
    finally:
        cleanup_bad_direct_route()

    check(intake["selected_route_count"] == 1, "bad direct route must be visible to intake")
    check(intake["selected_routes"] == ["direct_tau_PP_grid"], "bad direct route must select direct route")
    check(firewall["firewall_passed"] is False, "bad hash must fail firewall")
    check(
        "numeric_grid_sha256" in firewall["checks"][1]["mismatched_file_hashes"],
        "firewall must identify numeric_grid_sha256 mismatch",
    )
    check(
        readiness["readiness_decision"] == "BLOCKED_ON_ROUTE_EVIDENCE_FIREWALL",
        "readiness must split firewall blocker from missing-route blocker",
    )
    check(
        submission_audit["audit_decision"] == "BLOCKED_REPAIR_ROUTE_EVIDENCE_FIREWALL",
        "submission audit must split firewall repair from missing-route blocker",
    )
    check(
        submission_audit["numeric_route_ready_for_materializer"] is False,
        "bad route must not be ready for materializer",
    )
    check(readiness["score_run"] is False, "readiness smoke must not run score")
    check(readiness["dark_sector_verdict"] is False, "readiness smoke must not issue verdict")

    report = {
        "report_id": "tau_lensing_firewall_blocker_path_smoke_v01",
        "claim_boundary": "firewall_blocker_path_smoke_only_no_score_run_no_dark_sector_verdict",
        "synthetic_bad_route": "direct_tau_PP_grid_with_wrong_numeric_grid_sha256",
        "intake_selected_route_count": intake["selected_route_count"],
        "firewall_passed": firewall["firewall_passed"],
        "readiness_decision": readiness["readiness_decision"],
        "submission_audit_decision": submission_audit["audit_decision"],
        "numeric_route_ready_for_materializer": submission_audit["numeric_route_ready_for_materializer"],
        "blocking_layer": readiness["blocking_layer"],
        "score_run": False,
        "dark_sector_verdict": False,
        "smoke_passed": True,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
