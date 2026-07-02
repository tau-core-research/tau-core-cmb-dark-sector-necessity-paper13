#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_v01_candidate_only_"
    "no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_"
    "no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "candidate_row_id",
    "scoring_input_component",
    "target_payload_component",
    "scoring_input_candidate_status",
    "candidate_source",
    "required_accepted_payload",
    "candidate_construction_rule",
    "required_acceptance_decision",
    "required_scoring_contract",
    "candidate_blocker",
    "candidate_decision",
    "acceptance_allowed",
    "payload_accepted",
    "scoring_input_candidate_declared",
    "scoring_input_accepted",
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
    "candidate_rows_declared",
    "scoring_input_candidate_declared_rows",
    "acceptance_allowed_rows",
    "payload_accepted_rows",
    "scoring_input_accepted_rows",
    "evidence_package_passed_rows",
    "certificate_passed_rows",
    "phi_tau_eff_derived_rows",
    "scores_computed_rows",
    "cmb_likelihood_available_rows",
    "hard_failures_triggered",
    "evidence_payload_scoring_input_candidate_satisfied",
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


def candidate_rows() -> list[dict[str, str]]:
    rows = [
        ("manifest_scoring_input_candidate", "all_parent_payload_rows", "accepted manifest payload"),
        ("base_field_scoring_input_candidate", "base_field_state_payload_candidate", "accepted B_tau state payload"),
        ("seed_scoring_input_candidate", "morphological_seed_payload_candidate", "accepted seed_tau payload"),
        ("operator_scoring_input_candidate", "response_operator_payload_candidate", "accepted R_tau response-operator payload"),
        ("gauge_normalization_scoring_input_candidate", "gauge_normalization_payload_candidate", "accepted gauge/normalization payload"),
        ("endpoint_firewall_scoring_input_candidate", "endpoint_firewall_payload_candidate", "accepted endpoint-firewall payload"),
        ("executable_replay_scoring_input_candidate", "provenance_replay_payload_candidate", "accepted executable replay/provenance payload"),
    ]
    return [
        {
            "candidate_row_id": f"TCMBPTPIPEPSIC01_{index:03d}",
            "scoring_input_component": component,
            "target_payload_component": target,
            "scoring_input_candidate_status": "SCORING_INPUT_CANDIDATE_DECLARED_ACCEPTANCE_DECISION_CLOSED",
            "candidate_source": "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_v01",
            "required_accepted_payload": required,
            "candidate_construction_rule": "candidate can be constructed only from an accepted endpoint-blind evidence payload",
            "required_acceptance_decision": "acceptance_allowed must be true before scoring input can be accepted",
            "required_scoring_contract": "candidate must satisfy minimal scoring input contract before any score is computed",
            "candidate_blocker": "acceptance decision gate is closed",
            "candidate_decision": "candidate_declared_but_not_accepted",
            "acceptance_allowed": "false",
            "payload_accepted": "false",
            "scoring_input_candidate_declared": "true",
            "scoring_input_accepted": "false",
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
        for index, (component, target, required) in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_CANDIDATE_V01",
            "candidate_rows_declared": len(rows),
            "scoring_input_candidate_declared_rows": sum(
                row["scoring_input_candidate_declared"] == "true" for row in rows
            ),
            "acceptance_allowed_rows": sum(row["acceptance_allowed"] == "true" for row in rows),
            "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "evidence_package_passed_rows": sum(row["evidence_package_passed"] == "true" for row in rows),
            "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
            "phi_tau_eff_derived_rows": sum(row["phi_tau_eff_derived"] == "true" for row in rows),
            "scores_computed_rows": sum(row["scores_computed"] == "true" for row in rows),
            "cmb_likelihood_available_rows": sum(row["cmb_likelihood_available"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "evidence_payload_scoring_input_candidate_satisfied": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_CANDIDATE_DECLARED_NOT_ACCEPTED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Candidate v01

**Doc class:** parent-input evidence payload scoring input candidate
**Status:** scoring input candidates declared but not accepted; no payload accepted, no package pass, no certificate pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_summary_v01.csv
```

This artifact declares scoring input candidates that would be constructed from
accepted endpoint-blind evidence payloads. The acceptance decision gate is
closed, so no scoring input is accepted.

The evidence payload scoring input candidate is not satisfied:

```text
evidence_payload_scoring_input_candidate_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_v01
```

## Claim Boundary

This artifact declares scoring-input candidates only. It accepts no
parent-side payload, provides no evidence-package pass, provides no certificate
pass, accepts no scoring input, derives no `Phi_tau_eff`, computes no score,
supplies no CMB likelihood, declares no reproduction or failure, validates no
Tau-response source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = candidate_rows()
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_v01.csv",
        rows,
        FIELDS,
    )
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()


if __name__ == "__main__":
    main()
