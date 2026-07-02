# Tau CMB Readout Role Coordinate Null v01

**Doc class:** null/control role-coordinate candidate
**Status:** NULL_ROLE_COORDINATE_CONTROL_CANDIDATE_DECLARED_BLOCKED_NOT_ACCEPTED

## Claim Boundary

```text
tau_cmb_readout_role_coordinate_null_v01_control_candidate_only_null_not_accepted_no_physical_response_no_quotient_proof_no_concrete_R_CMB_no_carrier_certification_no_score_no_verdict
```

## Purpose

This artifact declares the candidate components of the null/control readout
role coordinate `e_null`. It is not a physical Tau response, not a quotient
proof, not a concrete `R_CMB` map, not carrier certification, not a score
entry, and not evidence for a dark-sector verdict.

## Coordinate Rows

- `TCMBRRCN01_001` `null_seed_anchor`: BLOCKED_NULL_SEED_NOT_ACCEPTED | `null_seed_tau_CMB`
- `TCMBRRCN01_002` `null_readout_anchor`: BLOCKED_NULL_READOUT_NOT_MATERIALIZED | `R_CMB(null_seed_tau_CMB) := null_readout`
- `TCMBRRCN01_003` `quotient_relation_hook`: BLOCKED_QUOTIENT_RELATION_NOT_PROVED | `R_CMB(seed) ~ R_CMB(null_seed)`
- `TCMBRRCN01_004` `zero_source_consistency`: GUARD_ZERO_SOURCE_CONTROL_DECLARED_NOT_PHYSICAL_PROOF | `zero_source -> zero Tau readout contribution`
- `TCMBRRCN01_005` `forbidden_promotion`: PROMOTION_FORBIDDEN_DECLARED | `null_seed != physical Tau response`

## Status

```text
NULL_ROLE_COORDINATE_CONTROL_CANDIDATE_DECLARED_BLOCKED_NOT_ACCEPTED
```

The null coordinate is explicit as a blocked control candidate. It anchors the
future null side of readout comparison, while preserving the rule that
zero-control is not physical response evidence and cannot be used as a
zero-source proof for a physical projection operator.

## Next Minimal Unblock

```text
tau_cmb_readout_role_coordinate_null_audit_v01
```
