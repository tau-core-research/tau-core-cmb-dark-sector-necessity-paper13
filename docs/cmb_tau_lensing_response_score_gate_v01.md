# CMB Tau Lensing Response Score Gate v01

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** score gate blocked
**Canonical parent:** `docs/cmb_lensing_reduced_score_adapter_contract_v01.md`

This gate combines the current ACT reduced lensing adapter status with the
Tau-side payload acceptance audits.

## Gate Inputs

The adapter side is technically available as a reduced diagnostic contract:

```text
y_ACT shape (18)
C_ACT shape (18, 18)
B_ACT shape (18, 3000)
```

The Tau-side inputs are not accepted:

```text
Phi_tau_eff source payload: rejected, missing
T_tau_CMB transfer payload: rejected, missing
tau_PP_grid or delta_PP_tau payload: rejected, missing/template only
```

## Decision

```text
TAU_SCORE_BLOCKED_INPUTS_MISSING
```

The adapter sanity check may remain documented, but no Tau score may be run
until all required Tau-side payloads are submitted and accepted.

## What This Means

The project has crossed the data/adapter readiness threshold for a reduced ACT
lensing diagnostic. It has not crossed the theory-response threshold required
to evaluate Tau Core.

## Claim Boundary

```text
tau_lensing_score_gate_no_tau_score_no_dark_sector_verdict
```

The score unblock plan is tracked at:

```text
data/source_manifest/cmb_tau_lensing_score_unblock_plan_v01.csv
docs/cmb_tau_lensing_score_unblock_plan_v01.md
```
