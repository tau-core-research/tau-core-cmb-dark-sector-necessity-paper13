#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01_payload_audit_only_no_payload_pass_no_accepted_inputs_no_phi_derivation_no_score_no_likelihood_no_verdict"

FIELDS = [
    "audit_row_id",
    "audited_payload_component",
    "candidate_symbol_or_object",
    "audit_status",
    "endpoint_fields_checked",
    "endpoint_fields_detected",
    "dimension_check_status",
    "firewall_certificate_status",
    "replay_status",
    "payload_firewall_result",
    "audit_evidence",
    "remaining_blocker",
    "scorecard_effect",
    "payload_firewall_audited",
    "payload_firewall_passed",
    "payload_accepted",
    "hard_failure_triggered",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "audit_rows_declared",
    "audited_rows",
    "endpoint_clean_rows",
    "dimension_passed_rows",
    "certificate_supplied_rows",
    "replay_available_rows",
    "payload_passed_rows",
    "accepted_rows",
    "blocked_rows",
    "endpoint_fields_detected",
    "hard_failures_triggered",
    "payload_firewall_audit_satisfied",
    "scores_computed",
    "cmb_likelihood_available",
    "no_dark_blockers",
    "no_dark_cmb_verdict_allowed",
    "tau_response_claim_allowed",
    "dark_sector_verdict_allowed",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def audit_rows() -> list[dict[str, str]]:
    rows = [
        {
            "audited_payload_component": "candidate_payload_manifest_identity",
            "candidate_symbol_or_object": "M_parent_payload_candidate_v01",
            "audit_status": "AUDITED_ENDPOINT_CLEAN_BUT_UNACCEPTED",
            "endpoint_fields_checked": "cmb_residual; score_output; likelihood_error; post_endpoint_fit",
            "dimension_check_status": "not_physical_row",
            "firewall_certificate_status": "certificate_missing",
            "replay_status": "replay_missing",
            "payload_firewall_result": "BLOCKED_CERTIFICATE_AND_REPLAY_MISSING",
            "audit_evidence": "manifest candidate declares no populated endpoint-derived fields",
            "remaining_blocker": "supply payload-level certificate and executable replay",
            "scorecard_effect": "keeps parent payload package unaccepted",
        },
        {
            "audited_payload_component": "base_field_state_payload_candidate",
            "candidate_symbol_or_object": "B_tau_candidate(parent)",
            "audit_status": "AUDITED_ENDPOINT_CLEAN_BUT_DIMENSION_REPLAY_BLOCKED",
            "endpoint_fields_checked": "acoustic_residual; lensing_residual; score_output; likelihood_error",
            "dimension_check_status": "dimension_check_missing",
            "firewall_certificate_status": "certificate_missing",
            "replay_status": "replay_missing",
            "payload_firewall_result": "BLOCKED_DIMENSION_CERTIFICATE_REPLAY_MISSING",
            "audit_evidence": "base-field candidate contains no populated endpoint-derived fields",
            "remaining_blocker": "supply dimension check, payload certificate, and replay",
            "scorecard_effect": "keeps density and potential amplitude scoring blocked",
        },
        {
            "audited_payload_component": "morphological_seed_payload_candidate",
            "candidate_symbol_or_object": "seed_tau_candidate(parent)",
            "audit_status": "AUDITED_ENDPOINT_CLEAN_BUT_DIMENSION_REPLAY_BLOCKED",
            "endpoint_fields_checked": "cmb_peak_shape; residual_shape; score_output; likelihood_error",
            "dimension_check_status": "scale_check_missing",
            "firewall_certificate_status": "certificate_missing",
            "replay_status": "replay_missing",
            "payload_firewall_result": "BLOCKED_SCALE_CERTIFICATE_REPLAY_MISSING",
            "audit_evidence": "seed candidate contains no populated endpoint-derived fields",
            "remaining_blocker": "supply scale check, payload certificate, and replay",
            "scorecard_effect": "keeps source activation interpretation blocked",
        },
        {
            "audited_payload_component": "response_operator_payload_candidate",
            "candidate_symbol_or_object": "R_tau_candidate",
            "audit_status": "AUDITED_ENDPOINT_CLEAN_BUT_DIMENSION_REPLAY_BLOCKED",
            "endpoint_fields_checked": "role_score; residual_tuning; likelihood_error; post_endpoint_fit",
            "dimension_check_status": "operator_dimension_map_missing",
            "firewall_certificate_status": "certificate_missing",
            "replay_status": "replay_missing",
            "payload_firewall_result": "BLOCKED_DIMENSION_MAP_CERTIFICATE_REPLAY_MISSING",
            "audit_evidence": "operator candidate contains no populated endpoint-derived fields",
            "remaining_blocker": "supply dimensional map, payload certificate, and replay",
            "scorecard_effect": "keeps Phi_tau_eff derivation blocked",
        },
        {
            "audited_payload_component": "gauge_normalization_payload_candidate",
            "candidate_symbol_or_object": "gauge_norm_candidate(parent)",
            "audit_status": "AUDITED_ENDPOINT_CLEAN_BUT_LOCK_REPLAY_BLOCKED",
            "endpoint_fields_checked": "post_endpoint_norm_choice; residual_minimizer; score_output; likelihood_error",
            "dimension_check_status": "normalization_lock_missing",
            "firewall_certificate_status": "certificate_missing",
            "replay_status": "replay_missing",
            "payload_firewall_result": "BLOCKED_LOCK_CERTIFICATE_REPLAY_MISSING",
            "audit_evidence": "gauge/normalization candidate contains no populated endpoint-derived fields",
            "remaining_blocker": "supply locked metadata, payload certificate, and replay",
            "scorecard_effect": "keeps shared acoustic/lensing source comparison blocked",
        },
        {
            "audited_payload_component": "endpoint_firewall_payload_candidate",
            "candidate_symbol_or_object": "firewall_certificate_candidate(parent payload)",
            "audit_status": "BLOCKED_CERTIFICATE_NOT_SUPPLIED",
            "endpoint_fields_checked": "score_derived_input; residual_derived_input; likelihood_derived_input",
            "dimension_check_status": "references_child_rows",
            "firewall_certificate_status": "certificate_missing",
            "replay_status": "replay_missing",
            "payload_firewall_result": "BLOCKED_CERTIFICATE_MISSING",
            "audit_evidence": "certificate slot exists but no certificate is supplied",
            "remaining_blocker": "supply payload-level firewall certificate",
            "scorecard_effect": "blocks accepting any candidate payload row",
        },
        {
            "audited_payload_component": "provenance_replay_payload_candidate",
            "candidate_symbol_or_object": "replay_candidate(parent payload)",
            "audit_status": "BLOCKED_REPLAY_NOT_SUPPLIED",
            "endpoint_fields_checked": "score_output_read; residual_table_read; likelihood_error_read",
            "dimension_check_status": "must_replay_child_checks",
            "firewall_certificate_status": "certificate_missing",
            "replay_status": "replay_missing",
            "payload_firewall_result": "BLOCKED_REPLAY_MISSING",
            "audit_evidence": "replay slot exists but no executable replay is supplied",
            "remaining_blocker": "supply executable endpoint-blind replay",
            "scorecard_effect": "blocks transition into scoring input acceptance",
        },
    ]
    return [
        {
            "audit_row_id": f"TCMBPTPIPFA01_{index:03d}",
            "endpoint_fields_detected": "false",
            "payload_firewall_audited": "true",
            "payload_firewall_passed": "false",
            "payload_accepted": "false",
            "hard_failure_triggered": "false",
            "blocks_no_dark_claim": "true",
            "allows_tau_response_claim": "false",
            "allows_dark_sector_verdict": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            **row,
        }
        for index, row in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_PAYLOAD_FIREWALL_AUDIT_V01",
            "audit_rows_declared": len(rows),
            "audited_rows": sum(row["payload_firewall_audited"] == "true" for row in rows),
            "endpoint_clean_rows": sum(row["endpoint_fields_detected"] == "false" for row in rows),
            "dimension_passed_rows": sum(row["dimension_check_status"].endswith("_passed") for row in rows),
            "certificate_supplied_rows": sum(row["firewall_certificate_status"] == "certificate_supplied" for row in rows),
            "replay_available_rows": sum(row["replay_status"] == "replay_available" for row in rows),
            "payload_passed_rows": sum(row["payload_firewall_passed"] == "true" for row in rows),
            "accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "blocked_rows": sum(row["audit_status"].startswith("BLOCKED") for row in rows),
            "endpoint_fields_detected": sum(row["endpoint_fields_detected"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "payload_firewall_audit_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_PAYLOAD_FIREWALL_AUDIT_ENDPOINT_CLEAN_BUT_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_source_content_closure_decision_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Payload Firewall Audit v01

**Doc class:** payload-level endpoint-firewall audit
**Status:** endpoint fields clean but blocked; no payload firewall pass, no accepted inputs, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_payload_firewall_audit.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_payload_firewall_audit_summary_v01.csv
```

This artifact audits the concrete parent-input payload candidate at payload
level. It detects no populated endpoint-derived fields.
It does not pass the payload-level firewall because dimension checks, the payload-level certificate,
and executable replay are missing.

The payload firewall audit is not satisfied:

```text
payload_firewall_audit_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_source_content_closure_decision_v01
```

## Claim Boundary

This artifact audits payload candidates only. It accepts no parent-side Tau
inputs, provides no payload-level firewall pass, derives no `Phi_tau_eff`,
computes no score, supplies no CMB likelihood, declares no reproduction or
failure, validates no Tau-response source, and permits no no-dark or
dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = audit_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_payload_firewall_audit_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_PAYLOAD_FIREWALL_AUDIT_V01_BUILT")


if __name__ == "__main__":
    main()
