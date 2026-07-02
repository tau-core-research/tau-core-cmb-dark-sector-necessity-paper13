#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
THEORY_ROOT = ROOT.parent / "tau-core-theory"
REQUEST_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_request_v01.csv"
REQUEST_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_request_audit_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_materialization_packet_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_materialization_packet_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_materialization_packet_v01_"
    "source_artifact_candidates_materialized_not_accepted_no_staging_write_no_payload_acceptance_"
    "no_checker_execution_no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict"
)

COMMON_SOURCES = [
    "docs/tau_cmb_source_grounding_gate_v01.md",
    "docs/tau_cmb_cosmology_derivation_spine_v01.md",
    "docs/tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01.md",
    "docs/tau_cmb_known_limit_and_dimension_audit_v01.md",
    "docs/tau_cmb_readout_role_space_basis_v01.md",
    "docs/tau_cmb_readout_role_space_basis_audit_v01.md",
    "../tau-core-theory/docs/tau_core_projection_induction_principle.md",
    "../tau-core-theory/docs/tau_core_morphology_theory.md",
    "../tau-core-theory/docs/tau_core_protected_readout_formalism.md",
    "../tau-core-theory/docs/tau_core_readout_stable_domain_selection_principle_001.md",
]

AREA_SOURCES = {
    "carrier_well_formedness": [
        "docs/tau_cmb_carrier_domain_certificate_requirements_v01.md",
        "docs/tau_cmb_carrier_domain_certificate_requirements_audit_v01.md",
        "docs/tau_cmb_carrier_domain_certificate_candidate_v01.md",
        "docs/tau_cmb_carrier_domain_checker_execution_packet_v01.md",
        "docs/tau_cmb_carrier_domain_proof_checker_payload_packet_v01.md",
    ],
    "domain_membership_rule": [
        "docs/tau_cmb_carrier_domain_predicate_candidate_v01.md",
        "docs/tau_cmb_carrier_domain_predicate_candidate_audit_v01.md",
        "docs/tau_cmb_seed_readout_domain_certificate_v01.md",
        "docs/tau_cmb_seed_support_domain_rule_candidate_v01.md",
        "docs/tau_cmb_seed_support_domain_rule_candidate_audit_v01.md",
    ],
    "seed_admissibility": [
        "docs/tau_cmb_morphological_seed_descriptor_candidate_v01.md",
        "docs/tau_cmb_morphological_seed_descriptor_candidate_audit_v01.md",
        "docs/tau_cmb_morphological_seed_activation_rule_candidate_v01.md",
        "docs/tau_cmb_morphological_seed_activation_rule_candidate_audit_v01.md",
        "docs/tau_cmb_seed_tau_payload_candidate_v01.md",
        "docs/tau_cmb_seed_tau_payload_candidate_audit_v01.md",
        "../tau-core-theory/docs/tau_core_seed_scale_bridge_001.md",
        "../tau-core-theory/docs/tau_core_morphological_root_multi_projection_principle_001.md",
    ],
    "null_control_admissibility": [
        "docs/tau_cmb_seed_zero_control_v01.md",
        "docs/tau_cmb_seed_zero_control_audit_v01.md",
        "docs/tau_cmb_readout_role_coordinate_null_v01.md",
        "docs/tau_cmb_readout_role_coordinate_null_audit_v01.md",
        "../tau-core-theory/docs/tau_core_null_gauge_readout_relativity_minimal_schema_001.md",
        "../tau-core-theory/docs/tau_core_protected_readout_comparison_matrix_008.md",
    ],
    "source_object_admissibility": [
        "docs/tau_cmb_effective_source_equation_v01.md",
        "docs/tau_cmb_minimal_source_term_candidate_v01.md",
        "docs/tau_cmb_source_term_dimensional_precheck_v01.md",
        "docs/tau_cmb_density_amplitude_derivation_v01.md",
        "docs/tau_cmb_density_amplitude_closure_v01.md",
        "../tau-core-theory/docs/tau_core_tau_dark_sector_b_tau_base_carrier_target_001.md",
        "../tau-core-theory/docs/tau_core_tau_dark_sector_response_rule_candidate_families_001.md",
    ],
    "quotient_and_equivalence_survival": [
        "docs/tau_cmb_morphological_seed_quotient_survival_test_v01.md",
        "docs/tau_cmb_seed_readout_quotient_relation_candidate_v01.md",
        "docs/tau_cmb_seed_readout_quotient_relation_candidate_audit_v01.md",
        "docs/tau_cmb_seed_readout_equivalence_relation_audit_v01.md",
        "docs/tau_cmb_seed_readout_equivalence_axiom_proof_obligation_v01.md",
        "../tau-core-theory/docs/tau_core_readout_degeneracy_minimal_schema_001.md",
        "../tau-core-theory/docs/tau_core_projection_bundle_compatibility_minimal_schema_001.md",
    ],
    "codomain_compatibility": [
        "docs/tau_cmb_concrete_R_CMB_carrier_certificate_v01.md",
        "docs/tau_cmb_concrete_R_CMB_carrier_certificate_audit_v01.md",
        "docs/tau_cmb_readout_role_coordinate_bundle_closure_v01.md",
        "docs/tau_cmb_readout_role_coordinate_bundle_closure_audit_v01.md",
        "docs/tau_cmb_readout_role_coordinate_lensing_v01.md",
        "docs/tau_cmb_lensing_N_parent_projection_packet_v01.md",
        "../tau-core-theory/docs/tau_core_scale_readout_profile_minimal_schema_001.md",
    ],
    "endpoint_firewall_replay": [
        "docs/tau_cmb_scoring_execution_gate_v01.md",
        "docs/cmb_tau_lensing_endpoint_blind_operator_prescore_lock_v01.md",
        "docs/cmb_tau_lensing_physical_projection_firewall_certificate_v01.md",
        "docs/cmb_tau_lensing_projection_post_population_firewall_spec_scaffold_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_provenance_v01.md",
        "payloads/seed_tau_payload_candidate_v01.replay.txt",
        "payloads/seed_tau_payload_candidate_v01.provenance.json",
    ],
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_source(path: str) -> Path:
    return (ROOT / path).resolve()


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_inventory(area: str) -> list[dict[str, Any]]:
    inventory: list[dict[str, Any]] = []
    for raw in COMMON_SOURCES + AREA_SOURCES[area]:
        path = resolve_source(raw)
        inventory.append(
            {
                "path": str(path),
                "exists": path.exists(),
                "sha256": sha256(path) if path.exists() and path.is_file() else None,
                "role": "endpoint_blind_tau_side_source_reference",
            }
        )
    return inventory


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def materialize_row(row: dict[str, str]) -> dict[str, Any]:
    artifact_path = ROOT / row["requested_source_artifact_path"]
    provenance_path = ROOT / row["requested_source_provenance_path"]
    replay_path = ROOT / row["requested_source_replay_path"]
    firewall_path = ROOT / row["requested_source_firewall_path"]
    hash_path = ROOT / row["requested_source_hash_path"]
    inventory = source_inventory(row["certificate_area"])

    artifact = {
        "artifact_id": row["request_row_id"],
        "artifact_status": "SOURCE_ARTIFACT_CANDIDATE_MATERIALIZED_NOT_ACCEPTED",
        "claim_boundary": CLAIM_BOUNDARY,
        "certificate_area": row["certificate_area"],
        "checker_name": row["checker_name"],
        "file_category": row["file_category"],
        "target_payload_staging_path": row["target_payload_staging_path"],
        "source_inventory": inventory,
        "endpoint_blind_rule": "constructed only from Tau Core theory/protocol artifacts; no CMB endpoint residual, likelihood error, score output, or post-endpoint tuning input is used",
        "acceptance_permissions": {
            "source_artifact_accepted": False,
            "staging_population_allowed": False,
            "payload_accepted": False,
            "checker_execution_allowed": False,
            "concrete_R_CMB_allowed": False,
            "score_entry_allowed": False,
            "likelihood_allowed": False,
            "dark_sector_verdict_allowed": False,
        },
    }
    provenance = {
        "artifact_id": row["request_row_id"],
        "claim_boundary": CLAIM_BOUNDARY,
        "construction_method": "local endpoint-blind source inventory materialization",
        "input_request_row": row,
        "source_inventory_count": len(inventory),
        "missing_source_references": [entry["path"] for entry in inventory if not entry["exists"]],
    }
    replay = {
        "artifact_id": row["request_row_id"],
        "claim_boundary": CLAIM_BOUNDARY,
        "replay_command": "make tau-cmb-carrier-domain-checker-input-payload-endpoint-blind-source-artifact-materialization-packet",
        "replay_scope": "rebuild source artifact, provenance, replay, firewall, and hash files from local endpoint-blind sources",
    }
    firewall = {
        "artifact_id": row["request_row_id"],
        "claim_boundary": CLAIM_BOUNDARY,
        "endpoint_blind_attestation": True,
        "forbidden_inputs": [
            "CMB endpoint residuals",
            "ACT/Planck likelihood errors",
            "score outputs",
            "post-endpoint tuning fields",
            "dark-sector verdict labels",
        ],
        "source_artifact_accepted": False,
        "staging_population_allowed": False,
    }

    write_json(artifact_path, artifact)
    write_json(provenance_path, provenance)
    write_json(replay_path, replay)
    write_json(firewall_path, firewall)
    hashes = {
        "artifact_id": row["request_row_id"],
        "claim_boundary": CLAIM_BOUNDARY,
        "hash_scope": "source_artifact_candidate_bundle",
        "files": {
            str(artifact_path): sha256(artifact_path),
            str(provenance_path): sha256(provenance_path),
            str(replay_path): sha256(replay_path),
            str(firewall_path): sha256(firewall_path),
        },
        "source_artifact_accepted": False,
    }
    write_json(hash_path, hashes)
    return {
        "request_row_id": row["request_row_id"],
        "certificate_area": row["certificate_area"],
        "file_category": row["file_category"],
        "artifact": str(artifact_path),
        "hash": str(hash_path),
        "provenance": str(provenance_path),
        "replay": str(replay_path),
        "firewall": str(firewall_path),
        "source_reference_count": len(inventory),
        "missing_source_reference_count": sum(not entry["exists"] for entry in inventory),
        "source_artifact_accepted": False,
        "staging_population_allowed": False,
    }


def build_report(write_sources: bool) -> dict[str, Any]:
    request_audit = load_json(REQUEST_AUDIT) if REQUEST_AUDIT.exists() else {}
    input_ok = (
        request_audit.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_REQUEST_AUDITED_NOT_SUPPLIED"
        and request_audit.get("failed_rows") == 0
        and REQUEST_TABLE.exists()
    )
    rows = read_csv(REQUEST_TABLE)
    materialized = [materialize_row(row) for row in rows] if write_sources else []
    return {
        "report_id": "tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_materialization_packet_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "input_request_table": str(REQUEST_TABLE),
        "input_request_audit": str(REQUEST_AUDIT),
        "input_chain_clean": input_ok,
        "requested_rows": len(rows),
        "source_artifact_bundles_materialized": len(materialized),
        "source_artifact_accepted_rows": 0,
        "staging_population_allowed_rows": 0,
        "payload_staging_written_rows": 0,
        "payload_accepted_rows": 0,
        "checker_executed_rows": 0,
        "certificate_passed_rows": 0,
        "accepted_domain_objects": 0,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "materialized_rows": materialized,
        "status": (
            "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_CANDIDATES_MATERIALIZED_NOT_ACCEPTED"
            if input_ok and write_sources
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_MATERIALIZATION_DRY_RUN"
            if input_ok
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_MATERIALIZATION_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "audit_tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_materialization_packet_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    text = f"""# Tau CMB Carrier Domain Checker Input Payload Endpoint-Blind Source Artifact Materialization Packet v01

**Doc class:** carrier/domain checker input payload endpoint-blind source artifact materialization packet
**Reader role:** Paper 13 / CMB readout route implementer
**Status:** {report["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This packet materializes endpoint-blind Tau-side source artifact candidate
bundles under `payload_sources/`. The bundles are built from local Tau Core
theory/protocol artifacts and are not accepted source inputs. The packet does
not populate `payload_staging/`, accept payloads, execute checkers, pass
certificates, accept domain objects, materialize `R_CMB`, open score entry,
compute a likelihood, or decide the dark-sector question.

## Summary

```text
requested_rows={report["requested_rows"]}
source_artifact_bundles_materialized={report["source_artifact_bundles_materialized"]}
source_artifact_accepted_rows={report["source_artifact_accepted_rows"]}
staging_population_allowed_rows={report["staging_population_allowed_rows"]}
payload_staging_written_rows={report["payload_staging_written_rows"]}
score_entry_allowed={report["score_entry_allowed"]}
likelihood_allowed={report["likelihood_allowed"]}
dark_sector_verdict_allowed={report["dark_sector_verdict_allowed"]}
```

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize endpoint-blind source artifact candidates for Tau CMB checker input payloads.")
    parser.add_argument("--write-sources", action="store_true")
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    report = build_report(write_sources=args.write_sources)
    if args.write_report:
        report_path = Path(args.write_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), report)
    print(json.dumps({k: v for k, v in report.items() if k != "materialized_rows"}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
