#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "payloads/seed_tau_payload_candidate_v01.csv"
SUPPORT_RULE = ROOT / "data/derived/tau_cmb_seed_support_domain_rule_candidate_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_seed_normalization_replay_candidate_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_seed_normalization_replay_candidate_summary_v01.json"
DEFAULT_REPLAY = ROOT / "payloads/seed_tau_normalization_replay_candidate_v01.txt"
DEFAULT_DOC = ROOT / "docs/tau_cmb_seed_normalization_replay_candidate_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_seed_normalization_replay_candidate_v01_replay_candidate_only_"
    "normalization_not_accepted_no_support_certification_no_domain_certificate_no_readout_no_score_no_verdict"
)

FIELDS = [
    "normalization_row_id",
    "component",
    "input_object",
    "candidate_rule",
    "output_object",
    "endpoint_blind_source",
    "status",
    "blocking_reason",
    "next_required_artifact",
    "allows_normalization_acceptance",
    "allows_support_certification",
    "allows_domain_certificate",
    "allows_score_entry",
    "claim_boundary",
]


def read_payload() -> dict[str, str]:
    with PAYLOAD.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 1:
        raise ValueError("seed_tau payload candidate must contain exactly one row")
    return rows[0]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def rows(payload: dict[str, str]) -> list[dict[str, str]]:
    raw_tuple = (
        payload["tau_side_descriptor"],
        payload["support_coordinate"],
        payload["scale_label"],
    )
    normalized_label = "CMB_readout_sector_scale_label_canonical_v01"
    return [
        {
            "component": "normalization_input_tuple",
            "input_object": "xi_seed = (morphology_class, readout_sector, scale_label)",
            "candidate_rule": f"read tuple from payload fields: {raw_tuple}",
            "output_object": "xi_seed_raw",
            "endpoint_blind_source": rel(PAYLOAD),
            "status": "INPUT_TUPLE_DECLARED_NOT_ACCEPTED",
            "blocking_reason": "input tuple is candidate-level evidence only",
            "next_required_artifact": "tau_cmb_seed_normalization_replay_candidate_audit_v01",
        },
        {
            "component": "scale_label_canonicalization",
            "input_object": payload["scale_label"],
            "candidate_rule": "replace candidate_not_normalized suffix with canonical_v01 under fixed support-domain convention",
            "output_object": normalized_label,
            "endpoint_blind_source": rel(SUPPORT_RULE),
            "status": "CANONICAL_LABEL_DECLARED_NOT_ACCEPTED",
            "blocking_reason": "canonical label is declared but not independently audited",
            "next_required_artifact": "tau_cmb_seed_normalization_replay_candidate_audit_v01",
        },
        {
            "component": "normalized_seed_descriptor",
            "input_object": "seed_tau_payload_candidate_v01",
            "candidate_rule": "N_seed keeps morphology_class and readout_sector fixed and only canonicalizes scale_label",
            "output_object": "normalized_seed_tau_CMB_candidate_v01",
            "endpoint_blind_source": "payload plus support-domain rule candidate",
            "status": "NORMALIZED_DESCRIPTOR_DECLARED_NOT_ACCEPTED",
            "blocking_reason": "normalization replay has not been audited against payload hashes and firewall",
            "next_required_artifact": "tau_cmb_seed_normalization_replay_candidate_audit_v01",
        },
        {
            "component": "forbidden_operations",
            "input_object": "O_CMB_endpoint",
            "candidate_rule": "normalization cannot use endpoint residuals, peak-shape fits, likelihood deltas, score outputs, or post-endpoint tuning",
            "output_object": "forbidden_endpoint_inputs_not_used",
            "endpoint_blind_source": "seed payload firewall candidate",
            "status": "FIREWALL_DEPENDENCY_DECLARED_NOT_ACCEPTED",
            "blocking_reason": "firewall attestation remains candidate-level and unaccepted",
            "next_required_artifact": "tau_cmb_seed_normalization_replay_candidate_audit_v01",
        },
        {
            "component": "zero_control_dependency",
            "input_object": "null_seed",
            "candidate_rule": "zero-control must use the same canonical scale convention",
            "output_object": "zero_control_pending_same_scale_convention",
            "endpoint_blind_source": "support-domain rule candidate",
            "status": "DEPENDENCY_DECLARED_NOT_EXECUTED",
            "blocking_reason": "zero-control candidate does not exist yet",
            "next_required_artifact": "tau_cmb_seed_zero_control_v01",
        },
    ]


