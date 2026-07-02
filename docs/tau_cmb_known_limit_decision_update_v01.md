# Tau CMB Known-Limit Decision Update v01

**Doc class:** known-limit decision update
**Status:** no role resolved; no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_known_limit_decision_update.py
```

Derived outputs:

```text
data/derived/tau_cmb_known_limit_decision_update_v01.csv
data/derived/tau_cmb_known_limit_decision_update_summary_v01.csv
```

This artifact updates the known-limit decision map after the focused v01
closure/evaluation gates:

```text
density amplitude closure
acoustic reduced evaluation
lensing-transfer reduced evaluation
growth-transfer kernel closure
radiation guard evaluation
```

No role is promoted to `REPRODUCE`, `APPROXIMATE`, or `FAIL`. This is deliberate:
the focused gates triggered no hard failures, but they also did not provide the
source, operator, amplitude, bound, or cross-role evidence needed to score a CMB
role.

Every row remains:

```text
UNRESOLVED_EVIDENCE_INSUFFICIENT
```

The known-limit decision update therefore keeps the scorecard blocked.

## Claim Boundary

This artifact updates decision states only. It computes no score, supplies no
CMB likelihood, declares no reproduction, declares no failure, validates no
Tau-response source, and permits no no-dark or dark-sector verdict.
