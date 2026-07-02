# Tau CMB Planck PR3 Peak Extraction Rule v01

**Doc class:** observable extraction rule
**Reader role:** Paper 13 CMB scoring input provenance
**Status:** official PR3 artifacts downloaded to gitignored cache; hashes and peak-observable table materialized; scoring remains blocked
**Canonical parent:** Paper 13 CMB scoring input fulfillment chain

## Rule

- Parse binned TT/TE/EE spectra as `l, Dl, -dDl, +dDl, BestFit`.
- For TT and EE, accept a local positive peak when `Dl_i > Dl_{i-1}` and `Dl_i >= Dl_{i+1}`.
- For TE, accept a signed extremum when `abs(Dl_i) > abs(Dl_{i-1})` and `abs(Dl_i) >= abs(Dl_{i+1})`.
- Retain the signed measured value, uncertainty columns, best-fit value, and measured-minus-best-fit residual.
- The baseline minimum-theory file is downloaded and hashed as a known-limit reference, but no theory-curve fitting is performed in this artifact.

## Receipt Summary

| spectrum | status | bytes | sha256 prefix |
| --- | --- | ---: | --- |
| TT | DOWNLOADED_TO_GITIGNORED_EXTERNAL_CACHE | 7143 | ed2b8b51b033e668 |
| TE | DOWNLOADED_TO_GITIGNORED_EXTERNAL_CACHE | 5698 | 191a588f9000885e |
| EE | DOWNLOADED_TO_GITIGNORED_EXTERNAL_CACHE | 5698 | bd30fc1121c0d1c2 |
| MINIMUM_THEORY | DOWNLOADED_TO_GITIGNORED_EXTERNAL_CACHE | 205647 | 50eecd4422e22026 |

## Extraction Result

- peak_rows_extracted = 36
- tt_peak_rows = 10
- te_extremum_rows = 13
- ee_peak_rows = 13
- parser_rule_frozen = true
- observable_table_materialized = true
- score_ready = false
- overall_status = PLANCK_PR3_PEAK_OBSERVABLE_TABLE_MATERIALIZED_SCORING_STILL_BLOCKED
- next_required_artifact = tau_cmb_planck_pr3_peak_scoring_input_candidate_v01

## First Extracted Rows

| peak_id | ell_center | D_ell | best_fit_D_ell | data_minus_bestfit |
| --- | ---: | ---: | ---: | ---: |
| TT_PEAK_01 | 225.164945 | 5793.43954 | 5726.93135 | 66.50819 |
| TT_PEAK_02 | 524.785320 | 2573.4805 | 2571.44487 | 2.03563 |
| TT_PEAK_03 | 824.681596 | 2521.9126 | 2522.77302 | -0.86042 |
| TT_PEAK_04 | 1124.633180 | 1231.87224 | 1238.5879 | -6.71566 |
| TT_PEAK_05 | 1424.605140 | 809.057064 | 816.784389 | -7.727325 |
| TT_PEAK_06 | 1724.586860 | 397.735803 | 397.391812 | 0.343991 |
| TT_PEAK_07 | 1994.575100 | 234.658998 | 231.209089 | 3.449909 |
| TT_PEAK_08 | 2294.565290 | 117.768892 | 115.70577 | 2.063122 |

## Claim Boundary

tau_cmb_planck_pr3_peak_extraction_rule_v01_observable_extraction_only_no_tau_prediction_no_likelihood_no_score_no_dark_sector_verdict

This artifact only materializes a reproducible observed-feature table from official Planck PR3 products. It does not compare Tau Core predictions to the table, does not run a CMB likelihood, and does not decide whether a dark-sector-like Tau response is necessary.
