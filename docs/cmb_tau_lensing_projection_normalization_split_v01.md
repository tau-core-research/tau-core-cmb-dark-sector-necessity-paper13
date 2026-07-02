# CMB Tau Lensing Projection Normalization Split v01

**Doc class:** projection-normalization split
**Reader role:** Paper 13 Tau-grid implementer
**Status:** Route B adapter replay locked; physical projection explicit non-score failure
**Canonical parent:** `docs/tau_cmb_lensing_N_parent_projection_packet_v01.md`

## Claim Boundary

```text
projection_normalization_split_only_no_physical_projection_derivation_no_score_no_dark_sector_verdict
```

## Split

There are two different projection notions in the current pipeline.

### Route B Adapter Replay

```text
operator = B_ACT @ grid
N_projection_adapter_replay = 1.0
locked = True
```

This is only the validation/replay map from a pre-materialized L-space Tau grid
to the ACT 18-band comparison vector. It does not derive a physical Tau
`Phi -> PP` projection.

### Physical Tau Projection

```text
operator = Projection_PP[Phi_lens_tau](L)
N_projection_physical = BLOCKED
```

Already locked:

```text
domain contract: Phi_lens_tau(a,k) = T_tau_CMB(k,a)[Phi_tau_eff], transfer-defined over a,k, no numeric field supplied
codomain convention: 3000-row L-space PP-style target, tau_PP(L) or delta_PP_tau(L), L=10..3009
endpoint firewall: pass for current skeleton only; rerun after operator/normalization/replay values
```

Structured failure branch:

```text
operator-rule accepted forms are declared and the current packet records an explicit non-score operator failure
physical source-to-grid replay requirements are declared but not materializable on the failure branch
N_projection_physical policy is declared; no numeric normalization before an accepted operator rule replaces the failure
```

The missing pieces are:

- lensing kernel or transfer support
- Fourier and L-space convention
- linearity/nonlinearity rule
- dimension and sign convention
- endpoint-blind replay from parent source to 3000-point PP grid

## Consequence

For Route B diagnostics, the adapter replay normalization is convention-locked.
For a physical endpoint-blind score retry, the `N_projection` row in the parent
projection packet is not merely open. It is explicitly failed for the current
packet and may only resume if an endpoint-blind physical projection operator,
normalization, replay, and refreshed firewall certificate replace the failure
before scoring.

The physical projection packet and audit are tracked at:

```text
docs/cmb_tau_lensing_physical_projection_operator_packet_v01.md
data/derived/cmb_tau_lensing_physical_projection_operator_packet_v01.csv
data/derived/cmb_tau_lensing_physical_projection_operator_packet_audit_v01.json
```
