# Tau CMB Acoustic Operator Dependency Unblock Plan v01

**Doc class:** acoustic operator dependency unblock plan
**Reader role:** Paper 13 CMB peak scoring path
**Status:** unblock plan declared; no dependency completed; score blocked
**Canonical parent:** Paper 13 CMB scoring input fulfillment chain

## Purpose

This artifact turns the failed minimal acoustic operator model attempt into an ordered dependency-unblock plan. It does not solve the operator. It identifies the exact artifacts that must be completed before a Planck peak score can be attempted.

## Summary

- unblock_rows_declared = 8
- critical_unblock_rows = 7
- completed_unblock_rows = 0
- pending_unblock_rows = 8
- operator_model_accepted_rows = 0
- executable_prediction_rows = 0
- score_ready_rows = 0
- overall_status = ACOUSTIC_OPERATOR_DEPENDENCY_UNBLOCK_PLAN_DECLARED_SCORE_BLOCKED
- next_required_artifact = tau_cmb_acoustic_domain_basis_lock_acceptance_v01

## Ordered Unblock Rows

| priority | component | required_unblock_artifact | unblock_status |
| --- | --- | --- | --- |
| 1 | domain_and_basis_lock | tau_cmb_acoustic_domain_basis_lock_acceptance_v01 | DECLARED_NOT_COMPLETED |
| 2 | effective_potential_input | tau_cmb_phi_tau_eff_acoustic_input_acceptance_v01 | DECLARED_NOT_COMPLETED |
| 3 | amplitude_input | tau_cmb_acoustic_amplitude_input_acceptance_v01 | DECLARED_NOT_COMPLETED |
| 4 | oscillator_kernel_rule | tau_cmb_acoustic_oscillator_kernel_acceptance_v01 | DECLARED_NOT_COMPLETED |
| 5 | baryon_loading_coupling | tau_cmb_acoustic_baryon_loading_coupling_acceptance_v01 | DECLARED_NOT_COMPLETED |
| 6 | projection_rule_to_peak_payload | tau_cmb_acoustic_peak_projection_payload_acceptance_v01 | DECLARED_NOT_COMPLETED |
| 7 | uncertainty_and_null_policy | tau_cmb_acoustic_uncertainty_or_null_policy_acceptance_v01 | DECLARED_NOT_COMPLETED |
| 8 | score_firewall | tau_cmb_acoustic_operator_score_entry_firewall_release_v01 | DECLARED_NOT_COMPLETED |

## Claim Boundary

tau_cmb_acoustic_operator_dependency_unblock_plan_v01_unblock_plan_only_no_operator_solution_no_peak_prediction_no_score_no_likelihood_no_verdict

This unblock plan does not solve the acoustic operator, does not derive an executable `S_tau_ac`, does not predict Planck peaks, does not compute a CMB score or likelihood, and does not decide whether a dark sector is needed.
