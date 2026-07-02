#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_L = np.arange(10, 3010, dtype=float)
DEFAULT_TABLE = ROOT / "payload_staging/tau_lensing_upstream_l_response_v01.csv"
DEFAULT_METADATA = ROOT / "payload_staging/tau_lensing_upstream_l_response_metadata_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_physical_candidate_upstream_precheck_v01.json"

FORBIDDEN_MARKERS = [
    "TEMPLATE_NOT_PAYLOAD",
    "FILL:",
    "physical_candidate_upstream_scaffold_template_not_payload",
    "ACT residuals",
    "Planck residuals",
    "reduced chi2",
    "dark-sector verdict preference",
]

FORBIDDEN_CLASS_WORDS = [
    "control",
    "identically zero",
    "null-control",
    "probe",
    "diagnostic",
    "not a physical tau response",
    "not a tau-derived physical response",
]

REQUIRED_PHYSICAL_MARKERS = [
    "tau-derived",
    "endpoint-blind",
    "normalization",
    "known-limit",
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_table(path: Path, l_column: str, value_column: str) -> tuple[np.ndarray, np.ndarray]:
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 3000:
        raise ValueError(f"expected exactly 3000 rows, got {len(rows)}")
    l_values = np.array([float(row[l_column]) for row in rows], dtype=float)
    values = np.array([float(row[value_column]) for row in rows], dtype=float)
    return l_values, values


def load_metadata(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError("metadata must be a JSON object")
    return data


def text_forbidden(path: Path) -> list[str]:
    text = path.read_text(errors="ignore") if path.exists() else ""
    return [marker for marker in FORBIDDEN_MARKERS if marker in text]


def metadata_forbidden(metadata: dict[str, Any]) -> list[str]:
    inspected = {
        key: value
        for key, value in metadata.items()
        if key
        not in {
            "endpoint_blind_statement",
            "parameter_policy",
            "known_limit_statement",
            "claim_boundary",
        }
    }
    text = json.dumps(inspected, sort_keys=True)
    return [marker for marker in FORBIDDEN_MARKERS if marker in text]


def metadata_text(metadata: dict[str, Any]) -> str:
    keys = [
        "formula_role",
        "endpoint_blind_statement",
        "parameter_policy",
        "normalization_statement",
        "known_limit_statement",
        "derivation_script_or_formula",
        "claim_boundary",
        "notes",
    ]
    source_chain = metadata.get("source_chain", [])
    source_text = " ".join(str(item) for item in source_chain) if isinstance(source_chain, list) else str(source_chain)
    return " ".join([*(str(metadata.get(key, "")) for key in keys), source_text]).lower()


def contains_required_physical_markers(metadata: dict[str, Any]) -> dict[str, bool]:
    text = metadata_text(metadata)
    endpoint_blind_statement = str(metadata.get("endpoint_blind_statement", "")).strip()
    normalization_statement = str(metadata.get("normalization_statement", "")).strip()
    known_limit_statement = str(metadata.get("known_limit_statement", "")).strip()
    checks = {
        "tau-derived": ("tau-derived" in text or "tau derived" in text or "tau-side" in text),
        "endpoint-blind": bool(endpoint_blind_statement)
        and ("endpoint-blind" in text or "endpoint blind" in text or "endpoint_blind" in text),
        "normalization": bool(normalization_statement),
        "known-limit": bool(known_limit_statement),
    }
    return checks


def build_report(table: Path, metadata_path: Path, min_abs: float) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    checks.append({"name": "table_exists", "passes": table.exists(), "detail": rel(table)})
    checks.append({"name": "metadata_exists", "passes": metadata_path.exists(), "detail": rel(metadata_path)})
    if not table.exists() or not metadata_path.exists():
        return finalize(checks, None, None)

    table_forbidden = text_forbidden(table)
    checks.append({"name": "table_forbidden_markers_absent", "passes": not table_forbidden, "detail": table_forbidden})

    try:
        metadata = load_metadata(metadata_path)
        checks.append({"name": "metadata_json_object", "passes": True})
    except (json.JSONDecodeError, ValueError) as exc:
        checks.append({"name": "metadata_json_object", "passes": False, "detail": str(exc)})
        return finalize(checks, None, None)

    metadata_forbidden_hits = metadata_forbidden(metadata)
    checks.append(
        {
            "name": "metadata_forbidden_markers_absent",
            "passes": not metadata_forbidden_hits,
            "detail": metadata_forbidden_hits,
        }
    )

    required_metadata = [
        "selected_route",
        "endpoint_blind_statement",
        "parameter_policy",
        "source_chain",
        "normalization_statement",
        "known_limit_statement",
        "derivation_script_or_formula",
        "claim_boundary",
    ]
    empty_required = [
        key
        for key in required_metadata
        if key not in metadata
        or metadata[key] in ("", None)
        or (isinstance(metadata[key], list) and len(metadata[key]) == 0)
    ]
    checks.append({"name": "metadata_required_fields_nonempty", "passes": not empty_required, "detail": empty_required})

    text = metadata_text(metadata)
    forbidden_class_hits = [word for word in FORBIDDEN_CLASS_WORDS if word in text]
    checks.append(
        {
            "name": "metadata_not_control_or_probe",
            "passes": not forbidden_class_hits,
            "detail": forbidden_class_hits,
        }
    )

    physical_marker_checks = contains_required_physical_markers(metadata)
    missing_markers = [marker for marker, present in physical_marker_checks.items() if not present]
    checks.append(
        {
            "name": "metadata_declares_physical_candidate_basis",
            "passes": not missing_markers,
            "detail": {"missing_markers": missing_markers, "marker_checks": physical_marker_checks},
        }
    )

    l_column = str(metadata.get("l_column", "L"))
    value_column = str(metadata.get("value_column", "tau_response_value"))
    try:
        l_values, values = read_table(table, l_column, value_column)
        checks.append({"name": "table_parse", "passes": True})
    except Exception as exc:
        checks.append({"name": "table_parse", "passes": False, "detail": str(exc)})
        return finalize(checks, metadata, None)

    l_ok = np.allclose(l_values, EXPECTED_L, rtol=0.0, atol=0.0)
    finite = bool(np.all(np.isfinite(values)))
    max_abs = float(np.max(np.abs(values))) if values.size else 0.0
    nonzero_count = int(np.count_nonzero(np.abs(values) > min_abs))
    checks.append({"name": "l_alignment_10_3009", "passes": bool(l_ok)})
    checks.append({"name": "finite_values", "passes": finite})
    checks.append({"name": "nonzero_response_present", "passes": nonzero_count > 0, "detail": {"min_abs": min_abs}})

    stats = {
        "rows": int(values.size),
        "min_value": float(np.min(values)),
        "max_value": float(np.max(values)),
        "mean_value": float(np.mean(values)),
        "max_abs_value": max_abs,
        "nonzero_count_above_min_abs": nonzero_count,
    }
    return finalize(checks, metadata, stats)


def finalize(checks: list[dict[str, Any]], metadata: dict[str, Any] | None, stats: dict[str, Any] | None) -> dict[str, Any]:
    precheck_passed = all(check.get("passes") is True for check in checks)
    return {
        "report_id": "cmb_tau_lensing_physical_candidate_upstream_precheck_v01",
        "claim_boundary": "physical_candidate_upstream_precheck_only_no_grid_promotion_no_score_no_dark_sector_verdict",
        "precheck_passed": precheck_passed,
        "checks": checks,
        "selected_route": metadata.get("selected_route") if metadata else None,
        "table_stats": stats,
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": (
            "run_make_tau-grid-handoff-write-staging_then_physical_candidate_route_package"
            if precheck_passed
            else "replace_control_or_probe_inputs_with_tau_derived_endpoint_blind_response"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Precheck a physical-candidate endpoint-blind Tau upstream L-response table."
    )
    parser.add_argument("--table", default=str(DEFAULT_TABLE))
    parser.add_argument("--metadata", default=str(DEFAULT_METADATA))
    parser.add_argument("--min-abs", type=float, default=0.0)
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    args = parser.parse_args()

    report = build_report(Path(args.table).resolve(), Path(args.metadata).resolve(), args.min_abs)
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.write_report:
        report_path = Path(args.write_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
