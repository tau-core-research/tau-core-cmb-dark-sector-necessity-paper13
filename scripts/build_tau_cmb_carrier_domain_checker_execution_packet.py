#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_proof_checker_payload_packet_audit_v01.json"
PAYLOAD_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_proof_checker_payload_packet_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_packet_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_packet_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_execution_packet_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_execution_packet_v01_execution_envelope_only_"
    "can_execute_false_no_checker_attempt_no_certificate_pass_no_domain_acceptance_"
    "no_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "execution_row_id",
    "certificate_area",
    "target_candidate_object",
    "checker_name",
    "execution_command_template",
    "execution_prerequisite_rule",
    "required_input_artifacts",
    "required_output_artifacts",
    "expected_pass_condition",
    "current_execution_status",
    "blocking_reason",
    "execution_packet_declared",
    "can_execute",
    "execution_attempted",
    "execution_succeeded",
    "checker_output_supplied",
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
        "target_candidate_object": "CarrierOK_candidate(x)",
        "checker_name": "run_carrier_ok_checker",
        "execution_command_template": "BLOCKED_UNTIL_PAYLOAD_POPULATED run_carrier_ok_checker --input carrier_payload.json --output carrier_ok_result.json",
        "execution_prerequisite_rule": "may execute only after carrier checker input payload, role-basis replay, bundle replay, and endpoint provenance are supplied",
        "required_input_artifacts": "carrier_payload.json; role_space_basis_replay.json; role_bundle_replay.json; carrier_provenance.json",
        "required_output_artifacts": "carrier_ok_result.json; carrier_ok_failures.json; carrier_ok_hashes.json",
        "expected_pass_condition": "all CarrierOK subchecks pass with no endpoint-fitted coordinate use",
        "current_execution_status": "EXECUTION_PACKET_DECLARED_BLOCKED_INPUTS_ABSENT",
        "blocking_reason": "carrier checker input payload and replay artifacts are absent",
    },
    {
        "certificate_area": "domain_membership_rule",
        "target_candidate_object": "DomOK_candidate(x)",
        "checker_name": "run_dom_ok_checker",
        "execution_command_template": "BLOCKED_UNTIL_PAYLOAD_POPULATED run_dom_ok_checker --input domain_payload.json --output dom_ok_result.json",
        "execution_prerequisite_rule": "may execute only after support, normalization, payload, replay, and firewall records are supplied",
        "required_input_artifacts": "domain_payload.json; support_record.json; normalization_record.json; replay_trace.json; firewall_trace.json",
        "required_output_artifacts": "dom_ok_result.json; dom_component_status.json; dom_ok_hashes.json",
        "expected_pass_condition": "ParentSideCMBObject, SupportOK, NormalizationOK, PayloadOK, ReplayOK, and FirewallOK all pass",
        "current_execution_status": "EXECUTION_PACKET_DECLARED_BLOCKED_INPUTS_ABSENT",
        "blocking_reason": "joint domain checker inputs are absent",
    },
    {
        "certificate_area": "seed_admissibility",
        "target_candidate_object": "SeedInDomain_candidate(seed_tau_CMB)",
        "checker_name": "run_seed_admissibility_checker",
        "execution_command_template": "BLOCKED_UNTIL_PAYLOAD_POPULATED run_seed_admissibility_checker --input seed_domain_payload.json --output seed_domain_result.json",
        "execution_prerequisite_rule": "may execute only after seed descriptor, activation, quotient survival, equivalence replay, and firewall records are supplied",
        "required_input_artifacts": "seed_domain_payload.json; seed_descriptor_pass.json; activation_pass.json; quotient_survival_witness.json; equivalence_replay.json",
        "required_output_artifacts": "seed_domain_result.json; seed_domain_failures.json; seed_domain_hashes.json",
        "expected_pass_condition": "descriptor, activation, quotient survival, equivalence replay, and firewall all pass",
        "current_execution_status": "EXECUTION_PACKET_DECLARED_BLOCKED_INPUTS_ABSENT",
        "blocking_reason": "seed pass records and quotient witness are absent",
    },
    {
        "certificate_area": "null_control_admissibility",
        "target_candidate_object": "NullControlInDomain_candidate(null_seed_tau_CMB)",
        "checker_name": "run_null_control_checker",
        "execution_command_template": "BLOCKED_UNTIL_PAYLOAD_POPULATED run_null_control_checker --input null_control_payload.json --output null_control_result.json",
        "execution_prerequisite_rule": "may execute only after zero-control replay, null-coordinate replay, domain convention, and null-readout candidate are supplied",
        "required_input_artifacts": "null_control_payload.json; zero_control_replay.json; null_coordinate_replay.json; null_readout_candidate.json",
        "required_output_artifacts": "null_control_result.json; null_no_response_result.json; null_control_hashes.json",
        "expected_pass_condition": "same-domain convention, null-readout mapping, and no-response proof all pass",
        "current_execution_status": "EXECUTION_PACKET_DECLARED_BLOCKED_INPUTS_ABSENT",
        "blocking_reason": "null readout materialization and no-response proof are absent",
    },
    {
        "certificate_area": "source_object_admissibility",
        "target_candidate_object": "SourceObjectInDomain_candidate(source_tau_CMB)",
        "checker_name": "run_source_object_checker",
        "execution_command_template": "BLOCKED_UNTIL_PAYLOAD_POPULATED run_source_object_checker --input source_object_payload.json --output source_object_result.json",
        "execution_prerequisite_rule": "may execute only after endpoint-blind source derivation, dimension/gauge replay, known-limit check, and firewall trace are supplied",
        "required_input_artifacts": "source_object_payload.json; derivation_transcript.json; dimension_gauge_replay.json; known_limit_check.json; source_firewall_trace.json",
        "required_output_artifacts": "source_object_result.json; source_object_failures.json; source_object_hashes.json",
        "expected_pass_condition": "endpoint-blind derivation, dimension/gauge, known-limit, and firewall checks all pass",
        "current_execution_status": "EXECUTION_PACKET_DECLARED_BLOCKED_INPUTS_ABSENT",
        "blocking_reason": "endpoint-blind source proof transcript is absent",
    },
    {
        "certificate_area": "quotient_and_equivalence_survival",
        "target_candidate_object": "QuotientSurvival_candidate([x])",
        "checker_name": "run_quotient_survival_checker",
        "execution_command_template": "BLOCKED_UNTIL_PAYLOAD_POPULATED run_quotient_survival_checker --input quotient_payload.json --output quotient_result.json",
        "execution_prerequisite_rule": "may execute only after equivalence relation, null class, representative family, and non-null witness are supplied",
        "required_input_artifacts": "quotient_payload.json; equivalence_relation.json; null_class.json; representative_family.json; non_null_witness.json",
        "required_output_artifacts": "quotient_result.json; representative_independence_result.json; quotient_hashes.json",
        "expected_pass_condition": "non-null survival and representative independence both pass",
        "current_execution_status": "EXECUTION_PACKET_DECLARED_BLOCKED_INPUTS_ABSENT",
        "blocking_reason": "non-null witness and representative-independence proof are absent",
    },
    {
        "certificate_area": "codomain_compatibility",
        "target_candidate_object": "CodomainOK_candidate(R_CMB(x))",
        "checker_name": "run_codomain_ok_checker",
        "execution_command_template": "BLOCKED_UNTIL_R_CMB_OUTPUT_EXISTS run_codomain_ok_checker --input codomain_payload.json --output codomain_result.json",
        "execution_prerequisite_rule": "may execute only after a concrete R_CMB output candidate and role-coordinate metadata are supplied",
        "required_input_artifacts": "codomain_payload.json; r_cmb_output_candidate.json; role_coordinate_basis.json; dimension_sign_metadata.json; numeric_guard_records.json",
        "required_output_artifacts": "codomain_result.json; role_typing_result.json; codomain_hashes.json",
        "expected_pass_condition": "role typing, unit/sign replay, and numeric guards all pass",
        "current_execution_status": "EXECUTION_PACKET_DECLARED_BLOCKED_NO_R_CMB_OUTPUT",
        "blocking_reason": "no concrete R_CMB output exists to check",
    },
    {
        "certificate_area": "endpoint_firewall_replay",
        "target_candidate_object": "EndpointBlindCarrierDomain_candidate",
        "checker_name": "run_endpoint_firewall_checker",
        "execution_command_template": "BLOCKED_UNTIL_VALUES_POPULATED run_endpoint_firewall_checker --input firewall_payload.json --output firewall_result.json",
        "execution_prerequisite_rule": "may execute only after populated carrier/domain/codomain records and endpoint access logs are supplied",
        "required_input_artifacts": "firewall_payload.json; populated_records.json; provenance_log.json; endpoint_data_access_log.json; score_access_log.json",
        "required_output_artifacts": "firewall_result.json; provenance_lock_result.json; firewall_hashes.json",
        "expected_pass_condition": "no residual use, no score use, no likelihood-delta use, and provenance lock all pass",
        "current_execution_status": "EXECUTION_PACKET_DECLARED_BLOCKED_VALUES_ABSENT",
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
            "execution_row_id": f"TCMBCDCEP01_{index:03d}",
            "execution_packet_declared": "true",
            "can_execute": "false",
            "execution_attempted": "false",
            "execution_succeeded": "false",
            "checker_output_supplied": "false",
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
    audit = load_json(PAYLOAD_AUDIT) if PAYLOAD_AUDIT.exists() else {}
    input_ok = (
        audit.get("status") == "CARRIER_DOMAIN_PROOF_CHECKER_PAYLOAD_PACKET_AUDITED_NOT_EXECUTED_NOT_SCORE_READY"
        and audit.get("failed_rows") == 0
        and PAYLOAD_TABLE.exists()
    )
    return {
        "report_id": "tau_cmb_carrier_domain_checker_execution_packet_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_payload_audit": rel(PAYLOAD_AUDIT),
        "input_payload_table": rel(PAYLOAD_TABLE),
        "input_chain_clean": input_ok,
        "execution_rows": len(rows),
        "execution_packet_declared_rows": sum(row["execution_packet_declared"] == "true" for row in rows),
        "can_execute_rows": sum(row["can_execute"] == "true" for row in rows),
        "execution_attempted_rows": sum(row["execution_attempted"] == "true" for row in rows),
        "execution_succeeded_rows": sum(row["execution_succeeded"] == "true" for row in rows),
        "checker_output_supplied_rows": sum(row["checker_output_supplied"] == "true" for row in rows),
        "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
        "accepted_domain_objects": sum(row["domain_object_accepted"] == "true" for row in rows),
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CHECKER_EXECUTION_PACKET_DECLARED_BLOCKED_NOT_EXECUTED"
            if input_ok
            else "CARRIER_DOMAIN_CHECKER_EXECUTION_PACKET_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "audit_tau_cmb_carrier_domain_checker_execution_packet_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        (
            f"- `{row['certificate_area']}`: {row['current_execution_status']} | "
            f"`{row['checker_name']}` | blocks: {row['blocking_reason']}"
        )
        for row in rows
    )
    text = f"""# Tau CMB Carrier Domain Checker Execution Packet v01

**Doc class:** carrier/domain checker execution packet
**Reader role:** Paper 13 / CMB readout route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact declares the execution envelope for the carrier/domain
proof-checkers. It does not execute any checker, pass certificates, accept
domain objects, materialize `R_CMB`, open score entry, compute a likelihood, or
decide the dark-sector question.

## Execution Rows

{row_text}

## Status

```text
{summary["status"]}
```

The route now has concrete checker command templates and prerequisite rules,
but all execution, success, pass, and acceptance flags remain false.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB carrier/domain checker execution packet.")
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
