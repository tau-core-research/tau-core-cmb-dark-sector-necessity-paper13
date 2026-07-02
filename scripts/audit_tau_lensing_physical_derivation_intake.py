#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_METADATA = ROOT / "payload_staging/tau_lensing_upstream_l_response_metadata_v01.json"
DEFAULT_AUDIT = ROOT / "data/derived/cmb_tau_lensing_physical_derivation_intake_audit_v01.json"

ROUTE_A_MARKERS = [
    "rho_tau_eff",
    "phi_tau_eff",
    "t_tau_cmb",
    "projection_pp",
]
ROUTE_B_MARKERS = [
    "delta_pp_tau",
    "f_tau_l",
    "parent_tau_source",
]
FORBIDDEN_MARKERS = [
    "template_not_payload",
    "fill:",
    "act residual",
    "planck residual",
    "reduced chi2",
    "score output",
    "dark-sector verdict",
    "diagnostic probe",
    "zero-control",
    "not a physical tau response",
]


def rel(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def load_metadata(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def text_blob(metadata: dict[str, Any]) -> str:
    return json.dumps(metadata, sort_keys=True).lower()


def evidence_text_blob(metadata: dict[str, Any]) -> str:
    evidence_keys = [
        "formula_role",
        "source_chain",
        "normalization_statement",
        "derivation_script_or_formula",
        "notes",
    ]
    return json.dumps({key: metadata.get(key) for key in evidence_keys}, sort_keys=True).lower()


def route_marker_status(text: str, markers: list[str]) -> dict[str, bool]:
    return {marker: marker in text for marker in markers}


def build_audit(metadata_path: Path) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    metadata = load_metadata(metadata_path)
    checks.append({"name": "metadata_exists_and_json_object", "passes": metadata is not None, "detail": rel(metadata_path)})
    if metadata is None:
        return finalize(checks, None, None, None)

    text = text_blob(metadata)
    evidence_text = evidence_text_blob(metadata)
    forbidden_hits = [marker for marker in FORBIDDEN_MARKERS if marker in evidence_text]
    checks.append({"name": "forbidden_endpoint_or_placeholder_markers_absent", "passes": not forbidden_hits, "detail": forbidden_hits})

    required_fields = [
        "selected_route",
        "formula_role",
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
        for key in required_fields
        if key not in metadata
        or metadata[key] in ("", None)
        or (isinstance(metadata[key], list) and not metadata[key])
    ]
    checks.append({"name": "required_derivation_metadata_fields_nonempty", "passes": not empty_required, "detail": empty_required})

    source_chain = metadata.get("source_chain", [])
    source_chain_is_list = isinstance(source_chain, list)
    checks.append({"name": "source_chain_is_list", "passes": source_chain_is_list})
    source_chain_has_tau_parent = bool(
        source_chain_is_list
        and any("tau" in str(item).lower() and "parent" in str(item).lower() for item in source_chain)
    )
    checks.append({"name": "source_chain_names_tau_parent_source", "passes": source_chain_has_tau_parent})

    endpoint_blind_text = str(metadata.get("endpoint_blind_statement", "")).lower()
    parameter_policy_text = str(metadata.get("parameter_policy", "")).lower()
    checks.append(
        {
            "name": "endpoint_blind_statement_declares_pre_score_fixation",
            "passes": bool(
                ("endpoint-blind" in endpoint_blind_text or "endpoint blind" in endpoint_blind_text)
                and ("before" in endpoint_blind_text or "pre" in endpoint_blind_text)
            ),
        }
    )
    checks.append(
        {
            "name": "parameter_policy_excludes_endpoint_tuning",
            "passes": bool(
                ("endpoint" in parameter_policy_text or "score" in parameter_policy_text)
                and ("no" in parameter_policy_text or "without" in parameter_policy_text or "exclude" in parameter_policy_text)
            ),
        }
    )

    route_a = route_marker_status(text, ROUTE_A_MARKERS)
    route_b = route_marker_status(text, ROUTE_B_MARKERS)
    route_a_complete = all(route_a.values())
    route_b_complete = all(route_b.values())
    exactly_one_route = bool(route_a_complete ^ route_b_complete)
    checks.append(
        {
            "name": "route_marker_status_recorded",
            "passes": True,
            "detail": {"route_A_complete": route_a_complete, "route_B_complete": route_b_complete},
        }
    )
    checks.append({"name": "exactly_one_physical_route_declared", "passes": exactly_one_route})

    selected_route_family = (
        "route_A_transfer_projection"
        if route_a_complete and not route_b_complete
        else "route_B_direct_L_space"
        if route_b_complete and not route_a_complete
        else "ambiguous_or_incomplete"
    )
    return finalize(checks, metadata, selected_route_family, {"route_A": route_a, "route_B": route_b})


def finalize(
    checks: list[dict[str, Any]],
    metadata: dict[str, Any] | None,
    selected_route_family: str | None,
    marker_status: dict[str, Any] | None,
) -> dict[str, Any]:
    audit_passed = all(check.get("passes") is True for check in checks)
    return {
        "report_id": "cmb_tau_lensing_physical_derivation_intake_audit_v01",
        "claim_boundary": "physical_derivation_intake_audit_only_no_grid_no_score_no_dark_sector_verdict",
        "audit_passed": audit_passed,
        "selected_route": metadata.get("selected_route") if metadata else None,
        "selected_route_family": selected_route_family,
        "marker_status": marker_status,
        "checks": checks,
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": (
            "run_make_tau-grid-physical-candidate-precheck"
            if audit_passed
            else "supply_unambiguous_tau_derived_route_A_or_route_B_metadata_before_physical_precheck"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit physical Tau-grid derivation metadata before table acceptance.")
    parser.add_argument("--metadata", default=str(DEFAULT_METADATA))
    parser.add_argument("--write-audit", nargs="?", const=str(DEFAULT_AUDIT))
    args = parser.parse_args()

    audit = build_audit(Path(args.metadata).resolve())
    text = json.dumps(audit, indent=2, sort_keys=True)
    if args.write_audit:
        path = Path(args.write_audit)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
