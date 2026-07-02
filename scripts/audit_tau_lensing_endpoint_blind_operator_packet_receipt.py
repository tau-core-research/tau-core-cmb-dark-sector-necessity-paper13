#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQUEST = ROOT / "data/derived/cmb_tau_lensing_endpoint_blind_operator_packet_request_v01.csv"
SUBMISSION = ROOT / "payloads/cmb_tau_lensing_endpoint_blind_operator_packet_submission_v01.csv"
TEMPLATE = ROOT / "payload_templates/cmb_tau_lensing_endpoint_blind_operator_packet_submission_TEMPLATE_v01.csv"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_endpoint_blind_operator_packet_receipt_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_endpoint_blind_operator_packet_receipt_audit_v01.md"


REQUIRED_COLUMNS = {
    "packet_slot",
    "supplied_object",
    "evidence_artifact",
    "provenance_hash",
    "endpoint_blind_attestation",
}


def is_placeholder(value: str) -> bool:
    text = str(value or "").strip()
    return not text or text.startswith("TODO_") or "template row" in text.lower()


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def build_report(submission_path: Path = SUBMISSION) -> dict[str, Any]:
    request_rows = read_csv(REQUEST)
    submission_rows = read_csv(submission_path)
    request_slots = {row.get("packet_slot", "") for row in request_rows}
    supplied_slots = {row.get("packet_slot", "") for row in submission_rows}
    missing_slots = sorted(slot for slot in request_slots if slot and slot not in supplied_slots)
    placeholder_rows: list[str] = []
    missing_evidence_artifacts: list[str] = []
    if not submission_path.exists():
        status = "OPERATOR_PACKET_RECEIPT_AUDIT_BLOCKED_NO_SUBMISSION"
        decision = "DO_NOT_SCORE_NO_ENDPOINT_BLIND_OPERATOR_PACKET_SUPPLIED"
        missing_columns: list[str] = []
    else:
        columns = set(submission_rows[0].keys()) if submission_rows else set()
        missing_columns = sorted(REQUIRED_COLUMNS - columns)
        if not missing_columns:
            for row in submission_rows:
                slot = row.get("packet_slot", "")
                content_fields = [
                    "supplied_object",
                    "evidence_artifact",
                    "provenance_hash",
                    "endpoint_blind_attestation",
                ]
                if any(is_placeholder(row.get(field, "")) for field in content_fields):
                    placeholder_rows.append(slot)
                artifact = row.get("evidence_artifact", "").strip()
                if artifact and not artifact.startswith("TODO_"):
                    artifact_path = ROOT / artifact
                    if not artifact_path.exists():
                        missing_evidence_artifacts.append(slot)
        status = "OPERATOR_PACKET_RECEIPT_AUDIT_BLOCKED_INCOMPLETE_SUBMISSION"
        decision = "DO_NOT_SCORE_INCOMPLETE_ENDPOINT_BLIND_OPERATOR_PACKET"
        if placeholder_rows:
            status = "OPERATOR_PACKET_RECEIPT_AUDIT_BLOCKED_TEMPLATE_PLACEHOLDERS_PRESENT"
            decision = "DO_NOT_SCORE_TEMPLATE_PLACEHOLDERS_PRESENT"
        elif missing_evidence_artifacts:
            status = "OPERATOR_PACKET_RECEIPT_AUDIT_BLOCKED_MISSING_EVIDENCE_ARTIFACTS"
            decision = "DO_NOT_SCORE_MISSING_EVIDENCE_ARTIFACTS"
        elif not missing_slots and not missing_columns:
            status = "OPERATOR_PACKET_RECEIPT_AUDIT_READY_FOR_CONTENT_AUDITS"
            decision = "ROUTE_TO_CONTENT_AUDITS_NOT_SCORE"
    return {
        "report_id": "cmb_tau_lensing_endpoint_blind_operator_packet_receipt_audit_v01",
        "claim_boundary": "endpoint_blind_operator_packet_receipt_audit_only_no_operator_acceptance_no_grid_no_score_no_dark_sector_verdict",
        "request": rel(REQUEST),
        "submission_template": rel(TEMPLATE),
        "expected_submission": rel(SUBMISSION),
        "audited_submission": rel(submission_path),
        "status": status,
        "decision": decision,
        "requested_slots": sorted(request_slots),
        "supplied_slots": sorted(supplied_slots),
        "missing_slots": missing_slots,
        "missing_required_columns": missing_columns,
        "placeholder_rows": sorted(placeholder_rows),
        "missing_evidence_artifact_rows": sorted(missing_evidence_artifacts),
        "next_if_ready": [
            "endpoint_blind_operator_packet_content_audit_router",
        ],
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(report: dict[str, Any], path: Path) -> None:
    missing = "\n".join(f"- `{item}`" for item in report["missing_slots"]) or "- none"
    placeholders = "\n".join(f"- `{item}`" for item in report["placeholder_rows"]) or "- none"
    missing_artifacts = "\n".join(f"- `{item}`" for item in report["missing_evidence_artifact_rows"]) or "- none"
    next_steps = "\n".join(f"- `{item}`" for item in report["next_if_ready"])
    text = f"""# CMB Tau Lensing Endpoint-Blind Operator Packet Receipt Audit v01

**Doc class:** endpoint-blind operator packet receipt audit
**Reader role:** Paper 13 Tau-grid implementer
**Status:** {report["status"]}
**Canonical parent:** `docs/cmb_tau_lensing_endpoint_blind_operator_packet_request_v01.md`

## Claim Boundary

```text
{report["claim_boundary"]}
```

## Decision

```text
{report["decision"]}
```

## Expected Submission

```text
{report["expected_submission"]}
```

## Audited Submission

```text
{report["audited_submission"]}
```

## Submission Template

```text
{report["submission_template"]}
```

## Missing Slots

{missing}

## Placeholder Rows

{placeholders}

## Missing Evidence Artifact Rows

{missing_artifacts}

## Next Audits If Receipt Is Complete

{next_steps}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit endpoint-blind operator packet receipt.")
    parser.add_argument("--submission", default=str(SUBMISSION))
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    report = build_report(Path(args.submission))
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if args.write_doc:
        write_doc(report, Path(args.write_doc))
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
