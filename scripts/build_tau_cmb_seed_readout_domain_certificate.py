#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_seed_readout_domain_certificate_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_seed_readout_domain_certificate_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_seed_readout_domain_certificate_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_seed_readout_domain_certificate_v01_certificate_requirements_only_"
    "domain_not_certified_no_readout_evaluation_no_survival_no_A_tau_value_no_score_no_verdict"
)

FIELDS = [
    "certificate_row_id",
    "certificate_component",
    "formal_object",
    "required_evidence",
    "available_evidence",
    "certificate_status",
    "blocking_reason",
    "next_required_artifact",
    "allows_domain_acceptance",
    "allows_readout_evaluation",
    "allows_survival_claim",
    "allows_A_tau_value",
    "allows_score_entry",
    "claim_boundary",
]

ROWS = [
    {
        "certificate_component": "seed_object_identity",
        "formal_object": "seed_tau_CMB",
        "required_evidence": "stable Tau-side object identity with hash/provenance and endpoint exclusion",
        "available_evidence": "morphological seed descriptor candidate declares a stable name and endpoint-exclusion boundary",
        "certificate_status": "EVIDENCE_PARTIAL_DESCRIPTOR_ONLY",
        "blocking_reason": "identity exists only as an unaccepted descriptor candidate, not as a supplied payload",
        "next_required_artifact": "seed_tau_payload.csv",
    },
    {
        "certificate_component": "support_domain",
        "formal_object": "supp(seed_tau_CMB) subset Tau_CMB_parent_domain",
        "required_evidence": "support coordinates, scale labels, and parent-domain convention fixed before endpoint readout",
        "available_evidence": "payload requests mention support coordinates and normalization convention",
        "certificate_status": "REQUIRED_SUPPORT_NOT_SUPPLIED",
        "blocking_reason": "no support coordinates or parent-domain construction are supplied",
        "next_required_artifact": "seed_tau_payload.csv.provenance.json",
    },
    {
        "certificate_component": "intrinsic_descriptor",
        "formal_object": "descriptor(seed_tau_CMB)",
        "required_evidence": "intrinsic morphology fields must be fixed without CMB endpoint target values",
        "available_evidence": "descriptor candidate forbids endpoint residual shape inputs",
        "certificate_status": "DECLARED_NOT_MATERIALIZED",
        "blocking_reason": "no concrete descriptor fields are materialized in an accepted payload",
        "next_required_artifact": "seed_tau_payload.csv",
    },
    {
        "certificate_component": "readout_domain_membership",
        "formal_object": "seed_tau_CMB in Dom(R_CMB)",
        "required_evidence": "a domain rule for R_CMB plus a replay showing seed_tau_CMB satisfies it",
        "available_evidence": "readout-interface candidate declares the membership schema",
        "certificate_status": "DOMAIN_RULE_NOT_DEFINED",
        "blocking_reason": "Dom(R_CMB) is not constructed and no membership replay exists",
        "next_required_artifact": "tau_cmb_readout_domain_rule_v01",
    },
    {
        "certificate_component": "endpoint_firewall",
        "formal_object": "seed_tau_CMB independent of O_CMB_endpoint",
        "required_evidence": "hash/provenance/firewall evidence showing the seed was frozen before endpoint evaluation",
        "available_evidence": "Paper 10-style source-freeze method is referenced as required protocol",
        "certificate_status": "FIREWALL_EVIDENCE_NOT_SUPPLIED",
        "blocking_reason": "no seed payload hash manifest, replay, or firewall attestation is supplied",
        "next_required_artifact": "seed_tau_payload.csv.firewall.json",
    },
    {
        "certificate_component": "zero_seed_membership",
        "formal_object": "null_seed in Dom(R_CMB)",
        "required_evidence": "zero/null seed must be admitted by the same domain rule for control replay",
        "available_evidence": "zero-seed control hook is declared in readout-interface candidate",
        "certificate_status": "CONTROL_DOMAIN_NOT_DEFINED",
        "blocking_reason": "null_seed and its domain membership are not defined",
        "next_required_artifact": "tau_cmb_seed_zero_control_v01",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def table_rows() -> list[dict[str, str]]:
    return [
        {
            "certificate_row_id": f"TCMBSRDC01_{index:03d}",
            "allows_domain_acceptance": "false",
            "allows_readout_evaluation": "false",
            "allows_survival_claim": "false",
            "allows_A_tau_value": "false",
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
    blocked = [
        row
        for row in rows
        if "NOT_" in row["certificate_status"]
        or "REQUIRED" in row["certificate_status"]
        or "PARTIAL" in row["certificate_status"]
    ]
    return {
        "report_id": "tau_cmb_seed_readout_domain_certificate_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "certificate_rows": len(rows),
        "blocked_or_partial_rows": len(blocked),
        "domain_acceptance_allowed": False,
        "readout_evaluation_allowed": False,
        "quotient_survival_claim_allowed": False,
        "seed_acceptance_allowed": False,
        "A_tau_value_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "SEED_READOUT_DOMAIN_CERTIFICATE_DECLARED_BLOCKED",
        "next_minimal_unblock": "materialize_endpoint_blind_seed_tau_payload_with_provenance_and_firewall",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['certificate_row_id']}` `{row['certificate_component']}`: "
        f"{row['certificate_status']} | blocks: {row['blocking_reason']}"
        for row in rows
    )
    text = f"""# Tau CMB Seed Readout Domain Certificate v01

**Doc class:** readout-domain certificate requirements
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact states what must be true before the CMB morphological seed can be
treated as a legitimate Tau-side input to `R_CMB`. It does not certify domain
membership, evaluate a readout, prove quotient survival, assign `A_tau(a,k)`,
enter scoring, or decide the dark-sector question.

## Certificate Target

```text
seed_tau_CMB in Dom(R_CMB)
```

The target is not accepted in v01 because the concrete seed payload, support
domain, domain rule, endpoint firewall, and zero-seed control are still absent.

## Certificate Rows

{row_text}

## Status

```text
{summary["status"]}
```

The domain gate is useful because it prevents a premature jump from a named
seed descriptor to CMB scoring. The next real unblock is not another broad
gate; it is a populated endpoint-blind `seed_tau` payload with provenance,
hashes, replay, support convention, and firewall evidence.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB seed readout domain certificate.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    table_path = Path(args.write_table or DEFAULT_TABLE)
    rows = table_rows()
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
