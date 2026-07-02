#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "data/derived/cmb_tau_lensing_endpoint_blind_operator_packet_request_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/cmb_tau_lensing_endpoint_blind_operator_packet_request_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_endpoint_blind_operator_packet_request_v01.md"


ROWS = [
    {
        "row_id": "TCMBEBOPR01_001",
        "packet_slot": "source_domain",
        "required_object": "Phi_lens_tau(a,k) domain declaration",
        "required_evidence": "endpoint-blind Phi_tau_eff/T_tau_CMB derivation artifact, domain support, units, and hash",
        "acceptance_gate": "domain matches projection equation and is not inferred from ACT/Planck residuals",
        "fills_matrix_row": "TCMBPFSAM01_001;TCMBPFSAM01_002",
        "current_status": "REQUESTED_NOT_SUPPLIED",
    },
    {
        "row_id": "TCMBEBOPR01_002",
        "packet_slot": "projection_equation",
        "required_object": "Projection_PP[Phi_lens_tau](L) equation",
        "required_evidence": "operator form, linearity or zero-preserving nonlinear policy, baseline/delta policy, composition order",
        "acceptance_gate": "equation is fixed before endpoint comparison and maps source domain to PP/delta_PP_tau codomain",
        "fills_matrix_row": "TCMBPFSAM01_001;TCMBPFSAM01_005",
        "current_status": "REQUESTED_NOT_SUPPLIED",
    },
    {
        "row_id": "TCMBEBOPR01_003",
        "packet_slot": "kernel_measure",
        "required_object": "K_tau_PP(L; a,k)dmu(a,k)",
        "required_evidence": "kernel table/equation, support, measure weights, L=10..3009 mapping, integrability bound, hash",
        "acceptance_gate": "finite kernel-measure is endpoint-blind and sufficient to replay every output L",
        "fills_matrix_row": "TCMBPFSAM01_002;TCMBPFSAM01_006",
        "current_status": "REQUESTED_NOT_SUPPLIED",
    },
    {
        "row_id": "TCMBEBOPR01_004",
        "packet_slot": "normalization",
        "required_object": "N_projection_physical",
        "required_evidence": "finite value or finite endpoint-blind range derived from operator convention, units, and sign",
        "acceptance_gate": "normalization is not fitted from score residuals, post-score alpha_star, or verdict preference",
        "fills_matrix_row": "TCMBPFSAM01_003;TCMBPFSAM01_006",
        "current_status": "REQUESTED_NOT_SUPPLIED",
    },
    {
        "row_id": "TCMBEBOPR01_005",
        "packet_slot": "output_replay",
        "required_object": "3000-row projected Tau-grid",
        "required_evidence": "replay script/command, input hashes, exact L=10..3009 axis, finite values, route declaration",
        "acceptance_gate": "grid is generated from source/equation/kernel/normalization artifacts before score",
        "fills_matrix_row": "TCMBPFSAM01_004",
        "current_status": "REQUESTED_NOT_SUPPLIED",
    },
    {
        "row_id": "TCMBEBOPR01_006",
        "packet_slot": "zero_source_limit",
        "required_object": "zero-source proof or replay",
        "required_evidence": "algebraic proof or replay showing Phi_lens_tau=0 gives zero Tau PP contribution",
        "acceptance_gate": "proof follows from supplied operator and does not substitute a synthetic control route for the physical operator",
        "fills_matrix_row": "TCMBPFSAM01_005",
        "current_status": "REQUESTED_NOT_SUPPLIED",
    },
    {
        "row_id": "TCMBEBOPR01_007",
        "packet_slot": "dimension_sign_audit",
        "required_object": "dimension/sign audit table",
        "required_evidence": "source units, kernel-measure units, normalization role, PP/delta_PP_tau codomain, sign convention",
        "acceptance_gate": "audit passes before materialization and before endpoint comparison",
        "fills_matrix_row": "TCMBPFSAM01_006",
        "current_status": "REQUESTED_NOT_SUPPLIED",
    },
    {
        "row_id": "TCMBEBOPR01_008",
        "packet_slot": "post_population_firewall",
        "required_object": "post-population endpoint firewall certificate",
        "required_evidence": "hash/provenance proof that operator, kernel, normalization, route, and grid were not shaped by endpoint residuals, score, or verdict preference",
        "acceptance_gate": "firewall passes after values are populated and before score is attempted",
        "fills_matrix_row": "TCMBPFSAM01_007",
        "current_status": "REQUESTED_NOT_SUPPLIED",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def write_table(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(ROWS[0].keys()))
        writer.writeheader()
        writer.writerows(ROWS)


def build_summary(table_path: Path) -> dict[str, Any]:
    return {
        "report_id": "cmb_tau_lensing_endpoint_blind_operator_packet_request_summary_v01",
        "claim_boundary": "endpoint_blind_operator_packet_request_only_no_operator_acceptance_no_grid_no_score_no_dark_sector_verdict",
        "table": rel(table_path),
        "status": "ENDPOINT_BLIND_OPERATOR_PACKET_REQUEST_OPEN",
        "target": "minimum supplied packet needed to test Projection_PP[Phi_lens_tau](L) for acceptance",
        "submission_template": "payload_templates/cmb_tau_lensing_endpoint_blind_operator_packet_submission_TEMPLATE_v01.csv",
        "intended_submission_path": "payloads/cmb_tau_lensing_endpoint_blind_operator_packet_submission_v01.csv",
        "rows": len(ROWS),
        "requested_rows": [row["row_id"] for row in ROWS],
        "accepts_automatic_scoring": False,
        "next_gate_after_supply": "operator_packet_receipt_audit",
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(summary: dict[str, Any], path: Path) -> None:
    rows = "\n".join(
        (
            f"- `{row['row_id']}` `{row['packet_slot']}`: {row['current_status']} | "
            f"object: {row['required_object']} | fills: `{row['fills_matrix_row']}`"
        )
        for row in ROWS
    )
    text = f"""# CMB Tau Lensing Endpoint-Blind Operator Packet Request v01

**Doc class:** endpoint-blind operator packet request
**Reader role:** Paper 13 Tau-grid implementer
**Status:** request open; no operator accepted; not a grid; not a score
**Canonical parent:** `docs/cmb_tau_lensing_projection_formula_spec_acceptance_matrix_v01.md`

## Claim Boundary

```text
{summary["claim_boundary"]}
```

## Target

```text
{summary["target"]}
```

## Submission Template

```text
{summary["submission_template"]}
```

## Intended Submission Path

```text
{summary["intended_submission_path"]}
```

## Requested Packet Slots

{rows}

## Submission Rule

The packet can only be considered after all requested slots are supplied with
endpoint-blind provenance. Supplying this packet does not itself allow a score:
it must first pass an operator-packet receipt audit, dimension/sign audit,
zero-source audit, replay audit, and post-population firewall.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build endpoint-blind operator packet request.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    table_path = Path(args.write_table or DEFAULT_TABLE)
    if args.write_table:
        write_table(table_path)
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
