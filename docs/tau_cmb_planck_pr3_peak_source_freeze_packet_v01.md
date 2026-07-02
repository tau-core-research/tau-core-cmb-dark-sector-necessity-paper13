# Tau CMB Planck PR3 Peak Source Freeze Packet v01

**Doc class:** source-freeze packet
**Reader role:** Paper 13 CMB scoring input provenance
**Status:** artifact URLs selected; local download, hash, extraction, likelihood, and scoring are pending
**Canonical parent:** Paper 13 CMB scoring input fulfillment chain

## Purpose

This packet replaces an abstract CMB peak-data blocker with a concrete, official Planck PR3 source-family selection. It records which public ancillary products should seed the first endpoint-blind CMB peak extraction attempt.

It does not download or redistribute the raw Planck products. It does not extract peaks, compute a likelihood, compute a score, or permit any Tau-response or dark-sector verdict.

## Selected Official Artifacts

| artifact_id | role | source_product_class | release | status |
| --- | --- | --- | --- | --- |
| PLANCK_PR3_PEAKSRC_001 | primary_tt_peak_observable | cmb_power_spectrum_tt_binned | Planck PR3/R3.01 | DECLARED_NOT_EXECUTED |
| PLANCK_PR3_PEAKSRC_002 | polarization_cross_check | cmb_power_spectrum_te_binned | Planck PR3/R3.02 | DECLARED_NOT_EXECUTED |
| PLANCK_PR3_PEAKSRC_003 | polarization_peak_check | cmb_power_spectrum_ee_binned | Planck PR3/R3.02 | DECLARED_NOT_EXECUTED |
| PLANCK_PR3_PEAKSRC_004 | lcdm_reference_curve | cmb_minimum_theory_baseline | Planck PR3/R3.01 | DECLARED_NOT_EXECUTED |

## Freeze Result

- artifact_rows_declared = 4
- artifact_urls_selected = 4
- local_hashes_computed = 0
- extraction_rules_executed = 0
- score_ready = false
- score_entry_allowed_rows = 0
- overall_status = PLANCK_PR3_ARTIFACT_URLS_SELECTED_EXTRACTION_FREEZE_PENDING
- next_required_artifact = tau_cmb_planck_pr3_peak_extraction_rule_v01

## Claim Boundary

tau_cmb_planck_pr3_peak_source_freeze_packet_v01_source_freeze_only_no_download_no_extraction_no_score_no_likelihood_no_verdict

This is a source-selection bridge only. The next admissible step is a frozen extraction rule that can turn the selected TT/TE/EE products into a reproducible peak-observable table with hashes and uncertainty handling.
