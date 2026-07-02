#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_L = np.arange(10, 3010, dtype=float)
DEFAULT_TEMPLATE = ROOT / "payload_templates/tau_lensing_route_b_parent_source_CONFIG_TEMPLATE_v01.json"
DEFAULT_TABLE = ROOT / "payload_staging/tau_lensing_upstream_l_response_v01.csv"
DEFAULT_METADATA = ROOT / "payload_staging/tau_lensing_upstream_l_response_metadata_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_route_b_parent_source_materialization_v01.json"

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


def write_template(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "template_status": "TEMPLATE_NOT_PAYLOAD",
        "config_id": "tau_lensing_route_b_parent_source_config_v01",
        "selected_route": "delta_PP_tau_against_named_fiducial_PP",
        "response_rule": "linear_parent_source_v01",
        "parent_source_table": "FILL: endpoint-blind Tau parent source L-table path",
        "parent_l_column": "L",
        "parent_value_column": "parent_tau_source_value",
        "normalization": "FILL: finite numeric multiplier fixed before endpoint score readout",
        "endpoint_blind_statement": "FILL: explain pre-score fixation of parent_tau_source and normalization",
        "parameter_policy": "FILL: no endpoint/score tuning; parameters fixed from Tau-side evidence",
        "source_chain": [
            "FILL: Tau parent source evidence artifact",
            "FILL: parent_source_table generator",
            "FILL: normalization/known-limit audit",
        ],
        "normalization_statement": "FILL: dimensionless delta_PP_tau = normalization * parent_tau_source_value",
        "known_limit_statement": "FILL: delta_PP_tau -> 0 when parent_tau_source_value -> 0",
        "claim_boundary": "route_b_parent_source_config_template_not_payload_no_grid_no_score_no_dark_sector_verdict",
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def reject_template_or_forbidden(config: dict[str, Any]) -> None:
    inspected = {
        key: value
        for key, value in config.items()
        if key
        not in {
            "endpoint_blind_statement",
            "parameter_policy",
            "known_limit_statement",
            "claim_boundary",
        }
    }
    text = json.dumps(inspected, sort_keys=True)
    hits = [marker for marker in FORBIDDEN_TEXT if marker in text]
    if hits:
        raise ValueError(f"Route B parent-source config contains forbidden/template markers: {hits}")


def require_string(config: dict[str, Any], key: str) -> str:
    value = config.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Route B config requires non-empty string field: {key}")
    return value.strip()


def require_source_chain(config: dict[str, Any]) -> list[str]:
    source_chain = config.get("source_chain")
    if not isinstance(source_chain, list) or not source_chain:
        raise ValueError("Route B config requires non-empty source_chain list")
    cleaned = []
    for item in source_chain:
        if not isinstance(item, str) or not item.strip():
            raise ValueError("source_chain entries must be non-empty strings")
        cleaned.append(item.strip())
    return cleaned


def read_parent_table(path: Path, l_column: str, value_column: str) -> np.ndarray:
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 3000:
        raise ValueError(f"parent source table requires exactly 3000 rows, got {len(rows)}")
    l_values = np.array([float(row[l_column]) for row in rows], dtype=float)
    if not np.allclose(l_values, EXPECTED_L, rtol=0.0, atol=0.0):
        raise ValueError("parent source table L column must be exactly 10..3009")
    values = np.array([float(row[value_column]) for row in rows], dtype=float)
    if not np.all(np.isfinite(values)):
        raise ValueError("parent source table contains non-finite values")
    return values


def materialize(config_path: Path, write_staging: bool) -> dict[str, Any]:
    config = json.loads(config_path.read_text())
    if not isinstance(config, dict):
        raise ValueError("Route B config must be a JSON object")
    reject_template_or_forbidden(config)

    response_rule = require_string(config, "response_rule")
    if response_rule != "linear_parent_source_v01":
        raise ValueError(f"unsupported Route B response_rule: {response_rule}")
    parent_table = (ROOT / require_string(config, "parent_source_table")).resolve()
    if not parent_table.exists():
        raise FileNotFoundError(parent_table)
    parent_l_column = require_string(config, "parent_l_column")
    parent_value_column = require_string(config, "parent_value_column")
    normalization = float(config.get("normalization"))
    if not np.isfinite(normalization):
        raise ValueError("normalization must be finite")
    endpoint_blind_statement = require_string(config, "endpoint_blind_statement")
    parameter_policy = require_string(config, "parameter_policy")
    normalization_statement = require_string(config, "normalization_statement")
    known_limit_statement = require_string(config, "known_limit_statement")
    source_chain = require_source_chain(config)

    parent_values = read_parent_table(parent_table, parent_l_column, parent_value_column)
    values = normalization * parent_values
    if not np.all(np.isfinite(values)):
        raise ValueError("Route B materialization produced non-finite values")

    metadata = {
        "selected_route": "delta_PP_tau_against_named_fiducial_PP",
        "l_column": "L",
        "value_column": "tau_response_value",
        "formula_role": "endpoint_blind_tau_derived_lensing_l_response_physical_candidate",
        "route_family": "route_B_direct_L_space",
        "endpoint_blind_statement": endpoint_blind_statement,
        "parameter_policy": parameter_policy,
        "source_chain": [*source_chain, rel(config_path), rel(parent_table)],
        "normalization_statement": normalization_statement,
        "known_limit_statement": known_limit_statement,
        "derivation_script_or_formula": (
            "delta_PP_tau(L) = F_tau_L(parent_tau_source, readout_profile, scale_profile; L); "
            "for response_rule=linear_parent_source_v01, "
            "delta_PP_tau(L)=normalization*parent_tau_source_value(L)"
        ),
        "claim_boundary": "route_b_parent_source_materialization_only_no_score_no_dark_sector_verdict",
        "parent_source_table": rel(parent_table),
        "parent_source_table_sha256": sha256_file(parent_table),
        "normalization": normalization,
    }
    report = {
        "report_id": "cmb_tau_lensing_route_b_parent_source_materialization_v01",
        "claim_boundary": "route_b_parent_source_materialization_only_no_score_no_dark_sector_verdict",
        "materialization_status": "ROUTE_B_PARENT_SOURCE_MATERIALIZED" if write_staging else "DRY_RUN_PASSED",
        "config": rel(config_path),
        "config_sha256": sha256_file(config_path),
        "parent_source_table": rel(parent_table),
        "parent_source_table_sha256": sha256_file(parent_table),
        "response_rule": response_rule,
        "normalization": normalization,
        "rows": int(values.size),
        "min_value": float(np.min(values)),
        "max_value": float(np.max(values)),
        "mean_value": float(np.mean(values)),
        "max_abs_value": float(np.max(np.abs(values))),
        "upstream_table": rel(DEFAULT_TABLE),
        "upstream_metadata": rel(DEFAULT_METADATA),
        "staging_written": False,
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": "run_make_tau-grid-derivation-intake-audit_then_physical_candidate_precheck",
    }
    if write_staging:
        DEFAULT_TABLE.parent.mkdir(parents=True, exist_ok=True)
        with DEFAULT_TABLE.open("w", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["L", "tau_response_value"])
            for ell, value in zip(EXPECTED_L.astype(int), values):
                writer.writerow([int(ell), format(float(value), ".17e")])
        DEFAULT_METADATA.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
        report["staging_written"] = True
        report["upstream_table_sha256"] = sha256_file(DEFAULT_TABLE)
        report["upstream_metadata_sha256"] = sha256_file(DEFAULT_METADATA)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize Route B upstream response from a Tau parent source table.")
    parser.add_argument("config", nargs="?", help="Route B parent-source config JSON.")
    parser.add_argument("--write-template", nargs="?", const=str(DEFAULT_TEMPLATE))
    parser.add_argument("--write-staging", action="store_true")
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    args = parser.parse_args()

    if args.write_template:
        write_template(Path(args.write_template))
        print(json.dumps({"template_written": str(Path(args.write_template).resolve())}, indent=2, sort_keys=True))
        return
    if not args.config:
        raise SystemExit("config path is required unless --write-template is used")

    report = materialize(Path(args.config).resolve(), args.write_staging)
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.write_report:
        report_path = Path(args.write_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
