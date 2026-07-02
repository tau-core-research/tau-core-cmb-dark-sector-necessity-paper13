# Tau CMB Readout Role Coordinate Density Audit v01

**Doc class:** density role-coordinate audit
**Status:** DENSITY_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED

## Claim Boundary

```text
tau_cmb_readout_role_coordinate_density_audit_v01_audit_only_coordinate_not_accepted_no_density_score_no_omega_c_h2_match_no_concrete_R_CMB_no_carrier_certification_no_verdict
```

## Purpose

This audit checks whether the density role-coordinate candidate has the
expected components, formal slots, dimension roles, dependency trace,
block/guard accounting, and promotion firewall. It does not accept the
coordinate, compute a density score, match `Omega_c h^2`, materialize concrete
`R_CMB`, certify the carrier, or decide the dark-sector question.

## Audit Rows

- `coordinate_row_shape`: PASS_DENSITY_COORDINATE_ROWS_PRESENT | coordinate_components=['density_ratio_guard', 'tau_effective_density', 'endpoint_blind_amplitude', 'omega_c_h2_role_comparison', 'density_stop_rule']
- `input_acoustic_chain`: PASS_ACOUSTIC_AUDIT_CHAIN | density coordinate follows a clean acoustic coordinate audit and density candidate summary
- `formal_slots_declared`: PASS_FORMAL_SLOTS_DECLARED | each density coordinate component has a formal slot
- `dimension_roles_declared`: PASS_DIMENSION_ROLES_DECLARED | each density coordinate component has a dimension/convention role
- `source_dependencies_declared`: PASS_SOURCE_DEPENDENCIES_DECLARED | each density coordinate component is tied to an existing blocker/evidence artifact
- `block_guard_accounting`: PASS_BLOCK_GUARD_ACCOUNTING | blocked_count=3, guard_count=2
- `promotion_firewall`: PASS_DENSITY_COORDINATE_FIREWALL_CLOSED | coordinate acceptance, density score, Omega_c h^2 match, concrete R_CMB, carrier certification, and verdict permissions remain closed
- `density_formula`: BLOCKED_DENSITY_FORMULA_NOT_DERIVED | rho_tau_eff(a,k) is declared only as a source slot
- `endpoint_blind_amplitude`: BLOCKED_ENDPOINT_BLIND_AMPLITUDE_MISSING | A_tau(a,k) is not yet proven independent of CMB residual fitting
- `omega_c_h2_comparison`: BLOCKED_NO_NUMERICAL_COMPARISON | no benchmark convention or numerical Omega_c h^2 comparison is supplied

## Status

```text
DENSITY_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED
```

The density coordinate is audit-visible but not materialized. It remains
blocked on deriving `rho_tau_eff(a,k)`, proving endpoint-blind `A_tau(a,k)`,
and supplying a numerical `Omega_c h^2` comparison under a declared benchmark
convention.

## Next Minimal Unblock

```text
tau_cmb_readout_role_coordinate_lensing_v01
```
