# Tau CMB Density Amplitude Closure v01

**Doc class:** density-amplitude blocker closure
**Status:** partial closure; density score still blocked, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_density_amplitude_closure.py
```

Derived outputs:

```text
data/derived/tau_cmb_density_amplitude_closure_v01.csv
data/derived/tau_cmb_density_amplitude_closure_summary_v01.csv
```

This artifact closes only the formal part of the density-amplitude blocker:

```text
A_tau(a,k) := rho_tau_eff(a,k) / rho_cdm_ref(a)
```

is a conditionally dimensionless ratio if both densities share a normalization.
The blocker is not fully closed because `rho_tau_eff(a,k)` and endpoint-blind
`A_tau(a,k)` are not derived, and the `Omega_c h^2` role is not compared.

The density score therefore remains blocked.

## Claim Boundary

This artifact is a partial closure only. It computes no density score, supplies
no CMB likelihood, declares no Omega_c h^2 match, validates no Tau-response
source, and permits no no-dark or dark-sector verdict.
