#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQUEST_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_request_v01.csv"
REQUEST_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_request_audit_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_fulfillment_packet_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_checker_input_payload_fulfillment_packet_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_checker_input_payload_fulfillment_packet_v01.md"

PAYLOAD_ROOT = ROOT / "payload_staging/tau_cmb_carrier_domain_checker_input_payloads"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_checker_input_payload_fulfillment_packet_v01_"
    "fulfillment_packet_only_payloads_not_accepted_no_checker_execution_"
    "no_certificate_pass_no_domain_acceptance_no_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "fulfillment_row_id",
    "source_request_row_id",
    "certificate_area",
    "checker_name",
    "payload_bundle_root",
    "requested_payload_paths",
    "requested_replay_paths",
    "requested_provenance_paths",
    "requested_hash_paths",
    "requested_firewall_paths",
    "payload_files_present",
    "replay_files_present",
    "provenance_files_present",
    "hash_files_present",
    "firewall_files_present",
    "all_required_files_present",
    "fulfillment_packet_declared",
    "payload_supplied",
    "replay_supplied",
    "provenance_supplied",
    "hash_supplied",
    "firewall_supplied",
    "payload_accepted",
    "can_execute_after_fulfillment",
    "checker_executed",
    "certificate_passed",
    "domain_object_accepted",
    "allows_concrete_R_CMB",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "current_fulfillment_status",
    "blocking_reason",
    "claim_boundary",
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def split_files(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def paths_for(area: str, value: str) -> list[Path]:
    return [PAYLOAD_ROOT / area / name for name in split_files(value)]


def joined_rel(paths: list[Path]) -> str:
    return "; ".join(rel(path) for path in paths)


def all_present(paths: list[Path]) -> bool:
    return bool(paths) and all(path.exists() for path in paths)


def table_rows() -> list[dict[str, str]]:
    request_rows = read_csv(REQUEST_TABLE)
    rows: list[dict[str, str]] = []
    for index, request in enumerate(request_rows, start=1):
        area = request["certificate_area"]
        payload_paths = paths_for(area, request["requested_payload_files"])
        replay_paths = paths_for(area, request["requested_replay_files"])
        provenance_paths = paths_for(area, request["requested_provenance_files"])
        hash_paths = paths_for(area, request["requested_hash_files"])
        firewall_paths = paths_for(area, request["requested_firewall_files"])

        payload_present = all_present(payload_paths)
        replay_present = all_present(replay_paths)
        provenance_present = all_present(provenance_paths)
        hash_present = all_present(hash_paths)
        firewall_present = all_present(firewall_paths)
        complete = all(
            [payload_present, replay_present, provenance_present, hash_present, firewall_present]
        )
        rows.append(
            {
                "fulfillment_row_id": f"TCMBCDIFP01_{index:03d}",
                "source_request_row_id": request["request_row_id"],
                "certificate_area": area,
                "checker_name": request["checker_name"],
                "payload_bundle_root": rel(PAYLOAD_ROOT / area),
                "requested_payload_paths": joined_rel(payload_paths),
                "requested_replay_paths": joined_rel(replay_paths),
                "requested_provenance_paths": joined_rel(provenance_paths),
                "requested_hash_paths": joined_rel(hash_paths),
                "requested_firewall_paths": joined_rel(firewall_paths),
                "payload_files_present": str(payload_present).lower(),
                "replay_files_present": str(replay_present).lower(),
                "provenance_files_present": str(provenance_present).lower(),
                "hash_files_present": str(hash_present).lower(),
                "firewall_files_present": str(firewall_present).lower(),
                "all_required_files_present": str(complete).lower(),
                "fulfillment_packet_declared": "true",
                "payload_supplied": str(payload_present).lower(),
                "replay_supplied": str(replay_present).lower(),
                "provenance_supplied": str(provenance_present).lower(),
                "hash_supplied": str(hash_present).lower(),
                "firewall_supplied": str(firewall_present).lower(),
                "payload_accepted": "false",
                "can_execute_after_fulfillment": "false",
                "checker_executed": "false",
                "certificate_passed": "false",
                "domain_object_accepted": "false",
                "allows_concrete_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "current_fulfillment_status": (
                    "INPUT_PAYLOAD_FILES_PRESENT_AWAITING_ACCEPTANCE_AUDIT"
                    if complete
                    else "INPUT_PAYLOAD_FULFILLMENT_PACKET_DECLARED_FILES_ABSENT_OR_INCOMPLETE"
                ),
                "blocking_reason": (
                    "all requested file categories are present but acceptance audit is still required"
                    if complete
                    else "one or more requested payload, replay, provenance, hash, or firewall files are absent"
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
    request_audit = load_json(REQUEST_AUDIT) if REQUEST_AUDIT.exists() else {}
    input_ok = (
        request_audit.get("status")
        == "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_REQUEST_AUDITED_UNFULFILLED_NOT_EXECUTABLE"
        and request_audit.get("failed_rows") == 0
        and REQUEST_TABLE.exists()
    )
    complete_rows = sum(row["all_required_files_present"] == "true" for row in rows)
    supplied_rows = sum(
        row["payload_supplied"] == "true"
        and row["replay_supplied"] == "true"
        and row["provenance_supplied"] == "true"
        and row["hash_supplied"] == "true"
        and row["firewall_supplied"] == "true"
        for row in rows
    )
    return {
        "report_id": "tau_cmb_carrier_domain_checker_input_payload_fulfillment_packet_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_request_table": rel(REQUEST_TABLE),
        "input_request_audit": rel(REQUEST_AUDIT),
        "input_chain_clean": input_ok,
        "fulfillment_rows": len(rows),
        "fulfillment_packets_declared": sum(row["fulfillment_packet_declared"] == "true" for row in rows),
        "complete_file_bundle_rows": complete_rows,
        "fully_supplied_rows": supplied_rows,
        "payload_accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
        "can_execute_after_fulfillment_rows": sum(row["can_execute_after_fulfillment"] == "true" for row in rows),
        "checker_executed_rows": sum(row["checker_executed"] == "true" for row in rows),
        "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
        "accepted_domain_objects": sum(row["domain_object_accepted"] == "true" for row in rows),
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_FULFILLMENT_PACKET_DECLARED_INCOMPLETE"
            if input_ok and complete_rows < len(rows)
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_FULFILLMENT_PACKET_DECLARED_AWAITING_ACCEPTANCE_AUDIT"
            if input_ok
            else "CARRIER_DOMAIN_CHECKER_INPUT_PAYLOAD_FULFILLMENT_PACKET_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "audit_tau_cmb_carrier_domain_checker_input_payload_fulfillment_packet_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        (
            f"- `{row['certificate_area']}`: {row['current_fulfillment_status']} | "
            f"complete={row['all_required_files_present']} | accepted={row['payload_accepted']} | "
            f"blocks: {row['blocking_reason']}"
        )
        for row in rows
    )
    text = f"""# Tau CMB Carrier Domain Checker Input Payload Fulfillment Packet v01

**Doc class:** carrier/domain checker input payload fulfillment packet
**Reader role:** Paper 13 / CMB readout route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This packet maps each audited checker input-payload request to concrete
payload-staging file paths. It may detect whether files are present, but it
does not accept payloads, execute checkers, pass certificates, accept domain
objects, materialize `R_CMB`, open score entry, compute a likelihood, or decide
the dark-sector question.

## Fulfillment Rows

{row_text}

## Summary

```text
fulfillment_rows={summary["fulfillment_rows"]}
complete_file_bundle_rows={summary["complete_file_bundle_rows"]}
fully_supplied_rows={summary["fully_supplied_rows"]}
payload_accepted_rows={summary["payload_accepted_rows"]}
can_execute_after_fulfillment_rows={summary["can_execute_after_fulfillment_rows"]}
checker_executed_rows={summary["checker_executed_rows"]}
certificate_passed_rows={summary["certificate_passed_rows"]}
accepted_domain_objects={summary["accepted_domain_objects"]}
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
    parser = argparse.ArgumentParser(description="Build Tau CMB carrier/domain checker input payload fulfillment packet.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = table_rows()
    table_path = Path(args.write_table) if args.write_table else DEFAULT_TABLE
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
