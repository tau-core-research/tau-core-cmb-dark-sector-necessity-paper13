#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GRID = ROOT / "payloads/tau_lensing_response_pp_grid_v01.csv"
DECLARATION = ROOT / "payloads/tau_lensing_response_grid_route_declaration_v01.md"
PROVENANCE = ROOT / "payloads/tau_lensing_response_grid_provenance_v01.json"
REPLAY = ROOT / "payloads/tau_lensing_pp_grid_projection_replay_v01.json"
TEMP_FILES = [GRID, DECLARATION, PROVENANCE, REPLAY]


def run_json(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout)


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_good_direct_route() -> None:
    preexisting = [str(path.relative_to(ROOT)) for path in TEMP_FILES if path.exists()]
    if preexisting:
        raise RuntimeError(f"refusing to overwrite existing route/replay payloads: {preexisting}")

    with GRID.open("w") as handle:
        for ell in range(10, 3010):
            handle.write(f"{ell},0.0\n")

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
                "numeric_grid_sha256": sha256_file(GRID),
                "source_chain": "synthetic_good_route_submission_smoke_only",
                "derivation_script_or_formula": "synthetic_good_route_submission_smoke_only",
                "no_endpoint_fit_statement": "synthetic_good_route_submission_smoke_only",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def cleanup_good_direct_route() -> None:
    for path in TEMP_FILES:
        if path.exists():
            path.unlink()


def main() -> None:
    try:
        write_good_direct_route()
        intake = run_json([sys.executable, "scripts/intake_tau_lensing_route_evidence.py"])
        firewall = run_json([sys.executable, "scripts/check_tau_lensing_route_evidence_firewall.py"])
        submission_audit = run_json([sys.executable, "scripts/audit_tau_lensing_route_submission.py"])
        materializer = run_json([sys.executable, "scripts/materialize_tau_lensing_projection_replay.py"])
        preflight = run_json([sys.executable, "scripts/preflight_tau_lensing_reduced_score.py"])
        pipeline_dry_run = run_json(
            [sys.executable, "scripts/run_tau_lensing_scoring_pipeline.py", "--dry-run"]
        )
        readiness = run_json([sys.executable, "scripts/decide_tau_lensing_score_readiness.py"])
    finally:
        cleanup_good_direct_route()

    check(intake["selected_route_count"] == 1, "good direct route must be visible to intake")
    check(intake["selected_routes"] == ["direct_tau_PP_grid"], "good route must select direct route")
    check(firewall["firewall_passed"] is True, "good route must pass firewall")
    check(
        submission_audit["audit_decision"] == "NUMERIC_ROUTE_READY_FOR_MATERIALIZE_REPLAY",
        "good route audit must be ready for materializer",
    )
    check(
        submission_audit["numeric_route_ready_for_materializer"] is True,
        "good route must be materializer-ready",
    )
    check(materializer["projection_replay_written"] is True, "materializer must write replay")
    check(materializer["projection_replay_valid_shape"] is True, "projection replay must have ACT shape 18")
    check(preflight["ready_for_reduced_score_execution"] is True, "preflight must be ready after replay")
    check(pipeline_dry_run["pipeline_ready"] is True, "dry-run pipeline must be ready after replay")
    check(pipeline_dry_run["score_run"] is False, "dry-run pipeline must not run score")
    check(readiness["readiness_decision"] == "READY_TO_SCORE", "readiness must reach READY_TO_SCORE")
    check(readiness["score_run"] is False, "readiness must not run score")
    check(materializer["score_run"] is False, "materializer must not run score")
    check(preflight["score_run"] is False, "preflight must not run score")
    check(materializer["dark_sector_verdict"] is False, "materializer must not issue verdict")
    check(preflight["dark_sector_verdict"] is False, "preflight must not issue verdict")

    report = {
        "report_id": "tau_lensing_good_route_submission_path_smoke_v01",
        "claim_boundary": "good_route_submission_smoke_synthetic_only_no_physical_tau_score_no_dark_sector_verdict",
        "synthetic_good_route": "direct_tau_PP_grid_zero_grid_L_10_to_3009",
        "intake_selected_route_count": intake["selected_route_count"],
        "firewall_passed": firewall["firewall_passed"],
        "submission_audit_decision": submission_audit["audit_decision"],
        "numeric_route_ready_for_materializer": submission_audit["numeric_route_ready_for_materializer"],
        "projection_replay_written": materializer["projection_replay_written"],
        "projection_replay_valid_shape": materializer["projection_replay_valid_shape"],
        "preflight_ready": preflight["ready_for_reduced_score_execution"],
        "pipeline_dry_run_ready": pipeline_dry_run["pipeline_ready"],
        "readiness_decision": readiness["readiness_decision"],
        "score_run": False,
        "score_is_physical_tau_score": False,
        "dark_sector_verdict": False,
        "smoke_passed": True,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
