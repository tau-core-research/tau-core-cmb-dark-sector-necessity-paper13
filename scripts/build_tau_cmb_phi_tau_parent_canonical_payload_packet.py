#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

SOURCE_TABLE = DERIVED / "tau_cmb_phi_tau_parent_evidence_payload_acquisition_candidate_v01.csv"

PACKET_ID = "TAU_CMB_PHI_TAU_PARENT_CANONICAL_PAYLOAD_PACKET_V01"
CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_canonical_payload_packet_v01_packet_materialization_only_"
    "candidate_payloads_repackaged_no_parent_acceptance_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

ROW_FIELDS = [
    "packet_row_id",
    "payload_row_id",
    "certificate_component",
    "target_payload_component",
    "canonical_packet_id",
    "source_artifact",
    "source_sha256",
    "canonical_packet_present",
    "receipt_binding_present",
    "dimension_binding_present",
    "replay_binding_present",
    "firewall_binding_present",
    "canonical_repackaging_completed",
    "binding_triads_complete",
    "parent_acceptance_ready",
    "parent_payload_accepted",
    "certificate_passed",
    "score_entry_allowed",
    "remaining_blocker",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "packet_rows_declared",
    "canonical_packet_present_rows",
    "receipt_binding_present_rows",
    "dimension_binding_present_rows",
    "replay_binding_present_rows",
    "firewall_binding_present_rows",
    "canonical_repackaging_completed_rows",
    "binding_triads_complete_rows",
    "parent_acceptance_ready_rows",
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


def packet_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(SOURCE_TABLE), start=1):
        dimension = source["dimension_payload_supplied"] == "true"
        replay = source["replay_payload_supplied"] == "true"
        firewall = source["firewall_payload_supplied"] == "true"
        triad = dimension and replay and firewall
        rows.append(
            {
                "packet_row_id": f"TCMBPTPCPP01_{index:03d}",
                "payload_row_id": source["payload_row_id"],
                "certificate_component": source["certificate_component"],
                "target_payload_component": source["target_payload_component"],
                "canonical_packet_id": f"phi_tau_parent_canonical_payload_packet_{index:03d}_v01",
                "source_artifact": source["candidate_source_artifact"],
                "source_sha256": source["candidate_source_sha256"],
                "canonical_packet_present": "true",
                "receipt_binding_present": "true",
                "dimension_binding_present": str(dimension).lower(),
                "replay_binding_present": str(replay).lower(),
                "firewall_binding_present": str(firewall).lower(),
                "canonical_repackaging_completed": "true",
                "binding_triads_complete": str(triad).lower(),
                "parent_acceptance_ready": "false",
                "parent_payload_accepted": "false",
                "certificate_passed": "false",
                "score_entry_allowed": "false",
                "remaining_blocker": (
                    "canonical packet exists, but parent acceptance still requires complete required binding set and certificate pass"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, str]]) -> dict[str, str]:
    return {
        "summary_id": PACKET_ID,
        "packet_rows_declared": str(len(rows)),
        "canonical_packet_present_rows": str(sum(row["canonical_packet_present"] == "true" for row in rows)),
        "receipt_binding_present_rows": str(sum(row["receipt_binding_present"] == "true" for row in rows)),
        "dimension_binding_present_rows": str(sum(row["dimension_binding_present"] == "true" for row in rows)),
        "replay_binding_present_rows": str(sum(row["replay_binding_present"] == "true" for row in rows)),
        "firewall_binding_present_rows": str(sum(row["firewall_binding_present"] == "true" for row in rows)),
        "canonical_repackaging_completed_rows": str(sum(row["canonical_repackaging_completed"] == "true" for row in rows)),
        "binding_triads_complete_rows": str(sum(row["binding_triads_complete"] == "true" for row in rows)),
        "parent_acceptance_ready_rows": str(sum(row["parent_acceptance_ready"] == "true" for row in rows)),
        "parent_payload_accepted_rows": str(sum(row["parent_payload_accepted"] == "true" for row in rows)),
        "certificate_passed_rows": str(sum(row["certificate_passed"] == "true" for row in rows)),
        "score_ready_rows": str(sum(row["score_entry_allowed"] == "true" for row in rows)),
        "scores_computed": "false",
        "cmb_likelihood_available": "false",
        "tau_response_claim_allowed": "false",
        "dark_sector_verdict_allowed": "false",
        "overall_status": "PHI_TAU_PARENT_CANONICAL_PAYLOAD_PACKETS_MATERIALIZED_NOT_ACCEPTED",
        "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_submission_gate_v01",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_json(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "phi_tau_parent_canonical_payload_packet",
        "status": row["overall_status"],
        "claim_boundary": CLAIM_BOUNDARY,
        "packet_rows": rows,
        "summary": row,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_doc(path: Path, row: dict[str, str]) -> None:
    text = f"""# Tau CMB Phi Tau Parent Canonical Payload Packet v01

**Doc class:** parent canonical payload packet materialization
**Reader role:** Paper 13 CMB scoring path
**Status:** candidate payloads repackaged as canonical packets; not accepted as parent inputs
**Canonical parent:** Paper 13 CMB scoring input fulfillment chain

## Purpose

This artifact turns the acquired hash-bound candidate payloads into canonical
parent payload packet rows. It closes the repackaging gap but does not close the
acceptance gap: the packet rows still need the required binding coverage and a
certificate pass before any parent input can enter scoring.

## Summary

```text
packet_rows_declared={row["packet_rows_declared"]}
canonical_packet_present_rows={row["canonical_packet_present_rows"]}
receipt_binding_present_rows={row["receipt_binding_present_rows"]}
dimension_binding_present_rows={row["dimension_binding_present_rows"]}
replay_binding_present_rows={row["replay_binding_present_rows"]}
firewall_binding_present_rows={row["firewall_binding_present_rows"]}
canonical_repackaging_completed_rows={row["canonical_repackaging_completed_rows"]}
binding_triads_complete_rows={row["binding_triads_complete_rows"]}
parent_acceptance_ready_rows={row["parent_acceptance_ready_rows"]}
parent_payload_accepted_rows={row["parent_payload_accepted_rows"]}
certificate_passed_rows={row["certificate_passed_rows"]}
score_ready_rows={row["score_ready_rows"]}
```

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

This packet artifact does not accept parent-side Tau inputs, does not close the
certificate layer, does not derive `Phi_tau_eff`, does not compute a CMB score
or likelihood, and does not decide whether a dark sector is needed.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    rows = packet_rows()
    row = summary(rows)
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_canonical_payload_packet_v01.csv", rows, ROW_FIELDS)
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_canonical_payload_packet_summary_v01.csv", [row], SUMMARY_FIELDS)
    write_json(DERIVED / "tau_cmb_phi_tau_parent_canonical_payload_packet_v01.json", rows, row)
    write_doc(DOCS / "tau_cmb_phi_tau_parent_canonical_payload_packet_v01.md", row)
    print("TAU_CMB_PHI_TAU_PARENT_CANONICAL_PAYLOAD_PACKET_V01_BUILT")


if __name__ == "__main__":
    main()
