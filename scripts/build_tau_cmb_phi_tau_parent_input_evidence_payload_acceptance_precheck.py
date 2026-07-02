#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_v01_acceptance_precheck_only_"
    "no_payload_materialized_no_packet_accepted_no_receipt_validated_no_acceptance_pass_no_package_pass_"
    "no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "precheck_row_id",
    "acceptance_component",
    "target_payload_component",
    "acceptance_precheck_status",
    "precheck_source",
    "required_input_object",
    "materialization_gate",
    "receipt_gate",
    "dimension_gate",
    "replay_gate",
    "firewall_gate",
    "acceptance_blocker",
    "precheck_decision",
    "payload_materialized",
    "packet_accepted",
    "receipt_validated",
    "receipt_accepted",
    "dimension_payload_received",
    "replay_payload_received",
    "firewall_payload_received",
    "acceptance_precheck_passed",
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
    "precheck_rows_declared",
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
    "evidence_payload_acceptance_precheck_satisfied",
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


def precheck_rows() -> list[dict[str, str]]:
    rows = [
        ("manifest_acceptance_precheck", "all_parent_payload_rows", "endpoint-blind manifest payload packet"),
        ("base_field_acceptance_precheck", "base_field_state_payload_candidate", "B_tau state payload packet"),
        ("seed_acceptance_precheck", "morphological_seed_payload_candidate", "seed_tau payload packet"),
        ("operator_acceptance_precheck", "response_operator_payload_candidate", "R_tau response-operator payload packet"),
        ("gauge_normalization_acceptance_precheck", "gauge_normalization_payload_candidate", "gauge/normalization payload packet"),
        ("endpoint_firewall_acceptance_precheck", "endpoint_firewall_payload_candidate", "endpoint-firewall payload packet"),
        ("executable_replay_acceptance_precheck", "provenance_replay_payload_candidate", "executable replay/provenance payload packet"),
    ]
    return [
        {
            "precheck_row_id": f"TCMBPTPIPEPAP01_{index:03d}",
            "acceptance_component": component,
            "target_payload_component": target,
            "acceptance_precheck_status": "ACCEPTANCE_PRECHECK_FAILED_MATERIALIZATION_AUDIT_NOT_SATISFIED",
            "precheck_source": "tau_cmb_phi_tau_parent_input_evidence_payload_materialization_audit_v01",
            "required_input_object": required,
            "materialization_gate": "requires materialized endpoint-blind payload packet",
            "receipt_gate": "requires validated receipt binding packet hash replay command and artifact path",
            "dimension_gate": "requires dimension and convention audit pass",
            "replay_gate": "requires deterministic replay evidence pass",
            "firewall_gate": "requires endpoint-blindness firewall pass",
            "acceptance_blocker": "materialization audit failed because no payload packet is materialized",
            "precheck_decision": "blocked_until_materialization_receipt_dimension_replay_and_firewall_gates_pass",
            "payload_materialized": "false",
            "packet_accepted": "false",
            "receipt_validated": "false",
            "receipt_accepted": "false",
            "dimension_payload_received": "false",
            "replay_payload_received": "false",
            "firewall_payload_received": "false",
            "acceptance_precheck_passed": "false",
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
        for index, (component, target, required) in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_ACCEPTANCE_PRECHECK_V01",
            "precheck_rows_declared": len(rows),
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
            "evidence_payload_acceptance_precheck_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_ACCEPTANCE_PRECHECK_FAILED_MATERIALIZATION_AUDIT_NOT_SATISFIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Acceptance Precheck v01

**Doc class:** parent-input evidence payload acceptance precheck
**Status:** acceptance precheck declared but failed because materialization audit is not satisfied; no payload accepted, no package pass, no certificate pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_summary_v01.csv
```

This artifact checks whether parent-side evidence payload packets are eligible
for acceptance. The materialization audit is not satisfied, so no payload is accepted.

The evidence payload acceptance precheck is not satisfied:

```text
evidence_payload_acceptance_precheck_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_v01
```

## Claim Boundary

This artifact performs an acceptance precheck only. It materializes no
parent-side payload, validates no receipt, accepts no receipt, provides no
evidence-package pass, provides no certificate pass, accepts no parent-side Tau
inputs, derives no `Phi_tau_eff`, computes no score, supplies no CMB likelihood,
declares no reproduction or failure, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = precheck_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_ACCEPTANCE_PRECHECK_V01_BUILT")


if __name__ == "__main__":
    main()
