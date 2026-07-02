#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

PREFIX = "tau_cmb_phi_tau_parent_acceptance_evidence_materialization_package_v01"
SOURCE_PREFIX = "tau_cmb_phi_tau_parent_acceptance_evidence_fulfillment_package_v01"
MATERIAL_DIR = DERIVED / "tau_cmb_phi_tau_parent_acceptance_evidence_materials_v01"

CLAIM_BOUNDARY = (
    f"{PREFIX}_materialization_only_records_created_and_hashed_no_receipt_accepted_no_evidence_accepted_"
    "no_decision_gate_reopen_no_scoring_input_accepted_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

MATERIALS = [
    "materialized_evidence_object",
    "hash_manifest",
    "provenance_record",
    "replay_record",
    "firewall_record",
    "acceptance_record",
    "scoring_handoff_record",
]

FIELDS = [
    "materialization_row_id",
    "package_row_id",
    "evidence_object",
    "target_gate",
    "source_fulfillment_package",
    "materialization_status",
    "materialized_evidence_object_present",
    "hash_manifest_present",
    "provenance_record_present",
    "replay_record_present",
    "firewall_record_present",
    "acceptance_record_present",
    "scoring_handoff_record_present",
    "material_records_created",
    "material_records_hashed",
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

MANIFEST_FIELDS = [
    "manifest_row_id",
    "package_row_id",
    "evidence_object",
    "material_type",
    "material_path",
    "sha256",
    "byte_size",
    "material_present",
    "endpoint_blind",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "acceptance_evidence_materialization_package_rows_declared",
    "material_records_required",
    "material_records_created",
    "material_records_hashed",
    "materialized_evidence_object_present_rows",
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
    "acceptance_evidence_materialization_package_satisfied",
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


def material_payload(package_row: dict[str, str], material_type: str) -> dict[str, str]:
    return {
        "artifact": PREFIX,
        "package_row_id": package_row["package_row_id"],
        "evidence_object": package_row["evidence_object"],
        "target_gate": package_row["target_gate"],
        "material_type": material_type,
        "source_fulfillment_package": SOURCE_PREFIX,
        "endpoint_blind": "true",
        "acceptance_status": "materialized_not_accepted",
        "score_status": "not_scored",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_material(package_row: dict[str, str], material_type: str) -> tuple[str, str, int]:
    MATERIAL_DIR.mkdir(parents=True, exist_ok=True)
    path = MATERIAL_DIR / f"{package_row['package_row_id']}_{material_type}.json"
    payload = material_payload(package_row, material_type)
    encoded = (json.dumps(payload, sort_keys=True, indent=2) + "\n").encode("utf-8")
    path.write_bytes(encoded)
    return str(path.relative_to(ROOT)), hashlib.sha256(encoded).hexdigest(), len(encoded)


def build_rows(package_rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, object]]]:
    materialization_rows = []
    manifest_rows = []
    for index, package_row in enumerate(package_rows, start=1):
        material_count = 0
        for material_index, material_type in enumerate(MATERIALS, start=1):
            rel_path, digest, byte_size = write_material(package_row, material_type)
            material_count += 1
            manifest_rows.append(
                {
                    "manifest_row_id": f"TCMBPTAEMP01_{index:03d}_{material_index:02d}",
                    "package_row_id": package_row["package_row_id"],
                    "evidence_object": package_row["evidence_object"],
                    "material_type": material_type,
                    "material_path": rel_path,
                    "sha256": digest,
                    "byte_size": byte_size,
                    "material_present": "true",
                    "endpoint_blind": "true",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        materialization_rows.append(
            {
                "materialization_row_id": f"TCMBPTAEMP01_{index:03d}",
                "package_row_id": package_row["package_row_id"],
                "evidence_object": package_row["evidence_object"],
                "target_gate": package_row["target_gate"],
                "source_fulfillment_package": SOURCE_PREFIX,
                "materialization_status": "ACCEPTANCE_EVIDENCE_MATERIALS_CREATED_HASHED_NOT_ACCEPTED",
                "materialized_evidence_object_present": "true",
                "hash_manifest_present": "true",
                "provenance_record_present": "true",
                "replay_record_present": "true",
                "firewall_record_present": "true",
                "acceptance_record_present": "true",
                "scoring_handoff_record_present": "true",
                "material_records_created": str(material_count),
                "material_records_hashed": str(material_count),
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
    return materialization_rows, manifest_rows


def summary(rows: list[dict[str, str]], manifest_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_MATERIALIZATION_PACKAGE_V01",
            "acceptance_evidence_materialization_package_rows_declared": len(rows),
            "material_records_required": len(rows) * len(MATERIALS),
            "material_records_created": len(manifest_rows),
            "material_records_hashed": len(manifest_rows),
            "materialized_evidence_object_present_rows": sum(
                row["materialized_evidence_object_present"] == "true" for row in rows
            ),
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
            "acceptance_evidence_materialization_package_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "ACCEPTANCE_EVIDENCE_MATERIALS_CREATED_HASHED_NOT_ACCEPTED_SCORING_STILL_BLOCKED",
            "next_required_artifact": "audit_acceptance_evidence_materialization_and_accept_receipts",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / f"{PREFIX}.md").write_text(
        """# Tau CMB Phi Tau Parent Acceptance Evidence Materialization Package v01

**Doc class:** parent-input acceptance-evidence materialization package
**Status:** evidence materials created and hashed; receipts/evidence not yet accepted; scoring remains blocked

This artifact materializes the seven required acceptance-evidence rows into
forty-nine endpoint-blind JSON material records and records their SHA-256
hashes. It advances the fulfillment package from requirements-only to
file-level evidence materialization, but does not accept any receipt or
evidence object.

```text
acceptance_evidence_materialization_package_rows_declared=7
material_records_required=49
material_records_created=49
material_records_hashed=49
receipt_accepted_rows=0
evidence_accepted_rows=0
decision_gate_reopen_allowed_rows=0
score_attempt_blocked_now_rows=7
```

## Claim Boundary

This artifact materializes and hashes acceptance-evidence materials only. It
accepts no receipt, accepts no evidence, reopens no decision gate, opens no
scoring handoff, derives no `Phi_tau_eff`, computes no score, supplies no CMB
likelihood, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows, manifest_rows = build_rows(source_rows())
    write_csv(DERIVED / f"{PREFIX}.csv", rows, FIELDS)
    write_csv(DERIVED / f"{PREFIX}_manifest.csv", manifest_rows, MANIFEST_FIELDS)
    write_csv(DERIVED / f"{PREFIX[:-4]}_summary_v01.csv", summary(rows, manifest_rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_MATERIALIZATION_PACKAGE_V01_BUILT")


if __name__ == "__main__":
    main()
