# Tau CMB Scorecard Readiness Audit v01

**Doc class:** scorecard readiness audit
**Status:** all scorecard rows blocked; no scores, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_scorecard_readiness_audit.py
```

Derived outputs:

```text
data/derived/tau_cmb_scorecard_readiness_audit_v01.csv
data/derived/tau_cmb_scorecard_readiness_audit_summary_v01.csv
```

This artifact audits whether the six CMB scorecard rows are ready to compute.
The answer in v01 is no:

```text
score_ready_rows = 0
score_blocked_rows = 6
```

The audit checks the density, acoustic, lensing, growth, radiation, and
known-limit inputs. Each exists as a scaffold, benchmark, guard, or map, but
none has been evaluated or specified enough to compute a score.

## Claim Boundary

This artifact is a readiness audit only. It computes no scores, supplies no CMB
likelihood, validates no Tau-response source, and permits no no-dark or
dark-sector verdict.
