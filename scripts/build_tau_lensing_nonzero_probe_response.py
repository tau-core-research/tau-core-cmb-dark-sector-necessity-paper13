#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "payload_staging/tau_lensing_upstream_l_response_v01.csv"
DEFAULT_METADATA = ROOT / "payload_staging/tau_lensing_upstream_l_response_metadata_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_nonzero_probe_response_v01.json"


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def response_value(ell: int, amplitude: float, l0: float, cutoff: float) -> float:
    return amplitude * (ell / l0) * math.exp(-((ell / cutoff) ** 2))


def write_table(path: Path, amplitude: float, l0: float, cutoff: float) -> dict[str, float]:
    path.parent.mkdir(parents=True, exist_ok=True)
    values: list[float] = []
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["L", "tau_response_value"])
        for ell in range(10, 3010):
            value = response_value(ell, amplitude, l0, cutoff)
            values.append(value)
            writer.writerow([ell, format(value, ".17e")])
    return {
        "rows": len(values),
        "min_value": min(values),
        "max_value": max(values),
        "mean_value": sum(values) / len(values),
        "max_abs_value": max(abs(value) for value in values),
    }


def write_metadata(path: Path, amplitude: float, l0: float, cutoff: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "selected_route": "delta_PP_tau_against_named_fiducial_PP",
        "l_column": "L",
        "value_column": "tau_response_value",
        "formula_role": "endpoint_blind_nonzero_tau_lensing_response_probe",
        "endpoint_blind_statement": (
            "Nonzero diagnostic probe fixed before endpoint residual or score readout; "
            "not fitted to endpoint measurement residuals and not a physical Tau response claim."
        ),
        "parameter_policy": (
            "probe parameters fixed by script constants before any endpoint score readout; "
            "replace with Tau-derived parameters before physical interpretation"
        ),
        "source_chain": [
            "scripts/build_tau_lensing_nonzero_probe_response.py",
            "docs/cmb_tau_lensing_upstream_table_formula_spec_contract_v01.md",
        ],
        "normalization_statement": (
            "dimensionless diagnostic delta_PP_tau probe amplitude; no physical PP normalization claim"
        ),
        "known_limit_statement": (
            "diagnostic nonzero handoff probe only; no LCDM reproduction, no failure verdict, no dark-sector verdict"
        ),
        "derivation_script_or_formula": (
            f"delta_PP_tau(L) = {amplitude} * (L/{l0}) * exp(-(L/{cutoff})^2) "
            "for L=10..3009; diagnostic probe only"
        ),
        "claim_boundary": "nonzero_probe_response_only_no_tau_score_no_dark_sector_verdict",
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Write a nonzero endpoint-blind Tau lensing response probe.")
    parser.add_argument("--table", default=str(DEFAULT_TABLE))
    parser.add_argument("--metadata", default=str(DEFAULT_METADATA))
    parser.add_argument("--amplitude", type=float, default=1.0e-9)
    parser.add_argument("--l0", type=float, default=1000.0)
    parser.add_argument("--cutoff", type=float, default=2200.0)
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    args = parser.parse_args()

    table = Path(args.table).resolve()
    metadata = Path(args.metadata).resolve()
    stats = write_table(table, args.amplitude, args.l0, args.cutoff)
    write_metadata(metadata, args.amplitude, args.l0, args.cutoff)
    report = {
        "report_id": "cmb_tau_lensing_nonzero_probe_response_v01",
        "claim_boundary": "nonzero_probe_response_only_no_tau_score_no_dark_sector_verdict",
        "probe_status": "NONZERO_PROBE_RESPONSE_WRITTEN",
        "upstream_table": rel(table),
        "upstream_metadata": rel(metadata),
        "selected_route": "delta_PP_tau_against_named_fiducial_PP",
        "parameters": {"amplitude": args.amplitude, "L0": args.l0, "cutoff_L": args.cutoff},
        "table_stats": stats,
        "score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": "run_make_tau-grid-nonzero-precheck",
    }
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.write_report:
        report_path = Path(args.write_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
