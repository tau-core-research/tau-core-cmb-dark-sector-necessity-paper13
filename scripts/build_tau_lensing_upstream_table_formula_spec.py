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
DEFAULT_TEMPLATE = ROOT / "payload_templates/tau_lensing_upstream_l_response_TABLE_TEMPLATE_v01.csv"
DEFAULT_METADATA_TEMPLATE = ROOT / "payload_templates/tau_lensing_upstream_l_response_METADATA_TEMPLATE_v01.json"
DEFAULT_SPEC = ROOT / "payload_staging/tau_lensing_grid_formula_spec_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_upstream_table_formula_spec_report_v01.json"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def validate_table(path: Path, l_column: str, value_column: str) -> tuple[np.ndarray, np.ndarray]:
    rows = read_rows(path)
    if len(rows) != 3000:
        raise ValueError(f"upstream Tau response table requires exactly 3000 rows, got {len(rows)}")
    l_values = np.array([float(row[l_column]) for row in rows], dtype=float)
    values = np.array([float(row[value_column]) for row in rows], dtype=float)
    if not np.allclose(l_values, EXPECTED_L, rtol=0.0, atol=0.0):
        raise ValueError("upstream Tau response table L column must be exactly 10..3009")
    if not np.all(np.isfinite(values)):
        raise ValueError("upstream Tau response table contains non-finite response values")
    return l_values, values


def require_text(value: str, field: str) -> str:
    if not value.strip():
        raise ValueError(f"{field} must be non-empty")
    return value.strip()


