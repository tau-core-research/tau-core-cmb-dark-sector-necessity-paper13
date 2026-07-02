# CMB Tau Lensing Projection Operator Rule Requirement v01

**Doc class:** projection-operator rule requirement
**Reader role:** Paper 13 Tau-grid implementer
**Status:** operator rule blocked; explicit failure branch ready
**Canonical parent:** `docs/cmb_tau_lensing_physical_projection_operator_packet_v01.md`

## Claim Boundary

```text
projection_operator_rule_requirement_only_no_operator_no_score_no_dark_sector_verdict
```

## Target

```text
Projection_PP[Phi_lens_tau](L)
```

## Accepted Forms

- closed operator equation with declared measure/kernel and dimensions
- hash-bound kernel table mapping accepted Phi_lens_tau support to L=10..3009
- transfer/projection integral with declared distance, window, and Fourier conventions
- explicit failure statement explaining why no lawful projection operator is currently supplied

## Required Metadata

- domain source: accepted Phi_lens_tau(a,k) contract or values
- codomain: tau_PP(L) or delta_PP_tau(L), L=10..3009
- line-of-sight or projection geometry convention
- k convention and L convention
- normalization and sign convention
- known-limit behavior for zero source
- endpoint firewall certificate

## Explicit Failure Branch

If no lawful projection operator is supplied, the row may be closed only as an
explicit non-score failure. The failure statement must name:

- missing operator equation/kernel/integral
- missing physical normalization
- missing source-to-grid replay
- next theoretical blocker

This does not accept `N_projection_physical`; it only prevents the blocker from
remaining vague.

## Source Evidence

- `docs/cmb_tau_lensing_grid_equation_packet_v01.md`
- `docs/cmb_tau_lensing_projection_normalization_split_v01.md`
- `docs/tau_cmb_lensing_transfer_benchmark_v01.md`
- `docs/tau_cmb_growth_transfer_kernel_closure_v01.md`
