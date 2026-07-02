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
INTAKE = ROOT / "scripts/intake_tau_lensing_route_evidence.py"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_route_evidence_firewall_report_v01.json"

ROUTE_DECLARATION = ROOT / "payloads/tau_lensing_response_grid_route_declaration_v01.md"
PROVENANCE = ROOT / "payloads/tau_lensing_response_grid_provenance_v01.json"
FIDUCIAL = ROOT / "payloads/tau_lensing_response_fiducial_pp_reference_v01.json"
FAILURE = ROOT / "payloads/tau_lensing_response_grid_failure_statement_v01.md"

FORBIDDEN_MARKERS = [
    "TEMPLATE_NOT_PAYLOAD",
    "ACT residuals",
    "Planck residuals",
    "reduced chi2",
    "dark-sector verdict preference",
]


def is_empty_value(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, (list, dict)):
        return len(value) == 0
    return False


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def run_intake() -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(INTAKE)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return json.loads(completed.stdout)


def text_file_checks(path: Path, required_fragments: list[str]) -> dict[str, Any]:
    text = path.read_text(errors="ignore")
    inspected_text = "\n".join(
        line for line in text.splitlines() if not line.startswith("endpoint_blind_statement:")
    )
    forbidden_found = [marker for marker in FORBIDDEN_MARKERS if marker in inspected_text]
    missing_required = [fragment for fragment in required_fragments if fragment not in text]
    return {
        "file": rel(path),
        "forbidden_markers_found": forbidden_found,
        "missing_required_fragments": missing_required,
        "passes": not forbidden_found and not missing_required,
    }


def text_key_value_checks(path: Path, required_keys: list[str]) -> dict[str, Any]:
    text = path.read_text(errors="ignore")
    forbidden_found = [marker for marker in FORBIDDEN_MARKERS if marker in text]
    values: dict[str, str] = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip()
    missing_required_keys = [key for key in required_keys if key not in values]
    empty_required_keys = [key for key in required_keys if key in values and values[key] == ""]
    return {
        "file": rel(path),
        "forbidden_markers_found": forbidden_found,
        "missing_required_keys": missing_required_keys,
        "empty_required_keys": empty_required_keys,
        "passes": not forbidden_found and not missing_required_keys and not empty_required_keys,
    }


def json_file_checks(
    path: Path,
    required_keys: list[str] | None = None,
    expected_values: dict[str, str] | None = None,
    expected_file_hashes: dict[str, Path] | None = None,
) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        return {
            "file": rel(path),
            "json_parse_ok": False,
            "error": str(exc),
            "passes": False,
        }
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
    forbidden_found = [marker for marker in FORBIDDEN_MARKERS if marker in inspected_text]
    required_keys = required_keys or []
    expected_values = expected_values or {}
    expected_file_hashes = expected_file_hashes or {}
    missing_required_keys = [key for key in required_keys if key not in data]
    empty_required_keys = [key for key in required_keys if key in data and is_empty_value(data[key])]
    mismatched_expected_values = {
        key: {"expected": expected, "actual": data.get(key)}
        for key, expected in expected_values.items()
        if data.get(key) != expected
    }
    mismatched_file_hashes: dict[str, dict[str, str]] = {}
    missing_hash_files: dict[str, str] = {}
    for key, file_path in expected_file_hashes.items():
        if key not in data:
            continue
        if not file_path.exists():
            missing_hash_files[key] = rel(file_path)
            continue
        expected_hash = sha256_file(file_path)
        if data.get(key) != expected_hash:
            mismatched_file_hashes[key] = {"expected": expected_hash, "actual": data.get(key)}
    return {
        "file": rel(path),
        "json_parse_ok": True,
        "top_level_type": type(data).__name__,
        "forbidden_markers_found": forbidden_found,
        "missing_required_keys": missing_required_keys,
        "empty_required_keys": empty_required_keys,
        "mismatched_expected_values": mismatched_expected_values,
        "missing_hash_files": missing_hash_files,
        "mismatched_file_hashes": mismatched_file_hashes,
        "passes": (
            not forbidden_found
            and not missing_required_keys
            and not empty_required_keys
            and not mismatched_expected_values
            and not missing_hash_files
            and not mismatched_file_hashes
        ),
    }


