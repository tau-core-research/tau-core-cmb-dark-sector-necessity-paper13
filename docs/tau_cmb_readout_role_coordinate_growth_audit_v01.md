# Tau CMB Readout Role Coordinate Growth Audit v01

**Doc class:** growth role-coordinate audit
**Status:** GROWTH_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED

## Claim Boundary

```text
tau_cmb_readout_role_coordinate_growth_audit_v01_audit_only_coordinate_not_accepted_no_growth_score_no_structure_match_no_concrete_R_CMB_no_carrier_certification_no_verdict
```

## Purpose

This audit checks whether the growth role-coordinate candidate has the expected
components, formal slots, dimension roles, dependency trace, block/guard
accounting, and promotion firewall. It does not accept the coordinate, compute
a growth score, match structure-growth data, materialize concrete `R_CMB`,
certify the carrier, or decide the dark-sector question.

## Audit Rows

- `coordinate_row_shape`: PASS_GROWTH_COORDINATE_ROWS_PRESENT | coordinate_components=['domain_specification', 'codomain_specification', 'time_scale_convention', 'operator_rule', 'cross_role_consistency', 'growth_stop_rule']
- `input_lensing_chain`: PASS_LENSING_AUDIT_CHAIN | growth coordinate follows a clean lensing coordinate audit and growth candidate summary
- `formal_slots_declared`: PASS_FORMAL_SLOTS_DECLARED | each growth coordinate component has a formal slot
- `dimension_roles_declared`: PASS_DIMENSION_ROLES_DECLARED | each growth coordinate component has a dimension/convention role
- `source_dependencies_declared`: PASS_SOURCE_DEPENDENCIES_DECLARED | each growth coordinate component is tied to an existing blocker/evidence artifact
- `block_guard_accounting`: PASS_BLOCK_GUARD_ACCOUNTING | blocked_count=2, guard_count=4
- `promotion_firewall`: PASS_GROWTH_COORDINATE_FIREWALL_CLOSED | coordinate acceptance, growth score, structure match, concrete R_CMB, carrier certification, and verdict permissions remain closed
- `domain_codomain_selection`: BLOCKED_DOMAIN_CODOMAIN_SELECTION_NOT_FIXED | domain and codomain families are declared but no endpoint-blind pair is selected
- `time_scale_numeric_convention`: BLOCKED_TIME_SCALE_CONVENTION_NOT_NUMERIC | k, scale-factor, epoch, and normalization convention are guarded but not numerically fixed
- `operator_rule`: BLOCKED_OPERATOR_RULE_NOT_DERIVED | Transfer_tau[X_tau_CMB](k,a) is not supplied as a lawful propagation rule
- `cross_role_consistency`: BLOCKED_DEPENDENT_ROLES_STILL_OPEN | density, acoustic, and lensing role coordinates remain blocked and unmaterialized

## Status

```text
GROWTH_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED
```

The growth coordinate is audit-visible but not materialized. It remains blocked
on fixing the endpoint-blind domain/codomain pair, fixing numeric time/scale
conventions, deriving `Transfer_tau[X_tau_CMB](k,a)`, and checking cross-role
consistency with the density, acoustic, and lensing coordinates.

## Next Minimal Unblock

```text
tau_cmb_readout_role_coordinate_radiation_v01
```