def load_metadata(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    metadata_path = Path(path).resolve()
    if not metadata_path.exists():
        raise FileNotFoundError(metadata_path)
    metadata = json.loads(metadata_path.read_text())
    if metadata.get("template_status") == "TEMPLATE_NOT_PAYLOAD":
        raise ValueError("metadata is still marked TEMPLATE_NOT_PAYLOAD")
    if not isinstance(metadata, dict):
        raise ValueError("metadata file must contain a JSON object")
    return metadata


def metadata_or_arg(metadata: dict[str, Any], args: argparse.Namespace, key: str, arg_name: str) -> Any:
    if key in metadata and metadata[key] not in (None, "", []):
        return metadata[key]
    value = getattr(args, arg_name)
    if value not in (None, "", []):
        return value
    return value


def build_spec(args: argparse.Namespace) -> dict[str, Any]:
    metadata = load_metadata(args.metadata)
    table = Path(args.table).resolve()
    if not table.exists():
        raise FileNotFoundError(table)
    l_column = metadata_or_arg(metadata, args, "l_column", "l_column")
    value_column = metadata_or_arg(metadata, args, "value_column", "value_column")
    route = metadata_or_arg(metadata, args, "selected_route", "route")
    formula_role = metadata_or_arg(metadata, args, "formula_role", "formula_role")
    parameter_policy = metadata_or_arg(metadata, args, "parameter_policy", "parameter_policy")
    endpoint_blind_statement = metadata_or_arg(
        metadata, args, "endpoint_blind_statement", "endpoint_blind_statement"
    )
    normalization_statement = metadata_or_arg(metadata, args, "normalization_statement", "normalization_statement")
    known_limit_statement = metadata_or_arg(metadata, args, "known_limit_statement", "known_limit_statement")
    derivation_script_or_formula = metadata_or_arg(
        metadata, args, "derivation_script_or_formula", "derivation_script_or_formula"
    )

    _, values = validate_table(table, l_column, value_column)
    table_hash = sha256_file(table)
    metadata_source_chain = metadata.get("source_chain", [])
    if not isinstance(metadata_source_chain, list):
        raise ValueError("metadata source_chain must be a list when supplied")
    source_chain = [item.strip() for item in [*metadata_source_chain, *args.source_chain] if item.strip()]
    if not source_chain:
        raise ValueError("--source-chain must be supplied at least once")
    if rel(table) not in source_chain:
        source_chain.append(rel(table))

    return {
        "spec_id": "tau_lensing_grid_formula_spec_v01",
        "claim_boundary": "tabulated_tau_response_to_grid_spec_only_no_score_no_dark_sector_verdict",
        "selected_route": route,
        "endpoint_blind_statement": require_text(endpoint_blind_statement, "endpoint_blind_statement"),
        "parameter_policy": require_text(parameter_policy, "parameter_policy"),
        "source_chain": source_chain,
        "formula_family": "tabulated_l_response_v01",
        "formula_role": formula_role,
        "parameters": {
            "source_table": rel(table),
            "l_column": l_column,
            "value_column": value_column,
            "source_table_sha256": table_hash,
        },
        "normalization_statement": require_text(normalization_statement, "normalization_statement"),
        "known_limit_statement": require_text(known_limit_statement, "known_limit_statement"),
        "derivation_script_or_formula": require_text(derivation_script_or_formula, "derivation_script_or_formula"),
        "upstream_table_stats": {
            "rows": 3000,
            "min_value": float(np.min(values)),
            "max_value": float(np.max(values)),
            "mean_value": float(np.mean(values)),
        },
    }


def build_report(spec: dict[str, Any], write_spec: bool, output_spec: Path) -> dict[str, Any]:
    return {
        "report_id": "cmb_tau_lensing_upstream_table_formula_spec_report_v01",
        "claim_boundary": "tabulated_tau_response_to_grid_spec_only_no_score_no_dark_sector_verdict",
        "formula_spec": rel(output_spec),
        "formula_spec_written": write_spec,
        "selected_route": spec["selected_route"],
        "formula_family": spec["formula_family"],
        "source_table": spec["parameters"]["source_table"],
        "source_table_sha256": spec["parameters"]["source_table_sha256"],
        "l_column": spec["parameters"]["l_column"],
        "value_column": spec["parameters"]["value_column"],
        "upstream_table_stats": spec["upstream_table_stats"],
        "materialization_command": "make tau-grid-from-formula",
        "score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": "run_make_tau-grid-from-formula_then_guarded_staging_promotion_dry_run",
    }


def write_template(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["L", "tau_response_value"])
        writer.writerow(["# TEMPLATE_NOT_PAYLOAD", "fill exactly L=10..3009 before use"])


def write_metadata_template(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "template_status": "TEMPLATE_NOT_PAYLOAD",
        "selected_route": "direct_tau_PP_grid",
        "l_column": "L",
        "value_column": "tau_response_value",
        "formula_role": "endpoint_blind_tabulated_tau_lensing_response",
        "endpoint_blind_statement": "",
        "parameter_policy": "parameters_fixed_before_ACT_or_Planck_residual_score_readout",
        "source_chain": [
            "Tau-side derivation script path",
            "Tau-side parent evidence artifact path",
        ],
        "normalization_statement": "",
        "known_limit_statement": "",
        "derivation_script_or_formula": "",
        "notes": "Remove template_status only after all fields describe endpoint-blind Tau-side evidence.",
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate an upstream Tau L-response table and build a tabulated_l_response_v01 formula spec."
    )
    parser.add_argument("--write-template", nargs="?", const=str(DEFAULT_TEMPLATE))
    parser.add_argument("--write-metadata-template", nargs="?", const=str(DEFAULT_METADATA_TEMPLATE))
    parser.add_argument("--table", help="Endpoint-blind upstream Tau L,response table.")
    parser.add_argument("--metadata", help="JSON sidecar with endpoint-blind provenance and formula-spec fields.")
    parser.add_argument("--route", choices=["direct_tau_PP_grid", "delta_PP_tau_against_named_fiducial_PP"], default="direct_tau_PP_grid")
    parser.add_argument("--l-column", default="L")
    parser.add_argument("--value-column", default="tau_response_value")
    parser.add_argument("--source-chain", action="append", default=[])
    parser.add_argument("--endpoint-blind-statement", default="")
    parser.add_argument("--parameter-policy", default="parameters_fixed_before_ACT_or_Planck_residual_score_readout")
    parser.add_argument("--formula-role", default="endpoint_blind_tabulated_tau_lensing_response")
    parser.add_argument("--normalization-statement", default="")
    parser.add_argument("--known-limit-statement", default="")
    parser.add_argument("--derivation-script-or-formula", default="")
    parser.add_argument("--write-spec", nargs="?", const=str(DEFAULT_SPEC))
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    args = parser.parse_args()

    if args.write_template:
        write_template(Path(args.write_template))
        print(json.dumps({"template_written": str(Path(args.write_template).resolve())}, indent=2, sort_keys=True))
        return
    if args.write_metadata_template:
        write_metadata_template(Path(args.write_metadata_template))
        print(
            json.dumps(
                {"metadata_template_written": str(Path(args.write_metadata_template).resolve())},
                indent=2,
                sort_keys=True,
            )
        )
        return
    if not args.table:
        raise SystemExit("--table is required unless --write-template is used")

    spec = build_spec(args)
    output_spec = Path(args.write_spec or DEFAULT_SPEC).resolve()
    report = build_report(spec, bool(args.write_spec), output_spec)
    if args.write_spec:
        output_spec.parent.mkdir(parents=True, exist_ok=True)
        output_spec.write_text(json.dumps(spec, indent=2, sort_keys=True) + "\n")
    if args.write_report:
        report_path = Path(args.write_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
