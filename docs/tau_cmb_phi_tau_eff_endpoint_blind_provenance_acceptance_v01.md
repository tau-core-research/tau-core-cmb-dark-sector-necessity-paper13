# Tau CMB Phi Tau Eff Endpoint-Blind Provenance Acceptance v01

**Doc class:** Phi_tau_eff endpoint-blind provenance acceptance audit
**Reader role:** Paper 13 CMB peak scoring path
**Status:** endpoint-exclusion policy accepted; endpoint-blind provenance blocked; score blocked
**Canonical parent:** Paper 13 CMB scoring input fulfillment chain

## Purpose

This artifact audits whether `Phi_tau_eff(a,k)` has acceptable endpoint-blind provenance after the acoustic input audit. It accepts only the endpoint-exclusion policy. It does not accept a parent-side source construction because the parent-input manifest, parent-side content, derivation rule, and replay package are still missing.

## Summary

- provenance_acceptance_rows_declared = 6
- accepted_policy_rows = 1
- blocked_rows = 4
- partial_rows = 1
- endpoint_exclusion_rule_accepted = true
- endpoint_blind_provenance_accepted = false
- phi_tau_eff_acoustic_input_accepted = false
- score_ready_rows = 0
- overall_status = PHI_TAU_EFF_ENDPOINT_BLIND_PROVENANCE_POLICY_ACCEPTED_PROVENANCE_BLOCKED_SCORE_BLOCKED
- next_required_artifact = tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_v01

## Acceptance Rows

| component | symbol_or_role | acceptance_status |
| --- | --- | --- |
| endpoint_exclusion_rule | endpoint_blind_policy(Phi_tau_eff) | ACCEPTED_POLICY_ONLY_ENDPOINT_EXCLUSION_RULE |
| parent_input_manifest | manifest(parent_inputs -> Phi_tau_eff) | BLOCKED_PARENT_INPUT_MANIFEST_NOT_SUPPLIED |
| parent_side_content | base_field_state + seed + response_operator | BLOCKED_PARENT_SIDE_CONTENT_NOT_ACCEPTED |
| derivation_rule | D_tau[parent_inputs] -> Phi_tau_eff | BLOCKED_DERIVATION_RULE_NOT_SUPPLIED |
| audit_replay_package | replay(parent_inputs, D_tau, Phi_tau_eff) | BLOCKED_REPLAY_PACKAGE_NOT_SUPPLIED |
| failure_branch | explicit_fail(Phi_tau_eff provenance) | PARTIAL_FAILURE_BRANCH_PRESERVED |

## Claim Boundary

tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_v01_policy_only_no_accepted_provenance_no_phi_derivation_no_score_no_likelihood_no_verdict

This acceptance audit accepts the endpoint-exclusion policy only. It does not accept endpoint-blind provenance for `Phi_tau_eff`, does not derive a source, does not solve the acoustic operator, does not predict CMB peaks, does not compute a CMB score or likelihood, and does not decide whether a dark sector is needed.
