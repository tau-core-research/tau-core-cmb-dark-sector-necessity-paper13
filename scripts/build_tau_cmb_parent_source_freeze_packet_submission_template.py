#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = ROOT / "payload_templates/tau_cmb_parent_source_freeze_packet_submission_TEMPLATE_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_parent_source_freeze_packet_submission_template_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_parent_source_freeze_packet_submission_template_v01.md"
SUBMISSION_CANDIDATE = "payloads/tau_cmb_parent_source_freeze_packet_submission_candidate_v01.csv"

CLAIM_BOUNDARY = (
    "tau_cmb_parent_source_freeze_packet_submission_template_v01_template_only_"
    "no_payload_submitted_no_source_acceptance_no_phi_derivation_no_score_no_verdict"
)

FIELDS = [
    "freeze_row_id",
    "freeze_component",
    "required_payload_field",
    "payload_value",
    "unit_or_dimension_status",
    "source_provenance",
    "replay_rule_or_command",
    "artifact_hash",
    "endpoint_exclusion_statement",
    "review_status",
    "acceptance_status",
    "notes",
]

ROWS = [
    {
        "freeze_row_id": "TCMBPSF01_001",
        "freeze_component": "freeze_packet_identity",
        "required_payload_field": "packet_id",
        "payload_value": "",
        "unit_or_dimension_status": "not_physical",
        "source_provenance": "",
        "replay_rule_or_command": "",
        "artifact_hash": "",
        "endpoint_exclusion_statement": "must be fixed before CMB endpoint residuals or scores are read",
        "review_status": "TEMPLATE_UNPOPULATED",
        "acceptance_status": "NOT_ACCEPTED",
        "notes": "Use a stable packet id and date/version.",
    },
    {
        "freeze_row_id": "TCMBPSF01_002",
        "freeze_component": "base_field_state",
        "required_payload_field": "B_tau_base_CMB_descriptor",
        "payload_value": "",
        "unit_or_dimension_status": "",
        "source_provenance": "",
        "replay_rule_or_command": "",
        "artifact_hash": "",
        "endpoint_exclusion_statement": "must not be selected from density-role, acoustic, or lensing residuals",
        "review_status": "TEMPLATE_UNPOPULATED",
        "acceptance_status": "NOT_ACCEPTED",
        "notes": "Describe the Tau base-field state or explicitly mark unavailable.",
    },
    {
        "freeze_row_id": "TCMBPSF01_003",
        "freeze_component": "morphological_seed",
        "required_payload_field": "seed_tau_CMB_descriptor",
        "payload_value": "",
        "unit_or_dimension_status": "",
        "source_provenance": "",
        "replay_rule_or_command": "",
        "artifact_hash": "",
        "endpoint_exclusion_statement": "must not be inferred from CMB peak residual shape or lensing residual direction",
        "review_status": "TEMPLATE_UNPOPULATED",
        "acceptance_status": "NOT_ACCEPTED",
        "notes": "Describe parent morphology/seed/boundary/capacity/readout context.",
    },
    {
        "freeze_row_id": "TCMBPSF01_004",
        "freeze_component": "response_operator_input",
        "required_payload_field": "R_tau_CMB_input_set",
        "payload_value": "",
        "unit_or_dimension_status": "",
        "source_provenance": "",
        "replay_rule_or_command": "",
        "artifact_hash": "",
        "endpoint_exclusion_statement": "must not be tuned from CMB likelihood, role-score deltas, or endpoint target shape",
        "review_status": "TEMPLATE_UNPOPULATED",
        "acceptance_status": "NOT_ACCEPTED",
        "notes": "Name the operator inputs, not a post-fit operator output.",
    },
    {
        "freeze_row_id": "TCMBPSF01_005",
        "freeze_component": "gauge_normalization_metadata",
        "required_payload_field": "gauge_norm_tau_CMB_metadata",
        "payload_value": "",
        "unit_or_dimension_status": "",
        "source_provenance": "",
        "replay_rule_or_command": "",
        "artifact_hash": "",
        "endpoint_exclusion_statement": "must not be changed after endpoint comparison",
        "review_status": "TEMPLATE_UNPOPULATED",
        "acceptance_status": "NOT_ACCEPTED",
        "notes": "Lock units, sign, gauge, scale, and normalization conventions.",
    },
    {
        "freeze_row_id": "TCMBPSF01_006",
        "freeze_component": "endpoint_firewall_certificate",
        "required_payload_field": "source_freeze_firewall_certificate",
        "payload_value": "",
        "unit_or_dimension_status": "not_physical",
        "source_provenance": "",
        "replay_rule_or_command": "",
        "artifact_hash": "",
        "endpoint_exclusion_statement": "must certify no score outputs, residual tables, target-shape labels, or fit-selected choices",
        "review_status": "TEMPLATE_UNPOPULATED",
        "acceptance_status": "NOT_ACCEPTED",
        "notes": "Certificate must be generated before scoring.",
    },
    {
        "freeze_row_id": "TCMBPSF01_007",
        "freeze_component": "provenance_replay_rule",
        "required_payload_field": "freeze_packet_replay_rule",
        "payload_value": "",
        "unit_or_dimension_status": "not_physical",
        "source_provenance": "",
        "replay_rule_or_command": "",
        "artifact_hash": "",
        "endpoint_exclusion_statement": "must not read score directories, residual tables, or post-score patch files",
        "review_status": "TEMPLATE_UNPOPULATED",
        "acceptance_status": "NOT_ACCEPTED",
        "notes": "Replay rule must regenerate the same payload and hashes.",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_summary(template_path: Path) -> dict[str, Any]:
    return {
        "report_id": "tau_cmb_parent_source_freeze_packet_submission_template_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "template": rel(template_path),
        "template_rows": len(ROWS),
        "populated_rows": 0,
        "accepted_rows": 0,
        "payload_submitted": False,
        "source_acceptance_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "PARENT_SOURCE_FREEZE_PACKET_SUBMISSION_TEMPLATE_DECLARED_UNPOPULATED",
        "next_minimal_unblock": "submit_populated_endpoint_blind_parent_source_freeze_packet_candidate",
        "negative_candidate": SUBMISSION_CANDIDATE,
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Parent-Source Freeze Packet Submission Template v01

**Doc class:** endpoint-blind freeze-packet submission template
**Status:** template declared; no payload submitted, no source accepted, no score

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact provides the concrete CSV shape for submitting a populated CMB
parent-source freeze packet. It is a template only. It does not submit values,
accept a source, derive `Phi_tau_eff`, or open scoring.

Template:

```text
{summary["template"]}
```

The required populated fields are:

```text
packet_id
B_tau_base_CMB_descriptor
seed_tau_CMB_descriptor
R_tau_CMB_input_set
gauge_norm_tau_CMB_metadata
source_freeze_firewall_certificate
freeze_packet_replay_rule
```

Each populated row must include provenance, replay information, an artifact
hash, dimensional/unit status where applicable, and an endpoint-exclusion
statement.

A reproducible negative candidate may be materialized at:

```text
{summary["negative_candidate"]}
```

## Status

```text
{summary["status"]}
```

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB parent-source freeze packet submission template.")
    parser.add_argument("--write-template", nargs="?", const=str(DEFAULT_TEMPLATE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()

    template_path = Path(args.write_template or DEFAULT_TEMPLATE)
    if args.write_template:
        write_csv(template_path, ROWS)
    summary = build_summary(template_path)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
