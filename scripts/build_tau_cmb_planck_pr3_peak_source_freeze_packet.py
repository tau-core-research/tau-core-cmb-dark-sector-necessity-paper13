#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

PACKET_ID = "TAU_CMB_PLANCK_PR3_PEAK_SOURCE_FREEZE_PACKET_V01"
CLAIM_BOUNDARY = (
    "tau_cmb_planck_pr3_peak_source_freeze_packet_v01_source_freeze_only_"
    "no_download_no_extraction_no_score_no_likelihood_no_verdict"
)
IRSA_BASE = "https://irsa.ipac.caltech.edu/data/Planck/release_3/ancillary-data/cosmoparams/"


ARTIFACTS = [
    {
        "artifact_id": "PLANCK_PR3_PEAKSRC_001",
        "artifact_role": "primary_tt_peak_observable",
        "cmb_role": "acoustic_peak_phase_and_height",
        "source_product_class": "cmb_power_spectrum_tt_binned",
        "release_label": "Planck PR3/R3.01",
        "official_url": IRSA_BASE + "COM_PowerSpect_CMB-TT-binned_R3.01.txt",
        "expected_use": "TT peak position and height extraction target",
        "extraction_rule_id": "planck_pr3_binned_peak_extract_v01",
    },
    {
        "artifact_id": "PLANCK_PR3_PEAKSRC_002",
        "artifact_role": "polarization_cross_check",
        "cmb_role": "acoustic_peak_phase_and_height",
        "source_product_class": "cmb_power_spectrum_te_binned",
        "release_label": "Planck PR3/R3.02",
        "official_url": IRSA_BASE + "COM_PowerSpect_CMB-TE-binned_R3.02.txt",
        "expected_use": "TE peak phase cross-check target",
        "extraction_rule_id": "planck_pr3_binned_peak_extract_v01",
    },
    {
        "artifact_id": "PLANCK_PR3_PEAKSRC_003",
        "artifact_role": "polarization_peak_check",
        "cmb_role": "acoustic_peak_phase_and_height",
        "source_product_class": "cmb_power_spectrum_ee_binned",
        "release_label": "Planck PR3/R3.02",
        "official_url": IRSA_BASE + "COM_PowerSpect_CMB-EE-binned_R3.02.txt",
        "expected_use": "EE peak and damping-tail cross-check target",
        "extraction_rule_id": "planck_pr3_binned_peak_extract_v01",
    },
    {
        "artifact_id": "PLANCK_PR3_PEAKSRC_004",
        "artifact_role": "lcdm_reference_curve",
        "cmb_role": "known_limit_or_explicit_failure",
        "source_product_class": "cmb_minimum_theory_baseline",
        "release_label": "Planck PR3/R3.01",
        "official_url": IRSA_BASE + "COM_PowerSpect_CMB-base-plikHM-TTTEEE-lowl-lowE-lensing-minimum-theory_R3.01.txt",
        "expected_use": "baseline minimum-theory curve reference for known-limit comparison",
        "extraction_rule_id": "planck_pr3_minimum_theory_reference_v01",
    },
]

ARTIFACT_FIELDS = [
    "artifact_id",
    "artifact_role",
    "cmb_role",
    "source_product_class",
    "release_label",
    "official_url",
    "expected_use",
    "extraction_rule_id",
    "download_status",
    "raw_artifact_hash",
    "local_artifact_path",
    "local_hash_status",
    "extraction_status",
    "score_entry_allowed",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "artifact_rows_declared",
    "artifact_urls_selected",
    "local_hashes_computed",
    "extraction_rules_declared",
    "extraction_rules_executed",
    "score_ready",
    "score_entry_allowed_rows",
    "scores_computed",
    "cmb_likelihood_available",
    "no_dark_cmb_verdict_allowed",
    "tau_response_claim_allowed",
    "dark_sector_verdict_allowed",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]


