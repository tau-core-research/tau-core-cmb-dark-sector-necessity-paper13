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
FILES = [GRID, DECLARATION, PROVENANCE]


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
                "endpoint_blind_statement: synthetic staging promotion smoke only; not physical Tau evidence",
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
                "source_chain": "synthetic_staging_promotion_smoke_only",
                "input_artifacts": ["synthetic_zero_grid"],
                "derivation_script_or_formula": "synthetic_staging_promotion_smoke_only",
                "created_utc": "not_physical_payload",
                "author_or_agent": "smoke_test",
                "no_endpoint_fit_statement": "synthetic route was generated before endpoint comparison and used no endpoint feedback",
                "notes": "Synthetic staging promotion smoke only. Do not copy to payloads as Tau evidence.",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="tau_lensing_staging_positive_") as tmp:
        tmpdir = Path(tmp)
        backup_staging(tmpdir)
        try:
            write_good_staging()
            precheck = run_json(
                [
                    sys.executable,
                    "scripts/precheck_tau_lensing_staging_promotion.py",
                    "--route",
                    ROUTE,
                ]
            )
        finally:
            restore_staging(tmpdir)

    check(precheck["promotion_ready"] is True, "good staging route must be promotion-ready")
    check(precheck["score_run"] is False, "staging precheck must not run score")
    check(precheck["dark_sector_verdict"] is False, "staging precheck must not issue verdict")
    check(all(item.get("passes") is True for item in precheck["checks"]), "all staging checks must pass")
    check(all(path.exists() for path in FILES), "original staging skeleton must be restored")
    check(
        any("TEMPLATE_NOT_PAYLOAD" in path.read_text(errors="ignore") for path in FILES),
        "restored staging skeleton should retain template marker",
    )

    report = {
        "report_id": "tau_lensing_staging_promotion_positive_path_smoke_v01",
        "claim_boundary": "staging_promotion_positive_smoke_synthetic_only_no_payload_copy_no_score_no_dark_sector_verdict",
        "synthetic_staging_route": ROUTE,
        "promotion_ready": precheck["promotion_ready"],
        "all_checks_passed": all(item.get("passes") is True for item in precheck["checks"]),
        "payload_copy_performed": False,
        "score_run": False,
        "dark_sector_verdict": False,
        "smoke_passed": True,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
