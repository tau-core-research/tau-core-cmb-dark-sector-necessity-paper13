#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_seed_chain_pre_acceptance_gate_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_seed_chain_pre_acceptance_gate_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_seed_chain_pre_acceptance_gate_v01.md"

SUPPORT_AUDIT = ROOT / "data/derived/tau_cmb_seed_support_domain_rule_candidate_audit_v01.json"
NORMALIZATION_AUDIT = ROOT / "data/derived/tau_cmb_seed_normalization_replay_candidate_audit_v01.json"
ZERO_CONTROL_AUDIT = ROOT / "data/derived/tau_cmb_seed_zero_control_audit_v01.json"

CLAIM_BOUNDARY = (
    "tau_cmb_seed_chain_pre_acceptance_gate_v01_pre_acceptance_only_"
    "clean_audit_chain_not_accepted_no_domain_certificate_no_concrete_R_CMB_no_quotient_no_score_no_verdict"
)

FIELDS = [
    "gate_row_id",
    "input_artifact",
    "required_status",
    "observed_status",
    "failed_rows",
    "passed_rows",
    "blocked_rows",
    "gate_result",
    "blocking_reason",
    "allows_chain_pre_acceptance",
    "allows_domain_certificate",
    "allows_concrete_readout",
    "allows_quotient_survival",
    "allows_score_entry",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

AUDITS = [
    {
        "input_artifact": SUPPORT_AUDIT,
        "required_status": "SEED_SUPPORT_DOMAIN_RULE_CANDIDATE_AUDITED_BLOCKED_NOT_CERTIFIED",
        "blocking_reason": "support rule is audited without failures, but support certification remains closed",
    },
    {
        "input_artifact": NORMALIZATION_AUDIT,
        "required_status": "SEED_NORMALIZATION_REPLAY_CANDIDATE_AUDITED_BLOCKED_NOT_ACCEPTED",
        "blocking_reason": "normalization replay is audited without failures, but normalization acceptance remains closed",
    },
    {
        "input_artifact": ZERO_CONTROL_AUDIT,
        "required_status": "SEED_ZERO_CONTROL_AUDITED_BLOCKED_NOT_ACCEPTED",
        "blocking_reason": "zero-control is audited without failures, but concrete R_CMB and quotient relation remain missing",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, item in enumerate(AUDITS, start=1):
        path = item["input_artifact"]
        if not path.exists():
            observed_status = "MISSING"
            failed_rows = "n/a"
            passed_rows = "n/a"
            blocked_rows = "n/a"
            clean = False
            result = "FAIL_REQUIRED_AUDIT_MISSING"
            blocking_reason = f"required audit artifact is absent: {rel(path)}"
        else:
            report = load_json(path)
            observed_status = str(report.get("status"))
            failed_rows = str(report.get("failed_rows", "n/a"))
            passed_rows = str(report.get("passed_rows", "n/a"))
            blocked_rows = str(report.get("blocked_rows", "n/a"))
            clean = observed_status == item["required_status"] and report.get("failed_rows") == 0
            result = "PASS_CLEAN_BLOCKED_AUDIT_INPUT" if clean else "FAIL_AUDIT_INPUT_NOT_CLEAN"
            blocking_reason = item["blocking_reason"] if clean else "audit status or failed-row count does not match gate requirement"
        rows.append(
            {
                "gate_row_id": f"TCMBSCPAG01_{index:03d}",
                "input_artifact": rel(path),
                "required_status": item["required_status"],
                "observed_status": observed_status,
                "failed_rows": failed_rows,
                "passed_rows": passed_rows,
                "blocked_rows": blocked_rows,
                "gate_result": result,
                "blocking_reason": blocking_reason,
                "allows_chain_pre_acceptance": "true" if clean else "false",
                "allows_domain_certificate": "false",
                "allows_concrete_readout": "false",
                "allows_quotient_survival": "false",
                "allows_score_entry": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def write_table(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_summary(table_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    all_clean = all(row["gate_result"] == "PASS_CLEAN_BLOCKED_AUDIT_INPUT" for row in rows)
    failed = sum(row["gate_result"].startswith("FAIL") for row in rows)
    passed = sum(row["gate_result"].startswith("PASS") for row in rows)
    return {
        "report_id": "tau_cmb_seed_chain_pre_acceptance_gate_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "gate_rows": len(rows),
        "passed_rows": passed,
        "failed_rows": failed,
        "seed_chain_audit_clean": all_clean,
        "chain_pre_acceptance_allowed": all_clean,
        "domain_certificate_allowed": False,
        "concrete_R_CMB_allowed": False,
        "quotient_survival_allowed": False,
        "readout_evaluation_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "SEED_CHAIN_PRE_ACCEPTANCE_GATE_CLEAN_BLOCKED_ON_READOUT_QUOTIENT"
            if all_clean
            else "SEED_CHAIN_PRE_ACCEPTANCE_GATE_FAILED_INPUT_AUDIT"
        ),
        "next_minimal_unblock": (
            "tau_cmb_seed_readout_quotient_relation_candidate_v01"
            if all_clean
            else "repair_failed_seed_pre_acceptance_input_audit"
        ),
        "remaining_blockers": [
            "concrete_R_CMB_missing",
            "quotient_equivalence_relation_missing",
            "domain_certificate_acceptance_missing",
            "score_entry_closed",
        ],
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['gate_row_id']}` `{row['input_artifact']}`: {row['gate_result']} | {row['observed_status']}"
        for row in rows
    )
    blockers = "\n".join(f"- `{blocker}`" for blocker in summary["remaining_blockers"])
    text = f"""# Tau CMB Seed Chain Pre-Acceptance Gate v01

**Doc class:** seed-chain pre-acceptance gate
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This gate checks whether the seed support-domain rule audit, normalization
replay audit, and zero-control audit form a clean candidate chain. It does not
accept the seed, certify a domain, define concrete `R_CMB`, prove quotient
survival, enter scoring, or decide the dark-sector question.

## Gate Rows

{row_text}

## Decision

```text
seed_chain_audit_clean = {str(summary["seed_chain_audit_clean"]).lower()}
chain_pre_acceptance_allowed = {str(summary["chain_pre_acceptance_allowed"]).lower()}
status = {summary["status"]}
```

The chain is clean at audit level when all required input audits have zero
failed rows and the expected non-accepted/non-certified status. This is only a
pre-acceptance condition. It does not remove the readout/quotient blockers.

## Remaining Blockers

{blockers}

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB seed chain pre-acceptance gate.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = build_rows()
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
