# CMB Tau Lensing Phi Source Acceptance Audit v01

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** Phi source acceptance audit, payload absent
**Canonical parent:** `docs/cmb_tau_lensing_phi_source_payload_v01.md`

This audit checks whether the `Phi_tau_eff(a,k)` source payload required by the
Tau lensing derivation route has actually been submitted.

## Result

No required `Phi_tau_eff` source payload component is present.

The current state is therefore rejected as a lensing response input. This is a
controlled blocker, not a Tau Core failure or score.

## Missing Components

```text
phi_source_identity
endpoint_blind_provenance
normalization_convention
time_scale_support
lensing_projection_readiness
cross_readout_guard
```

## Decision

```text
REJECT_FOR_LENSING_RESPONSE_INPUT
```

No `Phi_tau_eff` payload is accepted. No Tau lensing response vector can be
derived from this state.

## Claim Boundary

```text
phi_source_acceptance_audit_only_no_phi_payload_no_tau_score_no_dark_sector_verdict
```
