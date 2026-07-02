#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_seed_support_domain_rule_candidate_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_seed_support_domain_rule_candidate_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_seed_support_domain_rule_candidate_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_seed_support_domain_rule_candidate_v01_rule_candidate_only_"
    "support_not_certified_no_payload_acceptance_no_domain_certificate_no_readout_no_score_no_verdict"
)

FIELDS = [
    "rule_row_id",
    "rule_component",
    "formal_object",
    "candidate_rule",
    "endpoint_blind_source",
    "required_audit",
    "candidate_status",
    "blocking_reason",
    "next_required_artifact",
    "allows_support_certification",
    "allows_payload_acceptance",
    "allows_domain_certificate",
    "allows_readout_evaluation",
    "allows_score_entry",
    "claim_boundary",
]

ROWS = [
    {
        "rule_component": "parent_domain_symbol",
        "formal_object": "Tau_CMB_parent_domain := {morphology_readout_sector=CMB}",
        "candidate_rule": "treat the CMB parent domain as the Tau-side morphology/readout sector declared before endpoint evaluation",
        "endpoint_blind_source": "seed payload candidate; morphology-conditioned projection principle; CMB derivation spine role labels",
        "required_audit": "verify the symbol is a sector label only and not a fitted endpoint domain",
        "candidate_status": "DECLARED_SYMBOL_NOT_CERTIFIED",
        "blocking_reason": "parent-domain construction is still symbolic",
        "next_required_artifact": "tau_cmb_parent_domain_construction_audit_v01",
    },
    {
        "rule_component": "support_coordinate_basis",
        "formal_object": "xi_seed := (morphology_class, readout_sector, scale_label)",
        "candidate_rule": "use a dimensionless support coordinate tuple built from Tau-side descriptor fields",
        "endpoint_blind_source": "payload fields: tau_side_descriptor, support_coordinate, scale_label",
        "required_audit": "verify every coordinate component is fixed without endpoint residuals or scores",
        "candidate_status": "CANDIDATE_BASIS_DECLARED_NOT_ACCEPTED",
        "blocking_reason": "scale_label is not normalized and support coordinate is still sector-level",
        "next_required_artifact": "tau_cmb_seed_support_coordinate_audit_v01",
    },
    {
        "rule_component": "membership_rule",
        "formal_object": "seed_tau_CMB in Tau_CMB_parent_domain iff xi_seed is well-formed and endpoint-blind",
        "candidate_rule": "membership may be checked from payload candidate fields plus firewall evidence only",
        "endpoint_blind_source": "seed_tau_payload_candidate_v01.csv and firewall/provenance files",
        "required_audit": "verify well-formed tuple, hash binding, and endpoint firewall",
        "candidate_status": "MEMBERSHIP_RULE_DECLARED_NOT_PROVED",
        "blocking_reason": "well-formedness and firewall audit are not yet promoted to support certification",
        "next_required_artifact": "tau_cmb_seed_support_membership_audit_v01",
    },
    {
        "rule_component": "forbidden_endpoint_dependence",
        "formal_object": "xi_seed independent of O_CMB_endpoint",
        "candidate_rule": "support coordinates cannot be chosen from CMB residuals, peak shapes, likelihood deltas, or score outputs",
        "endpoint_blind_source": "candidate firewall attestation and forbidden endpoint input list",
        "required_audit": "prove the support coordinate text and provenance do not import forbidden endpoint values",
        "candidate_status": "FIREWALL_RULE_DECLARED_NOT_ACCEPTED",
        "blocking_reason": "candidate firewall attestation exists but no independent support audit has accepted it",
        "next_required_artifact": "tau_cmb_seed_support_firewall_audit_v01",
    },
    {
        "rule_component": "normalization_dependency",
        "formal_object": "N_seed may only act after xi_seed is fixed",
        "candidate_rule": "normalization replay must consume the support tuple, not redefine it",
        "endpoint_blind_source": "payload unblock triad dependency order",
        "required_audit": "verify normalization candidate references this support rule as fixed input",
        "candidate_status": "DEPENDENCY_DECLARED_NOT_EXECUTED",
        "blocking_reason": "normalization replay candidate does not exist yet",
        "next_required_artifact": "tau_cmb_seed_normalization_replay_candidate_v01",
    },
    {
        "rule_component": "zero_control_dependency",
        "formal_object": "null_seed in Tau_CMB_parent_domain uses same xi_seed convention",
        "candidate_rule": "zero-control must be stated over the same support convention and cannot become a physical response",
        "endpoint_blind_source": "quotient survival test and zero-source obligation",
        "required_audit": "verify null_seed is a control object, not a fitted physical source",
        "candidate_status": "DEPENDENCY_DECLARED_NOT_EXECUTED",
        "blocking_reason": "zero-control candidate does not exist yet",
        "next_required_artifact": "tau_cmb_seed_zero_control_v01",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def table_rows() -> list[dict[str, str]]:
    return [
        {
            "rule_row_id": f"TCMBSSDRC01_{index:03d}",
            "allows_support_certification": "false",
            "allows_payload_acceptance": "false",
            "allows_domain_certificate": "false",
            "allows_readout_evaluation": "false",
            "allows_score_entry": "false",
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
    return {
        "report_id": "tau_cmb_seed_support_domain_rule_candidate_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "rule_rows": len(rows),
        "support_rule_declared": True,
        "support_certification_allowed": False,
        "payload_acceptance_allowed": False,
        "domain_certificate_allowed": False,
        "readout_evaluation_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "SEED_SUPPORT_DOMAIN_RULE_CANDIDATE_DECLARED_NOT_CERTIFIED",
        "next_minimal_unblock": "tau_cmb_seed_support_domain_rule_candidate_audit_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['rule_row_id']}` `{row['rule_component']}`: {row['candidate_status']} | `{row['formal_object']}`"
        for row in rows
    )
    text = f"""# Tau CMB Seed Support Domain Rule Candidate v01

**Doc class:** support-domain rule candidate
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact declares a candidate support-domain rule for the CMB
`seed_tau` payload. It does not certify support, accept the payload, certify
`seed_tau_CMB in Dom(R_CMB)`, evaluate readout survival, assign `A_tau(a,k)`,
enter scoring, or decide the dark-sector question.

## Candidate Rule Shape

```text
Tau_CMB_parent_domain := {{morphology_readout_sector = CMB}}
xi_seed := (morphology_class, readout_sector, scale_label)
seed_tau_CMB in Tau_CMB_parent_domain iff xi_seed is well-formed and endpoint-blind
```

## Rows

{row_text}

## Status

```text
{summary["status"]}
```

The rule is useful because it gives normalization replay and zero-control a
shared parent-domain convention, but it remains uncertified until a support
audit checks well-formedness, hash/provenance binding, and endpoint blindness.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB seed support domain rule candidate.")
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
