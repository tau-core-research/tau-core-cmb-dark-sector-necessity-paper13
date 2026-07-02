#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "data/derived/cmb_tau_lensing_endpoint_blind_operator_packet_receipt_audit_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/cmb_tau_lensing_endpoint_blind_operator_packet_content_audit_router_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/cmb_tau_lensing_endpoint_blind_operator_packet_content_audit_router_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_endpoint_blind_operator_packet_content_audit_router_v01.md"


ROWS = [
    {
        "row_id": "TCMBEBOPCAR01_001",
        "packet_slot": "source_domain",
        "content_audit": "source_domain_endpoint_blindness_and_dimension_check",
        "acceptance_question": "Does Phi_lens_tau(a,k) come from endpoint-blind Tau-side artifacts with declared domain, support, units, and hash?",
        "routes_to": "projection_equation;kernel_measure;dimension_sign_audit",
    },
    {
        "row_id": "TCMBEBOPCAR01_002",
        "packet_slot": "projection_equation",
        "content_audit": "operator_equation_and_zero_preservation_check",
        "acceptance_question": "Does the equation map Phi_lens_tau to PP/delta_PP_tau with fixed baseline policy and zero-preserving behavior?",
        "routes_to": "zero_source_limit;dimension_sign_audit;operator_decision_gate",
    },
    {
        "row_id": "TCMBEBOPCAR01_003",
        "packet_slot": "kernel_measure",
        "content_audit": "kernel_measure_integrability_and_L_mapping_check",
        "acceptance_question": "Are support, measure, L mapping, units/sign, and integrability sufficient for finite L=10..3009 replay?",
        "routes_to": "output_replay;dimension_sign_audit",
    },
    {
        "row_id": "TCMBEBOPCAR01_004",
        "packet_slot": "normalization",
        "content_audit": "physical_normalization_independence_check",
        "acceptance_question": "Is N_projection_physical finite and derived from pre-score operator convention rather than endpoint residuals?",
        "routes_to": "dimension_sign_audit;operator_decision_gate",
    },
    {
        "row_id": "TCMBEBOPCAR01_005",
        "packet_slot": "output_replay",
        "content_audit": "grid_replay_and_hash_binding_check",
        "acceptance_question": "Can the 3000-row output grid be reproduced from source, equation, kernel, normalization, and route hashes?",
        "routes_to": "post_population_firewall;score_guard",
    },
    {
        "row_id": "TCMBEBOPCAR01_006",
        "packet_slot": "zero_source_limit",
        "content_audit": "zero_source_limit_discharge_check",
        "acceptance_question": "Does the supplied operator prove or replay Phi_lens_tau=0 -> zero Tau PP contribution?",
        "routes_to": "known_limit_audit;operator_decision_gate",
    },
    {
        "row_id": "TCMBEBOPCAR01_007",
        "packet_slot": "dimension_sign_audit",
        "content_audit": "dimension_sign_consistency_check",
        "acceptance_question": "Do source, kernel-measure, normalization, and PP/delta_PP_tau codomain dimensions and signs close?",
        "routes_to": "operator_decision_gate",
    },
    {
        "row_id": "TCMBEBOPCAR01_008",
        "packet_slot": "post_population_firewall",
        "content_audit": "post_population_endpoint_firewall_check",
        "acceptance_question": "After values are populated, is there evidence that no endpoint residual, score, or verdict preference shaped them?",
        "routes_to": "score_guard;operator_decision_gate",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_receipt() -> dict[str, Any]:
    if not RECEIPT.exists():
        return {
            "status": "RECEIPT_AUDIT_MISSING",
            "decision": "DO_NOT_SCORE_RECEIPT_AUDIT_MISSING",
            "supplied_slots": [],
        }
    return json.loads(RECEIPT.read_text())


def write_table(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_summary(table_path: Path) -> dict[str, Any]:
    receipt = read_receipt()
    receipt_ready = receipt.get("status") == "OPERATOR_PACKET_RECEIPT_AUDIT_READY_FOR_CONTENT_AUDITS"
    return {
        "report_id": "cmb_tau_lensing_endpoint_blind_operator_packet_content_audit_router_summary_v01",
        "claim_boundary": "endpoint_blind_operator_packet_content_audit_router_only_no_content_acceptance_no_grid_no_score_no_dark_sector_verdict",
        "table": rel(table_path),
        "receipt_audit": rel(RECEIPT),
        "receipt_status": receipt.get("status"),
        "receipt_decision": receipt.get("decision"),
        "status": "CONTENT_AUDIT_ROUTER_BLOCKED_UNTIL_RECEIPT_READY"
        if not receipt_ready
        else "CONTENT_AUDIT_ROUTER_READY_NOT_SCORE",
        "rows": len(ROWS),
        "routed_slots": [row["packet_slot"] for row in ROWS],
        "content_acceptance": False,
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(summary: dict[str, Any], path: Path) -> None:
    rows = "\n".join(
        (
            f"- `{row['packet_slot']}` -> `{row['content_audit']}` | "
            f"routes to: `{row['routes_to']}`"
        )
        for row in ROWS
    )
    text = f"""# CMB Tau Lensing Endpoint-Blind Operator Packet Content Audit Router v01

**Doc class:** content-audit router
**Reader role:** Paper 13 Tau-grid implementer
**Status:** {summary["status"]}
**Canonical parent:** `docs/cmb_tau_lensing_endpoint_blind_operator_packet_receipt_audit_v01.md`

## Claim Boundary

```text
{summary["claim_boundary"]}
```

## Receipt Status

```text
{summary["receipt_status"]}
{summary["receipt_decision"]}
```

## Routed Content Audits

{rows}

## Rule

This router does not accept physics content and does not allow scoring. It only
declares the next content audits after the endpoint-blind operator packet receipt
is complete.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build endpoint-blind operator packet content-audit router.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    table_path = Path(args.write_table or DEFAULT_TABLE)
    if args.write_table:
        write_table(table_path, ROWS)
    summary = build_summary(table_path)
    if args.write_summary:
        path = Path(args.write_summary)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    if args.write_doc:
        write_doc(summary, Path(args.write_doc))
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
