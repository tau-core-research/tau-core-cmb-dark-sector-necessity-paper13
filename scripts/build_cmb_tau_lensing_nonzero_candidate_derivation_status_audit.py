#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CANDIDATE_SUMMARY = DERIVED / "cmb_act_dr6_lensing_tau_nonzero_response_candidate_packet_v01_summary.json"
CANDIDATE_OBLIGATIONS = DERIVED / "cmb_act_dr6_lensing_tau_nonzero_response_candidate_packet_v01_obligations.csv"
HOLDOUT_SUMMARY = DERIVED / "cmb_planck_lensing_cross_readout_holdout_for_tau_candidate_v01_summary.json"
ACT_SCOREBOARD = DERIVED / "cmb_act_dr6_lensing_tau_shape_response_controls_v01_scoreboard.csv"

PREFIX = "cmb_tau_lensing_nonzero_candidate_derivation_status_audit_v01"
CLAIM_BOUNDARY = (
    "cmb_tau_lensing_nonzero_candidate_derivation_status_audit_v01_formula_level_status_only_"
    "zero_limit_closed_holdout_partial_shape_and_amplitude_tau_derivation_open_no_physical_tau_claim_no_verdict"
)

STATUS_FIELDS = [
    "obligation_id",
    "requirement",
    "status_after_audit",
    "evidence_artifact",
    "evidence_summary",
    "claim_allowed_after_audit",
    "remaining_blocker",
    "claim_boundary",
]

FORMULA_FIELDS = [
    "formula_row_id",
    "object",
    "definition",
    "dimension_or_units",
    "status",
    "claim_boundary",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_doc(summary: dict[str, object]) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / f"{PREFIX}.md").write_text(
        f"""# Tau Lensing Nonzero Candidate Derivation Status Audit v01

**Doc class:** derivation-status and obligation audit
**Status:** formula-level zero limit closed; Planck holdout partially addresses cross-readout; Tau-side shape and amplitude derivation remain open
**Canonical parent:** Paper 13 ACT/Planck lensing scoring route

This artifact audits the four obligations attached to the current nonzero
Tau-style lensing candidate. It does not promote the candidate to a physical
Tau prediction. It separates what is now closed at the formula/control level
from what still needs a Tau-side derivation.

Locked diagnostic response family:

```text
S(L; L_c,p,q) = ((L/L_c)^p)/(1+(L/L_c)^(p+q)) / max_L S_raw
R_tau^kk(L) = A S(L; L_c,p,q)
y_tau = R_tau^kk evaluated in the chosen lensing readout basis
```

Current candidate:

```text
candidate_id={summary["candidate_id"]}
A={summary["transferred_amplitude"]}
L_c={summary["transferred_ell_c"]}
p={summary["transferred_rise_power"]}
q={summary["transferred_fall_power"]}
```

Audit result:

```text
obligations_total={summary["obligations_total"]}
closed_formula_level={summary["closed_formula_level"]}
partially_addressed={summary["partially_addressed"]}
open_tau_derivation={summary["open_tau_derivation"]}
physical_tau_response_claim_allowed={summary["physical_tau_response_claim_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

The zero-source known limit is closed only for this diagnostic formula family:
if the Tau response amplitude is absent or set to \(A=0\), then
\(R_\\tau^{{\\kappa\\kappa}}(L)=0\) in every band. The Planck holdout partially
addresses the cross-readout obligation because the same ACT-selected candidate
was transferred unchanged and still improved over null in the Planck block.

## Remaining Blocker

The candidate still needs a Tau-side derivation or rejection of both:

1. the shape parameters \(L_c,p,q\) from morphology/readout structure;
2. the amplitude \(A\) from Tau-side normalization rather than endpoint
   selection.

Until those are supplied, this remains a diagnostic candidate, not a physical
Tau response.
""",
        encoding="utf-8",
    )


