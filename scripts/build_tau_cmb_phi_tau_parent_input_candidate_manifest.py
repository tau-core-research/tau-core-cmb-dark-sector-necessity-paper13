#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_phi_tau_parent_input_candidate_manifest_v01_candidate_classes_only_no_accepted_inputs_no_phi_derivation_no_score_no_likelihood_no_verdict"

FIELDS = [
    "manifest_row_id",
    "candidate_component",
    "candidate_symbol_or_object",
    "candidate_status",
    "evidence_source",
    "candidate_parent_side_role",
    "endpoint_exclusion_rule",
    "acceptance_requirement",
    "remaining_blocker",
    "scorecard_effect",
    "candidate_declared",
    "candidate_accepted",
    "manifest_satisfied",
    "hard_failure_triggered",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "manifest_rows_declared",
    "declared_rows",
    "candidate_rows",
    "partial_rows",
    "blocked_rows",
    "accepted_rows",
    "satisfied_rows",
    "hard_failures_triggered",
    "candidate_manifest_satisfied",
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


def manifest_rows() -> list[dict[str, str]]:
    rows = [
        {
            "candidate_component": "candidate_manifest_identity",
            "candidate_symbol_or_object": "M_parent_candidate_v01",
            "candidate_status": "DECLARED_CANDIDATE_MANIFEST",
            "evidence_source": "tau_cmb_phi_tau_parent_input_provenance_v01",
            "candidate_parent_side_role": "name the candidate parent-input packet before any CMB endpoint scoring",
            "endpoint_exclusion_rule": "manifest identity cannot be selected by CMB likelihood improvement",
            "acceptance_requirement": "manifest must be audited and replayed before accepted as a scoring input",
            "remaining_blocker": "manifest identity is declared but not accepted",
            "scorecard_effect": "creates a concrete packet target for the next firewall audit",
        },
        {
            "candidate_component": "base_field_state_candidate",
            "candidate_symbol_or_object": "B_tau_candidate(parent)",
            "candidate_status": "CANDIDATE_CLASS_DECLARED_UNACCEPTED",
            "evidence_source": "tau_cmb_effective_source_equation_v01",
            "candidate_parent_side_role": "candidate base-field carrier/state class for later source construction",
            "endpoint_exclusion_rule": "base-field candidate cannot be optimized against acoustic or lensing residuals",
            "acceptance_requirement": "must be traced to non-endpoint Tau-side assumptions or external parent-side evidence",
            "remaining_blocker": "no accepted base-field value or descriptor is supplied",
            "scorecard_effect": "keeps source-amplitude construction blocked",
        },
        {
            "candidate_component": "morphological_seed_candidate",
            "candidate_symbol_or_object": "seed_tau_candidate(parent)",
            "candidate_status": "CANDIDATE_CLASS_DECLARED_UNACCEPTED",
            "evidence_source": "tau_cmb_minimal_source_term_candidate_v01",
            "candidate_parent_side_role": "candidate morphology or disturbance class that could activate a Tau response",
            "endpoint_exclusion_rule": "seed candidate cannot be inferred from CMB peak residual shape",
            "acceptance_requirement": "must be specified before endpoint comparison and tied to parent-side morphology",
            "remaining_blocker": "no accepted seed descriptor is supplied",
            "scorecard_effect": "keeps the physical source interpretation blocked",
        },
        {
            "candidate_component": "response_operator_candidate",
            "candidate_symbol_or_object": "R_tau_candidate",
            "candidate_status": "CANDIDATE_CLASS_DECLARED_UNACCEPTED",
            "evidence_source": "tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01",
            "candidate_parent_side_role": "candidate operator class mapping parent data toward Phi_tau_eff",
            "endpoint_exclusion_rule": "operator candidate cannot be tuned using role-score outcomes",
            "acceptance_requirement": "must provide a replayable map from parent inputs to source ingredients",
            "remaining_blocker": "no accepted response-operator input set is supplied",
            "scorecard_effect": "keeps the Phi_tau_eff derivation rule blocked",
        },
        {
            "candidate_component": "gauge_normalization_candidate",
            "candidate_symbol_or_object": "gauge_norm_candidate",
            "candidate_status": "PARTIAL_CANDIDATE_METADATA_DECLARED",
            "evidence_source": "tau_cmb_effective_potential_source_handoff_v01",
            "candidate_parent_side_role": "candidate gauge, sign, unit, and normalization convention class",
            "endpoint_exclusion_rule": "metadata candidate cannot be changed after viewing endpoint residuals",
            "acceptance_requirement": "must be locked before acoustic and lensing comparisons share Phi_tau_eff",
            "remaining_blocker": "metadata class is declared but not locked",
            "scorecard_effect": "prevents convention drift from masquerading as agreement",
        },
        {
            "candidate_component": "endpoint_firewall_candidate",
            "candidate_symbol_or_object": "firewall_candidate(M_parent_candidate_v01)",
            "candidate_status": "PARTIAL_FIREWALL_CANDIDATE_DECLARED",
            "evidence_source": "tau_cmb_phi_tau_parent_input_provenance_v01",
            "candidate_parent_side_role": "candidate audit rule checking that parent inputs are endpoint-free",
            "endpoint_exclusion_rule": "audit must reject any score-derived, residual-derived, or likelihood-derived input",
            "acceptance_requirement": "must be executed against the candidate packet before score execution",
            "remaining_blocker": "firewall candidate is declared but not executed",
            "scorecard_effect": "makes the next gate an audit rather than a physics claim",
        },
        {
            "candidate_component": "provenance_replay_candidate",
            "candidate_symbol_or_object": "replay_candidate(parent inputs)",
            "candidate_status": "BLOCKED_REPLAY_CANDIDATE_NOT_SUPPLIED",
            "evidence_source": "tau_cmb_minimal_scoring_input_contract_v01",
            "candidate_parent_side_role": "replay object proving candidates were fixed before endpoint scoring",
            "endpoint_exclusion_rule": "replay cannot read score outputs or CMB residual tables",
            "acceptance_requirement": "must be executable and included in the public reproducibility package",
            "remaining_blocker": "no replay candidate is supplied",
            "scorecard_effect": "blocks score execution from accepting the candidate manifest",
        },
    ]
    return [
        {
            "manifest_row_id": f"TCMBPTPICM01_{index:03d}",
            "candidate_declared": "true",
            "candidate_accepted": "false",
            "manifest_satisfied": "false",
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
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_CANDIDATE_MANIFEST_V01",
            "manifest_rows_declared": len(rows),
            "declared_rows": sum(row["candidate_status"].startswith("DECLARED") for row in rows),
            "candidate_rows": sum(row["candidate_status"].startswith("CANDIDATE") for row in rows),
            "partial_rows": sum(row["candidate_status"].startswith("PARTIAL") for row in rows),
            "blocked_rows": sum(row["candidate_status"].startswith("BLOCKED") for row in rows),
            "accepted_rows": sum(row["candidate_accepted"] == "true" for row in rows),
            "satisfied_rows": sum(row["manifest_satisfied"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "candidate_manifest_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_CANDIDATE_MANIFEST_DECLARED_UNACCEPTED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_candidate_manifest_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Candidate Manifest v01

**Doc class:** parent-input candidate manifest
**Status:** candidate classes declared but unaccepted; no accepted parent inputs, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_candidate_manifest.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_candidate_manifest_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_candidate_manifest_summary_v01.csv
```

This artifact declares candidate parent-input classes for a later endpoint-blind
`Phi_tau_eff(a,k)` derivation. It does not accept any candidate input. It does
not derive `Phi_tau_eff`.

The candidate manifest is not satisfied:

```text
candidate_manifest_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_v01
```

## Claim Boundary

This artifact declares candidate input classes only. It accepts no parent-side
Tau inputs, derives no `Phi_tau_eff`, computes no score, supplies no CMB
likelihood, declares no reproduction or failure, validates no Tau-response
source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = manifest_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_candidate_manifest_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_candidate_manifest_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_CANDIDATE_MANIFEST_V01_BUILT")


if __name__ == "__main__":
    main()
