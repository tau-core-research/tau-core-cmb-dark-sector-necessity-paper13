#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

PACKET_ID = "TAU_CMB_PHI_TAU_PARENT_EVIDENCE_PACKAGE_CLOSURE_DECISION_V01"
CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_evidence_package_closure_decision_v01_decision_only_"
    "evidence_package_unpopulated_no_certificate_pass_no_parent_input_acceptance_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

ROW_FIELDS = [
    "closure_row_id",
    "evidence_component",
    "target_payload_component",
    "evidence_closure_status",
    "evidence_requested",
    "package_candidate_declared",
    "package_audited",
    "evidence_payload_supplied",
    "dimension_evidence_supplied",
    "replay_evidence_supplied",
    "firewall_evidence_supplied",
    "evidence_package_passed",
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
    "evidence_closure_rows_declared",
    "evidence_requested_rows",
    "package_candidate_declared_rows",
    "package_audited_rows",
    "evidence_payload_supplied_rows",
    "dimension_evidence_supplied_rows",
    "replay_evidence_supplied_rows",
    "firewall_evidence_supplied_rows",
    "evidence_package_passed_rows",
    "certificate_passed_rows",
    "payload_accepted_rows",
    "closed_rows",
    "blocked_rows",
    "phi_tau_parent_evidence_package_closed",
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
            "BLOCKED_MANIFEST_EVIDENCE_PAYLOAD_MISSING",
            "package manifest evidence payload and stable artifact hashes are not supplied",
            "keeps the whole parent evidence package outside scoring acceptance",
        ),
        (
            "base_field_dimension_replay_certificate_candidate",
            "base_field_state_payload_candidate",
            "BLOCKED_BASE_FIELD_EVIDENCE_PAYLOAD_MISSING",
            "B_tau dimension certificate, endpoint-blind replay trace, and firewall trace payloads are absent",
            "blocks density-amplitude and potential-source scoring inputs",
        ),
        (
            "seed_dimension_replay_certificate_candidate",
            "morphological_seed_payload_candidate",
            "BLOCKED_SEED_EVIDENCE_PAYLOAD_MISSING",
            "seed_tau scale certificate, endpoint-blind replay trace, and firewall trace payloads are absent",
            "blocks source-activation and readout-compatibility scoring inputs",
        ),
        (
            "operator_dimension_replay_certificate_candidate",
            "response_operator_payload_candidate",
            "BLOCKED_OPERATOR_EVIDENCE_PAYLOAD_MISSING",
            "R_tau dimensional-map certificate, endpoint-blind replay trace, and firewall trace payloads are absent",
            "blocks Phi_tau_eff derivation and transfer-kernel scoring inputs",
        ),
        (
            "gauge_normalization_replay_certificate_candidate",
            "gauge_normalization_payload_candidate",
            "BLOCKED_NORMALIZATION_EVIDENCE_PAYLOAD_MISSING",
            "gauge/sign/unit/normalization lock certificate, metadata replay, and firewall trace payloads are absent",
            "blocks acoustic, lensing, and growth comparisons outside scoring acceptance",
        ),
        (
            "payload_firewall_certificate_candidate",
            "endpoint_firewall_payload_candidate",
            "BLOCKED_PAYLOAD_FIREWALL_EVIDENCE_MISSING",
            "row-level evidence payload references and payload-wide firewall certificate payload are absent",
            "blocks accepting the full parent-input payload",
        ),
        (
            "executable_replay_certificate_candidate",
            "provenance_replay_payload_candidate",
            "BLOCKED_EXECUTABLE_REPLAY_EVIDENCE_MISSING",
            "endpoint-blind executable replay trace and input provenance hash payloads are absent",
            "blocks transition from evidence package audit to scoring input acceptance",
        ),
    ]
    rows: list[dict[str, str]] = []
    for index, (component, target, status, blocker, effect) in enumerate(base_rows, start=1):
        rows.append(
            {
                "closure_row_id": f"TCMBPTPEPCD01_{index:03d}",
                "evidence_component": component,
                "target_payload_component": target,
                "evidence_closure_status": status,
                "evidence_requested": "true",
                "package_candidate_declared": "true",
                "package_audited": "true",
                "evidence_payload_supplied": "false",
                "dimension_evidence_supplied": "false",
                "replay_evidence_supplied": "false",
                "firewall_evidence_supplied": "false",
                "evidence_package_passed": "false",
                "certificate_passed": "false",
                "payload_accepted": "false",
                "closure_decision": "BLOCKED_EVIDENCE_PACKAGE_NOT_CLOSED",
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
        "evidence_closure_rows_declared": str(len(rows)),
        "evidence_requested_rows": str(sum(row["evidence_requested"] == "true" for row in rows)),
        "package_candidate_declared_rows": str(sum(row["package_candidate_declared"] == "true" for row in rows)),
        "package_audited_rows": str(sum(row["package_audited"] == "true" for row in rows)),
        "evidence_payload_supplied_rows": str(sum(row["evidence_payload_supplied"] == "true" for row in rows)),
        "dimension_evidence_supplied_rows": str(sum(row["dimension_evidence_supplied"] == "true" for row in rows)),
        "replay_evidence_supplied_rows": str(sum(row["replay_evidence_supplied"] == "true" for row in rows)),
        "firewall_evidence_supplied_rows": str(sum(row["firewall_evidence_supplied"] == "true" for row in rows)),
        "evidence_package_passed_rows": str(sum(row["evidence_package_passed"] == "true" for row in rows)),
        "certificate_passed_rows": str(sum(row["certificate_passed"] == "true" for row in rows)),
        "payload_accepted_rows": str(sum(row["payload_accepted"] == "true" for row in rows)),
        "closed_rows": str(sum(row["closure_decision"].startswith("CLOSED") for row in rows)),
        "blocked_rows": str(sum(row["closure_decision"].startswith("BLOCKED") for row in rows)),
        "phi_tau_parent_evidence_package_closed": "false",
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
        "overall_status": "PHI_TAU_PARENT_EVIDENCE_PACKAGE_DECLARED_AND_AUDITED_BUT_UNCLOSED_SCORE_BLOCKED",
        "next_required_artifact": "tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck_v01",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_json(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "phi_tau_parent_evidence_package_closure_decision",
        "status": row["overall_status"],
        "claim_boundary": CLAIM_BOUNDARY,
        "closure_rows": rows,
        "summary": row,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_doc(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    lines = [
        "# Tau CMB Phi Tau Parent Evidence Package Closure Decision v01",
        "",
        "**Doc class:** parent evidence-package closure decision",
        "**Reader role:** Paper 13 CMB peak scoring path",
        "**Status:** evidence requested, package declared, and package audited; evidence package not closed; score blocked",
        "**Canonical parent:** Paper 13 CMB scoring input fulfillment chain",
        "",
        "## Purpose",
        "",
        "This artifact consolidates the certificate evidence request, evidence-package candidate, and evidence-package audit into one closure decision. It asks whether the parent-side evidence package is populated enough to become endpoint-blind scoring input for `Phi_tau_eff(a,k)`.",
        "",
        "## Summary",
        "",
        f"- evidence_closure_rows_declared = {row['evidence_closure_rows_declared']}",
        f"- evidence_requested_rows = {row['evidence_requested_rows']}",
        f"- package_candidate_declared_rows = {row['package_candidate_declared_rows']}",
        f"- package_audited_rows = {row['package_audited_rows']}",
        f"- evidence_payload_supplied_rows = {row['evidence_payload_supplied_rows']}",
        f"- dimension_evidence_supplied_rows = {row['dimension_evidence_supplied_rows']}",
        f"- replay_evidence_supplied_rows = {row['replay_evidence_supplied_rows']}",
        f"- firewall_evidence_supplied_rows = {row['firewall_evidence_supplied_rows']}",
        f"- evidence_package_passed_rows = {row['evidence_package_passed_rows']}",
        f"- certificate_passed_rows = {row['certificate_passed_rows']}",
        f"- payload_accepted_rows = {row['payload_accepted_rows']}",
        f"- phi_tau_parent_evidence_package_closed = {row['phi_tau_parent_evidence_package_closed']}",
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
            f"| {closure_row['evidence_component']} | {closure_row['target_payload_component']} | "
            f"{closure_row['evidence_closure_status']} |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            "The evidence-package layer is not closed. Evidence has been requested, package slots have been declared, and the package has been audited, but no dimension, replay, or firewall evidence payload is supplied; no evidence-package row passes; no certificate passes; and no parent payload is accepted.",
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
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_evidence_package_closure_decision_v01.csv", rows, ROW_FIELDS)
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_evidence_package_closure_decision_summary_v01.csv", [row], SUMMARY_FIELDS)
    write_json(DERIVED / "tau_cmb_phi_tau_parent_evidence_package_closure_decision_v01.json", rows, row)
    write_doc(DOCS / "tau_cmb_phi_tau_parent_evidence_package_closure_decision_v01.md", rows, row)
    print("TAU_CMB_PHI_TAU_PARENT_EVIDENCE_PACKAGE_CLOSURE_DECISION_V01_BUILT")


if __name__ == "__main__":
    main()
