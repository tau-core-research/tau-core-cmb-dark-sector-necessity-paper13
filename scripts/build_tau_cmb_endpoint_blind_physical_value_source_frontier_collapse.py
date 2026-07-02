#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKET_ACCEPTANCE_SUMMARY = ROOT / "data/derived/tau_cmb_endpoint_blind_physical_value_source_packet_acceptance_audit_summary_v01.json"
PACKET_TABLE = ROOT / "data/derived/tau_cmb_endpoint_blind_physical_value_source_packet_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_endpoint_blind_physical_value_source_frontier_collapse_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_endpoint_blind_physical_value_source_frontier_collapse_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_endpoint_blind_physical_value_source_frontier_collapse_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_endpoint_blind_physical_value_source_frontier_collapse_v01_"
    "triage_only_no_physical_source_acceptance_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "frontier_collapse_row_id",
    "source_physical_value_source_packet_row_id",
    "role_name",
    "coordinate_symbol",
    "coordinate_component",
    "formal_slot",
    "frontier_class",
    "collapse_bucket",
    "candidate_evidence_artifact",
    "candidate_evidence_status",
    "collapse_decision",
    "recommended_next_action",
    "physical_value_source_supplied",
    "physical_value_source_accepted",
    "allows_physical_CMB_score",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

