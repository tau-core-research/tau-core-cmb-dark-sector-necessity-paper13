#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "data/derived/cmb_tau_lensing_physical_candidate_upstream_request_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_physical_candidate_upstream_request_v01.md"


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def build_packet() -> dict:
    return {
        "report_id": "cmb_tau_lensing_physical_candidate_upstream_request_v01",
        "claim_boundary": "physical_candidate_upstream_request_only_no_grid_no_score_no_dark_sector_verdict",
        "purpose": (
            "Define the exact upstream deliverable needed to replace the current control/probe "
            "with a Tau-derived endpoint-blind CMB lensing Tau-grid candidate."
        ),
        "required_output_files": {
            "table": "payload_staging/tau_lensing_upstream_l_response_v01.csv",
            "metadata": "payload_staging/tau_lensing_upstream_l_response_metadata_v01.json",
        },
        "table_schema": {
            "rows": 3000,
            "l_column": "L",
            "value_column": "tau_response_value",
            "l_values": "exact integers 10..3009",
            "value_requirement": "finite numeric delta_PP_tau(L) or tau_PP(L) response values",
        },
        "metadata_required_fields": [
            "selected_route",
            "l_column",
            "value_column",
            "formula_role",
            "endpoint_blind_statement",
            "parameter_policy",
            "source_chain",
            "normalization_statement",
            "known_limit_statement",
            "derivation_script_or_formula",
            "claim_boundary",
        ],
        "allowed_routes": {
            "route_A_transfer_projection": {
                "status": "preferred_physical_route",
                "chain": [
                    "rho_tau_eff(a,k) = A_tau(a,k) * rho_ref(a)",
                    "k^2 Phi_tau_eff(a,k) = 4*pi*G*a^2*rho_tau_eff(a,k)*Delta_tau(a,k)",
                    "Phi_lens_tau(a,k) = T_tau_CMB(k,a)[Phi_tau_eff]",
                    "tau_PP(L) = Projection_PP[Phi_lens_tau](L)",
                ],
                "minimum_evidence": [
                    "endpoint-blind A_tau(a,k) or equivalent Tau parent source",
                    "Phi_tau_eff normalization and sign convention",
                    "T_tau_CMB domain, codomain, time/scale convention, and operator rule",
                    "PP projection convention from lensing potential to L-space",
                    "known-limit audit against zero-response/LCDM comparison behavior",
                ],
            },
            "route_B_direct_L_space": {
                "status": "allowed_only_if_tau_derived_before_endpoint_score",
                "chain": [
                    "delta_PP_tau(L) = F_tau_L(parent_tau_source, readout_profile, scale_profile; L)",
                    "write exact L,value table without fitting ACT/Planck residuals",
                ],
                "minimum_evidence": [
                    "parent Tau source object used by F_tau_L",
                    "parameter-free or endpoint-blind parameter fixation rule",
                    "normalization convention for dimensionless delta_PP_tau(L)",
                    "known-limit audit showing zero/null behavior when Tau source is absent",
                ],
            },
        },
        "forbidden_inputs": [
            "ACT residuals",
            "Planck residuals",
            "reduced chi2 tuning",
            "score output tuning",
            "dark-sector verdict preference",
            "diagnostic probe parameters",
            "zero-control definitions promoted as physical response",
        ],
        "acceptance_commands": [
            "make tau-grid-physical-candidate-precheck",
            "make tau-grid-handoff-write-staging",
            "make tau-grid-physical-candidate-package",
            "make staging-promote-delta-dry-run",
        ],
        "current_blocker": "no_tau_derived_endpoint_blind_numeric_l_response_table",
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": (
            "produce the required upstream table and metadata from route_A or route_B, then run "
            "make tau-grid-physical-candidate-precheck"
        ),
    }


def write_doc(packet: dict, path: Path) -> None:
    route_a = packet["allowed_routes"]["route_A_transfer_projection"]
    route_b = packet["allowed_routes"]["route_B_direct_L_space"]
    text = "\n".join(
        [
            "# CMB Tau Lensing Physical Candidate Upstream Request v01",
            "",
            "**Doc class:** physical-candidate Tau-grid upstream request",
            "**Status:** request only; no grid, no score, no verdict",
            "**Canonical script:** `scripts/build_tau_lensing_physical_candidate_upstream_request.py`",
            "**Canonical parent:** `docs/cmb_tau_lensing_upstream_table_formula_spec_contract_v01.md`",
            "",
            "This request defines the exact upstream object needed to move from the current",
            "control/probe state to a physical-candidate Tau lensing grid.",
            "",
            "## Required Output",
            "",
            "```text",
            packet["required_output_files"]["table"],
            packet["required_output_files"]["metadata"],
            "```",
            "",
            "The table must contain exactly 3000 finite rows with `L=10..3009` and one",
            "`tau_response_value` per row.",
            "",
            "## Route A: Transfer Projection",
            "",
            f"Status: `{route_a['status']}`",
            "",
            "```text",
            *route_a["chain"],
            "```",
            "",
            "Minimum evidence:",
            *[f"- {item}" for item in route_a["minimum_evidence"]],
            "",
            "## Route B: Direct L-Space",
            "",
            f"Status: `{route_b['status']}`",
            "",
            "```text",
            *route_b["chain"],
            "```",
            "",
            "Minimum evidence:",
            *[f"- {item}" for item in route_b["minimum_evidence"]],
            "",
            "## Forbidden Inputs",
            "",
            *[f"- {item}" for item in packet["forbidden_inputs"]],
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
            "This request does not derive a Tau response. It only defines the deliverable",
            "that must exist before the physical-candidate Tau-grid path can advance.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the physical-candidate Tau-grid upstream request packet.")
    parser.add_argument("--write-packet", nargs="?", const=str(DEFAULT_PACKET))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()

    packet = build_packet()
    text = json.dumps(packet, indent=2, sort_keys=True)
    if args.write_packet:
        packet_path = Path(args.write_packet)
        packet_path.parent.mkdir(parents=True, exist_ok=True)
        packet_path.write_text(text + "\n")
    if args.write_doc:
        write_doc(packet, Path(args.write_doc))
    print(text)


if __name__ == "__main__":
    main()
