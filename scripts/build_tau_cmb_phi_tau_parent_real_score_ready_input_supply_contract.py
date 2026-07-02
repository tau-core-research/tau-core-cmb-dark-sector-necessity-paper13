#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

PREFIX = "tau_cmb_phi_tau_parent_real_score_ready_input_supply_contract_v01"
SOURCE_PREFIX = "tau_cmb_phi_tau_parent_acceptance_evidence_route_completion_certificate_v01"

CLAIM_BOUNDARY = (
    f"{PREFIX}_unlock_contract_only_real_score_ready_input_required_"
    "no_input_supplied_no_scoring_input_accepted_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "contract_row_id",
    "certificate_row_id",
    "lock_row_id",
    "package_row_id",
    "evidence_object",
    "target_gate",
    "source_route_completion_certificate",
    "contract_status",
    "terminal_state",
    "route_completed",
    "null_response_locked",
    "required_score_ready_input",
    "requires_phi_tau_eff_source",
    "requires_dimension_replay",
    "requires_normalization_binding",
    "requires_endpoint_blind_provenance",
    "requires_cmb_readout_mapping",
    "requires_likelihood_adapter",
    "requires_acceptance_replay",
    "required_materials_count",
    "supplied_materials_count",
    "real_score_ready_input_supplied",
    "scoring_input_accepted",
    "reopen_scoring_route_allowed_now",
    "score_attempt_allowed_now",
    "score_attempt_blocked_now",
    "phi_tau_eff_derived",
    "scores_computed",
    "cmb_likelihood_available",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "real_score_ready_input_supply_contract_rows_declared",
    "route_completed_rows",
    "null_response_locked_rows",
    "required_materials_total",
    "supplied_materials_total",
    "real_score_ready_input_supplied_rows",
    "scoring_input_accepted_rows",
    "reopen_scoring_route_allowed_now_rows",
    "score_attempt_allowed_now_rows",
    "score_attempt_blocked_now_rows",
    "phi_tau_eff_derived_rows",
    "scores_computed_rows",
    "cmb_likelihood_available_rows",
    "real_score_ready_input_supply_contract_satisfied",
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


REQUIRED_MATERIALS = [
    "phi_tau_eff_source",
    "dimension_replay",
    "normalization_binding",
    "endpoint_blind_provenance",
    "cmb_readout_mapping",
    "likelihood_adapter",
    "acceptance_replay",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def contract_rows(certificate_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for index, certificate in enumerate(certificate_rows, start=1):
        route_locked = (
            certificate["route_completed"] == "true"
            and certificate["terminal_state"] == "null_response_locked"
            and certificate["null_response_locked"] == "true"
        )
        rows.append(
            {
                "contract_row_id": f"TCMBPTARSIC01_{index:03d}",
                "certificate_row_id": certificate["certificate_row_id"],
                "lock_row_id": certificate["lock_row_id"],
                "package_row_id": certificate["package_row_id"],
                "evidence_object": certificate["evidence_object"],
                "target_gate": certificate["target_gate"],
                "source_route_completion_certificate": SOURCE_PREFIX,
                "contract_status": (
                    "REAL_SCORE_READY_INPUT_REQUIRED_TO_UNLOCK_NULL_RESPONSE"
                    if route_locked
                    else "REAL_SCORE_READY_INPUT_CONTRACT_BLOCKED"
                ),
                "terminal_state": certificate["terminal_state"],
                "route_completed": str(route_locked).lower(),
                "null_response_locked": str(route_locked).lower(),
                "required_score_ready_input": "|".join(REQUIRED_MATERIALS),
                "requires_phi_tau_eff_source": "true",
                "requires_dimension_replay": "true",
                "requires_normalization_binding": "true",
                "requires_endpoint_blind_provenance": "true",
                "requires_cmb_readout_mapping": "true",
                "requires_likelihood_adapter": "true",
                "requires_acceptance_replay": "true",
                "required_materials_count": str(len(REQUIRED_MATERIALS)),
                "supplied_materials_count": "0",
                "real_score_ready_input_supplied": "false",
                "scoring_input_accepted": "false",
                "reopen_scoring_route_allowed_now": "false",
                "score_attempt_allowed_now": "false",
                "score_attempt_blocked_now": "true",
                "phi_tau_eff_derived": "false",
                "scores_computed": "false",
                "cmb_likelihood_available": "false",
                "blocks_no_dark_claim": "true",
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_REAL_SCORE_READY_INPUT_SUPPLY_CONTRACT_V01",
            "real_score_ready_input_supply_contract_rows_declared": len(rows),
            "route_completed_rows": sum(row["route_completed"] == "true" for row in rows),
            "null_response_locked_rows": sum(row["null_response_locked"] == "true" for row in rows),
            "required_materials_total": sum(int(row["required_materials_count"]) for row in rows),
            "supplied_materials_total": sum(int(row["supplied_materials_count"]) for row in rows),
            "real_score_ready_input_supplied_rows": sum(
                row["real_score_ready_input_supplied"] == "true" for row in rows
            ),
            "scoring_input_accepted_rows": sum(row["scoring_input_accepted"] == "true" for row in rows),
            "reopen_scoring_route_allowed_now_rows": sum(
                row["reopen_scoring_route_allowed_now"] == "true" for row in rows
            ),
            "score_attempt_allowed_now_rows": sum(row["score_attempt_allowed_now"] == "true" for row in rows),
            "score_attempt_blocked_now_rows": sum(row["score_attempt_blocked_now"] == "true" for row in rows),
            "phi_tau_eff_derived_rows": sum(row["phi_tau_eff_derived"] == "true" for row in rows),
            "scores_computed_rows": sum(row["scores_computed"] == "true" for row in rows),
            "cmb_likelihood_available_rows": sum(row["cmb_likelihood_available"] == "true" for row in rows),
            "real_score_ready_input_supply_contract_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "REAL_SCORE_READY_INPUT_SUPPLY_CONTRACT_DECLARED_INPUT_NOT_SUPPLIED_ROUTE_REMAINS_LOCKED",
            "next_required_artifact": "supply_all_real_score_ready_input_materials_or_keep_route_locked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / f"{PREFIX}.md").write_text(
        """# Tau CMB Phi Tau Parent Real Score-Ready Input Supply Contract v01

**Doc class:** real score-ready input supply contract
**Status:** unlock contract declared; no real score-ready input supplied

This artifact consumes the route-completion certificate and declares the
materials required to unlock the null-response locked route. It does not supply
those materials. It therefore keeps the scoring route locked.

Required materials per row:

```text
phi_tau_eff_source
dimension_replay
normalization_binding
endpoint_blind_provenance
cmb_readout_mapping
likelihood_adapter
acceptance_replay
```

Summary:

```text
route_completed_rows=7
null_response_locked_rows=7
required_materials_total=49
supplied_materials_total=0
real_score_ready_input_supplied_rows=0
scoring_input_accepted_rows=0
reopen_scoring_route_allowed_now_rows=0
score_attempt_blocked_now_rows=7
```

## Claim Boundary

This artifact declares the unlock contract only. It supplies no real score-ready
input, accepts no scoring input, derives no `Phi_tau_eff`, computes no score,
supplies no CMB likelihood, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = contract_rows(read_csv(DERIVED / f"{SOURCE_PREFIX}.csv"))
    write_csv(DERIVED / f"{PREFIX}.csv", rows, FIELDS)
    write_csv(DERIVED / f"{PREFIX[:-4]}_summary_v01.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_REAL_SCORE_READY_INPUT_SUPPLY_CONTRACT_V01_BUILT")


if __name__ == "__main__":
    main()
