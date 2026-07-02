# Tau CMB Readout Role Coordinate Acoustic v01

**Doc class:** acoustic role-coordinate candidate
**Status:** ACOUSTIC_ROLE_COORDINATE_CANDIDATE_DECLARED_BLOCKED_NOT_MATERIALIZED

## Claim Boundary

```text
tau_cmb_readout_role_coordinate_acoustic_v01_coordinate_candidate_only_not_materialized_no_acoustic_score_no_likelihood_no_concrete_R_CMB_no_carrier_certification_no_verdict
```

## Purpose

This artifact declares the candidate components of the acoustic readout role
coordinate `e_acoustic`. It is not an acoustic fit, not a CMB likelihood, not a
concrete `R_CMB` map, and not evidence for a dark-sector verdict.

## Coordinate Rows

- `TCMBRRCA01_001` `potential_source_presence`: BLOCKED_SOURCE_NOT_DERIVED | `Phi_tau_eff(a,k)|recombination`
- `TCMBRRCA01_002` `phase_support`: BLOCKED_OSCILLATOR_RESPONSE_NOT_EVALUATED | `phase_tau_acoustic`
- `TCMBRRCA01_003` `relative_peak_height`: BLOCKED_AMPLITUDE_NOT_AVAILABLE | `height_ratio_tau_acoustic`
- `TCMBRRCA01_004` `baryon_loading_coupling`: BLOCKED_COUPLING_SIGN_MISSING | `coupling_sign_tau_baryon`
- `TCMBRRCA01_005` `scale_horizon_guard`: CONVENTION_GUARD_DECLARED_NOT_NUMERIC | `(k,a_rec,r_s)_convention`
- `TCMBRRCA01_006` `failure_branch`: FAILURE_BRANCH_READY_NOT_TRIGGERED | `acoustic_fail_if_missing_required_inputs`

## Status

```text
ACOUSTIC_ROLE_COORDINATE_CANDIDATE_DECLARED_BLOCKED_NOT_MATERIALIZED
```

The acoustic coordinate is now explicit as a blocked role-coordinate candidate.
It remains unmaterialized because the Tau pre-recombination source, oscillator
response, endpoint-blind amplitude, and coupling sign are not supplied.

## Next Minimal Unblock

```text
tau_cmb_readout_role_coordinate_acoustic_audit_v01
```
