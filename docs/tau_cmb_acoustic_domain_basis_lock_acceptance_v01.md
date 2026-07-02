# Tau CMB Acoustic Domain Basis Lock Acceptance v01

**Doc class:** acoustic domain/basis lock acceptance
**Reader role:** Paper 13 CMB peak scoring path
**Status:** domain/basis conventions accepted; score blocked
**Canonical parent:** Paper 13 CMB scoring input fulfillment chain

## Purpose

This artifact closes the first acoustic-operator dependency row: the domain and basis convention for `P_ac`. It locks the reduced coordinates and comparison boundary needed before `Phi_tau_eff`, `A_tau`, oscillator-kernel, coupling, and peak-projection rows can be assessed.

It is a convention lock only. It does not solve the acoustic operator and does not create a Tau prediction.

## Summary

- lock_rows_declared = 7
- lock_rows_accepted = 7
- endpoint_blind_pass_rows = 7
- dimension_convention_locked_rows = 7
- domain_basis_lock_accepted = true
- operator_model_accepted_rows = 1
- executable_prediction_rows = 0
- score_ready_rows = 0
- overall_status = ACOUSTIC_DOMAIN_BASIS_LOCK_ACCEPTED_SCORE_BLOCKED
- next_required_artifact = tau_cmb_phi_tau_eff_acoustic_input_acceptance_v01

## Accepted Lock Rows

| component | symbol_or_role | acceptance_decision |
| --- | --- | --- |
| wavenumber_domain | k | ACCEPTED_DOMAIN_BASIS_LOCK_ROW |
| scale_readout_domain | a | ACCEPTED_DOMAIN_BASIS_LOCK_ROW |
| recombination_readout_slice | a_rec | ACCEPTED_DOMAIN_BASIS_LOCK_ROW |
| angular_peak_coordinate | ell | ACCEPTED_DOMAIN_BASIS_LOCK_ROW |
| integration_measure_placeholder | da | ACCEPTED_DOMAIN_BASIS_LOCK_ROW |
| spectrum_role_basis | spectrum_role in {TT,TE,EE} | ACCEPTED_DOMAIN_BASIS_LOCK_ROW |
| comparison_boundary | endpoint_blind_peak_comparison | ACCEPTED_DOMAIN_BASIS_LOCK_ROW |

## Claim Boundary

tau_cmb_acoustic_domain_basis_lock_acceptance_v01_convention_lock_only_no_operator_solution_no_peak_prediction_no_score_no_likelihood_no_verdict

This convention lock does not solve the acoustic operator, does not derive an executable `S_tau_ac`, does not predict Planck peaks, does not compute a CMB score or likelihood, and does not decide whether a dark sector is needed.
