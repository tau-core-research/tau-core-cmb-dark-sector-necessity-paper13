#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_phi_tau_parent_input_concrete_payload_candidate_v01_candidate_payload_only_no_accepted_inputs_no_payload_firewall_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"

FIELDS = [
    "candidate_row_id",
    "payload_component",
    "candidate_symbol_or_object",
    "candidate_status",
    "evidence_source",
    "candidate_payload_content",
    "dimension_or_units_status",
    "endpoint_blind_status",
    "replay_status",
    "acceptance_blocker",
    "scorecard_effect",
    "candidate_payload_declared",
    "concrete_payload_supplied",
    "dimension_check_passed",
    "endpoint_firewall_passed",
    "replay_available",
    "payload_accepted",
    "hard_failure_triggered",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "candidate_rows_declared",
    "manifest_rows",
    "candidate_payload_rows",
    "blocked_rows",
    "concrete_payload_rows",
    "dimension_passed_rows",
    "firewall_passed_rows",
    "replay_available_rows",
    "accepted_rows",
    "hard_failures_triggered",
    "concrete_payload_candidate_satisfied",
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


def candidate_rows() -> list[dict[str, str]]:
    rows = [
        {
            "payload_component": "candidate_payload_manifest_identity",
            "candidate_symbol_or_object": "M_parent_payload_candidate_v01",
            "candidate_status": "MANIFEST_CANDIDATE_DECLARED_UNACCEPTED",
            "evidence_source": "tau_cmb_phi_tau_parent_input_concrete_payload_requirements_v01",
            "candidate_payload_content": "candidate payload manifest identity and component list",
            "dimension_or_units_status": "not a physical payload row; references child dimensional checks",
            "endpoint_blind_status": "requires payload-level firewall certificate before acceptance",
            "replay_status": "requires executable replay before acceptance",
            "acceptance_blocker": "child candidate payload rows are not accepted",
            "scorecard_effect": "creates concrete candidate package target for payload-level firewall audit",
        },
        {
            "payload_component": "base_field_state_payload_candidate",
            "candidate_symbol_or_object": "B_tau_candidate(parent)",
            "candidate_status": "CANDIDATE_PAYLOAD_DECLARED_UNACCEPTED",
            "evidence_source": "tau_cmb_phi_tau_parent_input_concrete_payload_requirements_v01",
            "candidate_payload_content": "symbolic base-field state candidate with amplitude convention placeholder",
            "dimension_or_units_status": "declared placeholder; dimensional check not passed",
            "endpoint_blind_status": "endpoint-blind provenance not certified at payload level",
            "replay_status": "no executable replay",
            "acceptance_blocker": "missing dimension pass, firewall pass, and replay",
            "scorecard_effect": "keeps density and potential amplitude scoring blocked",
        },
        {
            "payload_component": "morphological_seed_payload_candidate",
            "candidate_symbol_or_object": "seed_tau_candidate(parent)",
            "candidate_status": "CANDIDATE_PAYLOAD_DECLARED_UNACCEPTED",
            "evidence_source": "tau_cmb_phi_tau_parent_input_concrete_payload_requirements_v01",
            "candidate_payload_content": "symbolic morphology/seed candidate with activation-class placeholder",
            "dimension_or_units_status": "scale and normalization placeholders declared; dimensional check not passed",
            "endpoint_blind_status": "endpoint-blind seed provenance not certified at payload level",
            "replay_status": "no executable replay",
            "acceptance_blocker": "missing scale lock, firewall pass, and replay",
            "scorecard_effect": "keeps source activation interpretation blocked",
        },
        {
            "payload_component": "response_operator_payload_candidate",
            "candidate_symbol_or_object": "R_tau_candidate",
            "candidate_status": "CANDIDATE_PAYLOAD_DECLARED_UNACCEPTED",
            "evidence_source": "tau_cmb_phi_tau_parent_input_concrete_payload_requirements_v01",
            "candidate_payload_content": "symbolic response-operator candidate mapping parent slots toward source ingredients",
            "dimension_or_units_status": "dimensional map placeholder declared; check not passed",
            "endpoint_blind_status": "operator tuning firewall not certified at payload level",
            "replay_status": "no executable replay",
            "acceptance_blocker": "missing dimensional map pass, firewall pass, and replay",
            "scorecard_effect": "keeps Phi_tau_eff derivation blocked",
        },
        {
            "payload_component": "gauge_normalization_payload_candidate",
            "candidate_symbol_or_object": "gauge_norm_candidate(parent)",
            "candidate_status": "CANDIDATE_PAYLOAD_DECLARED_UNACCEPTED",
            "evidence_source": "tau_cmb_phi_tau_parent_input_concrete_payload_requirements_v01",
            "candidate_payload_content": "candidate gauge/sign/unit/normalization metadata with lock placeholder",
            "dimension_or_units_status": "unit or dimensionless normalization placeholder declared; check not passed",
            "endpoint_blind_status": "post-endpoint convention choice not certified absent at payload level",
            "replay_status": "no executable replay",
            "acceptance_blocker": "missing metadata lock proof, firewall pass, and replay",
            "scorecard_effect": "keeps shared acoustic/lensing source comparison blocked",
        },
        {
            "payload_component": "endpoint_firewall_payload_candidate",
            "candidate_symbol_or_object": "firewall_certificate_candidate(parent payload)",
            "candidate_status": "BLOCKED_FIREWALL_CERTIFICATE_NOT_SUPPLIED",
            "evidence_source": "tau_cmb_phi_tau_parent_input_firewall_execution_v01",
            "candidate_payload_content": "certificate slot declared, certificate not supplied",
            "dimension_or_units_status": "references child dimensional checks; no physical value",
            "endpoint_blind_status": "payload-level firewall not passed",
            "replay_status": "no executable replay",
            "acceptance_blocker": "missing payload-level firewall certificate",
            "scorecard_effect": "blocks accepting any candidate payload row",
        },
        {
            "payload_component": "provenance_replay_payload_candidate",
            "candidate_symbol_or_object": "replay_candidate(parent payload)",
            "candidate_status": "BLOCKED_EXECUTABLE_REPLAY_NOT_SUPPLIED",
            "evidence_source": "tau_cmb_phi_tau_parent_input_concrete_payload_requirements_v01",
            "candidate_payload_content": "replay slot declared, executable replay not supplied",
            "dimension_or_units_status": "must replay child dimensional checks; not available",
            "endpoint_blind_status": "cannot certify endpoint blindness without replay",
            "replay_status": "no executable replay",
            "acceptance_blocker": "missing executable endpoint-blind replay",
            "scorecard_effect": "blocks transition into scoring input acceptance",
        },
    ]
    return [
        {
            "candidate_row_id": f"TCMBPTPICP01_{index:03d}",
            "candidate_payload_declared": "true",
            "concrete_payload_supplied": "true" if index <= 5 else "false",
            "dimension_check_passed": "false",
            "endpoint_firewall_passed": "false",
            "replay_available": "false",
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
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_CONCRETE_PAYLOAD_CANDIDATE_V01",
            "candidate_rows_declared": len(rows),
            "manifest_rows": sum(row["candidate_status"].startswith("MANIFEST") for row in rows),
            "candidate_payload_rows": sum(row["candidate_status"].startswith("CANDIDATE") for row in rows),
            "blocked_rows": sum(row["candidate_status"].startswith("BLOCKED") for row in rows),
            "concrete_payload_rows": sum(row["concrete_payload_supplied"] == "true" for row in rows),
            "dimension_passed_rows": sum(row["dimension_check_passed"] == "true" for row in rows),
            "firewall_passed_rows": sum(row["endpoint_firewall_passed"] == "true" for row in rows),
            "replay_available_rows": sum(row["replay_available"] == "true" for row in rows),
            "accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "concrete_payload_candidate_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_CONCRETE_PAYLOAD_CANDIDATE_DECLARED_UNACCEPTED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_concrete_payload_candidate_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Concrete Payload Candidate v01

**Doc class:** concrete parent-input payload candidate
**Status:** candidate payload declared but unaccepted; no payload firewall pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_concrete_payload_candidate.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_concrete_payload_candidate_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_concrete_payload_candidate_summary_v01.csv
```

This artifact declares a concrete payload candidate package for the parent-side
Tau inputs. It does not accept any candidate payload. It does not pass the
payload-level endpoint firewall. It does not derive `Phi_tau_eff`.

The concrete payload candidate is not satisfied:

```text
concrete_payload_candidate_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01
```

## Claim Boundary

This artifact declares candidate parent-side payload rows only. It accepts no
parent-side Tau inputs, provides no payload-level firewall pass, derives no
`Phi_tau_eff`, computes no score, supplies no CMB likelihood, declares no
reproduction or failure, validates no Tau-response source, and permits no
no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = candidate_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_concrete_payload_candidate_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_concrete_payload_candidate_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_CONCRETE_PAYLOAD_CANDIDATE_V01_BUILT")


if __name__ == "__main__":
    main()
