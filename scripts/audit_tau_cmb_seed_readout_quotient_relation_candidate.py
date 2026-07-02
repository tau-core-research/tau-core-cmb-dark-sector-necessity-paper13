#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RELATION_TABLE = ROOT / "data/derived/tau_cmb_seed_readout_quotient_relation_candidate_v01.csv"
RELATION_SUMMARY = ROOT / "data/derived/tau_cmb_seed_readout_quotient_relation_candidate_summary_v01.json"
PRE_ACCEPTANCE_GATE = ROOT / "data/derived/tau_cmb_seed_chain_pre_acceptance_gate_summary_v01.json"
ZERO_CONTROL_AUDIT = ROOT / "data/derived/tau_cmb_seed_zero_control_audit_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_seed_readout_quotient_relation_candidate_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_seed_readout_quotient_relation_candidate_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_seed_readout_quotient_relation_candidate_audit_v01_audit_only_"
    "relation_not_accepted_no_readout_evaluation_no_equivalence_proof_no_survival_proof_no_score_no_verdict"
)


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def audit_row(component: str, status: str, finding: str, passed: bool, blocking_reason: str) -> dict[str, Any]:
    return {
        "component": component,
        "audit_status": status,
        "finding": finding,
        "audit_passed": passed,
        "blocking_reason": blocking_reason,
    }


