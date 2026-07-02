# Tau CMB Planck PR3 Peak Scoring Input Candidate v01

**Doc class:** observed-side scoring input candidate
**Reader role:** Paper 13 CMB peak scoring path
**Status:** observed Planck PR3 peak inputs ready; Tau prediction/null-response missing; score blocked
**Canonical parent:** Paper 13 CMB scoring input fulfillment chain

## Purpose

This artifact converts the Planck PR3 TT/TE/EE peak-observable table into a scoring-input candidate for the acoustic peak phase/height role.

It fills the observed side of the comparison. It does not supply a Tau-side prediction, null response, likelihood, score, or verdict.

## Candidate Summary

- candidate_rows_declared = 36
- observed_side_ready_rows = 36
- comparison_rule_declared_rows = 36
- tau_prediction_required_rows = 36
- tau_prediction_supplied_rows = 0
- null_response_supplied_rows = 0
- score_ready_rows = 0
- observed_side_fulfillment_score = 1.000000
- overall_status = OBSERVED_PEAK_SCORING_INPUT_CANDIDATE_READY_TAU_PREDICTION_MISSING_SCORE_BLOCKED
- next_required_artifact = tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_v01

## First Candidate Rows

| candidate_id | source_peak_id | spectrum | ell_center | observed_value | score_blocker |
| --- | --- | --- | ---: | ---: | --- |
| TCMBP3PSC01_001 | TT_PEAK_01 | TT | 225.164945 | 5793.43954 | TAU_PREDICTION_OR_NULL_RESPONSE_NOT_SUPPLIED |
| TCMBP3PSC01_002 | TT_PEAK_02 | TT | 524.785320 | 2573.4805 | TAU_PREDICTION_OR_NULL_RESPONSE_NOT_SUPPLIED |
| TCMBP3PSC01_003 | TT_PEAK_03 | TT | 824.681596 | 2521.9126 | TAU_PREDICTION_OR_NULL_RESPONSE_NOT_SUPPLIED |
| TCMBP3PSC01_004 | TT_PEAK_04 | TT | 1124.633180 | 1231.87224 | TAU_PREDICTION_OR_NULL_RESPONSE_NOT_SUPPLIED |
| TCMBP3PSC01_005 | TT_PEAK_05 | TT | 1424.605140 | 809.057064 | TAU_PREDICTION_OR_NULL_RESPONSE_NOT_SUPPLIED |
| TCMBP3PSC01_006 | TT_PEAK_06 | TT | 1724.586860 | 397.735803 | TAU_PREDICTION_OR_NULL_RESPONSE_NOT_SUPPLIED |
| TCMBP3PSC01_007 | TT_PEAK_07 | TT | 1994.575100 | 234.658998 | TAU_PREDICTION_OR_NULL_RESPONSE_NOT_SUPPLIED |
| TCMBP3PSC01_008 | TT_PEAK_08 | TT | 2294.565290 | 117.768892 | TAU_PREDICTION_OR_NULL_RESPONSE_NOT_SUPPLIED |

## Claim Boundary

tau_cmb_planck_pr3_peak_scoring_input_candidate_v01_observed_side_candidate_only_no_tau_prediction_no_score_no_likelihood_no_dark_sector_verdict

This is a protocol-readiness artifact. The observed side is complete, but no Tau-side acoustic prediction or null response has been supplied, so scoring remains blocked.
