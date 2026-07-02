#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "payload_staging/tau_lensing_upstream_l_response_v01.csv"
DEFAULT_METADATA = ROOT / "payload_staging/tau_lensing_upstream_l_response_metadata_v01.json"
DEFAULT_SPEC = ROOT / "payload_staging/tau_lensing_grid_formula_spec_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_upstream_grid_handoff_dry_run_v01.json"

GRID_BY_ROUTE = {
    "direct_tau_PP_grid": ROOT / "payload_staging/direct_tau_PP_grid/tau_lensing_response_pp_grid_v01.csv",
    "delta_PP_tau_against_named_fiducial_PP": ROOT
    / "payload_staging/delta_PP_tau_against_named_fiducial_PP/tau_lensing_response_delta_pp_v01.csv",
}

VALIDATOR_ROUTE = {
    "direct_tau_PP_grid": "direct_tau_PP_grid",
    "delta_PP_tau_against_named_fiducial_PP": "delta_PP_tau",
}


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def run_json(command: list[str]) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(
            json.dumps(
                {
                    "command": command,
                    "returncode": completed.returncode,
                    "stdout": completed.stdout,
                    "stderr": completed.stderr,
                },
                indent=2,
                sort_keys=True,
            )
        )
    return json.loads(completed.stdout)


def missing_inputs(table: Path, metadata: Path) -> list[str]:
    missing = []
    if not table.exists():
        missing.append(rel(table))
    if not metadata.exists():
        missing.append(rel(metadata))
    return missing


def build_missing_report(table: Path, metadata: Path) -> dict[str, Any]:
    return {
        "report_id": "cmb_tau_lensing_upstream_grid_handoff_dry_run_v01",
        "claim_boundary": "upstream_grid_handoff_dry_run_only_no_score_no_dark_sector_verdict",
        "handoff_status": "MISSING_UPSTREAM_INPUTS",
        "missing_inputs": missing_inputs(table, metadata),
        "required_table": rel(table),
        "required_metadata": rel(metadata),
        "score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": "provide_upstream_tau_l_response_csv_and_metadata_json_then_rerun_handoff_dry_run",
    }


def build_invalid_report(table: Path, metadata: Path, error: Exception) -> dict[str, Any]:
    error_text = str(error)
    error_summary = error_text
    try:
        payload = json.loads(error_text)
        stderr_lines = [line.strip() for line in payload.get("stderr", "").splitlines() if line.strip()]
        if stderr_lines:
            error_summary = stderr_lines[-1]
    except json.JSONDecodeError:
        pass
    return {
        "report_id": "cmb_tau_lensing_upstream_grid_handoff_dry_run_v01",
        "claim_boundary": "upstream_grid_handoff_dry_run_only_no_score_no_dark_sector_verdict",
        "handoff_status": "UPSTREAM_INPUTS_PRESENT_BUT_INVALID",
        "required_table": rel(table),
        "required_metadata": rel(metadata),
        "error_summary": error_summary,
        "error_detail": error_text,
        "score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": "replace_template_or_invalid_upstream_inputs_with_endpoint_blind_tau_table_and_metadata",
    }


def build_success_report(table: Path, metadata: Path, spec: Path, write_staging: bool) -> dict[str, Any]:
    spec_report = run_json(
        [
            sys.executable,
            "scripts/build_tau_lensing_upstream_table_formula_spec.py",
            "--table",
            str(table),
            "--metadata",
            str(metadata),
            "--write-spec",
            str(spec),
            "--write-report",
        ]
    )
    materializer_command = [
        sys.executable,
        "scripts/materialize_tau_lensing_grid_from_formula_spec.py",
        str(spec),
        "--write-report",
    ]
    if write_staging:
        materializer_command.append("--write-staging")
    materializer_report = run_json(materializer_command)
    route = materializer_report["selected_route"]
    grid = GRID_BY_ROUTE[route]
    validation_report: dict[str, Any] | None = None
    if write_staging:
        validation_report = run_json(
            [
                sys.executable,
                "scripts/validate_tau_lensing_grid_payload.py",
                str(grid),
                "--route",
                VALIDATOR_ROUTE[route],
                "--project",
            ]
        )

    return {
        "report_id": "cmb_tau_lensing_upstream_grid_handoff_dry_run_v01",
        "claim_boundary": "upstream_grid_handoff_dry_run_only_no_score_no_dark_sector_verdict",
        "handoff_status": "GRID_HANDOFF_DRY_RUN_PASSED",
        "required_table": rel(table),
        "required_metadata": rel(metadata),
        "formula_spec": rel(spec),
        "selected_route": route,
        "staging_grid": rel(grid),
        "staging_grid_written": write_staging,
        "upstream_spec_report": spec_report,
        "materializer_report": materializer_report,
        "grid_validation_report": validation_report,
        "score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": (
            "review_grid_validation_then_run_matching_staging_promotion_dry_run"
            if write_staging
            else "rerun_with_write_staging_after_reviewing_upstream_spec_report"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Dry-run the upstream Tau table -> formula spec -> grid handoff.")
    parser.add_argument("--table", default=str(DEFAULT_TABLE))
    parser.add_argument("--metadata", default=str(DEFAULT_METADATA))
    parser.add_argument("--spec", default=str(DEFAULT_SPEC))
    parser.add_argument("--write-staging", action="store_true")
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    args = parser.parse_args()

    table = Path(args.table).resolve()
    metadata = Path(args.metadata).resolve()
    spec = Path(args.spec).resolve()
    if missing_inputs(table, metadata):
        report = build_missing_report(table, metadata)
    else:
        try:
            report = build_success_report(table, metadata, spec, args.write_staging)
        except Exception as error:
            report = build_invalid_report(table, metadata, error)

    text = json.dumps(report, indent=2, sort_keys=True)
    if args.write_report:
        report_path = Path(args.write_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
