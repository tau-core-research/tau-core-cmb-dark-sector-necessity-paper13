# Tau CMB Known-Limit Failure Map v01

**Doc class:** known-limit / explicit-failure map
**Status:** map declared; all role decisions unresolved, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_known_limit_failure_map.py
```

Derived outputs:

```text
data/derived/tau_cmb_known_limit_failure_map_v01.csv
data/derived/tau_cmb_known_limit_failure_map_summary_v01.csv
```

This artifact defines the decision states that every CMB role must eventually
enter:

```text
REPRODUCE
APPROXIMATE
FAIL
UNRESOLVED
```

In v01 every row remains:

```text
UNRESOLVED_INPUT_MISSING
```

The value of this map is not that it proves a role. Its value is that it
prevents a hidden promotion from "we have a Tau-like source slot" to "Tau Core
has replaced the CMB dark-sector role." A later artifact must provide enough
evidence to move each row from unresolved into reproduce, approximate, or fail.

The next useful artifact is:

```text
tau_cmb_density_amplitude_derivation_v01
```

## Claim Boundary

This artifact declares comparison states only. It computes no scores, supplies
no CMB likelihood, declares no reproduction, declares no failure, validates no
Tau-response source, and permits no no-dark or dark-sector verdict.
