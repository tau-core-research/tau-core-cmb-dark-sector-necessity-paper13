# CMB Tau Lensing Phi Source Acceptance Audit v02

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** accepted for transfer definition only, not accepted for score
**Canonical parent:** `docs/cmb_tau_lensing_phi_source_payload_submission_v01.md`

This audit reviews the six submitted `Phi_tau_eff(a,k)` source payload
components.

## Result

```text
ACCEPT_PHI_SOURCE_FOR_TRANSFER_DEFINITION_ONLY
```

The Phi source package is now complete enough to define the transfer payload
interface. It is not a numeric Tau lensing response, not a `PP` grid, and not a
CMB score input.

## Accepted For Transfer Definition

- identity;
- endpoint-blind provenance firewall;
- normalization obligation;
- time/scale support obligation;
- lensing handoff interface;
- cross-readout guard.

## Still Missing Before Score

- numeric or fully replayable transfer rule;
- accepted transfer domain/codomain/time-scale/operator/normalization package;
- accepted `tau_PP_grid` or `delta_PP_tau` projection payload;
- payload hash replay;
- endpoint-blind score firewall replay.

## Decision Boundary

```text
phi_source_acceptance_audit_v02_transfer_definition_only_no_tau_score_no_dark_sector_verdict
```

This audit closes only the Phi-source definition blocker. It does not claim that
Tau Core explains CMB lensing or that a dark-sector response is required.
