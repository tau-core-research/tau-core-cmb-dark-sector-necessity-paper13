#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_L = np.arange(10, 3010, dtype=float)
DEFAULT_TEMPLATE = ROOT / "payload_templates/tau_lensing_route_b_parent_source_formula_spec_TEMPLATE_v01.json"
DEFAULT_TABLE = ROOT / "payload_staging/tau_lensing_route_b_parent_source_v01.csv"
DEFAULT_CONFIG = ROOT / "payload_staging/tau_lensing_route_b_parent_source_config_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_route_b_parent_source_formula_materialization_v01.json"


FORBIDDEN_TEXT = [
    "TEMPLATE_NOT_PAYLOAD",
    "FILL:",
    "ACT residual",
    "Planck residual",
    "reduced chi2",
    "score output",
    "dark-sector verdict",
    "diagnostic probe",
    "zero-control",
]


def rel(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_array(values: np.ndarray) -> str:
    contiguous = np.ascontiguousarray(values.astype("<f8", copy=False))
    return hashlib.sha256(contiguous.tobytes()).hexdigest()


def template_spec() -> dict[str, Any]:
    return {
        "template_status": "TEMPLATE_NOT_PAYLOAD",
        "spec_id": "tau_lensing_route_b_parent_source_formula_spec_v01",
        "claim_boundary": "route_b_parent_source_formula_spec_template_only_no_parent_source_no_grid_no_score_no_verdict",
        "formula_family": "power_law_cutoff_parent_source_v01",
        "formula_role": "endpoint_blind_tau_parent_source_l_shape",
        "parameters": {
            "amplitude": 0.0,
            "L0": 1000.0,
            "tilt": 0.0,
            "cutoff_L": 2200.0,
            "cutoff_power": 2.0,
            "turnover_L": None,
            "turnover_power": 0.0,
        },
        "normalization": 1.0,
        "endpoint_blind_statement": "FILL: explain how the parent source and normalization were fixed before endpoint score readout",
        "parameter_policy": "FILL: no ACT/Planck residual, reduced-chi2, score-output, or verdict tuning",
        "source_chain": [
            "FILL: Tau parent-side morphology/source evidence artifact",
            "FILL: formula derivation or replay artifact",
            "FILL: normalization and known-limit audit artifact",
        ],
        "normalization_statement": "FILL: dimensionless delta_PP_tau = normalization * parent_tau_source_value",
        "known_limit_statement": "FILL: parent_tau_source_value -> 0 implies delta_PP_tau -> 0",
        "derivation_script_or_formula": (
            "parent_tau_source_value(L)=amplitude*(L/L0)^tilt*exp(-(L/cutoff_L)^cutoff_power)"
            "*(1+(L/turnover_L)^2)^(-turnover_power/2) when turnover_L is not null"
        ),
        "alternate_formula_family_example": {
            "formula_family": "tabulated_parent_source_v01",
            "parameters": {
                "source_table": "data/derived/endpoint_blind_parent_source_table.csv",
                "l_column": "L",
                "value_column": "parent_tau_source_value",
                "source_table_sha256": "",
            },
        },
        "notes": (
            "Remove template_status only after the formula and parameters are fixed by Tau-side "
            "evidence before endpoint score readout. This spec is not itself physical evidence."
        ),
    }


def reject_template_or_forbidden(spec: dict[str, Any]) -> None:
    inspected = {
        key: value
        for key, value in spec.items()
        if key
        not in {
            "endpoint_blind_statement",
            "parameter_policy",
            "known_limit_statement",
            "claim_boundary",
            "physical_validation_status",
        }
    }
    text = json.dumps(inspected, sort_keys=True)
    hits = [marker for marker in FORBIDDEN_TEXT if marker.lower() in text.lower()]
    if hits:
        raise ValueError(f"parent-source formula spec contains forbidden/template markers: {hits}")


def require_string(spec: dict[str, Any], key: str) -> str:
    value = spec.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"parent-source formula spec requires non-empty string field: {key}")
    return value.strip()


def require_source_chain(spec: dict[str, Any]) -> list[str]:
    source_chain = spec.get("source_chain")
    if not isinstance(source_chain, list) or not source_chain:
        raise ValueError("parent-source formula spec requires a non-empty source_chain list")
    cleaned = []
    for item in source_chain:
        if not isinstance(item, str) or not item.strip():
            raise ValueError("source_chain entries must be non-empty strings")
        cleaned.append(item.strip())
    return cleaned


