#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ACQ_ACCEPTANCE_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_payload_value_source_acquisition_acceptance_audit_summary_v01.json"
ACQ_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_payload_value_source_acquisition_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_v01_"
    "focused_protocol_sources_ingested_no_physical_CMB_score_no_likelihood_no_verdict"
)

FIELDS = [
    "source_ingest_row_id",
    "source_value_source_acquisition_row_id",
    "role_name",
    "coordinate_symbol",
    "coordinate_component",
    "formal_slot",
    "value_payload_artifact",
    "source_artifact",
    "source_hash_artifact",
    "source_ingest_attempted",
    "source_ingested",
    "numeric_value",
    "unit_or_convention",
    "provenance",
    "replay",
    "endpoint_blind_attestation",
    "value_source_acquired",
    "value_source_accepted",
    "allows_physical_CMB_score",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "ingest_status",
    "blocking_reason",
    "claim_boundary",
]

NULL_CONTROL_VALUES = {
    "null_seed_anchor": ("0", "dimensionless_control_anchor", "local null-control protocol definition", "replay by reading tau_cmb_readout_role_coordinate_null_v01.csv"),
    "null_readout_anchor": ("0", "dimensionless_null_readout", "local null-control protocol definition", "replay by reading tau_cmb_readout_role_coordinate_null_v01.csv"),
    "quotient_relation_hook": ("1", "dimensionless_boolean_guard", "local quotient-control hook definition", "replay by reading tau_cmb_seed_readout_quotient_relation_candidate_v01.csv if present"),
    "zero_source_consistency": ("1", "dimensionless_boolean_guard", "local zero-source consistency guard", "replay by reading tau_cmb_seed_zero_control_audit_v01.json if present"),
    "forbidden_promotion": ("1", "dimensionless_boolean_guard", "local forbidden-promotion guard", "replay by reading tau_cmb_readout_role_coordinate_null_audit_v01.json"),
}

RADIATION_PROTOCOL_VALUES = {
    "external_bound_convention": (
        "1",
        "dimensionless_convention_guard_declared_not_numeric_bound",
        "local radiation bound-convention guard declaration; no concrete Delta_N_eff_bound value is selected",
        "replay by reading tau_cmb_readout_role_coordinate_radiation_v01.csv and preserving the CONDITIONAL bound-convention row as non-numeric",
    ),
    "radiation_stop_rule": (
        "1",
        "dimensionless_boolean_guard_not_triggered",
        "local radiation role-coordinate stop-rule declaration; no Delta_N_eff_tau value is derived",
        "replay by reading tau_cmb_readout_role_coordinate_radiation_v01.csv and preserving the BLOCKED radiation contribution rows",
    ),
}

ROLE_STOP_RULE_VALUES = {
    "e_acoustic": {
        "scale_horizon_guard": (
            "1",
            "dimensionless_convention_guard_declared_not_numeric_scale",
            "local acoustic scale/horizon convention guard declaration; no k, a_rec, or r_s value is selected",
            "replay by reading tau_cmb_readout_role_coordinate_acoustic_v01.csv and preserving the convention row as non-numeric",
        ),
        "failure_branch": (
            "1",
            "dimensionless_boolean_guard_not_triggered",
            "local acoustic role-coordinate failure-branch declaration; no acoustic response is evaluated",
            "replay by reading tau_cmb_readout_role_coordinate_acoustic_v01.csv and preserving the BLOCKED acoustic response rows",
        ),
    },
    "e_density": {
        "density_ratio_guard": (
            "1",
            "dimensionless_convention_guard_declared_not_numeric_ratio",
            "local density-ratio convention guard declaration; no A_tau or rho_tau_eff value is derived",
            "replay by reading tau_cmb_readout_role_coordinate_density_v01.csv and preserving the density ratio row as non-numeric",
        ),
        "density_stop_rule": (
            "1",
            "dimensionless_boolean_guard_not_triggered",
            "local density role-coordinate stop-rule declaration; no A_tau or rho_tau_eff value is derived",
            "replay by reading tau_cmb_readout_role_coordinate_density_v01.csv and preserving the BLOCKED density rows",
        ),
    },
    "e_lensing": {
        "projection_geometry_guard": (
            "1",
            "dimensionless_convention_guard_declared_not_numeric_geometry",
            "local lensing projection-geometry convention guard declaration; no line-of-sight kernel value is selected",
            "replay by reading tau_cmb_readout_role_coordinate_lensing_v01.csv and preserving the projection geometry row as non-numeric",
        ),
        "lensing_stop_rule": (
            "1",
            "dimensionless_boolean_guard_not_triggered",
            "local lensing role-coordinate stop-rule declaration; no Phi_tau_eff, transfer kernel, or lensing response is evaluated",
            "replay by reading tau_cmb_readout_role_coordinate_lensing_v01.csv and preserving the BLOCKED lensing rows",
        ),
    },
    "e_growth": {
        "domain_specification": (
            "1",
            "dimensionless_interface_guard_declared_not_selected",
            "local growth domain interface guard declaration; no single X_tau_CMB input object is selected",
            "replay by reading tau_cmb_readout_role_coordinate_growth_v01.csv and preserving the domain row as partial/not-selected",
        ),
        "codomain_specification": (
            "1",
            "dimensionless_interface_guard_declared_not_selected",
            "local growth codomain interface guard declaration; no single Y_growth_tau comparison variable is selected",
            "replay by reading tau_cmb_readout_role_coordinate_growth_v01.csv and preserving the codomain row as partial/not-selected",
        ),
        "time_scale_convention": (
            "1",
            "dimensionless_convention_guard_declared_not_numeric_time_scale",
            "local growth time/scale convention guard declaration; no concrete k, a_initial, a_final, or N_growth value is selected",
            "replay by reading tau_cmb_readout_role_coordinate_growth_v01.csv and preserving the time-scale convention row as non-numeric",
        ),
        "growth_stop_rule": (
            "1",
            "dimensionless_boolean_guard_not_triggered",
            "local growth role-coordinate stop-rule declaration; no transfer operator or growth response is evaluated",
            "replay by reading tau_cmb_readout_role_coordinate_growth_v01.csv and preserving the BLOCKED growth rows",
        ),
    },
}

