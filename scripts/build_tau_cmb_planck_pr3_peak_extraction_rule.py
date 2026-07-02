#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"
EXTERNAL = ROOT / "data" / "external" / "planck_pr3"

PACKET_ID = "TAU_CMB_PLANCK_PR3_PEAK_EXTRACTION_RULE_V01"
CLAIM_BOUNDARY = (
    "tau_cmb_planck_pr3_peak_extraction_rule_v01_observable_extraction_only_"
    "no_tau_prediction_no_likelihood_no_score_no_dark_sector_verdict"
)
IRSA_BASE = "https://irsa.ipac.caltech.edu/data/Planck/release_3/ancillary-data/cosmoparams/"

SOURCES = [
    {
        "artifact_id": "PLANCK_PR3_PEAKSRC_001",
        "spectrum": "TT",
        "filename": "COM_PowerSpect_CMB-TT-binned_R3.01.txt",
        "parser_rule": "binned_spectrum_l_Dl_minus_plus_bestfit",
        "extremum_rule": "positive_local_maximum_in_Dl",
        "observable_role": "primary_acoustic_peak_height_phase",
    },
    {
        "artifact_id": "PLANCK_PR3_PEAKSRC_002",
        "spectrum": "TE",
        "filename": "COM_PowerSpect_CMB-TE-binned_R3.02.txt",
        "parser_rule": "binned_spectrum_l_Dl_minus_plus_bestfit",
        "extremum_rule": "local_extremum_in_abs_Dl_with_signed_Dl_retained",
        "observable_role": "cross_polarization_phase_extremum_check",
    },
    {
        "artifact_id": "PLANCK_PR3_PEAKSRC_003",
        "spectrum": "EE",
        "filename": "COM_PowerSpect_CMB-EE-binned_R3.02.txt",
        "parser_rule": "binned_spectrum_l_Dl_minus_plus_bestfit",
        "extremum_rule": "positive_local_maximum_in_Dl",
        "observable_role": "polarization_peak_and_damping_check",
    },
    {
        "artifact_id": "PLANCK_PR3_PEAKSRC_004",
        "spectrum": "MINIMUM_THEORY",
        "filename": "COM_PowerSpect_CMB-base-plikHM-TTTEEE-lowl-lowE-lensing-minimum-theory_R3.01.txt",
        "parser_rule": "minimum_theory_L_TT_TE_EE_BB_PP",
        "extremum_rule": "reference_curve_not_peak_extracted_in_v01",
        "observable_role": "lcdm_known_limit_reference_curve",
    },
]

RECEIPT_FIELDS = [
    "artifact_id",
    "spectrum",
    "official_url",
    "local_artifact_path",
    "download_status",
    "byte_size",
    "sha256",
    "parser_rule",
    "extremum_rule",
    "observable_role",
    "claim_boundary",
]

PEAK_FIELDS = [
    "peak_id",
    "artifact_id",
    "spectrum",
    "peak_rank",
    "ell_center",
    "D_ell",
    "sigma_minus",
    "sigma_plus",
    "best_fit_D_ell",
    "data_minus_bestfit",
    "extremum_kind",
    "observable_role",
    "extraction_rule_id",
    "score_entry_allowed",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "source_artifacts_declared",
    "source_artifacts_downloaded",
    "source_hashes_computed",
    "spectra_peak_extracted",
    "peak_rows_extracted",
    "tt_peak_rows",
    "te_extremum_rows",
    "ee_peak_rows",
    "minimum_theory_reference_downloaded",
    "parser_rule_frozen",
    "observable_table_materialized",
    "score_ready",
    "scores_computed",
    "cmb_likelihood_available",
    "no_dark_cmb_verdict_allowed",
    "tau_response_claim_allowed",
    "dark_sector_verdict_allowed",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]


def download_bytes(url: str) -> bytes:
    with urlopen(url, timeout=30) as response:
        return response.read()


