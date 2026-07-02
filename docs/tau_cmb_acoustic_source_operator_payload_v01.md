# Tau CMB Acoustic Source Operator Payload v01

**Doc class:** acoustic source-operator payload contract
**Reader role:** Paper 13 CMB peak scoring path
**Status:** operator payload contract declared; no operator payload accepted; score blocked
**Canonical parent:** Paper 13 CMB scoring input fulfillment chain

## Purpose

This artifact turns the formal `P_ac` slot into a concrete operator-payload contract. It specifies the rows that must be supplied before `S_tau_ac(k,a)` can become an executable Tau-side acoustic source for Planck PR3 peak prediction.

No operator solution is supplied here.

## Summary

- operator_rows_declared = 8
- required_operator_payload_rows = 7
- payload_supplied_rows = 0
- payload_accepted_rows = 0
- derived_source_rows = 0
- executable_prediction_rows = 0
- accepted_planck_payload_rows = 0
- score_ready_rows = 0
- overall_status = ACOUSTIC_SOURCE_OPERATOR_PAYLOAD_CONTRACT_DECLARED_PAYLOAD_NOT_SUPPLIED_SCORE_BLOCKED
- next_required_artifact = tau_cmb_acoustic_source_operator_payload_supply_v01

## Operator Payload Rows

| component | symbolic_slot | payload_status | acceptance_decision |
| --- | --- | --- | --- |
| domain_and_basis_lock | Dom(P_ac) | REQUIRED_NOT_SUPPLIED | REJECTED_OPERATOR_PAYLOAD_ROW_NOT_SUPPLIED |
| effective_potential_input | Phi_tau_eff(a,k) | REQUIRED_NOT_SUPPLIED | REJECTED_OPERATOR_PAYLOAD_ROW_NOT_SUPPLIED |
| amplitude_input | A_tau(a,k) | REQUIRED_NOT_SUPPLIED | REJECTED_OPERATOR_PAYLOAD_ROW_NOT_SUPPLIED |
| oscillator_kernel_rule | G_tau_ac(k,a;a_rec) | REQUIRED_NOT_SUPPLIED | REJECTED_OPERATOR_PAYLOAD_ROW_NOT_SUPPLIED |
| baryon_loading_coupling | C_tau_gamma_b(k,a) | REQUIRED_NOT_SUPPLIED | REJECTED_OPERATOR_PAYLOAD_ROW_NOT_SUPPLIED |
| projection_rule_to_peak_payload | Pi_peak[P_ac] | REQUIRED_NOT_SUPPLIED | REJECTED_OPERATOR_PAYLOAD_ROW_NOT_SUPPLIED |
| uncertainty_and_null_policy | sigma_tau_ac or N_tau_ac_null | REQUIRED_NOT_SUPPLIED | REJECTED_OPERATOR_PAYLOAD_ROW_NOT_SUPPLIED |
| score_firewall | score_guard(P_ac) | FIREWALL_DECLARED | REJECTED_OPERATOR_PAYLOAD_ROW_NOT_SUPPLIED |

## Claim Boundary

tau_cmb_acoustic_source_operator_payload_v01_operator_payload_contract_only_no_operator_solution_no_peak_prediction_no_score_no_likelihood_no_verdict

This is an operator-payload contract only. It does not solve the acoustic operator, does not derive `S_tau_ac`, does not predict Planck peaks, does not compute a CMB score or likelihood, and does not decide whether a dark sector is needed.
