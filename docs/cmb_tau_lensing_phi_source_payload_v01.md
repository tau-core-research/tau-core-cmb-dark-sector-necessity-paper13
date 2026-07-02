# CMB Tau Lensing Phi Source Payload v01

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** Phi source payload requirement, no payload
**Canonical parent:** `docs/cmb_tau_lensing_response_derivation_route_v01.md`

This packet translates the common Tau CMB effective-potential handoff into the
specific payload requirements needed before an ACT lensing `PP` grid can be
constructed.

## Required Source

The route requires:

```text
Phi_tau_eff(a,k)
```

as a potential-like metric readout with declared domain, codomain, normalization,
time/scale support, and endpoint-blind provenance.

## Required Payload Components

A valid `Phi_tau_eff` payload must provide:

- source identity and domain/codomain;
- endpoint-blind provenance;
- normalization convention;
- lensing-relevant time/scale support;
- interface to the transfer/projection route;
- cross-readout guard for reuse with acoustic and density roles.

## Current Status

No `Phi_tau_eff` payload is submitted. This packet only states what must be
provided before a lensing response can be built.

The status remains:

```text
BLOCKED_PAYLOAD_NOT_SUBMITTED
```

## Claim Boundary

```text
phi_source_payload_requirement_only_no_phi_derivation_no_tau_score_no_dark_sector_verdict
```

The Phi source acceptance audit is tracked at:

```text
data/source_manifest/cmb_tau_lensing_phi_source_acceptance_audit_v01.csv
docs/cmb_tau_lensing_phi_source_acceptance_audit_v01.md
```
