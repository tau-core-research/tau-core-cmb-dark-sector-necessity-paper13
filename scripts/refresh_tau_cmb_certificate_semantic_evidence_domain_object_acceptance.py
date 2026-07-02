#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CERT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_certificate_level_checker_replay_acceptance_audit_v01.csv"
CERT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_certificate_level_checker_replay_acceptance_audit_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_domain_object_acceptance_refresh_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_domain_object_acceptance_refresh_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_domain_object_acceptance_refresh_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_domain_object_acceptance_refresh_v01_"
    "domain_objects_accepted_from_semantic_certificate_pass_no_physical_R_CMB_"
    "no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "domain_object_acceptance_row_id",
    "source_certificate_level_checker_replay_acceptance_row_id",
    "certificate_area",
    "checker_name",
    "certificate_passed",
    "certificate_level_replay_accepted",
    "domain_object_name",
    "domain_object_accepted",
    "domain_object_kind",
    "physical_R_CMB_materialized",
    "allows_physical_R_CMB",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "acceptance_status",
    "blocking_reason",
    "claim_boundary",
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def input_chain_clean() -> bool:
    if not CERT_SUMMARY.exists():
        return False
    summary = load_json(CERT_SUMMARY)
    return (
        summary.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_CERTIFICATE_LEVEL_CHECKER_REPLAYS_ACCEPTED_SEMANTIC_CERTIFICATE_PASS"
        and summary.get("input_chain_clean") is True
        and summary.get("certificate_level_checker_replay_acceptance_rows") == 7
        and summary.get("certificate_level_replay_accepted_rows") == 7
        and summary.get("certificate_passed_rows") == 7
        and summary.get("accepted_domain_objects") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("certificate-level checker replay acceptance summary is not clean")
    out: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(CERT_TABLE), start=1):
        accepted = source["certificate_passed"] == "true" and source["certificate_level_replay_accepted"] == "true"
        area = source["certificate_area"]
        out.append(
            {
                "domain_object_acceptance_row_id": f"TCMBCDSEMDOMOBJ01_{index:03d}",
                "source_certificate_level_checker_replay_acceptance_row_id": source["certificate_level_checker_replay_acceptance_row_id"],
                "certificate_area": area,
                "checker_name": source["checker_name"],
                "certificate_passed": source["certificate_passed"],
                "certificate_level_replay_accepted": source["certificate_level_replay_accepted"],
                "domain_object_name": f"{area}_domain_object_v01",
                "domain_object_accepted": str(accepted).lower(),
                "domain_object_kind": "semantic_certificate_domain_object",
                "physical_R_CMB_materialized": "false",
                "allows_physical_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "acceptance_status": (
                    "DOMAIN_OBJECT_ACCEPTED_FROM_SEMANTIC_CERTIFICATE_PASS"
                    if accepted
                    else "DOMAIN_OBJECT_BLOCKED_CERTIFICATE_PASS_REQUIRED"
                ),
                "blocking_reason": (
                    "domain object accepted semantically; physical R_CMB materialization remains downstream"
                    if accepted
                    else "requires semantic certificate pass"
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
    accepted = sum(row["domain_object_accepted"] == "true" for row in rows)
    return {
        "report_id": "tau_cmb_certificate_semantic_evidence_domain_object_acceptance_refresh_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_certificate_level_checker_replay_acceptance_table": rel(CERT_TABLE),
        "input_certificate_level_checker_replay_acceptance_summary": rel(CERT_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "domain_object_acceptance_rows": len(rows),
        "accepted_domain_objects": accepted,
        "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_DOMAIN_OBJECTS_ACCEPTED_SEMANTIC_ONLY"
            if input_chain_clean() and len(rows) == 7 and accepted == 7
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_DOMAIN_OBJECT_ACCEPTANCE_REFRESH_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_request_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Domain Object Acceptance Refresh v01

**Doc class:** semantic evidence domain object acceptance refresh
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This refresh accepts semantic certificate domain objects from seven accepted
semantic certificate checker passes. It does not materialize physical R_CMB,
open scoring, evaluate likelihoods, or decide the dark-sector question.

## Summary

```text
domain_object_acceptance_rows={summary["domain_object_acceptance_rows"]}
accepted_domain_objects={summary["accepted_domain_objects"]}
certificate_passed_rows={summary["certificate_passed_rows"]}
physical_R_CMB_materialized={summary["physical_R_CMB_materialized"]}
score_entry_allowed={summary["score_entry_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Refresh Tau CMB semantic domain object acceptance.")
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
