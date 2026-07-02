#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD_ACCEPTANCE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_scaffold_output_acceptance_summary_v01.json"
STAGING_ROOT = ROOT / "payload_staging/tau_cmb_carrier_domain_checker_input_payloads"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_level_checker_rule_implementation_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_level_checker_rule_implementation_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_level_checker_rule_implementation_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_level_checker_rule_implementation_v01_"
    "certificate_predicate_rules_implemented_but_semantic_evidence_absent_"
    "no_certificate_pass_no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "rule_row_id",
    "certificate_area",
    "checker_name",
    "certificate_rule_predicates",
    "required_semantic_evidence_fields",
    "staging_dir",
    "rule_implementation_declared",
    "scaffold_output_accepted",
    "semantic_evidence_fields_present",
    "certificate_rule_executable",
    "certificate_passed",
    "domain_object_accepted",
    "allows_physical_R_CMB",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "rule_status",
    "blocking_reason",
    "claim_boundary",
]

RULES = [
    {
        "certificate_area": "carrier_well_formedness",
        "checker_name": "run_carrier_ok_checker",
        "certificate_rule_predicates": "CarrierOK := role_basis_valid and role_bundle_closes and carrier_provenance_endpoint_blind and carrier_hashes_match",
        "required_semantic_evidence_fields": "role_basis_valid; role_bundle_closes; carrier_hashes_match",
    },
    {
        "certificate_area": "domain_membership_rule",
        "checker_name": "run_dom_ok_checker",
        "certificate_rule_predicates": "DomOK := parent_side_object and support_ok and normalization_ok and replay_ok and firewall_ok",
        "required_semantic_evidence_fields": "parent_side_object; support_ok; normalization_ok; replay_ok; firewall_ok",
    },
    {
        "certificate_area": "seed_admissibility",
        "checker_name": "run_seed_admissibility_checker",
        "certificate_rule_predicates": "SeedInDomain := seed_descriptor_pass and activation_pass and quotient_survival_witness_pass and seed_equivalence_replay_pass",
        "required_semantic_evidence_fields": "seed_descriptor_pass; activation_pass; quotient_survival_witness_pass; seed_equivalence_replay_pass",
    },
    {
        "certificate_area": "null_control_admissibility",
        "checker_name": "run_null_control_checker",
        "certificate_rule_predicates": "NullControlInDomain := null_readout_candidate_valid and no_response_proof_pass and zero_control_replay_pass and null_coordinate_replay_pass",
        "required_semantic_evidence_fields": "null_readout_candidate_valid; no_response_proof_pass; zero_control_replay_pass; null_coordinate_replay_pass",
    },
    {
        "certificate_area": "source_object_admissibility",
        "checker_name": "run_source_object_checker",
        "certificate_rule_predicates": "SourceObjectInDomain := endpoint_blind_derivation_pass and known_limit_check_pass and dimension_gauge_replay_pass and source_firewall_pass",
        "required_semantic_evidence_fields": "endpoint_blind_derivation_pass; known_limit_check_pass; dimension_gauge_replay_pass; source_firewall_pass",
    },
    {
        "certificate_area": "quotient_and_equivalence_survival",
        "checker_name": "run_quotient_survival_checker",
        "certificate_rule_predicates": "QuotientSurvival := equivalence_relation_pass and null_class_identified and representative_independence_pass and non_null_witness_pass",
        "required_semantic_evidence_fields": "equivalence_relation_pass; null_class_identified; representative_independence_pass; non_null_witness_pass",
    },
    {
        "certificate_area": "endpoint_firewall_replay",
        "checker_name": "run_endpoint_firewall_checker",
        "certificate_rule_predicates": "EndpointFirewallOK := no_endpoint_data_access and no_score_access and no_post_endpoint_tuning and provenance_lock_pass",
        "required_semantic_evidence_fields": "no_endpoint_data_access; no_score_access; no_post_endpoint_tuning; provenance_lock_pass",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def input_chain_clean() -> bool:
    if not SCAFFOLD_ACCEPTANCE.exists():
        return False
    summary = load_json(SCAFFOLD_ACCEPTANCE)
    return (
        summary.get("status")
        == "CARRIER_DOMAIN_CHECKER_SCAFFOLD_OUTPUTS_ACCEPTED_FOR_CERTIFICATE_IMPLEMENTATION_DEVELOPMENT_ONLY"
        and summary.get("accepted_as_scaffold_output_rows") == 7
        and summary.get("certificate_passed_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def collect_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            keys.add(str(key))
            keys |= collect_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            keys |= collect_keys(nested)
    return keys


def semantic_fields_present(area: str, required_fields: list[str]) -> bool:
    staging_dir = STAGING_ROOT / area
    keys: set[str] = set()
    for path in staging_dir.glob("*.json"):
        keys |= collect_keys(load_json(path))
    return all(field in keys for field in required_fields)


def table_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    chain_ok = input_chain_clean()
    for index, rule in enumerate(RULES, start=1):
        fields = [item.strip() for item in rule["required_semantic_evidence_fields"].split(";")]
        semantic_ok = semantic_fields_present(rule["certificate_area"], fields)
        scaffold_ok = chain_ok
        executable = scaffold_ok and semantic_ok
        rows.append(
            {
                "rule_row_id": f"TCMBCDLCRI01_{index:03d}",
                "certificate_area": rule["certificate_area"],
                "checker_name": rule["checker_name"],
                "certificate_rule_predicates": rule["certificate_rule_predicates"],
                "required_semantic_evidence_fields": rule["required_semantic_evidence_fields"],
                "staging_dir": rel(STAGING_ROOT / rule["certificate_area"]),
                "rule_implementation_declared": "true",
                "scaffold_output_accepted": str(scaffold_ok).lower(),
                "semantic_evidence_fields_present": str(semantic_ok).lower(),
                "certificate_rule_executable": str(executable).lower(),
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_physical_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "rule_status": (
                    "CERTIFICATE_RULE_IMPLEMENTED_AND_EXECUTABLE_NOT_RUN_AS_CERTIFICATE"
                    if executable
                    else "CERTIFICATE_RULE_IMPLEMENTED_BLOCKED_BY_SEMANTIC_EVIDENCE"
                ),
                "blocking_reason": (
                    "certificate predicates are declared but required semantic evidence fields are absent from current staging payloads"
                    if not semantic_ok
                    else "certificate rule is executable, but certificate-pass audit remains downstream"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def write_table(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_summary(table_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "report_id": "tau_cmb_certificate_level_checker_rule_implementation_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_scaffold_output_acceptance_summary": rel(SCAFFOLD_ACCEPTANCE),
        "input_chain_clean": input_chain_clean(),
        "rule_rows": len(rows),
        "rule_implementation_declared_rows": sum(row["rule_implementation_declared"] == "true" for row in rows),
        "scaffold_output_accepted_rows": sum(row["scaffold_output_accepted"] == "true" for row in rows),
        "semantic_evidence_fields_present_rows": sum(row["semantic_evidence_fields_present"] == "true" for row in rows),
        "certificate_rule_executable_rows": sum(row["certificate_rule_executable"] == "true" for row in rows),
        "certificate_passed_rows": 0,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_LEVEL_CHECKER_RULES_IMPLEMENTED_BLOCKED_BY_SEMANTIC_EVIDENCE"
            if input_chain_clean() and len(rows) == 7 and all(row["rule_implementation_declared"] == "true" for row in rows)
            else "CMB_CERTIFICATE_LEVEL_CHECKER_RULE_IMPLEMENTATION_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_materialization_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['certificate_area']}`: {row['rule_status']} | semantic_evidence={row['semantic_evidence_fields_present']}"
        for row in rows
    )
    text = f"""# Tau CMB Certificate-Level Checker Rule Implementation v01

**Doc class:** certificate-level checker rule implementation
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact implements the certificate-level predicate targets for the seven
non-codomain checker families. It does not pass certificates. It checks whether
the current staging payloads contain the semantic evidence fields needed to
execute those certificate predicates.

## Rule Rows

{row_text}

## Summary

```text
rule_rows={summary["rule_rows"]}
rule_implementation_declared_rows={summary["rule_implementation_declared_rows"]}
scaffold_output_accepted_rows={summary["scaffold_output_accepted_rows"]}
semantic_evidence_fields_present_rows={summary["semantic_evidence_fields_present_rows"]}
certificate_rule_executable_rows={summary["certificate_rule_executable_rows"]}
certificate_passed_rows={summary["certificate_passed_rows"]}
accepted_domain_objects={summary["accepted_domain_objects"]}
score_entry_allowed={summary["score_entry_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB certificate-level checker rule implementation.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = table_rows()
    table_path = Path(args.write_table) if args.write_table else DEFAULT_TABLE
    summary = build_summary(table_path, rows)
    if args.write_table:
        write_table(table_path, rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), rows, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
