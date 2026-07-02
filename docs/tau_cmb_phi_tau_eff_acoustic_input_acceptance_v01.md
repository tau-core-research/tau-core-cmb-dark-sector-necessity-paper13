# Tau CMB Phi Tau Eff Acoustic Input Acceptance v01

**Doc class:** Phi_tau_eff acoustic input acceptance audit
**Reader role:** Paper 13 CMB peak scoring path
**Status:** source-slot identity accepted; full acoustic input blocked; score blocked
**Canonical parent:** Paper 13 CMB scoring input fulfillment chain

## Purpose

This artifact audits whether `Phi_tau_eff(a,k)` can be accepted as the effective-potential input for the acoustic operator after the domain/basis lock. The source-slot identity is accepted, but the full acoustic input is not accepted because endpoint-blind provenance, normalization, timing/sign, and baryon-photon coupling remain unresolved.

## Summary

- acceptance_rows_declared = 6
- accepted_rows = 1
- blocked_rows = 3
- partial_rows = 1
- phi_tau_eff_source_slot_accepted = true
- phi_tau_eff_acoustic_input_accepted = false
- operator_model_accepted_rows = 1
- executable_prediction_rows = 0
- score_ready_rows = 0
- overall_status = PHI_TAU_EFF_ACOUSTIC_INPUT_IDENTITY_ACCEPTED_INPUT_BLOCKED_SCORE_BLOCKED
- next_required_artifact = tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_v01

## Acceptance Rows

| component | symbol_or_role | acceptance_status |
| --- | --- | --- |
| source_slot_identity | Phi_tau_eff(a,k) | ACCEPTED_SOURCE_SLOT_IDENTITY_ONLY |
| endpoint_blind_provenance | provenance(Phi_tau_eff) | BLOCKED_ENDPOINT_BLIND_PROVENANCE_NOT_ACCEPTED |
| normalization_convention | norm(Phi_tau_eff) | PARTIAL_NORMALIZATION_DECLARED_NOT_ACCEPTED |
| timing_sign_convention | time/sign(Phi_tau_eff) | BLOCKED_TIMING_SIGN_NOT_ACCEPTED |
| baryon_photon_coupling_role | coupling(Phi_tau_eff, baryon-photon response) | BLOCKED_COUPLING_ROLE_NOT_ACCEPTED |
| score_firewall | score_guard(Phi_tau_eff acoustic input) | FIREWALL_PRESERVED |

## Claim Boundary

tau_cmb_phi_tau_eff_acoustic_input_acceptance_v01_acceptance_audit_only_no_accepted_effective_potential_no_operator_solution_no_peak_prediction_no_score_no_likelihood_no_verdict

This acceptance audit does not accept an executable effective potential, does not solve the acoustic operator, does not derive an executable `S_tau_ac`, does not predict Planck peaks, does not compute a CMB score or likelihood, and does not decide whether a dark sector is needed.
