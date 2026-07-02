# Tau CMB Readout Role Coordinate Radiation v01

**Doc class:** radiation role-coordinate candidate
**Status:** RADIATION_ROLE_COORDINATE_CANDIDATE_DECLARED_BLOCKED_NOT_MATERIALIZED

## Claim Boundary

```text
tau_cmb_readout_role_coordinate_radiation_v01_coordinate_candidate_only_not_materialized_no_radiation_score_no_neff_bound_eval_no_concrete_R_CMB_no_carrier_certification_no_verdict
```

## Purpose

This artifact declares the candidate components of the radiation/damping-tail
readout role coordinate `e_radiation`. It is not a radiation score, not a
numerical `Delta_N_eff` bound evaluation, not a CMB likelihood, not a concrete
`R_CMB` map, and not evidence for a dark-sector verdict.

## Coordinate Rows

- `TCMBRRCR01_001` `tau_radiation_like_contribution`: BLOCKED_TAU_DELTA_NEFF_NOT_DERIVED | `Delta_N_eff_tau`
- `TCMBRRCR01_002` `external_bound_convention`: CONDITIONAL_BOUND_CONVENTION_GUARD_DECLARED_NOT_NUMERIC | `Delta_N_eff_bound`
- `TCMBRRCR01_003` `damping_tail_inequality`: BLOCKED_BOUND_INEQUALITY_NOT_EVALUATED | `Delta_N_eff_tau <= Delta_N_eff_bound`
- `TCMBRRCR01_004` `cross_role_consistency`: BLOCKED_DEPENDENT_ROLES_STILL_OPEN | `Consistent(Delta_N_eff_tau,A_tau,Phi_tau_eff,T_tau_CMB)`
- `TCMBRRCR01_005` `radiation_stop_rule`: STOP_RULE_DECLARED_NOT_TRIGGERED | `radiation_fail_if_delta_neff_missing_or_bound_violated`

## Status

```text
RADIATION_ROLE_COORDINATE_CANDIDATE_DECLARED_BLOCKED_NOT_MATERIALIZED
```

The radiation coordinate is explicit as a blocked role-coordinate candidate. It
remains unmaterialized because `Delta_N_eff_tau`, the selected external bound,
the damping-tail inequality, and cross-role consistency are not supplied in
score-ready form.

## Next Minimal Unblock

```text
tau_cmb_readout_role_coordinate_radiation_audit_v01
```
