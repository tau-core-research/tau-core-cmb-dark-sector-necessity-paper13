#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_phi_tau_parent_input_payload_stub_v01_stub_schema_only_no_concrete_parent_values_no_firewall_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"

FIELDS = [
    "payload_row_id",
    "payload_component",
    "payload_symbol_or_object",
    "payload_status",
    "evidence_source",
    "stub_content",
    "endpoint_exclusion_metadata",
    "payload_limitation",
    "remaining_blocker",
    "scorecard_effect",
    "payload_stub_declared",
    "concrete_payload_supplied",
    "endpoint_firewall_executable",
    "payload_accepted",
    "payload_satisfied",
    "hard_failure_triggered",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "payload_rows_declared",
    "declared_rows",
    "stub_rows",
    "partial_rows",
    "blocked_rows",
    "concrete_payload_rows",
    "firewall_executable_rows",
    "accepted_rows",
    "satisfied_rows",
    "hard_failures_triggered",
    "payload_stub_satisfied",
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


def payload_rows() -> list[dict[str, str]]:
    rows = [
        {
            "payload_component": "payload_manifest_identity",
            "payload_symbol_or_object": "M_parent_payload_stub_v01",
            "payload_status": "DECLARED_PAYLOAD_STUB_MANIFEST",
            "evidence_source": "tau_cmb_phi_tau_parent_input_firewall_audit_v01",
            "stub_content": "manifest-level payload stub with no physical values",
            "endpoint_exclusion_metadata": "endpoint fields reserved and empty",
            "payload_limitation": "identity stub cannot be used as a source input",
            "remaining_blocker": "supply timestamped non-endpoint payload metadata",
            "scorecard_effect": "creates a file-level target for firewall execution",
        },
        {
            "payload_component": "base_field_state_payload_stub",
            "payload_symbol_or_object": "B_tau_payload_stub(parent)",
            "payload_status": "STUB_DECLARED_EMPTY",
            "evidence_source": "tau_cmb_phi_tau_parent_input_candidate_manifest_v01",
            "stub_content": "base-field state slot exists but value is empty",
            "endpoint_exclusion_metadata": "no acoustic, lensing, score, or likelihood fields populated",
            "payload_limitation": "no base-field amplitude, unit, or state descriptor is supplied",
            "remaining_blocker": "supply endpoint-blind base-field payload",
            "scorecard_effect": "keeps source-amplitude construction blocked",
        },
        {
            "payload_component": "morphological_seed_payload_stub",
            "payload_symbol_or_object": "seed_tau_payload_stub(parent)",
            "payload_status": "STUB_DECLARED_EMPTY",
            "evidence_source": "tau_cmb_phi_tau_parent_input_candidate_manifest_v01",
            "stub_content": "morphological seed slot exists but value is empty",
            "endpoint_exclusion_metadata": "no CMB peak-shape or residual-derived fields populated",
            "payload_limitation": "no seed morphology, scale, or activation descriptor is supplied",
            "remaining_blocker": "supply endpoint-blind seed payload",
            "scorecard_effect": "keeps source activation interpretation blocked",
        },
        {
            "payload_component": "response_operator_payload_stub",
            "payload_symbol_or_object": "R_tau_payload_stub",
            "payload_status": "STUB_DECLARED_EMPTY",
            "evidence_source": "tau_cmb_phi_tau_parent_input_candidate_manifest_v01",
            "stub_content": "response-operator slot exists but operator inputs are empty",
            "endpoint_exclusion_metadata": "no role-score or residual-derived tuning fields populated",
            "payload_limitation": "no map from parent inputs to Phi_tau_eff ingredients is supplied",
            "remaining_blocker": "supply endpoint-blind operator payload",
            "scorecard_effect": "keeps Phi_tau_eff derivation blocked",
        },
        {
            "payload_component": "gauge_normalization_payload_stub",
            "payload_symbol_or_object": "gauge_norm_payload_stub",
            "payload_status": "STUB_DECLARED_EMPTY",
            "evidence_source": "tau_cmb_phi_tau_parent_input_candidate_manifest_v01",
            "stub_content": "gauge, sign, unit, and normalization slots exist but values are empty",
            "endpoint_exclusion_metadata": "no post-endpoint convention-choice fields populated",
            "payload_limitation": "no locked convention payload is supplied",
            "remaining_blocker": "supply locked gauge and normalization payload",
            "scorecard_effect": "keeps acoustic/lensing shared-source comparison blocked",
        },
        {
            "payload_component": "endpoint_firewall_payload_stub",
            "payload_symbol_or_object": "firewall_payload_stub(M_parent_payload_stub_v01)",
            "payload_status": "PARTIAL_FIREWALL_STUB_READY_NO_EXECUTION",
            "evidence_source": "tau_cmb_phi_tau_parent_input_firewall_audit_v01",
            "stub_content": "firewall can inspect schema fields but not physical payload values",
            "endpoint_exclusion_metadata": "endpoint-derived input fields are reserved and must remain empty",
            "payload_limitation": "schema-level firewall inspection is possible, payload-level pass is not",
            "remaining_blocker": "execute firewall against a concrete payload packet",
            "scorecard_effect": "prepares the next firewall execution gate",
        },
        {
            "payload_component": "provenance_replay_payload_stub",
            "payload_symbol_or_object": "replay_payload_stub(parent inputs)",
            "payload_status": "BLOCKED_REPLAY_STUB_NOT_EXECUTABLE",
            "evidence_source": "tau_cmb_phi_tau_parent_input_firewall_audit_v01",
            "stub_content": "replay slot exists but executable replay is absent",
            "endpoint_exclusion_metadata": "no score-output or residual-table reads are declared",
            "payload_limitation": "absence of reads is not a replay proof because no executable replay exists",
            "remaining_blocker": "supply executable endpoint-blind replay payload",
            "scorecard_effect": "blocks score execution from accepting the payload stub",
        },
    ]
    return [
        {
            "payload_row_id": f"TCMBPTPIPS01_{index:03d}",
            "payload_stub_declared": "true",
            "concrete_payload_supplied": "false",
            "endpoint_firewall_executable": "false",
            "payload_accepted": "false",
            "payload_satisfied": "false",
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
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_PAYLOAD_STUB_V01",
            "payload_rows_declared": len(rows),
            "declared_rows": sum(row["payload_status"].startswith("DECLARED") for row in rows),
            "stub_rows": sum(row["payload_status"].startswith("STUB") for row in rows),
            "partial_rows": sum(row["payload_status"].startswith("PARTIAL") for row in rows),
            "blocked_rows": sum(row["payload_status"].startswith("BLOCKED") for row in rows),
            "concrete_payload_rows": sum(row["concrete_payload_supplied"] == "true" for row in rows),
            "firewall_executable_rows": sum(row["endpoint_firewall_executable"] == "true" for row in rows),
            "accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "satisfied_rows": sum(row["payload_satisfied"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "payload_stub_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_PAYLOAD_STUB_DECLARED_NO_CONCRETE_VALUES",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_firewall_execution_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_payload_stub_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Payload Stub v01

**Doc class:** parent-input payload stub
**Status:** payload schema declared but concrete values absent; no firewall pass, no accepted inputs, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_payload_stub.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_payload_stub_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_payload_stub_summary_v01.csv
```

This artifact declares a minimal payload-stub schema for the parent-input
candidate manifest. It does not supply concrete parent-input values. It does
not pass the endpoint firewall. It does not derive `Phi_tau_eff`.

The payload stub is not satisfied:

```text
payload_stub_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_firewall_execution_v01
```

## Claim Boundary

This artifact declares payload schema only. It supplies no concrete parent-side
Tau values, provides no payload-level firewall pass, accepts no parent-side Tau
inputs, derives no `Phi_tau_eff`, computes no score, supplies no CMB likelihood,
declares no reproduction or failure, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = payload_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_payload_stub_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_payload_stub_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_PAYLOAD_STUB_V01_BUILT")


if __name__ == "__main__":
    main()
