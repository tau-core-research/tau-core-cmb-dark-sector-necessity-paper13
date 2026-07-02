#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKET_TABLE = ROOT / "data/derived/tau_cmb_endpoint_blind_physical_value_source_packet_v01.csv"
PACKET_SUMMARY = ROOT / "data/derived/tau_cmb_endpoint_blind_physical_value_source_packet_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_endpoint_blind_physical_value_source_packet_acceptance_audit_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_endpoint_blind_physical_value_source_packet_acceptance_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_endpoint_blind_physical_value_source_packet_acceptance_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_endpoint_blind_physical_value_source_packet_acceptance_audit_v01_"
    "packet_contracts_accepted_sources_absent_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "physical_value_source_packet_acceptance_row_id",
    "source_physical_value_source_packet_row_id",
    "role_name",
    "coordinate_symbol",
    "coordinate_component",
    "formal_slot",
    "frontier_class",
    "packet_declared",
    "packet_hash_matches",
    "packet_contract_accepted",
    "physical_value_source_supplied",
    "physical_value_source_accepted",
    "allows_physical_CMB_score",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "acceptance_status",
    "blocking_reason",
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
    if not PACKET_SUMMARY.exists() or not PACKET_TABLE.exists():
        return False
    summary = load_json(PACKET_SUMMARY)
    return (
        summary.get("status") == "CMB_ENDPOINT_BLIND_PHYSICAL_VALUE_SOURCE_PACKET_DECLARED_SOURCES_NOT_SUPPLIED"
        and summary.get("next_minimal_unblock") == "tau_cmb_endpoint_blind_physical_value_source_supply_v01"
        and summary.get("physical_value_source_packet_rows") == 16
        and summary.get("packet_declared_rows") == 16
        and summary.get("packet_hash_matched_rows") == 16
        and summary.get("physical_value_source_supplied_rows") == 0
        and summary.get("physical_value_source_accepted_rows") == 0
        and summary.get("physical_CMB_score_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("physical value-source packet summary is not clean")
    out: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(PACKET_TABLE), start=1):
        contract_accepted = source["packet_declared"] == "true" and source["packet_hash_matches"] == "true"
        source_accepted = contract_accepted and source["physical_value_source_supplied"] == "true" and source["physical_value_source_accepted"] == "true"
        out.append(
            {
                "physical_value_source_packet_acceptance_row_id": f"TCMBEBPVSPACC01_{index:03d}",
                "source_physical_value_source_packet_row_id": source["physical_value_source_packet_row_id"],
                "role_name": source["role_name"],
                "coordinate_symbol": source["coordinate_symbol"],
                "coordinate_component": source["coordinate_component"],
                "formal_slot": source["formal_slot"],
                "frontier_class": source["frontier_class"],
                "packet_declared": source["packet_declared"],
                "packet_hash_matches": source["packet_hash_matches"],
                "packet_contract_accepted": str(contract_accepted).lower(),
                "physical_value_source_supplied": source["physical_value_source_supplied"],
                "physical_value_source_accepted": str(source_accepted).lower(),
                "allows_physical_CMB_score": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "acceptance_status": (
                    "PHYSICAL_VALUE_SOURCE_ACCEPTED_FOR_SCORE_INPUT"
                    if source_accepted
                    else "PHYSICAL_VALUE_SOURCE_PACKET_CONTRACT_ACCEPTED_SOURCE_ABSENT"
                ),
                "blocking_reason": (
                    "physical value source accepted"
                    if source_accepted
                    else "packet contract is accepted, but endpoint-blind physical value source or explicit fail evidence is absent"
                ),
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
    accepted_contracts = sum(row["packet_contract_accepted"] == "true" for row in rows)
    accepted_sources = sum(row["physical_value_source_accepted"] == "true" for row in rows)
    return {
        "report_id": "tau_cmb_endpoint_blind_physical_value_source_packet_acceptance_audit_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_packet_table": rel(PACKET_TABLE),
        "input_packet_summary": rel(PACKET_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "physical_value_source_packet_acceptance_rows": len(rows),
        "packet_contract_accepted_rows": accepted_contracts,
        "physical_value_source_supplied_rows": sum(row["physical_value_source_supplied"] == "true" for row in rows),
        "physical_value_source_accepted_rows": accepted_sources,
        "physical_CMB_score_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_ENDPOINT_BLIND_PHYSICAL_VALUE_SOURCE_PACKET_CONTRACTS_ACCEPTED_SOURCES_ABSENT"
            if input_chain_clean() and len(rows) == 16 and accepted_contracts == 16 and accepted_sources == 0
            else "CMB_ENDPOINT_BLIND_PHYSICAL_VALUE_SOURCE_PACKET_ACCEPTANCE_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_endpoint_blind_physical_value_source_supply_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Endpoint-Blind Physical Value Source Packet Acceptance Audit v01

**Doc class:** endpoint-blind physical value-source packet acceptance audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Summary

```text
physical_value_source_packet_acceptance_rows={summary["physical_value_source_packet_acceptance_rows"]}
packet_contract_accepted_rows={summary["packet_contract_accepted_rows"]}
physical_value_source_supplied_rows={summary["physical_value_source_supplied_rows"]}
physical_value_source_accepted_rows={summary["physical_value_source_accepted_rows"]}
physical_CMB_score_allowed={summary["physical_CMB_score_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

The packet contracts are accepted, but no physical value source is accepted for
score input.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB endpoint-blind physical value-source packet acceptance.")
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
