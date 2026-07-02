#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CANDIDATE = ROOT / "data/derived/tau_cmb_morphological_seed_descriptor_candidate_v01.csv"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_morphological_seed_descriptor_candidate_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_morphological_seed_descriptor_candidate_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_morphological_seed_descriptor_candidate_audit_v01_audit_only_"
    "no_seed_acceptance_no_source_acceptance_no_A_tau_derivation_no_phi_derivation_no_score_no_verdict"
)

REQUIRED_COLUMNS = {
    "seed_row_id",
    "descriptor_component",
    "candidate_value",
    "candidate_role",
    "tau_core_anchor",
    "endpoint_blind_basis",
    "dimension_or_unit_status",
    "support_domain",
    "activation_path",
    "required_next_audit",
    "current_status",
    "artifact_hash",
    "allows_seed_acceptance",
    "allows_source_acceptance",
    "allows_A_tau_derivation",
    "allows_phi_tau_derivation",
    "allows_score_entry",
    "claim_boundary",
}

REQUIRED_COMPONENTS = {
    "seed_identity",
    "intrinsic_morphology_basis",
    "readout_context",
    "activation_claim_boundary",
    "forbidden_endpoint_inputs",
}

FORBIDDEN_ENDPOINT_TOKENS = [
    "ACT RESIDUAL",
    "PLANCK RESIDUAL",
    "CMB ROLE SCORE",
    "LIKELIHOOD DELTA",
    "PEAK RESIDUAL",
    "LENSING RESIDUAL",
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def stable_row_hash(row: dict[str, str]) -> str:
    payload = json.dumps({key: value for key, value in row.items() if key != "artifact_hash"}, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def endpoint_hits(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for row in rows:
        if row.get("descriptor_component") == "forbidden_endpoint_inputs":
            continue
        blob = " ".join(str(value).upper().replace("_", " ") for value in row.values())
        for token in FORBIDDEN_ENDPOINT_TOKENS:
            if token in blob:
                hits.append({"seed_row_id": row.get("seed_row_id", ""), "token": token})
    return hits


def build_report(candidate_path: Path) -> dict[str, Any]:
    columns, rows = read_csv(candidate_path)
    components = {row.get("descriptor_component", "") for row in rows}
    missing_columns = sorted(REQUIRED_COLUMNS - set(columns))
    missing_components = sorted(REQUIRED_COMPONENTS - components)
    extra_components = sorted(component for component in components - REQUIRED_COMPONENTS if component)
    missing_hash_rows: list[str] = []
    hash_mismatch_rows: list[str] = []
    self_acceptance_rows: list[str] = []
    incomplete_boundary_rows: list[str] = []

    if not candidate_path.exists():
        status = "MORPHOLOGICAL_SEED_DESCRIPTOR_AUDIT_BLOCKED_NO_CANDIDATE"
        decision = "DO_NOT_ROUTE_NO_CANDIDATE"
    else:
        for row in rows:
            row_id = row.get("seed_row_id", "")
            if not row.get("artifact_hash"):
                missing_hash_rows.append(row_id)
            elif row.get("artifact_hash") != stable_row_hash(row):
                hash_mismatch_rows.append(row_id)
            if any(row.get(flag) != "false" for flag in [
                "allows_seed_acceptance",
                "allows_source_acceptance",
                "allows_A_tau_derivation",
                "allows_phi_tau_derivation",
                "allows_score_entry",
            ]):
                self_acceptance_rows.append(row_id)
            if "no_seed_acceptance" not in row.get("claim_boundary", ""):
                incomplete_boundary_rows.append(row_id)
        hits = endpoint_hits(rows)
        if missing_columns or missing_components or extra_components:
            status = "MORPHOLOGICAL_SEED_DESCRIPTOR_AUDIT_REJECTED_SCHEMA_MISMATCH"
            decision = "DO_NOT_ROUTE_SCHEMA_MISMATCH"
        elif missing_hash_rows or hash_mismatch_rows:
            status = "MORPHOLOGICAL_SEED_DESCRIPTOR_AUDIT_REJECTED_HASH_FAILURE"
            decision = "DO_NOT_ROUTE_HASH_FAILURE"
        elif hits:
            status = "MORPHOLOGICAL_SEED_DESCRIPTOR_AUDIT_REJECTED_ENDPOINT_TOKEN_HIT"
            decision = "DO_NOT_ROUTE_ENDPOINT_LEAKAGE_RISK"
        elif self_acceptance_rows or incomplete_boundary_rows:
            status = "MORPHOLOGICAL_SEED_DESCRIPTOR_AUDIT_REJECTED_CLAIM_BOUNDARY_FAILURE"
            decision = "DO_NOT_ROUTE_CLAIM_BOUNDARY_FAILURE"
        else:
            status = "MORPHOLOGICAL_SEED_DESCRIPTOR_AUDIT_READY_FOR_ACTIVATION_QUOTIENT_AUDIT"
            decision = "ROUTE_TO_ACTIVATION_QUOTIENT_AUDIT_NOT_ACCEPTED"

    hits = endpoint_hits(rows)
    return {
        "report_id": "tau_cmb_morphological_seed_descriptor_candidate_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_candidate": rel(candidate_path),
        "status": status,
        "decision": decision,
        "rows_received": len(rows),
        "missing_required_columns": missing_columns,
        "missing_components": missing_components,
        "extra_components": extra_components,
        "missing_hash_rows": sorted(missing_hash_rows),
        "hash_mismatch_rows": sorted(hash_mismatch_rows),
        "endpoint_token_hits": hits,
        "self_acceptance_rows": sorted(self_acceptance_rows),
        "incomplete_boundary_rows": sorted(incomplete_boundary_rows),
        "seed_acceptance_allowed": False,
        "source_acceptance_allowed": False,
        "A_tau_derivation_allowed": False,
        "phi_tau_derivation_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "next_minimal_unblock": "build_morphological_seed_activation_quotient_audit",
    }


def write_doc(report: dict[str, Any], path: Path) -> None:
    def bullet(values: list[Any]) -> str:
        return "\n".join(f"- `{value}`" for value in values) or "- none"

    text = f"""# Tau CMB Morphological Seed Descriptor Candidate Audit v01

**Doc class:** morphological-seed descriptor candidate audit
**Status:** {report["status"]}
**Decision:** {report["decision"]}

## Claim Boundary

```text
{report["claim_boundary"]}
```

## Audited Candidate

```text
{report["audited_candidate"]}
```

## Audit Result

```text
{report["decision"]}
```

This audit does not accept the seed. It only decides whether the candidate is
clean enough to route to activation/quotient/readout audits.

## Missing Columns

{bullet(report["missing_required_columns"])}

## Missing Components

{bullet(report["missing_components"])}

## Hash Problems

Missing hash rows:

{bullet(report["missing_hash_rows"])}

Hash mismatch rows:

{bullet(report["hash_mismatch_rows"])}

## Endpoint Token Hits

{bullet([f"{hit['seed_row_id']}:{hit['token']}" for hit in report["endpoint_token_hits"]])}

## Claim Boundary Problems

Self-acceptance rows:

{bullet(report["self_acceptance_rows"])}

Incomplete boundary rows:

{bullet(report["incomplete_boundary_rows"])}

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB morphological seed descriptor candidate.")
    parser.add_argument("--candidate", default=str(DEFAULT_CANDIDATE))
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    report = build_report(Path(args.candidate))
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(report, Path(args.write_doc))
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
