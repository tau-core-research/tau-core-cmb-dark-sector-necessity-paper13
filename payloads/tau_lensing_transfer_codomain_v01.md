# Tau Lensing Transfer Codomain v01

**Payload class:** transfer codomain
**Status:** submitted for review, not accepted
**Parent gate:** `docs/cmb_tau_lensing_transfer_payload_submission_v01.md`

This payload selects the output object for the CMB lensing transfer route.

## Selected Output Object

The transfer output is a lensing-era potential response object:

```text
Psi_tau_lens(a,k)
```

or an equivalent named potential-response variable accepted by a later transfer
operator payload.

## Codomain Statement

The codomain of the transfer route is:

```text
Codomain(T_tau_CMB) = { lensing-era potential response object projectable to
tau_PP_grid or delta_PP_tau }
```

This codomain is selected only as the bridge object between `Phi_tau_eff(a,k)`
and the later `PP` projection payload.

## Projection Compatibility

The codomain must be compatible with the already locked lensing route:

```text
Phi_tau_eff(a,k) -> T_tau_CMB -> tau_PP_grid or delta_PP_tau
```

This file does not define the transfer operator, `PP` projection kernel,
amplitude, covariance score, or dark-sector verdict.

## Endpoint-Blind Rule

The codomain is not chosen from ACT or Planck residuals, a reduced score value,
or a desired dark-sector verdict.

## Claim Boundary

```text
transfer_codomain_payload_only_no_operator_no_pp_grid_no_tau_score_no_dark_sector_verdict
```
