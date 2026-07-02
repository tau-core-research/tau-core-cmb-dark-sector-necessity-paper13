# Tau CMB Readout Role Coordinate Density v01

**Doc class:** density role-coordinate candidate
**Status:** DENSITY_ROLE_COORDINATE_CANDIDATE_DECLARED_BLOCKED_NOT_MATERIALIZED

## Claim Boundary

```text
tau_cmb_readout_role_coordinate_density_v01_coordinate_candidate_only_not_materialized_no_density_score_no_omega_c_h2_match_no_concrete_R_CMB_no_carrier_certification_no_verdict
```

## Purpose

This artifact declares the candidate components of the density readout role
coordinate `e_density`. It is not a density score, not an `Omega_c h^2` match,
not a CMB likelihood, not a concrete `R_CMB` map, and not evidence for a
dark-sector verdict.

## Coordinate Rows

- `TCMBRRCD01_001` `density_ratio_guard`: CONDITIONAL_RATIO_GUARD_DECLARED_NOT_NUMERIC | `A_tau(a,k) := rho_tau_eff(a,k) / rho_cdm_ref(a)`
- `TCMBRRCD01_002` `tau_effective_density`: BLOCKED_DENSITY_FORMULA_NOT_DERIVED | `rho_tau_eff(a,k)`
- `TCMBRRCD01_003` `endpoint_blind_amplitude`: BLOCKED_ENDPOINT_BLIND_AMPLITUDE_MISSING | `endpoint_blind(A_tau)`
- `TCMBRRCD01_004` `omega_c_h2_role_comparison`: BLOCKED_NO_NUMERICAL_COMPARISON | `Omega_c h^2 comparison role`
- `TCMBRRCD01_005` `density_stop_rule`: STOP_RULE_DECLARED_NOT_TRIGGERED | `density_fail_if_A_tau_missing`

## Status

```text
DENSITY_ROLE_COORDINATE_CANDIDATE_DECLARED_BLOCKED_NOT_MATERIALIZED
```

The density coordinate is explicit as a blocked role-coordinate candidate. It
remains unmaterialized because `rho_tau_eff(a,k)`, endpoint-blind `A_tau(a,k)`,
and a numerical `Omega_c h^2` comparison are not supplied.

## Next Minimal Unblock

```text
tau_cmb_readout_role_coordinate_density_audit_v01
```
