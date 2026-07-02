#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_seed_tau_payload_materialization_packet_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_seed_tau_payload_materialization_packet_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_seed_tau_payload_materialization_packet_v01.md"
DEFAULT_TEMPLATE = ROOT / "payload_templates/seed_tau_payload_TEMPLATE_v01.csv"

CLAIM_BOUNDARY = (
    "tau_cmb_seed_tau_payload_materialization_packet_v01_template_only_"
    "no_payload_values_no_payload_acceptance_no_domain_certificate_no_readout_no_score_no_verdict"
)

PAYLOAD_FIELDS = [
    "seed_id",
    "seed_component",
    "tau_side_descriptor",
    "support_coordinate",
    "scale_label",
    "normalization_convention",
    "dimension_role",
    "construction_source",
    "endpoint_exclusion_attestation",
    "null_limit_role",
    "notes",
]

PACKET_FIELDS = [
    "packet_row_id",
    "required_object",
    "artifact_path",
    "required_content",
    "template_status",
    "acceptance_status",
    "blocking_reason",
    "next_required_action",
    "allows_payload_acceptance",
    "allows_domain_certificate",
    "allows_readout_evaluation",
    "allows_score_entry",
    "claim_boundary",
]

ROWS = [
    {
        "required_object": "seed_tau_payload.csv",
        "artifact_path": "payload_templates/seed_tau_payload_TEMPLATE_v01.csv",
        "required_content": "endpoint-blind seed rows with support coordinates, scale labels, normalization convention, dimension role, and construction source",
        "template_status": "TEMPLATE_DECLARED_UNPOPULATED",
        "acceptance_status": "PAYLOAD_NOT_ACCEPTED",
        "blocking_reason": "template contains no populated seed values",
        "next_required_action": "populate seed_tau_payload.csv from Tau-side sources only",
    },
    {
        "required_object": "seed_tau_payload.csv.provenance.json",
        "artifact_path": "payload_templates/seed_tau_payload_TEMPLATE_v01.provenance.json",
        "required_content": "source paths, freeze time, source hashes, and construction rationale",
        "template_status": "REQUIRED_NOT_MATERIALIZED",
        "acceptance_status": "PROVENANCE_NOT_ACCEPTED",
        "blocking_reason": "no provenance file is materialized for a populated payload",
        "next_required_action": "materialize provenance for populated payload",
    },
    {
        "required_object": "seed_tau_payload.csv.replay.txt",
        "artifact_path": "payload_templates/seed_tau_payload_TEMPLATE_v01.replay.txt",
        "required_content": "deterministic command or manual replay protocol that rebuilds the seed payload without endpoint inputs",
        "template_status": "REQUIRED_NOT_MATERIALIZED",
        "acceptance_status": "REPLAY_NOT_ACCEPTED",
        "blocking_reason": "no replay file is materialized for a populated payload",
        "next_required_action": "materialize replay for populated payload",
    },
    {
        "required_object": "seed_tau_payload.csv.hashes.json",
        "artifact_path": "payload_templates/seed_tau_payload_TEMPLATE_v01.hashes.json",
        "required_content": "content hashes for payload, provenance, replay, and firewall evidence",
        "template_status": "REQUIRED_NOT_MATERIALIZED",
        "acceptance_status": "HASHES_NOT_ACCEPTED",
        "blocking_reason": "no hash manifest binds populated artifacts",
        "next_required_action": "materialize hash manifest after payload/provenance/replay exist",
    },
    {
        "required_object": "seed_tau_payload.csv.firewall.json",
        "artifact_path": "payload_templates/seed_tau_payload_TEMPLATE_v01.firewall.json",
        "required_content": "attestation that no CMB endpoint residual, peak-shape fit, likelihood error, score output, or post-endpoint tuning field was used",
        "template_status": "REQUIRED_NOT_MATERIALIZED",
        "acceptance_status": "FIREWALL_NOT_ACCEPTED",
        "blocking_reason": "no endpoint-blind firewall evidence is materialized",
        "next_required_action": "materialize firewall attestation for populated payload",
    },
    {
        "required_object": "tau_cmb_seed_zero_control_v01",
        "artifact_path": "docs/tau_cmb_seed_zero_control_v01.md",
        "required_content": "null_seed definition and proof obligation that null_seed is admitted by the same readout domain rule",
        "template_status": "REQUIRED_NOT_MATERIALIZED",
        "acceptance_status": "ZERO_CONTROL_NOT_ACCEPTED",
        "blocking_reason": "zero/null seed control is not defined",
        "next_required_action": "build zero-control scaffold after payload fields are fixed",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def template_rows() -> list[dict[str, str]]:
    return [
        {
            "seed_id": "UNPOPULATED",
            "seed_component": "morphological_seed",
            "tau_side_descriptor": "UNPOPULATED_TAU_SIDE_DESCRIPTOR",
            "support_coordinate": "UNPOPULATED_SUPPORT_COORDINATE",
            "scale_label": "UNPOPULATED_SCALE_LABEL",
            "normalization_convention": "UNPOPULATED_NORMALIZATION_CONVENTION",
            "dimension_role": "UNPOPULATED_DIMENSION_ROLE",
            "construction_source": "UNPOPULATED_TAU_SIDE_SOURCE_ONLY",
            "endpoint_exclusion_attestation": "MUST_NOT_USE_CMB_ENDPOINT_RESIDUALS_PEAK_SHAPES_SCORES_OR_POST_ENDPOINT_TUNING",
            "null_limit_role": "UNPOPULATED_NULL_LIMIT_ROLE",
            "notes": "template row only; not a payload",
        }
    ]


def packet_rows() -> list[dict[str, str]]:
    return [
        {
            "packet_row_id": f"TCMBSTPMP01_{index:03d}",
            "allows_payload_acceptance": "false",
            "allows_domain_certificate": "false",
            "allows_readout_evaluation": "false",
            "allows_score_entry": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            **row,
        }
        for index, row in enumerate(ROWS, start=1)
    ]


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_summary(table_path: Path, template_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "report_id": "tau_cmb_seed_tau_payload_materialization_packet_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "packet_table": rel(table_path),
        "payload_template": rel(template_path),
        "payload_template_sha256": sha256(template_path) if template_path.exists() else None,
        "packet_rows": len(rows),
        "payload_values_populated": False,
        "payload_acceptance_allowed": False,
        "domain_certificate_allowed": False,
        "readout_evaluation_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "SEED_TAU_PAYLOAD_MATERIALIZATION_PACKET_TEMPLATE_DECLARED_UNPOPULATED",
        "next_minimal_unblock": "populate_seed_tau_payload_from_tau_side_sources_only",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['packet_row_id']}` `{row['required_object']}`: "
        f"{row['template_status']} / {row['acceptance_status']} | blocks: {row['blocking_reason']}"
        for row in rows
    )
    text = f"""# Tau CMB Seed Tau Payload Materialization Packet v01

**Doc class:** endpoint-blind seed payload materialization packet
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact creates the narrow payload template needed by the seed readout
domain certificate. It does not populate seed values, accept a payload, certify
`seed_tau_CMB in Dom(R_CMB)`, evaluate a CMB readout, enter scoring, or decide
the Tau dark-sector question.

## Payload Template

```text
{summary["payload_template"]}
sha256={summary["payload_template_sha256"]}
```

The template is intentionally unpopulated. Any real payload must be built from
Tau-side morphology/readout sources only and must not read CMB endpoint
residuals, peak-shape fits, likelihood errors, score outputs, or post-endpoint
tuning fields.

## Packet Rows

{row_text}

## Status

```text
{summary["status"]}
```

This is the first place where the route becomes operationally concrete: the
next step is no longer to add another broad proof packet, but to populate the
declared payload and evidence files under the endpoint-blind firewall.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB seed_tau payload materialization packet.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    parser.add_argument("--write-template", nargs="?", const=str(DEFAULT_TEMPLATE))
    args = parser.parse_args()

    template_path = Path(args.write_template or DEFAULT_TEMPLATE)
    if args.write_template:
        write_csv(template_path, PAYLOAD_FIELDS, template_rows())

    table_path = Path(args.write_table or DEFAULT_TABLE)
    rows = packet_rows()
    if args.write_table:
        write_csv(table_path, PACKET_FIELDS, rows)

    summary = build_summary(table_path, template_path, rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), rows, summary)

    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
