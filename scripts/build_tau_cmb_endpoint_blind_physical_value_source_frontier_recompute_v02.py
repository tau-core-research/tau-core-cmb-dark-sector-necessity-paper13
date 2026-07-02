#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RECOMPUTE_V01_TABLE = ROOT / "data/derived/tau_cmb_endpoint_blind_physical_value_source_frontier_recompute_v01.csv"
TRANSFER_FAIL = ROOT / "data/derived/tau_cmb_lensing_transfer_kernel_explicit_fail_acceptance_audit_summary_v01.json"
AMPLITUDE_FAIL = ROOT / "data/derived/tau_cmb_lensing_amplitude_shape_response_explicit_fail_acceptance_audit_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_endpoint_blind_physical_value_source_frontier_recompute_v02.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_endpoint_blind_physical_value_source_frontier_recompute_summary_v02.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_endpoint_blind_physical_value_source_frontier_recompute_v02.md"

CLAIM_BOUNDARY = (
    "tau_cmb_endpoint_blind_physical_value_source_frontier_recompute_v02_"
    "two_explicit_failures_accepted_no_physical_source_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "frontier_recompute_row_id",
    "source_frontier_recompute_row_id",
    "role_name",
    "coordinate_symbol",
    "coordinate_component",
    "formal_slot",
    "previous_bucket",
    "updated_bucket",
    "updated_status",
    "recommended_next_action",
    "physical_value_source_accepted",
    "explicit_fail_accepted",
    "allows_physical_CMB_score",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "claim_boundary",
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def input_chain_clean() -> bool:
    if not RECOMPUTE_V01_TABLE.exists() or not TRANSFER_FAIL.exists() or not AMPLITUDE_FAIL.exists():
        return False
    transfer = load_json(TRANSFER_FAIL)
    amplitude = load_json(AMPLITUDE_FAIL)
    return (
        transfer.get("status") == "CMB_LENSING_TRANSFER_KERNEL_EXPLICIT_FAIL_ACCEPTED_PHYSICAL_SCORE_BLOCKED"
        and transfer.get("explicit_fail_accepted") is True
        and amplitude.get("status") == "CMB_LENSING_AMPLITUDE_SHAPE_RESPONSE_EXPLICIT_FAIL_ACCEPTED_PHYSICAL_SCORE_BLOCKED"
        and amplitude.get("next_minimal_unblock") == "tau_cmb_endpoint_blind_physical_value_source_frontier_recompute_v02"
        and amplitude.get("explicit_fail_accepted") is True
        and amplitude.get("physical_value_source_accepted") is False
        and amplitude.get("physical_CMB_score_allowed") is False
        and amplitude.get("likelihood_allowed") is False
        and amplitude.get("dark_sector_verdict_allowed") is False
    )


def rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("explicit fail acceptance summaries are not clean")
    out: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(RECOMPUTE_V01_TABLE), start=1):
        component = source["coordinate_component"]
        is_closed_fail = source["coordinate_symbol"] == "e_lensing" and component in {"transfer_kernel", "amplitude_shape_response"}
        if is_closed_fail:
            updated_bucket = "explicit_fail_accepted"
            updated_status = "ROW_CLOSED_AS_EXPLICIT_NON_SCORE_FAILURE"
            next_action = "do not score this row unless a replacement endpoint-blind value-source payload is supplied"
            explicit_fail_accepted = "true"
        else:
            updated_bucket = source["updated_bucket"]
            updated_status = source["updated_status"]
            next_action = source["recommended_next_action"]
            explicit_fail_accepted = source["explicit_fail_accepted"]
        out.append(
            {
                "frontier_recompute_row_id": f"TCMBEBPVSFR02_{index:03d}",
                "source_frontier_recompute_row_id": source["frontier_recompute_row_id"],
                "role_name": source["role_name"],
                "coordinate_symbol": source["coordinate_symbol"],
                "coordinate_component": component,
                "formal_slot": source["formal_slot"],
                "previous_bucket": source["updated_bucket"],
                "updated_bucket": updated_bucket,
                "updated_status": updated_status,
                "recommended_next_action": next_action,
                "physical_value_source_accepted": "false",
                "explicit_fail_accepted": explicit_fail_accepted,
                "allows_physical_CMB_score": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def write_table(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_summary(table_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    buckets: dict[str, int] = {}
    for row in rows:
        buckets[row["updated_bucket"]] = buckets.get(row["updated_bucket"], 0) + 1
    open_rows = sum(row["updated_status"] == "ROW_REMAINS_OPEN" for row in rows)
    return {
        "report_id": "tau_cmb_endpoint_blind_physical_value_source_frontier_recompute_summary_v02",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_frontier_recompute_v01_table": rel(RECOMPUTE_V01_TABLE),
        "input_transfer_kernel_explicit_fail_acceptance": rel(TRANSFER_FAIL),
        "input_amplitude_shape_explicit_fail_acceptance": rel(AMPLITUDE_FAIL),
        "input_chain_clean": input_chain_clean(),
        "frontier_rows": len(rows),
        "explicit_fail_accepted_rows": sum(row["explicit_fail_accepted"] == "true" for row in rows),
        "physical_value_source_accepted_rows": 0,
        "open_frontier_rows": open_rows,
        "updated_bucket_counts": buckets,
        "physical_CMB_score_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_ENDPOINT_BLIND_PHYSICAL_VALUE_SOURCE_FRONTIER_RECOMPUTED_TWO_EXPLICIT_FAILS_ACCEPTED"
            if input_chain_clean() and len(rows) == 16 and open_rows == 14
            else "CMB_ENDPOINT_BLIND_PHYSICAL_VALUE_SOURCE_FRONTIER_RECOMPUTE_V02_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_physical_source_dependency_unblock_plan_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Endpoint-Blind Physical Value Source Frontier Recompute v02

**Doc class:** frontier status update
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Summary

```text
frontier_rows={summary["frontier_rows"]}
explicit_fail_accepted_rows={summary["explicit_fail_accepted_rows"]}
physical_value_source_accepted_rows={summary["physical_value_source_accepted_rows"]}
open_frontier_rows={summary["open_frontier_rows"]}
updated_bucket_counts={summary["updated_bucket_counts"]}
physical_CMB_score_allowed={summary["physical_CMB_score_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

Both currently bridge-adjacent lensing rows are now closed as explicit
non-score failures. The remaining frontier is dependency-blocked.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Recompute Tau CMB endpoint-blind physical value-source frontier after two explicit fail acceptances.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    table_rows = rows()
    table_path = Path(args.write_table) if args.write_table else DEFAULT_TABLE
    summary = build_summary(table_path, table_rows)
    if args.write_table:
        write_table(table_path, table_rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
