#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUBMISSION = ROOT / "payloads/cmb_tau_lensing_endpoint_blind_operator_packet_submission_v01.csv"
ROUTER = ROOT / "data/derived/cmb_tau_lensing_endpoint_blind_operator_packet_content_audit_router_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/cmb_tau_lensing_endpoint_blind_operator_packet_content_audit_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/cmb_tau_lensing_endpoint_blind_operator_packet_content_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_endpoint_blind_operator_packet_content_audit_v01.md"


FIELDNAMES = [
    "audit_row_id",
    "packet_slot",
    "content_audit_status",
    "audit_result",
    "acceptance_effect",
    "remaining_blocker",
    "evidence_artifact",
    "provenance_hash",
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def classify(row: dict[str, str]) -> tuple[str, str, str, str]:
    slot = row["packet_slot"]
    joined = " ".join(
        row.get(key, "")
        for key in [
            "supplied_object",
            "dimension_status",
            "zero_source_status",
            "replay_status",
            "firewall_status",
            "notes",
        ]
    )
    if slot in {"kernel_measure", "normalization", "dimension_sign_audit", "post_population_firewall"}:
        return (
            "CONTENT_AUDIT_BLOCKED_REQUIRED_OPERATOR_COMPONENT_MISSING",
            "blocked",
            "blocks_physical_operator_acceptance",
            row.get("notes", "required component is blocked"),
        )
    if slot == "output_replay" and "not the physical Phi_lens_tau-to-PP operator" in joined:
        return (
            "CONTENT_AUDIT_PARTIAL_REPLAY_NOT_OPERATOR_ACCEPTANCE",
            "partial",
            "does_not_unblock_physical_score",
            "candidate grid replay exists but depends on unaccepted L-space candidate and lacks post-population firewall",
        )
    if slot == "zero_source_limit" and "not full operator proof" in joined:
        return (
            "CONTENT_AUDIT_PARTIAL_ZERO_LIMIT_NOT_DISCHARGED",
            "partial",
            "does_not_discharge_zero_source_obligation",
            "zero limit is stated for Route B linear parent-source adapter, not for full K_tau_PP/N_projection operator",
        )
    if slot in {"source_domain", "projection_equation"}:
        return (
            "CONTENT_AUDIT_PARTIAL_CANDIDATE_NOT_ACCEPTED",
            "partial",
            "can_seed_followup_audit_but_not_acceptance",
            "candidate is endpoint-blind-looking but not a full Phi_lens_tau(a,k)->PP projection operator",
        )
    return (
        "CONTENT_AUDIT_UNCLASSIFIED_BLOCKED",
        "blocked",
        "blocks_physical_operator_acceptance",
        "unclassified row must be reviewed before acceptance",
    )


def build_rows() -> list[dict[str, str]]:
    rows = []
    for idx, submission_row in enumerate(read_csv(SUBMISSION), start=1):
        status, result, effect, blocker = classify(submission_row)
        rows.append(
            {
                "audit_row_id": f"TCMBEBOPCA01_{idx:03d}",
                "packet_slot": submission_row["packet_slot"],
                "content_audit_status": status,
                "audit_result": result,
                "acceptance_effect": effect,
                "remaining_blocker": blocker,
                "evidence_artifact": submission_row["evidence_artifact"],
                "provenance_hash": submission_row["provenance_hash"],
            }
        )
    return rows


def write_table(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def build_summary(table_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    router = read_json(ROUTER)
    blocked = [row["packet_slot"] for row in rows if row["audit_result"] == "blocked"]
    partial = [row["packet_slot"] for row in rows if row["audit_result"] == "partial"]
    accepted = [row["packet_slot"] for row in rows if row["audit_result"] == "accepted"]
    content_acceptance = bool(rows) and len(accepted) == len(rows)
    return {
        "report_id": "cmb_tau_lensing_endpoint_blind_operator_packet_content_audit_summary_v01",
        "claim_boundary": "endpoint_blind_operator_packet_content_audit_only_no_operator_acceptance_no_physical_score_no_dark_sector_verdict",
        "table": rel(table_path),
        "submission": rel(SUBMISSION),
        "router_status": router.get("status"),
        "status": "CONTENT_AUDIT_BLOCKED_PARTIAL_CANDIDATE_NOT_ACCEPTED"
        if not content_acceptance
        else "CONTENT_AUDIT_ACCEPTED_NOT_SCORE",
        "rows": len(rows),
        "accepted_rows": accepted,
        "partial_rows": partial,
        "blocked_rows": blocked,
        "content_acceptance": content_acceptance,
        "next_minimal_unblock": "supply_full_kernel_measure_and_normalization_then_fill_dimension_firewall_audits",
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(summary: dict[str, Any], rows: list[dict[str, str]], path: Path) -> None:
    row_text = "\n".join(
        f"- `{row['packet_slot']}`: {row['content_audit_status']} | {row['remaining_blocker']}"
        for row in rows
    )
    text = f"""# CMB Tau Lensing Endpoint-Blind Operator Packet Content Audit v01

**Doc class:** endpoint-blind operator packet content audit
**Reader role:** Paper 13 Tau-grid implementer
**Status:** {summary["status"]}
**Canonical parent:** `docs/cmb_tau_lensing_endpoint_blind_operator_packet_content_audit_router_v01.md`

## Claim Boundary

```text
{summary["claim_boundary"]}
```

## Result

```text
content_acceptance = {summary["content_acceptance"]}
```

## Audit Rows

{row_text}

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit endpoint-blind operator packet content.")
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
        path = Path(args.write_summary)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    if args.write_doc:
        write_doc(summary, rows, Path(args.write_doc))
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
