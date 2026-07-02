# CMB Tau Lensing PP Grid Acceptance Audit v02

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** partial rules accepted for projection review, rejected for score
**Canonical parent:** `docs/cmb_tau_lensing_pp_grid_payload_submission_v01.md`

This audit reviews the current `tau_PP_grid` / `delta_PP_tau` projection payload
state after the non-numeric rule components were submitted.

## Result

```text
REJECT_FOR_SCORE_INPUT
```

Four rule components are present and usable for projection review:

```text
index alignment
normalization policy
delta route policy
claim boundary
```

Two score-critical components remain missing:

```text
real 3000-value tau_PP_grid or delta_PP_tau
projection replay showing B_ACT @ grid -> shape (18,)
```

## Decision

The PP-grid payload is not accepted for Tau scoring. The current state only
prepares the rules under which a future numeric grid may be judged.

## Claim Boundary

```text
pp_grid_acceptance_audit_v02_partial_rules_only_no_numeric_grid_no_tau_score_no_dark_sector_verdict
```

This audit does not evaluate ACT, Planck, Tau Core dark-sector necessity, or a
physical Tau response.
