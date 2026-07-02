# CMB Tau Lensing Response Derivation Route v01

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** derivation route, no payload
**Canonical parent:** `docs/cmb_tau_lensing_response_payload_template_packet_v01.md`

This route connects the existing Tau CMB scaffold to the concrete ACT lensing
payload templates. It does not derive the payload.

## Route

The direct payload route is:

```text
Phi_tau_eff(a,k)
-> T_tau_CMB(k,a)
-> lensing-era potential response
-> tau_theory_lenspotential_PP_grid, shape (3000,)
-> B_ACT @ tau_PP_grid, shape (18,)
```

The perturbative payload route is:

```text
Phi_tau_eff(a,k)
-> T_tau_CMB(k,a)
-> delta_PP_tau, shape (3000,)
-> tau_PP_grid = PP_fiducial + delta_PP_tau
```

## Current Blockers

The existing reduced lensing evaluation already identifies the same blockers:

- `Phi_tau_eff(a,k)` remains a target slot rather than a derived source;
- `T_tau_CMB(k,a)` is not yet a specified transfer operator;
- no lensing amplitude/shape response has been computed;
- cross-readout consistency is not available.

This route packet therefore does not unblock scoring. It makes the remaining
work exact.

## Acceptance Requirements

Before payload submission, the route must provide:

- source derivation for `Phi_tau_eff`;
- transfer operator with domain, codomain, time/scale convention, and
  normalization;
- map into a length-3000 `PP` or `delta_PP_tau` grid;
- declared parameter policy;
- endpoint firewall trace excluding ACT residual fitting;
- claim boundary preserving reduced diagnostic status.

## Claim Boundary

```text
tau_lensing_derivation_route_only_no_payload_no_tau_score_no_dark_sector_verdict
```

The Phi source payload requirement is tracked at:

```text
data/source_manifest/cmb_tau_lensing_phi_source_payload_v01.csv
docs/cmb_tau_lensing_phi_source_payload_v01.md
```

The transfer payload requirement is tracked at:

```text
data/source_manifest/cmb_tau_lensing_transfer_payload_v01.csv
docs/cmb_tau_lensing_transfer_payload_v01.md
```

The PP-grid projection payload requirement is tracked at:

```text
data/source_manifest/cmb_tau_lensing_pp_grid_projection_payload_v01.csv
docs/cmb_tau_lensing_pp_grid_projection_payload_v01.md
```
