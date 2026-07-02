#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHYSICAL_ACCEPTANCE_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_acceptance_audit_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_materialization_supply_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_materialization_supply_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_numeric_materialization_supply_v01.md"

ROLES = [
    ("acoustic", "e_acoustic"),
    ("density", "e_density"),
    ("lensing", "e_lensing"),
    ("growth", "e_growth"),
    ("radiation", "e_radiation"),
    ("null", "e_null"),
]

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_numeric_materialization_supply_v01_"
    "candidate_payloads_supplied_role_coordinates_blocked_no_concrete_R_CMB_"
    "no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "numeric_materialization_supply_row_id",
    "role_name",
    "coordinate_symbol",
    "role_summary",
    "role_audit",
    "role_table",
    "numeric_materialization_artifact",
    "numeric_materialization_hash_artifact",
    "candidate_artifact_supplied",
    "hash_supplied",
    "hash_matches",
    "role_coordinate_summary_present",
    "role_coordinate_audit_present",
    "role_coordinate_table_present",
    "role_coordinate_accepted",
    "numeric_values_materialized",
    "concrete_R_CMB_allowed",
    "endpoint_blind_materialization",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "supply_status",
    "blocking_reason",
    "claim_boundary",
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def input_chain_clean() -> bool:
    if not PHYSICAL_ACCEPTANCE_SUMMARY.exists():
        return False
    summary = load_json(PHYSICAL_ACCEPTANCE_SUMMARY)
    return (
        summary.get("status")
        == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_PHYSICAL_R_CMB_MATERIALIZATION_ACCEPTANCE_AUDITED_REJECTED_ROLE_COORDINATE_NUMERIC_MATERIALIZATION_REQUIRED"
        and summary.get("next_minimal_unblock") == "tau_cmb_readout_role_coordinate_numeric_materialization_supply_v01"
        and summary.get("materialization_accepted_rows") == 0
        and summary.get("role_coordinates_accepted_rows") == 0
        and summary.get("physical_R_CMB_materialized_rows") == 0
        and summary.get("numeric_values_materialized_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def role_paths(role_name: str) -> tuple[Path, Path, Path]:
    return (
        ROOT / f"data/derived/tau_cmb_readout_role_coordinate_{role_name}_summary_v01.json",
        ROOT / f"data/derived/tau_cmb_readout_role_coordinate_{role_name}_audit_v01.json",
        ROOT / f"data/derived/tau_cmb_readout_role_coordinate_{role_name}_v01.csv",
    )


def artifact_payload(role_name: str, coordinate_symbol: str) -> dict[str, Any]:
    summary_path, audit_path, table_path = role_paths(role_name)
    summary = load_json(summary_path) if summary_path.exists() else {}
    audit = load_json(audit_path) if audit_path.exists() else {}
    role_accepted = (
        summary.get("coordinate_acceptance_allowed") is True
        and summary.get("concrete_R_CMB_allowed") is True
        and audit.get("coordinate_acceptance_allowed") is True
        and audit.get("concrete_R_CMB_allowed") is True
    )
    return {
        "artifact_status": "ROLE_COORDINATE_NUMERIC_MATERIALIZATION_CANDIDATE_SUPPLIED_NOT_NUMERIC",
        "claim_boundary": CLAIM_BOUNDARY,
        "role_name": role_name,
        "coordinate_symbol": coordinate_symbol,
        "input_physical_R_CMB_materialization_acceptance_summary": rel(PHYSICAL_ACCEPTANCE_SUMMARY),
        "role_summary": rel(summary_path),
        "role_audit": rel(audit_path),
        "role_table": rel(table_path),
        "role_summary_status": summary.get("status"),
        "role_audit_status": audit.get("status"),
        "role_coordinate_summary_present": summary_path.exists(),
        "role_coordinate_audit_present": audit_path.exists(),
        "role_coordinate_table_present": table_path.exists(),
        "role_coordinate_accepted": role_accepted,
        "coordinate_acceptance_allowed": role_accepted,
        "numeric_values_materialized": False,
        "concrete_R_CMB_allowed": False,
        "endpoint_blind_firewall": {
            "cmb_endpoint_residuals_used": False,
            "act_planck_likelihood_used": False,
            "score_output_used": False,
            "post_endpoint_tuning_used": False,
            "dark_sector_verdict_used": False,
        },
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "blocking_reason": "role coordinate remains candidate-only or blocked; no numeric readout value is materialized",
        "next_required_step": "supply accepted endpoint-blind role-coordinate definitions and numeric value sources",
    }


def rows(write_artifacts: bool) -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("physical R_CMB materialization acceptance audit summary is not clean")
    out: list[dict[str, str]] = []
    for index, (role_name, coordinate_symbol) in enumerate(ROLES, start=1):
        summary_path, audit_path, table_path = role_paths(role_name)
        artifact = ROOT / "role_coordinate_numeric_materialization_payloads" / coordinate_symbol / f"{coordinate_symbol}_numeric_materialization_v01.json"
        hash_artifact = artifact.with_suffix(".hashes.json")
        if write_artifacts:
            write_json(artifact, artifact_payload(role_name, coordinate_symbol))
            write_json(
                hash_artifact,
                {
                    "target": rel(artifact),
                    "sha256": sha256(artifact),
                    "claim_boundary": CLAIM_BOUNDARY,
                    "role_coordinate_accepted": False,
                    "numeric_values_materialized": False,
                    "concrete_R_CMB_allowed": False,
                    "score_entry_allowed": False,
                    "likelihood_allowed": False,
                    "dark_sector_verdict_allowed": False,
                },
            )
        supplied = artifact.exists()
        hash_supplied = hash_artifact.exists()
        hash_matches = supplied and hash_supplied and load_json(hash_artifact).get("sha256") == sha256(artifact)
        payload = load_json(artifact) if supplied else {}
        out.append(
            {
                "numeric_materialization_supply_row_id": f"TCMBRRCNMSUP01_{index:03d}",
                "role_name": role_name,
                "coordinate_symbol": coordinate_symbol,
                "role_summary": rel(summary_path),
                "role_audit": rel(audit_path),
                "role_table": rel(table_path),
                "numeric_materialization_artifact": rel(artifact),
                "numeric_materialization_hash_artifact": rel(hash_artifact),
                "candidate_artifact_supplied": str(supplied).lower(),
                "hash_supplied": str(hash_supplied).lower(),
                "hash_matches": str(hash_matches).lower(),
                "role_coordinate_summary_present": str(summary_path.exists()).lower(),
                "role_coordinate_audit_present": str(audit_path.exists()).lower(),
                "role_coordinate_table_present": str(table_path.exists()).lower(),
                "role_coordinate_accepted": str(payload.get("role_coordinate_accepted") is True).lower(),
                "numeric_values_materialized": str(payload.get("numeric_values_materialized") is True).lower(),
                "concrete_R_CMB_allowed": str(payload.get("concrete_R_CMB_allowed") is True).lower(),
                "endpoint_blind_materialization": "true",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "supply_status": (
                    "ROLE_COORDINATE_NUMERIC_MATERIALIZATION_CANDIDATE_SUPPLIED_BLOCKED_NOT_NUMERIC"
                    if supplied and hash_matches
                    else "ROLE_COORDINATE_NUMERIC_MATERIALIZATION_SUPPLY_BLOCKED"
                ),
                "blocking_reason": "candidate payload is supplied, but the role coordinate is not accepted and no numeric readout value is materialized",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def write_table(path: Path, table_rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(table_rows)


def build_summary(table_path: Path, table_rows: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "report_id": "tau_cmb_readout_role_coordinate_numeric_materialization_supply_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_physical_R_CMB_materialization_acceptance_summary": rel(PHYSICAL_ACCEPTANCE_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "role_coordinate_numeric_materialization_supply_rows": len(table_rows),
        "candidate_artifact_supplied_rows": sum(row["candidate_artifact_supplied"] == "true" for row in table_rows),
        "hash_matched_rows": sum(row["hash_matches"] == "true" for row in table_rows),
        "role_coordinate_summary_present_rows": sum(row["role_coordinate_summary_present"] == "true" for row in table_rows),
        "role_coordinate_audit_present_rows": sum(row["role_coordinate_audit_present"] == "true" for row in table_rows),
        "role_coordinate_table_present_rows": sum(row["role_coordinate_table_present"] == "true" for row in table_rows),
        "role_coordinate_accepted_rows": sum(row["role_coordinate_accepted"] == "true" for row in table_rows),
        "numeric_values_materialized_rows": sum(row["numeric_values_materialized"] == "true" for row in table_rows),
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_MATERIALIZATION_CANDIDATES_SUPPLIED_BLOCKED_NOT_NUMERIC"
            if input_chain_clean() and len(table_rows) == 6 and all(row["hash_matches"] == "true" for row in table_rows)
            else "CMB_READOUT_ROLE_COORDINATE_NUMERIC_MATERIALIZATION_SUPPLY_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_readout_role_coordinate_numeric_materialization_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Readout Role-Coordinate Numeric Materialization Supply v01

**Doc class:** role-coordinate numeric materialization supply candidate
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This supply step materializes endpoint-blind, hash-bound candidate payloads for
the six CMB readout role coordinates. It does not accept them as numeric
coordinates: the existing role-coordinate summaries and audits still block
coordinate acceptance and concrete `R_CMB`.

## Summary

```text
role_coordinate_numeric_materialization_supply_rows={summary["role_coordinate_numeric_materialization_supply_rows"]}
candidate_artifact_supplied_rows={summary["candidate_artifact_supplied_rows"]}
hash_matched_rows={summary["hash_matched_rows"]}
role_coordinate_accepted_rows={summary["role_coordinate_accepted_rows"]}
numeric_values_materialized_rows={summary["numeric_values_materialized_rows"]}
concrete_R_CMB_allowed={summary["concrete_R_CMB_allowed"]}
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
    parser = argparse.ArgumentParser(description="Supply Tau CMB role-coordinate numeric materialization candidates.")
    parser.add_argument("--write-artifacts", action="store_true")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    table_rows = rows(write_artifacts=args.write_artifacts)
    table_path = Path(args.write_table) if args.write_table else DEFAULT_TABLE
    summary = build_summary(table_path, table_rows)
    if args.write_table:
        write_table(table_path, table_rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
