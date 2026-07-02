# Tau CMB Acoustic Tau Prediction Source Derivation v01

**Doc class:** acoustic Tau prediction source derivation spine
**Reader role:** Paper 13 CMB peak scoring path
**Status:** formal source target declared; source/operator not derived; score blocked
**Canonical parent:** Paper 13 CMB scoring input fulfillment chain

## Purpose

This artifact consolidates the acoustic Tau-side blocker into one derivation spine. It declares the minimal source target needed before the Planck PR3 peak payload can be populated:

```text
S_tau_ac(k,a) := P_ac[Phi_tau_eff,A_tau,Theta_tau_ac,C_rec](k,a)
```

`P_ac` is not supplied here. The equation is a target definition for the required source/operator payload, not a physical CMB solution.

## Summary

- derivation_rows_declared = 8
- formal_definition_rows = 1
- missing_dependency_rows = 6
- derived_source_rows = 0
- executable_prediction_rows = 0
- accepted_planck_payload_rows = 0
- score_ready_rows = 0
- overall_status = ACOUSTIC_TAU_PREDICTION_SOURCE_DERIVATION_SPINE_DECLARED_SOURCE_NOT_DERIVED_SCORE_BLOCKED
- next_required_artifact = tau_cmb_acoustic_source_operator_payload_v01

## Derivation Spine

| component | symbolic_object | derivation_status | planck_peak_payload_effect |
| --- | --- | --- | --- |
| formal_acoustic_source_target | S_tau_ac(k,a) | FORMAL_DEFINITION_ONLY_NOT_DERIVED | does_not_accept_planck_peak_payload |
| effective_potential_dependency | Phi_tau_eff(a,k) | BLOCKED_EFFECTIVE_POTENTIAL_NOT_DERIVED | blocks_predicted_peak_position_and_value |
| amplitude_dependency | A_tau(a,k) | BLOCKED_AMPLITUDE_NOT_DERIVED | blocks_predicted_observable_amplitude |
| oscillator_response_dependency | Theta_tau_ac(k,a) | BLOCKED_OSCILLATOR_RESPONSE_NOT_DERIVED | blocks_peak_phase_prediction |
| baryon_loading_dependency | B_tau_gamma_b(k,a) | BLOCKED_BARYON_LOADING_COUPLING_NOT_DERIVED | blocks_relative_peak_height_prediction |
| planck_peak_payload_handoff | P_tau_peak_payload | BLOCKED_NO_ACCEPTED_TAU_PEAK_PAYLOAD | keeps_all_36_peak_rows_rejected |
| null_response_control_dependency | N_tau_ac_null | BLOCKED_NO_ACCEPTED_NULL_RESPONSE_CONTROL | cannot_unblock_score_as_null_control |
| score_firewall | score(P_tau_peak_payload,Planck_PR3_peaks) | FIREWALL_CLOSED | prevents_dark_sector_verdict |

## Claim Boundary

tau_cmb_acoustic_tau_prediction_source_derivation_v01_derivation_spine_only_no_acoustic_source_solution_no_peak_prediction_no_score_no_likelihood_no_verdict

This is a derivation spine only. It does not derive an acoustic source, does not solve photon-baryon dynamics, does not predict Planck peak positions or amplitudes, does not compute a score or likelihood, and does not decide whether a dark sector is needed.
