#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RELATION_TABLE = ROOT / "data/derived/tau_cmb_seed_readout_quotient_relation_candidate_v01.csv"
RELATION_AUDIT = ROOT / "data/derived/tau_cmb_seed_readout_quotient_relation_candidate_audit_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_seed_readout_equivalence_relation_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_seed_readout_equivalence_relation_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_seed_readout_equivalence_relation_audit_v01_axiom_audit_only_"
    "equivalence_not_proved_no_readout_evaluation_no_quotient_map_no_survival_claim_no_score_no_verdict"
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
    required = [RELATION_TABLE, RELATION_AUDIT]
    missing = [path for path in required if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    relation_rows = read_csv(RELATION_TABLE)
    relation_audit = load_json(RELATION_AUDIT)
    by_component = {row.get("component"): row for row in relation_rows}

    input_ok = (
        relation_audit.get("status") == "SEED_READOUT_QUOTIENT_RELATION_CANDIDATE_AUDITED_BLOCKED_NOT_ACCEPTED"
        and relation_audit.get("failed_rows") == 0
    )
    rows.append(audit_row(
        "input_relation_candidate_audit",
        "PASS_RELATION_CANDIDATE_AUDITED" if input_ok else "FAIL_RELATION_CANDIDATE_AUDIT",
        "relation-candidate audit is present with zero failures",
        input_ok,
        "equivalence audit requires a clean relation-candidate audit input",
    ))

    carrier_ok = "readout_family_symbol" in by_component and "CMB_role_space_candidate" in by_component["readout_family_symbol"].get("formal_object", "")
    rows.append(audit_row(
        "carrier_space_declared",
        "PASS_CARRIER_SPACE_DECLARED" if carrier_ok else "FAIL_CARRIER_SPACE",
        "candidate carrier is the declared CMB role-space candidate",
        carrier_ok,
        "equivalence relation requires a declared carrier/codomain",
    ))

    relation_ok = (
        "readout_equivalence_relation" in by_component
        and "~_{R_CMB,seed}" in by_component["readout_equivalence_relation"].get("formal_object", "")
        and by_component["readout_equivalence_relation"].get("candidate_status") == "DECLARED_RELATION_NOT_PROVED"
    )
    rows.append(audit_row(
        "relation_symbol_declared",
        "PASS_RELATION_SYMBOL_DECLARED" if relation_ok else "FAIL_RELATION_SYMBOL",
        "relation symbol is declared and explicitly marked unproved",
        relation_ok,
        "relation must be named before axiom audit",
    ))

    controls_text = by_component.get("readout_equivalence_relation", {}).get("candidate_definition", "")
    controls_ok = all(token in controls_text for token in ["null", "gauge", "convention", "endpoint-blind"])
    rows.append(audit_row(
        "control_family_declared",
        "PASS_CONTROL_FAMILY_DECLARED" if controls_ok else "FAIL_CONTROL_FAMILY",
        "null, gauge, convention, and endpoint-blind controls are named",
        controls_ok,
        "relation must state the controls it quotients by",
    ))

    null_anchor_ok = (
        "null_readout_anchor" in by_component
        and "null_readout" in by_component["null_readout_anchor"].get("formal_object", "")
    )
    rows.append(audit_row(
        "null_anchor_compatibility",
        "PASS_NULL_ANCHOR_AVAILABLE" if null_anchor_ok else "FAIL_NULL_ANCHOR_COMPATIBILITY",
        "null anchor is available for future null-class compatibility",
        null_anchor_ok,
        "equivalence relation needs a null anchor before null-class tests",
    ))

    permissions_closed = (
        all(row.get("allows_equivalence_proof") == "false" for row in relation_rows)
        and all(row.get("allows_survival_claim") == "false" for row in relation_rows)
        and all(row.get("allows_score_entry") == "false" for row in relation_rows)
        and relation_audit.get("equivalence_proof_allowed") is False
        and relation_audit.get("quotient_survival_claim_allowed") is False
        and relation_audit.get("score_entry_allowed") is False
    )
    rows.append(audit_row(
        "promotion_firewall",
        "PASS_EQUIVALENCE_FIREWALL_CLOSED" if permissions_closed else "FAIL_EQUIVALENCE_FIREWALL",
        "equivalence proof, survival claim, score, and verdict permissions remain closed",
        permissions_closed,
        "axiom audit must not promote the candidate to a proof or score",
    ))

    rows.append(audit_row(
        "reflexivity",
        "BLOCKED_REFLEXIVITY_NOT_PROVED",
        "no formal predicate/control identity proof shows x ~ x on the carrier",
        False,
        "requires a concrete carrier predicate and identity-preserving control list",
    ))
    rows.append(audit_row(
        "symmetry",
        "BLOCKED_SYMMETRY_NOT_PROVED",
        "no formal predicate/control symmetry proof shows x ~ y implies y ~ x",
        False,
        "requires symmetric indistinguishability or a symmetric metric/tolerance rule",
    ))
    rows.append(audit_row(
        "transitivity",
        "BLOCKED_TRANSITIVITY_NOT_PROVED",
        "no formal predicate/control transitivity proof shows x ~ y and y ~ z imply x ~ z",
        False,
        "requires transitive controls or quotient-safe closure of the tolerance rule",
    ))
    rows.append(audit_row(
        "quotient_well_definedness",
        "BLOCKED_QUOTIENT_MAP_NOT_DEFINED",
        "quotient classes cannot be accepted until the equivalence axioms and carrier map are proved",
        False,
        "requires proved equivalence relation plus concrete quotient map",
    ))

    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(item["audit_passed"]) for item in rows)
    blocked = sum(item["audit_status"].startswith("BLOCKED") for item in rows)
    failed = sum(item["audit_status"].startswith("FAIL") for item in rows)
    return {
        "report_id": "tau_cmb_seed_readout_equivalence_relation_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_relation_table": rel(RELATION_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "equivalence_relation_audited": True,
        "equivalence_relation_proved": False,
        "quotient_map_allowed": False,
        "quotient_survival_claim_allowed": False,
        "readout_evaluation_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "SEED_READOUT_EQUIVALENCE_RELATION_AUDITED_BLOCKED_NOT_PROVED",
        "next_minimal_unblock": "tau_cmb_seed_readout_equivalence_axiom_proof_obligation_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{item['component']}`: {item['audit_status']} | {item['finding']}"
        for item in report["audit_rows"]
    )
    text = f"""# Tau CMB Seed Readout Equivalence Relation Audit v01

**Doc class:** readout equivalence relation axiom audit
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks whether the declared `~_{{R_CMB,seed}}` relation is ready to
serve as an equivalence relation for quotienting the CMB seed readout. It does
not prove the equivalence relation, define a quotient map, evaluate `R_CMB`,
prove survival, enter scoring, or decide the dark-sector question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The relation is audit-visible but not proved. Reflexivity, symmetry,
transitivity, and quotient well-definedness remain blocked until a concrete
carrier predicate, control list, and quotient-safe rule are supplied.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB seed readout equivalence relation.")
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
