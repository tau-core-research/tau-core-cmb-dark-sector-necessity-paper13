# Tau CMB Known-Limit And Dimension Audit v01

**Doc class:** known-limit and dimensional role audit
**Status:** slots declared; no formula-level dimensional proof and no LCDM role match

Script:

```text
scripts/build_tau_cmb_known_limit_and_dimension_audit.py
```

Derived outputs:

```text
data/derived/tau_cmb_known_limit_and_dimension_audit_v01.csv
data/derived/tau_cmb_known_limit_and_dimension_audit_summary_v01.csv
```

This audit checks the effective-source target from v01 at the level currently
available. The result is intentionally conservative: dimensional slots and
LCDM role obligations are named, but no component has an available formula, no
component has a proved dimensional consistency result, and no LCDM role is
matched.

The next useful step is therefore a minimal source-term candidate. That
candidate must either supply a checkable formula or record an explicit failure
mode for each CMB role.

## Claim Boundary

This artifact is an audit of target slots only. It provides no CMB source
equation, no dimensional proof, no Boltzmann solver, no CMB likelihood, no
Tau-response claim, and no dark-sector verdict.