def parse_numeric_table(text: str) -> list[list[float]]:
    rows: list[list[float]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        rows.append([float(part) for part in stripped.split()])
    return rows


def local_extrema(source: dict[str, str], numeric_rows: list[list[float]]) -> list[dict[str, str]]:
    spectrum = source["spectrum"]
    if spectrum == "MINIMUM_THEORY":
        return []

    peaks: list[dict[str, str]] = []
    for index in range(1, len(numeric_rows) - 1):
        previous = numeric_rows[index - 1][1]
        current = numeric_rows[index][1]
        following = numeric_rows[index + 1][1]
        is_extremum = False
        extremum_kind = "positive_peak"
        if spectrum == "TE":
            is_extremum = abs(current) > abs(previous) and abs(current) >= abs(following)
            extremum_kind = "signed_abs_extremum"
        else:
            is_extremum = current > previous and current >= following
        if not is_extremum:
            continue
        ell, d_ell, sigma_minus, sigma_plus, best_fit = numeric_rows[index][:5]
        peaks.append(
            {
                "peak_id": f"{spectrum}_PEAK_{len(peaks) + 1:02d}",
                "artifact_id": source["artifact_id"],
                "spectrum": spectrum,
                "peak_rank": str(len(peaks) + 1),
                "ell_center": f"{ell:.6f}",
                "D_ell": f"{d_ell:.9g}",
                "sigma_minus": f"{sigma_minus:.9g}",
                "sigma_plus": f"{sigma_plus:.9g}",
                "best_fit_D_ell": f"{best_fit:.9g}",
                "data_minus_bestfit": f"{d_ell - best_fit:.9g}",
                "extremum_kind": extremum_kind,
                "observable_role": source["observable_role"],
                "extraction_rule_id": "planck_pr3_binned_peak_extract_v01",
                "score_entry_allowed": "false",
                "allows_tau_response_claim": "false",
                "allows_dark_sector_verdict": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return peaks


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def build() -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, str]]:
    EXTERNAL.mkdir(parents=True, exist_ok=True)
    receipt_rows: list[dict[str, str]] = []
    peak_rows: list[dict[str, str]] = []
    for source in SOURCES:
        url = IRSA_BASE + source["filename"]
        local_path = EXTERNAL / source["filename"]
        raw = download_bytes(url)
        local_path.write_bytes(raw)
        digest = hashlib.sha256(raw).hexdigest()
        receipt_rows.append(
            {
                "artifact_id": source["artifact_id"],
                "spectrum": source["spectrum"],
                "official_url": url,
                "local_artifact_path": str(local_path.relative_to(ROOT)),
                "download_status": "DOWNLOADED_TO_GITIGNORED_EXTERNAL_CACHE",
                "byte_size": str(len(raw)),
                "sha256": digest,
                "parser_rule": source["parser_rule"],
                "extremum_rule": source["extremum_rule"],
                "observable_role": source["observable_role"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        numeric_rows = parse_numeric_table(raw.decode("utf-8"))
        peak_rows.extend(local_extrema(source, numeric_rows))

    tt_rows = sum(row["spectrum"] == "TT" for row in peak_rows)
    te_rows = sum(row["spectrum"] == "TE" for row in peak_rows)
    ee_rows = sum(row["spectrum"] == "EE" for row in peak_rows)
    summary = {
        "summary_id": PACKET_ID,
        "source_artifacts_declared": str(len(SOURCES)),
        "source_artifacts_downloaded": str(len(receipt_rows)),
        "source_hashes_computed": str(len(receipt_rows)),
        "spectra_peak_extracted": "3",
        "peak_rows_extracted": str(len(peak_rows)),
        "tt_peak_rows": str(tt_rows),
        "te_extremum_rows": str(te_rows),
        "ee_peak_rows": str(ee_rows),
        "minimum_theory_reference_downloaded": "true",
        "parser_rule_frozen": "true",
        "observable_table_materialized": "true",
        "score_ready": "false",
        "scores_computed": "false",
        "cmb_likelihood_available": "false",
        "no_dark_cmb_verdict_allowed": "false",
        "tau_response_claim_allowed": "false",
        "dark_sector_verdict_allowed": "false",
        "overall_status": "PLANCK_PR3_PEAK_OBSERVABLE_TABLE_MATERIALIZED_SCORING_STILL_BLOCKED",
        "next_required_artifact": "tau_cmb_planck_pr3_peak_scoring_input_candidate_v01",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return receipt_rows, peak_rows, summary


def write_json(path: Path, receipt_rows: list[dict[str, str]], peak_rows: list[dict[str, str]], summary: dict[str, str]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "doc_class": "observable_extraction_rule",
        "status": "Planck PR3 TT/TE/EE peak observable table materialized; scoring blocked",
        "claim_boundary": CLAIM_BOUNDARY,
        "receipt_rows": receipt_rows,
        "peak_rows": peak_rows,
        "summary": summary,
        "rule_definition": {
            "binned_parser": "Ignore comments and parse whitespace numeric columns l, Dl, -dDl, +dDl, BestFit.",
            "TT_EE_peak_rule": "A binned row is a peak if D_l is greater than the previous bin and not smaller than the following bin.",
            "TE_extremum_rule": "A binned row is an extremum if abs(D_l) is greater than the previous abs(D_l) and not smaller than the following abs(D_l); the signed D_l is retained.",
            "claim_limit": "The output is an observed-feature table only, not a Tau prediction or likelihood.",
        },
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_doc(path: Path, receipt_rows: list[dict[str, str]], peak_rows: list[dict[str, str]], summary: dict[str, str]) -> None:
    lines = [
        "# Tau CMB Planck PR3 Peak Extraction Rule v01",
        "",
        "**Doc class:** observable extraction rule",
        "**Reader role:** Paper 13 CMB scoring input provenance",
        "**Status:** official PR3 artifacts downloaded to gitignored cache; hashes and peak-observable table materialized; scoring remains blocked",
        "**Canonical parent:** Paper 13 CMB scoring input fulfillment chain",
        "",
        "## Rule",
        "",
        "- Parse binned TT/TE/EE spectra as `l, Dl, -dDl, +dDl, BestFit`.",
        "- For TT and EE, accept a local positive peak when `Dl_i > Dl_{i-1}` and `Dl_i >= Dl_{i+1}`.",
        "- For TE, accept a signed extremum when `abs(Dl_i) > abs(Dl_{i-1})` and `abs(Dl_i) >= abs(Dl_{i+1})`.",
        "- Retain the signed measured value, uncertainty columns, best-fit value, and measured-minus-best-fit residual.",
        "- The baseline minimum-theory file is downloaded and hashed as a known-limit reference, but no theory-curve fitting is performed in this artifact.",
        "",
        "## Receipt Summary",
        "",
        "| spectrum | status | bytes | sha256 prefix |",
        "| --- | --- | ---: | --- |",
    ]
    for row in receipt_rows:
        lines.append(
            f"| {row['spectrum']} | {row['download_status']} | {row['byte_size']} | {row['sha256'][:16]} |"
        )
    lines.extend(
        [
            "",
            "## Extraction Result",
            "",
            f"- peak_rows_extracted = {summary['peak_rows_extracted']}",
            f"- tt_peak_rows = {summary['tt_peak_rows']}",
            f"- te_extremum_rows = {summary['te_extremum_rows']}",
            f"- ee_peak_rows = {summary['ee_peak_rows']}",
            f"- parser_rule_frozen = {summary['parser_rule_frozen']}",
            f"- observable_table_materialized = {summary['observable_table_materialized']}",
            f"- score_ready = {summary['score_ready']}",
            f"- overall_status = {summary['overall_status']}",
            f"- next_required_artifact = {summary['next_required_artifact']}",
            "",
            "## First Extracted Rows",
            "",
            "| peak_id | ell_center | D_ell | best_fit_D_ell | data_minus_bestfit |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in peak_rows[:8]:
        lines.append(
            f"| {row['peak_id']} | {row['ell_center']} | {row['D_ell']} | "
            f"{row['best_fit_D_ell']} | {row['data_minus_bestfit']} |"
        )
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            CLAIM_BOUNDARY,
            "",
            "This artifact only materializes a reproducible observed-feature table from official Planck PR3 products. It does not compare Tau Core predictions to the table, does not run a CMB likelihood, and does not decide whether a dark-sector-like Tau response is necessary.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    receipt_rows, peak_rows, summary = build()
    write_csv(DERIVED / "tau_cmb_planck_pr3_source_receipt_v01.csv", receipt_rows, RECEIPT_FIELDS)
    write_csv(DERIVED / "tau_cmb_planck_pr3_peak_observable_table_v01.csv", peak_rows, PEAK_FIELDS)
    write_csv(DERIVED / "tau_cmb_planck_pr3_peak_extraction_rule_summary_v01.csv", [summary], SUMMARY_FIELDS)
    write_json(
        DERIVED / "tau_cmb_planck_pr3_peak_extraction_rule_v01.json",
        receipt_rows,
        peak_rows,
        summary,
    )
    write_doc(DOCS / "tau_cmb_planck_pr3_peak_extraction_rule_v01.md", receipt_rows, peak_rows, summary)
    print("TAU_CMB_PLANCK_PR3_PEAK_EXTRACTION_RULE_V01_BUILT")


if __name__ == "__main__":
    main()
