# Tau CMB Readout Role Coordinate Radiation Audit v01

**Doc class:** radiation role-coordinate audit
**Status:** RADIATION_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED

## Claim Boundary

```text
tau_cmb_readout_role_coordinate_radiation_audit_v01_audit_only_coordinate_not_accepted_no_radiation_score_no_neff_bound_eval_no_concrete_R_CMB_no_carrier_certification_no_verdict
```

## Purpose

This audit checks whether the radiation role-coordinate candidate has the
expected components, formal slots, dimension roles, dependency trace,
block/guard accounting, and promotion firewall. It does not accept the
coordinate, compute a radiation score, evaluate a numerical `Delta_N_eff`
bound, materialize concrete `R_CMB`, certify the carrier, or decide the
dark-sector question.

## Audit Rows

- `coordinate_row_shape`: PASS_RADIATION_COORDINATE_ROWS_PRESENT | coordinate_components=['tau_radiation_like_contribution', 'external_bound_convention', 'damping_tail_inequality', 'cross_role_consistency', 'radiation_stop_rule']
- `input_growth_chain`: PASS_GROWTH_AUDIT_CHAIN | radiation coordinate follows a clean growth coordinate audit and radiation candidate summary
- `formal_slots_declared`: PASS_FORMAL_SLOTS_DECLARED | each radiation coordinate component has a formal slot
- `dimension_roles_declared`: PASS_DIMENSION_ROLES_DECLARED | each radiation coordinate component has a dimension/convention role
- `source_dependencies_declared`: PASS_SOURCE_DEPENDENCIES_DECLARED | each radiation coordinate component is tied to an existing blocker/evidence artifact
- `block_guard_accounting`: PASS_BLOCK_GUARD_ACCOUNTING | blocked_count=3, guard_count=2
- `promotion_firewall`: PASS_RADIATION_COORDINATE_FIREWALL_CLOSED | coordinate acceptance, radiation score, Neff bound evaluation, concrete R_CMB, carrier certification, and verdict permissions remain closed
- `tau_radiation_like_contribution`: BLOCKED_TAU_DELTA_NEFF_NOT_DERIVED | Delta_N_eff_tau is declared only as a dimensionless contribution slot
- `damping_tail_inequality`: BLOCKED_BOUND_INEQUALITY_NOT_EVALUATED | Delta_N_eff_tau <= Delta_N_eff_bound is declared but not numerically evaluated
- `cross_role_consistency`: BLOCKED_DEPENDENT_ROLES_STILL_OPEN | density, acoustic, lensing, and growth role coordinates remain blocked and unmaterialized

## Status

```text
RADIATION_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED
```

The radiation coordinate is audit-visible but not materialized. It remains
blocked on deriving `Delta_N_eff_tau`, evaluating the damping-tail inequality
under a selected external bound, and checking cross-role consistency with the
density, acoustic, lensing, and growth coordinates.

## Next Minimal Unblock

```text
tau_cmb_readout_role_coordinate_null_v01
```
