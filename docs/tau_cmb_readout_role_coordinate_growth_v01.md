# Tau CMB Readout Role Coordinate Growth v01

**Doc class:** growth role-coordinate candidate
**Status:** GROWTH_ROLE_COORDINATE_CANDIDATE_DECLARED_BLOCKED_NOT_MATERIALIZED

## Claim Boundary

```text
tau_cmb_readout_role_coordinate_growth_v01_coordinate_candidate_only_not_materialized_no_growth_score_no_structure_match_no_concrete_R_CMB_no_carrier_certification_no_verdict
```

## Purpose

This artifact declares the candidate components of the growth readout role
coordinate `e_growth`. It is not a growth score, not a structure-growth match,
not a CMB likelihood, not a concrete `R_CMB` map, and not evidence for a
dark-sector verdict.

## Coordinate Rows

- `TCMBRRCG01_001` `domain_specification`: PARTIAL_DOMAIN_GUARD_DECLARED_NOT_SELECTED | `X_tau_CMB or (rho_tau_eff,Phi_tau_eff)`
- `TCMBRRCG01_002` `codomain_specification`: PARTIAL_CODOMAIN_GUARD_DECLARED_NOT_SELECTED | `Y_growth_tau(k,a)`
- `TCMBRRCG01_003` `time_scale_convention`: CONDITIONAL_TIME_SCALE_GUARD_DECLARED_NOT_NUMERIC | `K_growth[k,a_initial,a_final,N_growth]`
- `TCMBRRCG01_004` `operator_rule`: BLOCKED_OPERATOR_RULE_NOT_DERIVED | `Transfer_tau[X_tau_CMB](k,a)`
- `TCMBRRCG01_005` `cross_role_consistency`: BLOCKED_DEPENDENT_ROLES_STILL_OPEN | `Consistent(T_tau_CMB,e_density,e_acoustic,e_lensing)`
- `TCMBRRCG01_006` `growth_stop_rule`: STOP_RULE_DECLARED_NOT_TRIGGERED | `growth_fail_if_transfer_operator_or_consistency_missing`

## Status

```text
GROWTH_ROLE_COORDINATE_CANDIDATE_DECLARED_BLOCKED_NOT_MATERIALIZED
```

The growth coordinate is explicit as a blocked role-coordinate candidate. It
remains unmaterialized because no endpoint-blind domain/codomain selection,
numeric time/scale convention, lawful transfer operator, or cross-role
consistency proof is supplied in score-ready form.

## Next Minimal Unblock

```text
tau_cmb_readout_role_coordinate_growth_audit_v01
```
