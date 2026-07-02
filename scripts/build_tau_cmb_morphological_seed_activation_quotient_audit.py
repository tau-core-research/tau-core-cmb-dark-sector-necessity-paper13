#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SEED_AUDIT = ROOT / "data/derived/tau_cmb_morphological_seed_descriptor_candidate_audit_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_morphological_seed_activation_quotient_audit_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_morphological_seed_activation_quotient_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_morphological_seed_activation_quotient_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_morphological_seed_activation_quotient_audit_v01_audit_only_"
    "no_seed_acceptance_no_A_tau_derivation_no_source_acceptance_no_phi_derivation_no_score_no_verdict"
)

FIELDS = [
    "audit_row_id",
    "audit_gate",
    "required_condition",
    "available_evidence",
    "audit_status",
    "blocking_reason",
    "next_required_artifact",
    "allows_seed_acceptance",
    "allows_A_tau_derivation",
    "allows_source_acceptance",
    "allows_score_entry",
    "claim_boundary",
]

ROWS = [
    {
        "audit_gate": "candidate_cleanliness",
        "required_condition": "descriptor candidate must be schema-complete, hash-consistent, endpoint-clean, and claim-bounded",
        "available_evidence": "tau_cmb_morphological_seed_descriptor_candidate_audit_v01",
        "audit_status": "PASSED_ROUTE_ONLY_NOT_ACCEPTANCE",
        "blocking_reason": "cleanliness permits routing but does not prove activation",
        "next_required_artifact": "none",
    },
    {
        "audit_gate": "morphology_activation_sufficiency",
        "required_condition": "show that seed_tau_CMB can activate an A_tau(a,k) role without endpoint residuals",
        "available_evidence": "seed descriptor references morphology-conditioned projection principle",
        "audit_status": "BLOCKED_ACTIVATION_NOT_PROVED",
        "blocking_reason": "no activation rule maps seed_tau_CMB to A_tau(a,k)",
        "next_required_artifact": "tau_cmb_morphological_seed_activation_rule_candidate_v01",
    },
    {
        "audit_gate": "quotient_null_survival",
        "required_condition": "show seed is not erased by null/gauge/readout quotient controls",
        "available_evidence": "forbidden endpoint inputs and readout context are declared",
        "audit_status": "BLOCKED_QUOTIENT_SURVIVAL_NOT_PROVED",
        "blocking_reason": "no null model, quotient map, or survival test is supplied for the CMB seed",
        "next_required_artifact": "tau_cmb_morphological_seed_quotient_survival_test_v01",
    },
    {
        "audit_gate": "closure_stability",
        "required_condition": "show seed can enter a stable closure path toward rho_tau_eff/Phi_tau_eff obligations",
        "available_evidence": "derivation spine binding is declared",
        "audit_status": "BLOCKED_CLOSURE_STABILITY_NOT_PROVED",
        "blocking_reason": "no closure operator or stable source path is supplied",
        "next_required_artifact": "tau_cmb_morphological_seed_closure_stability_test_v01",
    },
    {
        "audit_gate": "readout_survival",
        "required_condition": "show seed survives CMB readout family into acoustic/lensing/growth/radiation roles",
        "available_evidence": "CMB role/readout family is declared but unscored",
        "audit_status": "BLOCKED_READOUT_SURVIVAL_NOT_PROVED",
        "blocking_reason": "no readout-survival response or non-null channel is supplied",
        "next_required_artifact": "tau_cmb_morphological_seed_readout_survival_test_v01",
    },
    {
        "audit_gate": "firewall_replay",
        "required_condition": "provide endpoint firewall certificate and replay rule for the seed descriptor",
        "available_evidence": "endpoint-token audit passed for descriptor candidate",
        "audit_status": "BLOCKED_FIREWALL_REPLAY_NOT_CERTIFIED",
        "blocking_reason": "no seed-specific firewall certificate or replay transcript is supplied",
        "next_required_artifact": "tau_cmb_morphological_seed_firewall_replay_certificate_v01",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def table_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_row_id": f"TCMBMSAQA01_{index:03d}",
            "allows_seed_acceptance": "false",
            "allows_A_tau_derivation": "false",
            "allows_source_acceptance": "false",
            "allows_score_entry": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            **row,
        }
        for index, row in enumerate(ROWS, start=1)
    ]


def write_table(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_summary(seed_audit_path: Path, table_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    seed_audit = read_json(seed_audit_path)
    blocked = [row for row in rows if row["audit_status"].startswith("BLOCKED")]
    passed_route_only = [row for row in rows if row["audit_status"].startswith("PASSED")]
    return {
        "report_id": "tau_cmb_morphological_seed_activation_quotient_audit_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "seed_descriptor_audit": rel(seed_audit_path),
        "seed_descriptor_audit_status": seed_audit.get("status", "UNKNOWN"),
        "table": rel(table_path),
        "audit_rows": len(rows),
        "passed_route_only_rows": len(passed_route_only),
        "blocked_rows": len(blocked),
        "seed_acceptance_allowed": False,
        "A_tau_derivation_allowed": False,
        "source_acceptance_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "MORPHOLOGICAL_SEED_ACTIVATION_QUOTIENT_AUDIT_BLOCKED_NOT_ACCEPTED",
        "next_minimal_unblock": "build_tau_cmb_morphological_seed_activation_rule_candidate_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        (
            f"- `{row['audit_row_id']}` `{row['audit_gate']}`: {row['audit_status']} | "
            f"blocks: {row['blocking_reason']}"
        )
        for row in rows
    )
    text = f"""# Tau CMB Morphological Seed Activation/Quotient Audit v01

**Doc class:** morphological-seed activation and quotient audit
**Status:** {summary["status"]}
**Seed descriptor audit:** `{summary["seed_descriptor_audit"]}`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact audits whether the endpoint-blind morphological-seed descriptor
candidate can move toward an `A_tau(a,k)` activation route. It does not accept
the seed and does not derive `A_tau`.

## Audit Rows

{row_text}

## Interpretation

The seed descriptor is clean enough to route into deeper audits, but it is not
sufficient for activation. The missing pieces are an activation rule, quotient
survival, closure stability, readout survival, and seed-specific firewall/replay
evidence.

## Status

```text
{summary["status"]}
```

No seed acceptance, `A_tau(a,k)` derivation, source acceptance, `Phi_tau_eff`
derivation, score entry, or dark-sector verdict is allowed.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB morphological seed activation/quotient audit.")
    parser.add_argument("--seed-audit", default=str(DEFAULT_SEED_AUDIT))
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    table_path = Path(args.write_table or DEFAULT_TABLE)
    rows = table_rows()
    if args.write_table:
        write_table(table_path, rows)
    summary = build_summary(Path(args.seed_audit), table_path, rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), rows, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
