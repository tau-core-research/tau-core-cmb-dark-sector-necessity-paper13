# Tau CMB Readout Role Space Basis Audit v01

**Doc class:** CMB readout role-space basis audit
**Status:** CMB_READOUT_ROLE_SPACE_BASIS_AUDITED_BLOCKED_NOT_CERTIFIED

## Claim Boundary

```text
tau_cmb_readout_role_space_basis_audit_v01_audit_only_carrier_basis_not_certified_no_concrete_R_CMB_no_equivalence_proof_no_readout_evaluation_no_score_no_verdict
```

## Purpose

This audit checks whether the CMB readout role-space basis candidate has the
expected role slots, basis symbols, endpoint-firewall labels, dimension labels,
and null anchor. It does not certify the carrier, materialize concrete `R_CMB`,
prove equivalence, evaluate readout, enter scoring, or decide the dark-sector
question.

## Audit Rows

- `basis_row_shape`: PASS_ROLE_SLOTS_PRESENT | role_slots=['acoustic_phase_height', 'density_amplitude', 'lensing_potential', 'growth_transfer', 'radiation_damping_guard', 'null_readout']
- `input_obligation_chain`: PASS_AXIOM_OBLIGATION_CHAIN | basis candidate follows a clean equivalence axiom proof-obligation input
- `basis_symbols`: PASS_BASIS_SYMBOLS_DECLARED | basis_symbols=['e_acoustic', 'e_density', 'e_lensing', 'e_growth', 'e_radiation', 'e_null']
- `endpoint_firewall_labels`: PASS_FORBIDDEN_ENDPOINT_DEPENDENCIES_DECLARED | each role slot declares a forbidden endpoint-tuning dependency
- `dimension_role_labels`: PASS_DIMENSION_ROLES_DECLARED | each role slot has a dimension/unit role label
- `null_basis_anchor`: PASS_NULL_BASIS_ANCHOR_DECLARED | null readout basis anchor is declared from audited zero-control
- `promotion_firewall`: PASS_BASIS_PROMOTION_FIREWALL_CLOSED | carrier certification, concrete R_CMB, equivalence proof, readout, score, and verdict permissions remain closed
- `role_coordinate_materialization`: BLOCKED_ROLE_COORDINATES_NOT_MATERIALIZED | role coordinates are declared but not materialized
- `carrier_certification`: BLOCKED_CARRIER_NOT_CERTIFIED | carrier predicate remains a candidate and is not certified
- `concrete_readout`: BLOCKED_CONCRETE_R_CMB_NOT_MATERIALIZED | basis candidate does not materialize a concrete R_CMB map

## Status

```text
CMB_READOUT_ROLE_SPACE_BASIS_AUDITED_BLOCKED_NOT_CERTIFIED
```

The role-space basis is now audit-visible as a carrier candidate. It remains
blocked because the role coordinates are not materialized, the carrier is not
certified, and no concrete `R_CMB` map is supplied.

## Next Minimal Unblock

```text
tau_cmb_readout_role_coordinate_acoustic_v01
```
