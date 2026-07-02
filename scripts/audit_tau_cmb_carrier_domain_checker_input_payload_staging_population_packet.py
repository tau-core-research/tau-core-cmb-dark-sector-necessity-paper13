#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
POP_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_staging_population_packet_v01.csv"
POP_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_staging_population_packet_summary_v01.json"
FILE_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_file_materialization_audit_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_staging_population_packet_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_input_payload_staging_population_packet_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_input_payload_staging_population_packet_audit_v01_"
    "audit_only_population_packet_clean_but_unpopulated_no_payload_acceptance_no_checker_execution_"
    "no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict"
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
    required = [POP_TABLE, POP_SUMMARY, FILE_AUDIT]
    missing = [path for path in required if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    pop_rows = read_csv(POP_TABLE)
    summary = load_json(POP_SUMMARY)
    file_audit = load_json(FILE_AUDIT)

    shape_ok = (
        len(pop_rows) == 66
        and {row.get("file_category") for row in pop_rows} == {"payload", "replay", "provenance", "hash", "firewall"}
    )
    rows.append(audit_row(
        "population_row_shape",
        "PASS_EXPECTED_POPULATION_ROWS_PRESENT" if shape_ok else "FAIL_POPULATION_ROW_SHAPE",
        f"rows={len(pop_rows)}",
        shape_ok,
        "staging population packet requires the 66 declared population obligations",
    ))

    input_ok = (
        summary.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_STAGING_POPULATION_PACKET_DECLARED_NOT_POPULATED"
        and summary.get("input_chain_clean") is True
        and file_audit.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_TEMPLATE_FILES_AUDITED_PAYLOADS_NOT_MATERIALIZED"
        and file_audit.get("failed_rows") == 0
    )
    rows.append(audit_row(
        "input_file_materialization_chain",
        "PASS_POPULATION_INPUT_CHAIN" if input_ok else "FAIL_POPULATION_INPUT_CHAIN",
        "staging population packet follows a clean audited template-file materialization",
        input_ok,
        "population audit must be downstream of a clean template-file materialization audit",
    ))

    source_rules_ok = all(
        "endpoint-blind" in row.get("required_endpoint_blind_source", "")
        and "Tau-side sources only" in row.get("required_endpoint_blind_source", "")
        and "acceptance audit" in row.get("required_acceptance_gate", "")
        and row.get("population_source_rule")
        for row in pop_rows
    )
    rows.append(audit_row(
        "population_source_rules",
        "PASS_ENDPOINT_BLIND_POPULATION_RULES" if source_rules_ok else "FAIL_POPULATION_SOURCE_RULES",
        "each row declares Tau-side endpoint-blind population source and acceptance gate",
        source_rules_ok,
        "population packet must declare endpoint-blind source rules and acceptance gates",
    ))

    template_ok = all(row.get("template_available") == "true" for row in pop_rows)
    rows.append(audit_row(
        "template_availability",
        "PASS_TEMPLATES_AVAILABLE" if template_ok else "FAIL_TEMPLATE_AVAILABILITY",
        f"template_available_rows={summary.get('template_available_rows')}",
        template_ok,
        "all population obligations require available templates",
    ))

    accounting_ok = (
        summary.get("population_rows") == 66
        and summary.get("population_packets_declared") == 66
        and summary.get("template_available_rows") == 66
        and summary.get("payload_staging_written_rows") == 0
        and summary.get("payload_staging_populated_rows") == 0
        and summary.get("payload_accepted_rows") == 0
        and summary.get("can_execute_after_population_rows") == 0
        and summary.get("checker_executed_rows") == 0
        and summary.get("certificate_passed_rows") == 0
        and summary.get("accepted_domain_objects") == 0
    )
    rows.append(audit_row(
        "population_accounting",
        "PASS_POPULATION_ACCOUNTING" if accounting_ok else "FAIL_POPULATION_ACCOUNTING",
        (
            f"rows={summary.get('population_rows')}, templates={summary.get('template_available_rows')}, "
            f"staging_written={summary.get('payload_staging_written_rows')}, populated={summary.get('payload_staging_populated_rows')}, "
            f"accepted={summary.get('payload_accepted_rows')}"
        ),
        accounting_ok,
        "population packet should declare 66 obligations with zero staging writes, population, or accepted rows",
    ))

    firewall_ok = (
        all(row.get("population_packet_declared") == "true" for row in pop_rows)
        and all(row.get("payload_staging_written") == "false" for row in pop_rows)
        and all(row.get("payload_staging_populated") == "false" for row in pop_rows)
        and all(row.get("payload_accepted") == "false" for row in pop_rows)
        and all(row.get("can_execute_after_population") == "false" for row in pop_rows)
        and all(row.get("checker_executed") == "false" for row in pop_rows)
        and all(row.get("certificate_passed") == "false" for row in pop_rows)
        and all(row.get("domain_object_accepted") == "false" for row in pop_rows)
        and all(row.get("allows_concrete_R_CMB") == "false" for row in pop_rows)
        and all(row.get("allows_score_entry") == "false" for row in pop_rows)
        and all(row.get("allows_likelihood") == "false" for row in pop_rows)
        and all(row.get("allows_dark_sector_verdict") == "false" for row in pop_rows)
        and summary.get("concrete_R_CMB_allowed") is False
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )
    rows.append(audit_row(
        "promotion_firewall",
        "PASS_POPULATION_FIREWALL_CLOSED" if firewall_ok else "FAIL_POPULATION_FIREWALL",
        "population packet does not open staging write, acceptance, execution, R_CMB, score, likelihood, or verdict",
        firewall_ok,
        "population packet must not promote obligations to populated or accepted payloads",
    ))

    rows.append(audit_row(
        "staging_population",
        "BLOCKED_STAGING_PAYLOADS_NOT_POPULATED",
        "payload_staging files are declared as targets but remain unpopulated",
        False,
        "requires endpoint-blind population of payload_staging files",
    ))
    rows.append(audit_row(
        "binding_checks",
        "BLOCKED_BINDINGS_NOT_AVAILABLE",
        "hash, provenance, replay, and firewall bindings cannot pass before staging population",
        False,
        "requires populated staging files and binding audit",
    ))
    rows.append(audit_row(
        "payload_acceptance",
        "BLOCKED_ACCEPTANCE_AUDIT_NOT_AVAILABLE",
        "payloads cannot be accepted before population and binding checks",
        False,
        "requires populated staging files and acceptance audit",
    ))
    rows.append(audit_row(
        "checker_execution_and_R_CMB",
        "BLOCKED_EXECUTION_AND_R_CMB",
        "checker execution, certificate pass, domain acceptance, and concrete R_CMB remain downstream",
        False,
        "requires accepted payloads before checker execution and downstream certificates",
    ))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(row["audit_passed"]) for row in rows)
    blocked = sum(row["audit_status"].startswith("BLOCKED") for row in rows)
    failed = sum(row["audit_status"].startswith("FAIL") for row in rows)
    clean = failed == 0
    return {
        "report_id": "tau_cmb_carrier_domain_checker_input_payload_staging_population_packet_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_table": rel(POP_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "staging_population_packet_audited": clean,
        "staging_population_allowed": False,
        "payload_acceptance_allowed": False,
        "checker_execution_allowed": False,
        "carrier_certificate_allowed": False,
        "domain_certificate_allowed": False,
        "domain_object_acceptance_allowed": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_STAGING_POPULATION_PACKET_AUDITED_NOT_POPULATED"
            if clean
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_STAGING_POPULATION_PACKET_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_checker_input_payload_staging_population_execution_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{row['component']}`: {row['audit_status']} | {row['finding']}"
        for row in report["audit_rows"]
    )
    text = f"""# Tau CMB Carrier Domain Checker Input Payload Staging Population Packet Audit v01

**Doc class:** carrier/domain checker input payload staging population packet audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit verifies that the staging-population packet declares endpoint-blind
Tau-side source rules and acceptance gates while leaving `payload_staging/`
unpopulated. It does not populate staging files, accept payloads, execute
checkers, pass certificates, accept domain objects, materialize `R_CMB`, open
score entry, compute a likelihood, or decide the dark-sector question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The population route is declared and auditable, but the staging payloads remain
absent.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB carrier/domain checker input payload staging population packet.")
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    report = build_report()
    if args.write_report:
        report_path = Path(args.write_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), report)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
