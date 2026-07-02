#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
POP_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_staging_population_packet_v01.csv"
ACCEPTANCE_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_acceptance_v01.csv"
ACCEPTANCE_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_acceptance_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_v01_"
    "staging_files_populated_from_accepted_endpoint_blind_tau_side_sources_no_payload_acceptance_"
    "no_checker_execution_no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "execution_row_id",
    "source_population_row_id",
    "source_acceptance_row_id",
    "certificate_area",
    "checker_name",
    "file_category",
    "target_payload_staging_path",
    "source_artifact_path",
    "execution_command",
    "pre_execution_guard",
    "post_execution_required_checks",
    "execution_packet_declared",
    "can_execute",
    "execution_attempted",
    "execution_succeeded",
    "payload_staging_written",
    "payload_staging_populated",
    "staging_sha256",
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


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def acceptance_by_population_id() -> dict[str, dict[str, str]]:
    accepted: dict[str, dict[str, str]] = {}
    for row in read_csv(ACCEPTANCE_TABLE):
        source_id = row["source_request_row_id"].replace("TCMBCDIEBSAR01_", "TCMBCDIPOP01_")
        accepted[source_id] = row
    return accepted


def endpoint_blind_input_chain_clean() -> bool:
    if not ACCEPTANCE_SUMMARY.exists():
        return False
    summary = load_json(ACCEPTANCE_SUMMARY)
    return (
        summary.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACTS_ACCEPTED_FOR_STAGING_POPULATION_ONLY"
        and summary.get("input_chain_clean") is True
        and summary.get("source_artifact_accepted_rows") == 66
        and summary.get("staging_population_allowed_rows") == 66
        and summary.get("payload_staging_written_rows") == 0
        and summary.get("payload_accepted_rows") == 0
        and summary.get("checker_executed_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def staging_payload(pop_row: dict[str, str], accepted_row: dict[str, str], source_artifact: dict[str, Any]) -> dict[str, Any]:
    return {
        "staging_status": "POPULATED_FROM_ACCEPTED_ENDPOINT_BLIND_TAU_SIDE_SOURCE_NOT_ACCEPTED",
        "claim_boundary": CLAIM_BOUNDARY,
        "population_row_id": pop_row["population_row_id"],
        "acceptance_row_id": accepted_row["acceptance_row_id"],
        "certificate_area": pop_row["certificate_area"],
        "checker_name": pop_row["checker_name"],
        "file_category": pop_row["file_category"],
        "template_artifact_path": pop_row["template_artifact_path"],
        "target_payload_staging_path": pop_row["target_payload_staging_path"],
        "source_artifact_path": accepted_row["source_artifact_path"],
        "source_hash_path": accepted_row["source_hash_path"],
        "source_replay_path": accepted_row["source_replay_path"],
        "source_provenance_path": accepted_row["source_provenance_path"],
        "source_firewall_path": accepted_row["source_firewall_path"],
        "endpoint_blind_firewall": {
            "cmb_endpoint_residuals_used": False,
            "act_planck_likelihood_used": False,
            "score_output_used": False,
            "post_endpoint_tuning_used": False,
            "dark_sector_verdict_used": False,
        },
        "accepted_source_summary": {
            "source_inventory_count": len(source_artifact.get("source_inventory", [])),
            "certificate_area": source_artifact.get("certificate_area"),
            "checker_name": source_artifact.get("checker_name"),
            "source_artifact_status": source_artifact.get("artifact_status"),
            "endpoint_blind_rule": source_artifact.get("endpoint_blind_rule"),
        },
        "population_rule": pop_row["population_source_rule"],
        "post_population_required_checks": pop_row["required_binding_after_population"],
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


def execute_population(write_staging: bool) -> list[dict[str, str]]:
    if not endpoint_blind_input_chain_clean():
        raise SystemExit("endpoint-blind source artifact acceptance summary is not clean")
    accepted = acceptance_by_population_id()
    rows: list[dict[str, str]] = []
    for index, pop_row in enumerate(read_csv(POP_TABLE), start=1):
        accepted_row = accepted[pop_row["population_row_id"]]
        source_path = ROOT / accepted_row["source_artifact_path"]
        source_artifact = load_json(source_path)
        target = ROOT / pop_row["target_payload_staging_path"]
        can_execute = (
            accepted_row["source_artifact_accepted"] == "true"
            and accepted_row["staging_population_allowed"] == "true"
            and source_path.exists()
        )
        if write_staging and can_execute:
            write_json(target, staging_payload(pop_row, accepted_row, source_artifact))
        written = target.exists()
        staging_hash = sha256(target) if written else ""
        rows.append(
            {
                "execution_row_id": f"TCMBCDIPOPEXE01_{index:03d}",
                "source_population_row_id": pop_row["population_row_id"],
                "source_acceptance_row_id": accepted_row["acceptance_row_id"],
                "certificate_area": pop_row["certificate_area"],
                "checker_name": pop_row["checker_name"],
                "file_category": pop_row["file_category"],
                "target_payload_staging_path": pop_row["target_payload_staging_path"],
                "source_artifact_path": accepted_row["source_artifact_path"],
                "execution_command": "python3 scripts/populate_tau_cmb_carrier_domain_checker_input_payload_staging.py --write-staging --write-table --write-summary --write-doc",
                "pre_execution_guard": "requires accepted endpoint-blind Tau-side source artifact bundle and clean acceptance summary",
                "post_execution_required_checks": "run staging population execution audit, then payload acceptance audit before checker execution",
                "execution_packet_declared": "true",
                "can_execute": str(can_execute).lower(),
                "execution_attempted": str(write_staging and can_execute).lower(),
                "execution_succeeded": str(write_staging and written and can_execute).lower(),
                "payload_staging_written": str(written).lower(),
                "payload_staging_populated": str(written).lower(),
                "staging_sha256": staging_hash,
                "hash_bound": str(written).lower(),
                "provenance_bound": str(written).lower(),
                "replay_bound": str(written).lower(),
                "firewall_bound": str(written).lower(),
                "payload_accepted": "false",
                "checker_executed": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_concrete_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "execution_status": (
                    "STAGING_POPULATION_EXECUTED_PAYLOAD_STAGING_POPULATED_NOT_ACCEPTED"
                    if written and can_execute
                    else "STAGING_POPULATION_EXECUTION_ALLOWED_NOT_WRITTEN"
                    if can_execute
                    else "STAGING_POPULATION_EXECUTION_BLOCKED_BY_SOURCE_ACCEPTANCE"
                ),
                "blocking_reason": (
                    "payload staging populated; requires payload acceptance audit before checker execution"
                    if written and can_execute
                    else "execution allowed but --write-staging was not requested"
                    if can_execute
                    else "accepted endpoint-blind source artifact was unavailable"
                ),
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
    written_rows = sum(row["payload_staging_written"] == "true" for row in rows)
    return {
        "report_id": "tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_population_table": rel(POP_TABLE),
        "input_source_acceptance_table": rel(ACCEPTANCE_TABLE),
        "input_source_acceptance_summary": rel(ACCEPTANCE_SUMMARY),
        "input_chain_clean": endpoint_blind_input_chain_clean(),
        "execution_rows": len(rows),
        "execution_packets_declared": sum(row["execution_packet_declared"] == "true" for row in rows),
        "can_execute_rows": sum(row["can_execute"] == "true" for row in rows),
        "execution_attempted_rows": sum(row["execution_attempted"] == "true" for row in rows),
        "execution_succeeded_rows": sum(row["execution_succeeded"] == "true" for row in rows),
        "payload_staging_written_rows": written_rows,
        "payload_staging_populated_rows": sum(row["payload_staging_populated"] == "true" for row in rows),
        "hash_bound_rows": sum(row["hash_bound"] == "true" for row in rows),
        "provenance_bound_rows": sum(row["provenance_bound"] == "true" for row in rows),
        "replay_bound_rows": sum(row["replay_bound"] == "true" for row in rows),
        "firewall_bound_rows": sum(row["firewall_bound"] == "true" for row in rows),
        "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
        "checker_executed_rows": sum(row["checker_executed"] == "true" for row in rows),
        "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
        "accepted_domain_objects": sum(row["domain_object_accepted"] == "true" for row in rows),
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_STAGING_POPULATION_EXECUTED_PAYLOADS_POPULATED_NOT_ACCEPTED"
            if written_rows == 66
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_STAGING_POPULATION_EXECUTION_ALLOWED_NOT_WRITTEN"
        ),
        "next_minimal_unblock": "audit_tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    area_counts: dict[str, int] = {}
    for row in rows:
        area_counts[row["certificate_area"]] = area_counts.get(row["certificate_area"], 0) + 1
    area_text = "\n".join(f"- `{area}`: {count} populated staging files" for area, count in area_counts.items())
    text = f"""# Tau CMB Carrier Domain Checker Input Payload Staging Population Execution v01

**Doc class:** carrier/domain checker input payload staging population execution
**Reader role:** Paper 13 / CMB readout route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact populates `payload_staging/` checker-input files from accepted
endpoint-blind Tau-side source artifact bundles. The populated files are not
accepted checker payloads. No checker is executed, no certificate passes, no
domain object is accepted, no concrete `R_CMB` is materialized, and no score,
likelihood, or dark-sector verdict is opened.

## Populated Staging Files

{area_text}

## Summary

```text
execution_rows={summary["execution_rows"]}
can_execute_rows={summary["can_execute_rows"]}
execution_attempted_rows={summary["execution_attempted_rows"]}
execution_succeeded_rows={summary["execution_succeeded_rows"]}
payload_staging_written_rows={summary["payload_staging_written_rows"]}
payload_staging_populated_rows={summary["payload_staging_populated_rows"]}
payload_accepted_rows={summary["payload_accepted_rows"]}
checker_executed_rows={summary["checker_executed_rows"]}
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
    parser = argparse.ArgumentParser(description="Populate Tau CMB carrier/domain checker input payload staging files.")
    parser.add_argument("--write-staging", action="store_true")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = execute_population(write_staging=args.write_staging)
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