def blocked_report(intake: dict[str, Any]) -> dict[str, Any]:
    return {
        "report_id": "tau_lensing_route_evidence_firewall_blocked_v01",
        "claim_boundary": "route_evidence_firewall_only_no_grid_validation_no_score_no_dark_sector_verdict",
        "firewall_passed": False,
        "score_run": False,
        "dark_sector_verdict": False,
        "blocking_intake": intake,
        "next_required_action": intake.get("next_required_action"),
    }


def build_report() -> dict[str, Any]:
    intake = run_intake()
    selected = intake.get("selected_routes", [])
    if intake.get("intake_decision") != "ONE_ROUTE_ACCEPTED_FOR_NEXT_VALIDATION" or len(selected) != 1:
        return blocked_report(intake)

    route = selected[0]
    checks: list[dict[str, Any]] = []
    if route == "direct_tau_PP_grid":
        checks.append(
            text_file_checks(
                ROUTE_DECLARATION,
                [
                    "selected_route:",
                    "direct_tau_PP_grid",
                    "numeric_grid_file: payloads/tau_lensing_response_pp_grid_v01.csv",
                    "fiducial_reference_file: not_used",
                    "provenance_file: payloads/tau_lensing_response_grid_provenance_v01.json",
                    "index_alignment: L = 10 + i",
                ],
            )
        )
        checks.append(
            json_file_checks(
                PROVENANCE,
                [
                    "selected_route",
                    "numeric_grid_file",
                    "numeric_grid_sha256",
                    "source_chain",
                    "derivation_script_or_formula",
                    "no_endpoint_fit_statement",
                ],
                {
                    "selected_route": "direct_tau_PP_grid",
                    "numeric_grid_file": "payloads/tau_lensing_response_pp_grid_v01.csv",
                },
                {"numeric_grid_sha256": ROOT / "payloads/tau_lensing_response_pp_grid_v01.csv"},
            )
        )
    elif route == "delta_PP_tau_against_named_fiducial_PP":
        checks.append(
            text_file_checks(
                ROUTE_DECLARATION,
                [
                    "selected_route:",
                    "delta_PP_tau_against_named_fiducial_PP",
                    "numeric_grid_file: payloads/tau_lensing_response_delta_pp_v01.csv",
                    "fiducial_reference_file: payloads/tau_lensing_response_fiducial_pp_reference_v01.json",
                    "provenance_file: payloads/tau_lensing_response_grid_provenance_v01.json",
                    "index_alignment: L = 10 + i",
                ],
            )
        )
        checks.append(
            json_file_checks(
                PROVENANCE,
                [
                    "selected_route",
                    "numeric_grid_file",
                    "numeric_grid_sha256",
                    "source_chain",
                    "derivation_script_or_formula",
                    "no_endpoint_fit_statement",
                ],
                {
                    "selected_route": "delta_PP_tau_against_named_fiducial_PP",
                    "numeric_grid_file": "payloads/tau_lensing_response_delta_pp_v01.csv",
                },
                {"numeric_grid_sha256": ROOT / "payloads/tau_lensing_response_delta_pp_v01.csv"},
            )
        )
        checks.append(
            json_file_checks(
                FIDUCIAL,
                ["fiducial_reference_file", "fiducial_reference_sha256"],
                {"fiducial_reference_file": "payloads/tau_lensing_response_fiducial_pp_reference_v01.json"},
            )
        )
    elif route == "explicit_failure_no_endpoint_blind_grid":
        checks.append(
            text_key_value_checks(
                FAILURE,
                [
                    "selected_route",
                    "failed_required_object",
                    "reason",
                    "missing_parent_input",
                    "missing_derivation_rule",
                    "missing_numeric_kernel",
                    "missing_normalization",
                    "next_theoretical_blocker",
                ],
            )
        )
    else:
        raise ValueError(f"unsupported route: {route}")

    firewall_passed = all(check["passes"] for check in checks)
    return {
        "report_id": "tau_lensing_route_evidence_firewall_v01",
        "claim_boundary": "route_evidence_firewall_only_no_grid_validation_no_score_no_dark_sector_verdict",
        "selected_route": route,
        "firewall_passed": firewall_passed,
        "checks": checks,
        "score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": (
            "run_materialize_replay" if firewall_passed and route != "explicit_failure_no_endpoint_blind_grid"
            else "repair_route_evidence_or_record_failure"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Check route evidence files before projection replay materialization.")
    parser.add_argument(
        "--write-report",
        default=None,
        nargs="?",
        const=str(DEFAULT_REPORT),
        help=f"Optional JSON report path. Defaults to {DEFAULT_REPORT} when passed without a path.",
    )
    args = parser.parse_args()

    report = build_report()
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