def build_report() -> dict[str, Any]:
    required = [RELATION_TABLE, RELATION_SUMMARY, PRE_ACCEPTANCE_GATE, ZERO_CONTROL_AUDIT]
    missing = [path for path in required if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    relation_rows = read_csv(RELATION_TABLE)
    summary = load_json(RELATION_SUMMARY)
    pre_gate = load_json(PRE_ACCEPTANCE_GATE)
    zero_audit = load_json(ZERO_CONTROL_AUDIT)
    components = [item.get("component") for item in relation_rows]
    expected = [
        "readout_family_symbol",
        "null_readout_anchor",
        "readout_equivalence_relation",
        "quotient_class_candidate",
        "survival_condition_candidate",
        "promotion_firewall",
    ]
    rows.append(audit_row(
        "relation_table_shape",
        "PASS_RELATION_ROWS_PRESENT" if components == expected else "FAIL_RELATION_ROW_SHAPE",
        f"components={components}",
        components == expected,
        "relation audit requires the six declared candidate rows",
    ))

    deps_ok = (
        summary.get("candidate_declarable") is True
        and pre_gate.get("status") == "SEED_CHAIN_PRE_ACCEPTANCE_GATE_CLEAN_BLOCKED_ON_READOUT_QUOTIENT"
        and zero_audit.get("status") == "SEED_ZERO_CONTROL_AUDITED_BLOCKED_NOT_ACCEPTED"
        and pre_gate.get("failed_rows") == 0
        and zero_audit.get("failed_rows") == 0
    )
    rows.append(audit_row(
        "input_dependency_chain",
        "PASS_INPUT_CHAIN_CLEAN" if deps_ok else "FAIL_INPUT_CHAIN",
        "pre-acceptance gate and zero-control audit are present with zero failures",
        deps_ok,
        "relation candidate can only be audited after clean seed-chain and zero-control inputs",
    ))

    formal_objects = "\n".join(item.get("formal_object", "") for item in relation_rows)
    readout_symbol_ok = "R_CMB^seed" in formal_objects and "CMB_role_space_candidate" in formal_objects
    rows.append(audit_row(
        "readout_family_symbol",
        "PASS_READOUT_SYMBOL_DECLARED" if readout_symbol_ok else "FAIL_READOUT_SYMBOL",
        "seed-level readout family symbol is declared",
        readout_symbol_ok,
        "audit requires a named readout symbol before quotient syntax",
    ))

    null_anchor_ok = "R_CMB^seed(null_seed_tau_CMB) := null_readout" in formal_objects
    rows.append(audit_row(
        "null_readout_anchor",
        "PASS_NULL_ANCHOR_DECLARED" if null_anchor_ok else "FAIL_NULL_ANCHOR",
        "null seed is anchored to null_readout in the relation candidate",
        null_anchor_ok,
        "quotient relation must expose its null anchor",
    ))

    relation_ok = any(
        item.get("component") == "readout_equivalence_relation"
        and "~_{R_CMB,seed}" in item.get("formal_object", "")
        and "DECLARED_RELATION_NOT_PROVED" == item.get("candidate_status")
        for item in relation_rows
    )
    rows.append(audit_row(
        "equivalence_relation_syntax",
        "PASS_EQUIVALENCE_SYNTAX_DECLARED" if relation_ok else "FAIL_EQUIVALENCE_SYNTAX",
        "readout equivalence relation syntax is declared but not proved",
        relation_ok,
        "candidate relation must remain explicitly unproved",
    ))

    survival_ok = any(
        item.get("component") == "survival_condition_candidate"
        and "Surv_R(seed_tau_CMB)" in item.get("formal_object", "")
        and "null_readout" in item.get("formal_object", "")
        and "DECLARED_CONDITION_NOT_TESTED" == item.get("candidate_status")
        for item in relation_rows
    )
    rows.append(audit_row(
        "survival_condition_syntax",
        "PASS_SURVIVAL_CONDITION_DECLARED" if survival_ok else "FAIL_SURVIVAL_CONDITION",
        "future non-null survival condition is declared but not tested",
        survival_ok,
        "survival condition must not be promoted to a survival proof",
    ))

    permissions_closed = (
        all(item.get("allows_readout_evaluation") == "false" for item in relation_rows)
        and all(item.get("allows_equivalence_proof") == "false" for item in relation_rows)
        and all(item.get("allows_survival_claim") == "false" for item in relation_rows)
        and all(item.get("allows_score_entry") == "false" for item in relation_rows)
        and summary.get("readout_evaluation_allowed") is False
        and summary.get("quotient_survival_claim_allowed") is False
        and summary.get("score_entry_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )
    rows.append(audit_row(
        "promotion_firewall",
        "PASS_PROMOTION_FIREWALL_CLOSED" if permissions_closed else "FAIL_PROMOTION_FIREWALL",
        "readout evaluation, equivalence proof, survival claim, score, and verdict permissions remain closed",
        permissions_closed,
        "relation candidate must not enter scoring or verdict logic",
    ))

    proof_missing = any(
        item.get("component") == "readout_equivalence_relation"
        and item.get("candidate_status") == "DECLARED_RELATION_NOT_PROVED"
        for item in relation_rows
    )
    rows.append(audit_row(
        "equivalence_axiom_proof",
        "BLOCKED_EQUIVALENCE_AXIOMS_NOT_PROVED" if proof_missing else "FAIL_EQUIVALENCE_PROOF_STATE",
        "reflexive/symmetric/transitive proof and control-list audit are not supplied",
        False,
        "equivalence relation still requires an axiom/control audit",
    ))

    readout_missing = any(
        item.get("component") == "readout_family_symbol"
        and item.get("candidate_status") == "DECLARED_SYMBOL_NOT_MATERIALIZED"
        for item in relation_rows
    )
    rows.append(audit_row(
        "readout_materialization",
        "BLOCKED_READOUT_NOT_MATERIALIZED" if readout_missing else "FAIL_READOUT_MATERIALIZATION_STATE",
        "role-space basis, transfer kernel, units, and numerical map are not supplied",
        False,
        "concrete R_CMB must be materialized before readout evaluation",
    ))

    survival_missing = any(
        item.get("component") == "survival_condition_candidate"
        and item.get("candidate_status") == "DECLARED_CONDITION_NOT_TESTED"
        for item in relation_rows
    )
    rows.append(audit_row(
        "non_null_survival_test",
        "BLOCKED_SURVIVAL_TEST_NOT_SUPPLIED" if survival_missing else "FAIL_SURVIVAL_TEST_STATE",
        "non-null class membership and sensitivity test are not supplied",
        False,
        "survival claim requires a tested non-null representative",
    ))

    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(item["audit_passed"]) for item in rows)
    blocked = sum(item["audit_status"].startswith("BLOCKED") for item in rows)
    failed = sum(item["audit_status"].startswith("FAIL") for item in rows)
    return {
        "report_id": "tau_cmb_seed_readout_quotient_relation_candidate_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_relation_table": rel(RELATION_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "relation_candidate_audited": True,
        "relation_acceptance_allowed": False,
        "readout_evaluation_allowed": False,
        "equivalence_proof_allowed": False,
        "quotient_survival_claim_allowed": False,
        "domain_certificate_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "SEED_READOUT_QUOTIENT_RELATION_CANDIDATE_AUDITED_BLOCKED_NOT_ACCEPTED",
        "next_minimal_unblock": "tau_cmb_seed_readout_equivalence_relation_audit_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{item['component']}`: {item['audit_status']} | {item['finding']}"
        for item in report["audit_rows"]
    )
    text = f"""# Tau CMB Seed Readout Quotient Relation Candidate Audit v01

**Doc class:** readout/quotient relation candidate audit
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks that the readout/quotient relation candidate is syntactically
declared from a clean seed-chain pre-acceptance state and that its promotion
firewall remains closed. It does not accept the relation, evaluate `R_CMB`,
prove the equivalence relation, prove quotient survival, certify a domain,
enter scoring, or decide the dark-sector question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The relation candidate is now audited as a candidate object. It remains blocked
because the equivalence axioms/control list, concrete readout materialization,
and non-null survival test are not supplied.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB seed readout quotient relation candidate.")
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    report = build_report()
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), report)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
