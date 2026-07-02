#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MATERIALIZATION_REPORT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_materialization_packet_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_materialization_packet_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_materialization_packet_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_materialization_packet_audit_v01_"
    "audit_only_source_artifact_candidates_materialized_not_accepted_no_staging_write_no_payload_acceptance_"
    "no_checker_execution_no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict"
)


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_row(component: str, status: str, finding: str, passed: bool, blocking_reason: str) -> dict[str, Any]:
    return {
        "component": component,
        "audit_status": status,
        "finding": finding,
        "audit_passed": passed,
        "blocking_reason": blocking_reason,
    }


def build_report() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    if not MATERIALIZATION_REPORT.exists():
        rows.append(audit_row(rel(MATERIALIZATION_REPORT), "FAIL_MISSING_ARTIFACT", "materialization report is absent", False, "audit package incomplete"))
        return finalize(rows)

    report = load_json(MATERIALIZATION_REPORT)
    materialized = report.get("materialized_rows", [])

    input_ok = (
        report.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_CANDIDATES_MATERIALIZED_NOT_ACCEPTED"
        and report.get("input_chain_clean") is True
        and report.get("requested_rows") == 66
        and report.get("source_artifact_bundles_materialized") == 66
    )
    rows.append(audit_row(
        "input_and_row_count",
        "PASS_MATERIALIZATION_INPUT_AND_ROW_COUNT" if input_ok else "FAIL_MATERIALIZATION_INPUT_OR_ROW_COUNT",
        f"requested={report.get('requested_rows')}, materialized={report.get('source_artifact_bundles_materialized')}",
        input_ok,
        "materialization requires clean input chain and 66 materialized bundles",
    ))

    files_ok = True
    missing: list[str] = []
    for row in materialized:
        for key in ["artifact", "hash", "provenance", "replay", "firewall"]:
            path = Path(row[key])
            if not path.exists():
                files_ok = False
                missing.append(str(path))
    rows.append(audit_row(
        "bundle_files_present",
        "PASS_ALL_SOURCE_BUNDLE_FILES_PRESENT" if files_ok else "FAIL_SOURCE_BUNDLE_FILES_MISSING",
        "all artifact/hash/provenance/replay/firewall files exist" if files_ok else f"missing={missing[:5]}",
        files_ok,
        "all source bundle files must exist",
    ))

    hash_ok = True
    bad_hashes: list[str] = []
    for row in materialized:
        hash_doc = load_json(Path(row["hash"]))
        files = hash_doc.get("files", {})
        for raw_path, expected_hash in files.items():
            path = Path(raw_path)
            if not path.exists() or sha256(path) != expected_hash:
                hash_ok = False
                bad_hashes.append(raw_path)
    rows.append(audit_row(
        "hash_binding",
        "PASS_SOURCE_BUNDLE_HASH_BINDING" if hash_ok else "FAIL_SOURCE_BUNDLE_HASH_BINDING",
        "hash manifests match artifact, provenance, replay, and firewall files" if hash_ok else f"bad_hashes={bad_hashes[:5]}",
        hash_ok,
        "hash manifests must bind all source bundle files",
    ))

    provenance_ok = all(row.get("missing_source_reference_count") == 0 for row in materialized)
    rows.append(audit_row(
        "source_inventory",
        "PASS_SOURCE_INVENTORY_REFERENCES_EXIST" if provenance_ok else "FAIL_SOURCE_INVENTORY_REFERENCES",
        "all source inventory references exist",
        provenance_ok,
        "source artifacts must not cite missing local source references",
    ))

    boundary_ok = True
    bad_boundary: list[str] = []
    for row in materialized:
        for key in ["artifact", "hash", "provenance", "replay", "firewall"]:
            payload = load_json(Path(row[key]))
            if (
                payload.get("claim_boundary") != report.get("claim_boundary")
                or payload.get("source_artifact_accepted", False) is True
                or payload.get("staging_population_allowed", False) is True
            ):
                if key == "artifact":
                    permissions = payload.get("acceptance_permissions", {})
                    if permissions.get("source_artifact_accepted") is False and permissions.get("staging_population_allowed") is False:
                        continue
                boundary_ok = False
                bad_boundary.append(row[key])
    rows.append(audit_row(
        "claim_boundary",
        "PASS_SOURCE_MATERIALIZATION_CLAIM_BOUNDARY" if boundary_ok else "FAIL_SOURCE_MATERIALIZATION_CLAIM_BOUNDARY",
        "all bundle files preserve not-accepted/no-staging boundary" if boundary_ok else f"bad_boundary={bad_boundary[:5]}",
        boundary_ok,
        "materialized source candidates must remain unaccepted and non-staging",
    ))

    firewall_ok = (
        report.get("source_artifact_accepted_rows") == 0
        and report.get("staging_population_allowed_rows") == 0
        and report.get("payload_staging_written_rows") == 0
        and report.get("payload_accepted_rows") == 0
        and report.get("checker_executed_rows") == 0
        and report.get("certificate_passed_rows") == 0
        and report.get("accepted_domain_objects") == 0
        and report.get("concrete_R_CMB_allowed") is False
        and report.get("score_entry_allowed") is False
        and report.get("likelihood_allowed") is False
        and report.get("dark_sector_verdict_allowed") is False
    )
    rows.append(audit_row(
        "promotion_firewall",
        "PASS_SOURCE_MATERIALIZATION_FIREWALL_CLOSED" if firewall_ok else "FAIL_SOURCE_MATERIALIZATION_FIREWALL",
        "materialization does not open acceptance, staging, execution, R_CMB, score, likelihood, or verdict",
        firewall_ok,
        "source materialization must not promote candidates to accepted/staging status",
    ))

    rows.append(audit_row("source_acceptance", "BLOCKED_SOURCE_ACCEPTANCE_NOT_AVAILABLE", "source candidates are materialized but not accepted", False, "requires source artifact acceptance audit"))
    rows.append(audit_row("staging_population", "BLOCKED_STAGING_POPULATION_NOT_ALLOWED", "staging population remains blocked until source candidates are accepted", False, "requires accepted source artifacts before staging population"))
    rows.append(audit_row("checker_execution_and_R_CMB", "BLOCKED_CHECKERS_AND_R_CMB", "checker execution, certificate pass, domain acceptance, and concrete R_CMB remain downstream", False, "requires accepted payloads before checker execution and downstream certificates"))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(row["audit_passed"]) for row in rows)
    blocked = sum(row["audit_status"].startswith("BLOCKED") for row in rows)
    failed = sum(row["audit_status"].startswith("FAIL") for row in rows)
    clean = failed == 0
    return {
        "report_id": "tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_materialization_packet_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_report": rel(MATERIALIZATION_REPORT),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "source_artifact_materialization_audited": clean,
        "source_artifact_acceptance_allowed": False,
        "staging_population_allowed": False,
        "payload_acceptance_allowed": False,
        "checker_execution_allowed": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_MATERIALIZATION_AUDITED_NOT_ACCEPTED"
            if clean
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_ENDPOINT_BLIND_SOURCE_ARTIFACT_MATERIALIZATION_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_acceptance_audit_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(f"- `{row['component']}`: {row['audit_status']} | {row['finding']}" for row in report["audit_rows"])
    text = f"""# Tau CMB Carrier Domain Checker Input Payload Endpoint-Blind Source Artifact Materialization Packet Audit v01

**Doc class:** carrier/domain checker input payload endpoint-blind source artifact materialization audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit verifies that endpoint-blind Tau-side source artifact candidate
bundles were materialized, hash-bound, provenance/replay/firewall accompanied,
and kept unaccepted. It does not populate `payload_staging/`, accept payloads,
execute checkers, pass certificates, accept domain objects, materialize
`R_CMB`, open score entry, compute a likelihood, or decide the dark-sector
question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The source candidates are present and auditable, but source acceptance remains
blocked.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB endpoint-blind source artifact materialization packet.")
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
