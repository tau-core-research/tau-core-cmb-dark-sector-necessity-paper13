#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

PACKET_ID = "TAU_CMB_ACOUSTIC_SOURCE_OPERATOR_PAYLOAD_SUPPLY_V01"
CONTRACT = DERIVED / "tau_cmb_acoustic_source_operator_payload_v01.csv"
CLAIM_BOUNDARY = (
    "tau_cmb_acoustic_source_operator_payload_supply_v01_explicit_empty_supply_"
    "no_operator_solution_no_peak_prediction_no_score_no_likelihood_no_verdict"
)

ROW_FIELDS = [
    "supply_row_id",
    "operator_row_id",
    "operator_component",
    "symbolic_slot",
    "required_payload_content",
    "source_dependency",
    "supply_mode",
    "supplied_artifact",
    "derivation_trace_status",
    "numeric_or_symbolic_rule_status",
    "endpoint_blind_attestation_status",
    "dimension_convention_status",
    "acceptance_decision",
    "score_entry_allowed",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "supply_rows_declared",
    "required_operator_payload_rows_checked",
    "operator_payload_supplied_rows",
    "operator_payload_accepted_rows",
    "operator_payload_rejected_rows",
    "firewall_preserved_rows",
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def supply_rows(contract_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for index, row in enumerate(contract_rows, start=1):
        is_firewall = row["operator_component"] == "score_firewall"
        out.append(
            {
                "supply_row_id": f"TCMBACSOPS01_{index:03d}",
                "operator_row_id": row["operator_row_id"],
                "operator_component": row["operator_component"],
                "symbolic_slot": row["symbolic_slot"],
                "required_payload_content": row["required_payload_content"],
                "source_dependency": row["source_dependency"],
                "supply_mode": "FIREWALL_PRESERVED" if is_firewall else "EXPLICIT_EMPTY_OPERATOR_PAYLOAD_SUPPLY",
                "supplied_artifact": "none" if not is_firewall else "tau_cmb_planck_pr3_peak_score_attempt_guard_v01",
                "derivation_trace_status": "not_applicable_firewall" if is_firewall else "missing",
                "numeric_or_symbolic_rule_status": "not_applicable_firewall" if is_firewall else "missing",
                "endpoint_blind_attestation_status": "firewall_preserved" if is_firewall else "missing",
                "dimension_convention_status": "score_closed_no_dimension_claim" if is_firewall else "missing",
                "acceptance_decision": (
                    "FIREWALL_PASSED_SCORE_STILL_BLOCKED"
                    if is_firewall
                    else "REJECTED_OPERATOR_PAYLOAD_SUPPLY_EMPTY"
                ),
                "score_entry_allowed": "false",
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def summary(rows: list[dict[str, str]]) -> dict[str, str]:
    required = [row for row in rows if row["supply_mode"] == "EXPLICIT_EMPTY_OPERATOR_PAYLOAD_SUPPLY"]
    firewall = [row for row in rows if row["supply_mode"] == "FIREWALL_PRESERVED"]
    return {
        "summary_id": PACKET_ID,
        "supply_rows_declared": str(len(rows)),
        "required_operator_payload_rows_checked": str(len(required)),
        "operator_payload_supplied_rows": "0",
        "operator_payload_accepted_rows": "0",
        "operator_payload_rejected_rows": str(
            sum(row["acceptance_decision"] == "REJECTED_OPERATOR_PAYLOAD_SUPPLY_EMPTY" for row in required)
        ),
        "firewall_preserved_rows": str(len(firewall)),
        "derived_source_rows": "0",
        "executable_prediction_rows": "0",
        "accepted_planck_payload_rows": "0",
        "score_ready_rows": "0",
        "scores_computed": "false",
        "cmb_likelihood_available": "false",
        "tau_response_claim_allowed": "false",
        "dark_sector_verdict_allowed": "false",
        "overall_status": "ACOUSTIC_SOURCE_OPERATOR_PAYLOAD_SUPPLY_EXPLICIT_EMPTY_SCORE_BLOCKED",
        "next_required_artifact": "tau_cmb_acoustic_minimal_operator_model_attempt_v01",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_json(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "acoustic_source_operator_payload_supply",
        "status": row["overall_status"],
        "claim_boundary": CLAIM_BOUNDARY,
        "contract_source": "tau_cmb_acoustic_source_operator_payload_v01",
        "operator_target": "P_ac[Phi_tau_eff,A_tau,Theta_tau_ac,C_rec](k,a)",
        "supply_rows": rows,
        "summary": row,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_doc(path: Path, rows: list[dict[str, str]], row: dict[str, str]) -> None:
    lines = [
        "# Tau CMB Acoustic Source Operator Payload Supply v01",
        "",
        "**Doc class:** acoustic source-operator payload supply attempt",
        "**Reader role:** Paper 13 CMB peak scoring path",
        "**Status:** explicit empty supply; no operator payload accepted; score blocked",
        "**Canonical parent:** Paper 13 CMB scoring input fulfillment chain",
        "",
        "## Purpose",
        "",
        "This artifact closes the gap between the `P_ac` operator-payload contract and the scoring firewall by recording the actual v01 supply state. The state is explicitly empty: no accepted operator solution, symbolic rule, numeric kernel, endpoint-blind derivation trace, peak prediction, uncertainty model, or null-response control is supplied.",
        "",
        "This is not another abstract gate. It is the auditable handoff that says the next substantive step must be a minimal acoustic operator model attempt.",
        "",
        "## Summary",
        "",
        f"- supply_rows_declared = {row['supply_rows_declared']}",
        f"- required_operator_payload_rows_checked = {row['required_operator_payload_rows_checked']}",
        f"- operator_payload_supplied_rows = {row['operator_payload_supplied_rows']}",
        f"- operator_payload_accepted_rows = {row['operator_payload_accepted_rows']}",
        f"- operator_payload_rejected_rows = {row['operator_payload_rejected_rows']}",
        f"- firewall_preserved_rows = {row['firewall_preserved_rows']}",
        f"- derived_source_rows = {row['derived_source_rows']}",
        f"- executable_prediction_rows = {row['executable_prediction_rows']}",
        f"- accepted_planck_payload_rows = {row['accepted_planck_payload_rows']}",
        f"- score_ready_rows = {row['score_ready_rows']}",
        f"- overall_status = {row['overall_status']}",
        f"- next_required_artifact = {row['next_required_artifact']}",
        "",
        "## Supply Rows",
        "",
        "| component | symbolic_slot | supply_mode | acceptance_decision |",
        "| --- | --- | --- | --- |",
    ]
    for supply_row in rows:
        lines.append(
            f"| {supply_row['operator_component']} | {supply_row['symbolic_slot']} | "
            f"{supply_row['supply_mode']} | {supply_row['acceptance_decision']} |"
        )
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            CLAIM_BOUNDARY,
            "",
            "This explicit empty supply record does not solve the acoustic operator, does not derive `S_tau_ac`, does not predict Planck peaks, does not compute a CMB score or likelihood, and does not decide whether a dark sector is needed.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    rows = supply_rows(read_csv(CONTRACT))
    row = summary(rows)
    write_csv(DERIVED / "tau_cmb_acoustic_source_operator_payload_supply_v01.csv", rows, ROW_FIELDS)
    write_csv(DERIVED / "tau_cmb_acoustic_source_operator_payload_supply_summary_v01.csv", [row], SUMMARY_FIELDS)
    write_json(DERIVED / "tau_cmb_acoustic_source_operator_payload_supply_v01.json", rows, row)
    write_doc(DOCS / "tau_cmb_acoustic_source_operator_payload_supply_v01.md", rows, row)
    print("TAU_CMB_ACOUSTIC_SOURCE_OPERATOR_PAYLOAD_SUPPLY_V01_BUILT")


if __name__ == "__main__":
    main()
