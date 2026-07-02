# Tau CMB Phi Tau Parent Real Score-Ready Input Supply Contract v01

**Doc class:** real score-ready input supply contract
**Status:** unlock contract declared; no real score-ready input supplied

This artifact consumes the route-completion certificate and declares the
materials required to unlock the null-response locked route. It does not supply
those materials. It therefore keeps the scoring route locked.

Required materials per row:

```text
phi_tau_eff_source
dimension_replay
normalization_binding
endpoint_blind_provenance
cmb_readout_mapping
likelihood_adapter
acceptance_replay
```

Summary:

```text
route_completed_rows=7
null_response_locked_rows=7
required_materials_total=49
supplied_materials_total=0
real_score_ready_input_supplied_rows=0
scoring_input_accepted_rows=0
reopen_scoring_route_allowed_now_rows=0
score_attempt_blocked_now_rows=7
```

## Claim Boundary

This artifact declares the unlock contract only. It supplies no real score-ready
input, accepts no scoring input, derives no `Phi_tau_eff`, computes no score,
supplies no CMB likelihood, and permits no no-dark or dark-sector verdict.
