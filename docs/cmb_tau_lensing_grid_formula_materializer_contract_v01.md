# CMB Tau Lensing Grid Formula Materializer Contract v01

**Doc class:** endpoint-blind Tau-grid production contract
**Status:** executable materialization path, not a score
**Canonical script:** `scripts/materialize_tau_lensing_grid_from_formula_spec.py`

This contract defines the first concrete route from a predeclared Tau formula to
the 3000-point ACT-compatible lensing grid required by the Paper 13 reduced
scoring adapter.

## Required Object

The materializer produces one of two staging grid objects:

```text
direct_tau_PP_grid:
  payload_staging/direct_tau_PP_grid/tau_lensing_response_pp_grid_v01.csv

delta_PP_tau_against_named_fiducial_PP:
  payload_staging/delta_PP_tau_against_named_fiducial_PP/tau_lensing_response_delta_pp_v01.csv
```

The output grid is always a two-column table:

```text
L, value
10, value_10
...
3009, value_3009
```

No score, likelihood, or dark-sector verdict is computed by this step.

## Formula Spec

The formula spec must be supplied before materialization and must not be marked
as a template. It must include:

- selected route;
- endpoint-blind statement;
- parameter policy;
- source chain;
- formula family;
- parameter values;
- normalization statement;
- known-limit statement;
- derivation script or formula.

The first supported parametric formula family is deliberately narrow:

```text
power_law_cutoff_response_v01

value(L) =
  amplitude * (L/L0)^tilt * exp(-(L/cutoff_L)^cutoff_power)
```

with an optional smooth turnover factor:

```text
(1 + (L/turnover_L)^2)^(-turnover_power/2)
```

This family is not a Tau Core physical derivation by itself. It is only an
adapter family for a Tau-derived response whose parameters have already been
fixed by endpoint-blind source evidence.

The materializer also supports a direct upstream-table family:

```text
tabulated_l_response_v01
```

This family reads an already-derived endpoint-blind Tau response table with
exactly 3000 rows and exact `L=10..3009` alignment. The required parameters are:

```text
source_table
l_column
value_column
source_table_sha256
```

This is the preferred handoff when another Tau-side derivation script has
already produced the numeric `tau_PP(L)` or `delta_PP_tau(L)` response. It still
does not certify physical correctness; it only preserves the upstream table
without manual rewriting.

## Claim Boundary

```text
formula_to_grid_materialization_only_no_score_no_dark_sector_verdict
```

The materializer may make a grid reproducible. It may not certify that the grid
is physically correct. Physical promotion still requires a Tau-side derivation
for `Phi_tau_eff(a,k)` or `delta_PP_tau(L)`, convention closure, and guarded
staging promotion.

## Next Required Scientific Step

Supply a non-template formula spec whose parameters are fixed from Tau-side
evidence before any ACT/Planck residual score readout. If that cannot be done,
the existing explicit failure route remains the correct scientific result.
