#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_scorecard_readiness_audit_v01_audit_only_no_scores_no_likelihood_no_verdict"

FIELDS = [
    "readiness_row_id",
    "cmb_role",
    "scorecard_row_id",
    "input_artifact_checked",
    "input_status",
    "score_readiness_status",
    "minimum_missing_input",
    "can_compute_score",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "readiness_rows_declared",
    "input_artifacts_checked",
    "score_ready_rows",
    "score_blocked_rows",
    "direct_no_dark_blockers",
    "scores_computed",
    "cmb_likelihood_available",
    "no_dark_cmb_verdict_allowed",
    "tau_response_claim_allowed",
    "dark_sector_verdict_allowed",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

READINESS = {
    "acoustic_peak_phase_and_height": (
        "tau_cmb_acoustic_role_reduced_benchmark_v01",
        "DECLARED_NOT_EVALUATED",
        "NOT_READY_BENCHMARK_NOT_EVALUATED",
        "evaluate reduced acoustic phase/height benchmark",
    ),
    "omega_c_h2_density_inference": (
        "tau_cmb_density_amplitude_derivation_v01",
        "DEFINITION_DECLARED_DERIVATION_BLOCKED",
        "NOT_READY_ENDPOINT_BLIND_DERIVATION_MISSING",
        "derive endpoint-blind A_tau(a,k) and compare the density role",
    ),
    "cmb_lensing_potential": (
        "tau_cmb_lensing_transfer_benchmark_v01",
        "DECLARED_NOT_EVALUATED",
        "NOT_READY_LENSING_TRANSFER_NOT_EVALUATED",
        "evaluate reduced lensing transfer benchmark",
    ),
    "damping_tail_and_radiation_guard": (
        "tau_cmb_radiation_guard_bound_check_v01",
        "DECLARED_NOT_EVALUATED",
        "NOT_READY_RADIATION_BOUND_NOT_EVALUATED",
        "evaluate Delta_N_eff_tau bound check under a declared convention",
    ),
    "growth_seed_and_transfer_consistency": (
        "tau_cmb_growth_transfer_kernel_v01",
        "DECLARED_NOT_SPECIFIED",
        "NOT_READY_TRANSFER_KERNEL_NOT_SPECIFIED",
        "supply or explicitly fail the Tau growth-transfer operator rule",
    ),
    "known_limit_or_explicit_failure": (
        "tau_cmb_known_limit_failure_map_v01",
        "UNRESOLVED_INPUT_MISSING",
        "NOT_READY_KNOWN_LIMIT_ROWS_UNRESOLVED",
        "assign reproduce/approximate/fail states after evidence rows are evaluated",
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


def readiness_rows() -> list[dict[str, str]]:
    scorecard_rows = read_csv(DERIVED / "tau_cmb_role_scorecard_template_v01.csv")
    rows: list[dict[str, str]] = []
    for index, row in enumerate(scorecard_rows, start=1):
        artifact, input_status, readiness_status, missing = READINESS[row["cmb_role"]]
        rows.append(
            {
                "readiness_row_id": f"TCMBSRA01_{index:03d}",
                "cmb_role": row["cmb_role"],
                "scorecard_row_id": row["scorecard_row_id"],
                "input_artifact_checked": artifact,
                "input_status": input_status,
                "score_readiness_status": readiness_status,
                "minimum_missing_input": missing,
                "can_compute_score": "false",
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
            "summary_id": "TAU_CMB_SCORECARD_READINESS_AUDIT_V01",
            "readiness_rows_declared": len(rows),
            "input_artifacts_checked": len({row["input_artifact_checked"] for row in rows}),
            "score_ready_rows": sum(row["can_compute_score"] == "true" for row in rows),
            "score_blocked_rows": sum(row["can_compute_score"] == "false" for row in rows),
            "direct_no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "SCORECARD_NOT_READY_ALL_ROWS_BLOCKED",
            "next_required_artifact": "tau_cmb_scorecard_blocker_closure_plan_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_scorecard_readiness_audit_v01.md").write_text(
        """# Tau CMB Scorecard Readiness Audit v01

**Doc class:** scorecard readiness audit
**Status:** all scorecard rows blocked; no scores, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_scorecard_readiness_audit.py
```

Derived outputs:

```text
data/derived/tau_cmb_scorecard_readiness_audit_v01.csv
data/derived/tau_cmb_scorecard_readiness_audit_summary_v01.csv
```

This artifact audits whether the six CMB scorecard rows are ready to compute.
The answer in v01 is no:

```text
score_ready_rows = 0
score_blocked_rows = 6
```

The audit checks the density, acoustic, lensing, growth, radiation, and
known-limit inputs. Each exists as a scaffold, benchmark, guard, or map, but
none has been evaluated or specified enough to compute a score.

## Claim Boundary

This artifact is a readiness audit only. It computes no scores, supplies no CMB
likelihood, validates no Tau-response source, and permits no no-dark or
dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = readiness_rows()
    write_csv(DERIVED / "tau_cmb_scorecard_readiness_audit_v01.csv", rows, FIELDS)
    write_csv(DERIVED / "tau_cmb_scorecard_readiness_audit_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_SCORECARD_READINESS_AUDIT_V01_BUILT")


if __name__ == "__main__":
    main()
