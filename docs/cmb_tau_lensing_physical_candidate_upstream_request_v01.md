# CMB Tau Lensing Physical Candidate Upstream Request v01

**Doc class:** physical-candidate Tau-grid upstream request
**Status:** request only; no grid, no score, no verdict
**Canonical script:** `scripts/build_tau_lensing_physical_candidate_upstream_request.py`
**Canonical parent:** `docs/cmb_tau_lensing_upstream_table_formula_spec_contract_v01.md`

This request defines the exact upstream object needed to move from the current
control/probe state to a physical-candidate Tau lensing grid.

## Required Output

```text
payload_staging/tau_lensing_upstream_l_response_v01.csv
payload_staging/tau_lensing_upstream_l_response_metadata_v01.json
```

The table must contain exactly 3000 finite rows with `L=10..3009` and one
`tau_response_value` per row.

## Route A: Transfer Projection

Status: `preferred_physical_route`

```text
rho_tau_eff(a,k) = A_tau(a,k) * rho_ref(a)
k^2 Phi_tau_eff(a,k) = 4*pi*G*a^2*rho_tau_eff(a,k)*Delta_tau(a,k)
Phi_lens_tau(a,k) = T_tau_CMB(k,a)[Phi_tau_eff]
tau_PP(L) = Projection_PP[Phi_lens_tau](L)
```

Minimum evidence:
- endpoint-blind A_tau(a,k) or equivalent Tau parent source
- Phi_tau_eff normalization and sign convention
- T_tau_CMB domain, codomain, time/scale convention, and operator rule
- PP projection convention from lensing potential to L-space
- known-limit audit against zero-response/LCDM comparison behavior

## Route B: Direct L-Space

Status: `allowed_only_if_tau_derived_before_endpoint_score`

```text
delta_PP_tau(L) = F_tau_L(parent_tau_source, readout_profile, scale_profile; L)
write exact L,value table without fitting ACT/Planck residuals
```

Minimum evidence:
- parent Tau source object used by F_tau_L
- parameter-free or endpoint-blind parameter fixation rule
- normalization convention for dimensionless delta_PP_tau(L)
- known-limit audit showing zero/null behavior when Tau source is absent

## Forbidden Inputs

- ACT residuals
- Planck residuals
- reduced chi2 tuning
- score output tuning
- dark-sector verdict preference
- diagnostic probe parameters
- zero-control definitions promoted as physical response

## Acceptance Commands

```text
make tau-grid-physical-candidate-precheck
make tau-grid-handoff-write-staging
make tau-grid-physical-candidate-package
make staging-promote-delta-dry-run
```

## Claim Boundary

```text
physical_candidate_upstream_request_only_no_grid_no_score_no_dark_sector_verdict
```

This request does not derive a Tau response. It only defines the deliverable
that must exist before the physical-candidate Tau-grid path can advance.
