#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
NUMERIC_MATERIALIZATION_AUDIT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_materialization_acceptance_audit_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_source_supply_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_source_supply_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_numeric_value_source_supply_v01.md"

ROLES = [
    ("acoustic", "e_acoustic"),
    ("density", "e_density"),
    ("lensing", "e_lensing"),
    ("growth", "e_growth"),
    ("radiation", "e_radiation"),
    ("null", "e_null"),
]

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_numeric_value_source_supply_v01_"
    "source_requirement_worklist_supplied_no_numeric_values_no_concrete_R_CMB_"
    "no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "numeric_value_source_supply_row_id",
    "role_name",
    "coordinate_symbol",
    "role_table",
    "role_audit",
    "numeric_value_source_artifact",
    "numeric_value_source_hash_artifact",
    "source_requirement_artifact_supplied",
    "hash_supplied",
    "hash_matches",
    "source_requirement_rows",
    "numeric_value_source_supplied",
    "numeric_values_materialized",
    "role_coordinate_acceptance_allowed",
    "concrete_R_CMB_allowed",
    "endpoint_blind_source_package",
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def input_chain_clean() -> bool:
    if not NUMERIC_MATERIALIZATION_AUDIT_SUMMARY.exists():
        return False
    summary = load_json(NUMERIC_MATERIALIZATION_AUDIT_SUMMARY)
    return (
        summary.get("status")
        == "CMB_READOUT_ROLE_COORDINATE_NUMERIC_MATERIALIZATION_ACCEPTANCE_AUDITED_REJECTED_COORDINATE_ACCEPTANCE_REQUIRED"
        and summary.get("next_minimal_unblock") == "tau_cmb_readout_role_coordinate_numeric_value_source_supply_v01"
        and summary.get("numeric_materialization_accepted_rows") == 0
        and summary.get("role_coordinate_accepted_rows") == 0
        and summary.get("numeric_values_materialized_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def role_paths(role_name: str) -> tuple[Path, Path]:
    return (
        ROOT / f"data/derived/tau_cmb_readout_role_coordinate_{role_name}_v01.csv",
        ROOT / f"data/derived/tau_cmb_readout_role_coordinate_{role_name}_audit_v01.json",
    )


def source_requirements(role_name: str) -> list[dict[str, Any]]:
    table_path, _ = role_paths(role_name)
    requirements: list[dict[str, Any]] = []
    for row in read_csv(table_path):
        requirements.append(
            {
                "coordinate_row_id": row.get("coordinate_row_id"),
                "coordinate_component": row.get("coordinate_component"),
                "formal_slot": row.get("formal_slot"),
                "candidate_definition": row.get("candidate_definition"),
                "source_dependency": row.get("source_dependency"),
                "blocked_by": row.get("blocked_by"),
                "coordinate_status": row.get("coordinate_status"),
                "dimension_role": row.get("dimension_role"),
                "minimum_numeric_source_condition": (
                    "endpoint-blind numeric value source, unit/convention replay, and provenance "
                    "must be supplied before this coordinate component can become numeric"
                ),
            }
        )
    return requirements


def artifact_payload(role_name: str, coordinate_symbol: str) -> dict[str, Any]:
    table_path, audit_path = role_paths(role_name)
    audit = load_json(audit_path) if audit_path.exists() else {}
    requirements = source_requirements(role_name)
    return {
        "artifact_status": "ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_REQUIREMENT_WORKLIST_SUPPLIED_NOT_NUMERIC",
        "claim_boundary": CLAIM_BOUNDARY,
        "role_name": role_name,
        "coordinate_symbol": coordinate_symbol,
        "input_numeric_materialization_acceptance_audit_summary": rel(NUMERIC_MATERIALIZATION_AUDIT_SUMMARY),
        "role_table": rel(table_path),
        "role_audit": rel(audit_path),
        "role_audit_status": audit.get("status"),
        "source_requirements": requirements,
        "source_requirement_rows": len(requirements),
        "numeric_value_source_supplied": False,
        "numeric_values_materialized": False,
        "role_coordinate_acceptance_allowed": False,
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
        "blocking_reason": "numeric source requirements are enumerated, but no accepted numeric source values are supplied",
        "next_required_step": "populate endpoint-blind numeric value source files with units, conventions, provenance, and replay",
    }


def rows(write_artifacts: bool) -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("role-coordinate numeric materialization acceptance audit summary is not clean")
    out: list[dict[str, str]] = []
    for index, (role_name, coordinate_symbol) in enumerate(ROLES, start=1):
        table_path, audit_path = role_paths(role_name)
        artifact = ROOT / "role_coordinate_numeric_value_sources" / coordinate_symbol / f"{coordinate_symbol}_numeric_value_source_requirements_v01.json"
        hash_artifact = artifact.with_suffix(".hashes.json")
        if write_artifacts:
            write_json(artifact, artifact_payload(role_name, coordinate_symbol))
            write_json(
                hash_artifact,
                {
                    "target": rel(artifact),
                    "sha256": sha256(artifact),
                    "claim_boundary": CLAIM_BOUNDARY,
                    "numeric_value_source_supplied": False,
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
                "numeric_value_source_supply_row_id": f"TCMBRRCNVSSUP01_{index:03d}",
                "role_name": role_name,
                "coordinate_symbol": coordinate_symbol,
                "role_table": rel(table_path),
                "role_audit": rel(audit_path),
                "numeric_value_source_artifact": rel(artifact),
                "numeric_value_source_hash_artifact": rel(hash_artifact),
                "source_requirement_artifact_supplied": str(supplied).lower(),
                "hash_supplied": str(hash_supplied).lower(),
                "hash_matches": str(hash_matches).lower(),
                "source_requirement_rows": str(payload.get("source_requirement_rows", 0)),
                "numeric_value_source_supplied": str(payload.get("numeric_value_source_supplied") is True).lower(),
                "numeric_values_materialized": str(payload.get("numeric_values_materialized") is True).lower(),
                "role_coordinate_acceptance_allowed": str(payload.get("role_coordinate_acceptance_allowed") is True).lower(),
                "concrete_R_CMB_allowed": str(payload.get("concrete_R_CMB_allowed") is True).lower(),
                "endpoint_blind_source_package": "true",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "supply_status": (
                    "ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_REQUIREMENT_WORKLIST_SUPPLIED_NOT_NUMERIC"
                    if supplied and hash_matches
                    else "ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_SUPPLY_BLOCKED"
                ),
                "blocking_reason": "source requirements are supplied, but numeric value sources and values are absent",
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
    source_requirement_rows = sum(int(row["source_requirement_rows"]) for row in table_rows)
    return {
        "report_id": "tau_cmb_readout_role_coordinate_numeric_value_source_supply_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_numeric_materialization_acceptance_audit_summary": rel(NUMERIC_MATERIALIZATION_AUDIT_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "numeric_value_source_supply_rows": len(table_rows),
        "source_requirement_artifact_supplied_rows": sum(row["source_requirement_artifact_supplied"] == "true" for row in table_rows),
        "hash_matched_rows": sum(row["hash_matches"] == "true" for row in table_rows),
        "source_requirement_rows": source_requirement_rows,
        "numeric_value_source_supplied_rows": sum(row["numeric_value_source_supplied"] == "true" for row in table_rows),
        "numeric_values_materialized_rows": sum(row["numeric_values_materialized"] == "true" for row in table_rows),
        "role_coordinate_acceptance_allowed_rows": sum(row["role_coordinate_acceptance_allowed"] == "true" for row in table_rows),
        "concrete_R_CMB_allowed_rows": sum(row["concrete_R_CMB_allowed"] == "true" for row in table_rows),
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_REQUIREMENT_WORKLIST_SUPPLIED_NOT_NUMERIC"
            if input_chain_clean() and len(table_rows) == 6 and all(row["hash_matches"] == "true" for row in table_rows)
            else "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_SUPPLY_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_readout_role_coordinate_numeric_value_source_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Readout Role-Coordinate Numeric Value Source Supply v01

**Doc class:** role-coordinate numeric value-source requirement supply
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This step converts the six blocked role-coordinate tables into a finite
numeric-value-source worklist. It supplies endpoint-blind requirement artifacts,
not numeric values. Therefore it does not accept role coordinates, materialize
concrete `R_CMB`, open score entry, compute likelihood, or decide the
dark-sector question.

## Summary

```text
numeric_value_source_supply_rows={summary["numeric_value_source_supply_rows"]}
source_requirement_artifact_supplied_rows={summary["source_requirement_artifact_supplied_rows"]}
hash_matched_rows={summary["hash_matched_rows"]}
source_requirement_rows={summary["source_requirement_rows"]}
numeric_value_source_supplied_rows={summary["numeric_value_source_supplied_rows"]}
numeric_values_materialized_rows={summary["numeric_values_materialized_rows"]}
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
    parser = argparse.ArgumentParser(description="Supply Tau CMB role-coordinate numeric value-source requirements.")
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
