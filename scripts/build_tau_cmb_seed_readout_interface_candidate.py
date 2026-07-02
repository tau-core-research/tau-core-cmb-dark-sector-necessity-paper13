#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_seed_readout_interface_candidate_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_seed_readout_interface_candidate_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_seed_readout_interface_candidate_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_seed_readout_interface_candidate_v01_interface_schema_only_"
    "no_readout_evaluation_no_quotient_survival_no_seed_acceptance_no_A_tau_value_no_score_no_verdict"
)

FIELDS = [
    "interface_row_id",
    "interface_component",
    "formal_object",
    "candidate_requirement",
    "allowed_source",
    "forbidden_source",
    "candidate_status",
    "blocking_reason",
    "next_required_artifact",
    "allows_readout_evaluation",
    "allows_survival_claim",
    "allows_A_tau_value",
    "allows_score_entry",
    "claim_boundary",
]

ROWS = [
    {
        "interface_component": "readout_domain",
        "formal_object": "seed_tau_CMB in Dom(R_CMB)",
        "candidate_requirement": "the CMB seed must be declared as a Tau-side morphology object before any endpoint readout",
        "allowed_source": "morphological seed descriptor candidate and activation-rule skeleton",
        "forbidden_source": "ACT/Planck endpoint residuals or fitted CMB spectra",
        "candidate_status": "DECLARED_SCHEMA_NOT_PROVED",
        "blocking_reason": "no concrete Tau-side domain construction is supplied",
        "next_required_artifact": "tau_cmb_seed_readout_domain_certificate_v01",
    },
    {
        "interface_component": "readout_codomain",
        "formal_object": "R_CMB(seed_tau_CMB) -> CMB_role_space",
        "candidate_requirement": "the readout target must be a role space, not a fitted endpoint curve",
        "allowed_source": "CMB derivation spine roles: acoustic, lensing, growth, density-amplitude",
        "forbidden_source": "endpoint likelihood, posterior fit, or scoring residual",
        "candidate_status": "DECLARED_SCHEMA_NOT_MATERIALIZED",
        "blocking_reason": "no basis, units, or transfer normalization for the role space is supplied",
        "next_required_artifact": "tau_cmb_readout_role_space_basis_v01",
    },
    {
        "interface_component": "endpoint_blindness",
        "formal_object": "R_CMB independent of O_CMB_endpoint",
        "candidate_requirement": "the interface must be definable without looking at endpoint target values",
        "allowed_source": "source-freeze protocol and Paper 10-style endpoint firewall",
        "forbidden_source": "any operation tuned to pass the endpoint score",
        "candidate_status": "REQUIRED_FIREWALL_NOT_PROVED",
        "blocking_reason": "no replay certificate shows endpoint independence for this interface",
        "next_required_artifact": "tau_cmb_seed_readout_endpoint_firewall_certificate_v01",
    },
    {
        "interface_component": "null_model_hook",
        "formal_object": "R_CMB(seed_tau_CMB) ~ N_R^CMB",
        "candidate_requirement": "the interface must expose the object compared against the null model",
        "allowed_source": "quotient/null survival test schema",
        "forbidden_source": "post-hoc null chosen after seeing endpoint mismatch",
        "candidate_status": "HOOK_DECLARED_NULL_NOT_SUPPLIED",
        "blocking_reason": "no null model or equivalence relation is supplied",
        "next_required_artifact": "tau_cmb_seed_null_model_candidate_v01",
    },
    {
        "interface_component": "dimension_role",
        "formal_object": "dim(R_CMB(seed_tau_CMB)) compatible with CMB_role_space",
        "candidate_requirement": "readout outputs must carry declared dimensional or dimensionless roles before comparison",
        "allowed_source": "known-limit and dimension audit scaffold",
        "forbidden_source": "dimensionless rescaling selected from endpoint fit quality",
        "candidate_status": "REQUIRED_DIMENSION_PROOF_NOT_SUPPLIED",
        "blocking_reason": "no formula-level dimensional replay exists for the readout interface",
        "next_required_artifact": "tau_cmb_seed_readout_dimension_replay_v01",
    },
    {
        "interface_component": "zero_seed_control_hook",
        "formal_object": "R_CMB(null_seed) = null_readout",
        "candidate_requirement": "the interface must preserve a zero/null seed control before activation scoring",
        "allowed_source": "zero-source limit obligation and quotient survival test",
        "forbidden_source": "nonzero baseline injected to improve score readiness",
        "candidate_status": "CONTROL_HOOK_DECLARED_NOT_PROVED",
        "blocking_reason": "null_seed, null_readout, and zero-preserving replay are missing",
        "next_required_artifact": "tau_cmb_seed_zero_control_v01",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def table_rows() -> list[dict[str, str]]:
    return [
        {
            "interface_row_id": f"TCMBSRIC01_{index:03d}",
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
    blocked = [row for row in rows if "NOT_" in row["candidate_status"] or "REQUIRED" in row["candidate_status"]]
    return {
        "report_id": "tau_cmb_seed_readout_interface_candidate_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "interface_rows": len(rows),
        "blocked_or_required_rows": len(blocked),
        "readout_evaluation_allowed": False,
        "quotient_survival_claim_allowed": False,
        "seed_acceptance_allowed": False,
        "A_tau_value_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "SEED_READOUT_INTERFACE_CANDIDATE_DECLARED_NOT_ACCEPTED",
        "next_minimal_unblock": "tau_cmb_seed_readout_domain_certificate_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['interface_row_id']}` `{row['interface_component']}`: "
        f"{row['candidate_status']} | blocks: {row['blocking_reason']}"
        for row in rows
    )
    text = f"""# Tau CMB Seed Readout Interface Candidate v01

**Doc class:** readout-interface candidate scaffold
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact declares the minimum interface that would let the CMB
morphological seed enter a quotient/null survival test. It is a schema-level
candidate only: it does not evaluate a readout, prove survival, accept the seed,
assign `A_tau(a,k)`, enter scoring, or decide whether a Tau dark-sector
component is necessary.

## Candidate Interface Shape

```text
seed_tau_CMB in Dom(R_CMB)
R_CMB(seed_tau_CMB) -> CMB_role_space
R_CMB(seed_tau_CMB) ~ N_R^CMB is the later quotient/null comparison
```

## Interface Rows

{row_text}

## Status

```text
{summary["status"]}
```

The interface is route-useful but not acceptance-useful. The next concrete
unblock is a domain certificate showing that `seed_tau_CMB` is a legitimate
Tau-side object in the domain of `R_CMB` without endpoint input.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB seed readout interface candidate.")
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
