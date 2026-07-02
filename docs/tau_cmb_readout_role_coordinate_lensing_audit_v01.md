# Tau CMB Readout Role Coordinate Lensing Audit v01

**Doc class:** lensing role-coordinate audit
**Status:** LENSING_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED

## Claim Boundary

```text
tau_cmb_readout_role_coordinate_lensing_audit_v01_audit_only_coordinate_not_accepted_no_lensing_score_no_act_planck_match_no_concrete_R_CMB_no_carrier_certification_no_verdict
```

## Purpose

This audit checks whether the lensing role-coordinate candidate has the
expected components, formal slots, dimension roles, dependency trace,
block/guard accounting, and promotion firewall. It does not accept the
coordinate, compute a lensing score, match ACT/Planck lensing data, materialize
concrete `R_CMB`, certify the carrier, or decide the dark-sector question.

## Audit Rows

- `coordinate_row_shape`: PASS_LENSING_COORDINATE_ROWS_PRESENT | coordinate_components=['lensing_potential_source', 'transfer_kernel', 'projection_geometry_guard', 'amplitude_shape_response', 'cross_readout_consistency', 'lensing_stop_rule']
- `input_density_chain`: PASS_DENSITY_AUDIT_CHAIN | lensing coordinate follows a clean density coordinate audit and lensing candidate summary
- `formal_slots_declared`: PASS_FORMAL_SLOTS_DECLARED | each lensing coordinate component has a formal slot
- `dimension_roles_declared`: PASS_DIMENSION_ROLES_DECLARED | each lensing coordinate component has a dimension/convention role
- `source_dependencies_declared`: PASS_SOURCE_DEPENDENCIES_DECLARED | each lensing coordinate component is tied to an existing blocker/evidence artifact
- `block_guard_accounting`: PASS_BLOCK_GUARD_ACCOUNTING | blocked_count=4, guard_count=2
- `promotion_firewall`: PASS_LENSING_COORDINATE_FIREWALL_CLOSED | coordinate acceptance, lensing score, ACT/Planck match, concrete R_CMB, carrier certification, and verdict permissions remain closed
- `potential_source`: BLOCKED_POTENTIAL_SOURCE_NOT_DERIVED | Phi_tau_eff(a,k) is declared only as a potential-source slot
- `transfer_kernel`: BLOCKED_TRANSFER_KERNEL_NOT_SPECIFIED | T_tau_CMB(k,a) is not specified with domain, codomain, convention, and normalization
- `amplitude_shape_response`: BLOCKED_AMPLITUDE_SHAPE_NOT_EVALUATED | no endpoint-blind lensing amplitude/shape response is evaluated
- `cross_readout_consistency`: BLOCKED_CROSS_READOUT_NOT_AVAILABLE | density and acoustic role coordinates remain blocked and unmaterialized

## Status

```text
LENSING_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED
```

The lensing coordinate is audit-visible but not materialized. It remains
blocked on deriving `Phi_tau_eff(a,k)`, specifying `T_tau_CMB(k,a)`, evaluating
endpoint-blind amplitude/shape response, and checking cross-readout
consistency with the acoustic and density coordinates.

## Next Minimal Unblock

```text
tau_cmb_readout_role_coordinate_growth_v01
```
