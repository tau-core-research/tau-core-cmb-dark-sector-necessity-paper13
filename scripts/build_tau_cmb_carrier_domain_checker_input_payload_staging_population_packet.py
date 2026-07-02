#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FILE_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_file_materialization_v01.csv"
FILE_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_file_materialization_audit_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_staging_population_packet_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_staging_population_packet_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_input_payload_staging_population_packet_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_input_payload_staging_population_packet_v01_"
    "population_packet_only_no_payload_staging_written_no_payload_acceptance_no_checker_execution_"
    "no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "population_row_id",
    "source_file_materialization_row_id",
    "certificate_area",
    "checker_name",
    "file_category",
    "template_artifact_path",
    "target_payload_staging_path",
    "population_source_rule",
    "required_endpoint_blind_source",
    "required_binding_after_population",
    "required_acceptance_gate",
    "population_packet_declared",
    "template_available",
    "payload_staging_written",
    "payload_staging_populated",
    "hash_bound",
    "provenance_bound",
    "replay_bound",
    "firewall_bound",
    "payload_accepted",
    "can_execute_after_population",
    "checker_executed",
    "certificate_passed",
    "domain_object_accepted",
    "allows_concrete_R_CMB",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "population_status",
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


def source_rule_for(category: str) -> str:
    rules = {
        "payload": "populate from endpoint-blind Tau-side carrier/domain/source/quotient/codomain material only",
        "replay": "populate deterministic replay trace from local construction commands without CMB endpoint target access",
        "provenance": "populate source-freeze provenance, source hashes, and construction rationale",
        "hash": "populate after target payload, replay, provenance, and firewall files exist",
        "firewall": "populate endpoint-blind access exclusion attestation and post-endpoint tuning denial",
    }
    return rules[category]


def table_rows() -> list[dict[str, str]]:
    source_rows = read_csv(FILE_TABLE)
    rows: list[dict[str, str]] = []
    for index, source in enumerate(source_rows, start=1):
        target = ROOT / source["required_payload_staging_path"]
        template = ROOT / source["template_artifact_path"]
        rows.append(
            {
                "population_row_id": f"TCMBCDIPOP01_{index:03d}",
                "source_file_materialization_row_id": source["file_materialization_row_id"],
                "certificate_area": source["certificate_area"],
                "checker_name": source["checker_name"],
                "file_category": source["file_category"],
                "template_artifact_path": source["template_artifact_path"],
                "target_payload_staging_path": source["required_payload_staging_path"],
                "population_source_rule": source_rule_for(source["file_category"]),
                "required_endpoint_blind_source": "endpoint-blind Tau-side sources only; no CMB endpoint residuals, likelihood errors, score outputs, or post-endpoint tuning",
                "required_binding_after_population": "content hash, provenance, replay, and firewall binding must be rebuilt after population",
                "required_acceptance_gate": "may become accepted only after populated staging files and bindings pass acceptance audit",
                "population_packet_declared": "true",
                "template_available": str(template.exists()).lower(),
                "payload_staging_written": str(target.exists()).lower(),
                "payload_staging_populated": "false",
                "hash_bound": "false",
                "provenance_bound": "false",
                "replay_bound": "false",
                "firewall_bound": "false",
                "payload_accepted": "false",
                "can_execute_after_population": "false",
                "checker_executed": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_concrete_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "population_status": "STAGING_POPULATION_PACKET_DECLARED_NOT_POPULATED",
                "blocking_reason": "payload_staging file is not populated from endpoint-blind Tau-side sources",
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
    audit = load_json(FILE_AUDIT) if FILE_AUDIT.exists() else {}
    input_ok = (
        audit.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_TEMPLATE_FILES_AUDITED_PAYLOADS_NOT_MATERIALIZED"
        and audit.get("failed_rows") == 0
        and FILE_TABLE.exists()
    )
    return {
        "report_id": "tau_cmb_carrier_domain_checker_input_payload_staging_population_packet_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_file_materialization_table": rel(FILE_TABLE),
        "input_file_materialization_audit": rel(FILE_AUDIT),
        "input_chain_clean": input_ok,
        "population_rows": len(rows),
        "population_packets_declared": sum(row["population_packet_declared"] == "true" for row in rows),
        "template_available_rows": sum(row["template_available"] == "true" for row in rows),
        "payload_staging_written_rows": sum(row["payload_staging_written"] == "true" for row in rows),
        "payload_staging_populated_rows": sum(row["payload_staging_populated"] == "true" for row in rows),
        "hash_bound_rows": sum(row["hash_bound"] == "true" for row in rows),
        "provenance_bound_rows": sum(row["provenance_bound"] == "true" for row in rows),
        "replay_bound_rows": sum(row["replay_bound"] == "true" for row in rows),
        "firewall_bound_rows": sum(row["firewall_bound"] == "true" for row in rows),
        "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
        "can_execute_after_population_rows": sum(row["can_execute_after_population"] == "true" for row in rows),
        "checker_executed_rows": sum(row["checker_executed"] == "true" for row in rows),
        "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
        "accepted_domain_objects": sum(row["domain_object_accepted"] == "true" for row in rows),
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_STAGING_POPULATION_PACKET_DECLARED_NOT_POPULATED"
            if input_ok
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_STAGING_POPULATION_PACKET_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "audit_tau_cmb_carrier_domain_checker_input_payload_staging_population_packet_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    area_counts: dict[str, int] = {}
    for row in rows:
        area_counts[row["certificate_area"]] = area_counts.get(row["certificate_area"], 0) + 1
    area_text = "\n".join(f"- `{area}`: {count} population obligations" for area, count in area_counts.items())
    text = f"""# Tau CMB Carrier Domain Checker Input Payload Staging Population Packet v01

**Doc class:** carrier/domain checker input payload staging population packet
**Reader role:** Paper 13 / CMB readout route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This packet declares how the existing unpopulated checker-input templates may
later be populated into `payload_staging/` from endpoint-blind Tau-side sources.
It does not write staging payloads, bind hashes, accept payloads, execute
checkers, pass certificates, accept domain objects, materialize `R_CMB`, open
score entry, compute a likelihood, or decide the dark-sector question.

## Population Obligations

{area_text}

## Summary

```text
population_rows={summary["population_rows"]}
template_available_rows={summary["template_available_rows"]}
payload_staging_written_rows={summary["payload_staging_written_rows"]}
payload_staging_populated_rows={summary["payload_staging_populated_rows"]}
payload_accepted_rows={summary["payload_accepted_rows"]}
can_execute_after_population_rows={summary["can_execute_after_population_rows"]}
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
    parser = argparse.ArgumentParser(description="Build Tau CMB carrier/domain checker input payload staging population packet.")
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
