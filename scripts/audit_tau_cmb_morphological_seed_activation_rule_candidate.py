#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CANDIDATE = ROOT / "data/derived/tau_cmb_morphological_seed_activation_rule_candidate_v01.csv"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_morphological_seed_activation_rule_candidate_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_morphological_seed_activation_rule_candidate_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_morphological_seed_activation_rule_candidate_audit_v01_audit_only_"
    "no_activation_acceptance_no_A_tau_value_no_source_acceptance_no_phi_derivation_no_score_no_verdict"
)

REQUIRED_COLUMNS = {
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
}

REQUIRED_COMPONENTS = {
    "activation_domain",
    "conditional_activation_map",
    "zero_seed_limit",
    "endpoint_blindness_constraint",
    "spine_binding",
}

FORBIDDEN_ENDPOINT_TOKENS = [
    "ACT RESIDUAL",
    "PLANCK RESIDUAL",
    "CMB ROLE SCORE",
    "LIKELIHOOD DELTA",
    "SCORE DELTA",
    "TARGET SHAPE",
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def endpoint_hits(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for row in rows:
        if row.get("rule_component") == "endpoint_blindness_constraint":
            continue
        blob = " ".join(str(value).upper().replace("_", " ") for value in row.values())
        for token in FORBIDDEN_ENDPOINT_TOKENS:
            if token in blob:
                hits.append({"rule_row_id": row.get("rule_row_id", ""), "token": token})
    return hits


def build_report(candidate_path: Path) -> dict[str, Any]:
    columns, rows = read_csv(candidate_path)
    components = {row.get("rule_component", "") for row in rows}
    missing_columns = sorted(REQUIRED_COLUMNS - set(columns))
    missing_components = sorted(REQUIRED_COMPONENTS - components)
    extra_components = sorted(component for component in components - REQUIRED_COMPONENTS if component)
    self_acceptance_rows: list[str] = []
    missing_blocker_rows: list[str] = []
    incomplete_boundary_rows: list[str] = []
    value_claim_rows: list[str] = []

    if not candidate_path.exists():
        status = "MORPHOLOGICAL_SEED_ACTIVATION_RULE_AUDIT_BLOCKED_NO_CANDIDATE"
        decision = "DO_NOT_ROUTE_NO_CANDIDATE"
    else:
        for row in rows:
            row_id = row.get("rule_row_id", "")
            if any(row.get(flag) != "false" for flag in [
                "allows_activation_acceptance",
                "allows_A_tau_value",
                "allows_source_acceptance",
                "allows_score_entry",
            ]):
                self_acceptance_rows.append(row_id)
            if not row.get("acceptance_blocker", "").strip():
                missing_blocker_rows.append(row_id)
            if "no_activation_proof" not in row.get("claim_boundary", ""):
                incomplete_boundary_rows.append(row_id)
            text = " ".join(str(row.get(field, "")) for field in ["formal_object", "candidate_rule_text", "current_status"])
            if "A_tau(" in text and "candidate" not in text and "value" in text.lower():
                value_claim_rows.append(row_id)
        hits = endpoint_hits(rows)
        if missing_columns or missing_components or extra_components:
            status = "MORPHOLOGICAL_SEED_ACTIVATION_RULE_AUDIT_REJECTED_SCHEMA_MISMATCH"
            decision = "DO_NOT_ROUTE_SCHEMA_MISMATCH"
        elif hits:
            status = "MORPHOLOGICAL_SEED_ACTIVATION_RULE_AUDIT_REJECTED_ENDPOINT_TOKEN_HIT"
            decision = "DO_NOT_ROUTE_ENDPOINT_LEAKAGE_RISK"
        elif self_acceptance_rows or incomplete_boundary_rows or value_claim_rows:
            status = "MORPHOLOGICAL_SEED_ACTIVATION_RULE_AUDIT_REJECTED_CLAIM_BOUNDARY_FAILURE"
            decision = "DO_NOT_ROUTE_CLAIM_BOUNDARY_FAILURE"
        elif missing_blocker_rows:
            status = "MORPHOLOGICAL_SEED_ACTIVATION_RULE_AUDIT_REJECTED_BLOCKERS_MISSING"
            decision = "DO_NOT_ROUTE_BLOCKERS_MISSING"
        else:
            status = "MORPHOLOGICAL_SEED_ACTIVATION_RULE_AUDIT_READY_FOR_QUOTIENT_SURVIVAL_TEST"
            decision = "ROUTE_TO_QUOTIENT_SURVIVAL_TEST_NOT_ACCEPTED"

    hits = endpoint_hits(rows)
    return {
        "report_id": "tau_cmb_morphological_seed_activation_rule_candidate_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_candidate": rel(candidate_path),
        "status": status,
        "decision": decision,
        "rows_received": len(rows),
        "missing_required_columns": missing_columns,
        "missing_components": missing_components,
        "extra_components": extra_components,
        "endpoint_token_hits": hits,
        "self_acceptance_rows": sorted(self_acceptance_rows),
        "missing_blocker_rows": sorted(missing_blocker_rows),
        "incomplete_boundary_rows": sorted(incomplete_boundary_rows),
        "value_claim_rows": sorted(value_claim_rows),
        "activation_acceptance_allowed": False,
        "A_tau_value_allowed": False,
        "source_acceptance_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "next_minimal_unblock": "build_tau_cmb_morphological_seed_quotient_survival_test_v01",
    }


def write_doc(report: dict[str, Any], path: Path) -> None:
    def bullet(values: list[Any]) -> str:
        return "\n".join(f"- `{value}`" for value in values) or "- none"

    text = f"""# Tau CMB Morphological Seed Activation Rule Candidate Audit v01

**Doc class:** activation-rule candidate audit
**Status:** {report["status"]}
**Decision:** {report["decision"]}

## Claim Boundary

```text
{report["claim_boundary"]}
```

## Audited Candidate

```text
{report["audited_candidate"]}
```

## Audit Result

```text
{report["decision"]}
```

This audit does not accept an activation rule and does not supply `A_tau(a,k)`.
It only decides whether the rule candidate is clean enough to route to a
quotient/null survival test.

## Missing Columns

{bullet(report["missing_required_columns"])}

## Missing Components

{bullet(report["missing_components"])}

## Endpoint Token Hits

{bullet([f"{hit['rule_row_id']}:{hit['token']}" for hit in report["endpoint_token_hits"]])}

## Claim Boundary Problems

Self-acceptance rows:

{bullet(report["self_acceptance_rows"])}

Incomplete boundary rows:

{bullet(report["incomplete_boundary_rows"])}

Value-claim rows:

{bullet(report["value_claim_rows"])}

## Missing Blocker Rows

{bullet(report["missing_blocker_rows"])}

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB morphological seed activation rule candidate.")
    parser.add_argument("--candidate", default=str(DEFAULT_CANDIDATE))
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    report = build_report(Path(args.candidate))
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(report, Path(args.write_doc))
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