EVIDENCE_MAP = {
    "potential_source_presence": (
        "dependency_blocked",
        "data/derived/tau_cmb_effective_potential_source_handoff_summary_v01.csv",
        "EFFECTIVE_POTENTIAL_SOURCE_HANDOFF_DECLARED_BUT_BLOCKED",
        "No endpoint-blind Phi_tau_eff source is accepted.",
        "derive or supply endpoint-blind Phi_tau_eff(a,k) or explicit fail evidence",
    ),
    "phase_support": (
        "dependency_blocked",
        "data/derived/tau_cmb_acoustic_reduced_evaluation_summary_v01.csv",
        "ACOUSTIC_REDUCED_EVALUATION_PARTIAL_SCORE_BLOCKED",
        "Acoustic reduced evaluation is partial and score-blocked.",
        "supply endpoint-blind acoustic oscillator response after source potential is available",
    ),
    "relative_peak_height": (
        "dependency_blocked",
        "data/derived/tau_cmb_acoustic_reduced_evaluation_summary_v01.csv",
        "ACOUSTIC_REDUCED_EVALUATION_PARTIAL_SCORE_BLOCKED",
        "Acoustic amplitude/height response is not available.",
        "supply endpoint-blind acoustic amplitude/height response or explicit fail evidence",
    ),
    "baryon_loading_coupling": (
        "dependency_blocked",
        "data/derived/tau_cmb_acoustic_reduced_evaluation_summary_v01.csv",
        "ACOUSTIC_REDUCED_EVALUATION_PARTIAL_SCORE_BLOCKED",
        "Baryon-loading coupling sign convention is not selected.",
        "supply endpoint-blind coupling sign convention or explicit fail evidence",
    ),
    "tau_effective_density": (
        "dependency_blocked",
        "data/derived/tau_cmb_density_amplitude_derivation_summary_v01.csv",
        "DENSITY_AMPLITUDE_DEFINITION_DECLARED_DERIVATION_AND_MATCH_BLOCKED",
        "rho_tau_eff is not derived as an endpoint-blind physical source.",
        "derive or supply endpoint-blind rho_tau_eff(a,k) or explicit fail evidence",
    ),
    "endpoint_blind_amplitude": (
        "dependency_blocked",
        "data/derived/tau_cmb_density_amplitude_closure_summary_v01.csv",
        "DENSITY_AMPLITUDE_PARTIAL_CLOSURE_SCORE_BLOCKED",
        "A_tau closure is partial and cannot be accepted as a physical amplitude.",
        "supply endpoint-blind A_tau value with provenance or explicit fail evidence",
    ),
    "omega_c_h2_role_comparison": (
        "dependency_blocked",
        "data/derived/tau_cmb_density_amplitude_derivation_summary_v01.csv",
        "DENSITY_AMPLITUDE_DEFINITION_DECLARED_DERIVATION_AND_MATCH_BLOCKED",
        "No numeric A_tau prediction or benchmark comparison is accepted.",
        "preselect benchmark convention and supply comparison value or explicit fail evidence",
    ),
    "lensing_potential_source": (
        "dependency_blocked",
        "data/derived/tau_cmb_effective_potential_source_handoff_summary_v01.csv",
        "EFFECTIVE_POTENTIAL_SOURCE_HANDOFF_DECLARED_BUT_BLOCKED",
        "No endpoint-blind lensing-era Phi_tau_eff source is accepted.",
        "derive or supply endpoint-blind lensing potential source or explicit fail evidence",
    ),
    "transfer_kernel": (
        "explicit_fail_candidate_available_not_accepted",
        "data/derived/cmb_tau_lensing_physical_projection_operator_packet_audit_v01.json",
        "DO_NOT_SCORE_EXPLICIT_OPERATOR_FAILURE",
        "A related lensing projection-operator explicit-failure audit exists, but it is not automatically the T_tau_CMB kernel.",
        "bridge-audit whether explicit projection-operator failure can lawfully satisfy this transfer-kernel row",
    ),
    "amplitude_shape_response": (
        "bridge_candidate_available_not_accepted",
        "data/derived/cmb_tau_lensing_scoring_status_summary_v01.json",
        "PHYSICAL_TAU_SCORE_ACCEPTED",
        "A related reduced lensing score artifact exists, but it is not accepted as this CMB value-source row without a bridge audit.",
        "bridge-audit the lensing reduced score against S_lens_tau(L) or provide explicit fail evidence",
    ),
    "cross_readout_consistency": (
        "dependency_blocked",
        "data/derived/tau_cmb_readout_role_coordinate_numeric_value_protocol_saturation_audit_summary_v01.json",
        "PHYSICAL_DEPENDENCIES_OPEN",
        "Cross-readout consistency depends on accepted density/acoustic/lensing rows.",
        "revisit after dependent physical source rows are accepted or explicitly failed",
    ),
    "operator_rule": (
        "dependency_blocked",
        "data/derived/tau_cmb_growth_transfer_kernel_closure_summary_v01.csv",
        "GROWTH_TRANSFER_KERNEL_PARTIAL_CLOSURE_SCORE_BLOCKED",
        "Growth transfer operator is not specified as an accepted operator.",
        "supply endpoint-blind growth transfer operator or explicit fail evidence",
    ),
    "cross_role_consistency": (
        "dependency_blocked",
        "data/derived/tau_cmb_readout_role_coordinate_numeric_value_protocol_saturation_audit_summary_v01.json",
        "PHYSICAL_DEPENDENCIES_OPEN",
        "Cross-role consistency depends on accepted physical source/operator rows.",
        "revisit after dependent physical source rows are accepted or explicitly failed",
    ),
    "tau_radiation_like_contribution": (
        "dependency_blocked",
        "data/derived/tau_cmb_effective_source_equation_summary_v01.csv",
        "EFFECTIVE_SOURCE_EQUATION_TARGET_DECLARED_NOT_FILLED",
        "Delta_N_eff_tau is not derived from a Tau response.",
        "derive or supply endpoint-blind Delta_N_eff_tau or explicit fail evidence",
    ),
    "damping_tail_inequality": (
        "dependency_blocked",
        "data/derived/tau_cmb_readout_role_coordinate_radiation_v01.csv",
        "BLOCKED_BOUND_INEQUALITY_NOT_EVALUATED",
        "The inequality cannot be evaluated until both Delta_N_eff_tau and a bound are numeric under one convention.",
        "evaluate after Delta_N_eff_tau and bound are supplied, or explicit fail evidence is accepted",
    ),
}


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def input_chain_clean() -> bool:
    if not PACKET_ACCEPTANCE_SUMMARY.exists() or not PACKET_TABLE.exists():
        return False
    summary = load_json(PACKET_ACCEPTANCE_SUMMARY)
    return (
        summary.get("status") == "CMB_ENDPOINT_BLIND_PHYSICAL_VALUE_SOURCE_PACKET_CONTRACTS_ACCEPTED_SOURCES_ABSENT"
        and summary.get("next_minimal_unblock") == "tau_cmb_endpoint_blind_physical_value_source_supply_v01"
        and summary.get("physical_value_source_packet_acceptance_rows") == 16
        and summary.get("packet_contract_accepted_rows") == 16
        and summary.get("physical_value_source_supplied_rows") == 0
        and summary.get("physical_value_source_accepted_rows") == 0
        and summary.get("physical_CMB_score_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def rows() -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("physical value-source packet acceptance summary is not clean")
    out: list[dict[str, str]] = []
    for index, source in enumerate(read_csv(PACKET_TABLE), start=1):
        bucket, artifact, status, decision, next_action = EVIDENCE_MAP[source["coordinate_component"]]
        out.append(
            {
                "frontier_collapse_row_id": f"TCMBEBPVSFC01_{index:03d}",
                "source_physical_value_source_packet_row_id": source["physical_value_source_packet_row_id"],
                "role_name": source["role_name"],
                "coordinate_symbol": source["coordinate_symbol"],
                "coordinate_component": source["coordinate_component"],
                "formal_slot": source["formal_slot"],
                "frontier_class": source["frontier_class"],
                "collapse_bucket": bucket,
                "candidate_evidence_artifact": artifact,
                "candidate_evidence_status": status,
                "collapse_decision": decision,
                "recommended_next_action": next_action,
                "physical_value_source_supplied": "false",
                "physical_value_source_accepted": "false",
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
    buckets: dict[str, int] = {}
    for row in rows:
        buckets[row["collapse_bucket"]] = buckets.get(row["collapse_bucket"], 0) + 1
    return {
        "report_id": "tau_cmb_endpoint_blind_physical_value_source_frontier_collapse_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_packet_acceptance_summary": rel(PACKET_ACCEPTANCE_SUMMARY),
        "input_packet_table": rel(PACKET_TABLE),
        "input_chain_clean": input_chain_clean(),
        "frontier_rows": len(rows),
        "collapse_bucket_counts": buckets,
        "physical_value_source_supplied_rows": 0,
        "physical_value_source_accepted_rows": 0,
        "physical_CMB_score_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_ENDPOINT_BLIND_PHYSICAL_VALUE_SOURCE_FRONTIER_COLLAPSED_TO_TRIAGE_NO_SOURCES_ACCEPTED"
            if input_chain_clean() and len(rows) == 16
            else "CMB_ENDPOINT_BLIND_PHYSICAL_VALUE_SOURCE_FRONTIER_COLLAPSE_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_endpoint_blind_physical_value_source_bridge_audit_or_explicit_fail_supply_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Endpoint-Blind Physical Value Source Frontier Collapse v01

**Doc class:** physical value-source frontier triage
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Summary

```text
frontier_rows={summary["frontier_rows"]}
collapse_bucket_counts={summary["collapse_bucket_counts"]}
physical_value_source_supplied_rows={summary["physical_value_source_supplied_rows"]}
physical_value_source_accepted_rows={summary["physical_value_source_accepted_rows"]}
physical_CMB_score_allowed={summary["physical_CMB_score_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

This pass does not accept physical value sources. It collapses the 16 frontier
rows into dependency-blocked rows, bridge-candidate rows, and explicit-fail
candidate rows.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Collapse Tau CMB endpoint-blind physical value-source frontier to triage buckets.")
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
