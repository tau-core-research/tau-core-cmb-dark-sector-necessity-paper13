# Tau Lensing Transfer Domain v01

**Payload class:** transfer domain
**Status:** submitted for review, not accepted
**Parent gate:** `docs/cmb_tau_lensing_transfer_payload_submission_v01.md`

This payload selects the input domain for the CMB lensing transfer route.

## Selected Input Object

The transfer input is:

```text
Phi_tau_eff(a,k)
```

under the transfer-definition-only acceptance recorded in:

```text
data/source_manifest/cmb_tau_lensing_phi_source_acceptance_audit_v02.csv
```

## Domain Statement

The transfer domain is the potential-like Tau-side source over the declared
scale-factor and comoving-wavenumber support:

```text
Domain(T_tau_CMB) = { Phi_tau_eff(a,k) with accepted identity, provenance,
normalization obligation, time/scale support obligation, lensing interface, and
cross-readout guard }
```

This does not provide a transfer operator, evolution equation, kernel table, or
numeric response vector.

## Endpoint-Blind Rule

The domain selection is inherited from the Phi source acceptance audit. It is
not selected from ACT or Planck residuals, a reduced score value, or a desired
dark-sector verdict.

## Claim Boundary

```text
transfer_domain_payload_only_no_codomain_no_operator_no_pp_grid_no_tau_score_no_dark_sector_verdict
```
