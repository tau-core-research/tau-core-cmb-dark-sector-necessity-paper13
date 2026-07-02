# Tau CMB Readout Role Coordinate Lensing v01

**Doc class:** lensing role-coordinate candidate
**Status:** LENSING_ROLE_COORDINATE_CANDIDATE_DECLARED_BLOCKED_NOT_MATERIALIZED

## Claim Boundary

```text
tau_cmb_readout_role_coordinate_lensing_v01_coordinate_candidate_only_not_materialized_no_lensing_score_no_act_planck_match_no_concrete_R_CMB_no_carrier_certification_no_verdict
```

## Purpose

This artifact declares the candidate components of the lensing readout role
coordinate `e_lensing`. It is not a lensing score, not an ACT/Planck match,
not a CMB likelihood, not a concrete `R_CMB` map, and not evidence for a
dark-sector verdict.

## Coordinate Rows

- `TCMBRRCL01_001` `lensing_potential_source`: BLOCKED_POTENTIAL_SOURCE_NOT_DERIVED | `Phi_tau_eff(a,k)`
- `TCMBRRCL01_002` `transfer_kernel`: BLOCKED_TRANSFER_KERNEL_NOT_SPECIFIED | `T_tau_CMB(k,a)`
- `TCMBRRCL01_003` `projection_geometry_guard`: CONDITIONAL_PROJECTION_GEOMETRY_GUARD_DECLARED_NOT_NUMERIC | `G_lens[line_of_sight,distance,kernel]`
- `TCMBRRCL01_004` `amplitude_shape_response`: BLOCKED_AMPLITUDE_SHAPE_NOT_EVALUATED | `S_lens_tau(L) or delta S_lens_tau(L)`
- `TCMBRRCL01_005` `cross_readout_consistency`: BLOCKED_CROSS_READOUT_NOT_AVAILABLE | `Consistent(A_tau,Phi_tau_eff,T_tau_CMB,e_acoustic,e_density)`
- `TCMBRRCL01_006` `lensing_stop_rule`: STOP_RULE_DECLARED_NOT_TRIGGERED | `lensing_fail_if_source_transfer_projection_or_shape_missing`

## Status

```text
LENSING_ROLE_COORDINATE_CANDIDATE_DECLARED_BLOCKED_NOT_MATERIALIZED
```

The lensing coordinate is explicit as a blocked role-coordinate candidate. It
remains unmaterialized because `Phi_tau_eff(a,k)`, `T_tau_CMB(k,a)`,
endpoint-blind amplitude/shape response, and cross-readout consistency are not
supplied in score-ready form.

## Next Minimal Unblock

```text
tau_cmb_readout_role_coordinate_lensing_audit_v01
```
