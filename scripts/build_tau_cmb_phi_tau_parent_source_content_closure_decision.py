#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

PACKET_ID = "TAU_CMB_PHI_TAU_PARENT_SOURCE_CONTENT_CLOSURE_DECISION_V01"
CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_source_content_closure_decision_v01_decision_only_"
    "endpoint_clean_but_unclosed_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

ROW_FIELDS = [
    "closure_row_id",
    "source_content_component",
    "candidate_symbol_or_object",
    "content_status",
    "candidate_content_present",
    "dimension_or_lock_passed",
    "endpoint_clean",
    "payload_firewall_passed",
    "replay_available",
    "accepted_as_parent_input",
    "closure_decision",
    "remaining_blocker",
    "score_effect",
    "score_entry_allowed",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "source_content_rows_declared",
    "candidate_content_rows",
    "endpoint_clean_rows",
    "dimension_or_lock_passed_rows",
    "payload_firewall_passed_rows",
    "replay_available_rows",
    "accepted_parent_input_rows",
    "closed_rows",
    "blocked_rows",
    "partial_rows",
    "phi_tau_parent_source_content_closed",
    "endpoint_blind_provenance_accepted",
    "phi_tau_eff_source_derivation_allowed",
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


def closure_rows() -> list[dict[str, str]]:
    rows = [
        {
            "source_content_component": "candidate_payload_manifest_identity",
            "candidate_symbol_or_object": "M_parent_payload_candidate_v01",
            "content_status": "PARTIAL_PACKAGE_IDENTITY_PRESENT_NOT_CLOSED",
            "candidate_content_present": "true",
            "dimension_or_lock_passed": "false",
            "endpoint_clean": "true",
            "payload_firewall_passed": "false",
            "replay_available": "false",
            "accepted_as_parent_input": "false",
            "closure_decision": "PARTIAL_IDENTITY_ONLY",
            "remaining_blocker": "child source-content rows are not accepted",
            "score_effect": "keeps the package addressable but not source-ready",
        },
        {
            "source_content_component": "base_field_state_payload_candidate",
            "candidate_symbol_or_object": "B_tau_candidate(parent)",
            "content_status": "BLOCKED_CONTENT_PRESENT_DIMENSION_FIREWALL_REPLAY_MISSING",
            "candidate_content_present": "true",
            "dimension_or_lock_passed": "false",
            "endpoint_clean": "true",
            "payload_firewall_passed": "false",
            "replay_available": "false",
            "accepted_as_parent_input": "false",
            "closure_decision": "BLOCKED_NOT_PARENT_INPUT",
            "remaining_blocker": "base-field dimension/unit pass, payload firewall certificate, and replay are missing",
            "score_effect": "blocks source-amplitude grounding",
        },
        {
            "source_content_component": "morphological_seed_payload_candidate",
            "candidate_symbol_or_object": "seed_tau_candidate(parent)",
            "content_status": "BLOCKED_CONTENT_PRESENT_SCALE_FIREWALL_REPLAY_MISSING",
            "candidate_content_present": "true",
            "dimension_or_lock_passed": "false",
            "endpoint_clean": "true",
            "payload_firewall_passed": "false",
            "replay_available": "false",
            "accepted_as_parent_input": "false",
            "closure_decision": "BLOCKED_NOT_PARENT_INPUT",
            "remaining_blocker": "seed scale/normalization pass, payload firewall certificate, and replay are missing",
            "score_effect": "blocks source activation grounding",
        },
        {
            "source_content_component": "response_operator_payload_candidate",
            "candidate_symbol_or_object": "R_tau_candidate",
            "content_status": "BLOCKED_CONTENT_PRESENT_OPERATOR_DIMENSION_FIREWALL_REPLAY_MISSING",
            "candidate_content_present": "true",
            "dimension_or_lock_passed": "false",
            "endpoint_clean": "true",
            "payload_firewall_passed": "false",
            "replay_available": "false",
            "accepted_as_parent_input": "false",
            "closure_decision": "BLOCKED_NOT_PARENT_INPUT",
            "remaining_blocker": "operator dimensional map pass, payload firewall certificate, and replay are missing",
            "score_effect": "blocks Phi_tau_eff derivation",
        },
        {
            "source_content_component": "gauge_normalization_payload_candidate",
            "candidate_symbol_or_object": "gauge_norm_candidate(parent)",
            "content_status": "PARTIAL_CONTENT_PRESENT_LOCK_FIREWALL_REPLAY_MISSING",
            "candidate_content_present": "true",
            "dimension_or_lock_passed": "false",
            "endpoint_clean": "true",
            "payload_firewall_passed": "false",
            "replay_available": "false",
            "accepted_as_parent_input": "false",
            "closure_decision": "PARTIAL_METADATA_NOT_LOCKED",
            "remaining_blocker": "gauge/normalization lock, payload firewall certificate, and replay are missing",
            "score_effect": "blocks shared-source normalization for acoustic and lensing roles",
        },
        {
            "source_content_component": "endpoint_firewall_payload_candidate",
            "candidate_symbol_or_object": "firewall_certificate_candidate(parent payload)",
            "content_status": "BLOCKED_CERTIFICATE_NOT_SUPPLIED",
            "candidate_content_present": "false",
            "dimension_or_lock_passed": "false",
            "endpoint_clean": "true",
            "payload_firewall_passed": "false",
            "replay_available": "false",
            "accepted_as_parent_input": "false",
            "closure_decision": "BLOCKED_FIREWALL_CERTIFICATE_MISSING",
            "remaining_blocker": "payload-level endpoint firewall certificate is missing",
            "score_effect": "blocks accepting every candidate payload row",
        },
        {
            "source_content_component": "provenance_replay_payload_candidate",
            "candidate_symbol_or_object": "replay_candidate(parent payload)",
            "content_status": "BLOCKED_EXECUTABLE_REPLAY_NOT_SUPPLIED",
            "candidate_content_present": "false",
            "dimension_or_lock_passed": "false",
            "endpoint_clean": "true",
            "payload_firewall_passed": "false",
            "replay_available": "false",
            "accepted_as_parent_input": "false",
            "closure_decision": "BLOCKED_REPLAY_MISSING",
            "remaining_blocker": "executable endpoint-blind replay is missing",
            "score_effect": "blocks endpoint-blind provenance promotion and score entry",
        },
    ]
    out: list[dict[str, str]] = []
    for index, row in enumerate(rows, start=1):
        out.append(
            {
                "closure_row_id": f"TCMBPTPSCCD01_{index:03d}",
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
        "source_content_rows_declared": str(len(rows)),
        "candidate_content_rows": str(sum(row["candidate_content_present"] == "true" for row in rows)),
        "endpoint_clean_rows": str(sum(row["endpoint_clean"] == "true" for row in rows)),
        "dimension_or_lock_passed_rows": str(sum(row["dimension_or_lock_passed"] == "true" for row in rows)),
        "payload_firewall_passed_rows": str(sum(row["payload_firewall_passed"] == "true" for row in rows)),
        "replay_available_rows": str(sum(row["replay_available"] == "true" for row in rows)),
        "accepted_parent_input_rows": str(sum(row["accepted_as_parent_input"] == "true" for row in rows)),
        "closed_rows": str(sum(row["closure_decision"].startswith("CLOSED") for row in rows)),
        "blocked_rows": str(sum(row["closure_decision"].startswith("BLOCKED") for row in rows)),
        "partial_rows": str(sum(row["closure_decision"].startswith("PARTIAL") for row in rows)),
        "phi_tau_parent_source_content_closed": "false",
        "endpoint_blind_provenance_accepted": "false",
        "phi_tau_eff_source_derivation_allowed": "false",
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
        "overall_status": "PHI_TAU_PARENT_SOURCE_CONTENT_ENDPOINT_CLEAN_BUT_UNCLOSED_SCORE_BLOCKED",
        "next_required_artifact": "tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_json(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "phi_tau_parent_source_content_closure_decision",
        "status": row["overall_status"],
        "claim_boundary": CLAIM_BOUNDARY,
        "closure_rows": rows,
        "summary": row,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_doc(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    lines = [
        "# Tau CMB Phi Tau Parent Source Content Closure Decision v01",
        "",
        "**Doc class:** parent-source-content closure decision",
        "**Reader role:** Paper 13 CMB peak scoring path",
        "**Status:** endpoint-clean candidate content exists, but source content is not closed; score blocked",
        "**Canonical parent:** Paper 13 CMB scoring input fulfillment chain",
        "",
        "## Purpose",
        "",
        "This artifact consolidates the parent-input candidate, concrete payload candidate, and payload firewall audit into one source-content closure decision. It asks whether the available parent-side material is sufficient to derive `Phi_tau_eff(a,k)` without endpoint contamination.",
        "",
        "## Summary",
        "",
        f"- source_content_rows_declared = {row['source_content_rows_declared']}",
        f"- candidate_content_rows = {row['candidate_content_rows']}",
        f"- endpoint_clean_rows = {row['endpoint_clean_rows']}",
        f"- dimension_or_lock_passed_rows = {row['dimension_or_lock_passed_rows']}",
        f"- payload_firewall_passed_rows = {row['payload_firewall_passed_rows']}",
        f"- replay_available_rows = {row['replay_available_rows']}",
        f"- accepted_parent_input_rows = {row['accepted_parent_input_rows']}",
        f"- phi_tau_parent_source_content_closed = {row['phi_tau_parent_source_content_closed']}",
        f"- phi_tau_eff_source_derivation_allowed = {row['phi_tau_eff_source_derivation_allowed']}",
        f"- score_ready_rows = {row['score_ready_rows']}",
        f"- overall_status = {row['overall_status']}",
        f"- next_required_artifact = {row['next_required_artifact']}",
        "",
        "## Closure Rows",
        "",
        "| component | content_status | closure_decision |",
        "| --- | --- | --- |",
    ]
    for closure_row in rows:
        lines.append(
            f"| {closure_row['source_content_component']} | {closure_row['content_status']} | "
            f"{closure_row['closure_decision']} |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            "The source-content package is endpoint-clean at the checked field level, but it is not closed. No dimensional or normalization lock passes, no payload-level firewall certificate is supplied, no executable replay is available, and no parent input is accepted.",
            "",
            "## Claim Boundary",
            "",
            CLAIM_BOUNDARY,
            "",
            "This decision artifact does not derive `Phi_tau_eff`, does not accept endpoint-blind provenance, does not solve the acoustic operator, does not predict CMB peaks, does not compute a CMB score or likelihood, and does not decide whether a dark sector is needed.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    rows = closure_rows()
    row = summary(rows)
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_source_content_closure_decision_v01.csv", rows, ROW_FIELDS)
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_source_content_closure_decision_summary_v01.csv",
        [row],
        SUMMARY_FIELDS,
    )
    write_json(DERIVED / "tau_cmb_phi_tau_parent_source_content_closure_decision_v01.json", rows, row)
    write_doc(DOCS / "tau_cmb_phi_tau_parent_source_content_closure_decision_v01.md", rows, row)
    print("TAU_CMB_PHI_TAU_PARENT_SOURCE_CONTENT_CLOSURE_DECISION_V01_BUILT")


if __name__ == "__main__":
    main()
