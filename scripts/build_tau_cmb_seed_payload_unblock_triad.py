#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_seed_payload_unblock_triad_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_seed_payload_unblock_triad_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_seed_payload_unblock_triad_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_seed_payload_unblock_triad_v01_unblock_plan_only_"
    "no_payload_acceptance_no_domain_certificate_no_readout_no_survival_no_A_tau_value_no_score_no_verdict"
)

FIELDS = [
    "triad_row_id",
    "blocker",
    "formal_target",
    "current_evidence",
    "required_unblock",
    "dependency_order",
    "status",
    "next_artifact",
    "allows_payload_acceptance",
    "allows_domain_certificate",
    "allows_readout_evaluation",
    "allows_score_entry",
    "claim_boundary",
]

ROWS = [
    {
        "blocker": "support_coordinate_system",
        "formal_target": "supp(seed_tau_CMB) subset Tau_CMB_parent_domain",
        "current_evidence": "payload candidate supplies a sector label: parent Tau morphology / CMB readout sector",
        "required_unblock": "define an endpoint-blind support coordinate convention and parent-domain membership rule",
        "dependency_order": "1",
        "status": "BLOCKED_SUPPORT_DOMAIN_RULE_MISSING",
        "next_artifact": "tau_cmb_seed_support_domain_rule_candidate_v01",
    },
    {
        "blocker": "tau_side_normalization_replay",
        "formal_target": "N_seed: descriptor(seed_tau_CMB) -> normalized_seed_tau_CMB",
        "current_evidence": "payload candidate declares dimensionless_structure_class_pending_normalization",
        "required_unblock": "define normalization inputs and replay command after support convention is fixed",
        "dependency_order": "2",
        "status": "BLOCKED_WAITING_FOR_SUPPORT_DOMAIN",
        "next_artifact": "tau_cmb_seed_normalization_replay_candidate_v01",
    },
    {
        "blocker": "null_limit_zero_control",
        "formal_target": "null_seed in Dom(R_CMB) and R_CMB(null_seed)=null_readout",
        "current_evidence": "readout-interface and quotient-survival tests require a null seed, but no definition exists",
        "required_unblock": "define null_seed over the same support convention and prove it remains non-physical control evidence",
        "dependency_order": "3",
        "status": "BLOCKED_WAITING_FOR_SUPPORT_AND_NORMALIZATION",
        "next_artifact": "tau_cmb_seed_zero_control_v01",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def table_rows() -> list[dict[str, str]]:
    return [
        {
            "triad_row_id": f"TCMBSPUT01_{index:03d}",
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
        "report_id": "tau_cmb_seed_payload_unblock_triad_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "triad_rows": len(rows),
        "blocked_rows": len(rows),
        "payload_acceptance_allowed": False,
        "domain_certificate_allowed": False,
        "readout_evaluation_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "SEED_PAYLOAD_UNBLOCK_TRIAD_DECLARED_BLOCKED",
        "next_minimal_unblock": "tau_cmb_seed_support_domain_rule_candidate_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['triad_row_id']}` `{row['blocker']}`: {row['status']} | next: `{row['next_artifact']}`"
        for row in rows
    )
    text = f"""# Tau CMB Seed Payload Unblock Triad v01

**Doc class:** seed-payload unblock plan
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact collapses the three remaining seed-payload audit blockers into a
single ordered unblock triad. It does not accept the payload, certify the
readout domain, evaluate CMB readout survival, assign `A_tau(a,k)`, enter
scoring, or decide the dark-sector question.

## Dependency Order

```text
support coordinate system
-> Tau-side normalization replay
-> null-limit / zero-control
```

The support-domain rule must come first because both normalization and
zero-control need to refer to the same parent-domain convention.

## Rows

{row_text}

## Status

```text
{summary["status"]}
```

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB seed payload unblock triad.")
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
