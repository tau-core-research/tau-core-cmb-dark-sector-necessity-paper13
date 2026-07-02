#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQUEST_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_request_v01.csv"
REQUEST_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_request_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_supply_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_supply_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_supply_v01.md"

ROLE_COORDINATE_AUDITS = [
    "tau_cmb_readout_role_coordinate_acoustic_audit_v01.json",
    "tau_cmb_readout_role_coordinate_density_audit_v01.json",
    "tau_cmb_readout_role_coordinate_lensing_audit_v01.json",
    "tau_cmb_readout_role_coordinate_growth_audit_v01.json",
    "tau_cmb_readout_role_coordinate_radiation_audit_v01.json",
    "tau_cmb_readout_role_coordinate_null_audit_v01.json",
]

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_supply_v01_"
    "materialization_candidate_supplied_role_coordinates_blocked_not_physical_R_CMB_"
    "no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "physical_R_CMB_materialization_supply_row_id",
    "source_materialization_request_row_id",
    "certificate_area",
    "checker_name",
    "domain_object_name",
    "materialization_artifact",
    "materialization_hash_artifact",
    "materialization_artifact_supplied",
    "hash_supplied",
    "hash_matches",
    "domain_object_accepted",
    "structural_R_CMB_candidate_available",
    "role_coordinate_audits_present",
    "role_coordinates_accepted",
    "endpoint_blind_materialization",
    "physical_R_CMB_materialized",
    "numeric_values_materialized",
    "codomain_checker_passed",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "supply_status",
    "blocking_reason",
    "claim_boundary",
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def input_chain_clean() -> bool:
    if not REQUEST_SUMMARY.exists():
        return False
    summary = load_json(REQUEST_SUMMARY)
    return (
        summary.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_PHYSICAL_R_CMB_MATERIALIZATION_REQUEST_DECLARED"
        and summary.get("input_chain_clean") is True
        and summary.get("physical_R_CMB_materialization_request_rows") == 7
        and summary.get("domain_object_accepted_rows") == 7
        and summary.get("physical_R_CMB_materialized_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def role_audit_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for name in ROLE_COORDINATE_AUDITS:
        path = ROOT / "data/derived" / name
        payload = load_json(path) if path.exists() else {}
        records.append(
            {
                "path": rel(path),
                "exists": path.exists(),
                "status": payload.get("status"),
                "failed_rows": payload.get("failed_rows"),
                "blocked_rows": payload.get("blocked_rows"),
                "concrete_R_CMB_allowed": payload.get("concrete_R_CMB_allowed"),
            }
        )
    return records


def materialization_payload(row: dict[str, str]) -> dict[str, Any]:
    audits = role_audit_records()
    all_audits_present = all(record["exists"] for record in audits)
    role_coordinates_accepted = all(record["concrete_R_CMB_allowed"] is True for record in audits)
    return {
        "artifact_status": "PHYSICAL_R_CMB_MATERIALIZATION_CANDIDATE_SUPPLIED_NOT_PHYSICAL",
        "claim_boundary": CLAIM_BOUNDARY,
        "certificate_area": row["certificate_area"],
        "checker_name": row["checker_name"],
        "domain_object_name": row["domain_object_name"],
        "structural_R_CMB_candidate_available": row["structural_R_CMB_candidate_available"] == "true",
        "role_coordinate_audit_records": audits,
        "role_coordinate_audits_present": all_audits_present,
        "role_coordinates_accepted": role_coordinates_accepted,
        "role_vector_slots": ["e_acoustic", "e_density", "e_lensing", "e_growth", "e_radiation", "e_null"],
        "endpoint_blind_firewall": {
            "cmb_endpoint_residuals_used": False,
            "act_planck_likelihood_used": False,
            "score_output_used": False,
            "post_endpoint_tuning_used": False,
            "dark_sector_verdict_used": False,
        },
        "physical_R_CMB_materialized": False,
        "numeric_values_materialized": False,
        "codomain_checker_passed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "blocking_reason": "role-coordinate audits are present but remain blocked/not materialized",
        "next_required_step": "accept and materialize role-coordinate numeric values before physical R_CMB can pass",
    }


def rows(write_artifacts: bool) -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("physical R_CMB materialization request summary is not clean")
    out: list[dict[str, str]] = []
    for index, request in enumerate(read_csv(REQUEST_TABLE), start=1):
        artifact = ROOT / request["required_materialization_artifact"].replace("physical_R_CMB_materialization_requests", "physical_R_CMB_materialization_payloads")
        hash_artifact = artifact.with_suffix(".hashes.json")
        if write_artifacts:
            write_json(artifact, materialization_payload(request))
            write_json(
                hash_artifact,
                {
                    "target": rel(artifact),
                    "sha256": sha256(artifact),
                    "claim_boundary": CLAIM_BOUNDARY,
                    "physical_R_CMB_materialized": False,
                    "numeric_values_materialized": False,
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
                "physical_R_CMB_materialization_supply_row_id": f"TCMBCDSEMPHRCMBSUP01_{index:03d}",
                "source_materialization_request_row_id": request["physical_R_CMB_materialization_request_row_id"],
                "certificate_area": request["certificate_area"],
                "checker_name": request["checker_name"],
                "domain_object_name": request["domain_object_name"],
                "materialization_artifact": rel(artifact),
                "materialization_hash_artifact": rel(hash_artifact),
                "materialization_artifact_supplied": str(supplied).lower(),
                "hash_supplied": str(hash_supplied).lower(),
                "hash_matches": str(hash_matches).lower(),
                "domain_object_accepted": request["domain_object_accepted"],
                "structural_R_CMB_candidate_available": request["structural_R_CMB_candidate_available"],
                "role_coordinate_audits_present": str(payload.get("role_coordinate_audits_present") is True).lower(),
                "role_coordinates_accepted": str(payload.get("role_coordinates_accepted") is True).lower(),
                "endpoint_blind_materialization": "true",
                "physical_R_CMB_materialized": str(payload.get("physical_R_CMB_materialized") is True).lower(),
                "numeric_values_materialized": str(payload.get("numeric_values_materialized") is True).lower(),
                "codomain_checker_passed": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "supply_status": (
                    "PHYSICAL_R_CMB_MATERIALIZATION_CANDIDATE_SUPPLIED_ROLE_COORDINATES_BLOCKED"
                    if supplied and hash_matches
                    else "PHYSICAL_R_CMB_MATERIALIZATION_SUPPLY_BLOCKED"
                ),
                "blocking_reason": "materialization candidate supplied, but role coordinates are not accepted/materialized as numeric readout values",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def write_table(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_summary(table_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "report_id": "tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_supply_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_physical_R_CMB_materialization_request_table": rel(REQUEST_TABLE),
        "input_physical_R_CMB_materialization_request_summary": rel(REQUEST_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "physical_R_CMB_materialization_supply_rows": len(rows),
        "materialization_artifact_supplied_rows": sum(row["materialization_artifact_supplied"] == "true" for row in rows),
        "hash_matched_rows": sum(row["hash_matches"] == "true" for row in rows),
        "domain_object_accepted_rows": sum(row["domain_object_accepted"] == "true" for row in rows),
        "role_coordinate_audits_present_rows": sum(row["role_coordinate_audits_present"] == "true" for row in rows),
        "role_coordinates_accepted_rows": sum(row["role_coordinates_accepted"] == "true" for row in rows),
        "physical_R_CMB_materialized_rows": sum(row["physical_R_CMB_materialized"] == "true" for row in rows),
        "numeric_values_materialized_rows": sum(row["numeric_values_materialized"] == "true" for row in rows),
        "codomain_checker_passed_rows": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_PHYSICAL_R_CMB_MATERIALIZATION_CANDIDATES_SUPPLIED_ROLE_COORDINATES_BLOCKED"
            if input_chain_clean() and len(rows) == 7 and all(row["hash_matches"] == "true" for row in rows)
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_PHYSICAL_R_CMB_MATERIALIZATION_SUPPLY_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Physical R_CMB Materialization Supply v01

**Doc class:** physical R_CMB materialization supply candidate
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This step supplies hash-bound materialization candidates for accepted semantic
domain objects. The candidates bind role-coordinate audits and preserve endpoint
blindness, but do not materialize physical/numeric R_CMB values because role
coordinates remain blocked/not accepted.

## Summary

```text
physical_R_CMB_materialization_supply_rows={summary["physical_R_CMB_materialization_supply_rows"]}
materialization_artifact_supplied_rows={summary["materialization_artifact_supplied_rows"]}
hash_matched_rows={summary["hash_matched_rows"]}
domain_object_accepted_rows={summary["domain_object_accepted_rows"]}
role_coordinate_audits_present_rows={summary["role_coordinate_audits_present_rows"]}
role_coordinates_accepted_rows={summary["role_coordinates_accepted_rows"]}
physical_R_CMB_materialized_rows={summary["physical_R_CMB_materialized_rows"]}
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
    parser = argparse.ArgumentParser(description="Supply Tau CMB physical R_CMB materialization candidates.")
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
