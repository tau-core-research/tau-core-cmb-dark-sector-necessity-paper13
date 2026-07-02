#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_phi_tau_parent_input_concrete_payload_requirements_v01_requirements_only_no_concrete_payload_no_phi_derivation_no_score_no_likelihood_no_verdict"

FIELDS = [
    "requirement_row_id",
    "payload_component",
    "required_symbol_or_object",
    "requirement_status",
    "evidence_source",
    "required_payload_type",
    "required_parent_side_content",
    "dimensional_or_units_requirement",
    "endpoint_blind_evidence_required",
    "replay_requirement",
    "acceptance_criterion",
    "remaining_blocker",
    "scorecard_effect",
    "concrete_payload_supplied",
    "requirement_satisfied",
    "hard_failure_triggered",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "requirement_rows_declared",
    "declared_rows",
    "requirement_rows",
    "blocked_rows",
    "concrete_payload_rows",
    "satisfied_rows",
    "hard_failures_triggered",
    "concrete_payload_requirements_satisfied",
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


def requirement_rows() -> list[dict[str, str]]:
    rows = [
        {
            "payload_component": "requirements_manifest_identity",
            "required_symbol_or_object": "M_parent_payload_requirements_v01",
            "requirement_status": "DECLARED_REQUIREMENTS_MANIFEST",
            "evidence_source": "tau_cmb_phi_tau_parent_input_firewall_execution_v01",
            "required_payload_type": "requirements manifest",
            "required_parent_side_content": "complete list of required concrete parent-side payload objects",
            "dimensional_or_units_requirement": "every physical payload row must declare dimension or unit status",
            "endpoint_blind_evidence_required": "manifest must be fixed before CMB endpoint scoring",
            "replay_requirement": "manifest must be replayable without reading CMB residual or score outputs",
            "acceptance_criterion": "all child payload requirements are supplied and firewall-passed",
            "remaining_blocker": "child payload requirements are not supplied",
            "scorecard_effect": "creates the contract for concrete payload candidate construction",
        },
        {
            "payload_component": "base_field_state_payload",
            "required_symbol_or_object": "B_tau(parent)",
            "requirement_status": "REQUIREMENT_DECLARED_PAYLOAD_MISSING",
            "evidence_source": "tau_cmb_phi_tau_parent_input_payload_stub_v01",
            "required_payload_type": "base-field state or carrier descriptor",
            "required_parent_side_content": "endpoint-blind Tau base-field state, amplitude convention, and parent-side provenance",
            "dimensional_or_units_requirement": "must declare whether dimensionless, normalized, or unit-carrying before source construction",
            "endpoint_blind_evidence_required": "must not be selected by acoustic, lensing, score, or likelihood residual minimization",
            "replay_requirement": "replay must show the base-field payload is fixed before endpoint evaluation",
            "acceptance_criterion": "payload supplied, dimension checked, endpoint firewall passed, replay available",
            "remaining_blocker": "no concrete base-field payload is supplied",
            "scorecard_effect": "blocks density and potential amplitude scoring",
        },
        {
            "payload_component": "morphological_seed_payload",
            "required_symbol_or_object": "seed_tau(parent)",
            "requirement_status": "REQUIREMENT_DECLARED_PAYLOAD_MISSING",
            "evidence_source": "tau_cmb_phi_tau_parent_input_payload_stub_v01",
            "required_payload_type": "morphological seed or disturbance descriptor",
            "required_parent_side_content": "seed morphology, activation class, scale label, and parent-side provenance",
            "dimensional_or_units_requirement": "must declare scale and normalization conventions before readout comparison",
            "endpoint_blind_evidence_required": "must not be inferred from CMB peak shape or residual shape",
            "replay_requirement": "replay must show seed payload is fixed before endpoint evaluation",
            "acceptance_criterion": "payload supplied, scale convention fixed, endpoint firewall passed, replay available",
            "remaining_blocker": "no concrete morphology/seed payload is supplied",
            "scorecard_effect": "blocks source activation interpretation",
        },
        {
            "payload_component": "response_operator_payload",
            "required_symbol_or_object": "R_tau(parent)",
            "requirement_status": "REQUIREMENT_DECLARED_PAYLOAD_MISSING",
            "evidence_source": "tau_cmb_phi_tau_parent_input_firewall_execution_v01",
            "required_payload_type": "response-operator input set",
            "required_parent_side_content": "operator inputs mapping parent-side payloads toward Phi_tau_eff ingredients",
            "dimensional_or_units_requirement": "must preserve declared dimensions from parent payloads into the source ingredients",
            "endpoint_blind_evidence_required": "must not be tuned from role scores, CMB residuals, or likelihood errors",
            "replay_requirement": "replay must rebuild the operator inputs without reading score outputs",
            "acceptance_criterion": "operator payload supplied, dimensional map checked, endpoint firewall passed, replay available",
            "remaining_blocker": "no concrete response-operator payload is supplied",
            "scorecard_effect": "blocks Phi_tau_eff derivation",
        },
        {
            "payload_component": "gauge_normalization_payload",
            "required_symbol_or_object": "gauge_norm(parent)",
            "requirement_status": "REQUIREMENT_DECLARED_PAYLOAD_MISSING",
            "evidence_source": "tau_cmb_phi_tau_parent_input_payload_stub_v01",
            "required_payload_type": "gauge, sign, unit, and normalization metadata",
            "required_parent_side_content": "locked gauge, sign, unit, and normalization convention fixed before endpoint comparison",
            "dimensional_or_units_requirement": "must specify unit conversion or dimensionless normalization used by all role rows",
            "endpoint_blind_evidence_required": "must not be chosen after viewing endpoint residuals",
            "replay_requirement": "replay must show metadata lock precedes endpoint evaluation",
            "acceptance_criterion": "metadata supplied, locked, endpoint firewall passed, replay available",
            "remaining_blocker": "no concrete locked metadata payload is supplied",
            "scorecard_effect": "blocks shared acoustic/lensing source comparison",
        },
        {
            "payload_component": "endpoint_firewall_payload",
            "required_symbol_or_object": "firewall(parent payload)",
            "requirement_status": "REQUIREMENT_DECLARED_PAYLOAD_MISSING",
            "evidence_source": "tau_cmb_phi_tau_parent_input_firewall_execution_v01",
            "required_payload_type": "payload-level firewall certificate",
            "required_parent_side_content": "certificate proving endpoint-derived fields are absent from concrete payload values",
            "dimensional_or_units_requirement": "not a physical dimension check; must reference dimension checks for physical payload rows",
            "endpoint_blind_evidence_required": "must reject score-derived, residual-derived, and likelihood-derived inputs",
            "replay_requirement": "firewall certificate must be reproducible from the payload package",
            "acceptance_criterion": "all concrete payload rows pass the endpoint firewall",
            "remaining_blocker": "no concrete payload exists for firewall certification",
            "scorecard_effect": "blocks accepting any parent input before payload-level audit",
        },
        {
            "payload_component": "provenance_replay_payload",
            "required_symbol_or_object": "replay(parent payload)",
            "requirement_status": "BLOCKED_EXECUTABLE_REPLAY_REQUIRED",
            "evidence_source": "tau_cmb_phi_tau_parent_input_firewall_execution_v01",
            "required_payload_type": "executable provenance replay",
            "required_parent_side_content": "script or manifest replay proving every concrete payload row is fixed before endpoint evaluation",
            "dimensional_or_units_requirement": "must replay or reference all dimensional checks for physical payload rows",
            "endpoint_blind_evidence_required": "must run without reading score outputs, residual tables, or likelihood error fields",
            "replay_requirement": "executable replay is mandatory before any source input can be accepted",
            "acceptance_criterion": "replay executes cleanly and confirms endpoint-blind provenance",
            "remaining_blocker": "no executable provenance replay is supplied",
            "scorecard_effect": "blocks transition from payload requirements to scoring input acceptance",
        },
    ]
    return [
        {
            "requirement_row_id": f"TCMBPTPICPR01_{index:03d}",
            "concrete_payload_supplied": "false",
            "requirement_satisfied": "false",
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
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_CONCRETE_PAYLOAD_REQUIREMENTS_V01",
            "requirement_rows_declared": len(rows),
            "declared_rows": sum(row["requirement_status"].startswith("DECLARED") for row in rows),
            "requirement_rows": sum(row["requirement_status"].startswith("REQUIREMENT") for row in rows),
            "blocked_rows": sum(row["requirement_status"].startswith("BLOCKED") for row in rows),
            "concrete_payload_rows": sum(row["concrete_payload_supplied"] == "true" for row in rows),
            "satisfied_rows": sum(row["requirement_satisfied"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "concrete_payload_requirements_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_CONCRETE_PAYLOAD_REQUIREMENTS_DECLARED_UNSATISFIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_concrete_payload_candidate_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_concrete_payload_requirements_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Concrete Payload Requirements v01

**Doc class:** concrete parent-input payload requirements
**Status:** requirements declared but unsatisfied; no concrete payload, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_concrete_payload_requirements.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_concrete_payload_requirements_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_concrete_payload_requirements_summary_v01.csv
```

This artifact declares the concrete parent-side payload requirements needed
before the payload-level firewall can pass.
It does not supply concrete parent-input values. It does not derive `Phi_tau_eff`.

The concrete payload requirements are not satisfied:

```text
concrete_payload_requirements_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_concrete_payload_candidate_v01
```

## Claim Boundary

This artifact declares concrete payload requirements only. It supplies no
concrete parent-side Tau values, provides no payload-level firewall pass,
accepts no parent-side Tau inputs, derives no `Phi_tau_eff`, computes no score,
supplies no CMB likelihood, declares no reproduction or failure, validates no
Tau-response source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = requirement_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_concrete_payload_requirements_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_concrete_payload_requirements_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_CONCRETE_PAYLOAD_REQUIREMENTS_V01_BUILT")


if __name__ == "__main__":
    main()