def table_rows(raw_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "normalization_row_id": f"TCMBSNRC01_{index:03d}",
            "allows_normalization_acceptance": "false",
            "allows_support_certification": "false",
            "allows_domain_certificate": "false",
            "allows_score_entry": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            **row,
        }
        for index, row in enumerate(raw_rows, start=1)
    ]


def write_table(path: Path, rows_: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows_)


def write_replay(path: Path, payload: dict[str, str]) -> None:
    text = f"""# seed_tau normalization replay candidate v01

Input tuple:

xi_seed = (
  morphology_class = {payload["tau_side_descriptor"]},
  readout_sector = {payload["support_coordinate"]},
  scale_label = {payload["scale_label"]}
)

Candidate transformation:

N_seed(xi_seed) keeps morphology_class and readout_sector fixed and maps
scale_label=CMB_readout_sector_scale_label_candidate_not_normalized
to scale_label=CMB_readout_sector_scale_label_canonical_v01.

Endpoint boundary:

No CMB residuals, peak-shape fits, likelihood deltas, score outputs, or
post-endpoint tuning fields are read by this replay candidate.

Acceptance boundary:

This replay is a candidate only. It does not accept normalization, certify
support, certify domain membership, evaluate readout, or enter scoring.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_summary(table_path: Path, replay_path: Path, rows_: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "report_id": "tau_cmb_seed_normalization_replay_candidate_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "replay": rel(replay_path),
        "normalization_rows": len(rows_),
        "normalization_replay_declared": True,
        "normalization_acceptance_allowed": False,
        "support_certification_allowed": False,
        "domain_certificate_allowed": False,
        "readout_evaluation_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "SEED_NORMALIZATION_REPLAY_CANDIDATE_DECLARED_NOT_ACCEPTED",
        "next_minimal_unblock": "tau_cmb_seed_normalization_replay_candidate_audit_v01",
    }


def write_doc(path: Path, rows_: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['normalization_row_id']}` `{row['component']}`: {row['status']} | `{row['output_object']}`"
        for row in rows_
    )
    text = f"""# Tau CMB Seed Normalization Replay Candidate v01

**Doc class:** seed normalization replay candidate
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact declares a deterministic Tau-side normalization replay candidate
for the CMB `seed_tau` support tuple. It does not accept normalization, certify
support, accept the payload, certify the readout domain, evaluate readout
survival, assign `A_tau(a,k)`, enter scoring, or decide the dark-sector
question.

## Replay

```text
{summary["replay"]}
```

## Rows

{row_text}

## Status

```text
{summary["status"]}
```

The candidate removes ambiguity from the scale-label route, but it remains
unaccepted until an audit checks endpoint blindness, payload/hash consistency,
and compatibility with the support-domain rule.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB seed normalization replay candidate.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-replay", nargs="?", const=str(DEFAULT_REPLAY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    payload = read_payload()
    raw = rows(payload)
    normalized_rows = table_rows(raw)
    table_path = Path(args.write_table or DEFAULT_TABLE)
    replay_path = Path(args.write_replay or DEFAULT_REPLAY)
    if args.write_table:
        write_table(table_path, normalized_rows)
    if args.write_replay:
        write_replay(replay_path, payload)
    summary = build_summary(table_path, replay_path, normalized_rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), normalized_rows, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
