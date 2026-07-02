#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "data/derived/cmb_tau_lensing_route_b_parent_source_request_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_route_b_parent_source_request_v01.md"


def build_packet() -> dict[str, Any]:
    return {
        "report_id": "cmb_tau_lensing_route_b_parent_source_request_v01",
        "claim_boundary": "route_b_parent_source_request_only_no_parent_source_no_grid_no_score_no_dark_sector_verdict",
        "purpose": (
            "Define the exact endpoint-blind Route B parent-source deliverable needed before the "
            "Tau-grid materializer may write a physical-candidate upstream L response."
        ),
        "current_blocker": "missing_endpoint_blind_tau_derived_parent_tau_source_l_table",
        "required_output_files": {
            "parent_source_table": "payload_staging/tau_lensing_route_b_parent_source_v01.csv",
            "parent_source_config": "payload_staging/tau_lensing_route_b_parent_source_config_v01.json",
        },
        "parent_source_table_schema": {
            "rows": 3000,
            "l_column": "L",
            "value_column": "parent_tau_source_value",
            "l_values": "exact integer sequence 10..3009",
            "value_requirement": (
                "finite numeric Tau-derived parent-source values; not a template, not a "
                "diagnostic probe, not a zero-control promoted as physics"
            ),
        },
        "parent_source_config_required_fields": [
            "config_id",
            "selected_route",
            "response_rule",
            "parent_source_table",
            "parent_l_column",
            "parent_value_column",
            "normalization",
            "endpoint_blind_statement",
            "parameter_policy",
            "source_chain",
            "normalization_statement",
            "known_limit_statement",
            "claim_boundary",
        ],
        "fixed_config_values": {
            "selected_route": "delta_PP_tau_against_named_fiducial_PP",
            "response_rule": "linear_parent_source_v01",
            "parent_l_column": "L",
            "parent_value_column": "parent_tau_source_value",
        },
        "required_evidence": [
            "parent_tau_source(L) is derived from Tau-side morphology/source structure before endpoint score readout",
            "source_chain names the derivation artifacts or scripts that generated the table",
            "normalization is finite and fixed before any score, residual, or verdict inspection",
            "known-limit statement verifies parent_tau_source_value -> 0 implies delta_PP_tau -> 0",
            "parameter_policy excludes ACT/Planck residual fitting, reduced chi2 tuning, score tuning, and verdict preference",
            "replay command or generator is identified so the table can be regenerated",
        ],
        "forbidden_inputs": [
            "ACT residuals",
            "Planck residuals",
            "reduced chi2 tuning",
            "score output tuning",
            "dark-sector verdict preference",
            "diagnostic probe parameters",
            "zero-control definitions promoted as physical response",
            "template placeholders",
        ],
        "acceptance_commands": [
            "make tau-grid-route-b-parent-table-precheck",
            "make tau-grid-route-b-parent-dry-run",
            "make tau-grid-route-b-parent-write-staging",
            "make tau-grid-derivation-intake-audit",
            "make tau-grid-physical-candidate-precheck",
            "make tau-grid-handoff-write-staging",
            "make tau-grid-physical-candidate-package",
            "make staging-promote-delta-dry-run",
        ],
        "materialization_rule": (
            "delta_PP_tau(L)=normalization*parent_tau_source_value(L) for "
            "response_rule=linear_parent_source_v01"
        ),
        "outputs_after_materialization": {
            "upstream_table": "payload_staging/tau_lensing_upstream_l_response_v01.csv",
            "upstream_metadata": "payload_staging/tau_lensing_upstream_l_response_metadata_v01.json",
        },
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": "produce_the_parent_source_table_and_config_then_run_parent_table_precheck",
    }


def write_doc(packet: dict[str, Any], path: Path) -> None:
    text = "\n".join(
        [
            "# CMB Tau Lensing Route B Parent Source Request v01",
            "",
            "**Doc class:** endpoint-blind Route B parent-source fulfillment request",
            "**Status:** request only; no parent source, no grid, no score, no verdict",
            "**Canonical script:** `scripts/build_tau_lensing_route_b_parent_source_request.py`",
            "**Canonical parent:** `docs/cmb_tau_lensing_physical_candidate_upstream_request_v01.md`",
            "",
            "This document narrows the Tau-grid blocker to the first concrete Route B",
            "object that must be supplied: a Tau-derived parent-source L-table and its",
            "non-template materialization config.",
            "",
            "## Required Files",
            "",
            "```text",
            packet["required_output_files"]["parent_source_table"],
            packet["required_output_files"]["parent_source_config"],
            "```",
            "",
            "## Parent Source Table",
            "",
            "```text",
            "L,parent_tau_source_value",
            "10,<finite Tau-derived value>",
            "...",
            "3009,<finite Tau-derived value>",
            "```",
            "",
            "The table must contain exactly 3000 rows with integer `L=10..3009`.",
            "`parent_tau_source_value` must be finite and non-template. It must not be",
            "a diagnostic probe or a zero-control promoted as a physical Tau response.",
            "",
            "## Config Contract",
            "",
            "Required fields:",
            *[f"- `{field}`" for field in packet["parent_source_config_required_fields"]],
            "",
            "Fixed values:",
            *[f"- `{key}` = `{value}`" for key, value in packet["fixed_config_values"].items()],
            "",
            "## Required Evidence",
            "",
            *[f"- {item}" for item in packet["required_evidence"]],
            "",
            "## Forbidden Inputs",
            "",
            *[f"- {item}" for item in packet["forbidden_inputs"]],
            "",
            "## Materialization Rule",
            "",
            "```text",
            packet["materialization_rule"],
            "```",
            "",
            "This rule is only an adapter from an already justified Tau parent source",
            "into the upstream L-response format. It does not prove the parent source.",
            "",
            "## Acceptance Commands",
            "",
            "```text",
            *packet["acceptance_commands"],
            "```",
            "",
            "## Claim Boundary",
            "",
            "```text",
            packet["claim_boundary"],
            "```",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Route B parent-source request packet.")
    parser.add_argument("--write-packet", nargs="?", const=str(DEFAULT_PACKET))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()

    packet = build_packet()
    text = json.dumps(packet, indent=2, sort_keys=True)
    if args.write_packet:
        path = Path(args.write_packet)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    if args.write_doc:
        write_doc(packet, Path(args.write_doc))
    print(text)


if __name__ == "__main__":
    main()
