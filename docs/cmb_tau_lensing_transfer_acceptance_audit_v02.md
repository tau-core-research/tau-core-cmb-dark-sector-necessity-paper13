# CMB Tau Lensing Transfer Acceptance Audit v02

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** accepted for projection definition only, not accepted for score
**Canonical parent:** `docs/cmb_tau_lensing_transfer_payload_submission_v01.md`

This audit reviews the six submitted `T_tau_CMB` transfer payload components.

## Result

```text
ACCEPT_TRANSFER_FOR_PROJECTION_DEFINITION_ONLY
```

The transfer package is now complete enough to define the PP-grid projection
payload interface. It is not a numeric transfer kernel, not a projected `PP`
grid, and not a CMB score input.

## Accepted For Projection Definition

- domain from the accepted Phi source definition;
- codomain as a lensing-era potential response;
- time/scale convention obligations;
- operator signature;
- normalization obligations;
- cross-role guard.

## Still Missing Before Score

- numeric transfer kernel, closed operator rule, or explicit failure statement;
- accepted `tau_PP_grid` or `delta_PP_tau` payload;
- PP-grid projection replay;
- payload hash replay;
- endpoint-blind score firewall replay.

## Decision Boundary

```text
transfer_acceptance_audit_v02_projection_definition_only_no_tau_score_no_dark_sector_verdict
```

This audit closes only the transfer-definition blocker. It does not claim that
Tau Core explains CMB lensing or that a dark-sector response is required.
