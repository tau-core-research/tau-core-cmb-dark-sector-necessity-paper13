#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_v01_decision_gate_only_"
    "no_acceptance_allowed_no_payload_accepted_no_scoring_input_accepted_no_package_pass_no_certificate_pass_"
    "no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "decision_row_id",
    "decision_component",
    "target_gate",
    "decision_gate_status",
    "decision_source",
    "required_prior_pass",
    "decision_rule",
    "decision_reason",
    "decision_output",
    "unblock_completed",
    "payload_materialized",
    "packet_accepted",
    "receipt_validated",
    "receipt_accepted",
    "dimension_payload_received",
    "replay_payload_received",
    "firewall_payload_received",
    "acceptance_precheck_passed",
    "acceptance_allowed",
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
    "decision_rows_declared",
    "acceptance_allowed_rows",
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
    "evidence_payload_acceptance_decision_gate_satisfied",
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


def decision_rows() -> list[dict[str, str]]:
    rows = [
        ("materialization_decision", "materialization_gate", "materialization unblock completion"),
        ("receipt_decision", "receipt_gate", "receipt unblock completion"),
        ("dimension_decision", "dimension_gate", "dimension unblock completion"),
        ("replay_decision", "replay_gate", "replay unblock completion"),
        ("firewall_decision", "firewall_gate", "firewall unblock completion"),
        ("evidence_package_decision", "evidence_package_gate", "evidence package unblock completion"),
        ("scoring_input_decision", "scoring_input_gate", "scoring input unblock completion"),
    ]
    return [
        {
            "decision_row_id": f"TCMBPTPIPEPAD01_{index:03d}",
            "decision_component": component,
            "target_gate": gate,
            "decision_gate_status": "ACCEPTANCE_DECISION_CLOSED_UNBLOCK_NOT_COMPLETED",
            "decision_source": "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_v01",
            "required_prior_pass": required,
            "decision_rule": "acceptance may open only if all upstream evidence gates are completed and audit-passed",
            "decision_reason": "acceptance unblock plan is not satisfied",
            "decision_output": "acceptance_closed",
            "unblock_completed": "false",
            "payload_materialized": "false",
            "packet_accepted": "false",
            "receipt_validated": "false",
            "receipt_accepted": "false",
            "dimension_payload_received": "false",
            "replay_payload_received": "false",
            "firewall_payload_received": "false",
            "acceptance_precheck_passed": "false",
            "acceptance_allowed": "false",
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
        for index, (component, gate, required) in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_ACCEPTANCE_DECISION_GATE_V01",
            "decision_rows_declared": len(rows),
            "acceptance_allowed_rows": sum(row["acceptance_allowed"] == "true" for row in rows),
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
            "evidence_payload_acceptance_decision_gate_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_ACCEPTANCE_DECISION_GATE_CLOSED_UNBLOCK_NOT_COMPLETED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Acceptance Decision Gate v01

**Doc class:** parent-input evidence payload acceptance decision gate
**Status:** acceptance decision gate closed because unblock plan is not completed; no payload accepted, no package pass, no certificate pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_summary_v01.csv
```

This artifact applies the payload acceptance decision rule after the acceptance
unblock plan. The unblock plan is not completed, so acceptance remains closed.

The evidence payload acceptance decision gate is not satisfied:

```text
evidence_payload_acceptance_decision_gate_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_v01
```

## Claim Boundary

This artifact applies an acceptance decision gate only. It materializes no
parent-side payload, validates no receipt, accepts no receipt, provides no
evidence-package pass, provides no certificate pass, accepts no parent-side Tau
inputs, derives no `Phi_tau_eff`, computes no score, supplies no CMB likelihood,
declares no reproduction or failure, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = decision_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_ACCEPTANCE_DECISION_GATE_V01_BUILT")


if __name__ == "__main__":
    main()
