#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_v01_unblock_plan_only_"
    "no_unblock_completed_no_payload_materialized_no_packet_accepted_no_acceptance_pass_no_package_pass_"
    "no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
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
    "payload_materialized",
    "packet_accepted",
    "receipt_validated",
    "receipt_accepted",
    "dimension_payload_received",
    "replay_payload_received",
    "firewall_payload_received",
    "acceptance_precheck_passed",
    "unblock_completed",
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
    "unblock_rows_declared",
    "unblock_completed_rows",
    "payload_materialized_rows",
    "packet_accepted_rows",
    "receipt_validated_rows",
    "receipt_accepted_rows",
    "dimension_payload_received_rows",
    "replay_payload_received_rows",
    "firewall_payload_received_rows",
    "acceptance_precheck_passed_rows",
    "evidence_package_passed_rows",
    "certificate_passed_rows",
    "accepted_rows",
    "scoring_input_accepted_rows",
    "hard_failures_triggered",
    "evidence_payload_acceptance_unblock_plan_satisfied",
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


def unblock_rows() -> list[dict[str, str]]:
    rows = [
        (
            "materialization_unblock",
            "materialization_gate",
            "materialize endpoint-blind payload packets with stable ids and content hashes",
            "materialized payload packet bundle",
        ),
        (
            "receipt_unblock",
            "receipt_gate",
            "bind payload packets to receipts, hashes, replay commands, and artifact paths",
            "validated receipt bundle",
        ),
        (
            "dimension_unblock",
            "dimension_gate",
            "attach dimension and convention audit passes for every payload packet",
            "dimension/convention audit bundle",
        ),
        (
            "replay_unblock",
            "replay_gate",
            "attach deterministic replay commands and reproduced artifacts",
            "replay evidence bundle",
        ),
        (
            "firewall_unblock",
            "firewall_gate",
            "pass endpoint-blindness firewall before CMB endpoint labels are used",
            "endpoint-blindness firewall pass",
        ),
        (
            "evidence_package_unblock",
            "evidence_package_gate",
            "assemble accepted packets into the parent-input evidence package",
            "accepted evidence package bundle",
        ),
        (
            "scoring_acceptance_unblock",
            "scoring_input_gate",
            "promote accepted evidence package into scoring input only after all upstream gates pass",
            "scoring input acceptance record",
        ),
    ]
    return [
        {
            "unblock_row_id": f"TCMBPTPIPEPAU01_{index:03d}",
            "unblock_component": component,
            "blocked_gate": gate,
            "unblock_status": "UNBLOCK_DECLARED_NOT_COMPLETED",
            "unblock_source": "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_v01",
            "required_unblock_action": action,
            "required_evidence_object": evidence,
            "required_exit_condition": "gate may exit only after evidence object is supplied and audit-passed",
            "unblock_priority": str(index),
            "payload_materialized": "false",
            "packet_accepted": "false",
            "receipt_validated": "false",
            "receipt_accepted": "false",
            "dimension_payload_received": "false",
            "replay_payload_received": "false",
            "firewall_payload_received": "false",
            "acceptance_precheck_passed": "false",
            "unblock_completed": "false",
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
        for index, (component, gate, action, evidence) in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_ACCEPTANCE_UNBLOCK_PLAN_V01",
            "unblock_rows_declared": len(rows),
            "unblock_completed_rows": sum(row["unblock_completed"] == "true" for row in rows),
            "payload_materialized_rows": sum(row["payload_materialized"] == "true" for row in rows),
            "packet_accepted_rows": sum(row["packet_accepted"] == "true" for row in rows),
            "receipt_validated_rows": sum(row["receipt_validated"] == "true" for row in rows),
            "receipt_accepted_rows": sum(row["receipt_accepted"] == "true" for row in rows),
            "dimension_payload_received_rows": sum(row["dimension_payload_received"] == "true" for row in rows),
            "replay_payload_received_rows": sum(row["replay_payload_received"] == "true" for row in rows),
            "firewall_payload_received_rows": sum(row["firewall_payload_received"] == "true" for row in rows),
            "acceptance_precheck_passed_rows": sum(row["acceptance_precheck_passed"] == "true" for row in rows),
            "evidence_package_passed_rows": sum(row["evidence_package_passed"] == "true" for row in rows),
            "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
            "accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "evidence_payload_acceptance_unblock_plan_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_ACCEPTANCE_UNBLOCK_PLAN_DECLARED_NOT_COMPLETED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Acceptance Unblock Plan v01

**Doc class:** parent-input evidence payload acceptance unblock plan
**Status:** unblock actions declared but not completed; no payload accepted, no package pass, no certificate pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_summary_v01.csv
```

This artifact declares the ordered actions required to unblock payload
acceptance. No unblock action is completed and no payload is accepted.

The evidence payload acceptance unblock plan is not satisfied:

```text
evidence_payload_acceptance_unblock_plan_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_v01
```

## Claim Boundary

This artifact declares acceptance-unblock actions only. It materializes no
parent-side payload, validates no receipt, accepts no receipt, provides no
evidence-package pass, provides no certificate pass, accepts no parent-side Tau
inputs, derives no `Phi_tau_eff`, computes no score, supplies no CMB likelihood,
declares no reproduction or failure, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = unblock_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_ACCEPTANCE_UNBLOCK_PLAN_V01_BUILT")


if __name__ == "__main__":
    main()
