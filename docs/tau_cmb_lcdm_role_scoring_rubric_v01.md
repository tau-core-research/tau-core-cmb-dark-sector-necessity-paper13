# Tau CMB LCDM Role Scoring Rubric v01

**Doc class:** scoring rubric
**Status:** rubric declared; no scores computed, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_lcdm_role_scoring_rubric.py
```

Derived outputs:

```text
data/derived/tau_cmb_lcdm_role_scoring_rubric_v01.csv
data/derived/tau_cmb_lcdm_role_scoring_rubric_summary_v01.csv
```

This artifact defines how a future Tau CMB source candidate should be scored
against the roles normally carried by the standard non-baryonic sector. It is
not a scorecard and it computes no numerical result.

Each row has three possible score levels:

```text
0 = role absent, wrong, or hard-failed
1 = qualitative/partial role support, not enough for verdict
2 = quantitative compatibility under a stated benchmark or likelihood
```

The rubric covers six CMB role families:

```text
acoustic peak phase and height
Omega_c h^2 density inference
CMB lensing potential
damping-tail / radiation guard
growth-seed and transfer consistency
known-limit or explicit failure branch
```

All rows are currently marked not scoreable because the preceding artifacts
have not yet supplied the response operator, transfer kernel, known-limit map,
or likelihood benchmark.

## Claim Boundary

This artifact declares scoring rules only. It computes no scores, provides no
CMB likelihood, matches no LCDM role, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
