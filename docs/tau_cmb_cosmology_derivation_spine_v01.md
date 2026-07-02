# Tau CMB Cosmology Derivation Spine v01

**Doc class:** Tau-side cosmology derivation spine
**Reader role:** Paper 13 / Tau CMB implementer
**Status:** partial derivation scaffold; not a Boltzmann solver; not score eligible
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
tau_cmb_cosmology_derivation_spine_only_minimal_derivation_scaffold_no_boltzmann_solver_no_likelihood_no_dark_sector_verdict
```

## Purpose

This artifact turns the Paper 13 CMB requirement map into a minimal Tau-side
cosmology derivation chain. It does not claim that Tau Core has solved CMB
cosmology. It identifies the smallest mathematical spine that must be populated
before CMB lensing or dark-sector necessity can be tested.

## Derivation Chain

```text
Tau background/readout
-> rho_tau_eff(a,k)
-> Phi_tau_eff(a,k)
-> Phi_lens_tau(a,k) via T_tau_CMB
-> tau_PP(L) via K_tau_PP and N_projection_physical
-> endpoint-blind CMB score grid
```

## Rows

- `TCMBCDS01_001` `tau_background`: DEFINITION_SCAFFOLD | `M_tau^CMB, a_tau, H_tau` | blocks: cannot define perturbation evolution without readout time/scale convention
- `TCMBCDS01_002` `tau_effective_source`: CONDITIONAL_ROLE_FORMULA | `rho_tau_eff(a,k)` | blocks: A_tau derivation and normalization are not supplied
- `TCMBCDS01_003` `tau_potential_constraint`: COMPARISON_SLOT_NOT_FIELD_EQUATION | `Phi_tau_eff(a,k)` | blocks: Delta_tau and Tau-side field equation are not derived
- `TCMBCDS01_004` `tau_transfer`: TRANSFER_OPERATOR_REQUIRED | `Phi_lens_tau(a,k) = T_tau_CMB(k,a)[Phi_tau_eff]` | blocks: numeric or analytic T_tau_CMB operator is not supplied
- `TCMBCDS01_005` `lensing_projection_kernel`: PROJECTION_KERNEL_REQUIRED | `K_tau_PP(L; a,k) dmu(a,k)` | blocks: full K_tau_PP, measure, support, and normalization are not supplied
- `TCMBCDS01_006` `projection_formula`: FORMULA_SCAFFOLD_NOT_ACCEPTED | `tau_PP(L)` | blocks: N_projection_physical, zero-source proof, dimension/sign audit, and firewall are not accepted
- `TCMBCDS01_007` `zero_source_limit`: PROOF_OBLIGATION_CONDITIONAL | `Phi_lens_tau -> 0 => tau_PP contribution -> 0` | blocks: cannot discharge until operator, kernel, and normalization are supplied
- `TCMBCDS01_008` `score_readout`: PRESCORE_LOCKED | `L=10..3009 grid -> ACT/Planck comparison` | blocks: content audit blocks physical Tau-route score

## Minimal Formula Spine

```text
H_tau := d ln a_tau / d t_readout
rho_tau_eff(a,k) := A_tau(a,k) rho_ref(a)
k^2 Phi_tau_eff(a,k) = 4 pi G a^2 rho_tau_eff(a,k) Delta_tau(a,k)
Phi_lens_tau(a,k) = T_tau_CMB(k,a)[Phi_tau_eff]
tau_PP(L) = N_projection_physical Integral[K_tau_PP(L; a,k) Phi_lens_tau(a,k) dmu(a,k)]
```

## Status

```text
DERIVATION_SPINE_DECLARED_PARTIAL_NOT_SCORE_ELIGIBLE
```

The first three mathematical slots are definitions or comparison targets. The
score-critical blockers remain the endpoint-blind transfer operator
`T_tau_CMB`, the projection kernel/measure `K_tau_PP dmu`, the physical
normalization `N_projection_physical`, the zero-source proof, and the
post-population firewall.

## Source-Grounding Dependency

The effective source row `rho_tau_eff(a,k)` is not source-accepted by this
spine. It must pass the separate source-grounding gate before it can be used as
a Tau-derived CMB source:

```text
docs/tau_cmb_source_grounding_gate_v01.md
```

## Next Minimal Unblock

```text
derive_endpoint_blind_T_tau_CMB_and_K_tau_PP_with_N_projection_physical
```
