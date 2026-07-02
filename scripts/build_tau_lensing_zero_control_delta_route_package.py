#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTE_DIR = ROOT / "payload_staging/delta_PP_tau_against_named_fiducial_PP"
GRID = ROUTE_DIR / "tau_lensing_response_delta_pp_v01.csv"
DECLARATION = ROUTE_DIR / "tau_lensing_response_grid_route_declaration_v01.md"
PROVENANCE = ROUTE_DIR / "tau_lensing_response_grid_provenance_v01.json"
FIDUCIAL = ROUTE_DIR / "tau_lensing_response_fiducial_pp_reference_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_zero_control_delta_route_package_v01.json"
DEFAULT_FIDUCIAL_SOURCE = (
    ROOT / "data/external/act_dr6_lensing/extracted/v1.2/like_corrs/cosmo2017_10K_acc3_lenspotentialCls.dat"
)


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_declaration() -> None:
    text = "\n".join(
        [
            "selected_route: delta_PP_tau_against_named_fiducial_PP",
            "numeric_grid_file: payloads/tau_lensing_response_delta_pp_v01.csv",
            "fiducial_reference_file: payloads/tau_lensing_response_fiducial_pp_reference_v01.json",
            "provenance_file: payloads/tau_lensing_response_grid_provenance_v01.json",
            "index_alignment: L = 10 + i",
            (
                "endpoint_blind_statement: zero-response control fixed by definition before any endpoint "
                "score readout; no endpoint-fit information enters the delta grid"
            ),
            "",
        ]
    )
    DECLARATION.write_text(text)


def write_provenance(grid_hash: str) -> None:
    payload = {
        "selected_route": "delta_PP_tau_against_named_fiducial_PP",
        "numeric_grid_file": "payloads/tau_lensing_response_delta_pp_v01.csv",
        "numeric_grid_sha256": grid_hash,
        "source_chain": [
            "scripts/build_tau_lensing_zero_response_control.py",
            "scripts/run_tau_lensing_upstream_grid_handoff_dry_run.py",
            "docs/cmb_tau_lensing_upstream_table_formula_spec_contract_v01.md",
        ],
        "input_artifacts": [
            "payload_staging/tau_lensing_upstream_l_response_v01.csv",
            "payload_staging/tau_lensing_upstream_l_response_metadata_v01.json",
            "payload_staging/tau_lensing_grid_formula_spec_v01.json",
        ],
        "derivation_script_or_formula": (
            "For every L in 10..3009, delta_PP_tau(L)=0 by endpoint-blind null-control definition."
        ),
        "no_endpoint_fit_statement": (
            "The grid is identically zero by control definition and is not adjusted using endpoint "
            "residuals, score outputs, or verdict preferences."
        ),
        "created_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "author_or_agent": "codex",
        "notes": "Null-control delta route package; not a Tau response success claim.",
    }
    PROVENANCE.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def write_fiducial(fiducial_source: Path) -> None:
    if not fiducial_source.exists():
        raise FileNotFoundError(fiducial_source)
    payload = {
        "fiducial_reference_file": "payloads/tau_lensing_response_fiducial_pp_reference_v01.json",
        "fiducial_reference_sha256": sha256_file(fiducial_source),
        "generated_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "files": [
            {
                "path": rel(fiducial_source),
                "sha256": sha256_file(fiducial_source),
                "role": "named_fiducial_lenspotential_PP_reference_for_delta_control",
            }
        ],
        "notes": "Fiducial reference metadata for the delta grid route; no score is computed here.",
    }
    FIDUCIAL.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Populate the zero-control delta route staging package.")
    parser.add_argument("--fiducial-source", default=str(DEFAULT_FIDUCIAL_SOURCE))
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    args = parser.parse_args()

    if not GRID.exists():
        raise FileNotFoundError(GRID)
    fiducial_source = Path(args.fiducial_source).resolve()
    grid_hash = sha256_file(GRID)
    write_declaration()
    write_provenance(grid_hash)
    write_fiducial(fiducial_source)
    report = {
        "report_id": "cmb_tau_lensing_zero_control_delta_route_package_v01",
        "claim_boundary": "zero_control_delta_route_package_only_no_score_no_dark_sector_verdict",
        "package_status": "ZERO_CONTROL_DELTA_ROUTE_STAGING_PACKAGE_WRITTEN",
        "selected_route": "delta_PP_tau_against_named_fiducial_PP",
        "grid": rel(GRID),
        "grid_sha256": grid_hash,
        "declaration": rel(DECLARATION),
        "provenance": rel(PROVENANCE),
        "fiducial_reference": rel(FIDUCIAL),
        "fiducial_source": rel(fiducial_source),
        "fiducial_source_sha256": sha256_file(fiducial_source),
        "score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": "run_make_staging-promote-delta-dry-run",
    }
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.write_report:
        report_path = Path(args.write_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
