# CMB Tau Lensing Endpoint-Blind Normalization Gate v01

**Doc class:** scoring precondition gate
**Reader role:** Paper 13 Tau-grid implementer
**Status:** blocks physical score retry until normalization is predeclared
**Canonical parent:** `docs/cmb_tau_lensing_route_b_normalization_gap_derivation_v01.md`

## Claim Boundary

```text
normalization_gate_only_no_payload_promotion_no_score_no_dark_sector_verdict
```

## Gate Status

```text
BLOCKED_FOR_PHYSICAL_SCORE_RETRY
```

The current Route B formula spec uses unit dimensionless normalization. The
diagnostic algebra gives:

```text
alpha_* = 1.0252273404414796e-08
```

but `alpha_*` is not endpoint-blind because it was computed from the ACT
bandpowers. It may define the amplitude gap to explain; it may not be inserted
as the physical Tau normalization.

## Required Object

```text
N_tau_CMB_lensing_v01
N_tau = N_parent_source * N_projection * N_PP_or_clkk_convention
```

It must contain:

- source-side derivation of N_parent_source
- projection operator normalization N_projection
- PP/clkk and binning convention normalization N_PP_or_clkk_convention
- dimension statement
- known-limit statement N_tau -> 0 or delta_PP_tau -> 0 when parent response -> 0
- endpoint-firewall statement excluding ACT/Planck residuals and score outputs
- frozen value/range before materialization

## Allowed Next Routes

- `strict_physical_retry`: derive N_tau from Tau-side and adapter-convention sources, update formula spec, rematerialize payload, rerun score
- `diagnostic_parameterized_retry`: declare a prior/range for normalization before scoring and treat score as parameterized diagnostic
- `shape_kernel_revision`: replace the current power-law cutoff unit shape from Tau-side theory before any new endpoint comparison

## Forbidden Shortcut

```text
Do not set normalization to the post-score alpha_star and call it a Tau derivation. That would be endpoint leakage.
```

## Downstream Tau-Side Obligation

The remaining Tau-side proof obligation is tracked at:

```text
docs/cmb_tau_lensing_tau_side_normalization_obligation_v01.md
data/derived/cmb_tau_lensing_tau_side_normalization_obligation_v01.json
```
