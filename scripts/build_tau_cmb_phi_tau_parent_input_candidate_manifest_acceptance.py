#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

PACKET_ID = "TAU_CMB_PHI_TAU_PARENT_INPUT_CANDIDATE_MANIFEST_ACCEPTANCE_V01"
CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_v01_identity_only_"
    "no_accepted_parent_inputs_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

ROW_FIELDS = [
    "acceptance_row_id",
    "candidate_component",
    "candidate_symbol_or_object",
    "acceptance_requirement",
    "evidence_source",
    "acceptance_status",
    "accepted_as_parent_input",
    "remaining_blocker",
    "score_effect",
    "score_entry_allowed",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "candidate_acceptance_rows_declared",
    "accepted_identity_rows",
    "accepted_parent_input_rows",
    "blocked_rows",
    "partial_rows",
    "candidate_packet_identity_accepted",
    "base_field_state_accepted",
    "morphological_seed_accepted",
    "response_operator_accepted",
    "gauge_normalization_locked",
    "endpoint_firewall_executed",
    "provenance_replay_supplied",
    "candidate_manifest_acceptance_satisfied",
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


def acceptance_rows() -> list[dict[str, str]]:
    rows = [
        {
            "candidate_component": "candidate_manifest_identity",
            "candidate_symbol_or_object": "M_parent_candidate_v01",
            "acceptance_requirement": "The manifest identity may be accepted only as the named candidate packet, not as a source input.",
            "evidence_source": "tau_cmb_phi_tau_parent_input_candidate_manifest_v01",
            "acceptance_status": "ACCEPTED_IDENTITY_ONLY_NOT_PARENT_INPUT",
            "accepted_as_parent_input": "false",
            "remaining_blocker": "manifest identity contains no physical parent-side content",
            "score_effect": "keeps the candidate packet addressable but does not open scoring",
        },
        {
            "candidate_component": "base_field_state_candidate",
            "candidate_symbol_or_object": "B_tau_candidate(parent)",
            "acceptance_requirement": "A base-field state descriptor must be supplied before it can ground Phi_tau_eff.",
            "evidence_source": "tau_cmb_phi_tau_parent_input_candidate_manifest_v01",
            "acceptance_status": "BLOCKED_BASE_FIELD_DESCRIPTOR_NOT_SUPPLIED",
            "accepted_as_parent_input": "false",
            "remaining_blocker": "no endpoint-blind base-field value, descriptor, or support domain is present",
            "score_effect": "blocks source amplitude and carrier-state grounding",
        },
        {
            "candidate_component": "morphological_seed_candidate",
            "candidate_symbol_or_object": "seed_tau_candidate(parent)",
            "acceptance_requirement": "A seed descriptor must be fixed before endpoint comparison and tied to parent-side morphology.",
            "evidence_source": "tau_cmb_phi_tau_parent_input_candidate_manifest_v01",
            "acceptance_status": "BLOCKED_MORPHOLOGICAL_SEED_NOT_SUPPLIED",
            "accepted_as_parent_input": "false",
            "remaining_blocker": "no endpoint-blind seed descriptor is present",
            "score_effect": "blocks physical source interpretation",
        },
        {
            "candidate_component": "response_operator_candidate",
            "candidate_symbol_or_object": "R_tau_candidate",
            "acceptance_requirement": "A response operator input set must map accepted parent inputs toward Phi_tau_eff.",
            "evidence_source": "tau_cmb_phi_tau_parent_input_candidate_manifest_v01",
            "acceptance_status": "BLOCKED_RESPONSE_OPERATOR_INPUTS_NOT_SUPPLIED",
            "accepted_as_parent_input": "false",
            "remaining_blocker": "no replayable operator input set is present",
            "score_effect": "blocks derivation rule construction",
        },
        {
            "candidate_component": "gauge_normalization_candidate",
            "candidate_symbol_or_object": "gauge_norm_candidate",
            "acceptance_requirement": "Gauge, sign, unit, and normalization metadata must be locked before acoustic/lensing use.",
            "evidence_source": "tau_cmb_phi_tau_parent_input_candidate_manifest_v01",
            "acceptance_status": "PARTIAL_METADATA_DECLARED_NOT_LOCKED",
            "accepted_as_parent_input": "false",
            "remaining_blocker": "metadata class is declared but not locked or dimension-replayed",
            "score_effect": "blocks cross-role comparison and amplitude interpretation",
        },
        {
            "candidate_component": "endpoint_firewall_candidate",
            "candidate_symbol_or_object": "firewall_candidate(M_parent_candidate_v01)",
            "acceptance_requirement": "The endpoint firewall must be executed against the candidate packet.",
            "evidence_source": "tau_cmb_phi_tau_parent_input_candidate_manifest_v01",
            "acceptance_status": "PARTIAL_FIREWALL_RULE_DECLARED_NOT_EXECUTED",
            "accepted_as_parent_input": "false",
            "remaining_blocker": "firewall rule is declared but no concrete packet has been audited",
            "score_effect": "keeps endpoint contamination policy explicit but blocks score entry",
        },
        {
            "candidate_component": "provenance_replay_candidate",
            "candidate_symbol_or_object": "replay_candidate(parent inputs)",
            "acceptance_requirement": "A replay package must prove the candidates were fixed before endpoint scoring.",
            "evidence_source": "tau_cmb_phi_tau_parent_input_candidate_manifest_v01",
            "acceptance_status": "BLOCKED_REPLAY_CANDIDATE_NOT_SUPPLIED",
            "accepted_as_parent_input": "false",
            "remaining_blocker": "no executable replay candidate is present",
            "score_effect": "blocks endpoint-blind provenance promotion",
        },
    ]
    out: list[dict[str, str]] = []
    for index, row in enumerate(rows, start=1):
        out.append(
            {
                "acceptance_row_id": f"TCMBPTPICMA01_{index:03d}",
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
        "candidate_acceptance_rows_declared": str(len(rows)),
        "accepted_identity_rows": str(sum(row["acceptance_status"].startswith("ACCEPTED_IDENTITY") for row in rows)),
        "accepted_parent_input_rows": str(sum(row["accepted_as_parent_input"] == "true" for row in rows)),
        "blocked_rows": str(sum(row["acceptance_status"].startswith("BLOCKED") for row in rows)),
        "partial_rows": str(sum(row["acceptance_status"].startswith("PARTIAL") for row in rows)),
        "candidate_packet_identity_accepted": "true",
        "base_field_state_accepted": "false",
        "morphological_seed_accepted": "false",
        "response_operator_accepted": "false",
        "gauge_normalization_locked": "false",
        "endpoint_firewall_executed": "false",
        "provenance_replay_supplied": "false",
        "candidate_manifest_acceptance_satisfied": "false",
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
        "overall_status": "PHI_TAU_PARENT_INPUT_CANDIDATE_MANIFEST_IDENTITY_ACCEPTED_INPUTS_BLOCKED_SCORE_BLOCKED",
        "next_required_artifact": "tau_cmb_phi_tau_parent_input_firewall_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_json(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "phi_tau_parent_input_candidate_manifest_acceptance_audit",
        "status": row["overall_status"],
        "claim_boundary": CLAIM_BOUNDARY,
        "acceptance_rows": rows,
        "summary": row,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_doc(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    lines = [
        "# Tau CMB Phi Tau Parent Input Candidate Manifest Acceptance v01",
        "",
        "**Doc class:** parent-input candidate manifest acceptance audit",
        "**Reader role:** Paper 13 CMB peak scoring path",
        "**Status:** candidate packet identity accepted; parent inputs blocked; score blocked",
        "**Canonical parent:** Paper 13 CMB scoring input fulfillment chain",
        "",
        "## Purpose",
        "",
        "This artifact audits whether the declared parent-input candidate manifest can be accepted as endpoint-blind provenance material for `Phi_tau_eff(a,k)`. It accepts only the manifest identity as a named packet. It accepts no parent-side input content.",
        "",
        "## Summary",
        "",
        f"- candidate_acceptance_rows_declared = {row['candidate_acceptance_rows_declared']}",
        f"- accepted_identity_rows = {row['accepted_identity_rows']}",
        f"- accepted_parent_input_rows = {row['accepted_parent_input_rows']}",
        f"- blocked_rows = {row['blocked_rows']}",
        f"- partial_rows = {row['partial_rows']}",
        f"- candidate_packet_identity_accepted = {row['candidate_packet_identity_accepted']}",
        f"- candidate_manifest_acceptance_satisfied = {row['candidate_manifest_acceptance_satisfied']}",
        f"- score_ready_rows = {row['score_ready_rows']}",
        f"- overall_status = {row['overall_status']}",
        f"- next_required_artifact = {row['next_required_artifact']}",
        "",
        "## Acceptance Rows",
        "",
        "| component | symbol_or_object | acceptance_status | accepted_as_parent_input |",
        "| --- | --- | --- | --- |",
    ]
    for acceptance_row in rows:
        lines.append(
            f"| {acceptance_row['candidate_component']} | {acceptance_row['candidate_symbol_or_object']} | "
            f"{acceptance_row['acceptance_status']} | {acceptance_row['accepted_as_parent_input']} |"
        )
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            CLAIM_BOUNDARY,
            "",
            "This acceptance audit accepts only the candidate packet identity. It accepts no base-field state, no morphological seed, no response operator, no locked normalization, no executed endpoint firewall, and no provenance replay. It derives no `Phi_tau_eff`, computes no score or likelihood, and permits no no-dark or dark-sector verdict.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    rows = acceptance_rows()
    row = summary(rows)
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_v01.csv", rows, ROW_FIELDS)
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_summary_v01.csv",
        [row],
        SUMMARY_FIELDS,
    )
    write_json(DERIVED / "tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_v01.json", rows, row)
    write_doc(DOCS / "tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_v01.md", rows, row)
    print("TAU_CMB_PHI_TAU_PARENT_INPUT_CANDIDATE_MANIFEST_ACCEPTANCE_V01_BUILT")


if __name__ == "__main__":
    main()
