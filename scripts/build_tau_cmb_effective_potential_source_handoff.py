#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_effective_potential_source_handoff_v01_handoff_only_no_source_derivation_no_score_no_likelihood_no_verdict"

FIELDS = [
    "handoff_row_id",
    "handoff_component",
    "symbol_or_object",
    "handoff_status",
    "evidence_source",
    "handoff_requirement",
    "remaining_blocker",
    "scorecard_effect",
    "source_handoff_completed",
    "hard_failure_triggered",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "handoff_rows_declared",
    "declared_rows",
    "partial_rows",
    "blocked_rows",
    "completed_rows",
    "hard_failures_triggered",
    "source_handoff_completed",
    "scores_computed",
    "cmb_likelihood_available",
    "no_dark_blockers",
    "no_dark_cmb_verdict_allowed",
    "tau_response_claim_allowed",
    "dark_sector_verdict_allowed",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def handoff_rows() -> list[dict[str, str]]:
    rows = [
        {
            "handoff_component": "source_slot_identity",
            "symbol_or_object": "Phi_tau_eff(a,k)",
            "handoff_status": "DECLARED_POTENTIAL_SOURCE_SLOT",
            "evidence_source": "tau_cmb_effective_source_equation_v01",
            "handoff_requirement": "Phi_tau_eff must be a potential-like metric readout, not a fitted residual",
            "remaining_blocker": "derive the source from Tau response data rather than CMB endpoint fitting",
            "scorecard_effect": "keeps common acoustic/lensing source slot explicit",
        },
        {
            "handoff_component": "endpoint_blind_provenance",
            "symbol_or_object": "provenance(Phi_tau_eff)",
            "handoff_status": "BLOCKED_ENDPOINT_BLIND_DERIVATION_MISSING",
            "evidence_source": "tau_cmb_known_limit_decision_update_v01",
            "handoff_requirement": "source construction must be independent of CMB residual fitting and role scores",
            "remaining_blocker": "no provenance rule proves endpoint-blind Phi_tau_eff construction",
            "scorecard_effect": "blocks acoustic and lensing score entry",
        },
        {
            "handoff_component": "normalization_convention",
            "symbol_or_object": "norm(Phi_tau_eff)",
            "handoff_status": "PARTIAL_HANDOFF_CONVENTION_REQUIRED",
            "evidence_source": "tau_cmb_acoustic_reduced_evaluation_v01; tau_cmb_lensing_transfer_reduced_evaluation_v01",
            "handoff_requirement": "normalization must be shared by acoustic and lensing readouts before comparison",
            "remaining_blocker": "concrete normalization is not selected",
            "scorecard_effect": "prevents false cross-role agreement from convention drift",
        },
        {
            "handoff_component": "timing_sign_convention",
            "symbol_or_object": "time/sign(Phi_tau_eff)",
            "handoff_status": "BLOCKED_TIMING_SIGN_NOT_SUPPLIED",
            "evidence_source": "tau_cmb_acoustic_reduced_evaluation_v01",
            "handoff_requirement": "pre-recombination timing and sign must be supplied for acoustic phase/height checks",
            "remaining_blocker": "no source-time dependence or sign convention is derived",
            "scorecard_effect": "blocks acoustic phase and height scoring",
        },
        {
            "handoff_component": "baryon_photon_coupling_role",
            "symbol_or_object": "coupling(Phi_tau_eff, baryon-photon response)",
            "handoff_status": "BLOCKED_COUPLING_ROLE_NOT_SUPPLIED",
            "evidence_source": "tau_cmb_acoustic_reduced_evaluation_v01",
            "handoff_requirement": "source coupling must not erase the baryon-loading odd/even peak role",
            "remaining_blocker": "no coupling role or sign is supplied",
            "scorecard_effect": "prevents acoustic promotion from a potential slot alone",
        },
        {
            "handoff_component": "lensing_projection_handoff",
            "symbol_or_object": "Phi_tau_eff(a,k) -> lensing projection",
            "handoff_status": "BLOCKED_LENSING_RESPONSE_NOT_SUPPLIED",
            "evidence_source": "tau_cmb_lensing_transfer_reduced_evaluation_v01",
            "handoff_requirement": "potential source must connect to lensing amplitude/shape through a declared projection and transfer convention",
            "remaining_blocker": "no lensing-ready response or transfer-linked potential is supplied",
            "scorecard_effect": "blocks lensing score entry",
        },
    ]
    return [
        {
            "handoff_row_id": f"TCMBEPSH01_{index:03d}",
            "source_handoff_completed": "false",
            "hard_failure_triggered": "false",
            "blocks_no_dark_claim": "true",
            "allows_tau_response_claim": "false",
            "allows_dark_sector_verdict": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            **row,
        }
        for index, row in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_EFFECTIVE_POTENTIAL_SOURCE_HANDOFF_V01",
            "handoff_rows_declared": len(rows),
            "declared_rows": sum(row["handoff_status"].startswith("DECLARED") for row in rows),
            "partial_rows": sum(row["handoff_status"].startswith("PARTIAL") for row in rows),
            "blocked_rows": sum(row["handoff_status"].startswith("BLOCKED") for row in rows),
            "completed_rows": sum(row["source_handoff_completed"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "source_handoff_completed": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "EFFECTIVE_POTENTIAL_SOURCE_HANDOFF_DECLARED_BUT_BLOCKED",
            "next_required_artifact": "tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_effective_potential_source_handoff_v01.md").write_text(
        """# Tau CMB Effective Potential Source Handoff v01

**Doc class:** effective-potential source handoff
**Status:** handoff declared but blocked; no source derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_effective_potential_source_handoff.py
```

Derived outputs:

```text
data/derived/tau_cmb_effective_potential_source_handoff_v01.csv
data/derived/tau_cmb_effective_potential_source_handoff_summary_v01.csv
```

This artifact declares the common handoff needed before acoustic and lensing
scoring can share a Tau effective potential source:

```text
Phi_tau_eff(a,k)
```

It does not derive `Phi_tau_eff`. The source slot is declared, but endpoint-blind
provenance, normalization, timing/sign, baryon-photon coupling, and lensing
projection response remain missing.

Therefore the effective-potential source handoff is not completed.

## Claim Boundary

This artifact is a handoff contract only. It derives no physical source,
computes no score, supplies no CMB likelihood, declares no reproduction or
failure, validates no Tau-response source, and permits no no-dark or
dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = handoff_rows()
    write_csv(DERIVED / "tau_cmb_effective_potential_source_handoff_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_effective_potential_source_handoff_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_EFFECTIVE_POTENTIAL_SOURCE_HANDOFF_V01_BUILT")


if __name__ == "__main__":
    main()