def artifact_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in ARTIFACTS:
        row = dict(item)
        row.update(
            {
                "download_status": "NOT_DOWNLOADED_BY_REPRO_PACKAGE",
                "raw_artifact_hash": "NOT_COMPUTED",
                "local_artifact_path": "data/external/planck_pr3/PRIVATE_WORKING_COPY_ONLY",
                "local_hash_status": "HASH_PENDING_REQUIRES_LOCAL_DOWNLOAD",
                "extraction_status": "DECLARED_NOT_EXECUTED",
                "score_entry_allowed": "false",
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        rows.append(row)
    return rows


def summary_row() -> dict[str, str]:
    rules = {item["extraction_rule_id"] for item in ARTIFACTS}
    return {
        "summary_id": PACKET_ID,
        "artifact_rows_declared": str(len(ARTIFACTS)),
        "artifact_urls_selected": str(len({item["official_url"] for item in ARTIFACTS})),
        "local_hashes_computed": "0",
        "extraction_rules_declared": str(len(rules)),
        "extraction_rules_executed": "0",
        "score_ready": "false",
        "score_entry_allowed_rows": "0",
        "scores_computed": "false",
        "cmb_likelihood_available": "false",
        "no_dark_cmb_verdict_allowed": "false",
        "tau_response_claim_allowed": "false",
        "dark_sector_verdict_allowed": "false",
        "overall_status": "PLANCK_PR3_ARTIFACT_URLS_SELECTED_EXTRACTION_FREEZE_PENDING",
        "next_required_artifact": "tau_cmb_planck_pr3_peak_extraction_rule_v01",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, rows: list[dict[str, str]], summary: dict[str, str]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "source_freeze_packet",
        "status": "artifact_urls_selected_extraction_pending",
        "claim_boundary": CLAIM_BOUNDARY,
        "source_family": "Planck PR3 ancillary cosmoparams power-spectrum products",
        "artifacts": rows,
        "summary": summary,
        "extraction_target_schema": {
            "status": "declared_not_executed",
            "peak_observable_target": "O_CMB_peak",
            "candidate_fields": [
                "spectrum_label",
                "ell_center",
                "D_ell",
                "sigma_minus",
                "sigma_plus",
                "peak_index",
                "peak_position",
                "peak_height",
                "phase_residual",
                "damping_proxy",
            ],
            "required_before_scoring": [
                "local byte hash for each selected raw artifact",
                "frozen parser/extraction rule",
                "peak table with uncertainty propagation",
                "endpoint-blind scoring input manifest",
                "null/gauge and known-limit controls",
            ],
        },
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, str]) -> None:
    lines = [
        "# Tau CMB Planck PR3 Peak Source Freeze Packet v01",
        "",
        "**Doc class:** source-freeze packet",
        "**Reader role:** Paper 13 CMB scoring input provenance",
        "**Status:** artifact URLs selected; local download, hash, extraction, likelihood, and scoring are pending",
        "**Canonical parent:** Paper 13 CMB scoring input fulfillment chain",
        "",
        "## Purpose",
        "",
        "This packet replaces an abstract CMB peak-data blocker with a concrete, official Planck PR3 source-family selection. It records which public ancillary products should seed the first endpoint-blind CMB peak extraction attempt.",
        "",
        "It does not download or redistribute the raw Planck products. It does not extract peaks, compute a likelihood, compute a score, or permit any Tau-response or dark-sector verdict.",
        "",
        "## Selected Official Artifacts",
        "",
        "| artifact_id | role | source_product_class | release | status |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['artifact_id']} | {row['artifact_role']} | {row['source_product_class']} | "
            f"{row['release_label']} | {row['extraction_status']} |"
        )
    lines.extend(
        [
            "",
            "## Freeze Result",
            "",
            f"- artifact_rows_declared = {summary['artifact_rows_declared']}",
            f"- artifact_urls_selected = {summary['artifact_urls_selected']}",
            f"- local_hashes_computed = {summary['local_hashes_computed']}",
            f"- extraction_rules_executed = {summary['extraction_rules_executed']}",
            f"- score_ready = {summary['score_ready']}",
            f"- score_entry_allowed_rows = {summary['score_entry_allowed_rows']}",
            f"- overall_status = {summary['overall_status']}",
            f"- next_required_artifact = {summary['next_required_artifact']}",
            "",
            "## Claim Boundary",
            "",
            CLAIM_BOUNDARY,
            "",
            "This is a source-selection bridge only. The next admissible step is a frozen extraction rule that can turn the selected TT/TE/EE products into a reproducible peak-observable table with hashes and uncertainty handling.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    rows = artifact_rows()
    summary = summary_row()
    write_csv(DERIVED / "tau_cmb_planck_pr3_peak_source_freeze_packet_v01.csv", rows, ARTIFACT_FIELDS)
    write_csv(
        DERIVED / "tau_cmb_planck_pr3_peak_source_freeze_packet_summary_v01.csv",
        [summary],
        SUMMARY_FIELDS,
    )
    write_json(DERIVED / "tau_cmb_planck_pr3_peak_source_freeze_packet_v01.json", rows, summary)
    write_doc(DOCS / "tau_cmb_planck_pr3_peak_source_freeze_packet_v01.md", rows, summary)
    print("TAU_CMB_PLANCK_PR3_PEAK_SOURCE_FREEZE_PACKET_V01_BUILT")


if __name__ == "__main__":
    main()
