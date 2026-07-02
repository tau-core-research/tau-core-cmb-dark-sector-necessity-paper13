#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

PACKET_ID = "TAU_CMB_ACOUSTIC_DOMAIN_BASIS_LOCK_ACCEPTANCE_V01"
CLAIM_BOUNDARY = (
    "tau_cmb_acoustic_domain_basis_lock_acceptance_v01_convention_lock_only_"
    "no_operator_solution_no_peak_prediction_no_score_no_likelihood_no_verdict"
)

ROW_FIELDS = [
    "lock_row_id",
    "basis_component",
    "locked_symbol_or_role",
    "locked_convention",
    "endpoint_blind_status",
    "dimension_convention_status",
    "acceptance_decision",
    "unblocks_operator_component",
    "score_entry_allowed",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "lock_rows_declared",
    "lock_rows_accepted",
    "endpoint_blind_pass_rows",
    "dimension_convention_locked_rows",
    "domain_basis_lock_accepted",
    "operator_model_accepted_rows",
    "derived_source_rows",
    "executable_prediction_rows",
    "accepted_planck_payload_rows",
    "score_ready_rows",
    "scores_computed",
    "cmb_likelihood_available",
    "tau_response_claim_allowed",
    "dark_sector_verdict_allowed",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def lock_rows() -> list[dict[str, str]]:
    rows = [
        {
            "basis_component": "wavenumber_domain",
            "locked_symbol_or_role": "k",
            "locked_convention": "Comoving acoustic wavenumber coordinate used only as a Tau-side operator-domain coordinate.",
        },
        {
            "basis_component": "scale_readout_domain",
            "locked_symbol_or_role": "a",
            "locked_convention": "Scale-factor/readout coordinate for the reduced acoustic role; no physical time claim is made here.",
        },
        {
            "basis_component": "recombination_readout_slice",
            "locked_symbol_or_role": "a_rec",
            "locked_convention": "Recombination readout slice used as an output boundary for the acoustic scaffold.",
        },
        {
            "basis_component": "angular_peak_coordinate",
            "locked_symbol_or_role": "ell",
            "locked_convention": "Observed-side multipole coordinate inherited from the Planck PR3 peak extraction chain.",
        },
        {
            "basis_component": "integration_measure_placeholder",
            "locked_symbol_or_role": "da",
            "locked_convention": "Formal reduced integration measure placeholder; physical normalization remains blocked until the kernel row.",
        },
        {
            "basis_component": "spectrum_role_basis",
            "locked_symbol_or_role": "spectrum_role in {TT,TE,EE}",
            "locked_convention": "Spectrum-role labels are inherited from the observed Planck peak table before any Tau prediction comparison.",
        },
        {
            "basis_component": "comparison_boundary",
            "locked_symbol_or_role": "endpoint_blind_peak_comparison",
            "locked_convention": "No endpoint residuals, fitted CMB likelihoods, or dark-sector labels may be read while constructing Tau-side payloads.",
        },
    ]
    out: list[dict[str, str]] = []
    for index, row in enumerate(rows, start=1):
        out.append(
            {
                "lock_row_id": f"TCMBACDBLA01_{index:03d}",
                "endpoint_blind_status": "PASS_NO_ENDPOINT_RESIDUALS_READ",
                "dimension_convention_status": "LOCKED_CONVENTION_ONLY",
                "acceptance_decision": "ACCEPTED_DOMAIN_BASIS_LOCK_ROW",
                "unblocks_operator_component": "domain_and_basis_lock",
                "score_entry_allowed": "false",
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
                **row,
            }
        )
    return out


def summary(rows: list[dict[str, str]]) -> dict[str, str]:
    accepted = sum(row["acceptance_decision"] == "ACCEPTED_DOMAIN_BASIS_LOCK_ROW" for row in rows)
    return {
        "summary_id": PACKET_ID,
        "lock_rows_declared": str(len(rows)),
        "lock_rows_accepted": str(accepted),
        "endpoint_blind_pass_rows": str(sum(row["endpoint_blind_status"] == "PASS_NO_ENDPOINT_RESIDUALS_READ" for row in rows)),
        "dimension_convention_locked_rows": str(sum(row["dimension_convention_status"] == "LOCKED_CONVENTION_ONLY" for row in rows)),
        "domain_basis_lock_accepted": "true" if accepted == len(rows) else "false",
        "operator_model_accepted_rows": "1",
        "derived_source_rows": "0",
        "executable_prediction_rows": "0",
        "accepted_planck_payload_rows": "0",
        "score_ready_rows": "0",
        "scores_computed": "false",
        "cmb_likelihood_available": "false",
        "tau_response_claim_allowed": "false",
        "dark_sector_verdict_allowed": "false",
        "overall_status": "ACOUSTIC_DOMAIN_BASIS_LOCK_ACCEPTED_SCORE_BLOCKED",
        "next_required_artifact": "tau_cmb_phi_tau_eff_acoustic_input_acceptance_v01",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_json(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "acoustic_domain_basis_lock_acceptance",
        "status": row["overall_status"],
        "claim_boundary": CLAIM_BOUNDARY,
        "lock_rows": rows,
        "summary": row,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_doc(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    lines = [
        "# Tau CMB Acoustic Domain Basis Lock Acceptance v01",
        "",
        "**Doc class:** acoustic domain/basis lock acceptance",
        "**Reader role:** Paper 13 CMB peak scoring path",
        "**Status:** domain/basis conventions accepted; score blocked",
        "**Canonical parent:** Paper 13 CMB scoring input fulfillment chain",
        "",
        "## Purpose",
        "",
        "This artifact closes the first acoustic-operator dependency row: the domain and basis convention for `P_ac`. It locks the reduced coordinates and comparison boundary needed before `Phi_tau_eff`, `A_tau`, oscillator-kernel, coupling, and peak-projection rows can be assessed.",
        "",
        "It is a convention lock only. It does not solve the acoustic operator and does not create a Tau prediction.",
        "",
        "## Summary",
        "",
        f"- lock_rows_declared = {row['lock_rows_declared']}",
        f"- lock_rows_accepted = {row['lock_rows_accepted']}",
        f"- endpoint_blind_pass_rows = {row['endpoint_blind_pass_rows']}",
        f"- dimension_convention_locked_rows = {row['dimension_convention_locked_rows']}",
        f"- domain_basis_lock_accepted = {row['domain_basis_lock_accepted']}",
        f"- operator_model_accepted_rows = {row['operator_model_accepted_rows']}",
        f"- executable_prediction_rows = {row['executable_prediction_rows']}",
        f"- score_ready_rows = {row['score_ready_rows']}",
        f"- overall_status = {row['overall_status']}",
        f"- next_required_artifact = {row['next_required_artifact']}",
        "",
        "## Accepted Lock Rows",
        "",
        "| component | symbol_or_role | acceptance_decision |",
        "| --- | --- | --- |",
    ]
    for lock_row in rows:
        lines.append(
            f"| {lock_row['basis_component']} | {lock_row['locked_symbol_or_role']} | "
            f"{lock_row['acceptance_decision']} |"
        )
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            CLAIM_BOUNDARY,
            "",
            "This convention lock does not solve the acoustic operator, does not derive an executable `S_tau_ac`, does not predict Planck peaks, does not compute a CMB score or likelihood, and does not decide whether a dark sector is needed.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    rows = lock_rows()
    row = summary(rows)
    write_csv(DERIVED / "tau_cmb_acoustic_domain_basis_lock_acceptance_v01.csv", rows, ROW_FIELDS)
    write_csv(DERIVED / "tau_cmb_acoustic_domain_basis_lock_acceptance_summary_v01.csv", [row], SUMMARY_FIELDS)
    write_json(DERIVED / "tau_cmb_acoustic_domain_basis_lock_acceptance_v01.json", rows, row)
    write_doc(DOCS / "tau_cmb_acoustic_domain_basis_lock_acceptance_v01.md", rows, row)
    print("TAU_CMB_ACOUSTIC_DOMAIN_BASIS_LOCK_ACCEPTANCE_V01_BUILT")


if __name__ == "__main__":
    main()
