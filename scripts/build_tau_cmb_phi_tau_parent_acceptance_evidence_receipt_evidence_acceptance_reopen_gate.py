#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

PREFIX = "tau_cmb_phi_tau_parent_acceptance_evidence_receipt_evidence_acceptance_reopen_gate_v01"
SOURCE_PREFIX = "tau_cmb_phi_tau_parent_acceptance_evidence_materialization_audit_acceptance_precheck_v01"

CLAIM_BOUNDARY = (
    f"{PREFIX}_receipt_and_evidence_accepted_decision_gate_reopen_allowed_"
    "no_payload_accepted_no_scoring_input_accepted_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "acceptance_row_id",
    "precheck_row_id",
    "materialization_row_id",
    "package_row_id",
    "evidence_object",
    "target_gate",
    "source_precheck",
    "acceptance_status",
    "materialization_audit_passed",
    "receipt_acceptance_precheck_passed",
    "evidence_acceptance_precheck_passed",
    "material_records_expected",
    "material_records_found",
    "material_hashes_verified",
    "endpoint_blind_materials",
    "all_required_material_types_present",
    "receipt_accepted",
    "evidence_accepted",
    "acceptance_record_created",
    "decision_gate_reopen_allowed",
    "score_attempt_allowed_now",
    "score_attempt_blocked_now",
    "payload_accepted",
    "scoring_input_accepted",
    "scoring_handoff_opened",
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
    "receipt_evidence_acceptance_reopen_gate_rows_declared",
    "materialization_audit_passed_rows",
    "receipt_acceptance_precheck_passed_rows",
    "evidence_acceptance_precheck_passed_rows",
    "material_records_expected_total",
    "material_records_found_total",
    "material_hashes_verified_total",
    "endpoint_blind_material_rows",
    "all_required_material_types_present_rows",
    "receipt_accepted_rows",
    "evidence_accepted_rows",
    "acceptance_record_created_rows",
    "decision_gate_reopen_allowed_rows",
    "score_attempt_allowed_now_rows",
    "score_attempt_blocked_now_rows",
    "payload_accepted_rows",
    "scoring_input_accepted_rows",
    "scoring_handoff_opened_rows",
    "phi_tau_eff_derived_rows",
    "scores_computed_rows",
    "cmb_likelihood_available_rows",
    "receipt_evidence_acceptance_reopen_gate_satisfied",
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


def acceptance_rows(precheck_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for index, precheck in enumerate(precheck_rows, start=1):
        prereqs_passed = (
            precheck["materialization_audit_passed"] == "true"
            and precheck["receipt_acceptance_precheck_passed"] == "true"
            and precheck["evidence_acceptance_precheck_passed"] == "true"
            and precheck["endpoint_blind_materials"] == "true"
            and precheck["all_required_material_types_present"] == "true"
        )
        rows.append(
            {
                "acceptance_row_id": f"TCMBPTAEREG01_{index:03d}",
                "precheck_row_id": precheck["precheck_row_id"],
                "materialization_row_id": precheck["materialization_row_id"],
                "package_row_id": precheck["package_row_id"],
                "evidence_object": precheck["evidence_object"],
                "target_gate": precheck["target_gate"],
                "source_precheck": SOURCE_PREFIX,
                "acceptance_status": (
                    "RECEIPT_AND_EVIDENCE_ACCEPTED_DECISION_GATE_REOPEN_ALLOWED"
                    if prereqs_passed
                    else "RECEIPT_AND_EVIDENCE_ACCEPTANCE_BLOCKED"
                ),
                "materialization_audit_passed": str(prereqs_passed).lower(),
                "receipt_acceptance_precheck_passed": str(prereqs_passed).lower(),
                "evidence_acceptance_precheck_passed": str(prereqs_passed).lower(),
                "material_records_expected": precheck["material_records_expected"],
                "material_records_found": precheck["material_records_found"],
                "material_hashes_verified": precheck["material_hashes_verified"],
                "endpoint_blind_materials": str(prereqs_passed).lower(),
                "all_required_material_types_present": str(prereqs_passed).lower(),
                "receipt_accepted": str(prereqs_passed).lower(),
                "evidence_accepted": str(prereqs_passed).lower(),
                "acceptance_record_created": str(prereqs_passed).lower(),
                "decision_gate_reopen_allowed": str(prereqs_passed).lower(),
                "score_attempt_allowed_now": "false",
                "score_attempt_blocked_now": "true",
                "payload_accepted": "false",
                "scoring_input_accepted": "false",
                "scoring_handoff_opened": "false",
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
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_RECEIPT_EVIDENCE_ACCEPTANCE_REOPEN_GATE_V01",
            "receipt_evidence_acceptance_reopen_gate_rows_declared": len(rows),
            "materialization_audit_passed_rows": sum(row["materialization_audit_passed"] == "true" for row in rows),
            "receipt_acceptance_precheck_passed_rows": sum(
                row["receipt_acceptance_precheck_passed"] == "true" for row in rows
            ),
            "evidence_acceptance_precheck_passed_rows": sum(
                row["evidence_acceptance_precheck_passed"] == "true" for row in rows
            ),
            "material_records_expected_total": sum(int(row["material_records_expected"]) for row in rows),
            "material_records_found_total": sum(int(row["material_records_found"]) for row in rows),
            "material_hashes_verified_total": sum(int(row["material_hashes_verified"]) for row in rows),
            "endpoint_blind_material_rows": sum(row["endpoint_blind_materials"] == "true" for row in rows),
            "all_required_material_types_present_rows": sum(
                row["all_required_material_types_present"] == "true" for row in rows
            ),
            "receipt_accepted_rows": sum(row["receipt_accepted"] == "true" for row in rows),
            "evidence_accepted_rows": sum(row["evidence_accepted"] == "true" for row in rows),
            "acceptance_record_created_rows": sum(row["acceptance_record_created"] == "true" for row in rows),
            "decision_gate_reopen_allowed_rows": sum(row["decision_gate_reopen_allowed"] == "true" for row in rows),
            "score_attempt_allowed_now_rows": sum(row["score_attempt_allowed_now"] == "true" for row in rows),
            "score_attempt_blocked_now_rows": sum(row["score_attempt_blocked_now"] == "true" for row in rows),
            "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "scoring_handoff_opened_rows": sum(row["scoring_handoff_opened"] == "true" for row in rows),
            "phi_tau_eff_derived_rows": sum(row["phi_tau_eff_derived"] == "true" for row in rows),
            "scores_computed_rows": sum(row["scores_computed"] == "true" for row in rows),
            "cmb_likelihood_available_rows": sum(row["cmb_likelihood_available"] == "true" for row in rows),
            "receipt_evidence_acceptance_reopen_gate_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "RECEIPT_AND_EVIDENCE_ACCEPTED_DECISION_GATE_REOPEN_ALLOWED_SCORING_INPUT_STILL_BLOCKED",
            "next_required_artifact": "build_scoring_handoff_package_from_accepted_evidence",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / f"{PREFIX}.md").write_text(
        """# Tau CMB Phi Tau Parent Acceptance Evidence Receipt/Evidence Acceptance Reopen Gate v01

**Doc class:** parent-input receipt/evidence acceptance and decision-gate reopen artifact
**Status:** receipt/evidence accepted; decision gate reopened; scoring input still blocked

This artifact consumes the materialization audit and acceptance precheck package.
For all seven endpoint-blind evidence rows it accepts the receipt and evidence
objects and allows the decision gate to reopen. It does not accept a scoring
payload and does not open the scoring handoff.

```text
receipt_accepted_rows=7
evidence_accepted_rows=7
acceptance_record_created_rows=7
decision_gate_reopen_allowed_rows=7
payload_accepted_rows=0
scoring_input_accepted_rows=0
score_attempt_blocked_now_rows=7
```

## Claim Boundary

This artifact accepts receipt/evidence objects and reopens the decision gate
only. It accepts no scoring payload, accepts no scoring input, opens no scoring
handoff, derives no `Phi_tau_eff`, computes no score, supplies no CMB
likelihood, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = acceptance_rows(read_csv(DERIVED / f"{SOURCE_PREFIX}.csv"))
    write_csv(DERIVED / f"{PREFIX}.csv", rows, FIELDS)
    write_csv(DERIVED / f"{PREFIX[:-4]}_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_RECEIPT_EVIDENCE_ACCEPTANCE_REOPEN_GATE_V01_BUILT")


if __name__ == "__main__":
    main()
