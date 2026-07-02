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
ROUTE = "direct_tau_PP_grid"
STAGING_DIR = ROOT / "payload_staging" / ROUTE
GRID = STAGING_DIR / "tau_lensing_response_pp_grid_v01.csv"
DECLARATION = STAGING_DIR / "tau_lensing_response_grid_route_declaration_v01.md"
PROVENANCE = STAGING_DIR / "tau_lensing_response_grid_provenance_v01.json"
PAYLOAD_GRID = ROOT / "payloads/tau_lensing_response_pp_grid_v01.csv"
PAYLOAD_DECLARATION = ROOT / "payloads/tau_lensing_response_grid_route_declaration_v01.md"
PAYLOAD_PROVENANCE = ROOT / "payloads/tau_lensing_response_grid_provenance_v01.json"
REPLAY = ROOT / "payloads/tau_lensing_pp_grid_projection_replay_v01.json"
PAYLOAD_TEMP_FILES = [PAYLOAD_GRID, PAYLOAD_DECLARATION, PAYLOAD_PROVENANCE, REPLAY]


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


def backup_staging(tmpdir: Path) -> None:
    if STAGING_DIR.exists():
        shutil.copytree(STAGING_DIR, tmpdir / "backup")


def restore_staging(tmpdir: Path) -> None:
    if STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)
    backup = tmpdir / "backup"
    if backup.exists():
        shutil.copytree(backup, STAGING_DIR)


def assert_no_existing_payloads() -> None:
    preexisting = [str(path.relative_to(ROOT)) for path in PAYLOAD_TEMP_FILES if path.exists()]
    if preexisting:
        raise RuntimeError(f"refusing to overwrite existing route/replay payloads: {preexisting}")


def cleanup_payloads() -> None:
    for path in PAYLOAD_TEMP_FILES:
        if path.exists():
            path.unlink()


def write_good_staging() -> None:
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
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
                "endpoint_blind_statement: synthetic staging promotion copy smoke only; not physical Tau evidence",
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
                "source_chain": "synthetic_staging_promotion_copy_smoke_only",
                "input_artifacts": ["synthetic_zero_grid"],
                "derivation_script_or_formula": "synthetic_staging_promotion_copy_smoke_only",
                "created_utc": "not_physical_payload",
                "author_or_agent": "smoke_test",
                "no_endpoint_fit_statement": "synthetic route was generated before endpoint comparison and used no endpoint feedback",
                "notes": "Synthetic staging promotion copy smoke only. Do not interpret as Tau evidence.",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def main() -> None:
    assert_no_existing_payloads()
    with tempfile.TemporaryDirectory(prefix="tau_lensing_staging_copy_") as tmp:
        tmpdir = Path(tmp)
        backup_staging(tmpdir)
        try:
            write_good_staging()
            promotion = run_json(
                [
                    sys.executable,
                    "scripts/promote_tau_lensing_staging_payload.py",
                    "--route",
                    ROUTE,
                ]
            )
            intake = run_json([sys.executable, "scripts/intake_tau_lensing_route_evidence.py"])
            firewall = run_json([sys.executable, "scripts/check_tau_lensing_route_evidence_firewall.py"])
            submission_audit = run_json([sys.executable, "scripts/audit_tau_lensing_route_submission.py"])
            materializer = run_json([sys.executable, "scripts/materialize_tau_lensing_projection_replay.py"])
            preflight = run_json([sys.executable, "scripts/preflight_tau_lensing_reduced_score.py"])
        finally:
            cleanup_payloads()
            restore_staging(tmpdir)

    check(promotion["promotion_decision"] == "PROMOTED_TO_PAYLOADS", "promotion must copy valid staging")
    check(promotion["payload_copy_performed"] is True, "payload copy must be performed for valid staging")
    check(intake["selected_route_count"] == 1, "promoted route must be visible to intake")
    check(firewall["firewall_passed"] is True, "promoted route must pass firewall")
    check(
        submission_audit["audit_decision"] == "NUMERIC_ROUTE_READY_FOR_MATERIALIZE_REPLAY",
        "promoted route audit must be materializer-ready",
    )
    check(materializer["projection_replay_valid_shape"] is True, "promoted route replay must have ACT shape")
    check(preflight["ready_for_reduced_score_execution"] is True, "promoted route must reach score preflight")
    check(all(not path.exists() for path in PAYLOAD_TEMP_FILES), "temporary payload/replay files must be cleaned")
    check("TEMPLATE_NOT_PAYLOAD" in GRID.read_text(errors="ignore"), "staging skeleton must be restored")

    report = {
        "report_id": "tau_lensing_staging_promotion_copy_path_smoke_v01",
        "claim_boundary": "staging_promotion_copy_path_smoke_synthetic_only_no_physical_tau_score_no_dark_sector_verdict",
        "synthetic_staging_route": ROUTE,
        "promotion_decision": promotion["promotion_decision"],
        "payload_copy_performed": True,
        "firewall_passed": firewall["firewall_passed"],
        "submission_audit_decision": submission_audit["audit_decision"],
        "projection_replay_valid_shape": materializer["projection_replay_valid_shape"],
        "preflight_ready": preflight["ready_for_reduced_score_execution"],
        "temporary_payloads_cleaned": True,
        "score_run": False,
        "score_is_physical_tau_score": False,
        "dark_sector_verdict": False,
        "smoke_passed": True,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
