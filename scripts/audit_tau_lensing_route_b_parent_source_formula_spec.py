#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SPEC = ROOT / "payload_staging/tau_lensing_route_b_parent_source_formula_spec_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_route_b_parent_source_formula_spec_audit_v01.json"

REQUIRED_FIELDS = [
    "spec_id",
    "formula_family",
    "formula_role",
    "parameters",
    "normalization",
    "endpoint_blind_statement",
    "parameter_policy",
    "source_chain",
    "normalization_statement",
    "known_limit_statement",
    "derivation_script_or_formula",
    "claim_boundary",
]

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

REQUIRED_ENDPOINT_TERMS = [
    "before endpoint",
    "before score",
    "endpoint-blind",
]

REQUIRED_POLICY_EXCLUSIONS = [
    "residual",
    "score",
    "tuning",
]


def rel(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def text_hits(text: str, markers: list[str]) -> list[str]:
    lowered = text.lower()
    return [marker for marker in markers if marker.lower() in lowered]


def forbidden_evidence_hits(spec: dict[str, Any]) -> list[str]:
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
    return text_hits(json.dumps(inspected, sort_keys=True), FORBIDDEN_MARKERS)


def source_chain_status(spec: dict[str, Any]) -> tuple[bool, list[dict[str, Any]]]:
    source_chain = spec.get("source_chain")
    if not isinstance(source_chain, list) or not source_chain:
        return False, []
    rows: list[dict[str, Any]] = []
    all_ok = True
    for item in source_chain:
        if not isinstance(item, str) or not item.strip():
            rows.append({"source": item, "exists": False, "reason": "not_a_nonempty_string"})
            all_ok = False
            continue
        candidate = (ROOT / item).resolve()
        exists = candidate.exists()
        rows.append({"source": item, "exists": exists})
        if not exists:
            all_ok = False
    return all_ok, rows


def numeric_parameter_status(spec: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    parameters = spec.get("parameters")
    if not isinstance(parameters, dict):
        return False, {"reason": "parameters_not_object"}
    numeric_values: dict[str, float] = {}
    for key, value in parameters.items():
        if value is None:
            continue
        try:
            number = float(value)
        except (TypeError, ValueError):
            return False, {"reason": "non_numeric_parameter", "key": key, "value": value}
        if not math.isfinite(number):
            return False, {"reason": "non_finite_parameter", "key": key, "value": value}
        numeric_values[key] = number
    try:
        normalization = float(spec.get("normalization"))
    except (TypeError, ValueError):
        return False, {"reason": "normalization_not_numeric"}
    if not math.isfinite(normalization):
        return False, {"reason": "normalization_not_finite"}
    nonzero_amplitude = abs(float(parameters.get("amplitude", 0.0))) > 0.0
    return nonzero_amplitude, {
        "numeric_parameters": numeric_values,
        "normalization": normalization,
        "nonzero_amplitude": nonzero_amplitude,
    }


def build_report(spec_path: Path) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    checks.append({"name": "spec_exists", "passes": spec_path.exists(), "detail": rel(spec_path)})
    spec = load_json(spec_path)
    checks.append({"name": "spec_valid_json_object", "passes": spec is not None})
    if spec is None:
        return finalize(checks, None)

    forbidden = forbidden_evidence_hits(spec)
    checks.append({"name": "forbidden_markers_absent", "passes": not forbidden, "detail": forbidden})

    missing_fields = [field for field in REQUIRED_FIELDS if field not in spec]
    checks.append({"name": "required_fields_present", "passes": not missing_fields, "detail": missing_fields})

    formula_family = spec.get("formula_family")
    checks.append(
        {
            "name": "formula_family_supported",
            "passes": formula_family
            in {"power_law_cutoff_parent_source_v01", "tabulated_parent_source_v01"},
            "detail": formula_family,
        }
    )

    endpoint_text = str(spec.get("endpoint_blind_statement", ""))
    endpoint_hits = text_hits(endpoint_text, REQUIRED_ENDPOINT_TERMS)
    checks.append(
        {
            "name": "endpoint_blind_statement_declares_pre_score_fixation",
            "passes": bool(endpoint_hits),
            "detail": endpoint_hits,
        }
    )

    policy_text = str(spec.get("parameter_policy", ""))
    policy_hits = text_hits(policy_text, REQUIRED_POLICY_EXCLUSIONS)
    checks.append(
        {
            "name": "parameter_policy_excludes_endpoint_tuning",
            "passes": len(policy_hits) >= 3,
            "detail": policy_hits,
        }
    )

    known_limit_text = str(spec.get("known_limit_statement", "")).lower()
    checks.append(
        {
            "name": "known_limit_declares_zero_parent_zero_response",
            "passes": "0" in known_limit_text and "delta_pp_tau" in known_limit_text,
            "detail": spec.get("known_limit_statement"),
        }
    )

    source_ok, source_rows = source_chain_status(spec)
    checks.append({"name": "source_chain_paths_exist", "passes": source_ok, "detail": source_rows})

    numeric_ok, numeric_detail = numeric_parameter_status(spec)
    checks.append({"name": "numeric_parameters_finite_and_nonzero", "passes": numeric_ok, "detail": numeric_detail})

    proof_status = {
        "spec_file": rel(spec_path),
        "formula_family": formula_family,
        "formula_role": spec.get("formula_role"),
        "source_chain": spec.get("source_chain"),
        "critical_claim_boundary": (
            "audit proves protocol eligibility only; it does not prove that the "
            "formula is a correct physical Tau response"
        ),
    }
    return finalize(checks, proof_status)


def finalize(checks: list[dict[str, Any]], proof_status: dict[str, Any] | None) -> dict[str, Any]:
    audit_passed = all(check.get("passes") is True for check in checks)
    return {
        "report_id": "cmb_tau_lensing_route_b_parent_source_formula_spec_audit_v01",
        "claim_boundary": "route_b_parent_source_formula_spec_audit_only_no_grid_no_score_no_dark_sector_verdict",
        "audit_passed": audit_passed,
        "formula_spec_protocol_eligible": audit_passed,
        "checks": checks,
        "proof_status": proof_status,
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": (
            "run_make_tau-grid-route-b-parent-from-formula-dry-run"
            if audit_passed
            else "supply_endpoint_blind_tau_derived_formula_spec_with_existing_source_chain_evidence"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Route B parent-source formula spec eligibility.")
    parser.add_argument("--spec", default=str(DEFAULT_SPEC))
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    args = parser.parse_args()

    report = build_report(Path(args.spec).resolve())
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
