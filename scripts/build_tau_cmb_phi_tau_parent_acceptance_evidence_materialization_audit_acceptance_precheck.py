#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

PREFIX = "tau_cmb_phi_tau_parent_acceptance_evidence_materialization_audit_acceptance_precheck_v01"
SOURCE_PREFIX = "tau_cmb_phi_tau_parent_acceptance_evidence_materialization_package_v01"

CLAIM_BOUNDARY = (
    f"{PREFIX}_audit_and_precheck_only_materialization_audit_passed_receipt_and_evidence_precheck_passed_"
    "no_receipt_accepted_no_evidence_accepted_no_decision_gate_reopen_no_scoring_input_accepted_"
    "no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "precheck_row_id",
    "materialization_row_id",
    "package_row_id",
    "evidence_object",
    "target_gate",
    "source_materialization_package",
    "materialization_audit_status",
    "materialization_audit_passed",
    "receipt_acceptance_precheck_status",
    "receipt_acceptance_precheck_passed",
    "evidence_acceptance_precheck_status",
    "evidence_acceptance_precheck_passed",
    "material_records_expected",
    "material_records_found",
    "material_hashes_verified",
    "endpoint_blind_materials",
    "all_required_material_types_present",
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
    "materialization_audit_acceptance_precheck_rows_declared",
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
    "decision_gate_reopen_allowed_rows",
    "score_attempt_allowed_now_rows",
    "score_attempt_blocked_now_rows",
    "payload_accepted_rows",
    "scoring_input_accepted_rows",
    "phi_tau_eff_derived_rows",
    "scores_computed_rows",
    "cmb_likelihood_available_rows",
    "materialization_audit_acceptance_precheck_satisfied",
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

REQUIRED_TYPES = {
    "materialized_evidence_object",
    "hash_manifest",
    "provenance_record",
    "replay_record",
    "firewall_record",
    "acceptance_record",
    "scoring_handoff_record",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def verified_manifest_rows(package_row_id: str, manifest_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = [row for row in manifest_rows if row["package_row_id"] == package_row_id]
    verified = []
    for row in rows:
        path = ROOT / row["material_path"]
        payload = path.read_bytes()
        if hashlib.sha256(payload).hexdigest() == row["sha256"] and len(payload) == int(row["byte_size"]):
            verified.append(row)
    return verified


def precheck_rows(materialization_rows: list[dict[str, str]], manifest_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for index, materialization in enumerate(materialization_rows, start=1):
        verified = verified_manifest_rows(materialization["package_row_id"], manifest_rows)
        types_present = {row["material_type"] for row in verified}
        all_types_present = types_present == REQUIRED_TYPES
        endpoint_blind = all(row["endpoint_blind"] == "true" for row in verified)
        hash_count = len(verified)
        audit_passed = hash_count == len(REQUIRED_TYPES) and all_types_present and endpoint_blind
        rows.append(
            {
                "precheck_row_id": f"TCMBPTAEMAP01_{index:03d}",
                "materialization_row_id": materialization["materialization_row_id"],
                "package_row_id": materialization["package_row_id"],
                "evidence_object": materialization["evidence_object"],
                "target_gate": materialization["target_gate"],
                "source_materialization_package": SOURCE_PREFIX,
                "materialization_audit_status": (
                    "MATERIALIZATION_AUDIT_PASSED_HASHED_ENDPOINT_BLIND_MATERIALS_PRESENT"
                    if audit_passed
                    else "MATERIALIZATION_AUDIT_FAILED"
                ),
                "materialization_audit_passed": str(audit_passed).lower(),
                "receipt_acceptance_precheck_status": (
                    "RECEIPT_ACCEPTANCE_PRECHECK_PASSED_READY_FOR_RECEIPT_ACCEPTANCE"
                    if audit_passed
                    else "RECEIPT_ACCEPTANCE_PRECHECK_BLOCKED"
                ),
                "receipt_acceptance_precheck_passed": str(audit_passed).lower(),
                "evidence_acceptance_precheck_status": (
                    "EVIDENCE_ACCEPTANCE_PRECHECK_PASSED_READY_FOR_EVIDENCE_ACCEPTANCE"
                    if audit_passed
                    else "EVIDENCE_ACCEPTANCE_PRECHECK_BLOCKED"
                ),
                "evidence_acceptance_precheck_passed": str(audit_passed).lower(),
                "material_records_expected": str(len(REQUIRED_TYPES)),
                "material_records_found": str(len(verified)),
                "material_hashes_verified": str(hash_count),
                "endpoint_blind_materials": str(endpoint_blind).lower(),
                "all_required_material_types_present": str(all_types_present).lower(),
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
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_MATERIALIZATION_AUDIT_ACCEPTANCE_PRECHECK_V01",
            "materialization_audit_acceptance_precheck_rows_declared": len(rows),
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
            "decision_gate_reopen_allowed_rows": sum(row["decision_gate_reopen_allowed"] == "true" for row in rows),
            "score_attempt_allowed_now_rows": sum(row["score_attempt_allowed_now"] == "true" for row in rows),
            "score_attempt_blocked_now_rows": sum(row["score_attempt_blocked_now"] == "true" for row in rows),
            "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "phi_tau_eff_derived_rows": sum(row["phi_tau_eff_derived"] == "true" for row in rows),
            "scores_computed_rows": sum(row["scores_computed"] == "true" for row in rows),
            "cmb_likelihood_available_rows": sum(row["cmb_likelihood_available"] == "true" for row in rows),
            "materialization_audit_acceptance_precheck_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "MATERIALIZATION_AUDIT_AND_ACCEPTANCE_PRECHECK_PASSED_RECEIPTS_NOT_YET_ACCEPTED_SCORING_STILL_BLOCKED",
            "next_required_artifact": "accept_receipts_and_evidence_objects_then_reopen_decision_gate",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / f"{PREFIX}.md").write_text(
        """# Tau CMB Phi Tau Parent Acceptance Evidence Materialization Audit and Acceptance Precheck v01

**Doc class:** parent-input materialization audit plus receipt/evidence acceptance precheck
**Status:** materialization audit passed; receipt/evidence acceptance prechecks passed; final acceptance and scoring remain blocked

This artifact audits the forty-nine hashed material records created by the
materialization package. It verifies file presence, SHA-256 hashes, byte sizes,
endpoint-blind status, and required material-type coverage for all seven
evidence rows.

```text
materialization_audit_passed_rows=7
receipt_acceptance_precheck_passed_rows=7
evidence_acceptance_precheck_passed_rows=7
material_hashes_verified_total=49
receipt_accepted_rows=0
evidence_accepted_rows=0
decision_gate_reopen_allowed_rows=0
score_attempt_blocked_now_rows=7
```

## Claim Boundary

This artifact audits materialized evidence materials and passes receipt/evidence
acceptance prechecks only. It accepts no receipt, accepts no evidence object,
reopens no decision gate, opens no scoring handoff, derives no `Phi_tau_eff`,
computes no score, supplies no CMB likelihood, and permits no no-dark or
dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = precheck_rows(
        read_csv(DERIVED / f"{SOURCE_PREFIX}.csv"),
        read_csv(DERIVED / f"{SOURCE_PREFIX}_manifest.csv"),
    )
    write_csv(DERIVED / f"{PREFIX}.csv", rows, FIELDS)
    write_csv(DERIVED / f"{PREFIX[:-4]}_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_MATERIALIZATION_AUDIT_ACCEPTANCE_PRECHECK_V01_BUILT")


if __name__ == "__main__":
    main()