def main() -> None:
    candidate = json.loads(CANDIDATE_SUMMARY.read_text())
    holdout = json.loads(HOLDOUT_SUMMARY.read_text())
    obligations = {row["obligation_id"]: row for row in read_csv(CANDIDATE_OBLIGATIONS)}
    best_score = next(row for row in read_csv(ACT_SCOREBOARD) if row["candidate_id"] == candidate["candidate_id"])

    formula_rows = [
        {
            "formula_row_id": "FORMULA_001",
            "object": "dimensionless_shape_S",
            "definition": "S(L;L_c,p,q)=((L/L_c)^p)/(1+(L/L_c)^(p+q))/max_L(S_raw)",
            "dimension_or_units": "dimensionless",
            "status": "locked_for_diagnostic_candidate_family",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "formula_row_id": "FORMULA_002",
            "object": "candidate_response_R_tau_kk",
            "definition": "R_tau^kk(L)=A*S(L;L_c,p,q)",
            "dimension_or_units": "same_units_as_C_L^kk_in_ACT_or_Planck_lensing_readout",
            "status": "diagnostic_formula_not_tau_side_derivation",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "formula_row_id": "FORMULA_003",
            "object": "zero_source_known_limit",
            "definition": "A=0_or_absent_tau_response_source_implies_R_tau^kk(L)=0_for_all_L_and_y_tau=0_in_all_bins",
            "dimension_or_units": "formula_level_limit",
            "status": "closed_for_this_candidate_formula_family_not_full_tau_physics",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "formula_row_id": "FORMULA_004",
            "object": "tau_side_derivation_gap",
            "definition": "derive_or_reject_L_c_p_q_and_A_from_tau_morphology_readout_normalization_without_endpoint_fit",
            "dimension_or_units": "open_theory_derivation",
            "status": "open",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    status_rows = [
        {
            "obligation_id": "NZRESP_OBL_001",
            "requirement": obligations["NZRESP_OBL_001"]["requirement"],
            "status_after_audit": "open_tau_derivation_required",
            "evidence_artifact": "",
            "evidence_summary": "Shape parameters remain selected by diagnostic control family; no Tau-side morphology derivation supplied.",
            "claim_allowed_after_audit": "diagnostic_candidate_only",
            "remaining_blocker": "derive_or_reject_L_c_p_q_from_tau_side_morphology",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "obligation_id": "NZRESP_OBL_002",
            "requirement": obligations["NZRESP_OBL_002"]["requirement"],
            "status_after_audit": "open_tau_derivation_required",
            "evidence_artifact": "",
            "evidence_summary": "Amplitude remains diagnostic; no Tau-side normalization rule supplies A independently.",
            "claim_allowed_after_audit": "diagnostic_candidate_only",
            "remaining_blocker": "derive_or_bound_A_from_tau_side_normalization_without_endpoint_selection",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "obligation_id": "NZRESP_OBL_003",
            "requirement": obligations["NZRESP_OBL_003"]["requirement"],
            "status_after_audit": "closed_formula_level_only",
            "evidence_artifact": f"{PREFIX}_formula_spec.csv",
            "evidence_summary": "For R_tau^kk(L)=A*S(L), A=0 gives y_tau=0 in every lensing readout bin.",
            "claim_allowed_after_audit": "zero_limit_for_diagnostic_formula_family_only",
            "remaining_blocker": "full_tau_zero_source_theorem_still_outside_this_artifact",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "obligation_id": "NZRESP_OBL_004",
            "requirement": obligations["NZRESP_OBL_004"]["requirement"],
            "status_after_audit": "partially_addressed_not_closed",
            "evidence_artifact": str(HOLDOUT_SUMMARY.relative_to(ROOT)),
            "evidence_summary": (
                "ACT-selected candidate transferred unchanged to Planck block: "
                f"Planck null chi2={holdout['null_chi2']:.12g}; "
                f"candidate chi2={holdout['candidate_chi2']:.12g}; "
                f"fractional improvement={holdout['candidate_fractional_chi2_improvement_vs_null']:.12g}."
            ),
            "claim_allowed_after_audit": "cross_readout_diagnostic_support_only",
            "remaining_blocker": "independent_likelihood_or_tau_side_prediction_still_required_for_physical_claim",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    formula_path = DERIVED / f"{PREFIX}_formula_spec.csv"
    status_path = DERIVED / f"{PREFIX}.csv"
    summary_path = DERIVED / f"{PREFIX}_summary.json"
    write_csv(formula_path, formula_rows, FORMULA_FIELDS)
    write_csv(status_path, status_rows, STATUS_FIELDS)

    summary = {
        "summary_id": "CMB_TAU_LENSING_NONZERO_CANDIDATE_DERIVATION_STATUS_AUDIT_V01",
        "candidate_summary_path": str(CANDIDATE_SUMMARY.relative_to(ROOT)),
        "candidate_summary_sha256": sha256(CANDIDATE_SUMMARY),
        "candidate_obligations_path": str(CANDIDATE_OBLIGATIONS.relative_to(ROOT)),
        "candidate_obligations_sha256": sha256(CANDIDATE_OBLIGATIONS),
        "holdout_summary_path": str(HOLDOUT_SUMMARY.relative_to(ROOT)),
        "holdout_summary_sha256": sha256(HOLDOUT_SUMMARY),
        "formula_spec_path": str(formula_path.relative_to(ROOT)),
        "formula_spec_sha256": sha256(formula_path),
        "status_path": str(status_path.relative_to(ROOT)),
        "status_sha256": sha256(status_path),
        "candidate_id": candidate["candidate_id"],
        "transferred_amplitude": holdout["transferred_amplitude"],
        "transferred_ell_c": holdout["transferred_ell_c"],
        "transferred_rise_power": holdout["transferred_rise_power"],
        "transferred_fall_power": holdout["transferred_fall_power"],
        "act_candidate_chi2": candidate["chi2_tau"],
        "act_delta_chi2_vs_null": candidate["delta_chi2_vs_null"],
        "planck_candidate_chi2": holdout["candidate_chi2"],
        "planck_delta_chi2_vs_null": holdout["candidate_delta_chi2_vs_null"],
        "obligations_total": len(status_rows),
        "closed_formula_level": 1,
        "partially_addressed": 1,
        "open_tau_derivation": 2,
        "zero_limit_closed_for_formula_family": True,
        "cross_readout_holdout_support_present": True,
        "shape_tau_derivation_present": False,
        "amplitude_tau_derivation_present": False,
        "physical_tau_response_claim_allowed": False,
        "dark_sector_verdict_allowed": False,
        "next_required_artifact": "tau_side_shape_and_amplitude_derivation_or_rejection",
        "best_score_source_candidate_id": best_score["candidate_id"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_doc(summary)
    print(
        ",".join(
            [
                summary["summary_id"],
                summary["candidate_id"],
                str(summary["closed_formula_level"]),
                str(summary["partially_addressed"]),
                str(summary["open_tau_derivation"]),
                str(summary["physical_tau_response_claim_allowed"]).lower(),
            ]
        )
    )


if __name__ == "__main__":
    main()
