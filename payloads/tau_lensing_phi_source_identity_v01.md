# Tau Lensing Phi Source Identity v01

**Payload class:** Phi source identity
**Status:** submitted for review, not accepted
**Parent gate:** `docs/cmb_tau_lensing_phi_source_payload_submission_v01.md`

This payload defines the identity and role of the candidate Tau-side effective
potential source used by the CMB lensing route.

## Definition

Let

```text
Phi_tau_eff(a, k)
```

denote a Tau-side effective potential-response object over scale factor `a` and
comoving wavenumber `k`.

## Domain

```text
a: dimensionless scale factor over the lensing-relevant epoch
k: comoving wavenumber under the later transfer convention
```

The exact numerical support, sampling, and normalization are not supplied in
this identity payload. They remain separate required payloads.

## Codomain

`Phi_tau_eff(a, k)` is treated as a potential-like metric/readout source for the
lensing projection route. This file does not choose a `PP` grid normalization,
does not compute bandpowers, and does not compare to ACT or Planck data.

## Source Role

The object is intended to be the pre-transfer Tau-side source for:

```text
Phi_tau_eff(a, k) -> T_tau_CMB -> tau_PP_grid or delta_PP_tau
```

It is a source identity statement only. It is not a physical detection, a fitted
dark-sector model, or a CMB likelihood component.

## Claim Boundary

```text
phi_source_identity_payload_only_no_normalization_no_transfer_no_pp_grid_no_tau_score_no_dark_sector_verdict
```
