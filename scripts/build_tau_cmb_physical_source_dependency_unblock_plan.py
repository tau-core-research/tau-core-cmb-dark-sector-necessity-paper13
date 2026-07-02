#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FRONTIER_SUMMARY = ROOT / "data/derived/tau_cmb_endpoint_blind_physical_value_source_frontier_recompute_summary_v02.json"
FRONTIER_TABLE = ROOT / "data/derived/tau_cmb_endpoint_blind_physical_value_source_frontier_recompute_v02.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_physical_source_dependency_unblock_plan_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_physical_source_dependency_unblock_plan_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_physical_source_dependency_unblock_plan_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_physical_source_dependency_unblock_plan_v01_"
    "dependency_unblock_plan_only_no_physical_source_acceptance_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "unblock_plan_row_id",
    "unblock_target",
    "target_class",
    "affected_coordinate_components",
    "affected_row_count",
    "minimum_required_artifact",
    "currently_available_evidence",
    "current_status",
    "recommended_action",
    "priority_rank",
    "allows_physical_CMB_score",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

PLAN_ROWS = [
    {
        "unblock_target": "Phi_tau_eff(a,k)",
        "target_class": "shared_potential_source",
        "affected_coordinate_components": "potential_source_presence;lensing_potential_source;phase_support;cross_readout_consistency;radiation_cross_role_consistency",
        "minimum_required_artifact": "endpoint-blind Phi_tau_eff source/derivation with domain, units/convention, provenance, replay, and forbidden-input attestation",
        "currently_available_evidence": "data/derived/tau_cmb_effective_potential_source_handoff_summary_v01.csv",
        "current_status": "handoff declared but blocked; no endpoint-blind source accepted",
        "recommended_action": "build tau_cmb_endpoint_blind_phi_tau_source_or_explicit_fail_supply_v01",
        "priority_rank": 1,
    },
    {
        "unblock_target": "rho_tau_eff(a,k) and A_tau",
        "target_class": "density_source_and_amplitude",
        "affected_coordinate_components": "tau_effective_density;endpoint_blind_amplitude;omega_c_h2_role_comparison;cross_readout_consistency;radiation_cross_role_consistency",
        "minimum_required_artifact": "endpoint-blind density source plus A_tau amplitude/provenance or explicit fail evidence",
        "currently_available_evidence": "data/derived/tau_cmb_density_amplitude_derivation_summary_v01.csv;data/derived/tau_cmb_density_amplitude_closure_summary_v01.csv",
        "current_status": "definition/partial closure only; derivation and benchmark match blocked",
        "recommended_action": "build tau_cmb_density_source_amplitude_or_explicit_fail_supply_v01",
        "priority_rank": 2,
    },
    {
        "unblock_target": "Delta_N_eff_tau",
        "target_class": "radiation_source",
        "affected_coordinate_components": "tau_radiation_like_contribution;damping_tail_inequality;radiation_cross_role_consistency",
        "minimum_required_artifact": "endpoint-blind Delta_N_eff_tau derivation/source or explicit fail evidence under selected convention",
        "currently_available_evidence": "data/derived/tau_cmb_effective_source_equation_summary_v01.csv;data/derived/tau_cmb_readout_role_coordinate_radiation_v01.csv",
        "current_status": "slot declared; source equation target not filled; inequality not evaluated",
        "recommended_action": "build tau_cmb_delta_neff_or_explicit_fail_supply_v01",
        "priority_rank": 3,
    },
    {
        "unblock_target": "acoustic_response_bundle",
        "target_class": "acoustic_response",
        "affected_coordinate_components": "phase_support;relative_peak_height;baryon_loading_coupling",
        "minimum_required_artifact": "endpoint-blind acoustic oscillator response, peak-height response, and baryon-loading sign convention or explicit fail evidence",
        "currently_available_evidence": "data/derived/tau_cmb_acoustic_reduced_evaluation_summary_v01.csv",
        "current_status": "partial acoustic reduced evaluation; score blocked",
        "recommended_action": "build tau_cmb_acoustic_response_bundle_or_explicit_fail_supply_v01 after Phi_tau_eff decision",
        "priority_rank": 4,
    },
    {
        "unblock_target": "growth_transfer_operator",
        "target_class": "growth_operator",
        "affected_coordinate_components": "operator_rule;growth_cross_role_consistency",
        "minimum_required_artifact": "endpoint-blind growth transfer operator or explicit fail evidence",
        "currently_available_evidence": "data/derived/tau_cmb_growth_transfer_kernel_summary_v01.csv;data/derived/tau_cmb_growth_transfer_kernel_closure_summary_v01.csv",
        "current_status": "kernel declared/partial closure; operator not specified",
        "recommended_action": "build tau_cmb_growth_transfer_operator_or_explicit_fail_supply_v01",
        "priority_rank": 5,
    },
    {
        "unblock_target": "cross_role_consistency_bundle",
        "target_class": "dependent_consistency",
        "affected_coordinate_components": "cross_readout_consistency;growth_cross_role_consistency;radiation_cross_role_consistency",
        "minimum_required_artifact": "accepted or explicitly failed source/operator rows for dependent density, acoustic, lensing, growth, and radiation roles",
        "currently_available_evidence": "data/derived/tau_cmb_endpoint_blind_physical_value_source_frontier_recompute_summary_v02.json",
        "current_status": "blocked until upstream physical source/operator rows are accepted or explicitly failed",
        "recommended_action": "recompute only after priority 1-5 rows are resolved",
        "priority_rank": 6,
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def input_chain_clean() -> bool:
    if not FRONTIER_SUMMARY.exists() or not FRONTIER_TABLE.exists():
        return False
    summary = load_json(FRONTIER_SUMMARY)
    return (
        summary.get("status") == "CMB_ENDPOINT_BLIND_PHYSICAL_VALUE_SOURCE_FRONTIER_RECOMPUTED_TWO_EXPLICIT_FAILS_ACCEPTED"
        and summary.get("next_minimal_unblock") == "tau_cmb_physical_source_dependency_unblock_plan_v01"
        and summary.get("explicit_fail_accepted_rows") == 2
        and summary.get("open_frontier_rows") == 14
        and summary.get("physical_value_source_accepted_rows") == 0
        and summary.get("physical_CMB_score_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("frontier recompute v02 summary is not clean")
    out: list[dict[str, str]] = []
    for index, row in enumerate(PLAN_ROWS, start=1):
        affected = row["affected_coordinate_components"].split(";")
        out.append(
            {
                "unblock_plan_row_id": f"TCMBPSDU01_{index:03d}",
                "unblock_target": row["unblock_target"],
                "target_class": row["target_class"],
                "affected_coordinate_components": row["affected_coordinate_components"],
                "affected_row_count": str(len(affected)),
                "minimum_required_artifact": row["minimum_required_artifact"],
                "currently_available_evidence": row["currently_available_evidence"],
                "current_status": row["current_status"],
                "recommended_action": row["recommended_action"],
                "priority_rank": str(row["priority_rank"]),
                "allows_physical_CMB_score": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
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
    top = min(rows, key=lambda row: int(row["priority_rank"]))
    return {
        "report_id": "tau_cmb_physical_source_dependency_unblock_plan_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_frontier_recompute_summary_v02": rel(FRONTIER_SUMMARY),
        "input_frontier_recompute_table_v02": rel(FRONTIER_TABLE),
        "input_chain_clean": input_chain_clean(),
        "unblock_plan_rows": len(rows),
        "top_priority_target": top["unblock_target"],
        "top_priority_recommended_action": top["recommended_action"],
        "open_frontier_rows": 14,
        "explicit_fail_accepted_rows": 2,
        "physical_value_source_accepted_rows": 0,
        "physical_CMB_score_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_PHYSICAL_SOURCE_DEPENDENCY_UNBLOCK_PLAN_ACCEPTED_PRIORITIZED_NO_SCORE"
            if input_chain_clean() and len(rows) == 6
            else "CMB_PHYSICAL_SOURCE_DEPENDENCY_UNBLOCK_PLAN_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": top["recommended_action"],
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Physical Source Dependency Unblock Plan v01

**Doc class:** dependency unblock plan
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Summary

```text
unblock_plan_rows={summary["unblock_plan_rows"]}
top_priority_target={summary["top_priority_target"]}
top_priority_recommended_action={summary["top_priority_recommended_action"]}
open_frontier_rows={summary["open_frontier_rows"]}
explicit_fail_accepted_rows={summary["explicit_fail_accepted_rows"]}
physical_value_source_accepted_rows={summary["physical_value_source_accepted_rows"]}
physical_CMB_score_allowed={summary["physical_CMB_score_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

The plan ranks dependency blockers by how many frontier rows they can unblock.
It does not accept physical sources or run a score.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB physical source dependency unblock plan.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    table_rows = rows()
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
