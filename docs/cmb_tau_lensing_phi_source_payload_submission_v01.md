# CMB Tau Lensing Phi Source Payload Submission v01

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** submission packet, payload not submitted
**Canonical parent:** `docs/cmb_tau_lensing_score_unblock_plan_v01.md`

This packet defines the concrete files required to close the first unblock step:
the `Phi_tau_eff(a,k)` source payload.

## Required Files

```text
tau_lensing_phi_source_identity_v01.md
tau_lensing_phi_source_provenance_v01.json
tau_lensing_phi_source_normalization_v01.md
tau_lensing_phi_source_time_scale_support_v01.csv
tau_lensing_phi_source_lensing_interface_v01.md
tau_lensing_phi_source_cross_readout_guard_v01.md
```

## Acceptance Rule

The files must establish `Phi_tau_eff(a,k)` as an endpoint-blind,
potential-like source with declared domain, codomain, normalization,
lensing-relevant time/scale support, and cross-readout guard.

They must not use ACT/Planck residuals, likelihood errors, previous score
outputs, or desired dark-sector verdicts as construction inputs.

## Current Status

```text
PAYLOAD_NOT_SUBMITTED
```

No `Phi_tau_eff` payload is accepted and no Tau score is allowed.

## Claim Boundary

```text
phi_source_submission_packet_only_no_phi_payload_no_tau_score_no_dark_sector_verdict
```

## Partial Submission Update

All six Phi source components have now been submitted for review at:

```text
payloads/tau_lensing_phi_source_identity_v01.md
payloads/tau_lensing_phi_source_provenance_v01.json
payloads/tau_lensing_phi_source_normalization_v01.md
payloads/tau_lensing_phi_source_time_scale_support_v01.csv
payloads/tau_lensing_phi_source_lensing_interface_v01.md
payloads/tau_lensing_phi_source_cross_readout_guard_v01.md
```

This completes the submission packet for review. It does not accept the Phi
source payload for scoring. A separate acceptance audit must still pass before
the transfer and PP-grid route can be promoted toward a reduced score attempt.
