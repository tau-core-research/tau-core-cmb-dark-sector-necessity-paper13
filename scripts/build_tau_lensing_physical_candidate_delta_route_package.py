#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ROUTE_DIR = ROOT / "payload_staging/delta_PP_tau_against_named_fiducial_PP"
GRID = ROUTE_DIR / "tau_lensing_response_delta_pp_v01.csv"
DECLARATION = ROUTE_DIR / "tau_lensing_response_grid_route_declaration_v01.md"
PROVENANCE = ROUTE_DIR / "tau_lensing_response_grid_provenance_v01.json"
FIDUCIAL = ROUTE_DIR / "tau_lensing_response_fiducial_pp_reference_v01.json"
PRECHECK = ROOT / "scripts/precheck_tau_lensing_physical_candidate_upstream_table.py"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_physical_candidate_delta_route_package_v01.json"
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


def run_json(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout)


def load_metadata(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def write_declaration(metadata: dict[str, Any]) -> None:
    endpoint_blind = str(metadata["endpoint_blind_statement"]).strip()
    text = "\n".join(
        [
            "selected_route: delta_PP_tau_against_named_fiducial_PP",
            "numeric_grid_file: payloads/tau_lensing_response_delta_pp_v01.csv",
            "fiducial_reference_file: payloads/tau_lensing_response_fiducial_pp_reference_v01.json",
            "provenance_file: payloads/tau_lensing_response_grid_provenance_v01.json",
            "index_alignment: L = 10 + i",
            f"endpoint_blind_statement: {endpoint_blind}",
            "",
        ]
    )
    DECLARATION.write_text(text)


def write_provenance(grid_hash: str, metadata: dict[str, Any]) -> None:
    payload = {
        "selected_route": "delta_PP_tau_against_named_fiducial_PP",
        "numeric_grid_file": "payloads/tau_lensing_response_delta_pp_v01.csv",
        "numeric_grid_sha256": grid_hash,
        "source_chain": metadata["source_chain"],
        "input_artifacts": [
            "payload_staging/tau_lensing_upstream_l_response_v01.csv",
            "payload_staging/tau_lensing_upstream_l_response_metadata_v01.json",
            "payload_staging/tau_lensing_grid_formula_spec_v01.json",
        ],
        "formula_role": metadata.get("formula_role", "endpoint_blind_tabulated_tau_lensing_response"),
        "parameter_policy": metadata["parameter_policy"],
        "normalization_statement": metadata["normalization_statement"],
        "known_limit_statement": metadata["known_limit_statement"],
        "derivation_script_or_formula": metadata["derivation_script_or_formula"],
        "no_endpoint_fit_statement": (
            "The physical-candidate Tau grid is fixed before endpoint score readout and is not adjusted using "
            "endpoint measurement residuals, score outputs, or verdict preferences."
        ),
        "route_classification": "physical_candidate",
        "created_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "author_or_agent": "codex",
        "notes": "Physical-candidate route package; still no score, likelihood, or dark-sector verdict.",
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
                "role": "named_fiducial_lenspotential_PP_reference_for_physical_candidate_delta_route",
            }
        ],
        "notes": "Fiducial reference metadata for the physical-candidate delta grid route; no score is computed here.",
    }
    FIDUCIAL.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Populate the physical-candidate delta route staging package.")
    parser.add_argument("--metadata", default="payload_staging/tau_lensing_upstream_l_response_metadata_v01.json")
    parser.add_argument("--fiducial-source", default=str(DEFAULT_FIDUCIAL_SOURCE))
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    args = parser.parse_args()

    metadata_path = Path(args.metadata).resolve()
    precheck = run_json([sys.executable, str(PRECHECK), "--metadata", str(metadata_path), "--write-report"])
    if precheck.get("precheck_passed") is not True:
        report = {
            "report_id": "cmb_tau_lensing_physical_candidate_delta_route_package_v01",
            "claim_boundary": "physical_candidate_delta_route_package_blocked_no_score_no_dark_sector_verdict",
            "package_status": "BLOCKED_PHYSICAL_CANDIDATE_PRECHECK_FAILED",
            "precheck": precheck,
            "score_run": False,
            "physical_tau_score_run": False,
            "dark_sector_verdict": False,
            "next_required_action": "replace_control_or_probe_inputs_with_tau_derived_endpoint_blind_response",
        }
    else:
        if not GRID.exists():
            raise FileNotFoundError(GRID)
        metadata = load_metadata(metadata_path)
        fiducial_source = Path(args.fiducial_source).resolve()
        grid_hash = sha256_file(GRID)
        write_declaration(metadata)
        write_provenance(grid_hash, metadata)
        write_fiducial(fiducial_source)
        report = {
            "report_id": "cmb_tau_lensing_physical_candidate_delta_route_package_v01",
            "claim_boundary": "physical_candidate_delta_route_package_only_no_score_no_dark_sector_verdict",
            "package_status": "PHYSICAL_CANDIDATE_DELTA_ROUTE_STAGING_PACKAGE_WRITTEN",
            "selected_route": "delta_PP_tau_against_named_fiducial_PP",
            "grid": rel(GRID),
            "grid_sha256": grid_hash,
            "declaration": rel(DECLARATION),
            "provenance": rel(PROVENANCE),
            "fiducial_reference": rel(FIDUCIAL),
            "fiducial_source": rel(fiducial_source),
            "fiducial_source_sha256": sha256_file(fiducial_source),
            "precheck": precheck,
            "score_run": False,
            "physical_tau_score_run": False,
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
