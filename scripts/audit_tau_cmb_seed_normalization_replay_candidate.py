#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
NORMALIZATION_TABLE = ROOT / "data/derived/tau_cmb_seed_normalization_replay_candidate_v01.csv"
NORMALIZATION_REPLAY = ROOT / "payloads/seed_tau_normalization_replay_candidate_v01.txt"
PAYLOAD = ROOT / "payloads/seed_tau_payload_candidate_v01.csv"
FIREWALL = ROOT / "payloads/seed_tau_payload_candidate_v01.firewall.json"
SUPPORT_AUDIT = ROOT / "data/derived/tau_cmb_seed_support_domain_rule_candidate_audit_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_seed_normalization_replay_candidate_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_seed_normalization_replay_candidate_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_seed_normalization_replay_candidate_audit_v01_audit_only_"
    "normalization_not_accepted_no_support_certification_no_domain_certificate_no_readout_no_score_no_verdict"
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
    required = [NORMALIZATION_TABLE, NORMALIZATION_REPLAY, PAYLOAD, FIREWALL, SUPPORT_AUDIT]
    missing = [path for path in required if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    norm_rows = read_csv(NORMALIZATION_TABLE)
    payload_rows = read_csv(PAYLOAD)
    firewall = load_json(FIREWALL)
    support_audit = load_json(SUPPORT_AUDIT)
    replay_text = NORMALIZATION_REPLAY.read_text(encoding="utf-8")
    payload = payload_rows[0] if payload_rows else {}

    expected_components = [
        "normalization_input_tuple",
        "scale_label_canonicalization",
        "normalized_seed_descriptor",
        "forbidden_operations",
        "zero_control_dependency",
    ]
    components = [item.get("component") for item in norm_rows]
    rows.append(
        audit_row(
            "normalization_table_shape",
            "PASS_NORMALIZATION_ROWS_PRESENT" if components == expected_components else "FAIL_NORMALIZATION_ROW_SHAPE",
            f"components={components}",
            components == expected_components,
            "normalization audit requires the five declared candidate rows",
        )
    )

    mapping_ok = (
        "CMB_readout_sector_scale_label_candidate_not_normalized" in replay_text
        and "CMB_readout_sector_scale_label_canonical_v01" in replay_text
        and any(
            item.get("input_object") == "CMB_readout_sector_scale_label_candidate_not_normalized"
            and item.get("output_object") == "CMB_readout_sector_scale_label_canonical_v01"
            for item in norm_rows
        )
    )
    rows.append(
        audit_row(
            "canonical_mapping",
            "PASS_CANONICAL_MAPPING_DECLARED" if mapping_ok else "FAIL_CANONICAL_MAPPING",
            "candidate_not_normalized -> canonical_v01 mapping is present in table and replay",
            mapping_ok,
            "canonical scale mapping must be explicit before support certification",
        )
    )

    tuple_fixed_ok = (
        payload.get("tau_side_descriptor") in replay_text
        and payload.get("support_coordinate") in replay_text
        and "keeps morphology_class and readout_sector fixed" in replay_text
    )
    rows.append(
        audit_row(
            "tuple_invariance",
            "PASS_TUPLE_INVARIANCE_DECLARED" if tuple_fixed_ok else "FAIL_TUPLE_INVARIANCE",
            "replay keeps morphology class and readout sector fixed",
            tuple_fixed_ok,
            "normalization cannot redefine support coordinates",
        )
    )

    endpoint_ok = (
        firewall.get("endpoint_inputs_used") == []
        and "No CMB residuals" in replay_text
        and "score outputs" in replay_text
    )
    rows.append(
        audit_row(
            "endpoint_boundary",
            "PASS_ENDPOINT_BOUNDARY_DECLARED" if endpoint_ok else "FAIL_ENDPOINT_BOUNDARY",
            "firewall endpoint_inputs_used=[] and replay forbids endpoint inputs",
            endpoint_ok,
            "normalization replay must not use endpoint data",
        )
    )

    support_dependency_ok = (
        support_audit.get("status") == "SEED_SUPPORT_DOMAIN_RULE_CANDIDATE_AUDITED_BLOCKED_NOT_CERTIFIED"
        and support_audit.get("failed_rows") == 0
    )
    rows.append(
        audit_row(
            "support_rule_dependency",
            "PASS_SUPPORT_RULE_AUDITED_AS_CANDIDATE" if support_dependency_ok else "FAIL_SUPPORT_RULE_DEPENDENCY",
            "support rule candidate audit has zero failures but remains uncertified",
            support_dependency_ok,
            "normalization can reference support candidate but cannot certify support",
        )
    )

    zero_control_missing = any(item.get("component") == "zero_control_dependency" for item in norm_rows)
    rows.append(
        audit_row(
            "zero_control_dependency",
            "BLOCKED_ZERO_CONTROL_NOT_DEFINED" if zero_control_missing else "FAIL_ZERO_CONTROL_DEPENDENCY_MISSING",
            "normalization correctly declares same-scale zero-control dependency",
            False,
            "zero-control must be defined before quotient survival or domain certificate",
        )
    )

    acceptance_closed = all(item.get("allows_normalization_acceptance") == "false" for item in norm_rows)
    rows.append(
        audit_row(
            "normalization_acceptance",
            "BLOCKED_NORMALIZATION_ACCEPTANCE_CLOSED" if acceptance_closed else "FAIL_ACCEPTANCE_PERMISSION_OPEN",
            "normalization candidate keeps acceptance permissions closed",
            False,
            "normalization acceptance requires a separate acceptance gate after zero-control",
        )
    )

    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(item["audit_passed"]) for item in rows)
    blocked = sum(item["audit_status"].startswith("BLOCKED") for item in rows)
    failed = sum(item["audit_status"].startswith("FAIL") for item in rows)
    return {
        "report_id": "tau_cmb_seed_normalization_replay_candidate_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_normalization_table": rel(NORMALIZATION_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "normalization_replay_candidate_audited": True,
        "normalization_acceptance_allowed": False,
        "support_certification_allowed": False,
        "domain_certificate_allowed": False,
        "readout_evaluation_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "SEED_NORMALIZATION_REPLAY_CANDIDATE_AUDITED_BLOCKED_NOT_ACCEPTED",
        "next_minimal_unblock": "tau_cmb_seed_zero_control_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{item['component']}`: {item['audit_status']} | {item['finding']}"
        for item in report["audit_rows"]
    )
    text = f"""# Tau CMB Seed Normalization Replay Candidate Audit v01

**Doc class:** seed normalization replay candidate audit
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks whether the seed normalization replay candidate is
deterministic, endpoint-blind, and compatible with the support-domain rule
candidate. It does not accept normalization, certify support, certify domain
membership, evaluate readout survival, assign `A_tau(a,k)`, enter scoring, or
decide the dark-sector question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The normalization replay is now audited as a candidate, but acceptance remains
blocked because zero-control is not defined and normalization acceptance is a
separate later gate.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB seed normalization replay candidate.")
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
