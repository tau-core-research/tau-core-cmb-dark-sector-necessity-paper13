#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

PREFIX = "tau_cmb_phi_tau_parent_acceptance_evidence_fulfillment_package_v01"
SOURCE_PREFIX = (
    "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_"
    "scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_audit_v01"
)

CLAIM_BOUNDARY = (
    f"{PREFIX}_fulfillment_package_only_requirements_declared_no_evidence_materialized_no_receipt_accepted_"
    "no_handoff_reopened_no_payload_accepted_no_scoring_input_accepted_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

REQUIRED_MATERIALS = [
    "materialized_evidence_object",
    "hash_manifest",
    "provenance_record",
    "replay_record",
    "firewall_record",
    "acceptance_record",
    "scoring_handoff_record",
]

FIELDS = [
    "package_row_id",
    "evidence_object",
    "target_gate",
    "source_decision_gate_audit",
    "fulfillment_status",
    "required_materials",
    "required_material_count",
    "requirements_declared",
    "evidence_materialized",
    "hash_manifest_present",
    "provenance_record_present",
    "replay_record_present",
    "firewall_record_present",
    "acceptance_record_present",
    "scoring_handoff_record_present",
    "receipt_accepted",
    "evidence_accepted",
    "decision_gate_reopen_allowed",
    "score_attempt_allowed_now",
    "score_attempt_blocked_now",
    "payload_accepted",
    "scoring_input_accepted",
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
    "acceptance_evidence_fulfillment_package_rows_declared",
    "requirements_declared_rows",
    "required_material_count_total",
    "evidence_materialized_rows",
    "hash_manifest_present_rows",
    "provenance_record_present_rows",
    "replay_record_present_rows",
    "firewall_record_present_rows",
    "acceptance_record_present_rows",
    "scoring_handoff_record_present_rows",
    "receipt_accepted_rows",
    "evidence_accepted_rows",
    "decision_gate_reopen_allowed_rows",
    "score_attempt_allowed_now_rows",
    "score_attempt_blocked_now_rows",
    "payload_accepted_rows",
    "scoring_input_accepted_rows",
    "phi_tau_eff_derived_rows",
    "scores_computed_rows",
    "cmb_likelihood_available_rows",
    "acceptance_evidence_fulfillment_package_satisfied",
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


def source_rows() -> list[dict[str, str]]:
    with (DERIVED / f"{SOURCE_PREFIX}.csv").open(newline="") as handle:
        return list(csv.DictReader(handle))


def package_rows(decision_audit_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for index, source in enumerate(decision_audit_rows, start=1):
        rows.append(
            {
                "package_row_id": f"TCMBPTAEFP01_{index:03d}",
                "evidence_object": source["evidence_object"],
                "target_gate": source["target_gate"],
                "source_decision_gate_audit": SOURCE_PREFIX,
                "fulfillment_status": "ACCEPTANCE_EVIDENCE_FULFILLMENT_PACKAGE_DECLARED_NOT_MATERIALIZED",
                "required_materials": ";".join(REQUIRED_MATERIALS),
                "required_material_count": str(len(REQUIRED_MATERIALS)),
                "requirements_declared": "true",
                "evidence_materialized": "false",
                "hash_manifest_present": "false",
                "provenance_record_present": "false",
                "replay_record_present": "false",
                "firewall_record_present": "false",
                "acceptance_record_present": "false",
                "scoring_handoff_record_present": "false",
                "receipt_accepted": "false",
                "evidence_accepted": "false",
                "decision_gate_reopen_allowed": "false",
                "score_attempt_allowed_now": "false",
                "score_attempt_blocked_now": "true",
                "payload_accepted": "false",
                "scoring_input_accepted": "false",
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


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_FULFILLMENT_PACKAGE_V01",
            "acceptance_evidence_fulfillment_package_rows_declared": len(rows),
            "requirements_declared_rows": sum(row["requirements_declared"] == "true" for row in rows),
            "required_material_count_total": sum(int(row["required_material_count"]) for row in rows),
            "evidence_materialized_rows": sum(row["evidence_materialized"] == "true" for row in rows),
            "hash_manifest_present_rows": sum(row["hash_manifest_present"] == "true" for row in rows),
            "provenance_record_present_rows": sum(row["provenance_record_present"] == "true" for row in rows),
            "replay_record_present_rows": sum(row["replay_record_present"] == "true" for row in rows),
            "firewall_record_present_rows": sum(row["firewall_record_present"] == "true" for row in rows),
            "acceptance_record_present_rows": sum(row["acceptance_record_present"] == "true" for row in rows),
            "scoring_handoff_record_present_rows": sum(row["scoring_handoff_record_present"] == "true" for row in rows),
            "receipt_accepted_rows": sum(row["receipt_accepted"] == "true" for row in rows),
            "evidence_accepted_rows": sum(row["evidence_accepted"] == "true" for row in rows),
            "decision_gate_reopen_allowed_rows": sum(row["decision_gate_reopen_allowed"] == "true" for row in rows),
            "score_attempt_allowed_now_rows": sum(row["score_attempt_allowed_now"] == "true" for row in rows),
            "score_attempt_blocked_now_rows": sum(row["score_attempt_blocked_now"] == "true" for row in rows),
            "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "phi_tau_eff_derived_rows": sum(row["phi_tau_eff_derived"] == "true" for row in rows),
            "scores_computed_rows": sum(row["scores_computed"] == "true" for row in rows),
            "cmb_likelihood_available_rows": sum(row["cmb_likelihood_available"] == "true" for row in rows),
            "acceptance_evidence_fulfillment_package_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "ACCEPTANCE_EVIDENCE_FULFILLMENT_PACKAGE_DECLARED_NOT_MATERIALIZED_SCORING_STILL_BLOCKED",
            "next_required_artifact": "materialize_acceptance_evidence_objects_and_replay_acceptance_checks",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / f"{PREFIX}.md").write_text(
        """# Tau CMB Phi Tau Parent Acceptance Evidence Fulfillment Package v01

**Doc class:** parent-input acceptance-evidence fulfillment package
**Status:** requirements declared; acceptance evidence not materialized; scoring remains blocked

This package consolidates the seven acceptance-evidence rows required to reopen
the closed decision gate. Each row requires a materialized evidence object,
hash manifest, provenance record, replay record, firewall record, acceptance
record, and scoring-handoff record.

```text
acceptance_evidence_fulfillment_package_rows_declared=7
requirements_declared_rows=7
required_material_count_total=49
evidence_materialized_rows=0
receipt_accepted_rows=0
evidence_accepted_rows=0
decision_gate_reopen_allowed_rows=0
score_attempt_blocked_now_rows=7
```

## Claim Boundary

This artifact declares a fulfillment package only. It materializes no evidence
object, accepts no receipt, accepts no evidence, reopens no decision gate,
opens no scoring handoff, derives no `Phi_tau_eff`, computes no score, supplies
no CMB likelihood, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = package_rows(source_rows())
    write_csv(DERIVED / f"{PREFIX}.csv", rows, FIELDS)
    write_csv(DERIVED / f"{PREFIX[:-4]}_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_FULFILLMENT_PACKAGE_V01_BUILT")


if __name__ == "__main__":
    main()
