#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

SOURCE_TABLE = DERIVED / "tau_cmb_phi_tau_parent_evidence_payload_acquisition_candidate_v01.csv"
SOURCE_SUMMARY = DERIVED / "tau_cmb_phi_tau_parent_evidence_payload_acquisition_candidate_summary_v01.csv"

PACKET_ID = "TAU_CMB_PHI_TAU_PARENT_EVIDENCE_PAYLOAD_ACQUISITION_AUDIT_V01"
CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_evidence_payload_acquisition_audit_v01_audit_only_"
    "payload_candidates_present_hash_bound_but_not_parent_accepted_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

ROW_FIELDS = [
    "audit_row_id",
    "payload_row_id",
    "certificate_component",
    "audit_status",
    "source_artifact_present",
    "hash_bound",
    "endpoint_blind_candidate",
    "semantic_replay_candidate",
    "candidate_payload_supplied",
    "candidate_payload_audit_passed",
    "parent_acceptance_decision",
    "certificate_passed",
    "parent_payload_accepted",
    "score_entry_allowed",
    "remaining_blocker",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "audit_rows_declared",
    "source_artifact_present_rows",
    "hash_bound_rows",
    "endpoint_blind_candidate_rows",
    "semantic_replay_candidate_rows",
    "candidate_payload_supplied_rows",
    "candidate_payload_audit_passed_rows",
    "certificate_passed_rows",
    "parent_payload_accepted_rows",
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


def audit_rows() -> list[dict[str, str]]:
    source_rows = read_csv(SOURCE_TABLE)
    rows: list[dict[str, str]] = []
    for index, source in enumerate(source_rows, start=1):
        candidate_ok = (
            source["source_artifact_present"] == "true"
            and source["hash_bound"] == "true"
            and source["endpoint_blind_candidate"] == "true"
            and source["semantic_replay_candidate"] == "true"
            and source["candidate_payload_supplied"] == "true"
        )
        rows.append(
            {
                "audit_row_id": f"TCMBPTPEPAA01_{index:03d}",
                "payload_row_id": source["payload_row_id"],
                "certificate_component": source["certificate_component"],
                "audit_status": (
                    "PAYLOAD_CANDIDATE_AUDIT_PASS_NOT_PARENT_ACCEPTED"
                    if candidate_ok
                    else "PAYLOAD_CANDIDATE_AUDIT_FAIL_SOURCE_INCOMPLETE"
                ),
                "source_artifact_present": source["source_artifact_present"],
                "hash_bound": source["hash_bound"],
                "endpoint_blind_candidate": source["endpoint_blind_candidate"],
                "semantic_replay_candidate": source["semantic_replay_candidate"],
                "candidate_payload_supplied": source["candidate_payload_supplied"],
                "candidate_payload_audit_passed": str(candidate_ok).lower(),
                "parent_acceptance_decision": "reject_for_parent_acceptance_until_certificate_pass",
                "certificate_passed": "false",
                "parent_payload_accepted": "false",
                "score_entry_allowed": "false",
                "remaining_blocker": "candidate payload must be promoted through parent evidence-package acceptance and certificate pass before scoring",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, str]]) -> dict[str, str]:
    return {
        "summary_id": PACKET_ID,
        "audit_rows_declared": str(len(rows)),
        "source_artifact_present_rows": str(sum(row["source_artifact_present"] == "true" for row in rows)),
        "hash_bound_rows": str(sum(row["hash_bound"] == "true" for row in rows)),
        "endpoint_blind_candidate_rows": str(sum(row["endpoint_blind_candidate"] == "true" for row in rows)),
        "semantic_replay_candidate_rows": str(sum(row["semantic_replay_candidate"] == "true" for row in rows)),
        "candidate_payload_supplied_rows": str(sum(row["candidate_payload_supplied"] == "true" for row in rows)),
        "candidate_payload_audit_passed_rows": str(sum(row["candidate_payload_audit_passed"] == "true" for row in rows)),
        "certificate_passed_rows": str(sum(row["certificate_passed"] == "true" for row in rows)),
        "parent_payload_accepted_rows": str(sum(row["parent_payload_accepted"] == "true" for row in rows)),
        "score_ready_rows": str(sum(row["score_entry_allowed"] == "true" for row in rows)),
        "scores_computed": "false",
        "cmb_likelihood_available": "false",
        "tau_response_claim_allowed": "false",
        "dark_sector_verdict_allowed": "false",
        "overall_status": "PHI_TAU_PARENT_EVIDENCE_PAYLOAD_CANDIDATES_AUDITED_PRESENT_BUT_NOT_ACCEPTED",
        "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_v01",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_json(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "phi_tau_parent_evidence_payload_acquisition_audit",
        "status": row["overall_status"],
        "claim_boundary": CLAIM_BOUNDARY,
        "audit_rows": rows,
        "summary": row,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_doc(path: Path, row: dict[str, str]) -> None:
    text = f"""# Tau CMB Phi Tau Parent Evidence Payload Acquisition Audit v01

**Doc class:** parent evidence-payload acquisition audit
**Reader role:** Paper 13 CMB scoring path
**Status:** candidate payloads are present and hash-bound, but not accepted as parent inputs
**Canonical parent:** Paper 13 CMB scoring input fulfillment chain

## Purpose

This artifact audits the payload acquisition candidate. It distinguishes a real
candidate payload source from an accepted parent input: the former is now
present and hash-bound; the latter still requires parent package acceptance and
certificate pass.

## Summary

```text
audit_rows_declared={row["audit_rows_declared"]}
source_artifact_present_rows={row["source_artifact_present_rows"]}
hash_bound_rows={row["hash_bound_rows"]}
candidate_payload_supplied_rows={row["candidate_payload_supplied_rows"]}
candidate_payload_audit_passed_rows={row["candidate_payload_audit_passed_rows"]}
certificate_passed_rows={row["certificate_passed_rows"]}
parent_payload_accepted_rows={row["parent_payload_accepted_rows"]}
score_ready_rows={row["score_ready_rows"]}
```

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

The audit does not accept parent-side Tau inputs, does not close the certificate
layer, does not derive `Phi_tau_eff`, does not compute a CMB score or
likelihood, and does not decide whether a dark sector is needed.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    rows = audit_rows()
    row = summary(rows)
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_evidence_payload_acquisition_audit_v01.csv", rows, ROW_FIELDS)
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_evidence_payload_acquisition_audit_summary_v01.csv", [row], SUMMARY_FIELDS)
    write_json(DERIVED / "tau_cmb_phi_tau_parent_evidence_payload_acquisition_audit_v01.json", rows, row)
    write_doc(DOCS / "tau_cmb_phi_tau_parent_evidence_payload_acquisition_audit_v01.md", row)
    print("TAU_CMB_PHI_TAU_PARENT_EVIDENCE_PAYLOAD_ACQUISITION_AUDIT_V01_BUILT")


if __name__ == "__main__":
    main()
