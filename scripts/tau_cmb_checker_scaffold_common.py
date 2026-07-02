#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STAGING_ROOT = ROOT / "payload_staging/tau_cmb_carrier_domain_checker_input_payloads"
OUTPUT_ROOT = ROOT / "data/derived/tau_cmb_checker_scaffold_outputs"

CLAIM_BOUNDARY = (
    "tau_cmb_checker_scaffold_execution_v01_structural_input_validation_only_"
    "no_certificate_pass_no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FORBIDDEN_TRUE_FIREWALL_KEYS = [
    "cmb_endpoint_residuals_used",
    "act_planck_likelihood_used",
    "score_output_used",
    "post_endpoint_tuning_used",
    "dark_sector_verdict_used",
]

DOWNSTREAM_PERMISSION_KEYS = [
    "certificate_pass_allowed",
    "checker_execution_allowed",
    "concrete_R_CMB_allowed",
    "dark_sector_verdict_allowed",
    "domain_acceptance_allowed",
    "likelihood_allowed",
    "score_entry_allowed",
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> tuple[dict[str, Any] | None, str]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), ""
    except Exception as exc:  # pragma: no cover - exact parser text is environment-specific
        return None, str(exc)


def default_output(checker_name: str) -> Path:
    return OUTPUT_ROOT / f"{checker_name}_scaffold_result_v01.json"


def default_hash_output(checker_name: str) -> Path:
    return OUTPUT_ROOT / f"{checker_name}_scaffold_result_v01.hashes.json"


def validate_payloads(
    certificate_area: str,
    checker_name: str,
    required_files: list[str],
    input_dir: Path,
) -> dict[str, Any]:
    file_rows: list[dict[str, Any]] = []
    missing: list[str] = []
    malformed: list[str] = []
    metadata_failures: list[str] = []
    firewall_failures: list[str] = []
    permission_failures: list[str] = []
    claim_failures: list[str] = []

    for name in required_files:
        path = input_dir / name
        if not path.exists():
            missing.append(name)
            file_rows.append({"path": rel(path), "exists": False})
            continue
        payload, error = read_json(path)
        if payload is None:
            malformed.append(name)
            file_rows.append({"path": rel(path), "exists": True, "json_valid": False, "error": error})
            continue

        area_ok = payload.get("certificate_area") == certificate_area
        checker_ok = payload.get("checker_name") == checker_name
        if not area_ok or not checker_ok:
            metadata_failures.append(name)

        firewall = payload.get("endpoint_blind_firewall", {})
        firewall_ok = isinstance(firewall, dict) and all(firewall.get(key) is False for key in FORBIDDEN_TRUE_FIREWALL_KEYS)
        if not firewall_ok:
            firewall_failures.append(name)

        permissions = payload.get("acceptance_permissions", {})
        permissions_closed = isinstance(permissions, dict) and all(permissions.get(key) is False for key in DOWNSTREAM_PERMISSION_KEYS)
        if not permissions_closed:
            permission_failures.append(name)

        boundary = str(payload.get("claim_boundary", ""))
        boundary_ok = "no_score" in boundary and "no_likelihood" in boundary and "no_verdict" in boundary
        if not boundary_ok:
            claim_failures.append(name)

        file_rows.append(
            {
                "path": rel(path),
                "exists": True,
                "json_valid": True,
                "sha256": sha256(path),
                "certificate_area_ok": area_ok,
                "checker_name_ok": checker_ok,
                "endpoint_firewall_clean": firewall_ok,
                "downstream_permissions_closed": permissions_closed,
                "claim_boundary_closed": boundary_ok,
            }
        )

    scaffold_checks_passed = not any([missing, malformed, metadata_failures, firewall_failures, permission_failures, claim_failures])
    return {
        "report_id": f"{checker_name}_scaffold_result_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "certificate_area": certificate_area,
        "checker_name": checker_name,
        "input_dir": rel(input_dir),
        "required_files": required_files,
        "file_rows": file_rows,
        "required_file_count": len(required_files),
        "files_seen": sum(1 for row in file_rows if row.get("exists") is True),
        "missing_input_files": missing,
        "malformed_input_files": malformed,
        "metadata_failures": metadata_failures,
        "firewall_failures": firewall_failures,
        "permission_failures": permission_failures,
        "claim_boundary_failures": claim_failures,
        "endpoint_blind_input_validated": len(firewall_failures) == 0 and len(malformed) == 0 and len(missing) == 0,
        "scaffold_checks_passed": scaffold_checks_passed,
        "checker_scaffold_executed": True,
        "execution_succeeded": scaffold_checks_passed,
        "checker_output_supplied": True,
        "certificate_passed": False,
        "domain_object_accepted": False,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CHECKER_SCAFFOLD_EXECUTED_STRUCTURAL_INPUT_CHECKS_PASSED_NOT_CERTIFICATE"
            if scaffold_checks_passed
            else "CHECKER_SCAFFOLD_EXECUTED_STRUCTURAL_INPUT_CHECKS_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_checker_scaffold_output_acceptance_audit_v01",
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_checker(certificate_area: str, checker_name: str, required_files: list[str]) -> int:
    parser = argparse.ArgumentParser(description=f"Run structural scaffold checks for {checker_name}.")
    parser.add_argument("--input-dir", default=str(STAGING_ROOT / certificate_area))
    parser.add_argument("--output", default=str(default_output(checker_name)))
    parser.add_argument("--hash-output", default=str(default_hash_output(checker_name)))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        result = {
            "checker_name": checker_name,
            "certificate_area": certificate_area,
            "required_file_count": len(required_files),
            "claim_boundary": CLAIM_BOUNDARY,
            "self_test_passed": True,
            "certificate_passed": False,
            "score_entry_allowed": False,
            "likelihood_allowed": False,
            "dark_sector_verdict_allowed": False,
            "status": "CHECKER_SCAFFOLD_SELF_TEST_PASSED_NOT_CERTIFICATE",
        }
    else:
        result = validate_payloads(certificate_area, checker_name, required_files, Path(args.input_dir))

    output = Path(args.output)
    write_json(output, result)
    hash_payload = {
        "target": rel(output),
        "sha256": sha256(output),
        "claim_boundary": CLAIM_BOUNDARY,
        "certificate_passed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
    }
    write_json(Path(args.hash_output), hash_payload)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("execution_succeeded", result.get("self_test_passed")) else 2