def power_law_cutoff_parent_source(parameters: dict[str, Any]) -> np.ndarray:
    required = ["amplitude", "L0", "tilt", "cutoff_L", "cutoff_power"]
    for key in required:
        if key not in parameters:
            raise ValueError(f"missing power_law_cutoff_parent_source parameter: {key}")
    amplitude = float(parameters["amplitude"])
    l0 = float(parameters["L0"])
    tilt = float(parameters["tilt"])
    cutoff_l = float(parameters["cutoff_L"])
    cutoff_power = float(parameters["cutoff_power"])
    turnover_l_raw = parameters.get("turnover_L")
    turnover_power = float(parameters.get("turnover_power", 0.0))

    if l0 <= 0 or cutoff_l <= 0 or cutoff_power <= 0:
        raise ValueError("L0, cutoff_L, and cutoff_power must be positive")
    values = amplitude * np.power(EXPECTED_L / l0, tilt) * np.exp(-np.power(EXPECTED_L / cutoff_l, cutoff_power))
    if turnover_l_raw is not None:
        turnover_l = float(turnover_l_raw)
        if turnover_l <= 0:
            raise ValueError("turnover_L must be positive when supplied")
        values = values * np.power(1.0 + np.square(EXPECTED_L / turnover_l), -0.5 * turnover_power)
    if not np.all(np.isfinite(values)):
        raise ValueError("parent-source formula produced non-finite values")
    return values


def read_csv_table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        sample = handle.read(4096)
        handle.seek(0)
        dialect = csv.Sniffer().sniff(sample, delimiters=",\t ")
        reader = csv.DictReader(handle, dialect=dialect)
        if reader.fieldnames is None:
            raise ValueError(f"tabulated parent source has no header: {path}")
        return list(reader)


def tabulated_parent_source(parameters: dict[str, Any]) -> tuple[np.ndarray, dict[str, Any]]:
    required = ["source_table", "l_column", "value_column"]
    for key in required:
        if key not in parameters:
            raise ValueError(f"missing tabulated_parent_source parameter: {key}")
    source_table = (ROOT / str(parameters["source_table"])).resolve()
    if not source_table.exists():
        raise FileNotFoundError(source_table)
    expected_hash = str(parameters.get("source_table_sha256", "")).strip()
    actual_hash = sha256_file(source_table)
    if expected_hash and expected_hash != actual_hash:
        raise ValueError("source_table_sha256 does not match source_table")

    l_column = str(parameters["l_column"])
    value_column = str(parameters["value_column"])
    rows = read_csv_table(source_table)
    if len(rows) != 3000:
        raise ValueError(f"tabulated_parent_source requires exactly 3000 rows, got {len(rows)}")
    l_values = np.array([float(row[l_column]) for row in rows], dtype=float)
    if not np.allclose(l_values, EXPECTED_L, rtol=0.0, atol=0.0):
        raise ValueError("tabulated_parent_source L column must be exactly 10..3009")
    values = np.array([float(row[value_column]) for row in rows], dtype=float)
    if not np.all(np.isfinite(values)):
        raise ValueError("tabulated_parent_source produced non-finite values")
    return values, {
        "source_table": rel(source_table),
        "source_table_sha256": actual_hash,
        "l_column": l_column,
        "value_column": value_column,
    }


def evaluate_formula(formula_family: str, parameters: dict[str, Any]) -> tuple[np.ndarray, dict[str, Any]]:
    if formula_family == "power_law_cutoff_parent_source_v01":
        return power_law_cutoff_parent_source(parameters), {}
    if formula_family == "tabulated_parent_source_v01":
        return tabulated_parent_source(parameters)
    raise ValueError(f"unsupported formula_family: {formula_family}")


