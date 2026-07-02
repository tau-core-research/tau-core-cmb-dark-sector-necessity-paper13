# Tau CMB Minimal Source-Term Candidate v01

**Doc class:** source-term candidate scaffold
**Status:** formula skeletons declared; no dimensional proof, no CMB likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_minimal_source_term_candidate.py
```

Derived outputs:

```text
data/derived/tau_cmb_minimal_source_term_candidate_v01.csv
data/derived/tau_cmb_minimal_source_term_candidate_summary_v01.csv
```

This artifact writes the smallest useful CMB source-term candidate table for
Paper 13. It is not a Tau Core CMB solution. It exists so the later scoring
work has a concrete object to test instead of a loose verbal claim.

The candidate chain is:

```text
X_tau_CMB = Response_tau_CMB(B_tau_base_CMB, delta_M_CMB; OI, ell, h)
rho_tau_eff(a,k) = A_tau(a,k) rho_cdm_ref(a)
k^2 Phi_tau_eff(a,k) = 4 pi G a^2 rho_tau_eff(a,k) Delta_tau(a,k)
T_tau_CMB(k,a) = Transfer_tau[X_tau_CMB](k,a)
Delta_N_eff_tau <= Delta_N_eff_bound
LCDM_role_limit_or_failure
```

The Poisson-like row is a standard-form comparison slot, not a derived Tau
field equation. The density row is conditionally dimension-checkable only if
`A_tau(a,k)` is supplied as a dimensionless Tau-response amplitude rather than
a post-fit residual.

## Claim Boundary

This artifact declares a minimal source-term candidate skeleton only. It proves
no dimensional consistency result, matches no LCDM role, provides no Boltzmann
solver, provides no CMB likelihood, permits no Tau-response claim, and permits
no dark-sector verdict.
