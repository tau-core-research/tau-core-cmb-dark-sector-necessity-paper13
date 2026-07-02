#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = ROOT / "payload_templates/tau_cmb_parent_source_freeze_packet_submission_TEMPLATE_v01.csv"
DEFAULT_CANDIDATE = ROOT / "payloads/tau_cmb_parent_source_freeze_packet_submission_candidate_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_parent_source_freeze_packet_submission_candidate_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_parent_source_freeze_packet_submission_candidate_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_parent_source_freeze_packet_submission_candidate_v01_negative_candidate_only_"
    "no_populated_source_values_no_source_acceptance_no_phi_derivation_no_score_no_verdict"
)

UNSUPPLIED = "UNSUPPLIED_ENDPOINT_BLIND_VALUE"


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_template(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def stable_row_hash(row: dict[str, str]) -> str:
    hash_row = {key: value for key, value in row.items() if key != "artifact_hash"}
    payload = json.dumps(hash_row, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def candidate_rows(template_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in template_rows:
        candidate = dict(row)
        if not candidate.get("payload_value"):
            candidate["payload_value"] = UNSUPPLIED
        if not candidate.get("source_provenance"):
            candidate["source_provenance"] = "NO_SOURCE_PROVENANCE_SUPPLIED"
        if not candidate.get("replay_rule_or_command"):
            candidate["replay_rule_or_command"] = (
                "python3 scripts/build_tau_cmb_parent_source_freeze_packet_submission_candidate.py "
                "--write-candidate --write-summary --write-doc"
            )
        candidate["review_status"] = "NEGATIVE_CANDIDATE_UNPOPULATED"
        candidate["acceptance_status"] = "REJECTED_NO_POPULATED_SOURCE_VALUE"
        candidate["notes"] = (
            f"{candidate.get('notes', '')} Negative candidate: value intentionally unsupplied; "
            "does not satisfy source-freeze packet."
        ).strip()
        candidate["artifact_hash"] = stable_row_hash(candidate)
        rows.append(candidate)
    return rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_summary(candidate_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    supplied_rows = [row for row in rows if row["payload_value"] != UNSUPPLIED]
    accepted_rows = [row for row in rows if row["acceptance_status"].startswith("ACCEPTED")]
    return {
        "report_id": "tau_cmb_parent_source_freeze_packet_submission_candidate_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate": rel(candidate_path),
        "candidate_rows": len(rows),
        "populated_source_value_rows": len(supplied_rows),
        "accepted_rows": len(accepted_rows),
        "artifact_hash_rows": sum(bool(row.get("artifact_hash")) for row in rows),
        "payload_submitted": True,
        "source_acceptance_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "PARENT_SOURCE_FREEZE_PACKET_NEGATIVE_CANDIDATE_REJECTED_NO_POPULATED_VALUES",
        "next_minimal_unblock": "provide_real_endpoint_blind_parent_source_values_or_record_explicit_source_unavailability",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Parent-Source Freeze Packet Submission Candidate v01

**Doc class:** endpoint-blind freeze-packet submission candidate
**Status:** negative candidate; no populated source values; rejected for source acceptance

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact materializes a replayable submission candidate from the freeze
packet template. It intentionally supplies no Tau-side source values. Each row
is marked as `UNSUPPLIED_ENDPOINT_BLIND_VALUE` and receives a stable row hash.

Candidate:

```text
{summary["candidate"]}
```

This preserves the negative result in a reproducible form: the current repository
does not yet contain the endpoint-blind base-field, seed, response-operator,
gauge/normalization, firewall, and replay payload needed to accept a CMB
parent-source freeze packet.

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
    parser = argparse.ArgumentParser(description="Build Tau CMB parent-source freeze packet submission candidate.")
    parser.add_argument("--template", default=str(DEFAULT_TEMPLATE))
    parser.add_argument("--write-candidate", nargs="?", const=str(DEFAULT_CANDIDATE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()

    fieldnames, template_rows = read_template(Path(args.template))
    rows = candidate_rows(template_rows)
    candidate_path = Path(args.write_candidate or DEFAULT_CANDIDATE)
    if args.write_candidate:
        write_csv(candidate_path, fieldnames, rows)
    summary = build_summary(candidate_path, rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
