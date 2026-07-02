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
TMP_SCORE = ROOT / ".tmp/tau_lensing_guarded_positive_smoke_score.json"
TMP_REPORT = ROOT / ".tmp/tau_lensing_guarded_positive_smoke_report.json"
TMP_RECEIPT = ROOT / ".tmp/tau_lensing_guarded_positive_smoke_receipt.json"
TEMP_FILES = [GRID, DECLARATION, PROVENANCE, REPLAY, TMP_SCORE, TMP_REPORT, TMP_RECEIPT]


def run_json(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if completed.returncode != 0:
        raise RuntimeError(
            f"command failed: {' '.join(args)}\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
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
        raise RuntimeError(f"refusing to overwrite existing temporary score smoke files: {preexisting}")

    GRID.parent.mkdir(parents=True, exist_ok=True)
    TMP_SCORE.parent.mkdir(parents=True, exist_ok=True)
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
                "source_chain": "synthetic_guarded_positive_score_entrypoint_smoke_only",
                "derivation_script_or_formula": "synthetic_guarded_positive_score_entrypoint_smoke_only",
                "no_endpoint_fit_statement": "synthetic_guarded_positive_score_entrypoint_smoke_only",
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
        guard = run_json([sys.executable, "scripts/guard_tau_lensing_score_attempt.py"])
        guarded_score = run_json(
            [
                sys.executable,
                "scripts/run_tau_lensing_guarded_score_report.py",
                "--score-out",
                str(TMP_SCORE),
                "--write-report",
                str(TMP_REPORT),
                "--write-receipt",
                str(TMP_RECEIPT),
            ]
        )
        receipt = json.loads(TMP_RECEIPT.read_text())
        score_validation = run_json([sys.executable, "scripts/validate_tau_lensing_reduced_score_output.py", str(TMP_SCORE)])
    finally:
        cleanup()

    check(materializer["projection_replay_written"] is True, "synthetic route must materialize replay")
    check(guard["score_attempt_allowed"] is True, "synthetic good route must allow guarded score attempt")
    check(guarded_score["guarded_score_report"] is True, "guarded score must record guarded entrypoint")
    check(guarded_score["score_run"] is True, "guarded score must run on synthetic accepted route")
    check(guarded_score["dark_sector_verdict"] is False, "guarded score must not issue verdict")
    check(receipt["receipt_status"] == "REDUCED_SCORE_EXECUTION_COMPLETED", "completed receipt status mismatch")
    check(receipt["score_output_validation_passed"] is True, "completed receipt must bind output validation")
    check(isinstance(receipt["score_output_sha256"], str), "completed receipt must bind score output hash")
    check(score_validation["validated"] is True, "synthetic guarded score output must validate")
    check(not TMP_SCORE.exists(), "temporary score output must be cleaned")
    check(not TMP_RECEIPT.exists(), "temporary receipt must be cleaned")
    check(not REPLAY.exists(), "temporary replay must be cleaned")

    report = {
        "report_id": "tau_lensing_guarded_positive_score_entrypoint_smoke_v01",
        "claim_boundary": "guarded_positive_score_entrypoint_smoke_synthetic_only_no_physical_tau_score_no_dark_sector_verdict",
        "synthetic_good_route": "direct_tau_PP_grid_zero_grid_L_10_to_3009",
        "score_attempt_allowed": guard["score_attempt_allowed"],
        "guarded_score_report": guarded_score["guarded_score_report"],
        "score_schema_validated": score_validation["validated"],
        "receipt_status": receipt["receipt_status"],
        "score_output_sha256_bound": isinstance(receipt["score_output_sha256"], str),
        "score_run": True,
        "score_is_physical_tau_score": False,
        "temporary_score_output_cleaned": True,
        "dark_sector_verdict": False,
        "smoke_passed": True,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
