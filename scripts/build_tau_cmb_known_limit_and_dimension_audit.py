#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_known_limit_and_dimension_audit_v01_no_formula_no_likelihood_no_verdict"

FIELDS = [
    "audit_row_id",
    "equation_row_id",
    "target_component",
    "symbolic_role",
    "dimension_slot_status",
    "formula_available",
    "dimensional_consistency_proved",
    "lcdm_role_check_status",
    "minimum_failure_mode_required",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "audited_components",
    "dimension_slots_declared",
    "formula_available_components",
    "dimensional_consistency_proved_components",
    "lcdm_roles_matched",
    "lcdm_roles_unmatched",
    "no_dark_blockers",
    "no_dark_cmb_verdict_allowed",
    "tau_response_claim_allowed",
    "dark_sector_verdict_allowed",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

DIMENSION_SLOT_STATUS = {
    "base_carrier": "CARRIER_SLOT_DECLARED_NO_PHYSICAL_UNITS_ASSIGNED",
    "disturbance_seed": "SOURCE_SLOT_DECLARED_PARENT_SIDE_UNITS_UNFILLED",
    "response_operator": "OPERATOR_SLOT_DECLARED_DOMAIN_CODOMAIN_UNFILLED",
    "effective_density": "DENSITY_SLOT_DECLARED_FORMULA_UNFILLED",
    "effective_potential": "DIMENSIONLESS_POTENTIAL_SLOT_DECLARED_FORMULA_UNFILLED",
    "transfer_response": "DIMENSIONLESS_TRANSFER_SLOT_DECLARED_FORMULA_UNFILLED",
    "radiation_guard": "DIMENSIONLESS_RADIATION_GUARD_SLOT_DECLARED_FORMULA_UNFILLED",
    "known_limit_gate": "COMPARISON_SLOT_DECLARED_NOT_A_PHYSICAL_VARIABLE",
}

LCDM_ROLE_STATUS = {
    "base_carrier": "LCDM_ROLE_TARGET_DECLARED_NOT_MATCHED",
    "disturbance_seed": "SOURCE_INDEPENDENCE_TARGET_DECLARED_NOT_PROVED",
    "response_operator": "CDM_SOURCE_REPLACEMENT_TARGET_DECLARED_NOT_MATCHED",
    "effective_density": "OMEGA_C_H2_ROLE_DECLARED_NOT_MATCHED",
    "effective_potential": "ACOUSTIC_LENSING_POTENTIAL_ROLE_DECLARED_NOT_MATCHED",
    "transfer_response": "GROWTH_LENSING_TRANSFER_ROLE_DECLARED_NOT_MATCHED",
    "radiation_guard": "NEFF_DAMPING_GUARD_DECLARED_NOT_EVALUATED",
    "known_limit_gate": "KNOWN_LIMIT_COMPARISON_DECLARED_NOT_RUN",
}

FAILURE_MODE = {
    "base_carrier": "state whether no admissible CMB-era carrier exists",
    "disturbance_seed": "state whether no endpoint-blind CMB disturbance source exists",
    "response_operator": "state whether no lawful Tau CMB response operator exists",
    "effective_density": "state whether no density-like source mapping exists",
    "effective_potential": "state whether no metric-potential handoff exists",
    "transfer_response": "state whether no transfer response can match growth/lensing roles",
    "radiation_guard": "state whether Tau response violates or avoids radiation-content bounds",
    "known_limit_gate": "state reproduce/approximate/fail for each LCDM role",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def audit_rows() -> list[dict[str, str]]:
    source_rows = read_csv(DERIVED / "tau_cmb_effective_source_equation_v01.csv")
    rows: list[dict[str, str]] = []
    for index, row in enumerate(source_rows, start=1):
        component = row["target_component"]
        rows.append(
            {
                "audit_row_id": f"TCMBKLD01_{index:03d}",
                "equation_row_id": row["equation_row_id"],
                "target_component": component,
                "symbolic_role": row["symbolic_role"],
                "dimension_slot_status": DIMENSION_SLOT_STATUS[component],
                "formula_available": "false",
                "dimensional_consistency_proved": "false",
                "lcdm_role_check_status": LCDM_ROLE_STATUS[component],
                "minimum_failure_mode_required": FAILURE_MODE[component],
                "blocks_no_dark_claim": row["blocks_no_dark_claim"],
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_KNOWN_LIMIT_AND_DIMENSION_AUDIT_V01",
            "audited_components": len(rows),
            "dimension_slots_declared": sum(row["dimension_slot_status"] != "" for row in rows),
            "formula_available_components": sum(row["formula_available"] == "true" for row in rows),
            "dimensional_consistency_proved_components": sum(
                row["dimensional_consistency_proved"] == "true" for row in rows
            ),
            "lcdm_roles_matched": sum(
                row["lcdm_role_check_status"].endswith("_MATCHED")
                and not row["lcdm_role_check_status"].endswith("_NOT_MATCHED")
                for row in rows
            ),
            "lcdm_roles_unmatched": len(rows),
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "KNOWN_LIMIT_DIMENSION_SLOTS_DECLARED_FORMULA_AND_LCDM_MATCH_BLOCKED",
            "next_required_artifact": "tau_cmb_minimal_source_term_candidate_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_known_limit_and_dimension_audit_v01.md").write_text(
        """# Tau CMB Known-Limit And Dimension Audit v01

**Doc class:** known-limit and dimensional role audit
**Status:** slots declared; no formula-level dimensional proof and no LCDM role match

Script:

```text
scripts/build_tau_cmb_known_limit_and_dimension_audit.py
```

Derived outputs:

```text
data/derived/tau_cmb_known_limit_and_dimension_audit_v01.csv
data/derived/tau_cmb_known_limit_and_dimension_audit_summary_v01.csv
```

This audit checks the effective-source target from v01 at the level currently
available. The result is intentionally conservative: dimensional slots and
LCDM role obligations are named, but no component has an available formula, no
component has a proved dimensional consistency result, and no LCDM role is
matched.

The next useful step is therefore a minimal source-term candidate. That
candidate must either supply a checkable formula or record an explicit failure
mode for each CMB role.

## Claim Boundary

This artifact is an audit of target slots only. It provides no CMB source
equation, no dimensional proof, no Boltzmann solver, no CMB likelihood, no
Tau-response claim, and no dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = audit_rows()
    write_csv(DERIVED / "tau_cmb_known_limit_and_dimension_audit_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_known_limit_and_dimension_audit_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_KNOWN_LIMIT_AND_DIMENSION_AUDIT_V01_BUILT")


if __name__ == "__main__":
    main()
