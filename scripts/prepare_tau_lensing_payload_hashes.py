#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

ROUTE_FILES = {
    "direct_tau_PP_grid": ROOT / "payloads/tau_lensing_response_pp_grid_v01.csv",
    "delta_PP_tau_against_named_fiducial_PP": ROOT / "payloads/tau_lensing_response_delta_pp_v01.csv",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_report(route: str) -> dict[str, Any]:
    grid = ROUTE_FILES[route]
    exists = grid.exists()
    report: dict[str, Any] = {
        "report_id": "tau_lensing_payload_hash_preparation_v01",
        "claim_boundary": "payload_hash_preparation_only_no_grid_validation_no_score_no_dark_sector_verdict",
        "selected_route": route,
        "numeric_grid_file": rel(grid),
        "numeric_grid_exists": exists,
        "score_run": False,
        "dark_sector_verdict": False,
    }
    if not exists:
        report["ready_for_provenance_copy"] = False
        report["next_required_action"] = f"create_{rel(grid)}_from_blind_tau_route_evidence"
        return report

    grid_hash = sha256_file(grid)
    report.update(
        {
            "numeric_grid_sha256": grid_hash,
            "ready_for_provenance_copy": True,
            "provenance_fields_to_copy": {
                "selected_route": route,
                "numeric_grid_file": rel(grid),
                "numeric_grid_sha256": grid_hash,
            },
            "next_required_action": "copy_fields_into_payloads/tau_lensing_response_grid_provenance_v01.json_then_run_make_evidence_check",
        }
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepare SHA256 provenance fields for a submitted Tau lensing numeric payload."
    )
    parser.add_argument(
        "--route",
        required=True,
        choices=sorted(ROUTE_FILES),
        help="Route whose numeric grid hash should be prepared.",
    )
    args = parser.parse_args()
    print(json.dumps(build_report(args.route), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
