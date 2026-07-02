# Tau CMB Planck PR3 Peak Score Attempt Guard v01

**Doc class:** score-attempt guard
**Reader role:** Paper 13 CMB peak scoring path
**Status:** observed side ready; Tau-side response missing; score attempt blocked
**Canonical parent:** Paper 13 CMB scoring input fulfillment chain

## Summary

- guard_rows_declared = 3
- guard_pass_rows = 1
- guard_block_rows = 2
- observed_side_ready = true
- tau_side_response_ready = false
- score_attempt_allowed = false
- overall_status = PLANCK_PR3_PEAK_SCORE_ATTEMPT_BLOCKED_TAU_SIDE_RESPONSE_MISSING
- next_required_artifact = tau_cmb_planck_pr3_peak_tau_prediction_materialization_v01

## Guard Rows

| guard_component | observed_status | guard_decision |
| --- | --- | --- |
| observed_peak_candidate_table | PASS_OBSERVED_SIDE_READY | GUARD_PASSED |
| tau_side_prediction_or_null_response | BLOCKED_TAU_SIDE_RESPONSE_MISSING | SCORE_ATTEMPT_BLOCKED |
| score_entry_integrity | BLOCKED_SCORE_READY_ROWS_ZERO | SCORE_ATTEMPT_BLOCKED |

## Claim Boundary

tau_cmb_planck_pr3_peak_score_attempt_guard_v01_guard_only_score_blocked_no_likelihood_no_tau_response_claim_no_dark_sector_verdict

This guard computes no score and reads no CMB likelihood. It only states that the Planck PR3 observed peak input is ready while the Tau-side prediction/null-response half is not ready.
