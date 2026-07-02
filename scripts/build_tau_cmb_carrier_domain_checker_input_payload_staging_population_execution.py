#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
POP_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_staging_population_packet_v01.csv"
POP_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_staging_population_packet_audit_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_v01_"
    "execution_envelope_only_can_execute_false_no_staging_write_no_payload_acceptance_"
    "no_checker_execution_no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "execution_row_id",
    "source_population_row_id",
    "certificate_area",
    "checker_name",
    "file_category",
    "target_payload_staging_path",
    "execution_command_template",
    "pre_execution_guard",
    "post_execution_required_checks",
    "execution_packet_declared",
    "can_execute",
    "execution_attempted",
    "execution_succeeded",
    "payload_staging_written",
    "payload_staging_populated",
    "hash_bound",
    "provenance_bound",
    "replay_bound",
    "firewall_bound",
    "payload_accepted",
    "checker_executed",
    "certificate_passed",
    "domain_object_accepted",
    "allows_concrete_R_CMB",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "execution_status",
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


def table_rows() -> list[dict[str, str]]:
    population_rows = read_csv(POP_TABLE)
    rows: list[dict[str, str]] = []
    for index, source in enumerate(population_rows, start=1):
        rows.append(
            {
                "execution_row_id": f"TCMBCDIPOPEXE01_{index:03d}",
                "source_population_row_id": source["population_row_id"],
                "certificate_area": source["certificate_area"],
                "checker_name": source["checker_name"],
                "file_category": source["file_category"],
                "target_payload_staging_path": source["target_payload_staging_path"],
                "execution_command_template": (
                    "python3 scripts/populate_tau_cmb_carrier_domain_checker_input_payload_staging.py "
                    f"--population-row {source['population_row_id']} --endpoint-blind-source <TAU_SIDE_SOURCE> --write"
                ),
                "pre_execution_guard": (
                    "requires populated endpoint-blind Tau-side source artifact, source hash, replay rule, "
                    "and endpoint firewall attestation; current guard blocks execution"
                ),
                "post_execution_required_checks": (
                    "recompute hash binding; verify provenance, replay, and firewall; then run payload acceptance audit"
                ),
                "execution_packet_declared": "true",
                "can_execute": "false",
                "execution_attempted": "false",
                "execution_succeeded": "false",
                "payload_staging_written": "false",
                "payload_staging_populated": "false",
                "hash_bound": "false",
                "provenance_bound": "false",
                "replay_bound": "false",
                "firewall_bound": "false",
                "payload_accepted": "false",
                "checker_executed": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_concrete_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "execution_status": "STAGING_POPULATION_EXECUTION_DECLARED_BLOCKED_NOT_EXECUTED",
                "blocking_reason": "endpoint-blind Tau-side source artifact and binding evidence are not supplied",
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
    audit = load_json(POP_AUDIT) if POP_AUDIT.exists() else {}
    input_ok = (
        audit.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_STAGING_POPULATION_PACKET_AUDITED_NOT_POPULATED"
        and audit.get("failed_rows") == 0
        and POP_TABLE.exists()
    )
    return {
        "report_id": "tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_population_table": rel(POP_TABLE),
        "input_population_audit": rel(POP_AUDIT),
        "input_chain_clean": input_ok,
        "execution_rows": len(rows),
        "execution_packets_declared": sum(row["execution_packet_declared"] == "true" for row in rows),
        "can_execute_rows": sum(row["can_execute"] == "true" for row in rows),
        "execution_attempted_rows": sum(row["execution_attempted"] == "true" for row in rows),
        "execution_succeeded_rows": sum(row["execution_succeeded"] == "true" for row in rows),
        "payload_staging_written_rows": sum(row["payload_staging_written"] == "true" for row in rows),
        "payload_staging_populated_rows": sum(row["payload_staging_populated"] == "true" for row in rows),
        "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
        "checker_executed_rows": sum(row["checker_executed"] == "true" for row in rows),
        "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
        "accepted_domain_objects": sum(row["domain_object_accepted"] == "true" for row in rows),
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_STAGING_POPULATION_EXECUTION_DECLARED_BLOCKED_NOT_EXECUTED"
            if input_ok
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_STAGING_POPULATION_EXECUTION_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "audit_tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    area_counts: dict[str, int] = {}
    for row in rows:
        area_counts[row["certificate_area"]] = area_counts.get(row["certificate_area"], 0) + 1
    area_text = "\n".join(f"- `{area}`: {count} blocked execution envelopes" for area, count in area_counts.items())
    text = f"""# Tau CMB Carrier Domain Checker Input Payload Staging Population Execution v01

**Doc class:** carrier/domain checker input payload staging population execution envelope
**Reader role:** Paper 13 / CMB readout route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact declares blocked execution envelopes for populating
`payload_staging/` from endpoint-blind Tau-side sources. It does not run the
commands, write staging files, accept payloads, execute checkers, pass
certificates, accept domain objects, materialize `R_CMB`, open score entry,
compute a likelihood, or decide the dark-sector question.

## Execution Envelopes

{area_text}

## Summary

```text
execution_rows={summary["execution_rows"]}
can_execute_rows={summary["can_execute_rows"]}
execution_attempted_rows={summary["execution_attempted_rows"]}
execution_succeeded_rows={summary["execution_succeeded_rows"]}
payload_staging_written_rows={summary["payload_staging_written_rows"]}
payload_accepted_rows={summary["payload_accepted_rows"]}
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
    parser = argparse.ArgumentParser(description="Build Tau CMB carrier/domain checker input payload staging population execution envelope.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = table_rows()
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
