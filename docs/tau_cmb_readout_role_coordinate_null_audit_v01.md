# Tau CMB Readout Role Coordinate Null Audit v01

**Doc class:** null/control role-coordinate audit
**Status:** NULL_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_ACCEPTED

## Claim Boundary

```text
tau_cmb_readout_role_coordinate_null_audit_v01_audit_only_null_not_accepted_no_physical_response_no_quotient_proof_no_concrete_R_CMB_no_carrier_certification_no_score_no_verdict
```

## Purpose

This audit checks whether the null/control role-coordinate candidate has the
expected components, formal slots, control roles, dependency trace,
block/guard accounting, and promotion firewall. It does not accept the null
coordinate, claim physical Tau response, prove the quotient relation,
materialize concrete `R_CMB`, certify the carrier, open score entry, or decide
the dark-sector question.

## Audit Rows

- `coordinate_row_shape`: PASS_NULL_COORDINATE_ROWS_PRESENT | coordinate_components=['null_seed_anchor', 'null_readout_anchor', 'quotient_relation_hook', 'zero_source_consistency', 'forbidden_promotion']
- `input_control_chain`: PASS_CONTROL_AUDIT_CHAIN | null coordinate follows clean radiation, zero-control, and quotient-relation candidate audits
- `formal_slots_declared`: PASS_FORMAL_SLOTS_DECLARED | each null coordinate component has a formal slot
- `dimension_roles_declared`: PASS_DIMENSION_ROLES_DECLARED | each null coordinate component has a control/dimension role
- `source_dependencies_declared`: PASS_SOURCE_DEPENDENCIES_DECLARED | each null coordinate component is tied to existing zero-control or quotient artifacts
- `block_guard_accounting`: PASS_BLOCK_GUARD_ACCOUNTING | blocked_count=3, guard_count=2
- `promotion_firewall`: PASS_NULL_COORDINATE_FIREWALL_CLOSED | coordinate acceptance, physical response, quotient proof, concrete R_CMB, carrier certification, score, and verdict permissions remain closed
- `null_seed_acceptance`: BLOCKED_NULL_SEED_NOT_ACCEPTED | null seed is audited as control but not accepted as a readout-domain member
- `null_readout_materialization`: BLOCKED_NULL_READOUT_NOT_MATERIALIZED | R_CMB(null_seed) := null_readout is declared but concrete R_CMB is not materialized
- `quotient_relation_proof`: BLOCKED_QUOTIENT_RELATION_NOT_PROVED | quotient relation hook is declared but equivalence relation, quotient map, and survival condition are not proved
- `zero_control_not_physical_proof`: GUARD_ZERO_SOURCE_CONTROL_NOT_PHYSICAL_PROOF | zero-control is kept separate from physical zero-source projection proof

## Status

```text
NULL_ROLE_COORDINATE_AUDITED_BLOCKED_NOT_ACCEPTED
```

The null coordinate is audit-visible but not accepted. It remains blocked on
null-seed domain acceptance, concrete null-readout materialization, and
quotient-relation proof. The audit also preserves the guard that zero-control
is not a physical zero-source proof.

## Next Minimal Unblock

```text
tau_cmb_readout_role_coordinate_bundle_closure_v01
```
