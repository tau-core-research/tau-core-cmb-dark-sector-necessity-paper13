#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "payload_staging/tau_lensing_upstream_l_response_v01.csv"
DEFAULT_METADATA = ROOT / "payload_staging/tau_lensing_upstream_l_response_metadata_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_zero_response_control_v01.json"


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def write_table(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["L", "tau_response_value"])
        for ell in range(10, 3010):
            writer.writerow([ell, "0.00000000000000000e+00"])


def metadata_payload() -> dict[str, object]:
    return {
        "selected_route": "delta_PP_tau_against_named_fiducial_PP",
        "l_column": "L",
        "value_column": "tau_response_value",
        "formula_role": "endpoint_blind_zero_tau_lensing_response_control",
        "endpoint_blind_statement": (
            "Zero-response control fixed before endpoint residual or score readout; "
            "not a fitted Tau response and not a physical dark-sector verdict."
        ),
        "parameter_policy": "all_values_fixed_to_zero_by_control_definition_before_ACT_or_Planck_residual_score_readout",
        "source_chain": [
            "scripts/build_tau_lensing_zero_response_control.py",
            "docs/cmb_tau_lensing_upstream_table_formula_spec_contract_v01.md",
        ],
        "normalization_statement": (
            "delta_PP_tau(L)=0 in the selected PP/delta response slot; this is a null-control normalization only."
        ),
        "known_limit_statement": (
            "Known-limit control: no additional Tau lensing response relative to the named fiducial reference."
        ),
        "derivation_script_or_formula": (
            "For all L in 10..3009, delta_PP_tau(L)=0 by explicit endpoint-blind control definition."
        ),
        "claim_boundary": "zero_response_control_only_no_tau_score_no_dark_sector_verdict",
    }


def write_metadata(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metadata_payload(), indent=2, sort_keys=True) + "\n")


def build_report(table: Path, metadata: Path) -> dict[str, object]:
    return {
        "report_id": "cmb_tau_lensing_zero_response_control_v01",
        "claim_boundary": "zero_response_control_only_no_tau_score_no_dark_sector_verdict",
        "control_status": "ZERO_RESPONSE_CONTROL_WRITTEN",
        "upstream_table": rel(table),
        "upstream_metadata": rel(metadata),
        "selected_route": "delta_PP_tau_against_named_fiducial_PP",
        "rows": 3000,
        "value_rule": "delta_PP_tau(L)=0 for L=10..3009",
        "score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": "run_make_tau-grid-handoff-write-staging_for_control_grid_validation",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Write an endpoint-blind zero Tau lensing response control.")
    parser.add_argument("--table", default=str(DEFAULT_TABLE))
    parser.add_argument("--metadata", default=str(DEFAULT_METADATA))
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    args = parser.parse_args()

    table = Path(args.table).resolve()
    metadata = Path(args.metadata).resolve()
    write_table(table)
    write_metadata(metadata)
    report = build_report(table, metadata)
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.write_report:
        report_path = Path(args.write_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
