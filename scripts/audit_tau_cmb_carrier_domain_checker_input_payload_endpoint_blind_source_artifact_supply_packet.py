#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUPPLY_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_supply_packet_v01.csv"
SUPPLY_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_supply_packet_summary_v01.json"
REQUEST_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_request_audit_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_supply_packet_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_supply_packet_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_supply_packet_audit_v01_"
    "audit_only_supply_packet_clean_but_bundle_absent_no_source_acceptance_no_staging_write_"
    "no_payload_acceptance_no_checker_execution_no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict"
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
    required = [SUPPLY_TABLE, SUPPLY_SUMMARY, REQUEST_AUDIT]
    missing = [path for path in required if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(audit_row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    supply_rows = read_csv(SUPPLY_TABLE)
    summary = load_json(SUPPLY_SUMMARY)
    request_audit = load_json(REQUEST_AUDIT)

    shape_ok = len(supply_rows) == 66 and {row.get("file_category") for row in supply_rows} == {"payload", "replay", "provenance", "hash", "firewall"}
    rows.append(audit_row(
        "supply_row_shape",
        "PASS_EXPECTED_SOURCE_SUPPLY_ROWS_PRESENT" if shape_ok else "FAIL_SOURCE_SUPPLY_ROW_SHAPE",
        f"rows={len(supply_rows)}",
        shape_ok,
        "source artifact supply packet requires 66 rows across the five file categories",
    ))

    input_ok = (
        summary.get("status")
        in {
            "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_SUPPLY_PACKET_DECLARED_BUNDLE_ABSENT",
            "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_SUPPLY_PACKET_DECLARED_AWAITING_ACCEPTANCE_AUDIT",
        }
        and summary.get("input_chain_clean") is True
        and request_audit.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_REQUEST_AUDITED_NOT_SUPPLIED"
        and request_audit.get("failed_rows") == 0
    )
    rows.append(audit_row(
        "input_request_chain",
        "PASS_SOURCE_SUPPLY_INPUT_CHAIN" if input_ok else "FAIL_SOURCE_SUPPLY_INPUT_CHAIN",
        "source supply packet follows a clean audited source artifact request",
        input_ok,
        "source supply audit must be downstream of a clean source artifact request audit",
    ))

    all_absent = (
        all(row.get("source_artifact_present") == "false" for row in supply_rows)
        and all(row.get("source_hash_present") == "false" for row in supply_rows)
        and all(row.get("source_replay_present") == "false" for row in supply_rows)
        and all(row.get("source_provenance_present") == "false" for row in supply_rows)
        and all(row.get("source_firewall_present") == "false" for row in supply_rows)
        and all(row.get("complete_source_bundle_present") == "false" for row in supply_rows)
    )
    all_present = (
        all(row.get("source_artifact_present") == "true" for row in supply_rows)
        and all(row.get("source_hash_present") == "true" for row in supply_rows)
        and all(row.get("source_replay_present") == "true" for row in supply_rows)
        and all(row.get("source_provenance_present") == "true" for row in supply_rows)
        and all(row.get("source_firewall_present") == "true" for row in supply_rows)
        and all(row.get("complete_source_bundle_present") == "true" for row in supply_rows)
    )
    presence_ok = all_absent or all_present
    rows.append(audit_row(
        "source_bundle_presence",
        "PASS_SOURCE_BUNDLES_PRESENT_AWAITING_ACCEPTANCE" if all_present else "PASS_SOURCE_BUNDLES_ABSENT_AS_DECLARED" if all_absent else "FAIL_SOURCE_BUNDLE_PRESENCE_MISMATCH",
        "all source artifact bundles are present but unaccepted" if all_present else "all source artifact bundles are absent" if all_absent else "partial source artifact file presence detected",
        presence_ok,
        "supply packet must accurately reflect source artifact file presence",
    ))

    present_rows = summary.get("complete_source_bundle_present_rows")
    accounting_ok = (
        summary.get("supply_rows") == 66
        and summary.get("source_artifact_present_rows") == present_rows
        and present_rows in {0, 66}
        and summary.get("source_artifact_supplied_rows") == present_rows
        and summary.get("source_bundle_supplied_rows") == present_rows
        and summary.get("source_artifact_accepted_rows") == 0
        and summary.get("staging_population_allowed_rows") == 0
        and summary.get("payload_staging_written_rows") == 0
        and summary.get("payload_accepted_rows") == 0
        and summary.get("checker_executed_rows") == 0
        and summary.get("certificate_passed_rows") == 0
        and summary.get("accepted_domain_objects") == 0
    )
    rows.append(audit_row(
        "source_supply_accounting",
        "PASS_SOURCE_SUPPLY_ACCOUNTING" if accounting_ok else "FAIL_SOURCE_SUPPLY_ACCOUNTING",
        (
            f"rows={summary.get('supply_rows')}, present={summary.get('source_artifact_present_rows')}, "
            f"complete={summary.get('complete_source_bundle_present_rows')}, accepted={summary.get('source_artifact_accepted_rows')}, "
            f"staging_allowed={summary.get('staging_population_allowed_rows')}"
        ),
        accounting_ok,
        "source supply packet should declare either zero or complete bundle presence with zero accepted or staging-allowed rows",
    ))

    firewall_ok = (
        all(row.get("source_artifact_accepted") == "false" for row in supply_rows)
        and all(row.get("staging_population_allowed") == "false" for row in supply_rows)
        and all(row.get("payload_staging_written") == "false" for row in supply_rows)
        and all(row.get("payload_accepted") == "false" for row in supply_rows)
        and all(row.get("checker_executed") == "false" for row in supply_rows)
        and all(row.get("certificate_passed") == "false" for row in supply_rows)
        and all(row.get("domain_object_accepted") == "false" for row in supply_rows)
        and all(row.get("allows_concrete_R_CMB") == "false" for row in supply_rows)
        and all(row.get("allows_score_entry") == "false" for row in supply_rows)
        and all(row.get("allows_likelihood") == "false" for row in supply_rows)
        and all(row.get("allows_dark_sector_verdict") == "false" for row in supply_rows)
        and summary.get("concrete_R_CMB_allowed") is False
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )
    rows.append(audit_row(
        "promotion_firewall",
        "PASS_SOURCE_SUPPLY_FIREWALL_CLOSED" if firewall_ok else "FAIL_SOURCE_SUPPLY_FIREWALL",
        "source supply packet does not open source acceptance, staging population, payload acceptance, R_CMB, score, likelihood, or verdict",
        firewall_ok,
        "source supply packet must not promote absent artifacts to accepted/staging status",
    ))

    boundary_ok = all(
        "supply_packet_only" in row.get("claim_boundary", "")
        and "source_artifacts_not_supplied" in row.get("claim_boundary", "")
        and "no_source_acceptance" in row.get("claim_boundary", "")
        and "no_staging_write" in row.get("claim_boundary", "")
        and "no_payload_acceptance" in row.get("claim_boundary", "")
        and "no_score" in row.get("claim_boundary", "")
        and "no_likelihood" in row.get("claim_boundary", "")
        and "no_verdict" in row.get("claim_boundary", "")
        for row in supply_rows
    )
    rows.append(audit_row(
        "claim_boundary",
        "PASS_SOURCE_SUPPLY_CLAIM_BOUNDARY" if boundary_ok else "FAIL_SOURCE_SUPPLY_CLAIM_BOUNDARY",
        "row claim boundaries mark supply-packet-only source artifacts with no acceptance/staging/score/verdict",
        boundary_ok,
        "source supply packet must preserve supply-only no-acceptance boundary",
    ))

    if all_present:
        rows.append(audit_row("source_artifact_materialization", "PASS_SOURCE_ARTIFACTS_MATERIALIZED_UNACCEPTED", "endpoint-blind Tau-side source artifact bundles are materialized but unaccepted", True, "requires source artifact acceptance audit before staging population"))
    else:
        rows.append(audit_row("source_artifact_materialization", "BLOCKED_SOURCE_ARTIFACTS_ABSENT", "endpoint-blind Tau-side source artifact bundles are absent", False, "requires source artifact materialization or explicit impossibility record"))
    rows.append(audit_row("source_artifact_acceptance", "BLOCKED_SOURCE_ACCEPTANCE_NOT_AVAILABLE", "source artifacts cannot be accepted before materialization, hash, replay, provenance, and firewall checks", False, "requires source artifact receipt and acceptance audit"))
    rows.append(audit_row("staging_population", "BLOCKED_STAGING_POPULATION_NOT_ALLOWED", "staging population remains blocked until source artifacts are accepted", False, "requires accepted endpoint-blind source artifacts before staging population"))
    rows.append(audit_row("checker_execution_and_R_CMB", "BLOCKED_CHECKERS_AND_R_CMB", "checker execution, certificate pass, domain acceptance, and concrete R_CMB remain downstream", False, "requires accepted payloads before checker execution and downstream certificates"))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(row["audit_passed"]) for row in rows)
    blocked = sum(row["audit_status"].startswith("BLOCKED") for row in rows)
    failed = sum(row["audit_status"].startswith("FAIL") for row in rows)
    clean = failed == 0
    return {
        "report_id": "tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_supply_packet_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_table": rel(SUPPLY_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "source_artifact_supply_packet_audited": clean,
        "source_artifact_materialization_allowed": False,
        "source_artifact_acceptance_allowed": False,
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
            "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_SUPPLY_PACKET_AUDITED"
            if clean
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_SUPPLY_PACKET_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_acceptance_audit_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(f"- `{row['component']}`: {row['audit_status']} | {row['finding']}" for row in report["audit_rows"])
    text = f"""# Tau CMB Carrier Domain Checker Input Payload Endpoint-Blind Source Artifact Supply Packet Audit v01

**Doc class:** carrier/domain checker input payload endpoint-blind source artifact supply packet audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks whether requested endpoint-blind Tau-side source artifact
bundles are present. It confirms that they remain absent and that no source
acceptance, staging population, payload acceptance, checker execution,
certificate pass, concrete `R_CMB`, score, likelihood, or dark-sector verdict
is opened.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The source supply packet is auditable, but the requested endpoint-blind
Tau-side source artifact bundles are absent.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB checker input endpoint-blind source artifact supply packet.")
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
