#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
TEMPLATES = ROOT / "data/score_ready_input_templates"

PREFIX = "tau_cmb_phi_tau_parent_real_score_ready_payload_template_manifest_v01"
SOURCE_PREFIX = "tau_cmb_phi_tau_parent_real_score_ready_payload_slot_spec_v01"

CLAIM_BOUNDARY = (
    f"{PREFIX}_template_manifest_only_no_real_payload_no_hash_binding_"
    "no_slot_accepted_no_scoring_input_accepted_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

CSV_TEMPLATES = {
    "phi_tau_eff_source": [
        "source_id",
        "k_grid",
        "a_grid",
        "phi_tau_eff_values",
        "units",
        "sign_convention",
        "derivation_rule_id",
    ],
    "normalization_binding": [
        "normalization_id",
        "gauge_choice",
        "amplitude_reference",
        "zero_source_limit",
    ],
    "cmb_readout_mapping": [
        "mapping_id",
        "observable_family",
        "ell_or_k_mapping",
        "transfer_interface",
    ],
}

JSON_TEMPLATES = {
    "dimension_replay": {
        "replay_command": "",
        "input_hashes": [],
        "output_hash": "",
        "unit_audit": "",
        "convention_audit": "",
    },
    "endpoint_blind_provenance": {
        "provenance_id": "",
        "source_hash": "",
        "endpoint_label_firewall": "",
        "freeze_timestamp": "",
    },
    "likelihood_adapter": {
        "adapter_id": "",
        "data_vector_binding": "",
        "covariance_binding": "",
        "likelihood_command": "",
    },
    "acceptance_replay": {
        "acceptance_id": "",
        "validator_command": "",
        "expected_pass_fields": [],
        "acceptance_hash": "",
    },
}

FIELDS = [
    "template_binding_row_id",
    "slot_row_id",
    "contract_row_id",
    "material_class",
    "expected_artifact_path",
    "template_path",
    "template_format",
    "required_schema_fields",
    "template_status",
    "template_file_exists",
    "real_payload_materialized",
    "payload_hash_bound",
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
    "slot_rows_consumed",
    "template_bindings_declared",
    "template_files_declared",
    "template_files_written",
    "real_payload_materialized_rows",
    "payload_hash_bound_rows",
    "slot_accepted_rows",
    "scoring_input_accepted_rows",
    "reopen_scoring_route_allowed_now_rows",
    "score_attempt_allowed_now_rows",
    "score_attempt_blocked_now_rows",
    "phi_tau_eff_derived_rows",
    "scores_computed_rows",
    "cmb_likelihood_available_rows",
    "payload_template_manifest_satisfied",
    "all_real_payloads_materialized",
    "all_slots_accepted",
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


def template_path(material_class: str) -> Path:
    suffix = "csv" if material_class in CSV_TEMPLATES else "json"
    return TEMPLATES / f"{material_class}_template.{suffix}"


def write_templates() -> None:
    TEMPLATES.mkdir(parents=True, exist_ok=True)
    for material_class, fields in CSV_TEMPLATES.items():
        write_csv(template_path(material_class), [], fields)
    for material_class, payload in JSON_TEMPLATES.items():
        template_path(material_class).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def binding_rows(slot_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for index, slot in enumerate(slot_rows, start=1):
        path = template_path(slot["material_class"])
        rows.append(
            {
                "template_binding_row_id": f"TCMBPTARSPTM01_{index:03d}",
                "slot_row_id": slot["slot_row_id"],
                "contract_row_id": slot["contract_row_id"],
                "material_class": slot["material_class"],
                "expected_artifact_path": slot["expected_artifact_path"],
                "template_path": str(path.relative_to(ROOT)),
                "template_format": path.suffix.removeprefix("."),
                "required_schema_fields": slot["required_schema_fields"],
                "template_status": "TEMPLATE_BOUND_REAL_PAYLOAD_NOT_MATERIALIZED",
                "template_file_exists": str(path.exists()).lower(),
                "real_payload_materialized": "false",
                "payload_hash_bound": "false",
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


def summary(rows: list[dict[str, str]], slot_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    template_files = {row["template_path"] for row in rows}
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_REAL_SCORE_READY_PAYLOAD_TEMPLATE_MANIFEST_V01",
            "slot_rows_consumed": len(slot_rows),
            "template_bindings_declared": len(rows),
            "template_files_declared": len(template_files),
            "template_files_written": sum((ROOT / path).exists() for path in template_files),
            "real_payload_materialized_rows": sum(row["real_payload_materialized"] == "true" for row in rows),
            "payload_hash_bound_rows": sum(row["payload_hash_bound"] == "true" for row in rows),
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
            "payload_template_manifest_satisfied": "true",
            "all_real_payloads_materialized": "false",
            "all_slots_accepted": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PAYLOAD_TEMPLATE_MANIFEST_DECLARED_REAL_PAYLOAD_NOT_MATERIALIZED_ROUTE_REMAINS_LOCKED",
            "next_required_artifact": "populate_template_files_with_endpoint_blind_real_payloads_and_hash_receipts",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc(rows: list[dict[str, str]]) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    templates = sorted({row["template_path"] for row in rows})
    template_lines = "\n".join(f"- `{path}`" for path in templates)
    (DOCS / f"{PREFIX}.md").write_text(
        f"""# Tau CMB Phi Tau Parent Real Score-Ready Payload Template Manifest v01

**Doc class:** score-ready payload template manifest
**Status:** templates written; no real payload materialized

This artifact binds the 49 payload slots to seven reusable template files. The
templates are input shapes only. They are not real Tau-side CMB payloads, do not
carry physical values, and do not unlock scoring.

Template files:

{template_lines}

Summary:

```text
slot_rows_consumed=49
template_bindings_declared=49
template_files_declared=7
template_files_written=7
real_payload_materialized_rows=0
slot_accepted_rows=0
scoring_input_accepted_rows=0
score_attempt_blocked_now_rows=49
```

## Claim Boundary

This artifact provides template shapes only. It materializes no real payload,
binds no payload hash, accepts no slot, accepts no scoring input, derives no
`Phi_tau_eff`, computes no score, supplies no CMB likelihood, and permits no
no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    write_templates()
    slots = read_csv(DERIVED / f"{SOURCE_PREFIX}.csv")
    rows = binding_rows(slots)
    write_csv(DERIVED / f"{PREFIX}.csv", rows, FIELDS)
    write_csv(DERIVED / f"{PREFIX[:-4]}_summary_v01.csv", summary(rows, slots), SUMMARY_FIELDS)
    write_doc(rows)
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_REAL_SCORE_READY_PAYLOAD_TEMPLATE_MANIFEST_V01_BUILT")


if __name__ == "__main__":
    main()
