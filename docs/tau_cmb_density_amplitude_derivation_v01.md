# Tau CMB Density Amplitude Derivation v01

**Doc class:** density-amplitude derivation scaffold
**Status:** conditional definition declared; no endpoint-blind derivation, no fit, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_density_amplitude_derivation.py
```

Derived outputs:

```text
data/derived/tau_cmb_density_amplitude_derivation_v01.csv
data/derived/tau_cmb_density_amplitude_derivation_summary_v01.csv
```

This artifact declares the formal amplitude slot:

```text
A_tau(a,k) := rho_tau_eff(a,k) / rho_cdm_ref(a)
```

This is conditionally dimensionless if `rho_tau_eff` and `rho_cdm_ref` are
both density-normalized under the same convention. That conditional dimension
check is useful, but it is not yet a Tau-side derivation of `A_tau`, not an
Omega_c h^2 match, and not a CMB likelihood result.

The density role remains blocked until `A_tau(a,k)` is derived endpoint-blind
from Tau-side data rather than tuned from CMB residuals.

## Claim Boundary

This artifact declares a conditional density-amplitude definition only. It
computes no numerical amplitude, proves no endpoint-blind derivation, matches no Omega_c h^2 role, computes no score, supplies no CMB likelihood, and permits no no-dark or dark-sector verdict.
