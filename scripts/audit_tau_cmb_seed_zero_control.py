#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ZERO_TABLE = ROOT / "data/derived/tau_cmb_seed_zero_control_v01.csv"
ZERO_REPLAY = ROOT / "payloads/seed_tau_zero_control_v01.replay.txt"
NORMALIZATION_AUDIT = ROOT / "data/derived/tau_cmb_seed_normalization_replay_candidate_audit_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_seed_zero_control_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_seed_zero_control_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_seed_zero_control_audit_v01_audit_only_"
    "zero_control_not_accepted_no_physical_response_no_domain_certificate_no_readout_no_score_no_verdict"
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
    required = [ZERO_TABLE, ZERO_REPLAY, NORMALIZATION_AUDIT]
    missing = [path for path in required if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    zero_rows = read_csv(ZERO_TABLE)
    replay_text = ZERO_REPLAY.read_text(encoding="utf-8")
    norm_audit = load_json(NORMALIZATION_AUDIT)
    components = [item.get("component") for item in zero_rows]
    expected = [
        "null_seed_definition",
        "same_domain_convention",
        "inactive_activation",
        "null_readout_role",
        "forbidden_promotion",
        "quotient_survival_dependency",
    ]
    rows.append(audit_row(
        "zero_table_shape",
        "PASS_ZERO_ROWS_PRESENT" if components == expected else "FAIL_ZERO_ROW_SHAPE",
        f"components={components}",
        components == expected,
        "zero-control audit requires the six declared rows",
    ))

    tuple_ok = (
        "null_morphology_control" in replay_text
        and "CMB_readout_sector" in replay_text
        and "CMB_readout_sector_scale_label_canonical_v01" in replay_text
    )
    rows.append(audit_row(
        "null_seed_tuple",
        "PASS_NULL_SEED_TUPLE_DECLARED" if tuple_ok else "FAIL_NULL_SEED_TUPLE",
        "null seed uses null morphology, CMB readout sector, and canonical scale",
        tuple_ok,
        "null_seed must use the same canonical scale convention",
    ))

    norm_ok = norm_audit.get("failed_rows") == 0 and norm_audit.get("status") == "SEED_NORMALIZATION_REPLAY_CANDIDATE_AUDITED_BLOCKED_NOT_ACCEPTED"
    rows.append(audit_row(
        "normalization_dependency",
        "PASS_NORMALIZATION_AUDITED_AS_CANDIDATE" if norm_ok else "FAIL_NORMALIZATION_DEPENDENCY",
        "normalization replay audit has zero failures and remains non-accepted",
        norm_ok,
        "zero-control can reference normalization candidate but cannot accept normalization",
    ))

    inactive_ok = "Act_tau_CMB[null_seed_tau_CMB](a,k) := 0 or inactive" in replay_text
    rows.append(audit_row(
        "inactive_activation",
        "PASS_INACTIVE_ACTIVATION_DECLARED" if inactive_ok else "FAIL_INACTIVE_ACTIVATION",
        "null seed activation is declared zero or inactive",
        inactive_ok,
        "null seed must not create A_tau_candidate",
    ))

    readout_ok = "R_CMB(null_seed_tau_CMB) := null_readout" in replay_text
    rows.append(audit_row(
        "null_readout_role",
        "PASS_NULL_READOUT_DECLARED" if readout_ok else "FAIL_NULL_READOUT",
        "null seed readout role is declared as null_readout",
        readout_ok,
        "null readout is needed as later quotient/null reference",
    ))

    forbidden_ok = (
        "not a physical Tau response" in replay_text
        and "not a dark" in replay_text
        and "not a score input" in replay_text
        and all(item.get("allows_physical_response_claim") == "false" for item in zero_rows)
        and all(item.get("allows_score_entry") == "false" for item in zero_rows)
    )
    rows.append(audit_row(
        "forbidden_promotion",
        "PASS_PROMOTION_FORBIDDEN" if forbidden_ok else "FAIL_PROMOTION_BOUNDARY",
        "zero-control cannot be promoted to physical response, dark-sector claim, or score input",
        forbidden_ok,
        "control object must remain non-physical and non-scoring",
    ))

    quotient_block = any(item.get("component") == "quotient_survival_dependency" for item in zero_rows)
    rows.append(audit_row(
        "quotient_survival_dependency",
        "BLOCKED_QUOTIENT_RELATION_NOT_DEFINED" if quotient_block else "FAIL_QUOTIENT_DEPENDENCY_MISSING",
        "zero-control supplies null side, but concrete R_CMB and equivalence relation are missing",
        False,
        "quotient survival still requires concrete readout and equivalence relation",
    ))

    acceptance_closed = all(item.get("allows_zero_control_acceptance") == "false" for item in zero_rows)
    rows.append(audit_row(
        "zero_control_acceptance",
        "BLOCKED_ZERO_CONTROL_ACCEPTANCE_CLOSED" if acceptance_closed else "FAIL_ZERO_ACCEPTANCE_OPEN",
        "zero-control candidate keeps acceptance permissions closed",
        False,
        "zero-control acceptance requires a later explicit acceptance gate",
    ))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(item["audit_passed"]) for item in rows)
    blocked = sum(item["audit_status"].startswith("BLOCKED") for item in rows)
    failed = sum(item["audit_status"].startswith("FAIL") for item in rows)
    return {
        "report_id": "tau_cmb_seed_zero_control_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_zero_table": rel(ZERO_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "zero_control_audited": True,
        "zero_control_acceptance_allowed": False,
        "physical_response_claim_allowed": False,
        "domain_certificate_allowed": False,
        "readout_evaluation_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "SEED_ZERO_CONTROL_AUDITED_BLOCKED_NOT_ACCEPTED",
        "next_minimal_unblock": "tau_cmb_seed_chain_pre_acceptance_gate_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{item['component']}`: {item['audit_status']} | {item['finding']}"
        for item in report["audit_rows"]
    )
    text = f"""# Tau CMB Seed Zero Control Audit v01

**Doc class:** zero-control audit
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks whether the zero-control candidate is a same-convention,
inactive, null-readout control object and whether physical/scoring promotion is
forbidden. It does not accept zero-control, certify domain membership, evaluate
readout survival, assign `A_tau(a,k)`, enter scoring, or decide the dark-sector
question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The zero-control side is now audited as a candidate. Acceptance remains closed
because quotient survival still needs concrete `R_CMB`, an equivalence relation,
and a separate pre-acceptance gate.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB seed zero-control candidate.")
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
