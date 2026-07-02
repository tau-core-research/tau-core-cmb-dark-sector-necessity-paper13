# CMB Tau Lensing Grid Formula Spec Candidate v01

**Doc class:** Tau-grid formula candidate audit
**Status:** candidate only; not a payload, not a score
**Canonical script:** `scripts/build_tau_lensing_grid_formula_spec_candidate.py`
**Canonical parent:** `docs/cmb_tau_lensing_grid_formula_materializer_contract_v01.md`

This artifact connects the existing Tau CMB source skeleton to the new
formula-to-grid materializer. It does not claim that a Tau lensing grid has
been derived. Its purpose is narrower: identify the shortest current path from
the existing source skeleton to a materializable `tau_PP(L)` or `delta_PP_tau(L)`
grid.

## Current Candidate Chain

```text
X_tau_CMB
-> A_tau(a,k)
-> rho_tau_eff(a,k)
-> Phi_tau_eff(a,k)
-> T_tau_CMB(k,a)
-> tau_PP(L) or delta_PP_tau(L)
```

The first conditionally usable slot is:

```text
rho_tau_eff(a,k) = A_tau(a,k) rho_cdm_ref(a)
```

provided that `A_tau(a,k)` is dimensionless and derived from Tau-side evidence,
not from endpoint score behavior.

The next conditionally usable slot is:

```text
k^2 Phi_tau_eff(a,k) = 4 pi G a^2 rho_tau_eff(a,k) Delta_tau(a,k)
```

provided that Fourier convention, scale-factor convention, potential
normalization, and `Delta_tau` convention are locked.

## Why It Is Not Materializable Yet

The candidate still lacks:

- parent-side provenance for `Phi_tau_eff`;
- a rule from parent Tau response data to `Phi_tau_eff(a,k)`;
- a shared normalization convention;
- a transfer or direct L-space response rule;
- numeric formula parameters fixed before score readout.

Therefore the candidate remains:

```text
CANDIDATE_NOT_PAYLOAD
```

## Claim Boundary

```text
formula_spec_candidate_audit_only_no_grid_no_score_no_dark_sector_verdict
```

This artifact advances the Tau-grid production route by isolating the exact
objects that must become a non-template formula spec. It does not validate a
physical Tau response and does not permit a CMB dark-sector verdict.
