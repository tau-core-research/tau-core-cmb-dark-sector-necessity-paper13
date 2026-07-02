#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_morphological_seed_quotient_survival_test_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_morphological_seed_quotient_survival_test_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_morphological_seed_quotient_survival_test_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_morphological_seed_quotient_survival_test_v01_test_schema_only_"
    "no_survival_proof_no_seed_acceptance_no_A_tau_value_no_source_acceptance_no_score_no_verdict"
)

FIELDS = [
    "test_row_id",
    "test_component",
    "formal_object",
    "required_condition",
    "available_evidence",
    "test_status",
    "blocking_reason",
    "next_required_artifact",
    "allows_survival_claim",
    "allows_seed_acceptance",
    "allows_A_tau_value",
    "allows_source_acceptance",
    "allows_score_entry",
    "claim_boundary",
]

ROWS = [
    {
        "test_component": "readout_family",
        "formal_object": "R_CMB(seed_tau_CMB)",
        "required_condition": "declare the CMB readout map/interface under which seed survival is tested",
        "available_evidence": "CMB role family is declared in derivation spine",
        "test_status": "DECLARED_NOT_SPECIFIED",
        "blocking_reason": "no concrete R_CMB map or interface is supplied",
        "next_required_artifact": "tau_cmb_seed_readout_interface_candidate_v01",
    },
    {
        "test_component": "null_model",
        "formal_object": "N_R^CMB",
        "required_condition": "declare the null model against which the seed is compared",
        "available_evidence": "null/gauge readout-relativity principle imported from Tau Core theory",
        "test_status": "REQUIRED_NOT_SUPPLIED",
        "blocking_reason": "no CMB seed null model is supplied",
        "next_required_artifact": "tau_cmb_seed_null_model_candidate_v01",
    },
    {
        "test_component": "equivalence_relation",
        "formal_object": "R_CMB(seed_tau_CMB) ~ N_R^CMB",
        "required_condition": "declare observational/readout equivalence relation for null absorption or gauge redundancy",
        "available_evidence": "formal schema exists in Tau Core readout notes",
        "test_status": "REQUIRED_NOT_SUPPLIED",
        "blocking_reason": "no equivalence relation is supplied for CMB seed readout",
        "next_required_artifact": "tau_cmb_seed_readout_equivalence_relation_v01",
    },
    {
        "test_component": "quotient_map",
        "formal_object": "[seed_tau_CMB]_{~_R}",
        "required_condition": "define the quotient class and show the seed is not collapsed to the null class",
        "available_evidence": "seed descriptor candidate and activation rule skeleton exist",
        "test_status": "BLOCKED_QUOTIENT_MAP_NOT_DEFINED",
        "blocking_reason": "no quotient map or quotient class is defined",
        "next_required_artifact": "tau_cmb_seed_quotient_map_candidate_v01",
    },
    {
        "test_component": "survival_condition",
        "formal_object": "not Null_R_CMB(seed_tau_CMB)",
        "required_condition": "show the seed is distinguishable from the declared null model under the declared readout",
        "available_evidence": "none beyond descriptor cleanliness",
        "test_status": "BLOCKED_SURVIVAL_NOT_PROVED",
        "blocking_reason": "readout, null model, equivalence relation, quotient map, and sensitivity are missing",
        "next_required_artifact": "tau_cmb_seed_survival_condition_candidate_v01",
    },
    {
        "test_component": "zero_seed_control",
        "formal_object": "seed_tau_CMB = null_seed => inactive activation",
        "required_condition": "prove the null seed does not create A_tau_candidate by construction",
        "available_evidence": "zero-seed limit is required in activation rule candidate",
        "test_status": "BLOCKED_ZERO_CONTROL_NOT_PROVED",
        "blocking_reason": "null_seed and zero-preserving activation proof are missing",
        "next_required_artifact": "tau_cmb_seed_zero_control_v01",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def table_rows() -> list[dict[str, str]]:
    return [
        {
            "test_row_id": f"TCMBMSQST01_{index:03d}",
            "allows_survival_claim": "false",
            "allows_seed_acceptance": "false",
            "allows_A_tau_value": "false",
            "allows_source_acceptance": "false",
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
    blocked = [row for row in rows if "BLOCKED" in row["test_status"] or "REQUIRED" in row["test_status"]]
    return {
        "report_id": "tau_cmb_morphological_seed_quotient_survival_test_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "test_rows": len(rows),
        "blocked_or_required_rows": len(blocked),
        "survival_claim_allowed": False,
        "seed_acceptance_allowed": False,
        "A_tau_value_allowed": False,
        "source_acceptance_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "MORPHOLOGICAL_SEED_QUOTIENT_SURVIVAL_TEST_DECLARED_BLOCKED",
        "next_minimal_unblock": "build_tau_cmb_seed_readout_interface_candidate_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['test_row_id']}` `{row['test_component']}`: {row['test_status']} | blocks: {row['blocking_reason']}"
        for row in rows
    )
    text = f"""# Tau CMB Morphological Seed Quotient Survival Test v01

**Doc class:** quotient/null survival test schema
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact declares the quotient/null survival test that the CMB
morphological seed must eventually pass before it can support activation toward
`A_tau(a,k)`. It does not prove survival and does not accept the seed.

## Minimal Formal Shape

```text
Null_R(seed_tau_CMB) iff R_CMB(seed_tau_CMB) ~ N_R^CMB
survival requires: not Null_R(seed_tau_CMB)
```

## Test Rows

{row_text}

## Status

```text
{summary["status"]}
```

No quotient survival claim, seed acceptance, `A_tau(a,k)` value, source
acceptance, score entry, or dark-sector verdict is allowed.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB morphological seed quotient survival test.")
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
