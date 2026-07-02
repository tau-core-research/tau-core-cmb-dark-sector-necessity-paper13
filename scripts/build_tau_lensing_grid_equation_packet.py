#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "data/derived/cmb_tau_lensing_grid_equation_packet_v01.json"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def build_packet() -> dict[str, Any]:
    return {
        "report_id": "cmb_tau_lensing_grid_equation_packet_v01",
        "claim_boundary": "tau_grid_equation_packet_only_no_grid_no_score_no_dark_sector_verdict",
        "purpose": "shortest_equation_level_path_from_tau_source_skeleton_to_materializable_lensing_grid",
        "target_grid_contract": {
            "grid": "tau_PP(L) or delta_PP_tau(L)",
            "index_domain": "L = 10..3009",
            "accepted_file_shape": "3000 rows; explicit two-column L,value table preferred",
            "materializer": "scripts/materialize_tau_lensing_grid_from_formula_spec.py",
        },
        "route_A_transfer_projection": {
            "route_id": "Phi_tau_eff_transfer_projection_to_tau_PP",
            "mathematical_skeleton": [
                "rho_tau_eff(a,k) = A_tau(a,k) * rho_ref(a)",
                "k^2 * Phi_tau_eff(a,k) = 4*pi*G*a^2*rho_tau_eff(a,k)*Delta_tau(a,k)",
                "Phi_lens_tau(a,k) = T_tau_CMB(k,a) * Phi_tau_eff(a,k)",
                "tau_PP(L) = Projection_PP[Phi_lens_tau](L) under a declared CMB lensing convention",
            ],
            "dimension_status": [
                "A_tau must be dimensionless",
                "Delta_tau must be dimensionless",
                "rho_ref must carry density units",
                "Phi_tau_eff is dimensionless in the standard scalar-potential comparison slot",
                "T_tau_CMB must be dimensionless or explicitly normalized",
            ],
            "currently_missing": [
                "endpoint-blind A_tau(a,k) derivation",
                "parent -> Phi_tau_eff(a,k) rule",
                "Phi_tau_eff normalization and sign convention",
                "T_tau_CMB(k,a) propagation rule",
                "Projection_PP convention and normalization",
            ],
            "materializable_now": False,
        },
        "route_B_direct_L_space": {
            "route_id": "direct_endpoint_blind_delta_PP_tau_L",
            "mathematical_skeleton": [
                "delta_PP_tau(L) = F_tau_L(B_tau_base_CMB, delta_M_CMB, OI, scale_profile; L)",
                "F_tau_L must be fixed before ACT/Planck residual score readout",
                "F_tau_L may be implemented by a supported formula family after provenance review",
            ],
            "allowed_adapter_families": [
                "power_law_cutoff_response_v01",
                "tabulated_l_response_v01",
            ],
            "currently_missing": [
                "endpoint-blind parent-side evidence fixing all formula parameters",
                "or an endpoint-blind upstream Tau response table with exact L=10..3009 alignment",
                "known-limit statement for zero, LCDM-like, or failure behavior",
                "normalization statement for PP or delta_PP_tau units",
                "route declaration and provenance with matching grid hash",
            ],
            "materializable_now": False,
        },
        "minimal_next_choice": {
            "preferred_for_physics": "route_A_transfer_projection",
            "preferred_for_fast_endpoint_blind_scoring_probe": "route_B_direct_L_space",
            "caution": (
                "route_B is faster but weaker unless its parameters are fixed by a Tau-side derivation; "
                "otherwise it becomes an arbitrary shape ansatz."
            ),
        },
        "candidate_formula_spec_status": {
            "candidate_spec": "payload_staging/tau_lensing_grid_formula_spec_candidate_v01.json",
            "candidate_audit": "data/derived/cmb_tau_lensing_grid_formula_spec_candidate_audit_v01.json",
            "status": "CANDIDATE_NOT_PAYLOAD",
        },
        "next_required_action": (
            "choose route_A by deriving T_tau_CMB/projection, or choose route_B by supplying "
            "an endpoint-blind direct L-space Tau response with fixed parameters"
        ),
        "score_run": False,
        "dark_sector_verdict": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the Tau lensing grid equation packet.")
    parser.add_argument("--write-packet", nargs="?", const=str(DEFAULT_PACKET))
    args = parser.parse_args()
    packet = build_packet()
    text = json.dumps(packet, indent=2, sort_keys=True)
    if args.write_packet:
        path = Path(args.write_packet)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
