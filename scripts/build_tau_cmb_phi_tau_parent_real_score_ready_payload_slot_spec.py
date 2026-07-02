#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

PREFIX = "tau_cmb_phi_tau_parent_real_score_ready_payload_slot_spec_v01"
SOURCE_PREFIX = "tau_cmb_phi_tau_parent_real_score_ready_input_supply_contract_v01"

CLAIM_BOUNDARY = (
    f"{PREFIX}_slot_spec_only_no_payload_materialized_no_slot_accepted_"
    "no_scoring_input_accepted_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

MATERIAL_SPECS = {
    "phi_tau_eff_source": {
        "artifact_suffix": "phi_tau_eff_source.csv",
        "schema_fields": "source_id|k_grid|a_grid|phi_tau_eff_values|units|sign_convention|derivation_rule_id",
        "validation_rule": "dimensioned Phi_tau_eff(a,k) source with endpoint-blind derivation replay",
        "required_to_unlock": "Phi_tau_eff source must be materialized and accepted",
    },
    "dimension_replay": {
        "artifact_suffix": "dimension_replay.json",
        "schema_fields": "replay_command|input_hashes|output_hash|unit_audit|convention_audit",
        "validation_rule": "deterministic replay must reproduce the dimension and convention audit",
        "required_to_unlock": "dimension replay must pass for the same source object",
    },
    "normalization_binding": {
        "artifact_suffix": "normalization_binding.csv",
        "schema_fields": "normalization_id|gauge_choice|amplitude_reference|zero_source_limit",
        "validation_rule": "normalization and gauge choices must be bound before endpoint readout",
        "required_to_unlock": "normalization must be bound without endpoint fitting",
    },
    "endpoint_blind_provenance": {
        "artifact_suffix": "endpoint_blind_provenance.json",
        "schema_fields": "provenance_id|source_hash|endpoint_label_firewall|freeze_timestamp",
        "validation_rule": "source provenance must be frozen before any CMB endpoint labels enter",
        "required_to_unlock": "endpoint-blind provenance must pass the firewall",
    },
    "cmb_readout_mapping": {
        "artifact_suffix": "cmb_readout_mapping.csv",
        "schema_fields": "mapping_id|observable_family|ell_or_k_mapping|transfer_interface",
        "validation_rule": "Tau-side source must map to CMB acoustic/lensing/growth readout slots",
        "required_to_unlock": "CMB readout mapping must be declared and replayable",
    },
    "likelihood_adapter": {
        "artifact_suffix": "likelihood_adapter.json",
        "schema_fields": "adapter_id|data_vector_binding|covariance_binding|likelihood_command",
        "validation_rule": "adapter must bind the accepted prediction vector to the frozen CMB likelihood",
        "required_to_unlock": "likelihood adapter must be executable without changing source parameters",
    },
    "acceptance_replay": {
        "artifact_suffix": "acceptance_replay.json",
        "schema_fields": "acceptance_id|validator_command|expected_pass_fields|acceptance_hash",
        "validation_rule": "the full accepted-input decision must be replayable from materialized artifacts",
        "required_to_unlock": "acceptance replay must pass and produce accepted scoring input",
    },
}

FIELDS = [
    "slot_row_id",
    "contract_row_id",
    "certificate_row_id",
    "evidence_object",
    "target_gate",
    "material_class",
    "expected_artifact_path",
    "required_schema_fields",
    "validation_rule",
    "required_to_unlock",
    "source_contract",
    "slot_status",
    "payload_materialized",
    "payload_hash_bound",
    "dimension_replay_passed",
    "endpoint_blind_firewall_passed",
    "slot_accepted",
    "scoring_input_accepted",
    "reopen_scoring_route_allowed_now",
    "score_attempt_allowed_now",
    "phi_tau_eff_derived",
    "scores_computed",
    "cmb_likelihood_available",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "contract_rows",
    "payload_slot_rows_declared",
    "material_classes_per_contract_row",
    "expected_artifact_paths_declared",
    "payload_materialized_rows",
    "payload_hash_bound_rows",
    "dimension_replay_passed_rows",
    "endpoint_blind_firewall_passed_rows",
    "slot_accepted_rows",
    "scoring_input_accepted_rows",
    "reopen_scoring_route_allowed_now_rows",
    "score_attempt_allowed_now_rows",
    "score_attempt_blocked_now_rows",
    "phi_tau_eff_derived_rows",
    "scores_computed_rows",
    "cmb_likelihood_available_rows",
    "payload_slot_spec_satisfied",
    "all_required_slots_materialized",
    "all_required_slots_accepted",
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def slot_rows(contract_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for contract_index, contract in enumerate(contract_rows, start=1):
        for material_index, (material_class, spec) in enumerate(MATERIAL_SPECS.items(), start=1):
            row_index = (contract_index - 1) * len(MATERIAL_SPECS) + material_index
            rows.append(
                {
                    "slot_row_id": f"TCMBPTARSPS01_{row_index:03d}",
                    "contract_row_id": contract["contract_row_id"],
                    "certificate_row_id": contract["certificate_row_id"],
                    "evidence_object": contract["evidence_object"],
                    "target_gate": contract["target_gate"],
                    "material_class": material_class,
                    "expected_artifact_path": (
                        "data/score_ready_input/"
                        f"{contract['contract_row_id']}/{spec['artifact_suffix']}"
                    ),
                    "required_schema_fields": spec["schema_fields"],
                    "validation_rule": spec["validation_rule"],
                    "required_to_unlock": spec["required_to_unlock"],
                    "source_contract": SOURCE_PREFIX,
                    "slot_status": "PAYLOAD_SLOT_DECLARED_INPUT_NOT_MATERIALIZED",
                    "payload_materialized": "false",
                    "payload_hash_bound": "false",
                    "dimension_replay_passed": "false",
                    "endpoint_blind_firewall_passed": "false",
                    "slot_accepted": "false",
                    "scoring_input_accepted": "false",
                    "reopen_scoring_route_allowed_now": "false",
                    "score_attempt_allowed_now": "false",
                    "phi_tau_eff_derived": "false",
                    "scores_computed": "false",
                    "cmb_likelihood_available": "false",
                    "blocks_no_dark_claim": "true",
                    "allows_tau_response_claim": "false",
                    "allows_dark_sector_verdict": "false",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def summary(rows: list[dict[str, str]], contract_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_REAL_SCORE_READY_PAYLOAD_SLOT_SPEC_V01",
            "contract_rows": len(contract_rows),
            "payload_slot_rows_declared": len(rows),
            "material_classes_per_contract_row": len(MATERIAL_SPECS),
            "expected_artifact_paths_declared": sum(bool(row["expected_artifact_path"]) for row in rows),
            "payload_materialized_rows": sum(row["payload_materialized"] == "true" for row in rows),
            "payload_hash_bound_rows": sum(row["payload_hash_bound"] == "true" for row in rows),
            "dimension_replay_passed_rows": sum(row["dimension_replay_passed"] == "true" for row in rows),
            "endpoint_blind_firewall_passed_rows": sum(
                row["endpoint_blind_firewall_passed"] == "true" for row in rows
            ),
            "slot_accepted_rows": sum(row["slot_accepted"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "reopen_scoring_route_allowed_now_rows": sum(
                row["reopen_scoring_route_allowed_now"] == "true" for row in rows
            ),
            "score_attempt_allowed_now_rows": sum(row["score_attempt_allowed_now"] == "true" for row in rows),
            "score_attempt_blocked_now_rows": sum(row["score_attempt_allowed_now"] == "false" for row in rows),
            "phi_tau_eff_derived_rows": sum(row["phi_tau_eff_derived"] == "true" for row in rows),
            "scores_computed_rows": sum(row["scores_computed"] == "true" for row in rows),
            "cmb_likelihood_available_rows": sum(row["cmb_likelihood_available"] == "true" for row in rows),
            "payload_slot_spec_satisfied": "true",
            "all_required_slots_materialized": "false",
            "all_required_slots_accepted": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PAYLOAD_SLOT_SPEC_DECLARED_INPUT_NOT_MATERIALIZED_ROUTE_REMAINS_LOCKED",
            "next_required_artifact": "materialize_all_payload_slots_with_hash_bound_endpoint_blind_replay",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    material_lines = "\n".join(
        f"- `{name}`: `{spec['schema_fields']}`" for name, spec in MATERIAL_SPECS.items()
    )
    (DOCS / f"{PREFIX}.md").write_text(
        f"""# Tau CMB Phi Tau Parent Real Score-Ready Payload Slot Spec v01

**Doc class:** real score-ready payload slot specification
**Status:** slot specification declared; no payload materialized

This artifact expands the real score-ready input supply contract into concrete
payload slots. Each locked route row receives seven expected artifact paths and
field schemas. The package does not materialize any payload file and does not
accept any scoring input.

Required material schemas:

{material_lines}

Summary:

```text
contract_rows=7
payload_slot_rows_declared=49
expected_artifact_paths_declared=49
payload_materialized_rows=0
slot_accepted_rows=0
scoring_input_accepted_rows=0
score_attempt_blocked_now_rows=49
```

## Claim Boundary

This artifact is a slot specification only. It supplies no score-ready payload,
binds no payload hash, accepts no scoring input, derives no `Phi_tau_eff`,
computes no score, supplies no CMB likelihood, and permits no no-dark or
dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    contract = read_csv(DERIVED / f"{SOURCE_PREFIX}.csv")
    rows = slot_rows(contract)
    write_csv(DERIVED / f"{PREFIX}.csv", rows, FIELDS)
    write_csv(DERIVED / f"{PREFIX[:-4]}_summary_v01.csv", summary(rows, contract), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_REAL_SCORE_READY_PAYLOAD_SLOT_SPEC_V01_BUILT")


if __name__ == "__main__":
    main()
