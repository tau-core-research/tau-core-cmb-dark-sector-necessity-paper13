#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUDIT = ROOT / "data/derived/tau_cmb_parent_source_freeze_packet_submission_candidate_audit_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_parent_source_unavailability_record_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_parent_source_unavailability_record_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_parent_source_unavailability_record_v01_record_only_"
    "no_physical_failure_claim_no_source_acceptance_no_phi_derivation_no_score_no_verdict"
)


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def build_report(audit_path: Path) -> dict[str, Any]:
    audit = read_json(audit_path)
    decision = audit.get("decision", "AUDIT_MISSING")
    unsupplied = audit.get("unsupplied_payload_rows", [])
    endpoint_hits = audit.get("endpoint_token_hits", [])
    hash_mismatches = audit.get("hash_mismatch_rows", [])
    missing_columns = audit.get("missing_required_columns", [])
    missing_rows = audit.get("missing_rows", [])

    audit_clean_except_unpopulated = (
        decision == "DO_NOT_ACCEPT_NO_POPULATED_SOURCE_VALUES"
        and len(unsupplied) == 7
        and not endpoint_hits
        and not hash_mismatches
        and not missing_columns
        and not missing_rows
    )
    status = (
        "PARENT_SOURCE_UNAVAILABILITY_RECORDED_CLEAN_NEGATIVE_AUDIT"
        if audit_clean_except_unpopulated
        else "PARENT_SOURCE_UNAVAILABILITY_RECORD_BLOCKED_AUDIT_NOT_CLEAN"
    )
    return {
        "report_id": "tau_cmb_parent_source_unavailability_record_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "source_audit": rel(audit_path),
        "audit_decision": decision,
        "status": status,
        "unavailable_components": [
            "B_tau_base_CMB_descriptor",
            "seed_tau_CMB_descriptor",
            "R_tau_CMB_input_set",
            "gauge_norm_tau_CMB_metadata",
            "source_freeze_firewall_certificate",
            "freeze_packet_replay_rule",
        ],
        "clean_negative_audit": audit_clean_except_unpopulated,
        "source_acceptance_allowed": False,
        "phi_tau_derivation_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "physical_failure_claim_allowed": False,
        "interpretation": (
            "The repository currently lacks the endpoint-blind CMB parent-source "
            "payload needed to accept the freeze packet. This is a source-availability "
            "blocker, not evidence that Tau Core fails CMB physics."
        ),
        "next_minimal_unblock": "supply_endpoint_blind_values_for_one_freeze_packet_component_or_keep_unavailability_record_as_stop_state",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    components = "\n".join(f"- `{item}`" for item in report["unavailable_components"])
    text = f"""# Tau CMB Parent-Source Unavailability Record v01

**Doc class:** CMB parent-source unavailability record
**Status:** {report["status"]}
**Source audit:** `{report["source_audit"]}`

## Claim Boundary

```text
{report["claim_boundary"]}
```

## Purpose

This artifact records the current stop-state after the freeze-packet submission
candidate audit. The audit found a clean negative candidate: required rows and
hashes are present and no endpoint-token hit is detected, but no populated
Tau-side source values are supplied.

This is not a physical failure claim. It only says that the repository does not
currently contain an acceptable endpoint-blind CMB parent-source payload.

## Unavailable Components

{components}

## Interpretation

```text
{report["interpretation"]}
```

## Status

```text
{report["status"]}
```

No source may be accepted from this record. No `Phi_tau_eff` derivation, CMB
score, no-dark claim, Tau-response success claim, or dark-sector verdict is
allowed.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB parent-source unavailability record.")
    parser.add_argument("--audit", default=str(DEFAULT_AUDIT))
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    report = build_report(Path(args.audit))
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), report)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
