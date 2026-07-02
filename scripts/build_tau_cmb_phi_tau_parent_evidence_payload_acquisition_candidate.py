#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

PACKET_ID = "TAU_CMB_PHI_TAU_PARENT_EVIDENCE_PAYLOAD_ACQUISITION_CANDIDATE_V01"
CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_evidence_payload_acquisition_candidate_v01_payload_candidate_only_"
    "semantic_replay_sources_hash_bound_not_parent_input_accepted_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

ROW_FIELDS = [
    "payload_row_id",
    "certificate_component",
    "target_payload_component",
    "payload_role",
    "candidate_source_kind",
    "candidate_source_artifact",
    "candidate_source_sha256",
    "source_artifact_present",
    "hash_bound",
    "endpoint_blind_candidate",
    "semantic_replay_candidate",
    "candidate_payload_supplied",
    "dimension_payload_supplied",
    "replay_payload_supplied",
    "firewall_payload_supplied",
    "certificate_pass_candidate",
    "certificate_passed",
    "parent_payload_accepted",
    "score_entry_allowed",
    "blocking_reason",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "payload_candidate_rows_declared",
    "source_artifact_present_rows",
    "hash_bound_rows",
    "endpoint_blind_candidate_rows",
    "semantic_replay_candidate_rows",
    "candidate_payload_supplied_rows",
    "dimension_payload_supplied_rows",
    "replay_payload_supplied_rows",
    "firewall_payload_supplied_rows",
    "certificate_pass_candidate_rows",
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


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def source_rows() -> list[tuple[str, str, str, str, str]]:
    return [
        (
            "certificate_candidate_manifest_identity",
            "all_parent_payload_rows",
            "package manifest candidate with certificate-level replay supply table",
            "certificate_level_replay_supply_table",
            "data/derived/tau_cmb_certificate_semantic_evidence_certificate_level_checker_replay_supply_v01.csv",
        ),
        (
            "base_field_dimension_replay_certificate_candidate",
            "base_field_state_payload_candidate",
            "base/carrier semantic checker replay candidate",
            "certificate_level_checker_replay_json",
            "semantic_evidence_certificate_level_checker_replays/carrier_well_formedness/run_carrier_ok_checker_certificate_level_replay_v01.json",
        ),
        (
            "seed_dimension_replay_certificate_candidate",
            "morphological_seed_payload_candidate",
            "seed semantic checker replay candidate",
            "certificate_level_checker_replay_json",
            "semantic_evidence_certificate_level_checker_replays/seed_admissibility/run_seed_admissibility_checker_certificate_level_replay_v01.json",
        ),
        (
            "operator_dimension_replay_certificate_candidate",
            "response_operator_payload_candidate",
            "source/operator semantic checker replay candidate",
            "certificate_level_checker_replay_json",
            "semantic_evidence_certificate_level_checker_replays/source_object_admissibility/run_source_object_checker_certificate_level_replay_v01.json",
        ),
        (
            "gauge_normalization_replay_certificate_candidate",
            "gauge_normalization_payload_candidate",
            "domain membership and normalization semantic checker replay candidate",
            "certificate_level_checker_replay_json",
            "semantic_evidence_certificate_level_checker_replays/domain_membership_rule/run_dom_ok_checker_certificate_level_replay_v01.json",
        ),
        (
            "payload_firewall_certificate_candidate",
            "endpoint_firewall_payload_candidate",
            "endpoint firewall semantic checker replay candidate",
            "certificate_level_checker_replay_json",
            "semantic_evidence_certificate_level_checker_replays/endpoint_firewall_replay/run_endpoint_firewall_checker_certificate_level_replay_v01.json",
        ),
        (
            "executable_replay_certificate_candidate",
            "provenance_replay_payload_candidate",
            "checker execution replay supply table",
            "checker_execution_replay_supply_table",
            "data/derived/tau_cmb_certificate_semantic_evidence_checker_execution_replay_supply_v01.csv",
        ),
    ]


def rows() -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for index, (component, target, role, kind, source) in enumerate(source_rows(), start=1):
        path = ROOT / source
        present = path.exists()
        digest = sha256(path) if present else ""
        dimension = component in {
            "base_field_dimension_replay_certificate_candidate",
            "seed_dimension_replay_certificate_candidate",
            "operator_dimension_replay_certificate_candidate",
            "gauge_normalization_replay_certificate_candidate",
        }
        replay = component != "payload_firewall_certificate_candidate"
        firewall = component in {
            "payload_firewall_certificate_candidate",
            "certificate_candidate_manifest_identity",
            "executable_replay_certificate_candidate",
        }
        output.append(
            {
                "payload_row_id": f"TCMBPTPEPAC01_{index:03d}",
                "certificate_component": component,
                "target_payload_component": target,
                "payload_role": role,
                "candidate_source_kind": kind,
                "candidate_source_artifact": source,
                "candidate_source_sha256": digest,
                "source_artifact_present": str(present).lower(),
                "hash_bound": str(bool(digest)).lower(),
                "endpoint_blind_candidate": "true" if present else "false",
                "semantic_replay_candidate": "true" if present else "false",
                "candidate_payload_supplied": "true" if present else "false",
                "dimension_payload_supplied": str(dimension and present).lower(),
                "replay_payload_supplied": str(replay and present).lower(),
                "firewall_payload_supplied": str(firewall and present).lower(),
                "certificate_pass_candidate": "true" if present else "false",
                "certificate_passed": "false",
                "parent_payload_accepted": "false",
                "score_entry_allowed": "false",
                "blocking_reason": (
                    "hash-bound semantic replay candidate is acquired, but parent-input acceptance still requires package audit and certificate pass"
                    if present
                    else "source artifact missing"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def summary(rows: list[dict[str, str]]) -> dict[str, str]:
    return {
        "summary_id": PACKET_ID,
        "payload_candidate_rows_declared": str(len(rows)),
        "source_artifact_present_rows": str(sum(row["source_artifact_present"] == "true" for row in rows)),
        "hash_bound_rows": str(sum(row["hash_bound"] == "true" for row in rows)),
        "endpoint_blind_candidate_rows": str(sum(row["endpoint_blind_candidate"] == "true" for row in rows)),
        "semantic_replay_candidate_rows": str(sum(row["semantic_replay_candidate"] == "true" for row in rows)),
        "candidate_payload_supplied_rows": str(sum(row["candidate_payload_supplied"] == "true" for row in rows)),
        "dimension_payload_supplied_rows": str(sum(row["dimension_payload_supplied"] == "true" for row in rows)),
        "replay_payload_supplied_rows": str(sum(row["replay_payload_supplied"] == "true" for row in rows)),
        "firewall_payload_supplied_rows": str(sum(row["firewall_payload_supplied"] == "true" for row in rows)),
        "certificate_pass_candidate_rows": str(sum(row["certificate_pass_candidate"] == "true" for row in rows)),
        "certificate_passed_rows": str(sum(row["certificate_passed"] == "true" for row in rows)),
        "parent_payload_accepted_rows": str(sum(row["parent_payload_accepted"] == "true" for row in rows)),
        "score_ready_rows": str(sum(row["score_entry_allowed"] == "true" for row in rows)),
        "scores_computed": "false",
        "cmb_likelihood_available": "false",
        "tau_response_claim_allowed": "false",
        "dark_sector_verdict_allowed": "false",
        "overall_status": "PHI_TAU_PARENT_EVIDENCE_PAYLOAD_CANDIDATES_ACQUIRED_NOT_ACCEPTED",
        "next_required_artifact": "tau_cmb_phi_tau_parent_evidence_payload_acquisition_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_json(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "phi_tau_parent_evidence_payload_acquisition_candidate",
        "status": row["overall_status"],
        "claim_boundary": CLAIM_BOUNDARY,
        "payload_rows": rows,
        "summary": row,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_doc(path: Path, row: dict[str, str]) -> None:
    text = f"""# Tau CMB Phi Tau Parent Evidence Payload Acquisition Candidate v01

**Doc class:** parent evidence-payload acquisition candidate
**Reader role:** Paper 13 CMB scoring path
**Status:** hash-bound semantic replay payload candidates acquired; not accepted as parent input
**Canonical parent:** Paper 13 CMB scoring input fulfillment chain

## Purpose

This artifact acquires concrete, endpoint-blind candidate payload sources for
the seven Phi Tau parent evidence-package rows. The sources are existing
semantic certificate replay artifacts and replay-supply tables. They are
payload candidates only: the acquisition does not by itself pass the parent
certificate layer.

## Summary

```text
payload_candidate_rows_declared={row["payload_candidate_rows_declared"]}
source_artifact_present_rows={row["source_artifact_present_rows"]}
hash_bound_rows={row["hash_bound_rows"]}
endpoint_blind_candidate_rows={row["endpoint_blind_candidate_rows"]}
semantic_replay_candidate_rows={row["semantic_replay_candidate_rows"]}
candidate_payload_supplied_rows={row["candidate_payload_supplied_rows"]}
dimension_payload_supplied_rows={row["dimension_payload_supplied_rows"]}
replay_payload_supplied_rows={row["replay_payload_supplied_rows"]}
firewall_payload_supplied_rows={row["firewall_payload_supplied_rows"]}
certificate_pass_candidate_rows={row["certificate_pass_candidate_rows"]}
certificate_passed_rows={row["certificate_passed_rows"]}
parent_payload_accepted_rows={row["parent_payload_accepted_rows"]}
score_ready_rows={row["score_ready_rows"]}
```

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

This artifact supplies candidate payload source references and hashes only. It
does not accept parent-side Tau inputs, does not close the certificate layer,
does not derive `Phi_tau_eff`, does not compute a CMB score or likelihood, and
does not decide whether a dark sector is needed.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    payload_rows = rows()
    row = summary(payload_rows)
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_evidence_payload_acquisition_candidate_v01.csv", payload_rows, ROW_FIELDS)
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_evidence_payload_acquisition_candidate_summary_v01.csv", [row], SUMMARY_FIELDS)
    write_json(DERIVED / "tau_cmb_phi_tau_parent_evidence_payload_acquisition_candidate_v01.json", payload_rows, row)
    write_doc(DOCS / "tau_cmb_phi_tau_parent_evidence_payload_acquisition_candidate_v01.md", row)
    print("TAU_CMB_PHI_TAU_PARENT_EVIDENCE_PAYLOAD_ACQUISITION_CANDIDATE_V01_BUILT")


if __name__ == "__main__":
    main()
