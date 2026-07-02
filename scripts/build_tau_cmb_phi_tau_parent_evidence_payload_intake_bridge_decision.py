#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

SOURCE_TABLE = DERIVED / "tau_cmb_phi_tau_parent_evidence_payload_acquisition_audit_v01.csv"

PACKET_ID = "TAU_CMB_PHI_TAU_PARENT_EVIDENCE_PAYLOAD_INTAKE_BRIDGE_DECISION_V01"
CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_evidence_payload_intake_bridge_decision_v01_bridge_decision_only_"
    "candidate_payload_acquired_but_requires_canonical_repackaging_no_parent_acceptance_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

ROW_FIELDS = [
    "bridge_row_id",
    "payload_row_id",
    "certificate_component",
    "bridge_status",
    "candidate_payload_audit_passed",
    "canonical_submission_packet_present",
    "receipt_binding_present",
    "dimension_receipt_ready",
    "replay_receipt_ready",
    "firewall_receipt_ready",
    "canonical_repackaging_required",
    "intake_bridge_passed",
    "parent_payload_accepted",
    "certificate_passed",
    "score_entry_allowed",
    "bridge_decision",
    "next_required_object",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "bridge_rows_declared",
    "candidate_payload_audit_passed_rows",
    "canonical_submission_packet_present_rows",
    "receipt_binding_present_rows",
    "dimension_receipt_ready_rows",
    "replay_receipt_ready_rows",
    "firewall_receipt_ready_rows",
    "canonical_repackaging_required_rows",
    "intake_bridge_passed_rows",
    "parent_payload_accepted_rows",
    "certificate_passed_rows",
    "score_ready_rows",
    "scores_computed",
    "cmb_likelihood_available",
    "tau_response_claim_allowed",
    "dark_sector_verdict_allowed",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bridge_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(SOURCE_TABLE), start=1):
        candidate_passed = source["candidate_payload_audit_passed"] == "true"
        rows.append(
            {
                "bridge_row_id": f"TCMBPTPEPIBD01_{index:03d}",
                "payload_row_id": source["payload_row_id"],
                "certificate_component": source["certificate_component"],
                "bridge_status": (
                    "CANDIDATE_PAYLOAD_ACQUIRED_REPACKAGING_REQUIRED"
                    if candidate_passed
                    else "CANDIDATE_PAYLOAD_NOT_AVAILABLE"
                ),
                "candidate_payload_audit_passed": str(candidate_passed).lower(),
                "canonical_submission_packet_present": "false",
                "receipt_binding_present": "false",
                "dimension_receipt_ready": "false",
                "replay_receipt_ready": "false",
                "firewall_receipt_ready": "false",
                "canonical_repackaging_required": str(candidate_passed).lower(),
                "intake_bridge_passed": "false",
                "parent_payload_accepted": "false",
                "certificate_passed": "false",
                "score_entry_allowed": "false",
                "bridge_decision": "ROUTE_TO_CANONICAL_PAYLOAD_PACKET_AND_RECEIPT_BINDING",
                "next_required_object": "canonical endpoint-blind payload packet with receipt, dimension/replay/firewall binding, and certificate acceptance evidence",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, str]]) -> dict[str, str]:
    return {
        "summary_id": PACKET_ID,
        "bridge_rows_declared": str(len(rows)),
        "candidate_payload_audit_passed_rows": str(sum(row["candidate_payload_audit_passed"] == "true" for row in rows)),
        "canonical_submission_packet_present_rows": str(sum(row["canonical_submission_packet_present"] == "true" for row in rows)),
        "receipt_binding_present_rows": str(sum(row["receipt_binding_present"] == "true" for row in rows)),
        "dimension_receipt_ready_rows": str(sum(row["dimension_receipt_ready"] == "true" for row in rows)),
        "replay_receipt_ready_rows": str(sum(row["replay_receipt_ready"] == "true" for row in rows)),
        "firewall_receipt_ready_rows": str(sum(row["firewall_receipt_ready"] == "true" for row in rows)),
        "canonical_repackaging_required_rows": str(sum(row["canonical_repackaging_required"] == "true" for row in rows)),
        "intake_bridge_passed_rows": str(sum(row["intake_bridge_passed"] == "true" for row in rows)),
        "parent_payload_accepted_rows": str(sum(row["parent_payload_accepted"] == "true" for row in rows)),
        "certificate_passed_rows": str(sum(row["certificate_passed"] == "true" for row in rows)),
        "score_ready_rows": str(sum(row["score_entry_allowed"] == "true" for row in rows)),
        "scores_computed": "false",
        "cmb_likelihood_available": "false",
        "tau_response_claim_allowed": "false",
        "dark_sector_verdict_allowed": "false",
        "overall_status": "PHI_TAU_PARENT_EVIDENCE_PAYLOAD_CANDIDATE_ACQUIRED_CANONICAL_REPACKAGING_REQUIRED",
        "next_required_artifact": "tau_cmb_phi_tau_parent_canonical_payload_packet_v01",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_json(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "phi_tau_parent_evidence_payload_intake_bridge_decision",
        "status": row["overall_status"],
        "claim_boundary": CLAIM_BOUNDARY,
        "bridge_rows": rows,
        "summary": row,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_doc(path: Path, row: dict[str, str]) -> None:
    text = f"""# Tau CMB Phi Tau Parent Evidence Payload Intake Bridge Decision v01

**Doc class:** parent evidence-payload intake bridge decision
**Reader role:** Paper 13 CMB scoring path
**Status:** candidate payload acquired; canonical repackaging and receipt binding required before acceptance
**Canonical parent:** Paper 13 CMB scoring input fulfillment chain

## Purpose

This artifact bridges the newly acquired hash-bound candidate payloads into the
older canonical submission/materialization route. It makes the state explicit:
candidate payloads exist, but they are not yet canonical parent payload packets
with receipt, dimension, replay, firewall, and certificate acceptance binding.

## Summary

```text
bridge_rows_declared={row["bridge_rows_declared"]}
candidate_payload_audit_passed_rows={row["candidate_payload_audit_passed_rows"]}
canonical_submission_packet_present_rows={row["canonical_submission_packet_present_rows"]}
receipt_binding_present_rows={row["receipt_binding_present_rows"]}
canonical_repackaging_required_rows={row["canonical_repackaging_required_rows"]}
intake_bridge_passed_rows={row["intake_bridge_passed_rows"]}
parent_payload_accepted_rows={row["parent_payload_accepted_rows"]}
certificate_passed_rows={row["certificate_passed_rows"]}
score_ready_rows={row["score_ready_rows"]}
```

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

This bridge decision does not accept parent-side Tau inputs, does not close the
certificate layer, does not derive `Phi_tau_eff`, does not compute a CMB score
or likelihood, and does not decide whether a dark sector is needed.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    rows = bridge_rows()
    row = summary(rows)
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_evidence_payload_intake_bridge_decision_v01.csv", rows, ROW_FIELDS)
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_evidence_payload_intake_bridge_decision_summary_v01.csv", [row], SUMMARY_FIELDS)
    write_json(DERIVED / "tau_cmb_phi_tau_parent_evidence_payload_intake_bridge_decision_v01.json", rows, row)
    write_doc(DOCS / "tau_cmb_phi_tau_parent_evidence_payload_intake_bridge_decision_v01.md", row)
    print("TAU_CMB_PHI_TAU_PARENT_EVIDENCE_PAYLOAD_INTAKE_BRIDGE_DECISION_V01_BUILT")


if __name__ == "__main__":
    main()
