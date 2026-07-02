#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_seed_readout_quotient_relation_candidate_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_seed_readout_quotient_relation_candidate_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_seed_readout_quotient_relation_candidate_v01.md"

PRE_ACCEPTANCE_GATE = ROOT / "data/derived/tau_cmb_seed_chain_pre_acceptance_gate_summary_v01.json"
READOUT_INTERFACE = ROOT / "data/derived/tau_cmb_seed_readout_interface_candidate_summary_v01.json"
QUOTIENT_SCHEMA = ROOT / "data/derived/tau_cmb_morphological_seed_quotient_survival_test_summary_v01.json"
ZERO_CONTROL_AUDIT = ROOT / "data/derived/tau_cmb_seed_zero_control_audit_v01.json"

CLAIM_BOUNDARY = (
    "tau_cmb_seed_readout_quotient_relation_candidate_v01_relation_candidate_only_"
    "no_readout_evaluation_no_equivalence_proof_no_survival_proof_no_domain_certificate_no_score_no_verdict"
)

FIELDS = [
    "relation_row_id",
    "component",
    "formal_object",
    "candidate_definition",
    "input_dependency",
    "candidate_status",
    "blocking_reason",
    "next_required_artifact",
    "allows_readout_evaluation",
    "allows_equivalence_proof",
    "allows_survival_claim",
    "allows_domain_certificate",
    "allows_score_entry",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

ROWS = [
    {
        "component": "readout_family_symbol",
        "formal_object": "R_CMB^seed: {seed_tau_CMB, null_seed_tau_CMB} -> CMB_role_space_candidate",
        "candidate_definition": "declare a seed-level CMB readout family symbol over the audited seed and null seed",
        "input_dependency": "seed-chain pre-acceptance gate; seed readout-interface candidate",
        "candidate_status": "DECLARED_SYMBOL_NOT_MATERIALIZED",
        "blocking_reason": "no basis, transfer kernel, units, or numerical map is supplied",
        "next_required_artifact": "tau_cmb_readout_role_space_basis_v01",
    },
    {
        "component": "null_readout_anchor",
        "formal_object": "R_CMB^seed(null_seed_tau_CMB) := null_readout",
        "candidate_definition": "reuse the audited zero-control object as the null anchor for the quotient relation",
        "input_dependency": "zero-control audit",
        "candidate_status": "DECLARED_ANCHOR_NOT_ACCEPTED",
        "blocking_reason": "zero-control is audited but not accepted as a readout-domain member",
        "next_required_artifact": "tau_cmb_seed_readout_domain_certificate_v01",
    },
    {
        "component": "readout_equivalence_relation",
        "formal_object": "x ~_{R_CMB,seed} y",
        "candidate_definition": "x and y are equivalent only if their CMB role-space representatives remain indistinguishable after declared null, gauge, convention, and endpoint-blind controls",
        "input_dependency": "quotient-survival schema; Tau Core null/gauge readout-relativity principle",
        "candidate_status": "DECLARED_RELATION_NOT_PROVED",
        "blocking_reason": "reflexive/symmetric/transitive proof and control list are not supplied",
        "next_required_artifact": "tau_cmb_seed_readout_equivalence_relation_audit_v01",
    },
    {
        "component": "quotient_class_candidate",
        "formal_object": "[seed_tau_CMB]_{~_{R_CMB,seed}}",
        "candidate_definition": "candidate quotient class of the CMB morphological seed under the declared readout equivalence relation",
        "input_dependency": "morphological seed quotient survival test",
        "candidate_status": "DECLARED_CLASS_NOT_EVALUATED",
        "blocking_reason": "non-null class membership is not tested",
        "next_required_artifact": "tau_cmb_seed_quotient_map_candidate_v01",
    },
    {
        "component": "survival_condition_candidate",
        "formal_object": "Surv_R(seed_tau_CMB) iff not (R_CMB^seed(seed_tau_CMB) ~_{R_CMB,seed} null_readout)",
        "candidate_definition": "survival is the future condition that the seed readout is not absorbed into the null-readout class",
        "input_dependency": "readout family symbol; null anchor; equivalence relation",
        "candidate_status": "DECLARED_CONDITION_NOT_TESTED",
        "blocking_reason": "no non-null readout representative or sensitivity test is supplied",
        "next_required_artifact": "tau_cmb_seed_survival_condition_candidate_v01",
    },
    {
        "component": "promotion_firewall",
        "formal_object": "relation_candidate != score_input",
        "candidate_definition": "the relation candidate cannot be used as CMB likelihood evidence or a Tau dark-sector verdict",
        "input_dependency": "claim-boundary firewall",
        "candidate_status": "PROMOTION_FORBIDDEN",
        "blocking_reason": "relation syntax is not empirical readout evaluation",
        "next_required_artifact": "tau_cmb_seed_readout_quotient_relation_candidate_audit_v01",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dependency_status() -> dict[str, Any]:
    deps = {
        "pre_acceptance_gate": PRE_ACCEPTANCE_GATE,
        "readout_interface": READOUT_INTERFACE,
        "quotient_schema": QUOTIENT_SCHEMA,
        "zero_control_audit": ZERO_CONTROL_AUDIT,
    }
    result: dict[str, Any] = {}
    for name, path in deps.items():
        if path.exists():
            data = load_json(path)
            result[name] = {
                "path": rel(path),
                "present": True,
                "status": data.get("status"),
                "failed_rows": data.get("failed_rows"),
            }
        else:
            result[name] = {"path": rel(path), "present": False, "status": "MISSING", "failed_rows": None}
    return result


def table_rows() -> list[dict[str, str]]:
    return [
        {
            "relation_row_id": f"TCMBSRQR01_{index:03d}",
            "allows_readout_evaluation": "false",
            "allows_equivalence_proof": "false",
            "allows_survival_claim": "false",
            "allows_domain_certificate": "false",
            "allows_score_entry": "false",
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
    deps = dependency_status()
    deps_present = all(item["present"] for item in deps.values())
    pre_gate_clean = deps["pre_acceptance_gate"].get("status") == "SEED_CHAIN_PRE_ACCEPTANCE_GATE_CLEAN_BLOCKED_ON_READOUT_QUOTIENT"
    zero_audited = deps["zero_control_audit"].get("status") == "SEED_ZERO_CONTROL_AUDITED_BLOCKED_NOT_ACCEPTED"
    candidate_declarable = deps_present and pre_gate_clean and zero_audited
    return {
        "report_id": "tau_cmb_seed_readout_quotient_relation_candidate_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "relation_rows": len(rows),
        "dependencies": deps,
        "candidate_declarable": candidate_declarable,
        "readout_family_symbol_declared": candidate_declarable,
        "null_anchor_declared": candidate_declarable,
        "equivalence_relation_declared": candidate_declarable,
        "survival_condition_declared": candidate_declarable,
        "readout_evaluation_allowed": False,
        "equivalence_proof_allowed": False,
        "quotient_survival_claim_allowed": False,
        "domain_certificate_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "SEED_READOUT_QUOTIENT_RELATION_CANDIDATE_DECLARED_NOT_ACCEPTED"
            if candidate_declarable
            else "SEED_READOUT_QUOTIENT_RELATION_CANDIDATE_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": (
            "tau_cmb_seed_readout_quotient_relation_candidate_audit_v01"
            if candidate_declarable
            else "repair_seed_readout_quotient_relation_inputs"
        ),
        "remaining_blockers": [
            "role_space_basis_missing",
            "readout_domain_certificate_missing",
            "equivalence_relation_axiom_audit_missing",
            "non_null_survival_test_missing",
            "score_entry_closed",
        ],
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['relation_row_id']}` `{row['component']}`: {row['candidate_status']} | {row['formal_object']}"
        for row in rows
    )
    blockers = "\n".join(f"- `{blocker}`" for blocker in summary["remaining_blockers"])
    text = f"""# Tau CMB Seed Readout Quotient Relation Candidate v01

**Doc class:** readout/quotient relation candidate
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact connects the clean seed-chain pre-acceptance gate to the missing
readout/quotient blocker. It declares a candidate readout-family symbol, a
null-readout anchor, a candidate readout equivalence relation, and the future
survival condition. It does not evaluate a readout, prove an equivalence
relation, prove quotient survival, certify the readout domain, enter scoring,
or decide the dark-sector question.

## Candidate Formal Shape

```text
R_CMB^seed: {{seed_tau_CMB, null_seed_tau_CMB}} -> CMB_role_space_candidate
R_CMB^seed(null_seed_tau_CMB) := null_readout
x ~_{{R_CMB,seed}} y
Surv_R(seed_tau_CMB) iff not (R_CMB^seed(seed_tau_CMB) ~_{{R_CMB,seed}} null_readout)
```

The equivalence relation is only declared as a candidate: two readout objects
may be identified only after declared null, gauge, convention, and
endpoint-blind controls. The equivalence axioms and the non-null survival test
are still future obligations.

## Rows

{row_text}

## Remaining Blockers

{blockers}

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
    parser = argparse.ArgumentParser(description="Build Tau CMB seed readout quotient relation candidate.")
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
