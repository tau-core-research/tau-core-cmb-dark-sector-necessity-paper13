#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_phi_tau_parent_input_firewall_audit_v01_audit_rules_only_no_payload_pass_no_accepted_inputs_no_phi_derivation_no_score_no_likelihood_no_verdict"

FIELDS = [
    "audit_row_id",
    "audited_candidate_component",
    "candidate_symbol_or_object",
    "endpoint_risk_class",
    "audit_status",
    "audit_rule",
    "observed_endpoint_dependency",
    "audit_evidence",
    "remaining_blocker",
    "scorecard_effect",
    "endpoint_firewall_passed",
    "candidate_accepted",
    "audit_satisfied",
    "hard_failure_triggered",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "audit_rows_declared",
    "declared_rows",
    "partial_rows",
    "blocked_rows",
    "passed_rows",
    "accepted_rows",
    "satisfied_rows",
    "endpoint_dependencies_detected",
    "hard_failures_triggered",
    "endpoint_firewall_audit_satisfied",
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
            "audited_candidate_component": "candidate_manifest_identity",
            "candidate_symbol_or_object": "M_parent_candidate_v01",
            "endpoint_risk_class": "identity_selection_risk",
            "audit_status": "PARTIAL_RULE_AUDIT_DECLARED_NO_PAYLOAD",
            "audit_rule": "manifest identity must be fixed before CMB endpoint scoring",
            "audit_evidence": "candidate manifest declares the endpoint-exclusion rule but no payload timestamp or replay exists",
            "remaining_blocker": "supply payload identity metadata fixed before endpoint evaluation",
            "scorecard_effect": "blocks accepting the manifest as a scoring input",
        },
        {
            "audited_candidate_component": "base_field_state_candidate",
            "candidate_symbol_or_object": "B_tau_candidate(parent)",
            "endpoint_risk_class": "amplitude_tuning_risk",
            "audit_status": "BLOCKED_NO_BASE_FIELD_PAYLOAD",
            "audit_rule": "base-field payload must not be optimized against acoustic or lensing residuals",
            "audit_evidence": "no concrete base-field payload is supplied",
            "remaining_blocker": "supply endpoint-blind base-field payload or mark the source path failed",
            "scorecard_effect": "keeps density and potential amplitude scoring blocked",
        },
        {
            "audited_candidate_component": "morphological_seed_candidate",
            "candidate_symbol_or_object": "seed_tau_candidate(parent)",
            "endpoint_risk_class": "shape_backfit_risk",
            "audit_status": "BLOCKED_NO_SEED_PAYLOAD",
            "audit_rule": "seed payload must not be inferred from CMB peak residual shape",
            "audit_evidence": "no concrete seed payload is supplied",
            "remaining_blocker": "supply endpoint-blind morphology/seed payload or mark the source path failed",
            "scorecard_effect": "keeps source activation interpretation blocked",
        },
        {
            "audited_candidate_component": "response_operator_candidate",
            "candidate_symbol_or_object": "R_tau_candidate",
            "endpoint_risk_class": "operator_tuning_risk",
            "audit_status": "BLOCKED_NO_OPERATOR_PAYLOAD",
            "audit_rule": "operator payload must not be tuned from role-score outcomes",
            "audit_evidence": "no concrete response-operator payload is supplied",
            "remaining_blocker": "supply endpoint-blind operator payload or mark the derivation path failed",
            "scorecard_effect": "keeps Phi_tau_eff derivation blocked",
        },
        {
            "audited_candidate_component": "gauge_normalization_candidate",
            "candidate_symbol_or_object": "gauge_norm_candidate",
            "endpoint_risk_class": "convention_drift_risk",
            "audit_status": "BLOCKED_NO_METADATA_PAYLOAD",
            "audit_rule": "gauge and normalization payload must be locked before endpoint residual inspection",
            "audit_evidence": "no concrete gauge/normalization payload is supplied",
            "remaining_blocker": "supply locked metadata payload or keep convention-dependent scoring blocked",
            "scorecard_effect": "prevents convention drift from entering acoustic/lensing comparison",
        },
        {
            "audited_candidate_component": "endpoint_firewall_candidate",
            "candidate_symbol_or_object": "firewall_candidate(M_parent_candidate_v01)",
            "endpoint_risk_class": "circularity_detection_rule",
            "audit_status": "DECLARED_FIREWALL_RULE_READY_NO_EXECUTION",
            "audit_rule": "reject any score-derived, residual-derived, or likelihood-derived input",
            "audit_evidence": "firewall rule is declared but cannot be executed without a candidate payload packet",
            "remaining_blocker": "execute the firewall against a concrete payload packet",
            "scorecard_effect": "makes the next gate a payload-and-replay requirement",
        },
        {
            "audited_candidate_component": "provenance_replay_candidate",
            "candidate_symbol_or_object": "replay_candidate(parent inputs)",
            "endpoint_risk_class": "non_reproducible_provenance_risk",
            "audit_status": "BLOCKED_NO_REPLAY_PAYLOAD",
            "audit_rule": "replay must run without reading score outputs or CMB residual tables",
            "audit_evidence": "no replay candidate is supplied",
            "remaining_blocker": "supply endpoint-blind replay payload before any score execution",
            "scorecard_effect": "blocks score execution from accepting the candidate manifest",
        },
    ]
    return [
        {
            "audit_row_id": f"TCMBPTPIFA01_{index:03d}",
            "observed_endpoint_dependency": "false",
            "endpoint_firewall_passed": "false",
            "candidate_accepted": "false",
            "audit_satisfied": "false",
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
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_FIREWALL_AUDIT_V01",
            "audit_rows_declared": len(rows),
            "declared_rows": sum(row["audit_status"].startswith("DECLARED") for row in rows),
            "partial_rows": sum(row["audit_status"].startswith("PARTIAL") for row in rows),
            "blocked_rows": sum(row["audit_status"].startswith("BLOCKED") for row in rows),
            "passed_rows": sum(row["endpoint_firewall_passed"] == "true" for row in rows),
            "accepted_rows": sum(row["candidate_accepted"] == "true" for row in rows),
            "satisfied_rows": sum(row["audit_satisfied"] == "true" for row in rows),
            "endpoint_dependencies_detected": sum(row["observed_endpoint_dependency"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "endpoint_firewall_audit_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_FIREWALL_AUDIT_DECLARED_BLOCKED_BY_MISSING_PAYLOAD",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_payload_stub_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_firewall_audit_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Firewall Audit v01

**Doc class:** endpoint-firewall audit scaffold
**Status:** audit rules declared but blocked by missing payload; no firewall pass, no accepted inputs, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_firewall_audit.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_firewall_audit_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_firewall_audit_summary_v01.csv
```

This artifact audits the candidate parent-input manifest at the rule level. It
does not pass the endpoint firewall because no concrete candidate payload packet
exists. It does not accept any candidate input. It does not derive
`Phi_tau_eff`.

No endpoint dependency is detected because there is no payload to inspect, not
because the candidate manifest has passed:

```text
endpoint_firewall_audit_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_payload_stub_v01
```

## Claim Boundary

This artifact declares firewall audit rules only. It provides no payload-level
firewall pass, accepts no parent-side Tau inputs, derives no `Phi_tau_eff`,
computes no score, supplies no CMB likelihood, declares no reproduction or
failure, validates no Tau-response source, and permits no no-dark or
dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = audit_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_firewall_audit_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_firewall_audit_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_FIREWALL_AUDIT_V01_BUILT")


if __name__ == "__main__":
    main()
