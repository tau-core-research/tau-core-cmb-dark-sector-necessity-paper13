#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQUEST = ROOT / "data/derived/cmb_tau_lensing_endpoint_blind_operator_packet_request_v01.csv"
DEFAULT_TEMPLATE = ROOT / "payload_templates/cmb_tau_lensing_endpoint_blind_operator_packet_submission_TEMPLATE_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/cmb_tau_lensing_endpoint_blind_operator_packet_submission_template_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_endpoint_blind_operator_packet_submission_template_v01.md"


FIELDNAMES = [
    "packet_slot",
    "supplied_object",
    "evidence_artifact",
    "provenance_hash",
    "endpoint_blind_attestation",
    "dimension_status",
    "zero_source_status",
    "replay_status",
    "firewall_status",
    "notes",
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_request_slots(path: Path) -> list[str]:
    with path.open(newline="") as handle:
        return [row["packet_slot"] for row in csv.DictReader(handle)]


def write_template(path: Path, slots: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for slot in slots:
            writer.writerow(
                {
                    "packet_slot": slot,
                    "supplied_object": "TODO_ENDPOINT_BLIND_OBJECT",
                    "evidence_artifact": "TODO_RELATIVE_PATH",
                    "provenance_hash": "TODO_SHA256_OR_EQUIVALENT",
                    "endpoint_blind_attestation": "TODO_PRE_ENDPOINT_COMPARISON_ATTESTATION",
                    "dimension_status": "TODO_PASS_OR_BLOCKED",
                    "zero_source_status": "TODO_PASS_OR_BLOCKED_OR_NOT_APPLICABLE",
                    "replay_status": "TODO_PASS_OR_BLOCKED_OR_NOT_APPLICABLE",
                    "firewall_status": "TODO_PASS_OR_BLOCKED",
                    "notes": "template row; do not treat as submitted evidence",
                }
            )


def build_summary(template_path: Path, slots: list[str]) -> dict[str, Any]:
    return {
        "report_id": "cmb_tau_lensing_endpoint_blind_operator_packet_submission_template_summary_v01",
        "claim_boundary": "endpoint_blind_operator_packet_submission_template_only_no_submission_no_operator_acceptance_no_grid_no_score_no_dark_sector_verdict",
        "template": rel(template_path),
        "status": "SUBMISSION_TEMPLATE_DECLARED_NOT_SUBMITTED",
        "intended_submission_path": "payloads/cmb_tau_lensing_endpoint_blind_operator_packet_submission_v01.csv",
        "rows": len(slots),
        "packet_slots": slots,
        "required_columns": FIELDNAMES,
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(summary: dict[str, Any], path: Path) -> None:
    columns = "\n".join(f"- `{item}`" for item in summary["required_columns"])
    slots = "\n".join(f"- `{item}`" for item in summary["packet_slots"])
    text = f"""# CMB Tau Lensing Endpoint-Blind Operator Packet Submission Template v01

**Doc class:** endpoint-blind operator packet submission template
**Reader role:** Paper 13 Tau-grid implementer
**Status:** template only; not submitted; not accepted; not a score
**Canonical parent:** `docs/cmb_tau_lensing_endpoint_blind_operator_packet_request_v01.md`

## Claim Boundary

```text
{summary["claim_boundary"]}
```

## Template Path

```text
{summary["template"]}
```

## Intended Submission Path

```text
{summary["intended_submission_path"]}
```

## Required Columns

{columns}

## Required Packet Slots

{slots}

## Use Rule

Copying this template into the intended submission path is not acceptance. The
template rows must be replaced by actual endpoint-blind evidence artifacts and
then pass receipt, content, replay, zero-source, dimension/sign, and firewall
audits before any score attempt can be considered.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build endpoint-blind operator packet submission template.")
    parser.add_argument("--write-template", nargs="?", const=str(DEFAULT_TEMPLATE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    slots = read_request_slots(REQUEST)
    template_path = Path(args.write_template or DEFAULT_TEMPLATE)
    if args.write_template:
        write_template(template_path, slots)
    summary = build_summary(template_path, slots)
    if args.write_summary:
        path = Path(args.write_summary)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    if args.write_doc:
        write_doc(summary, Path(args.write_doc))
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
