#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "payload_staging"
GRID_VALIDATOR = ROOT / "scripts/validate_tau_lensing_grid_payload.py"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_staging_promotion_precheck_v01.json"


ROUTE_FILES = {
    "direct_tau_PP_grid": {
        "grid": "tau_lensing_response_pp_grid_v01.csv",
        "declaration": "tau_lensing_response_grid_route_declaration_v01.md",
        "provenance": "tau_lensing_response_grid_provenance_v01.json",
        "validator_route": "direct_tau_PP_grid",
        "payload_grid_path": "payloads/tau_lensing_response_pp_grid_v01.csv",
    },
    "delta_PP_tau_against_named_fiducial_PP": {
        "grid": "tau_lensing_response_delta_pp_v01.csv",
        "declaration": "tau_lensing_response_grid_route_declaration_v01.md",
        "provenance": "tau_lensing_response_grid_provenance_v01.json",
        "fiducial": "tau_lensing_response_fiducial_pp_reference_v01.json",
        "validator_route": "delta_PP_tau",
        "payload_grid_path": "payloads/tau_lensing_response_delta_pp_v01.csv",
    },
    "explicit_failure_no_endpoint_blind_grid": {
        "failure": "tau_lensing_response_grid_failure_statement_v01.md",
    },
}

FORBIDDEN_MARKERS = [
    "TEMPLATE_NOT_PAYLOAD",
    "ACT residuals",
    "Planck residuals",
    "reduced chi2",
    "dark-sector verdict preference",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_json(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout)


def is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, (list, dict)):
        return len(value) == 0
    return False


def text_markers(path: Path) -> dict[str, Any]:
    text = path.read_text(errors="ignore") if path.exists() else ""
    return {
        "file": rel(path),
        "exists": path.exists(),
        "forbidden_markers_found": [marker for marker in FORBIDDEN_MARKERS if marker in text],
    }


def json_check(path: Path, required_keys: list[str], expected_values: dict[str, str] | None = None) -> dict[str, Any]:
    base = {"file": rel(path), "exists": path.exists(), "forbidden_markers_found": []}
    if not path.exists():
        return {**base, "json_parse_ok": False, "passes": False}
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        return {**base, "json_parse_ok": False, "error": str(exc), "passes": False}
    inspected = {
        key: value
        for key, value in data.items()
        if key
        not in {
            "endpoint_blind_statement",
            "parameter_policy",
            "no_endpoint_fit_statement",
            "known_limit_statement",
            "notes",
        }
    }
    inspected_text = json.dumps(inspected, sort_keys=True)
    base["forbidden_markers_found"] = [marker for marker in FORBIDDEN_MARKERS if marker in inspected_text]
    expected_values = expected_values or {}
    missing = [key for key in required_keys if key not in data]
    empty = [key for key in required_keys if key in data and is_empty(data[key])]
    mismatched = {
        key: {"expected": expected, "actual": data.get(key)}
        for key, expected in expected_values.items()
        if data.get(key) != expected
    }
    return {
        **base,
        "json_parse_ok": True,
        "missing_required_keys": missing,
        "empty_required_keys": empty,
        "mismatched_expected_values": mismatched,
        "passes": (
            base["exists"]
            and not base["forbidden_markers_found"]
            and not missing
            and not empty
            and not mismatched
        ),
    }


def declaration_check(path: Path, required_fragments: list[str]) -> dict[str, Any]:
    text = path.read_text(errors="ignore") if path.exists() else ""
    inspected_text = "\n".join(
        line for line in text.splitlines() if not line.startswith("endpoint_blind_statement:")
    )
    base = {
        "file": rel(path),
        "exists": path.exists(),
        "forbidden_markers_found": [marker for marker in FORBIDDEN_MARKERS if marker in inspected_text],
    }
    missing = [fragment for fragment in required_fragments if fragment not in text]
    endpoint_blind_empty = "endpoint_blind_statement:" in text and "endpoint_blind_statement:\n" in text
    return {
        **base,
        "missing_required_fragments": missing,
        "endpoint_blind_statement_empty": endpoint_blind_empty,
        "passes": base["exists"] and not base["forbidden_markers_found"] and not missing and not endpoint_blind_empty,
    }


