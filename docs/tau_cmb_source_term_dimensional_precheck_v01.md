# Tau CMB Source-Term Dimensional Precheck v01

**Doc class:** dimensional precheck
**Status:** partial conditional precheck; no full dimensional proof, no scoring verdict

Script:

```text
scripts/build_tau_cmb_source_term_dimensional_precheck.py
```

Derived outputs:

```text
data/derived/tau_cmb_source_term_dimensional_precheck_v01.csv
data/derived/tau_cmb_source_term_dimensional_precheck_summary_v01.csv
```

This artifact checks the minimal source-term candidate only at the level of
dimensional preconditions. Three rows are conditionally precheckable:

```text
rho_tau_eff(a,k) = A_tau(a,k) rho_cdm_ref(a)
k^2 Phi_tau_eff(a,k) = 4 pi G a^2 rho_tau_eff(a,k) Delta_tau(a,k)
Delta_N_eff_tau <= Delta_N_eff_bound
```

The other three rows remain blocked because the response operator, transfer
kernel, and known-limit map are not yet supplied. Therefore the artifact moves
Paper 13 closer to scoring, but still blocks a CMB no-dark claim and any
dark-sector verdict.

## Claim Boundary

This is a conditional dimensional precheck only. It proves no full dimensional
consistency theorem, matches no CMB likelihood, supplies no Boltzmann solver,
and permits no Tau-response or dark-sector verdict.
