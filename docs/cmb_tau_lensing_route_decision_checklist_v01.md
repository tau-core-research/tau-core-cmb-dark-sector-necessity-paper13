# CMB Tau Lensing Route Decision Checklist v01

**Doc class:** decision checklist
**Reader role:** Paper 13 scoring implementer
**Status:** route decision blocked
**Canonical parent:** `docs/cmb_tau_lensing_route_choice_rubric_v01.md`

This checklist turns the route rubric into concrete yes/no conditions.

## Result

```text
route_decision_blocked
```

No allowed route currently satisfies its required answers.

## Direct Route Opens Only If

```text
endpoint-blind absolute tau_PP_grid exists
grid has 3000 finite values under L = 10 + i
endpoint-blind provenance exists
```

## Delta Route Opens Only If

```text
named hashable fiducial PP exists
endpoint-blind 3000-value delta_PP_tau exists
route is locked before ACT projection
```

## Failure Route Opens Only If

```text
both numeric routes are unavailable without endpoint leakage
failure statement identifies the missing theoretical blocker
```

## Claim Boundary

```text
route_decision_checklist_only_no_selected_route_no_grid_payload_no_tau_score_no_dark_sector_verdict
```
