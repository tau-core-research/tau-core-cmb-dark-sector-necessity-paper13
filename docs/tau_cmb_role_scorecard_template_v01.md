# Tau CMB Role Scorecard Template v01

**Doc class:** scorecard template
**Status:** template declared; all scores blocked, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_role_scorecard_template.py
```

Derived outputs:

```text
data/derived/tau_cmb_role_scorecard_template_v01.csv
data/derived/tau_cmb_role_scorecard_template_summary_v01.csv
```

This artifact converts the LCDM-role scoring rubric into the empty scorecard
that a future CMB scoring run must fill. It deliberately computes no scores.
Every row is marked:

```text
NOT_COMPUTED_INPUT_BLOCKED
```

The template also names the minimum artifact needed to unblock each role:

```text
acoustic benchmark
density-amplitude derivation
lensing-transfer benchmark
radiation-guard bound check
growth-transfer kernel
known-limit/failure map
```

This is the first place where Paper 13 has the shape of an actual scorecard,
but it remains a blocked template rather than a result.

## Claim Boundary

This artifact is a scorecard template only. It computes no scores, triggers no
hard failure, provides no CMB likelihood, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
