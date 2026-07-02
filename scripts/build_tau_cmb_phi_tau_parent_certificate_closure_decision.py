#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

PACKET_ID = "TAU_CMB_PHI_TAU_PARENT_CERTIFICATE_CLOSURE_DECISION_V01"
CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_certificate_closure_decision_v01_decision_only_"
    "certificates_unpassed_no_parent_input_acceptance_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

ROW_FIELDS = [
    "closure_row_id",
    "certificate_component",
    "target_payload_component",
    "certificate_closure_status",
    "requirement_declared",
    "candidate_declared",
    "candidate_audited",
    "certificate_evidence_supplied",
    "dimension_passed",
    "replay_passed",
    "firewall_passed",
    "certificate_passed",
    "payload_accepted",
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
    "certificate_closure_rows_declared",
    "requirements_declared_rows",
    "candidate_declared_rows",
    "candidate_audited_rows",
    "certificate_evidence_supplied_rows",
    "dimension_passed_rows",
    "replay_passed_rows",
    "firewall_passed_rows",
    "certificate_passed_rows",
    "payload_accepted_rows",
    "closed_rows",
    "blocked_rows",
    "phi_tau_parent_certificates_closed",
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
    base_rows = [
        (
            "certificate_candidate_manifest_identity",
            "all_parent_payload_rows",
            "BLOCKED_MANIFEST_CERTIFICATE_EVIDENCE_MISSING",
            "certificate package index, replay trace, and payload firewall certificate are missing",
            "keeps the certificate package outside scoring acceptance",
        ),
        (
            "base_field_dimension_replay_certificate_candidate",
            "base_field_state_payload_candidate",
            "BLOCKED_DIMENSION_REPLAY_FIREWALL_EVIDENCE_MISSING",
            "B_tau dimension/unit proof, endpoint-blind replay, and endpoint-firewall proof are missing",
            "blocks density-amplitude and potential-source grounding",
        ),
        (
            "seed_dimension_replay_certificate_candidate",
            "morphological_seed_payload_candidate",
            "BLOCKED_SCALE_REPLAY_FIREWALL_EVIDENCE_MISSING",
            "seed_tau scale proof, seed replay, and endpoint-firewall proof are missing",
            "blocks source-activation grounding",
        ),
        (
            "operator_dimension_replay_certificate_candidate",
            "response_operator_payload_candidate",
            "BLOCKED_OPERATOR_REPLAY_FIREWALL_EVIDENCE_MISSING",
            "R_tau dimensional-map proof, operator replay, and endpoint-firewall proof are missing",
            "blocks Phi_tau_eff derivation",
        ),
        (
            "gauge_normalization_replay_certificate_candidate",
            "gauge_normalization_payload_candidate",
            "BLOCKED_NORMALIZATION_REPLAY_FIREWALL_EVIDENCE_MISSING",
            "gauge/sign/unit/normalization proof, metadata-lock replay, and endpoint-firewall proof are missing",
            "blocks shared-source normalization for CMB roles",
        ),
        (
            "payload_firewall_certificate_candidate",
            "endpoint_firewall_payload_candidate",
            "BLOCKED_PAYLOAD_FIREWALL_CERTIFICATE_MISSING",
            "aggregate payload-level firewall certificate is missing",
            "blocks accepting any parent-input payload row",
        ),
        (
            "executable_replay_certificate_candidate",
            "provenance_replay_payload_candidate",
            "BLOCKED_EXECUTABLE_REPLAY_CERTIFICATE_MISSING",
            "endpoint-blind executable replay trace and input provenance hash are missing",
            "blocks transition into scoring input acceptance",
        ),
    ]
    rows: list[dict[str, str]] = []
    for index, (component, target, status, blocker, effect) in enumerate(base_rows, start=1):
        rows.append(
            {
                "closure_row_id": f"TCMBPTPCCD01_{index:03d}",
                "certificate_component": component,
                "target_payload_component": target,
                "certificate_closure_status": status,
                "requirement_declared": "true",
                "candidate_declared": "true",
                "candidate_audited": "true",
                "certificate_evidence_supplied": "false",
                "dimension_passed": "false",
                "replay_passed": "false",
                "firewall_passed": "false",
                "certificate_passed": "false",
                "payload_accepted": "false",
                "closure_decision": "BLOCKED_CERTIFICATE_NOT_CLOSED",
                "remaining_blocker": blocker,
                "score_effect": effect,
                "score_entry_allowed": "false",
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, str]]) -> dict[str, str]:
    return {
        "summary_id": PACKET_ID,
        "certificate_closure_rows_declared": str(len(rows)),
        "requirements_declared_rows": str(sum(row["requirement_declared"] == "true" for row in rows)),
        "candidate_declared_rows": str(sum(row["candidate_declared"] == "true" for row in rows)),
        "candidate_audited_rows": str(sum(row["candidate_audited"] == "true" for row in rows)),
        "certificate_evidence_supplied_rows": str(sum(row["certificate_evidence_supplied"] == "true" for row in rows)),
        "dimension_passed_rows": str(sum(row["dimension_passed"] == "true" for row in rows)),
        "replay_passed_rows": str(sum(row["replay_passed"] == "true" for row in rows)),
        "firewall_passed_rows": str(sum(row["firewall_passed"] == "true" for row in rows)),
        "certificate_passed_rows": str(sum(row["certificate_passed"] == "true" for row in rows)),
        "payload_accepted_rows": str(sum(row["payload_accepted"] == "true" for row in rows)),
        "closed_rows": str(sum(row["closure_decision"].startswith("CLOSED") for row in rows)),
        "blocked_rows": str(sum(row["closure_decision"].startswith("BLOCKED") for row in rows)),
        "phi_tau_parent_certificates_closed": "false",
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
        "overall_status": "PHI_TAU_PARENT_CERTIFICATES_DECLARED_AND_AUDITED_BUT_UNCLOSED_SCORE_BLOCKED",
        "next_required_artifact": "tau_cmb_phi_tau_parent_input_certificate_evidence_request_v01",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_json(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "phi_tau_parent_certificate_closure_decision",
        "status": row["overall_status"],
        "claim_boundary": CLAIM_BOUNDARY,
        "closure_rows": rows,
        "summary": row,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_doc(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    lines = [
        "# Tau CMB Phi Tau Parent Certificate Closure Decision v01",
        "",
        "**Doc class:** parent-certificate closure decision",
        "**Reader role:** Paper 13 CMB peak scoring path",
        "**Status:** certificate requirements and candidates are declared and audited, but no certificate closes; score blocked",
        "**Canonical parent:** Paper 13 CMB scoring input fulfillment chain",
        "",
        "## Purpose",
        "",
        "This artifact consolidates the dimension/replay certificate requirements, certificate candidates, and certificate audit into one closure decision. It asks whether the parent-side payload has enough certificate evidence to be accepted as endpoint-blind source material for `Phi_tau_eff(a,k)`.",
        "",
        "## Summary",
        "",
        f"- certificate_closure_rows_declared = {row['certificate_closure_rows_declared']}",
        f"- requirements_declared_rows = {row['requirements_declared_rows']}",
        f"- candidate_declared_rows = {row['candidate_declared_rows']}",
        f"- candidate_audited_rows = {row['candidate_audited_rows']}",
        f"- certificate_evidence_supplied_rows = {row['certificate_evidence_supplied_rows']}",
        f"- dimension_passed_rows = {row['dimension_passed_rows']}",
        f"- replay_passed_rows = {row['replay_passed_rows']}",
        f"- firewall_passed_rows = {row['firewall_passed_rows']}",
        f"- certificate_passed_rows = {row['certificate_passed_rows']}",
        f"- payload_accepted_rows = {row['payload_accepted_rows']}",
        f"- phi_tau_parent_certificates_closed = {row['phi_tau_parent_certificates_closed']}",
        f"- phi_tau_eff_source_derivation_allowed = {row['phi_tau_eff_source_derivation_allowed']}",
        f"- score_ready_rows = {row['score_ready_rows']}",
        f"- overall_status = {row['overall_status']}",
        f"- next_required_artifact = {row['next_required_artifact']}",
        "",
        "## Closure Rows",
        "",
        "| component | target | closure_status |",
        "| --- | --- | --- |",
    ]
    for closure_row in rows:
        lines.append(
            f"| {closure_row['certificate_component']} | {closure_row['target_payload_component']} | "
            f"{closure_row['certificate_closure_status']} |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            "The certificate layer is not closed. Requirements exist, candidates exist, and candidates are audited, but no certificate evidence is supplied, no dimension/replay/firewall audit passes, and no payload row is accepted.",
            "",
            "## Claim Boundary",
            "",
            CLAIM_BOUNDARY,
            "",
            "This decision artifact does not accept parent-side Tau inputs, does not derive `Phi_tau_eff`, does not accept endpoint-blind provenance, does not solve the acoustic operator, does not compute a CMB score or likelihood, and does not decide whether a dark sector is needed.",
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
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_certificate_closure_decision_v01.csv", rows, ROW_FIELDS)
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_certificate_closure_decision_summary_v01.csv", [row], SUMMARY_FIELDS)
    write_json(DERIVED / "tau_cmb_phi_tau_parent_certificate_closure_decision_v01.json", rows, row)
    write_doc(DOCS / "tau_cmb_phi_tau_parent_certificate_closure_decision_v01.md", rows, row)
    print("TAU_CMB_PHI_TAU_PARENT_CERTIFICATE_CLOSURE_DECISION_V01_BUILT")


if __name__ == "__main__":
    main()
