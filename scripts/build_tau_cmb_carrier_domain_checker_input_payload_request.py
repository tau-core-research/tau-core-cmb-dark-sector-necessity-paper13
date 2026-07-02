#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXEC_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_packet_audit_v01.json"
EXEC_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_packet_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_request_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_request_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_input_payload_request_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_input_payload_request_v01_request_only_"
    "payloads_not_supplied_no_checker_execution_no_certificate_pass_no_domain_acceptance_"
    "no_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "request_row_id",
    "certificate_area",
    "checker_name",
    "requested_payload_files",
    "requested_replay_files",
    "requested_provenance_files",
    "requested_hash_files",
    "requested_firewall_files",
    "minimum_acceptance_condition",
    "current_request_status",
    "blocking_reason",
    "request_declared",
    "payload_supplied",
    "replay_supplied",
    "provenance_supplied",
    "hash_supplied",
    "firewall_supplied",
    "payload_accepted",
    "can_execute_after_fulfillment",
    "checker_executed",
    "certificate_passed",
    "domain_object_accepted",
    "allows_concrete_R_CMB",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

ROWS = [
    {
        "certificate_area": "carrier_well_formedness",
        "checker_name": "run_carrier_ok_checker",
        "requested_payload_files": "carrier_payload.json",
        "requested_replay_files": "role_space_basis_replay.json; role_bundle_replay.json",
        "requested_provenance_files": "carrier_provenance.json",
        "requested_hash_files": "carrier_payload.hashes.json",
        "requested_firewall_files": "carrier_endpoint_firewall_attestation.json",
        "minimum_acceptance_condition": "all requested carrier files are supplied, hash-checked, and endpoint-blind before can_execute may become true",
        "current_request_status": "INPUT_PAYLOAD_REQUEST_DECLARED_NOT_SUPPLIED",
        "blocking_reason": "carrier input payload bundle is absent",
    },
    {
        "certificate_area": "domain_membership_rule",
        "checker_name": "run_dom_ok_checker",
        "requested_payload_files": "domain_payload.json; support_record.json; normalization_record.json",
        "requested_replay_files": "domain_replay_trace.json",
        "requested_provenance_files": "domain_provenance.json",
        "requested_hash_files": "domain_payload.hashes.json",
        "requested_firewall_files": "domain_firewall_trace.json",
        "minimum_acceptance_condition": "support, normalization, payload, replay, provenance, hash, and firewall files are supplied and mutually consistent",
        "current_request_status": "INPUT_PAYLOAD_REQUEST_DECLARED_NOT_SUPPLIED",
        "blocking_reason": "joint domain input payload bundle is absent",
    },
    {
        "certificate_area": "seed_admissibility",
        "checker_name": "run_seed_admissibility_checker",
        "requested_payload_files": "seed_domain_payload.json; seed_descriptor_pass.json; activation_pass.json; quotient_survival_witness.json",
        "requested_replay_files": "seed_equivalence_replay.json; seed_activation_replay.json",
        "requested_provenance_files": "seed_domain_provenance.json",
        "requested_hash_files": "seed_domain_payload.hashes.json",
        "requested_firewall_files": "seed_endpoint_firewall_attestation.json",
        "minimum_acceptance_condition": "seed descriptor, activation, quotient witness, equivalence replay, provenance, hashes, and firewall are supplied",
        "current_request_status": "INPUT_PAYLOAD_REQUEST_DECLARED_NOT_SUPPLIED",
        "blocking_reason": "seed admissibility payload and quotient witness are absent",
    },
    {
        "certificate_area": "null_control_admissibility",
        "checker_name": "run_null_control_checker",
        "requested_payload_files": "null_control_payload.json; null_readout_candidate.json; no_response_proof_candidate.json",
        "requested_replay_files": "zero_control_replay.json; null_coordinate_replay.json; null_domain_replay.json",
        "requested_provenance_files": "null_control_provenance.json",
        "requested_hash_files": "null_control_payload.hashes.json",
        "requested_firewall_files": "null_control_firewall_attestation.json",
        "minimum_acceptance_condition": "zero-control, null-coordinate, same-domain, null-readout, no-response, and firewall payloads are supplied",
        "current_request_status": "INPUT_PAYLOAD_REQUEST_DECLARED_NOT_SUPPLIED",
        "blocking_reason": "null control payload and null readout materialization are absent",
    },
    {
        "certificate_area": "source_object_admissibility",
        "checker_name": "run_source_object_checker",
        "requested_payload_files": "source_object_payload.json; source_derivation_transcript.json; known_limit_check.json",
        "requested_replay_files": "source_dimension_gauge_replay.json; source_derivation_replay.json",
        "requested_provenance_files": "source_object_provenance.json",
        "requested_hash_files": "source_object_payload.hashes.json",
        "requested_firewall_files": "source_endpoint_firewall_trace.json",
        "minimum_acceptance_condition": "endpoint-blind source derivation, dimension/gauge replay, known-limit check, provenance, hashes, and firewall are supplied",
        "current_request_status": "INPUT_PAYLOAD_REQUEST_DECLARED_NOT_SUPPLIED",
        "blocking_reason": "endpoint-blind source object payload is absent",
    },
    {
        "certificate_area": "quotient_and_equivalence_survival",
        "checker_name": "run_quotient_survival_checker",
        "requested_payload_files": "quotient_payload.json; equivalence_relation.json; null_class.json; representative_family.json; non_null_witness.json",
        "requested_replay_files": "quotient_relation_replay.json; equivalence_axiom_replay.json",
        "requested_provenance_files": "quotient_provenance.json",
        "requested_hash_files": "quotient_payload.hashes.json",
        "requested_firewall_files": "quotient_firewall_attestation.json",
        "minimum_acceptance_condition": "equivalence relation, null class, representatives, non-null witness, replay, provenance, hashes, and firewall are supplied",
        "current_request_status": "INPUT_PAYLOAD_REQUEST_DECLARED_NOT_SUPPLIED",
        "blocking_reason": "non-null witness and representative-family payload are absent",
    },
    {
        "certificate_area": "codomain_compatibility",
        "checker_name": "run_codomain_ok_checker",
        "requested_payload_files": "codomain_payload.json; r_cmb_output_candidate.json; role_coordinate_basis.json; numeric_guard_records.json",
        "requested_replay_files": "dimension_sign_replay.json; role_coordinate_bundle_replay.json",
        "requested_provenance_files": "codomain_provenance.json",
        "requested_hash_files": "codomain_payload.hashes.json",
        "requested_firewall_files": "codomain_firewall_attestation.json",
        "minimum_acceptance_condition": "R_CMB output candidate, role basis, numeric guards, dimension/sign replay, provenance, hashes, and firewall are supplied",
        "current_request_status": "INPUT_PAYLOAD_REQUEST_DECLARED_NOT_SUPPLIED",
        "blocking_reason": "concrete R_CMB output candidate is absent",
    },
    {
        "certificate_area": "endpoint_firewall_replay",
        "checker_name": "run_endpoint_firewall_checker",
        "requested_payload_files": "firewall_payload.json; populated_records.json",
        "requested_replay_files": "post_population_firewall_replay.json",
        "requested_provenance_files": "provenance_log.json; endpoint_data_access_log.json; score_access_log.json",
        "requested_hash_files": "firewall_payload.hashes.json",
        "requested_firewall_files": "endpoint_firewall_attestation.json",
        "minimum_acceptance_condition": "populated records, provenance log, endpoint data log, score access log, hashes, and firewall attestation are supplied",
        "current_request_status": "INPUT_PAYLOAD_REQUEST_DECLARED_NOT_SUPPLIED",
        "blocking_reason": "populated values and endpoint access logs are absent",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def table_rows() -> list[dict[str, str]]:
    return [
        {
            "request_row_id": f"TCMBCDIPR01_{index:03d}",
            "request_declared": "true",
            "payload_supplied": "false",
            "replay_supplied": "false",
            "provenance_supplied": "false",
            "hash_supplied": "false",
            "firewall_supplied": "false",
            "payload_accepted": "false",
            "can_execute_after_fulfillment": "false",
            "checker_executed": "false",
            "certificate_passed": "false",
            "domain_object_accepted": "false",
            "allows_concrete_R_CMB": "false",
            "allows_score_entry": "false",
            "allows_likelihood": "false",
            "allows_dark_sector_verdict": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            **row,
        }
        for index, row in enumerate(ROWS, start=1)
    ]


def write_table(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_summary(table_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    audit = load_json(EXEC_AUDIT) if EXEC_AUDIT.exists() else {}
    input_ok = (
        audit.get("status") == "CARRIER_DOMAIN_CHECKER_EXECUTION_PACKET_AUDITED_BLOCKED_NOT_EXECUTABLE"
        and audit.get("failed_rows") == 0
        and EXEC_TABLE.exists()
    )
    return {
        "report_id": "tau_cmb_carrier_domain_checker_input_payload_request_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_execution_audit": rel(EXEC_AUDIT),
        "input_execution_table": rel(EXEC_TABLE),
        "input_chain_clean": input_ok,
        "request_rows": len(rows),
        "requests_declared": sum(row["request_declared"] == "true" for row in rows),
        "payload_supplied_rows": sum(row["payload_supplied"] == "true" for row in rows),
        "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
        "can_execute_after_fulfillment_rows": sum(row["can_execute_after_fulfillment"] == "true" for row in rows),
        "checker_executed_rows": sum(row["checker_executed"] == "true" for row in rows),
        "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
        "accepted_domain_objects": sum(row["domain_object_accepted"] == "true" for row in rows),
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_REQUEST_DECLARED_NOT_FULFILLED"
            if input_ok
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_REQUEST_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "audit_tau_cmb_carrier_domain_checker_input_payload_request_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        (
            f"- `{row['certificate_area']}`: {row['current_request_status']} | "
            f"`{row['checker_name']}` | request: {row['requested_payload_files']} | "
            f"blocks: {row['blocking_reason']}"
        )
        for row in rows
    )
    text = f"""# Tau CMB Carrier Domain Checker Input Payload Request v01

**Doc class:** carrier/domain checker input payload request
**Reader role:** Paper 13 / CMB readout route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact requests the concrete input payloads required before the
carrier/domain checkers can become executable. It does not supply or accept
payloads, execute checkers, pass certificates, accept domain objects,
materialize `R_CMB`, open score entry, compute a likelihood, or decide the
dark-sector question.

## Request Rows

{row_text}

## Status

```text
{summary["status"]}
```

The route now has a concrete payload request list, but all fulfillment,
acceptance, execution, pass, and scoring flags remain false.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB carrier/domain checker input payload request.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = table_rows()
    table_path = Path(args.write_table or DEFAULT_TABLE)
    if args.write_table:
        write_table(table_path, rows)
    summary = build_summary(table_path, rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), rows, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