def materialize(spec_path: Path, write_staging: bool) -> dict[str, Any]:
    spec = json.loads(spec_path.read_text())
    if not isinstance(spec, dict):
        raise ValueError("parent-source formula spec must be a JSON object")
    reject_template_or_forbidden(spec)

    formula_family = require_string(spec, "formula_family")
    endpoint_blind_statement = require_string(spec, "endpoint_blind_statement")
    parameter_policy = require_string(spec, "parameter_policy")
    normalization_statement = require_string(spec, "normalization_statement")
    known_limit_statement = require_string(spec, "known_limit_statement")
    derivation = require_string(spec, "derivation_script_or_formula")
    source_chain = require_source_chain(spec)
    parameters = spec.get("parameters")
    if not isinstance(parameters, dict):
        raise ValueError("parent-source formula spec requires object field: parameters")
    normalization = float(spec.get("normalization", 1.0))
    if not np.isfinite(normalization):
        raise ValueError("normalization must be finite")

    values, formula_metadata = evaluate_formula(formula_family, parameters)
    report: dict[str, Any] = {
        "report_id": "cmb_tau_lensing_route_b_parent_source_formula_materialization_v01",
        "claim_boundary": "route_b_parent_source_formula_materialization_only_no_grid_no_score_no_dark_sector_verdict",
        "spec_file": rel(spec_path),
        "spec_sha256": sha256_file(spec_path),
        "formula_family": formula_family,
        "formula_role": spec.get("formula_role", ""),
        "endpoint_blind_statement": endpoint_blind_statement,
        "parameter_policy": parameter_policy,
        "source_chain": source_chain,
        "normalization": normalization,
        "normalization_statement": normalization_statement,
        "known_limit_statement": known_limit_statement,
        "derivation_script_or_formula": derivation,
        "formula_metadata": formula_metadata,
        "parent_source_shape": [3000],
        "index_alignment": {"grid_index": "0..2999", "L": "10+i", "explicit_L_column_written": True},
        "parent_source_value_sha256_le_float64": sha256_array(values),
        "finite_values": bool(np.all(np.isfinite(values))),
        "nonzero_count": int(np.count_nonzero(values)),
        "min_value": float(np.min(values)),
        "max_value": float(np.max(values)),
        "mean_value": float(np.mean(values)),
        "parent_source_table": rel(DEFAULT_TABLE),
        "parent_source_config": rel(DEFAULT_CONFIG),
        "staging_written": False,
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
        "created_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "next_required_action": "run_make_tau-grid-route-b-parent-table-precheck_then_parent_write_staging",
    }

    if write_staging:
        DEFAULT_TABLE.parent.mkdir(parents=True, exist_ok=True)
        with DEFAULT_TABLE.open("w", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["L", "parent_tau_source_value"])
            for ell, value in zip(EXPECTED_L.astype(int), values):
                writer.writerow([int(ell), format(float(value), ".17e")])
        config = {
            "config_id": "tau_lensing_route_b_parent_source_config_v01",
            "selected_route": "delta_PP_tau_against_named_fiducial_PP",
            "response_rule": "linear_parent_source_v01",
            "parent_source_table": rel(DEFAULT_TABLE),
            "parent_l_column": "L",
            "parent_value_column": "parent_tau_source_value",
            "normalization": normalization,
            "endpoint_blind_statement": endpoint_blind_statement,
            "parameter_policy": parameter_policy,
            "source_chain": [*source_chain, rel(spec_path)],
            "normalization_statement": normalization_statement,
            "known_limit_statement": known_limit_statement,
            "claim_boundary": "route_b_parent_source_config_from_formula_spec_no_grid_no_score_no_dark_sector_verdict",
        }
        DEFAULT_CONFIG.write_text(json.dumps(config, indent=2, sort_keys=True) + "\n")
        report["staging_written"] = True
        report["parent_source_table_sha256"] = sha256_file(DEFAULT_TABLE)
        report["parent_source_config_sha256"] = sha256_file(DEFAULT_CONFIG)

    return report


def write_template(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(template_spec(), indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Materialize a Route B Tau parent-source L table from a predeclared formula spec."
    )
    parser.add_argument("spec", nargs="?", help="Parent-source formula spec JSON path.")
    parser.add_argument("--write-template", nargs="?", const=str(DEFAULT_TEMPLATE))
    parser.add_argument("--write-staging", action="store_true")
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    args = parser.parse_args()

    if args.write_template:
        write_template(Path(args.write_template))
        print(json.dumps({"template_written": str(Path(args.write_template).resolve())}, indent=2, sort_keys=True))
        return
    if not args.spec:
        raise SystemExit("spec path is required unless --write-template is used")

    report = materialize(Path(args.spec).resolve(), args.write_staging)
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
