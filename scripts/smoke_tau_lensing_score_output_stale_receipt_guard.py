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
                "source_chain": "synthetic_stale_receipt_guard_smoke_only",
                "derivation_script_or_formula": "synthetic_stale_receipt_guard_smoke_only",
                "no_endpoint_fit_statement": "synthetic_stale_receipt_guard_smoke_only",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def cleanup() -> None:
    for path in TEMP_FILES:
        if path.exists():
            path.unlink()


def main() -> None:
    try:
        write_good_direct_route()
        materializer = run_json([sys.executable, "scripts/materialize_tau_lensing_projection_replay.py"])
        audit = run_json([sys.executable, "scripts/audit_tau_lensing_score_output_status.py"])
    finally:
        cleanup()

    check(materializer["projection_replay_valid_shape"] is True, "synthetic route must reach replay")
    check(audit["score_attempt_allowed"] is True, "synthetic route should make guard allow")
    check(audit["score_gate_passed"] is True, "synthetic route should make score gate pass")
    check(
        audit["physical_tau_score_output_accepted"] is False,
        "existing score must not be accepted without matching completed receipt",
    )
    check(
        audit["score_execution_receipt_matches_score_output"] is False,
        "stale or blocked receipt must not match score output",
    )
    check(audit["score_run"] is False, "audit must not run score")
    check(audit["dark_sector_verdict"] is False, "audit must not issue verdict")

    report = {
        "report_id": "tau_lensing_score_output_stale_receipt_guard_smoke_v01",
        "claim_boundary": "score_output_stale_receipt_guard_smoke_only_no_new_score_no_dark_sector_verdict",
        "synthetic_good_route": "direct_tau_PP_grid_zero_grid_L_10_to_3009",
        "score_attempt_allowed": audit["score_attempt_allowed"],
        "score_gate_passed": audit["score_gate_passed"],
        "physical_tau_score_output_accepted": audit["physical_tau_score_output_accepted"],
        "score_execution_receipt_matches_score_output": audit["score_execution_receipt_matches_score_output"],
        "score_run": False,
        "dark_sector_verdict": False,
        "smoke_passed": True,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
