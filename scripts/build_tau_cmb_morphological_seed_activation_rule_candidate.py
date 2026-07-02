#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_morphological_seed_activation_rule_candidate_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_morphological_seed_activation_rule_candidate_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_morphological_seed_activation_rule_candidate_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_morphological_seed_activation_rule_candidate_v01_rule_candidate_only_"
    "no_activation_proof_no_A_tau_value_no_source_acceptance_no_phi_derivation_no_score_no_verdict"
)

FIELDS = [
    "rule_row_id",
    "rule_component",
    "formal_object",
    "candidate_rule_text",
    "required_inputs",
    "dimension_or_unit_status",
    "acceptance_blocker",
    "current_status",
    "allows_activation_acceptance",
    "allows_A_tau_value",
    "allows_source_acceptance",
    "allows_score_entry",
    "claim_boundary",
]

ROWS = [
    {
        "rule_component": "activation_domain",
        "formal_object": "seed_tau_CMB in Dom(Act_tau_CMB)",
        "candidate_rule_text": "The seed may enter an activation rule only if its morphology/readout descriptor is endpoint-blind and audit-routable.",
        "required_inputs": "seed descriptor candidate audit; source-grounding gate; parent-source freeze packet",
        "dimension_or_unit_status": "domain condition, not a physical unit",
        "acceptance_blocker": "domain is declared but not proven admissible under quotient/null survival",
        "current_status": "DOMAIN_DECLARED_NOT_ACCEPTED",
    },
    {
        "rule_component": "conditional_activation_map",
        "formal_object": "Act_tau_CMB[seed_tau_CMB](a,k) -> A_tau_candidate(a,k)",
        "candidate_rule_text": "A future activation map may send a CMB morphological seed to a dimensionless amplitude candidate A_tau(a,k).",
        "required_inputs": "quotient survival; closure stability; readout survival; gauge/normalization lock",
        "dimension_or_unit_status": "A_tau_candidate must be dimensionless if promoted",
        "acceptance_blocker": "no map, formula, coefficients, support, or normalization are supplied",
        "current_status": "MAP_SKELETON_DECLARED_NOT_DERIVED",
    },
    {
        "rule_component": "zero_seed_limit",
        "formal_object": "seed_tau_CMB = null_seed => A_tau_candidate(a,k) = 0 or inactive",
        "candidate_rule_text": "A promoted rule must include a null-seed limit so activation cannot arise from nothing or from endpoint fitting.",
        "required_inputs": "declared null seed; quotient/null model; zero-preserving activation rule",
        "dimension_or_unit_status": "limit condition, not a unit claim",
        "acceptance_blocker": "null seed and zero-preserving proof are not supplied",
        "current_status": "LIMIT_REQUIRED_NOT_PROVED",
    },
    {
        "rule_component": "endpoint_blindness_constraint",
        "formal_object": "Act_tau_CMB independent of endpoint residuals and scores",
        "candidate_rule_text": "The activation rule inputs must exclude CMB residual shapes, score deltas, likelihood deltas, and post-hoc tuning.",
        "required_inputs": "seed firewall/replay certificate; provenance hash; endpoint-token audit",
        "dimension_or_unit_status": "firewall condition, not physical",
        "acceptance_blocker": "seed-specific firewall/replay certificate is absent",
        "current_status": "FIREWALL_CONSTRAINT_DECLARED_NOT_CERTIFIED",
    },
    {
        "rule_component": "spine_binding",
        "formal_object": "A_tau_candidate(a,k) -> rho_tau_eff(a,k) role slot only after acceptance",
        "candidate_rule_text": "Even if A_tau_candidate is later derived, it may enter rho_tau_eff only after source-grounding acceptance.",
        "required_inputs": "activation acceptance; source-grounding gate pass; dimensional precheck",
        "dimension_or_unit_status": "rho_tau_eff inherits density units only after accepted A_tau is dimensionless",
        "acceptance_blocker": "source-grounding acceptance is not available",
        "current_status": "BINDING_DECLARED_NOT_ACCEPTED",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def table_rows() -> list[dict[str, str]]:
    return [
        {
            "rule_row_id": f"TCMBMSARC01_{index:03d}",
            "allows_activation_acceptance": "false",
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
    return {
        "report_id": "tau_cmb_morphological_seed_activation_rule_candidate_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "rows": len(rows),
        "rule_candidate_declared": True,
        "activation_acceptance_allowed": False,
        "A_tau_value_supplied": False,
        "source_acceptance_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "MORPHOLOGICAL_SEED_ACTIVATION_RULE_CANDIDATE_DECLARED_NOT_DERIVED",
        "next_minimal_unblock": "audit_tau_cmb_morphological_seed_activation_rule_candidate_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['rule_row_id']}` `{row['rule_component']}`: {row['current_status']} | `{row['formal_object']}`"
        for row in rows
    )
    text = f"""# Tau CMB Morphological Seed Activation Rule Candidate v01

**Doc class:** morphological-seed activation rule candidate
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact declares the smallest conditional activation-rule skeleton from a
CMB morphological seed toward a possible `A_tau(a,k)` candidate. It does not
derive `A_tau`, supply an amplitude, accept the seed, or accept a source.

## Candidate Rule Skeleton

```text
seed_tau_CMB in Dom(Act_tau_CMB)
Act_tau_CMB[seed_tau_CMB](a,k) -> A_tau_candidate(a,k)
```

The skeleton is only meaningful if quotient/null survival, closure stability,
readout survival, gauge/normalization, and firewall/replay certificates are
later supplied.

## Rule Rows

{row_text}

## Status

```text
{summary["status"]}
```

No activation acceptance, `A_tau(a,k)` value, source acceptance, `Phi_tau_eff`
derivation, score entry, or dark-sector verdict is allowed.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB morphological seed activation rule candidate.")
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
