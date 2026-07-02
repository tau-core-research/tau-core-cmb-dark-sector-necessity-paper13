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
DEFAULT_ACT_BINNING = ROOT / "data/external/act_dr6_lensing/extracted/v1.2/binning_matrix_act.txt"
EXPECTED_L = np.arange(10, 3010, dtype=float)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_array(values: np.ndarray) -> str:
    contiguous = np.ascontiguousarray(values.astype("<f8", copy=False))
    return hashlib.sha256(contiguous.tobytes()).hexdigest()


def load_grid(path: Path) -> tuple[np.ndarray, bool]:
    try:
        values = np.loadtxt(path, delimiter=",")
    except ValueError:
        values = np.loadtxt(path)
    values = np.asarray(values, dtype=float)
    if values.ndim == 2 and 1 in values.shape:
        values = values.reshape(-1)
    if values.ndim == 2 and values.shape[1] == 2:
        if values.shape[0] != 3000:
            raise ValueError(f"expected 3000 L,value rows, got {values.shape[0]}")
        if not np.allclose(values[:, 0], EXPECTED_L, rtol=0.0, atol=0.0):
            raise ValueError("two-column grid must use L values exactly 10..3009")
        values = values[:, 1]
        return values, True
    if values.ndim != 1:
        raise ValueError(f"expected one numeric grid column or two-column L,value table, got shape {values.shape}")
    return values, False


def read_template_marker(path: Path) -> bool:
    sample = path.read_text(errors="ignore")[:4096]
    return "TEMPLATE_NOT_PAYLOAD" in sample


def validate_grid(path: Path) -> tuple[np.ndarray, bool]:
    if not path.exists():
        raise FileNotFoundError(path)
    if read_template_marker(path):
        raise ValueError(f"{path} is marked TEMPLATE_NOT_PAYLOAD")
    values, explicit_l_alignment = load_grid(path)
    if values.shape != (3000,):
        raise ValueError(f"expected 3000 finite values, got shape {values.shape}")
    if not np.all(np.isfinite(values)):
        raise ValueError("grid contains non-finite values")
    return values, explicit_l_alignment


def project_grid(values: np.ndarray, binning_path: Path) -> tuple[np.ndarray, str]:
    if not binning_path.exists():
        raise FileNotFoundError(binning_path)
    matrix = np.loadtxt(binning_path)
    if matrix.shape != (18, 3000):
        raise ValueError(f"expected ACT binning shape (18, 3000), got {matrix.shape}")
    projected = matrix @ values
    if projected.shape != (18,):
        raise ValueError(f"expected projected shape (18,), got {projected.shape}")
    if not np.all(np.isfinite(projected)):
        raise ValueError("projected vector contains non-finite values")
    return projected, sha256_file(binning_path)


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    grid_path = Path(args.grid).resolve()
    values, explicit_l_alignment = validate_grid(grid_path)
    report: dict[str, Any] = {
        "report_id": "tau_lensing_grid_payload_validation_v01",
        "claim_boundary": "grid_payload_validation_only_no_tau_score_no_dark_sector_verdict",
        "route_id": args.route,
        "grid_file": str(grid_path),
        "grid_sha256": sha256_file(grid_path),
        "grid_value_sha256_le_float64": sha256_array(values),
        "grid_shape": list(values.shape),
        "index_alignment": {
            "grid_index": "0..2999",
            "L": "10+i",
            "explicit_L_column_verified": explicit_l_alignment,
        },
        "finite_values": bool(np.all(np.isfinite(values))),
        "score_computed": False,
        "dark_sector_verdict": False,
    }
    if args.project:
        projected, binning_sha = project_grid(values, Path(args.act_binning).resolve())
        report.update(
            {
                "projection_replay": {
                    "adapter": "schema_locked_ACT_binning_matrix",
                    "act_binning_file": str(Path(args.act_binning).resolve()),
                    "act_binning_sha256": binning_sha,
                    "operation": "B_ACT @ grid",
                    "projected_shape": list(projected.shape),
                    "projected_vector_sha256_le_float64": sha256_array(projected),
                }
            }
        )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate a Tau CMB lensing PP-grid payload without computing a score."
    )
    parser.add_argument("grid", help="Path to tau_PP_grid or delta_PP_tau numeric CSV/TXT payload.")
    parser.add_argument(
        "--route",
        choices=["direct_tau_PP_grid", "delta_PP_tau"],
        required=True,
        help="Predeclared grid route.",
    )
    parser.add_argument(
        "--project",
        action="store_true",
        help="Replay B_ACT @ grid shape/hash projection without computing score.",
    )
    parser.add_argument(
        "--act-binning",
        default=str(DEFAULT_ACT_BINNING),
        help="ACT binning matrix path for projection replay.",
    )
    parser.add_argument(
        "--write-replay",
        help="Optional path for replay JSON. Only writes validation/projection hashes, not a score.",
    )
    args = parser.parse_args()

    report = build_report(args)
    payload = json.dumps(report, indent=2, sort_keys=True)
    if args.write_replay:
        Path(args.write_replay).write_text(payload + "\n")
    print(payload)


if __name__ == "__main__":
    main()
