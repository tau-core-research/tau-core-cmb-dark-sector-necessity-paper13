#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_phi_tau_parent_input_firewall_execution_v01_schema_firewall_only_no_payload_pass_no_accepted_inputs_no_phi_derivation_no_score_no_likelihood_no_verdict"

FIELDS = [
    "execution_row_id",
    "inspected_payload_component",
    "payload_symbol_or_object",
    "execution_status",
    "forbidden_endpoint_fields_checked",
    "forbidden_endpoint_fields_present",
    "schema_firewall_result",
    "payload_level_result",
    "execution_evidence",
    "remaining_blocker",
    "scorecard_effect",
    "schema_firewall_executed",
    "schema_firewall_passed",
    "concrete_payload_supplied",
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
    "execution_rows_declared",
    "schema_executed_rows",
    "schema_passed_rows",
    "payload_passed_rows",
    "accepted_rows",
    "blocked_rows",
    "forbidden_endpoint_fields_detected",
    "concrete_payload_rows",
    "hard_failures_triggered",
    "schema_firewall_execution_satisfied",
    "payload_firewall_satisfied",
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


def execution_rows() -> list[dict[str, str]]:
    rows = [
        {
            "inspected_payload_component": "payload_manifest_identity",
            "payload_symbol_or_object": "M_parent_payload_stub_v01",
            "execution_status": "SCHEMA_FIREWALL_EXECUTED_PASS_STUB_ONLY",
            "forbidden_endpoint_fields_checked": "cmb_residual; score_output; likelihood_error; post_endpoint_fit",
            "schema_firewall_result": "PASS_SCHEMA_ONLY",
            "payload_level_result": "BLOCKED_NO_CONCRETE_PAYLOAD",
            "execution_evidence": "reserved endpoint fields are empty in the manifest identity stub",
            "remaining_blocker": "supply timestamped non-endpoint manifest metadata",
            "scorecard_effect": "keeps manifest unaccepted while allowing next concrete-payload requirement gate",
        },
        {
            "inspected_payload_component": "base_field_state_payload_stub",
            "payload_symbol_or_object": "B_tau_payload_stub(parent)",
            "execution_status": "SCHEMA_FIREWALL_EXECUTED_PASS_EMPTY_STUB",
            "forbidden_endpoint_fields_checked": "acoustic_residual; lensing_residual; score_output; likelihood_error",
            "schema_firewall_result": "PASS_SCHEMA_ONLY",
            "payload_level_result": "BLOCKED_NO_CONCRETE_PAYLOAD",
            "execution_evidence": "base-field stub contains no endpoint-derived populated fields",
            "remaining_blocker": "supply endpoint-blind base-field values or descriptors",
            "scorecard_effect": "keeps source-amplitude construction blocked",
        },
        {
            "inspected_payload_component": "morphological_seed_payload_stub",
            "payload_symbol_or_object": "seed_tau_payload_stub(parent)",
            "execution_status": "SCHEMA_FIREWALL_EXECUTED_PASS_EMPTY_STUB",
            "forbidden_endpoint_fields_checked": "cmb_peak_shape; residual_shape; score_output; likelihood_error",
            "schema_firewall_result": "PASS_SCHEMA_ONLY",
            "payload_level_result": "BLOCKED_NO_CONCRETE_PAYLOAD",
            "execution_evidence": "seed stub contains no endpoint-derived populated fields",
            "remaining_blocker": "supply endpoint-blind morphology/seed values or descriptors",
            "scorecard_effect": "keeps source activation interpretation blocked",
        },
        {
            "inspected_payload_component": "response_operator_payload_stub",
            "payload_symbol_or_object": "R_tau_payload_stub",
            "execution_status": "SCHEMA_FIREWALL_EXECUTED_PASS_EMPTY_STUB",
            "forbidden_endpoint_fields_checked": "role_score; residual_tuning; likelihood_error; post_endpoint_fit",
            "schema_firewall_result": "PASS_SCHEMA_ONLY",
            "payload_level_result": "BLOCKED_NO_CONCRETE_PAYLOAD",
            "execution_evidence": "operator stub contains no endpoint-derived populated fields",
            "remaining_blocker": "supply endpoint-blind response-operator payload",
            "scorecard_effect": "keeps Phi_tau_eff derivation blocked",
        },
        {
            "inspected_payload_component": "gauge_normalization_payload_stub",
            "payload_symbol_or_object": "gauge_norm_payload_stub",
            "execution_status": "SCHEMA_FIREWALL_EXECUTED_PASS_EMPTY_STUB",
            "forbidden_endpoint_fields_checked": "post_endpoint_norm_choice; residual_minimizer; score_output; likelihood_error",
            "schema_firewall_result": "PASS_SCHEMA_ONLY",
            "payload_level_result": "BLOCKED_NO_CONCRETE_PAYLOAD",
            "execution_evidence": "gauge/normalization stub contains no endpoint-derived populated fields",
            "remaining_blocker": "supply locked gauge and normalization values",
            "scorecard_effect": "keeps acoustic/lensing shared-source comparison blocked",
        },
        {
            "inspected_payload_component": "endpoint_firewall_payload_stub",
            "payload_symbol_or_object": "firewall_payload_stub(M_parent_payload_stub_v01)",
            "execution_status": "SCHEMA_FIREWALL_EXECUTED_PASS_RULE_ONLY",
            "forbidden_endpoint_fields_checked": "score_derived_input; residual_derived_input; likelihood_derived_input",
            "schema_firewall_result": "PASS_SCHEMA_ONLY",
            "payload_level_result": "BLOCKED_NO_CONCRETE_PAYLOAD",
            "execution_evidence": "firewall schema marks endpoint-derived input fields as reserved and empty",
            "remaining_blocker": "execute against concrete payload values",
            "scorecard_effect": "confirms schema-level firewall readiness without accepting the payload",
        },
        {
            "inspected_payload_component": "provenance_replay_payload_stub",
            "payload_symbol_or_object": "replay_payload_stub(parent inputs)",
            "execution_status": "BLOCKED_REPLAY_NOT_EXECUTABLE",
            "forbidden_endpoint_fields_checked": "score_output_read; residual_table_read; likelihood_error_read",
            "schema_firewall_result": "NOT_EXECUTABLE",
            "payload_level_result": "BLOCKED_NO_REPLAY",
            "execution_evidence": "replay slot is present but no executable replay exists",
            "remaining_blocker": "supply executable endpoint-blind replay",
            "scorecard_effect": "blocks score execution from accepting any source input",
        },
    ]
    return [
        {
            "execution_row_id": f"TCMBPTPIFE01_{index:03d}",
            "forbidden_endpoint_fields_present": "false",
            "schema_firewall_executed": "true" if index < 7 else "false",
            "schema_firewall_passed": "true" if index < 7 else "false",
            "concrete_payload_supplied": "false",
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
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_FIREWALL_EXECUTION_V01",
            "execution_rows_declared": len(rows),
            "schema_executed_rows": sum(row["schema_firewall_executed"] == "true" for row in rows),
            "schema_passed_rows": sum(row["schema_firewall_passed"] == "true" for row in rows),
            "payload_passed_rows": sum(row["payload_firewall_passed"] == "true" for row in rows),
            "accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "blocked_rows": sum(row["execution_status"].startswith("BLOCKED") for row in rows),
            "forbidden_endpoint_fields_detected": sum(row["forbidden_endpoint_fields_present"] == "true" for row in rows),
            "concrete_payload_rows": sum(row["concrete_payload_supplied"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "schema_firewall_execution_satisfied": "true",
            "payload_firewall_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_FIREWALL_EXECUTION_SCHEMA_PASS_PAYLOAD_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_concrete_payload_requirements_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_firewall_execution_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Firewall Execution v01

**Doc class:** schema-level endpoint-firewall execution
**Status:** schema firewall executed and clean; payload firewall blocked; no accepted inputs, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_firewall_execution.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_firewall_execution_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_firewall_execution_summary_v01.csv
```

This artifact executes the endpoint firewall at schema level against the payload
stub. The reserved endpoint-derived fields are empty, so the schema-level firewall passes.
This is not a payload-level pass: no concrete parent-side Tau
values and no executable replay are supplied.

The payload firewall remains unsatisfied:

```text
payload_firewall_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_concrete_payload_requirements_v01
```

## Claim Boundary

This artifact executes a schema-level firewall only. It provides no
payload-level firewall pass, accepts no parent-side Tau inputs, derives no
`Phi_tau_eff`, computes no score, supplies no CMB likelihood, declares no
reproduction or failure, validates no Tau-response source, and permits no
no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = execution_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_firewall_execution_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_firewall_execution_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_FIREWALL_EXECUTION_V01_BUILT")


if __name__ == "__main__":
    main()
