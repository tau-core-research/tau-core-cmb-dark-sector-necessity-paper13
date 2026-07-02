#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MATERIALIZATION_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_materialization_packet_v01.csv"
MATERIALIZATION_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_materialization_packet_audit_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_file_materialization_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_file_materialization_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_input_payload_file_materialization_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_input_payload_file_materialization_v01_"
    "template_files_materialized_only_no_payload_staging_files_no_payload_acceptance_"
    "no_checker_execution_no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "file_materialization_row_id",
    "source_materialization_row_id",
    "certificate_area",
    "checker_name",
    "file_category",
    "template_artifact_path",
    "required_payload_staging_path",
    "template_file_written",
    "template_sha256",
    "payload_staging_file_written",
    "payload_file_materialized",
    "hash_bound",
    "provenance_bound",
    "replay_bound",
    "firewall_bound",
    "payload_accepted",
    "can_execute_after_file_materialization",
    "checker_executed",
    "certificate_passed",
    "domain_object_accepted",
    "allows_concrete_R_CMB",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "materialization_status",
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def template_payload(source: dict[str, str]) -> dict[str, Any]:
    return {
        "template_status": "UNPOPULATED_TEMPLATE_NOT_PAYLOAD",
        "claim_boundary": CLAIM_BOUNDARY,
        "certificate_area": source["certificate_area"],
        "checker_name": source["checker_name"],
        "file_category": source["file_category"],
        "required_payload_staging_path": source["required_payload_staging_path"],
        "materialization_requirement": source["materialization_requirement"],
        "endpoint_blind_firewall": {
            "cmb_endpoint_residuals_used": False,
            "act_planck_likelihood_used": False,
            "score_output_used": False,
            "post_endpoint_tuning_used": False,
        },
        "required_population_rule": (
            "Populate a payload_staging file from endpoint-blind Tau-side sources only; "
            "this template file is not accepted as checker input."
        ),
        "acceptance_permissions": {
            "payload_accepted": False,
            "checker_execution_allowed": False,
            "certificate_pass_allowed": False,
            "domain_acceptance_allowed": False,
            "concrete_R_CMB_allowed": False,
            "score_entry_allowed": False,
            "likelihood_allowed": False,
            "dark_sector_verdict_allowed": False,
        },
    }


def write_template_file(path: Path, source: dict[str, str]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = template_payload(source)
    path.write_text(json.dumps(content, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return sha256(path)


def table_rows(write_templates: bool) -> list[dict[str, str]]:
    source_rows = read_csv(MATERIALIZATION_TABLE)
    rows: list[dict[str, str]] = []
    for index, source in enumerate(source_rows, start=1):
        template_path = ROOT / source["template_artifact_path"]
        template_hash = write_template_file(template_path, source) if write_templates else (
            sha256(template_path) if template_path.exists() else ""
        )
        rows.append(
            {
                "file_materialization_row_id": f"TCMBCDIFM01_{index:03d}",
                "source_materialization_row_id": source["materialization_row_id"],
                "certificate_area": source["certificate_area"],
                "checker_name": source["checker_name"],
                "file_category": source["file_category"],
                "template_artifact_path": source["template_artifact_path"],
                "required_payload_staging_path": source["required_payload_staging_path"],
                "template_file_written": str(template_path.exists()).lower(),
                "template_sha256": template_hash,
                "payload_staging_file_written": str((ROOT / source["required_payload_staging_path"]).exists()).lower(),
                "payload_file_materialized": "false",
                "hash_bound": "false",
                "provenance_bound": "false",
                "replay_bound": "false",
                "firewall_bound": "false",
                "payload_accepted": "false",
                "can_execute_after_file_materialization": "false",
                "checker_executed": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_concrete_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "materialization_status": "TEMPLATE_FILE_MATERIALIZED_PAYLOAD_STAGING_FILE_ABSENT",
                "blocking_reason": "template file is materialized but required payload_staging file is not populated or accepted",
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
    audit = load_json(MATERIALIZATION_AUDIT) if MATERIALIZATION_AUDIT.exists() else {}
    input_ok = (
        audit.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_MATERIALIZATION_PACKET_AUDITED_SCHEMA_ONLY_NOT_EXECUTABLE"
        and audit.get("failed_rows") == 0
        and MATERIALIZATION_TABLE.exists()
    )
    return {
        "report_id": "tau_cmb_carrier_domain_checker_input_payload_file_materialization_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_materialization_table": rel(MATERIALIZATION_TABLE),
        "input_materialization_audit": rel(MATERIALIZATION_AUDIT),
        "input_chain_clean": input_ok,
        "file_materialization_rows": len(rows),
        "template_files_written": sum(row["template_file_written"] == "true" for row in rows),
        "payload_staging_files_written": sum(row["payload_staging_file_written"] == "true" for row in rows),
        "payload_file_materialized_rows": sum(row["payload_file_materialized"] == "true" for row in rows),
        "hash_bound_rows": sum(row["hash_bound"] == "true" for row in rows),
        "provenance_bound_rows": sum(row["provenance_bound"] == "true" for row in rows),
        "replay_bound_rows": sum(row["replay_bound"] == "true" for row in rows),
        "firewall_bound_rows": sum(row["firewall_bound"] == "true" for row in rows),
        "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
        "can_execute_after_file_materialization_rows": sum(row["can_execute_after_file_materialization"] == "true" for row in rows),
        "checker_executed_rows": sum(row["checker_executed"] == "true" for row in rows),
        "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
        "accepted_domain_objects": sum(row["domain_object_accepted"] == "true" for row in rows),
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_TEMPLATE_FILES_MATERIALIZED_PAYLOADS_NOT_MATERIALIZED"
            if input_ok
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_FILE_MATERIALIZATION_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "audit_tau_cmb_carrier_domain_checker_input_payload_file_materialization_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    area_counts: dict[str, int] = {}
    for row in rows:
        area_counts[row["certificate_area"]] = area_counts.get(row["certificate_area"], 0) + 1
    area_text = "\n".join(f"- `{area}`: {count} template files" for area, count in area_counts.items())
    text = f"""# Tau CMB Carrier Domain Checker Input Payload File Materialization v01

**Doc class:** carrier/domain checker input payload template-file materialization
**Reader role:** Paper 13 / CMB readout route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact materializes the declared checker-input template files under
`payload_templates/`. These files are unpopulated templates, not submitted
checker payloads. No `payload_staging/` input file is populated, no payload is
accepted, no checker is executable, no certificate passes, no domain object is
accepted, no concrete `R_CMB` is materialized, and no score, likelihood, or
dark-sector verdict is opened.

## Template Counts

{area_text}

## Summary

```text
file_materialization_rows={summary["file_materialization_rows"]}
template_files_written={summary["template_files_written"]}
payload_staging_files_written={summary["payload_staging_files_written"]}
payload_file_materialized_rows={summary["payload_file_materialized_rows"]}
payload_accepted_rows={summary["payload_accepted_rows"]}
can_execute_after_file_materialization_rows={summary["can_execute_after_file_materialization_rows"]}
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
    parser = argparse.ArgumentParser(description="Build Tau CMB carrier/domain checker input payload template-file materialization.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    parser.add_argument("--write-templates", action="store_true")
    args = parser.parse_args()
    rows = table_rows(write_templates=args.write_templates)
    table_path = Path(args.write_table or DEFAULT_TABLE)
    summary = build_summary(table_path, rows)
    if args.write_table:
        write_table(table_path, rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), rows, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
