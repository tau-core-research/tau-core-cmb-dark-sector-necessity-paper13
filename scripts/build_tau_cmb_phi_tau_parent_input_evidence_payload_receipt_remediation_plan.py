#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan_v01_remediation_plan_only_"
    "no_payload_materialized_no_remediation_completed_no_receipt_validated_no_package_pass_no_certificate_pass_"
    "no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "remediation_row_id",
    "blocker_component",
    "target_payload_component",
    "remediation_status",
    "remediation_source",
    "missing_payload_object",
    "required_remediation_action",
    "required_receipt_binding",
    "required_evidence_bundle",
    "acceptance_exit_gate",
    "priority",
    "payload_received",
    "remediation_completed",
    "receipt_validated",
    "receipt_accepted",
    "dimension_payload_received",
    "replay_payload_received",
    "firewall_payload_received",
    "evidence_package_passed",
    "certificate_passed",
    "payload_accepted",
    "scoring_input_accepted",
    "hard_failure_triggered",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "remediation_rows_declared",
    "payload_received_rows",
    "remediation_completed_rows",
    "receipt_validated_rows",
    "receipt_accepted_rows",
    "dimension_payload_received_rows",
    "replay_payload_received_rows",
    "firewall_payload_received_rows",
    "evidence_package_passed_rows",
    "certificate_passed_rows",
    "accepted_rows",
    "scoring_input_accepted_rows",
    "hard_failures_triggered",
    "evidence_payload_receipt_remediation_plan_satisfied",
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


def remediation_rows() -> list[dict[str, str]]:
    rows = [
        (
            "certificate_candidate_manifest_identity",
            "all_parent_payload_rows",
            "endpoint-blind manifest payload bundle",
            "supply manifest payload object with stable row ids and hashes",
            "manifest object, provenance hash, replay command, artifact path",
        ),
        (
            "base_field_dimension_replay_certificate_candidate",
            "base_field_state_payload_candidate",
            "endpoint-blind B_tau state payload",
            "supply base-field dimensional payload and replay certificate",
            "B_tau state object, dimensional audit hash, replay command, artifact path",
        ),
        (
            "seed_dimension_replay_certificate_candidate",
            "morphological_seed_payload_candidate",
            "endpoint-blind seed_tau payload",
            "supply morphological-seed payload and replay certificate",
            "seed_tau object, dimensional audit hash, replay command, artifact path",
        ),
        (
            "operator_dimension_replay_certificate_candidate",
            "response_operator_payload_candidate",
            "endpoint-blind R_tau response-operator payload",
            "supply response-operator payload and replay certificate",
            "R_tau object, dimensional audit hash, replay command, artifact path",
        ),
        (
            "gauge_normalization_replay_certificate_candidate",
            "gauge_normalization_payload_candidate",
            "endpoint-blind gauge and normalization payload",
            "supply gauge/normalization payload and replay certificate",
            "gauge-normalization object, convention hash, replay command, artifact path",
        ),
        (
            "payload_firewall_certificate_candidate",
            "endpoint_firewall_payload_candidate",
            "endpoint-firewall payload bundle",
            "supply aggregate firewall payload before any CMB endpoint labels are used",
            "firewall object, endpoint-blindness hash, replay command, artifact path",
        ),
        (
            "executable_replay_certificate_candidate",
            "provenance_replay_payload_candidate",
            "executable replay/provenance payload",
            "supply executable replay payload with deterministic command and artifact paths",
            "replay object, source hash, replay command, artifact path",
        ),
    ]
    return [
        {
            "remediation_row_id": f"TCMBPTPIPEPRP01_{index:03d}",
            "blocker_component": component,
            "target_payload_component": target,
            "remediation_status": "REMEDIATION_DECLARED_NOT_COMPLETED",
            "remediation_source": "tau_cmb_phi_tau_parent_input_evidence_payload_receipt_audit_v01",
            "missing_payload_object": missing,
            "required_remediation_action": action,
            "required_receipt_binding": binding,
            "required_evidence_bundle": "payload object plus provenance hash plus replay command plus artifact path",
            "acceptance_exit_gate": "may exit only after matching payload and receipt are supplied and audit-passed",
            "priority": str(index),
            "payload_received": "false",
            "remediation_completed": "false",
            "receipt_validated": "false",
            "receipt_accepted": "false",
            "dimension_payload_received": "false",
            "replay_payload_received": "false",
            "firewall_payload_received": "false",
            "evidence_package_passed": "false",
            "certificate_passed": "false",
            "payload_accepted": "false",
            "scoring_input_accepted": "false",
            "hard_failure_triggered": "false",
            "blocks_no_dark_claim": "true",
            "allows_tau_response_claim": "false",
            "allows_dark_sector_verdict": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, (component, target, missing, action, binding) in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_RECEIPT_REMEDIATION_PLAN_V01",
            "remediation_rows_declared": len(rows),
            "payload_received_rows": sum(row["payload_received"] == "true" for row in rows),
            "remediation_completed_rows": sum(row["remediation_completed"] == "true" for row in rows),
            "receipt_validated_rows": sum(row["receipt_validated"] == "true" for row in rows),
            "receipt_accepted_rows": sum(row["receipt_accepted"] == "true" for row in rows),
            "dimension_payload_received_rows": sum(row["dimension_payload_received"] == "true" for row in rows),
            "replay_payload_received_rows": sum(row["replay_payload_received"] == "true" for row in rows),
            "firewall_payload_received_rows": sum(row["firewall_payload_received"] == "true" for row in rows),
            "evidence_package_passed_rows": sum(row["evidence_package_passed"] == "true" for row in rows),
            "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
            "accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "evidence_payload_receipt_remediation_plan_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_RECEIPT_REMEDIATION_PLAN_DECLARED_NOT_COMPLETED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_materialization_packet_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Receipt Remediation Plan v01

**Doc class:** parent-input evidence payload receipt remediation plan
**Status:** remediation actions declared but not completed; no payload materialized, no receipt validated, no package pass, no certificate pass, no payload pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan_summary_v01.csv
```

This artifact declares the remediation actions required after the receipt audit
failed without payload records. It does not supply or validate any payload.

The evidence payload receipt remediation plan is not satisfied:

```text
evidence_payload_receipt_remediation_plan_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_materialization_packet_v01
```

## Claim Boundary

This artifact declares remediation actions only. It materializes no parent-side
payload, validates no receipt, accepts no receipt, provides no evidence-package
pass, provides no certificate pass, accepts no parent-side Tau inputs, derives
no `Phi_tau_eff`, computes no score, supplies no CMB likelihood, declares no
reproduction or failure, validates no Tau-response source, and permits no
no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = remediation_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_RECEIPT_REMEDIATION_PLAN_V01_BUILT")


if __name__ == "__main__":
    main()
