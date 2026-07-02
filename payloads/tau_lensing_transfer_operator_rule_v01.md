# Tau Lensing Transfer Operator Rule v01

**Payload class:** transfer operator rule
**Status:** submitted for review, not accepted
**Parent gate:** `docs/cmb_tau_lensing_transfer_payload_submission_v01.md`

This payload declares the minimal operator rule scaffold for transferring the
accepted `Phi_tau_eff(a,k)` source definition into a lensing-era potential
response object.

## Formal Rule

Define a transfer map:

```text
T_tau_CMB: Phi_tau_eff(a,k) -> Psi_tau_lens(a,k)
```

where `Phi_tau_eff(a,k)` is the transfer-domain object and `Psi_tau_lens(a,k)`
is the transfer-codomain object.

## Operator Status

The present payload supplies a formal operator signature only:

```text
Psi_tau_lens(a,k) = T_tau_CMB[Phi_tau_eff](a,k)
```

It does not supply a numerical kernel, closed-form evolution equation,
Boltzmann solver, line-of-sight integral, or `PP` grid.

## Endpoint-Blind Constraint

The operator rule must not be chosen by minimizing:

```text
ACT lensing residuals
Planck residuals
reduced chi2
dark-sector verdict preference
```

Any later numerical kernel must be derived from Tau-side assumptions and
declared before score evaluation.

## Failure Boundary

If no endpoint-blind numerical operator can be supplied, the transfer route must
remain blocked rather than replaced with a fitted response curve.

## Claim Boundary

```text
transfer_operator_rule_payload_signature_only_no_numeric_kernel_no_pp_grid_no_tau_score_no_dark_sector_verdict
```
