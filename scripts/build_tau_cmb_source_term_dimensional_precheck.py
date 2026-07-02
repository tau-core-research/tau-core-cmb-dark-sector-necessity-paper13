#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_source_term_dimensional_precheck_v01_conditional_only_no_likelihood_no_verdict"

FIELDS = [
    "precheck_row_id",
    "candidate_row_id",
    "source_term_component",
    "candidate_symbol",
    "candidate_expression_skeleton",
    "precheck_result",
    "required_condition",
    "unresolved_dependency",
    "blocks_scoring",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "prechecked_components",
    "conditional_dimension_passes",
    "blocked_dimension_rows",
    "full_dimensional_proofs",
    "scoring_blockers",
    "no_dark_blockers",
    "no_dark_cmb_verdict_allowed",
    "tau_response_claim_allowed",
    "dark_sector_verdict_allowed",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

PRECHECKS = {
    "carrier_to_response_state": (
        "BLOCKED_OPERATOR_DOMAIN_CODOMAIN_UNFILLED",
        "declare response-state codomain and carrier units",
        "Response_tau_CMB not defined",
        "true",
    ),
    "effective_density_source": (
        "CONDITIONAL_PASS_IF_A_TAU_DIMENSIONLESS",
        "A_tau(a,k) dimensionless and rho_cdm_ref density-normalized",
        "A_tau derivation not supplied",
        "false",
    ),
    "effective_potential_poisson_slot": (
        "CONDITIONAL_PASS_IF_STANDARD_POISSON_CONVENTION_DECLARED",
        "Fourier k, scale factor a, potential normalization, and Delta_tau convention declared",
        "metric handoff convention not supplied",
        "false",
    ),
    "transfer_kernel_slot": (
        "BLOCKED_TRANSFER_RULE_UNFILLED",
        "declare transfer kernel normalization and propagation law",
        "Transfer_tau not defined",
        "true",
    ),
    "radiation_guard_slot": (
        "CONDITIONAL_PASS_DIMENSIONLESS_GUARD",
        "Delta_N_eff_tau and Delta_N_eff_bound dimensionless under same convention",
        "external bound and Tau radiation-like contribution not evaluated",
        "false",
    ),
    "known_limit_branch": (
        "BLOCKED_LIMIT_MAP_UNFILLED",
        "declare map from Tau variables to standard comparison variables",
        "LCDM role limit/failure map not supplied",
        "true",
    ),
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


def precheck_rows() -> list[dict[str, str]]:
    candidate_rows = read_csv(DERIVED / "tau_cmb_minimal_source_term_candidate_v01.csv")
    rows: list[dict[str, str]] = []
    for index, row in enumerate(candidate_rows, start=1):
        result, condition, unresolved, blocks_scoring = PRECHECKS[row["source_term_component"]]
        rows.append(
            {
                "precheck_row_id": f"TCMBSTDP01_{index:03d}",
                "candidate_row_id": row["candidate_row_id"],
                "source_term_component": row["source_term_component"],
                "candidate_symbol": row["candidate_symbol"],
                "candidate_expression_skeleton": row["candidate_expression_skeleton"],
                "precheck_result": result,
                "required_condition": condition,
                "unresolved_dependency": unresolved,
                "blocks_scoring": blocks_scoring,
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
            "summary_id": "TAU_CMB_SOURCE_TERM_DIMENSIONAL_PRECHECK_V01",
            "prechecked_components": len(rows),
            "conditional_dimension_passes": sum(row["precheck_result"].startswith("CONDITIONAL_PASS") for row in rows),
            "blocked_dimension_rows": sum(row["precheck_result"].startswith("BLOCKED") for row in rows),
            "full_dimensional_proofs": 0,
            "scoring_blockers": sum(row["blocks_scoring"] == "true" for row in rows),
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "SOURCE_TERM_DIMENSIONAL_PRECHECK_PARTIAL_CONDITIONAL_SCORING_BLOCKED",
            "next_required_artifact": "tau_cmb_lcdm_role_scoring_rubric_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_source_term_dimensional_precheck_v01.md").write_text(
        """# Tau CMB Source-Term Dimensional Precheck v01

**Doc class:** dimensional precheck
**Status:** partial conditional precheck; no full dimensional proof, no scoring verdict

Script:

```text
scripts/build_tau_cmb_source_term_dimensional_precheck.py
```

Derived outputs:

```text
data/derived/tau_cmb_source_term_dimensional_precheck_v01.csv
data/derived/tau_cmb_source_term_dimensional_precheck_summary_v01.csv
```

This artifact checks the minimal source-term candidate only at the level of
dimensional preconditions. Three rows are conditionally precheckable:

```text
rho_tau_eff(a,k) = A_tau(a,k) rho_cdm_ref(a)
k^2 Phi_tau_eff(a,k) = 4 pi G a^2 rho_tau_eff(a,k) Delta_tau(a,k)
Delta_N_eff_tau <= Delta_N_eff_bound
```

The other three rows remain blocked because the response operator, transfer
kernel, and known-limit map are not yet supplied. Therefore the artifact moves
Paper 13 closer to scoring, but still blocks a CMB no-dark claim and any
dark-sector verdict.

## Claim Boundary

This is a conditional dimensional precheck only. It proves no full dimensional
consistency theorem, matches no CMB likelihood, supplies no Boltzmann solver,
and permits no Tau-response or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = precheck_rows()
    write_csv(DERIVED / "tau_cmb_source_term_dimensional_precheck_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_source_term_dimensional_precheck_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_SOURCE_TERM_DIMENSIONAL_PRECHECK_V01_BUILT")


if __name__ == "__main__":
    main()
