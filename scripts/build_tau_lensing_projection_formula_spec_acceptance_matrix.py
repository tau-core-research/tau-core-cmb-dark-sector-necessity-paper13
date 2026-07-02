#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "data/derived/cmb_tau_lensing_projection_formula_spec_acceptance_matrix_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/cmb_tau_lensing_projection_formula_spec_acceptance_matrix_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_projection_formula_spec_acceptance_matrix_v01.md"


ROWS = [
    {
        "row_id": "TCMBPFSAM01_001",
        "acceptance_area": "projection_equation",
        "required_artifact": "docs/cmb_tau_lensing_projection_equation_spec_scaffold_v01.md",
        "current_status": "PROJECTION_EQUATION_SPEC_DECLARED_NOT_FILLED",
        "acceptance_condition": "operator equation, linearity/baseline policy, composition order, and materialization rule are fixed before endpoint comparison",
        "blocks": "physical Tau-grid materialization and score",
    },
    {
        "row_id": "TCMBPFSAM01_002",
        "acceptance_area": "kernel_measure",
        "required_artifact": "docs/cmb_tau_lensing_projection_kernel_measure_spec_scaffold_v01.md",
        "current_status": "KERNEL_MEASURE_SPEC_DECLARED_NOT_FILLED",
        "acceptance_condition": "domain support, measure, L mapping, units/sign, integrability, and kernel artifact are supplied endpoint-blind",
        "blocks": "finite PP-grid replay",
    },
    {
        "row_id": "TCMBPFSAM01_003",
        "acceptance_area": "normalization",
        "required_artifact": "docs/cmb_tau_lensing_projection_normalization_spec_scaffold_v01.md",
        "current_status": "NORMALIZATION_SPEC_DECLARED_NOT_FILLED",
        "acceptance_condition": "N_projection_physical is derived from operator convention, not from score residuals or post-score alpha_star",
        "blocks": "accepted physical projection operator packet",
    },
    {
        "row_id": "TCMBPFSAM01_004",
        "acceptance_area": "output_replay",
        "required_artifact": "docs/cmb_tau_lensing_projection_output_replay_spec_scaffold_v01.md",
        "current_status": "OUTPUT_REPLAY_SPEC_DECLARED_NOT_FILLED",
        "acceptance_condition": "3000-row L=10..3009 grid is produced by replay from hash-bound source, equation, kernel, normalization, and route artifacts",
        "blocks": "score input handoff",
    },
    {
        "row_id": "TCMBPFSAM01_005",
        "acceptance_area": "zero_source_limit",
        "required_artifact": "docs/cmb_tau_lensing_projection_zero_source_limit_obligation_v01.md",
        "current_status": "PROOF_OBLIGATION_DECLARED_NOT_DISCHARGED",
        "acceptance_condition": "zero Tau source algebraically gives zero direct Tau PP contribution under the supplied operator",
        "blocks": "known-limit and null-control acceptance",
    },
    {
        "row_id": "TCMBPFSAM01_006",
        "acceptance_area": "dimension_sign_audit",
        "required_artifact": "docs/cmb_tau_lensing_projection_dimension_sign_audit_scaffold_v01.md",
        "current_status": "AUDIT_SCHEMA_DECLARED_NOT_FILLED",
        "acceptance_condition": "domain, kernel-measure, normalization, codomain, zero-limit, and firewall rows pass dimension/sign audit",
        "blocks": "review-safe operator acceptance",
    },
    {
        "row_id": "TCMBPFSAM01_007",
        "acceptance_area": "post_population_firewall",
        "required_artifact": "docs/cmb_tau_lensing_projection_post_population_firewall_spec_scaffold_v01.md",
        "current_status": "POST_POPULATION_FIREWALL_SPEC_DECLARED_NOT_RUN",
        "acceptance_condition": "firewall is rerun after values are populated and proves no endpoint residual, score, or verdict preference shaped the route",
        "blocks": "endpoint-blind score attempt",
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
        "report_id": "cmb_tau_lensing_projection_formula_spec_acceptance_matrix_summary_v01",
        "claim_boundary": "projection_formula_spec_acceptance_matrix_only_no_operator_acceptance_no_grid_no_score_no_dark_sector_verdict",
        "table": rel(table_path),
        "status": "FORMULA_SPEC_ACCEPTANCE_MATRIX_DECLARED_BLOCKED",
        "target": "accepted endpoint-blind Projection_PP[Phi_lens_tau](L) formula-spec",
        "rows": len(ROWS),
        "blocking_rows": [row["row_id"] for row in ROWS],
        "accepted_rows": [],
        "only_two_valid_next_paths": [
            "SUPPLY_ENDPOINT_BLIND_OPERATOR_PACKET",
            "KEEP_EXPLICIT_NON_SCORE_FAILURE",
        ],
        "endpoint_blind_operator_packet_request": "docs/cmb_tau_lensing_endpoint_blind_operator_packet_request_v01.md",
        "blocked_shortcuts": [
            "do not score from the scaffold",
            "do not use post-score alpha_star as physical normalization",
            "do not use B_ACT adapter replay as the physical source-to-PP operator",
            "do not issue a dark-sector verdict before an accepted score route exists",
        ],
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(summary: dict[str, Any], path: Path) -> None:
    rows = "\n".join(
        (
            f"- `{row['row_id']}` `{row['acceptance_area']}`: {row['current_status']} | "
            f"artifact: `{row['required_artifact']}` | blocks: {row['blocks']}"
        )
        for row in ROWS
    )
    paths = "\n".join(f"- `{item}`" for item in summary["only_two_valid_next_paths"])
    shortcuts = "\n".join(f"- {item}" for item in summary["blocked_shortcuts"])
    text = f"""# CMB Tau Lensing Projection Formula-Spec Acceptance Matrix v01

**Doc class:** formula-spec acceptance matrix
**Reader role:** Paper 13 Tau-grid implementer
**Status:** blocked until endpoint-blind operator packet is supplied; not a score
**Canonical parent:** `docs/cmb_tau_lensing_projection_operator_formula_spec_scaffold_v01.md`

## Claim Boundary

```text
{summary["claim_boundary"]}
```

## Target

```text
{summary["target"]}
```

## Acceptance Matrix

{rows}

## Only Valid Next Paths

{paths}

## Endpoint-Blind Operator Packet Request

```text
{summary["endpoint_blind_operator_packet_request"]}
```

## Blocked Shortcuts

{shortcuts}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build projection formula-spec acceptance matrix.")
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
