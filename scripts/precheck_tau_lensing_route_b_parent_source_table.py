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
DEFAULT_TABLE = ROOT / "payload_staging/tau_lensing_route_b_parent_source_v01.csv"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_route_b_parent_source_precheck_v01.json"

FORBIDDEN_MARKERS = [
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


def text_forbidden(path: Path) -> list[str]:
    text = path.read_text(errors="ignore") if path.exists() else ""
    lowered = text.lower()
    return [marker for marker in FORBIDDEN_MARKERS if marker.lower() in lowered]


def read_parent_table(path: Path, l_column: str, value_column: str) -> tuple[np.ndarray, np.ndarray]:
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 3000:
        raise ValueError(f"expected exactly 3000 rows, got {len(rows)}")
    l_values = np.array([float(row[l_column]) for row in rows], dtype=float)
    values = np.array([float(row[value_column]) for row in rows], dtype=float)
    return l_values, values


def build_report(table: Path, l_column: str, value_column: str, min_abs: float) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    checks.append({"name": "table_exists", "passes": table.exists(), "detail": rel(table)})
    if not table.exists():
        return finalize(checks, None)

    forbidden = text_forbidden(table)
    checks.append({"name": "table_forbidden_markers_absent", "passes": not forbidden, "detail": forbidden})

    try:
        l_values, values = read_parent_table(table, l_column, value_column)
        checks.append({"name": "table_parse", "passes": True})
    except Exception as exc:
        checks.append({"name": "table_parse", "passes": False, "detail": str(exc)})
        return finalize(checks, None)

    l_ok = bool(np.allclose(l_values, EXPECTED_L, rtol=0.0, atol=0.0))
    finite = bool(np.all(np.isfinite(values)))
    nonzero_count = int(np.count_nonzero(np.abs(values) > min_abs))
    checks.append({"name": "l_alignment_10_3009", "passes": l_ok})
    checks.append({"name": "finite_values", "passes": finite})
    checks.append({"name": "nonzero_parent_source_present", "passes": nonzero_count > 0, "detail": {"min_abs": min_abs}})

    stats = {
        "rows": int(values.size),
        "min_value": float(np.min(values)),
        "max_value": float(np.max(values)),
        "mean_value": float(np.mean(values)),
        "max_abs_value": float(np.max(np.abs(values))),
        "nonzero_count_above_min_abs": nonzero_count,
    }
    return finalize(checks, stats)


def finalize(checks: list[dict[str, Any]], stats: dict[str, Any] | None) -> dict[str, Any]:
    precheck_passed = all(check.get("passes") is True for check in checks)
    return {
        "report_id": "cmb_tau_lensing_route_b_parent_source_precheck_v01",
        "claim_boundary": "route_b_parent_source_precheck_only_no_grid_no_score_no_dark_sector_verdict",
        "precheck_passed": precheck_passed,
        "checks": checks,
        "table_stats": stats,
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": (
            "run_route_b_parent_source_materializer_with_non_template_config"
            if precheck_passed
            else "supply_endpoint_blind_tau_derived_parent_source_l_table"
        ),
    }


def write_template(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["L", "parent_tau_source_value"])
        writer.writerow(["# TEMPLATE_NOT_PAYLOAD", "replace with exact integer L=10..3009 and finite values"])
        writer.writerow(["# REQUIRED_ROWS", "3000"])
        writer.writerow(["# CLAIM_BOUNDARY", "route_b_parent_source_table_template_not_payload_no_grid_no_score"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Precheck Route B Tau parent-source L table.")
    parser.add_argument("--table", default=str(DEFAULT_TABLE))
    parser.add_argument("--l-column", default="L")
    parser.add_argument("--value-column", default="parent_tau_source_value")
    parser.add_argument("--min-abs", type=float, default=0.0)
    parser.add_argument("--write-template", nargs="?")
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    args = parser.parse_args()

    if args.write_template is not None:
        template_path = Path(args.write_template or DEFAULT_TABLE).resolve()
        write_template(template_path)
        print(json.dumps({"template_written": rel(template_path)}, indent=2, sort_keys=True))
        return

    report = build_report(Path(args.table).resolve(), args.l_column, args.value_column, args.min_abs)
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
