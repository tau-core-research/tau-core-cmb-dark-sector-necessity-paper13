#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_v01_"
    "unblock_plan_only_no_unblock_completed_no_execution_allowed_no_scoring_input_accepted_"
    "no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "unblock_row_id",
    "unblock_component",
    "blocked_gate",
    "unblock_status",
    "unblock_source",
    "required_unblock_action",
    "required_evidence_object",
    "required_exit_condition",
    "unblock_priority",
    "execution_packet_audited",
    "payload_supplied",
    "completion_evidence_supplied",
    "provenance_supplied",
    "replay_supplied",
    "hash_manifest_supplied",
    "firewall_attestation_supplied",
    "payload_accepted",
    "scoring_input_accepted",
    "unblock_completed",
    "can_execute",
    "execution_attempted",
    "execution_succeeded",
    "evidence_package_passed",
    "certificate_passed",
    "phi_tau_eff_derived",
    "scores_computed",
    "cmb_likelihood_available",
    "hard_failure_triggered",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "unblock_rows_declared",
    "execution_packet_audited_rows",
    "unblock_completed_rows",
    "payload_supplied_rows",
    "completion_evidence_supplied_rows",
    "provenance_supplied_rows",
    "replay_supplied_rows",
    "hash_manifest_supplied_rows",
    "firewall_attestation_supplied_rows",
    "payload_accepted_rows",
    "scoring_input_accepted_rows",
    "can_execute_rows",
    "execution_attempted_rows",
    "execution_succeeded_rows",
    "evidence_package_passed_rows",
    "certificate_passed_rows",
    "phi_tau_eff_derived_rows",
    "scores_computed_rows",
    "cmb_likelihood_available_rows",
    "hard_failures_triggered",
    "evidence_payload_scoring_input_payload_submission_execution_unblock_plan_satisfied",
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


def unblock_rows() -> list[dict[str, str]]:
    rows = [
        (
            "payload_supply_unblock",
            "payload_supply_gate",
            "supply all seven required submission payload files with stable component ids",
            "complete submission payload bundle",
        ),
        (
            "completion_evidence_unblock",
            "completion_evidence_gate",
            "attach completion evidence proving each requested payload slot is actually populated",
            "per-payload completion evidence bundle",
        ),
        (
            "provenance_unblock",
            "provenance_gate",
            "attach source paths, construction stage, timestamps, and hashes for every payload file",
            "per-payload provenance bundle",
        ),
        (
            "replay_unblock",
            "replay_gate",
            "attach deterministic replay commands and environment pins for each payload construction",
            "per-payload replay command bundle",
        ),
        (
            "hash_manifest_unblock",
            "hash_manifest_gate",
            "attach row-level and file-level hash manifests for every submitted payload",
            "hash manifest bundle",
        ),
        (
            "firewall_unblock",
            "endpoint_firewall_gate",
            "attach endpoint-blind firewall attestation excluding CMB target leakage and posterior tuning",
            "endpoint firewall attestation bundle",
        ),
        (
            "acceptance_unblock",
            "payload_and_scoring_input_acceptance_gate",
            "accept payload and scoring input only after all upstream evidence objects audit-pass",
            "payload acceptance and scoring-input acceptance record",
        ),
    ]
    return [
        {
            "unblock_row_id": f"TCMBPTPIPEPSIPSEUP01_{index:03d}",
            "unblock_component": component,
            "blocked_gate": gate,
            "unblock_status": "EXECUTION_UNBLOCK_DECLARED_NOT_COMPLETED",
            "unblock_source": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_audit_v01",
            "required_unblock_action": action,
            "required_evidence_object": evidence,
            "required_exit_condition": "gate may exit only after required evidence object is supplied and audit-passed without endpoint leakage",
            "unblock_priority": str(index),
            "execution_packet_audited": "true",
            "payload_supplied": "false",
            "completion_evidence_supplied": "false",
            "provenance_supplied": "false",
            "replay_supplied": "false",
            "hash_manifest_supplied": "false",
            "firewall_attestation_supplied": "false",
            "payload_accepted": "false",
            "scoring_input_accepted": "false",
            "unblock_completed": "false",
            "can_execute": "false",
            "execution_attempted": "false",
            "execution_succeeded": "false",
            "evidence_package_passed": "false",
            "certificate_passed": "false",
            "phi_tau_eff_derived": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "hard_failure_triggered": "false",
            "blocks_no_dark_claim": "true",
            "allows_tau_response_claim": "false",
            "allows_dark_sector_verdict": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, (component, gate, action, evidence) in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EXECUTION_UNBLOCK_PLAN_V01",
            "unblock_rows_declared": len(rows),
            "execution_packet_audited_rows": sum(row["execution_packet_audited"] == "true" for row in rows),
            "unblock_completed_rows": sum(row["unblock_completed"] == "true" for row in rows),
            "payload_supplied_rows": sum(row["payload_supplied"] == "true" for row in rows),
            "completion_evidence_supplied_rows": sum(
                row["completion_evidence_supplied"] == "true" for row in rows
            ),
            "provenance_supplied_rows": sum(row["provenance_supplied"] == "true" for row in rows),
            "replay_supplied_rows": sum(row["replay_supplied"] == "true" for row in rows),
            "hash_manifest_supplied_rows": sum(row["hash_manifest_supplied"] == "true" for row in rows),
            "firewall_attestation_supplied_rows": sum(row["firewall_attestation_supplied"] == "true" for row in rows),
            "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "can_execute_rows": sum(row["can_execute"] == "true" for row in rows),
            "execution_attempted_rows": sum(row["execution_attempted"] == "true" for row in rows),
            "execution_succeeded_rows": sum(row["execution_succeeded"] == "true" for row in rows),
            "evidence_package_passed_rows": sum(row["evidence_package_passed"] == "true" for row in rows),
            "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
            "phi_tau_eff_derived_rows": sum(row["phi_tau_eff_derived"] == "true" for row in rows),
            "scores_computed_rows": sum(row["scores_computed"] == "true" for row in rows),
            "cmb_likelihood_available_rows": sum(row["cmb_likelihood_available"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "evidence_payload_scoring_input_payload_submission_execution_unblock_plan_satisfied": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EXECUTION_UNBLOCK_PLAN_DECLARED_NOT_COMPLETED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_audit_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (
        DOCS
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_v01.md"
    ).write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Execution Unblock Plan v01

**Doc class:** parent-input evidence payload scoring input payload submission execution unblock plan
**Status:** unblock plan declared but not completed; no execution allowed, no payload accepted, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_summary_v01.csv
```

This artifact declares the ordered actions required to unblock the audited
submission execution packet. No unblock action is completed and execution
remains disallowed.

The evidence payload scoring input payload submission execution unblock plan is
not satisfied:

```text
evidence_payload_scoring_input_payload_submission_execution_unblock_plan_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_audit_v01
```

## Claim Boundary

This artifact declares an unblock plan only. It executes nothing, accepts no
parent-side payload, provides no evidence-package pass, provides no certificate
pass, accepts no scoring input, derives no `Phi_tau_eff`, computes no score,
supplies no CMB likelihood, validates no Tau-response source, and permits no
no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = unblock_rows()
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_v01.csv",
        rows,
        FIELDS,
    )
    write_csv(
        DERIVED
        / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()


if __name__ == "__main__":
    main()