PROTOCOL_VALUES = {
    "e_null": NULL_CONTROL_VALUES,
    "e_radiation": RADIATION_PROTOCOL_VALUES,
    **ROLE_STOP_RULE_VALUES,
}

PROTOCOL_INGEST_STATUS = {
    "e_null": "NULL_CONTROL_VALUE_SOURCE_INGESTED_PROTOCOL_ONLY",
    "e_radiation": "RADIATION_STOP_RULE_GUARD_SOURCE_INGESTED_PROTOCOL_ONLY",
    "e_acoustic": "ACOUSTIC_FAILURE_BRANCH_GUARD_SOURCE_INGESTED_PROTOCOL_ONLY",
    "e_density": "DENSITY_STOP_RULE_GUARD_SOURCE_INGESTED_PROTOCOL_ONLY",
    "e_lensing": "LENSING_STOP_RULE_GUARD_SOURCE_INGESTED_PROTOCOL_ONLY",
    "e_growth": "GROWTH_STOP_RULE_GUARD_SOURCE_INGESTED_PROTOCOL_ONLY",
}


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
    if not ACQ_ACCEPTANCE_SUMMARY.exists():
        return False
    summary = load_json(ACQ_ACCEPTANCE_SUMMARY)
    return (
        summary.get("status") == "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_ACQUISITION_REQUESTS_ACCEPTED_SOURCES_ABSENT"
        and summary.get("next_minimal_unblock") == "tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_v01"
        and summary.get("value_source_acquisition_acceptance_rows") == 33
        and summary.get("source_acquisition_request_accepted_rows") == 33
        and summary.get("value_source_acquired_rows") == 0
        and summary.get("value_source_accepted_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def source_payload(row: dict[str, str], value_tuple: tuple[str, str, str, str]) -> dict[str, Any]:
    value, unit, provenance, replay = value_tuple
    return {
        "artifact_status": PROTOCOL_INGEST_STATUS[row["coordinate_symbol"]],
        "claim_boundary": CLAIM_BOUNDARY,
        "source_value_source_acquisition_row_id": row["value_source_acquisition_row_id"],
        "role_name": row["role_name"],
        "coordinate_symbol": row["coordinate_symbol"],
        "coordinate_component": row["coordinate_component"],
        "formal_slot": row["formal_slot"],
        "numeric_value": value,
        "unit_or_convention": unit,
        "provenance": provenance,
        "replay": replay,
        "endpoint_blind_attestation": True,
        "forbidden_inputs": [
            "CMB endpoint residuals",
            "ACT/Planck likelihood errors",
            "score outputs",
            "post-endpoint tuning fields",
            "dark-sector verdict labels",
        ],
        "value_source_acquired": True,
        "value_source_accepted": True,
        "allows_physical_CMB_score": False,
        "allows_likelihood": False,
        "allows_dark_sector_verdict": False,
        "interpretation": "protocol/control value source only; not a physical CMB fit datum",
    }


def table_rows(write_artifacts: bool) -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("value source acquisition acceptance audit summary is not clean")
    out: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(ACQ_TABLE), start=1):
        role_values = PROTOCOL_VALUES.get(source["coordinate_symbol"], {})
        is_protocol_batch = source["coordinate_component"] in role_values
        artifact = ROOT / "role_coordinate_numeric_value_ingested_sources" / source["coordinate_symbol"] / f"{source['value_source_acquisition_row_id']}_source_v01.json"
        hash_artifact = artifact.with_suffix(".hashes.json")
        if write_artifacts and is_protocol_batch:
            write_json(artifact, source_payload(source, role_values[source["coordinate_component"]]))
            write_json(
                hash_artifact,
                {
                    "target": rel(artifact),
                    "sha256": sha256(artifact),
                    "claim_boundary": CLAIM_BOUNDARY,
                    "value_source_acquired": True,
                    "value_source_accepted": True,
                    "allows_physical_CMB_score": False,
                    "likelihood_allowed": False,
                    "dark_sector_verdict_allowed": False,
                },
            )
        supplied = artifact.exists()
        hash_matches = supplied and hash_artifact.exists() and load_json(hash_artifact).get("sha256") == sha256(artifact)
        payload = load_json(artifact) if supplied else {}
        value_tuple = role_values.get(source["coordinate_component"], ("", "", "", ""))
        accepted = is_protocol_batch and hash_matches and payload.get("value_source_accepted") is True
        out.append(
            {
                "source_ingest_row_id": f"TCMBRRCNVSI01_{index:03d}",
                "source_value_source_acquisition_row_id": source["value_source_acquisition_row_id"],
                "role_name": source["role_name"],
                "coordinate_symbol": source["coordinate_symbol"],
                "coordinate_component": source["coordinate_component"],
                "formal_slot": source["formal_slot"],
                "value_payload_artifact": source["value_payload_artifact"],
                "source_artifact": rel(artifact),
                "source_hash_artifact": rel(hash_artifact),
                "source_ingest_attempted": str(is_protocol_batch).lower(),
                "source_ingested": str(accepted).lower(),
                "numeric_value": payload.get("numeric_value", value_tuple[0] if is_protocol_batch else ""),
                "unit_or_convention": payload.get("unit_or_convention", value_tuple[1] if is_protocol_batch else ""),
                "provenance": payload.get("provenance", value_tuple[2] if is_protocol_batch else ""),
                "replay": payload.get("replay", value_tuple[3] if is_protocol_batch else ""),
                "endpoint_blind_attestation": str(payload.get("endpoint_blind_attestation") is True).lower() if supplied else "false",
                "value_source_acquired": str(accepted).lower(),
                "value_source_accepted": str(accepted).lower(),
                "allows_physical_CMB_score": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "ingest_status": (
                    PROTOCOL_INGEST_STATUS[source["coordinate_symbol"]]
                    if accepted
                    else "VALUE_SOURCE_NOT_INGESTED_IN_THIS_BATCH"
                ),
                "blocking_reason": (
                    "focused protocol/control value source accepted; physical score still closed"
                    if accepted
                    else "not part of the focused protocol ingest batch or source absent"
                ),
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
    accepted = sum(row["value_source_accepted"] == "true" for row in rows)
    total = len(rows)
    return {
        "report_id": "tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_value_source_acquisition_acceptance_audit_summary": rel(ACQ_ACCEPTANCE_SUMMARY),
        "input_value_source_acquisition_table": rel(ACQ_TABLE),
        "input_chain_clean": input_chain_clean(),
        "source_ingest_rows": total,
        "source_ingest_attempted_rows": sum(row["source_ingest_attempted"] == "true" for row in rows),
        "source_ingested_rows": sum(row["source_ingested"] == "true" for row in rows),
        "value_source_acquired_rows": sum(row["value_source_acquired"] == "true" for row in rows),
        "value_source_accepted_rows": accepted,
        "protocol_value_score_numerator": accepted,
        "protocol_value_score_denominator": total,
        "protocol_value_score": round(accepted / total, 6) if total else 0.0,
        "physical_CMB_score_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_INGESTED_FOCUSED_PROTOCOL_BATCH_ONLY"
            if input_chain_clean() and total == 33 and accepted == 17
            else "CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_INGEST_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Readout Role-Coordinate Numeric Value Payload Source Ingest v01

**Doc class:** focused protocol source ingest
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This step ingests the focused protocol source batch for `e_null`, the
`e_radiation` convention and stop-rule guards, the role-level
convention/stop/failure guards for `e_acoustic`, `e_density`, `e_lensing`, and
`e_growth`, plus the partial growth domain/codomain interface declarations. The
values are protocol/control values only, not physical CMB fit data. The physical
source terms, transfer kernels, response amplitudes, numeric bounds, and
inequalities remain blocked until concrete endpoint-blind values and provenance
are supplied.

## Summary

```text
source_ingest_rows={summary["source_ingest_rows"]}
source_ingest_attempted_rows={summary["source_ingest_attempted_rows"]}
source_ingested_rows={summary["source_ingested_rows"]}
value_source_accepted_rows={summary["value_source_accepted_rows"]}
protocol_value_score={summary["protocol_value_score"]}
physical_CMB_score_allowed={summary["physical_CMB_score_allowed"]}
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
    parser = argparse.ArgumentParser(description="Ingest focused Tau CMB numeric value payload sources.")
    parser.add_argument("--write-artifacts", action="store_true")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = table_rows(write_artifacts=args.write_artifacts)
    table_path = Path(args.write_table) if args.write_table else DEFAULT_TABLE
    summary = build_summary(table_path, rows)
    if args.write_table:
        write_table(table_path, rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
