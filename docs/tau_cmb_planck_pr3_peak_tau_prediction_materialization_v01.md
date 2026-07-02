# Tau CMB Planck PR3 Peak Tau Prediction Materialization v01

**Doc class:** Tau-side prediction materialization specification
**Reader role:** Paper 13 CMB peak scoring path
**Status:** materialization contract ready; endpoint-blind Tau prediction payload missing; score blocked
**Canonical parent:** Paper 13 CMB scoring input fulfillment chain

## Purpose

This artifact converts the previous score blocker into an explicit Tau-side payload contract. It states, row by row, what an endpoint-blind Tau acoustic prediction must provide before a Planck PR3 peak score can be attempted.

It does not supply the prediction. It prevents the pipeline from treating a missing Tau response as a CMB failure, a likelihood result, or a dark-sector verdict.

## Acceptance Rule

A score entry is allowed only when every observed peak candidate has either a matching endpoint-blind Tau prediction or an accepted null-response control with locked spectrum role, normalization convention, predicted peak position/value, uncertainty model, and derivation provenance.

## Summary

- materialization_rows_declared = 36
- required_tau_payload_rows = 36
- tau_prediction_value_rows = 0
- tau_prediction_ell_rows = 0
- endpoint_blind_attestation_rows = 0
- accepted_materialization_rows = 0
- score_ready_rows = 0
- missing_prediction_rows = 36
- overall_status = TAU_PEAK_PREDICTION_MATERIALIZATION_SPEC_READY_PAYLOAD_MISSING_SCORE_BLOCKED
- next_required_artifact = tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_v01

## First Rows

| materialization_row_id | candidate_id | spectrum | ell_center | materialization_acceptance_status | score_blocker |
| --- | --- | --- | --- | --- | --- |
| TCMBP3PTPM01_001 | TCMBP3PSC01_001 | TT | 225.164945 | BLOCKED_TAU_PREDICTION_PAYLOAD_NOT_MATERIALIZED | ENDPOINT_BLIND_TAU_PEAK_PREDICTION_PAYLOAD_MISSING |
| TCMBP3PTPM01_002 | TCMBP3PSC01_002 | TT | 524.785320 | BLOCKED_TAU_PREDICTION_PAYLOAD_NOT_MATERIALIZED | ENDPOINT_BLIND_TAU_PEAK_PREDICTION_PAYLOAD_MISSING |
| TCMBP3PTPM01_003 | TCMBP3PSC01_003 | TT | 824.681596 | BLOCKED_TAU_PREDICTION_PAYLOAD_NOT_MATERIALIZED | ENDPOINT_BLIND_TAU_PEAK_PREDICTION_PAYLOAD_MISSING |
| TCMBP3PTPM01_004 | TCMBP3PSC01_004 | TT | 1124.633180 | BLOCKED_TAU_PREDICTION_PAYLOAD_NOT_MATERIALIZED | ENDPOINT_BLIND_TAU_PEAK_PREDICTION_PAYLOAD_MISSING |
| TCMBP3PTPM01_005 | TCMBP3PSC01_005 | TT | 1424.605140 | BLOCKED_TAU_PREDICTION_PAYLOAD_NOT_MATERIALIZED | ENDPOINT_BLIND_TAU_PEAK_PREDICTION_PAYLOAD_MISSING |
| TCMBP3PTPM01_006 | TCMBP3PSC01_006 | TT | 1724.586860 | BLOCKED_TAU_PREDICTION_PAYLOAD_NOT_MATERIALIZED | ENDPOINT_BLIND_TAU_PEAK_PREDICTION_PAYLOAD_MISSING |
| TCMBP3PTPM01_007 | TCMBP3PSC01_007 | TT | 1994.575100 | BLOCKED_TAU_PREDICTION_PAYLOAD_NOT_MATERIALIZED | ENDPOINT_BLIND_TAU_PEAK_PREDICTION_PAYLOAD_MISSING |
| TCMBP3PTPM01_008 | TCMBP3PSC01_008 | TT | 2294.565290 | BLOCKED_TAU_PREDICTION_PAYLOAD_NOT_MATERIALIZED | ENDPOINT_BLIND_TAU_PEAK_PREDICTION_PAYLOAD_MISSING |

## Claim Boundary

tau_cmb_planck_pr3_peak_tau_prediction_materialization_v01_materialization_spec_only_no_tau_prediction_no_score_no_likelihood_no_dark_sector_verdict

This is a materialization specification only. It is not a Tau acoustic prediction, not a CMB score, not a likelihood comparison, and not a decision about whether a dark sector is needed.
