# Tau CMB Readout Role Coordinate Acoustic Audit v01

**Doc class:** acoustic role-coordinate audit
**Status:** ACOUSTIC_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED

## Claim Boundary

```text
tau_cmb_readout_role_coordinate_acoustic_audit_v01_audit_only_coordinate_not_accepted_no_acoustic_score_no_likelihood_no_concrete_R_CMB_no_carrier_certification_no_verdict
```

## Purpose

This audit checks whether the acoustic role-coordinate candidate has the
expected components, formal slots, dimension roles, dependency trace, and
promotion firewall. It does not accept the coordinate, compute an acoustic
score, materialize concrete `R_CMB`, certify the carrier, or decide the
dark-sector question.

## Audit Rows

- `coordinate_row_shape`: PASS_ACOUSTIC_COORDINATE_ROWS_PRESENT | coordinate_components=['potential_source_presence', 'phase_support', 'relative_peak_height', 'baryon_loading_coupling', 'scale_horizon_guard', 'failure_branch']
- `input_basis_chain`: PASS_BASIS_AUDIT_CHAIN | acoustic coordinate follows a clean role-space basis audit
- `formal_slots_declared`: PASS_FORMAL_SLOTS_DECLARED | each acoustic coordinate component has a formal slot
- `dimension_roles_declared`: PASS_DIMENSION_ROLES_DECLARED | each acoustic coordinate component has a dimension/convention role
- `source_dependencies_declared`: PASS_SOURCE_DEPENDENCIES_DECLARED | each acoustic coordinate component is tied to an existing blocker/evidence artifact
- `block_guard_accounting`: PASS_BLOCK_GUARD_ACCOUNTING | blocked_count=4, guard_count=2
- `promotion_firewall`: PASS_ACOUSTIC_COORDINATE_FIREWALL_CLOSED | coordinate acceptance, acoustic score, concrete R_CMB, carrier certification, and verdict permissions remain closed
- `source_materialization`: BLOCKED_SOURCE_NOT_DERIVED | pre-recombination Tau potential/source handoff is not derived
- `oscillator_response`: BLOCKED_OSCILLATOR_RESPONSE_NOT_EVALUATED | photon-baryon oscillator response is not evaluated for the Tau source
- `amplitude_and_coupling`: BLOCKED_AMPLITUDE_AND_COUPLING_NOT_SUPPLIED | endpoint-blind amplitude and baryon-loading coupling sign are missing

## Status

```text
ACOUSTIC_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_MATERIALIZED
```

The acoustic coordinate is audit-visible but not materialized. It remains
blocked on the Tau pre-recombination source handoff, oscillator response,
endpoint-blind amplitude, and baryon-loading coupling sign.

## Next Minimal Unblock

```text
tau_cmb_readout_role_coordinate_density_v01
```
