#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GRID = ROOT / "payloads/tau_lensing_response_pp_grid_v01.csv"
DECLARATION = ROOT / "payloads/tau_lensing_response_grid_route_declaration_v01.md"
PROVENANCE = ROOT / "payloads/tau_lensing_response_grid_provenance_v01.json"
REPLAY = ROOT / "payloads/tau_lensing_pp_grid_projection_replay_v01.json"
SCORE = ROOT / "payloads/tau_lensing_reduced_score_v01.json"
RECEIPT = ROOT / "data/derived/cmb_tau_lensing_score_execution_receipt_v01.json"
PIPELINE_REPORT = ROOT / "data/derived/cmb_tau_lensing_scoring_pipeline_report_v01.json"
TEMP_ROUTE_FILES = [GRID, DECLARATION, PROVENANCE, REPLAY]
BACKUP_FILES = [SCORE, RECEIPT, PIPELINE_REPORT]


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


def backup_files(tmpdir: Path) -> None:
    for path in BACKUP_FILES:
        if path.exists():
            target = tmpdir / path.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def restore_files(tmpdir: Path) -> None:
    for path in BACKUP_FILES:
        backup = tmpdir / path.relative_to(ROOT)
        if backup.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup, path)
        elif path.exists():
            path.unlink()


def assert_no_existing_route_files() -> None:
    preexisting = [str(path.relative_to(ROOT)) for path in TEMP_ROUTE_FILES if path.exists()]
    if preexisting:
        raise RuntimeError(f"refusing to overwrite existing route/replay payloads: {preexisting}")


def cleanup_route_files() -> None:
    for path in TEMP_ROUTE_FILES:
        if path.exists():
            path.unlink()


def write_good_direct_route() -> None:
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
                "source_chain": "synthetic_matching_receipt_acceptance_smoke_only",
                "derivation_script_or_formula": "synthetic_matching_receipt_acceptance_smoke_only",
                "no_endpoint_fit_statement": "synthetic_matching_receipt_acceptance_smoke_only",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def main() -> None:
    assert_no_existing_route_files()
    with tempfile.TemporaryDirectory(prefix="tau_lensing_matching_receipt_") as tmp:
        tmpdir = Path(tmp)
        backup_files(tmpdir)
        try:
            write_good_direct_route()
            materializer = run_json([sys.executable, "scripts/materialize_tau_lensing_projection_replay.py"])
            guarded_score = run_json(
                [
                    sys.executable,
                    "scripts/run_tau_lensing_guarded_score_report.py",
                    "--write-report",
                    "--write-receipt",
                ]
            )
            audit = run_json([sys.executable, "scripts/audit_tau_lensing_score_output_status.py"])
        finally:
            cleanup_route_files()
            restore_files(tmpdir)

    check(materializer["projection_replay_valid_shape"] is True, "synthetic route must reach replay")
    check(guarded_score["score_run"] is True, "guarded score must run for synthetic accepted route")
    check(guarded_score["guarded_score_report"] is True, "guarded score report marker missing")
    check(audit["score_attempt_allowed"] is True, "guard should allow during synthetic route")
    check(audit["score_gate_passed"] is True, "score gate should pass during synthetic route")
    check(audit["score_execution_receipt_matches_score_output"] is True, "receipt hash must match score output")
    check(audit["physical_tau_score_output_accepted"] is True, "matching receipt score must be accepted by audit")
    check(audit["dark_sector_verdict"] is False, "audit must not issue verdict")
    check(not REPLAY.exists(), "temporary replay must be cleaned")

    report = {
        "report_id": "tau_lensing_score_output_matching_receipt_acceptance_smoke_v01",
        "claim_boundary": "score_output_matching_receipt_acceptance_smoke_synthetic_only_no_dark_sector_verdict",
        "synthetic_good_route": "direct_tau_PP_grid_zero_grid_L_10_to_3009",
        "score_attempt_allowed": audit["score_attempt_allowed"],
        "score_gate_passed": audit["score_gate_passed"],
        "score_execution_receipt_matches_score_output": audit["score_execution_receipt_matches_score_output"],
        "physical_tau_score_output_accepted": audit["physical_tau_score_output_accepted"],
        "score_run": True,
        "score_is_physical_tau_score": False,
        "defaults_restored_after_smoke": True,
        "dark_sector_verdict": False,
        "smoke_passed": True,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
