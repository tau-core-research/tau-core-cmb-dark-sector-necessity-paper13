#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_phi_tau_parent_input_provenance_v01_provenance_slots_only_no_parent_inputs_no_phi_derivation_no_score_no_likelihood_no_verdict"

FIELDS = [
    "provenance_row_id",
    "parent_input_component",
    "symbol_or_object",
    "provenance_status",
    "evidence_source",
    "required_parent_side_content",
    "endpoint_firewall_rule",
    "remaining_blocker",
    "scorecard_effect",
    "parent_input_supplied",
    "provenance_satisfied",
    "hard_failure_triggered",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "provenance_rows_declared",
    "declared_rows",
    "partial_rows",
    "blocked_rows",
    "supplied_rows",
    "satisfied_rows",
    "hard_failures_triggered",
    "parent_input_provenance_satisfied",
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


def provenance_rows() -> list[dict[str, str]]:
    rows = [
        {
            "parent_input_component": "parent_input_manifest_identity",
            "symbol_or_object": "M_parent(Phi_tau_eff)",
            "provenance_status": "DECLARED_PARENT_INPUT_MANIFEST_SLOT",
            "evidence_source": "tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01",
            "required_parent_side_content": "a manifest naming all non-CMB inputs used to construct Phi_tau_eff",
            "endpoint_firewall_rule": "the manifest cannot contain acoustic residuals, lensing residuals, score labels, or CMB likelihood errors",
            "remaining_blocker": "manifest slot exists but the actual parent input manifest is not supplied",
            "scorecard_effect": "creates the provenance object that later score gates must inspect",
        },
        {
            "parent_input_component": "tau_base_field_state",
            "symbol_or_object": "B_tau(parent)",
            "provenance_status": "BLOCKED_BASE_FIELD_STATE_NOT_SUPPLIED",
            "evidence_source": "tau_cmb_effective_source_equation_v01",
            "required_parent_side_content": "base-field state or carrier descriptor independent of CMB endpoint fitting",
            "endpoint_firewall_rule": "base-field state cannot be selected by minimizing CMB score residuals",
            "remaining_blocker": "no parent-side base-field state descriptor is supplied",
            "scorecard_effect": "blocks source normalization and response construction",
        },
        {
            "parent_input_component": "morphological_seed_descriptor",
            "symbol_or_object": "seed_tau(parent)",
            "provenance_status": "BLOCKED_MORPHOLOGICAL_SEED_NOT_SUPPLIED",
            "evidence_source": "tau_cmb_minimal_source_term_candidate_v01",
            "required_parent_side_content": "seed, disturbance, or morphology descriptor that activates the Tau response",
            "endpoint_firewall_rule": "seed descriptor cannot be inferred from the CMB peak pattern after scoring",
            "remaining_blocker": "no endpoint-blind seed descriptor is supplied",
            "scorecard_effect": "blocks a physical interpretation of the source term",
        },
        {
            "parent_input_component": "response_operator_inputs",
            "symbol_or_object": "R_tau inputs",
            "provenance_status": "BLOCKED_RESPONSE_OPERATOR_INPUTS_NOT_SUPPLIED",
            "evidence_source": "tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01",
            "required_parent_side_content": "operator inputs needed to map parent-side Tau data toward an effective potential",
            "endpoint_firewall_rule": "operator inputs cannot be tuned using acoustic, lensing, growth, or radiation score rows",
            "remaining_blocker": "no response-operator input packet is supplied",
            "scorecard_effect": "blocks the Phi_tau_eff derivation rule",
        },
        {
            "parent_input_component": "gauge_normalization_metadata",
            "symbol_or_object": "gauge/norm metadata",
            "provenance_status": "PARTIAL_PARENT_METADATA_REQUIRED",
            "evidence_source": "tau_cmb_effective_potential_source_handoff_v01",
            "required_parent_side_content": "gauge, normalization, sign, and unit metadata fixed before endpoint comparison",
            "endpoint_firewall_rule": "metadata cannot be changed after observing endpoint residuals",
            "remaining_blocker": "metadata requirement is declared but no locked metadata packet exists",
            "scorecard_effect": "prevents false agreement from convention drift",
        },
        {
            "parent_input_component": "endpoint_firewall_audit",
            "symbol_or_object": "audit(endpoint-free parent inputs)",
            "provenance_status": "PARTIAL_FIREWALL_RULE_DECLARED",
            "evidence_source": "tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01",
            "required_parent_side_content": "audit rule proving that no CMB endpoint-derived values enter the parent input packet",
            "endpoint_firewall_rule": "all parent inputs must be traceable to non-endpoint sources before scoring",
            "remaining_blocker": "firewall rule is declared but no input packet exists to audit",
            "scorecard_effect": "prevents circular no-dark scoring",
        },
        {
            "parent_input_component": "provenance_replay_status",
            "symbol_or_object": "replay(parent input provenance)",
            "provenance_status": "BLOCKED_PROVENANCE_REPLAY_NOT_SUPPLIED",
            "evidence_source": "tau_cmb_minimal_scoring_input_contract_v01",
            "required_parent_side_content": "reproducible replay proving parent inputs are fixed before endpoint evaluation",
            "endpoint_firewall_rule": "replay must be executable without reading score outputs or CMB residual tables",
            "remaining_blocker": "no replay package exists",
            "scorecard_effect": "blocks acceptance of Phi_tau_eff as a scoring input",
        },
    ]
    return [
        {
            "provenance_row_id": f"TCMBPTPIP01_{index:03d}",
            "parent_input_supplied": "false",
            "provenance_satisfied": "false",
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
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_PROVENANCE_V01",
            "provenance_rows_declared": len(rows),
            "declared_rows": sum(row["provenance_status"].startswith("DECLARED") for row in rows),
            "partial_rows": sum(row["provenance_status"].startswith("PARTIAL") for row in rows),
            "blocked_rows": sum(row["provenance_status"].startswith("BLOCKED") for row in rows),
            "supplied_rows": sum(row["parent_input_supplied"] == "true" for row in rows),
            "satisfied_rows": sum(row["provenance_satisfied"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "parent_input_provenance_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_PROVENANCE_DECLARED_UNSATISFIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_candidate_manifest_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_provenance_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Provenance v01

**Doc class:** parent-input provenance manifest scaffold
**Status:** provenance slots declared but unsatisfied; no parent inputs, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_provenance.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_provenance_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_provenance_summary_v01.csv
```

This artifact declares the parent-side input provenance slots required before
`Phi_tau_eff(a,k)` can be derived endpoint-blind.
It does not supply parent inputs. It does not derive `Phi_tau_eff`.

The endpoint firewall is explicit: acoustic residuals, lensing residuals, score
labels, and CMB likelihood errors cannot enter the parent-input packet.

The parent-input provenance is not satisfied:

```text
parent_input_provenance_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_candidate_manifest_v01
```

## Claim Boundary

This artifact declares provenance slots only. It supplies no parent-side Tau
inputs, derives no `Phi_tau_eff`, computes no score, supplies no CMB likelihood,
declares no reproduction or failure, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = provenance_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_provenance_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_provenance_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_PROVENANCE_V01_BUILT")


if __name__ == "__main__":
    main()