def failure_check(path: Path) -> dict[str, Any]:
    required = [
        "selected_route",
        "failed_required_object",
        "reason",
        "missing_parent_input",
        "missing_derivation_rule",
        "missing_numeric_kernel",
        "missing_normalization",
        "next_theoretical_blocker",
    ]
    base = text_markers(path)
    text = path.read_text(errors="ignore") if path.exists() else ""
    values: dict[str, str] = {}
    for line in text.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    missing = [key for key in required if key not in values]
    empty = [key for key in required if key in values and values[key] == ""]
    return {
        **base,
        "missing_required_keys": missing,
        "empty_required_keys": empty,
        "passes": base["exists"] and not base["forbidden_markers_found"] and not missing and not empty,
    }


def grid_check(path: Path, validator_route: str) -> dict[str, Any]:
    base = text_markers(path)
    if not path.exists() or base["forbidden_markers_found"]:
        return {**base, "grid_valid": False, "passes": False}
    try:
        validation = run_json([sys.executable, str(GRID_VALIDATOR), str(path), "--route", validator_route])
    except subprocess.CalledProcessError as exc:
        return {
            **base,
            "grid_valid": False,
            "error": exc.stderr.strip() or exc.stdout.strip(),
            "passes": False,
        }
    return {
        **base,
        "grid_valid": True,
        "grid_sha256": sha256_file(path),
        "grid_shape": validation.get("grid_shape"),
        "explicit_L_column_verified": validation.get("index_alignment", {}).get("explicit_L_column_verified"),
        "passes": True,
    }


def build_precheck(route: str) -> dict[str, Any]:
    spec = ROUTE_FILES[route]
    route_dir = STAGING / route
    checks: list[dict[str, Any]] = []

    if route == "explicit_failure_no_endpoint_blind_grid":
        checks.append(failure_check(route_dir / spec["failure"]))
    else:
        grid_path = route_dir / spec["grid"]
        checks.append(grid_check(grid_path, spec["validator_route"]))
        checks.append(
            declaration_check(
                route_dir / spec["declaration"],
                [
                    f"selected_route: {route}",
                    f"numeric_grid_file: {spec['payload_grid_path']}",
                    "provenance_file: payloads/tau_lensing_response_grid_provenance_v01.json",
                    "index_alignment: L = 10 + i",
                    "endpoint_blind_statement:",
                ],
            )
        )
        checks.append(
            json_check(
                route_dir / spec["provenance"],
                [
                    "selected_route",
                    "numeric_grid_file",
                    "numeric_grid_sha256",
                    "source_chain",
                    "derivation_script_or_formula",
                    "no_endpoint_fit_statement",
                ],
                {
                    "selected_route": route,
                    "numeric_grid_file": spec["payload_grid_path"],
                    "numeric_grid_sha256": sha256_file(grid_path) if grid_path.exists() else "",
                },
            )
        )
        if "fiducial" in spec:
            checks.append(
                json_check(
                    route_dir / spec["fiducial"],
                    ["fiducial_reference_file", "fiducial_reference_sha256"],
                    {"fiducial_reference_file": "payloads/tau_lensing_response_fiducial_pp_reference_v01.json"},
                )
            )

    promotion_ready = all(check.get("passes") is True for check in checks)
    return {
        "report_id": "tau_lensing_staging_promotion_precheck_v01",
        "claim_boundary": "staging_promotion_precheck_only_no_payload_copy_no_score_no_dark_sector_verdict",
        "selected_route": route,
        "staging_directory": rel(route_dir),
        "promotion_ready": promotion_ready,
        "checks": checks,
        "score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": (
            "run_matching_make_staging_promote_command_to_promote_reviewed_payload"
            if promotion_ready
            else "repair_staging_files_before_guarded_payload_promotion"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Precheck staging files before guarded promotion into payloads/.")
    parser.add_argument("--route", choices=sorted(ROUTE_FILES), required=True)
    parser.add_argument(
        "--write-report",
        default=None,
        nargs="?",
        const=str(DEFAULT_REPORT),
        help=f"Optional JSON report path. Defaults to {DEFAULT_REPORT} when passed without a path.",
    )
    args = parser.parse_args()
    report = build_precheck(args.route)
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
