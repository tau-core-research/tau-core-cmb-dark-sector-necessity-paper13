#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

PACKET_ID = "TAU_CMB_PHI_TAU_EFF_ENDPOINT_BLIND_PROVENANCE_ACCEPTANCE_V01"
CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_v01_policy_only_"
    "no_accepted_provenance_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

ROW_FIELDS = [
    "provenance_row_id",
    "provenance_component",
    "symbol_or_role",
    "acceptance_requirement",
    "evidence_source",
    "acceptance_status",
    "remaining_blocker",
    "score_effect",
    "score_entry_allowed",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "provenance_acceptance_rows_declared",
    "accepted_policy_rows",
    "blocked_rows",
    "partial_rows",
    "endpoint_exclusion_rule_accepted",
    "parent_input_manifest_supplied",
    "derivation_rule_supplied",
    "replay_package_supplied",
    "endpoint_blind_provenance_accepted",
    "phi_tau_eff_acoustic_input_accepted",
    "operator_model_accepted_rows",
    "derived_source_rows",
    "executable_prediction_rows",
    "accepted_planck_payload_rows",
    "score_ready_rows",
    "scores_computed",
    "cmb_likelihood_available",
    "tau_response_claim_allowed",
    "dark_sector_verdict_allowed",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def provenance_rows() -> list[dict[str, str]]:
    rows = [
        {
            "provenance_component": "endpoint_exclusion_rule",
            "symbol_or_role": "endpoint_blind_policy(Phi_tau_eff)",
            "acceptance_requirement": "Declare that Phi_tau_eff provenance must not use CMB residual fitting, role scores, endpoint labels, or dark-sector verdict feedback.",
            "evidence_source": "tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01",
            "acceptance_status": "ACCEPTED_POLICY_ONLY_ENDPOINT_EXCLUSION_RULE",
            "remaining_blocker": "policy acceptance is not a parent-side derivation",
            "score_effect": "keeps score firewall explicit but does not open scoring",
        },
        {
            "provenance_component": "parent_input_manifest",
            "symbol_or_role": "manifest(parent_inputs -> Phi_tau_eff)",
            "acceptance_requirement": "Supply a concrete parent-side manifest identifying the Tau base-field state, seed descriptor, operator inputs, and normalization metadata.",
            "evidence_source": "tau_cmb_phi_tau_parent_input_provenance_v01",
            "acceptance_status": "BLOCKED_PARENT_INPUT_MANIFEST_NOT_SUPPLIED",
            "remaining_blocker": "parent-input provenance has no supplied rows",
            "score_effect": "blocks endpoint-blind source acceptance",
        },
        {
            "provenance_component": "parent_side_content",
            "symbol_or_role": "base_field_state + seed + response_operator",
            "acceptance_requirement": "Provide parent-side content sufficient to construct Phi_tau_eff without endpoint data.",
            "evidence_source": "tau_cmb_phi_tau_parent_input_candidate_manifest_v01",
            "acceptance_status": "BLOCKED_PARENT_SIDE_CONTENT_NOT_ACCEPTED",
            "remaining_blocker": "candidate classes are declared but not accepted as concrete content",
            "score_effect": "blocks source derivation and acoustic input acceptance",
        },
        {
            "provenance_component": "derivation_rule",
            "symbol_or_role": "D_tau[parent_inputs] -> Phi_tau_eff",
            "acceptance_requirement": "Supply a reproducible derivation rule mapping accepted parent inputs to Phi_tau_eff with dimensions and known limits audited.",
            "evidence_source": "tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01",
            "acceptance_status": "BLOCKED_DERIVATION_RULE_NOT_SUPPLIED",
            "remaining_blocker": "no derivation operator is supplied",
            "score_effect": "blocks executable effective-potential construction",
        },
        {
            "provenance_component": "audit_replay_package",
            "symbol_or_role": "replay(parent_inputs, D_tau, Phi_tau_eff)",
            "acceptance_requirement": "Provide a replayable audit package proving that the source construction is endpoint-blind.",
            "evidence_source": "tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01",
            "acceptance_status": "BLOCKED_REPLAY_PACKAGE_NOT_SUPPLIED",
            "remaining_blocker": "no replay package is supplied",
            "score_effect": "blocks promotion to score-ready input",
        },
        {
            "provenance_component": "failure_branch",
            "symbol_or_role": "explicit_fail(Phi_tau_eff provenance)",
            "acceptance_requirement": "Preserve an explicit failure branch when endpoint-blind provenance is not accepted.",
            "evidence_source": "tau_cmb_phi_tau_eff_acoustic_input_acceptance_v01",
            "acceptance_status": "PARTIAL_FAILURE_BRANCH_PRESERVED",
            "remaining_blocker": "failure branch is available, but it is not a positive provenance proof",
            "score_effect": "prevents premature score or dark-sector verdict",
        },
    ]
    out: list[dict[str, str]] = []
    for index, row in enumerate(rows, start=1):
        out.append(
            {
                "provenance_row_id": f"TCMBPTEEBPA01_{index:03d}",
                "score_entry_allowed": "false",
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
                **row,
            }
        )
    return out


def summary(rows: list[dict[str, str]]) -> dict[str, str]:
    return {
        "summary_id": PACKET_ID,
        "provenance_acceptance_rows_declared": str(len(rows)),
        "accepted_policy_rows": str(sum(row["acceptance_status"].startswith("ACCEPTED_POLICY") for row in rows)),
        "blocked_rows": str(sum(row["acceptance_status"].startswith("BLOCKED") for row in rows)),
        "partial_rows": str(sum(row["acceptance_status"].startswith("PARTIAL") for row in rows)),
        "endpoint_exclusion_rule_accepted": "true",
        "parent_input_manifest_supplied": "false",
        "derivation_rule_supplied": "false",
        "replay_package_supplied": "false",
        "endpoint_blind_provenance_accepted": "false",
        "phi_tau_eff_acoustic_input_accepted": "false",
        "operator_model_accepted_rows": "1",
        "derived_source_rows": "0",
        "executable_prediction_rows": "0",
        "accepted_planck_payload_rows": "0",
        "score_ready_rows": "0",
        "scores_computed": "false",
        "cmb_likelihood_available": "false",
        "tau_response_claim_allowed": "false",
        "dark_sector_verdict_allowed": "false",
        "overall_status": "PHI_TAU_EFF_ENDPOINT_BLIND_PROVENANCE_POLICY_ACCEPTED_PROVENANCE_BLOCKED_SCORE_BLOCKED",
        "next_required_artifact": "tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_v01",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_json(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "phi_tau_eff_endpoint_blind_provenance_acceptance_audit",
        "status": row["overall_status"],
        "claim_boundary": CLAIM_BOUNDARY,
        "provenance_acceptance_rows": rows,
        "summary": row,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_doc(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    lines = [
        "# Tau CMB Phi Tau Eff Endpoint-Blind Provenance Acceptance v01",
        "",
        "**Doc class:** Phi_tau_eff endpoint-blind provenance acceptance audit",
        "**Reader role:** Paper 13 CMB peak scoring path",
        "**Status:** endpoint-exclusion policy accepted; endpoint-blind provenance blocked; score blocked",
        "**Canonical parent:** Paper 13 CMB scoring input fulfillment chain",
        "",
        "## Purpose",
        "",
        "This artifact audits whether `Phi_tau_eff(a,k)` has acceptable endpoint-blind provenance after the acoustic input audit. It accepts only the endpoint-exclusion policy. It does not accept a parent-side source construction because the parent-input manifest, parent-side content, derivation rule, and replay package are still missing.",
        "",
        "## Summary",
        "",
        f"- provenance_acceptance_rows_declared = {row['provenance_acceptance_rows_declared']}",
        f"- accepted_policy_rows = {row['accepted_policy_rows']}",
        f"- blocked_rows = {row['blocked_rows']}",
        f"- partial_rows = {row['partial_rows']}",
        f"- endpoint_exclusion_rule_accepted = {row['endpoint_exclusion_rule_accepted']}",
        f"- endpoint_blind_provenance_accepted = {row['endpoint_blind_provenance_accepted']}",
        f"- phi_tau_eff_acoustic_input_accepted = {row['phi_tau_eff_acoustic_input_accepted']}",
        f"- score_ready_rows = {row['score_ready_rows']}",
        f"- overall_status = {row['overall_status']}",
        f"- next_required_artifact = {row['next_required_artifact']}",
        "",
        "## Acceptance Rows",
        "",
        "| component | symbol_or_role | acceptance_status |",
        "| --- | --- | --- |",
    ]
    for provenance_row in rows:
        lines.append(
            f"| {provenance_row['provenance_component']} | {provenance_row['symbol_or_role']} | "
            f"{provenance_row['acceptance_status']} |"
        )
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            CLAIM_BOUNDARY,
            "",
            "This acceptance audit accepts the endpoint-exclusion policy only. It does not accept endpoint-blind provenance for `Phi_tau_eff`, does not derive a source, does not solve the acoustic operator, does not predict CMB peaks, does not compute a CMB score or likelihood, and does not decide whether a dark sector is needed.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    rows = provenance_rows()
    row = summary(rows)
    write_csv(DERIVED / "tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_v01.csv", rows, ROW_FIELDS)
    write_csv(
        DERIVED / "tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_summary_v01.csv",
        [row],
        SUMMARY_FIELDS,
    )
    write_json(DERIVED / "tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_v01.json", rows, row)
    write_doc(DOCS / "tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_v01.md", rows, row)
    print("TAU_CMB_PHI_TAU_EFF_ENDPOINT_BLIND_PROVENANCE_ACCEPTANCE_V01_BUILT")


if __name__ == "__main__":
    main()
