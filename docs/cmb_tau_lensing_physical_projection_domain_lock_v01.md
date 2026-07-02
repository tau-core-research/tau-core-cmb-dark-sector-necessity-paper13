# CMB Tau Lensing Physical Projection Domain Lock v01

**Doc class:** projection-domain contract lock
**Reader role:** Paper 13 Tau-grid implementer
**Status:** domain contract locked for transfer definition only
**Canonical parent:** `docs/cmb_tau_lensing_physical_projection_operator_packet_v01.md`

## Claim Boundary

```text
projection_domain_lock_only_no_numeric_phi_lens_no_operator_no_score_no_dark_sector_verdict
```

## Domain Contract

The physical projection input object is:

```text
Phi_lens_tau(a,k)
Phi_lens_tau(a,k) = T_tau_CMB(k,a)[Phi_tau_eff]
```

Accepted domain variables:

```text
a: scale-factor/time support over the lensing-relevant transfer interval
k: Fourier scale variable under a declared k convention
```

This locks the domain contract only. It does not supply a numeric
`Phi_lens_tau(a,k)` field and does not derive the projection operator.

## Source Evidence

- `docs/cmb_tau_lensing_phi_source_acceptance_audit_v02.md`
- `docs/cmb_tau_lensing_transfer_payload_v01.md`
- `docs/cmb_tau_lensing_response_derivation_route_v01.md`
- `docs/cmb_tau_lensing_grid_equation_packet_v01.md`

## Still Missing

- numeric or replayable T_tau_CMB operator
- accepted Phi_lens_tau values/kernel
- gauge/sign normalization pass
- physical projection operator rule
- projection normalization
- source-to-grid replay
- projection endpoint firewall certificate
