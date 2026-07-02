#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CANDIDATE = ROOT / "payloads/tau_cmb_parent_source_freeze_packet_submission_candidate_v01.csv"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_parent_source_freeze_packet_submission_candidate_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_parent_source_freeze_packet_submission_candidate_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_parent_source_freeze_packet_submission_candidate_audit_v01_audit_only_"
    "no_source_acceptance_no_phi_derivation_no_score_no_verdict"
)

REQUIRED_COLUMNS = {
    "freeze_row_id",
    "freeze_component",
    "required_payload_field",
    "payload_value",
    "unit_or_dimension_status",
    "source_provenance",
    "replay_rule_or_command",
    "artifact_hash",
    "endpoint_exclusion_statement",
    "review_status",
    "acceptance_status",
    "notes",
}

REQUIRED_ROWS = {
    "TCMBPSF01_001",
    "TCMBPSF01_002",
    "TCMBPSF01_003",
    "TCMBPSF01_004",
    "TCMBPSF01_005",
    "TCMBPSF01_006",
    "TCMBPSF01_007",
}

UNSUPPLIED = "UNSUPPLIED_ENDPOINT_BLIND_VALUE"
FORBIDDEN_TOKENS = [
    "ACT_RESIDUAL",
    "PLANCK_RESIDUAL",
    "CMB_ROLE_SCORE",
    "FIT_IMPROVEMENT",
    "POST_HOC_SOURCE",
    "LIKELIHOOD_DELTA",
    "TARGET_SHAPE",
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def stable_row_hash(row: dict[str, str]) -> str:
    hash_row = {key: value for key, value in row.items() if key != "artifact_hash"}
    payload = json.dumps(hash_row, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def endpoint_hits(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for row in rows:
        blob = " ".join(str(value).upper() for value in row.values())
        for token in FORBIDDEN_TOKENS:
            if token in blob:
                hits.append({"freeze_row_id": row.get("freeze_row_id", ""), "token": token})
    return hits


def build_report(candidate_path: Path) -> dict[str, Any]:
    columns, rows = read_csv(candidate_path)
    supplied_ids = {row.get("freeze_row_id", "") for row in rows}
    missing_columns = sorted(REQUIRED_COLUMNS - set(columns))
    missing_rows = sorted(REQUIRED_ROWS - supplied_ids)
    extra_rows = sorted(row_id for row_id in supplied_ids - REQUIRED_ROWS if row_id)
    missing_hash_rows: list[str] = []
    hash_mismatch_rows: list[str] = []
    unsupplied_rows: list[str] = []
    accepted_rows: list[str] = []

    if not candidate_path.exists():
        status = "PARENT_SOURCE_FREEZE_PACKET_AUDIT_BLOCKED_NO_CANDIDATE"
        decision = "DO_NOT_ACCEPT_NO_CANDIDATE"
    else:
        for row in rows:
            row_id = row.get("freeze_row_id", "")
            if not row.get("artifact_hash"):
                missing_hash_rows.append(row_id)
            elif row.get("artifact_hash") != stable_row_hash(row):
                hash_mismatch_rows.append(row_id)
            if row.get("payload_value") == UNSUPPLIED:
                unsupplied_rows.append(row_id)
            if row.get("acceptance_status", "").startswith("ACCEPTED"):
                accepted_rows.append(row_id)
        hits = endpoint_hits(rows)
        if missing_columns or missing_rows or extra_rows:
            status = "PARENT_SOURCE_FREEZE_PACKET_AUDIT_REJECTED_SCHEMA_MISMATCH"
            decision = "DO_NOT_ACCEPT_SCHEMA_MISMATCH"
        elif missing_hash_rows or hash_mismatch_rows:
            status = "PARENT_SOURCE_FREEZE_PACKET_AUDIT_REJECTED_HASH_FAILURE"
            decision = "DO_NOT_ACCEPT_HASH_FAILURE"
        elif hits:
            status = "PARENT_SOURCE_FREEZE_PACKET_AUDIT_REJECTED_ENDPOINT_TOKEN_HIT"
            decision = "DO_NOT_ACCEPT_ENDPOINT_LEAKAGE_RISK"
        elif unsupplied_rows:
            status = "PARENT_SOURCE_FREEZE_PACKET_AUDIT_REJECTED_NO_POPULATED_SOURCE_VALUES"
            decision = "DO_NOT_ACCEPT_NO_POPULATED_SOURCE_VALUES"
        elif accepted_rows:
            status = "PARENT_SOURCE_FREEZE_PACKET_AUDIT_BLOCKED_SELF_ACCEPTED_ROWS"
            decision = "DO_NOT_ACCEPT_SELF_ACCEPTED_PAYLOAD_WITHOUT_INDEPENDENT_AUDIT"
        else:
            status = "PARENT_SOURCE_FREEZE_PACKET_AUDIT_READY_FOR_CONTENT_AUDIT"
            decision = "ROUTE_TO_CONTENT_AUDIT_NOT_SCORE"

    hits = endpoint_hits(rows)
    return {
        "report_id": "tau_cmb_parent_source_freeze_packet_submission_candidate_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_candidate": rel(candidate_path),
        "status": status,
        "decision": decision,
        "rows_received": len(rows),
        "required_rows": sorted(REQUIRED_ROWS),
        "missing_required_columns": missing_columns,
        "missing_rows": missing_rows,
        "extra_rows": extra_rows,
        "missing_hash_rows": sorted(missing_hash_rows),
        "hash_mismatch_rows": sorted(hash_mismatch_rows),
        "unsupplied_payload_rows": sorted(unsupplied_rows),
        "accepted_rows_in_candidate": sorted(accepted_rows),
        "endpoint_token_hits": hits,
        "source_acceptance_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "next_minimal_unblock": "provide_real_endpoint_blind_parent_source_values_or_record_explicit_source_unavailability",
    }


def write_doc(report: dict[str, Any], path: Path) -> None:
    def bullet(values: list[Any]) -> str:
        return "\n".join(f"- `{value}`" for value in values) or "- none"

    text = f"""# Tau CMB Parent-Source Freeze Packet Submission Candidate Audit v01

**Doc class:** freeze-packet submission candidate audit
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

The candidate is not source-accepted. It may not be used to derive
`Phi_tau_eff`, open scoring, or support a dark-sector verdict.

## Missing Columns

{bullet(report["missing_required_columns"])}

## Missing Rows

{bullet(report["missing_rows"])}

## Hash Problems

Missing hash rows:

{bullet(report["missing_hash_rows"])}

Hash mismatch rows:

{bullet(report["hash_mismatch_rows"])}

## Unsupplied Payload Rows

{bullet(report["unsupplied_payload_rows"])}

## Endpoint Token Hits

{bullet([f"{hit['freeze_row_id']}:{hit['token']}" for hit in report["endpoint_token_hits"]])}

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB parent-source freeze packet submission candidate.")
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
