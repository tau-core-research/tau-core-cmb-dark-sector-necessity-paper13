# CMB Tau Lensing Grid Equation Packet v01

**Doc class:** Tau-grid equation packet
**Status:** equation-level route only; no grid, no score, no verdict
**Canonical script:** `scripts/build_tau_lensing_grid_equation_packet.py`
**Canonical parent:** `docs/cmb_tau_lensing_grid_formula_spec_candidate_v01.md`

This packet narrows Tau-grid production to two concrete mathematical routes.
It does not supply a physical Tau grid.

## Target

The scoring adapter needs one endpoint-blind numeric object:

```text
tau_PP(L) or delta_PP_tau(L), for L = 10..3009
```

The materializer can write the 3000-row staging grid after a non-template
formula spec exists.

## Route A: Transfer Projection

This is the stronger physics route:

```text
rho_tau_eff(a,k) = A_tau(a,k) * rho_ref(a)

k^2 * Phi_tau_eff(a,k)
  = 4*pi*G*a^2*rho_tau_eff(a,k)*Delta_tau(a,k)

Phi_lens_tau(a,k)
  = T_tau_CMB(k,a) * Phi_tau_eff(a,k)

tau_PP(L)
  = Projection_PP[Phi_lens_tau](L)
```

This route needs:

- endpoint-blind `A_tau(a,k)`;
- parent-to-`Phi_tau_eff` rule;
- potential normalization and sign convention;
- `T_tau_CMB(k,a)` propagation rule;
- CMB lensing `PP` projection convention.

## Route B: Direct L-Space Response

This is the faster endpoint-blind scoring probe:

```text
delta_PP_tau(L)
  = F_tau_L(B_tau_base_CMB, delta_M_CMB, OI, scale_profile; L)
```

This may be materialized through the first supported adapter family:

```text
power_law_cutoff_response_v01
```

or, preferably when an upstream Tau derivation already produced the numeric
response:

```text
tabulated_l_response_v01
```

but only if all parameters are fixed before ACT/Planck residual score readout.
Without that Tau-side parameter fixation, Route B is only an arbitrary shape
ansatz and must not be promoted.

## Current Status

```text
materializable_now = false
candidate_spec_status = CANDIDATE_NOT_PAYLOAD
```

## Claim Boundary

```text
tau_grid_equation_packet_only_no_grid_no_score_no_dark_sector_verdict
```

This packet advances the Tau-grid path by reducing the next decision to:

```text
derive T_tau_CMB/projection
or
supply endpoint-blind direct L-space Tau response
```
