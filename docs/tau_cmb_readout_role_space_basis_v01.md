# Tau CMB Readout Role Space Basis v01

**Doc class:** CMB readout role-space basis candidate
**Status:** CMB_READOUT_ROLE_SPACE_BASIS_CANDIDATE_DECLARED_NOT_CERTIFIED

## Claim Boundary

```text
tau_cmb_readout_role_space_basis_v01_basis_candidate_only_carrier_not_certified_no_concrete_R_CMB_no_equivalence_proof_no_readout_evaluation_no_score_no_verdict
```

## Purpose

This artifact declares the candidate role-space basis needed to type the future
carrier predicate `C_CMB^seed`. It does not certify the carrier, materialize a
concrete `R_CMB`, prove the equivalence relation, evaluate CMB readout, enter
scoring, or decide the dark-sector question.

## Candidate Carrier Shape

```text
C_CMB^seed := span_or_product_role_basis(e_acoustic,e_density,e_lensing,e_growth,e_radiation,e_null)
```

This is a role-space basis candidate, not a vector-space theorem and not a
numerical CMB likelihood basis. Each role coordinate still needs its own
coordinate definition, unit/dimension replay, and endpoint-blind provenance.

## Basis Rows

- `TCMBRRSB01_001` `acoustic_phase_height`: BASIS_ROLE_DECLARED_NOT_MATERIALIZED | `e_acoustic`
- `TCMBRRSB01_002` `density_amplitude`: BASIS_ROLE_DECLARED_NOT_MATERIALIZED | `e_density`
- `TCMBRRSB01_003` `lensing_potential`: BASIS_ROLE_DECLARED_NOT_MATERIALIZED | `e_lensing`
- `TCMBRRSB01_004` `growth_transfer`: BASIS_ROLE_DECLARED_NOT_MATERIALIZED | `e_growth`
- `TCMBRRSB01_005` `radiation_damping_guard`: BASIS_ROLE_DECLARED_NOT_MATERIALIZED | `e_radiation`
- `TCMBRRSB01_006` `null_readout`: NULL_BASIS_ANCHOR_DECLARED_NOT_ACCEPTED | `e_null`

## Status

```text
CMB_READOUT_ROLE_SPACE_BASIS_CANDIDATE_DECLARED_NOT_CERTIFIED
```

## Next Minimal Unblock

```text
tau_cmb_readout_role_space_basis_audit_v01
```
